"""Validated preparation for a prespecified molecular analysis. No clinical data are bundled."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

def validate_metadata(metadata):
    required=['sample_id','patient_id','partition','fraction_percent','absolute_copies_ml','assay','phenotype']
    if not set(required)<=set(metadata) or metadata.empty or metadata[required].isna().any().any():
        raise ValueError('Complete matched metadata required: '+', '.join(required))
    if metadata[['sample_id','patient_id','partition','assay','phenotype']].astype(str).apply(lambda s:s.str.strip().eq('')).any().any():
        raise ValueError('Blank identifiers or labels are not valid metadata')
    if metadata.sample_id.duplicated().any():
        raise ValueError('Duplicate sample ID')
    if not metadata.partition.isin(['discovery','validation']).all() or set(metadata.partition)!= {'discovery','validation'}:
        raise ValueError('Both discovery and validation partitions required')
    if metadata.groupby('patient_id').partition.nunique().gt(1).any():
        raise ValueError('Patient leakage across partitions')
    if (metadata.fraction_percent.le(0)|metadata.fraction_percent.gt(100)|metadata.absolute_copies_ml.le(0)).any() or not np.isfinite(metadata[['fraction_percent','absolute_copies_ml']].to_numpy(dtype=float)).all():
        raise ValueError('Invalid paired measurements')

def module_scores(expression, metadata, modules):
    """Genes x samples, normalized gene-level expression. Training-only z scaling.

    Probe mapping and module provenance must be resolved upstream. Validation
    samples use discovery means and SDs; no outcome-guided feature selection.
    """
    validate_metadata(metadata)
    if expression.index.duplicated().any() or expression.columns.duplicated().any() or not expression.index.is_unique:
        raise ValueError('Unique gene IDs and sample columns required')
    if set(expression.columns)!=set(metadata.sample_id):
        raise ValueError('Expression and metadata sample IDs must match exactly')
    if not modules or any(not genes or len(genes)!=len(set(genes)) for genes in modules.values()):
        raise ValueError('Nonempty, unique prespecified module gene lists required')
    genes=sorted(set(g for values in modules.values() for g in values))
    if not set(genes)<=set(expression.index):
        raise ValueError('Missing module genes; do not silently change the module')
    x=expression.loc[genes].astype(float)
    if not np.isfinite(x.to_numpy()).all():
        raise ValueError('Nonfinite expression')
    discovery=metadata.loc[metadata.partition.eq('discovery'),'sample_id'].tolist()
    if len(discovery)<3:
        raise ValueError('At least three discovery observations needed to compute scaling; not a power criterion')
    mean=x[discovery].mean(axis=1); sd=x[discovery].std(axis=1,ddof=1)
    if sd.le(0).any():
        raise ValueError('Zero-variance module gene in discovery')
    z=x.sub(mean,axis=0).div(sd,axis=0)
    return pd.DataFrame({name:z.loc[values].mean(axis=0) for name,values in modules.items()}).loc[metadata.sample_id]

def freeze_specification(path):
    """Returns an integrity hash, not evidence of prospective registration."""
    raw=Path(path).read_bytes(); spec=json.loads(raw)
    for key in ['question','modules','gene_set_sources','threshold_source','covariates','primary_contrasts','validation_plan','multiplicity_plan']:
        if not spec.get(key):
            raise ValueError('Incomplete analysis specification: '+key)
    return hashlib.sha256(raw).hexdigest()

def association_estimates(scores, metadata, replicates=10000, seed=20261110):
    """Separate discovery/validation OLS with patient-cluster bootstrap intervals.

    Predictors: log fraction and log absolute. No third, algebraically dependent
    total-cfDNA predictor. Bonferroni percentile intervals span all reported
    module x predictor x partition coefficients. Descriptive/incompletely
    adjusted unless the locked study design explicitly justifies this model.
    No clinical-effect or causal interpretation is supported by this function.
    """
    validate_metadata(metadata)
    if scores.empty or set(scores.index)!=set(metadata.sample_id) or not scores.index.is_unique or not scores.columns.is_unique or not np.isfinite(scores.to_numpy(dtype=float)).all():
        raise ValueError('Complete, unique matched module scores required')
    if replicates < 1000:
        raise ValueError('At least 1000 bootstrap replicates required; inspect tail resolution')
    rng=np.random.default_rng(seed); rows=[]
    family=4*len(scores.columns)
    tail=.05/(2*family)
    if replicates*tail < 10:
        raise ValueError('Too few replicates for multiplicity-adjusted interval tails')
    for partition,group in metadata.groupby('partition',sort=True):
        ids=group.sample_id.tolist(); patients=group.patient_id.unique()
        if len(patients)<20:
            raise ValueError('Fewer than 20 patient clusters: this estimator is not enabled; obtain a precision assessment')
        x=np.column_stack([np.ones(len(group)),np.log(group.fraction_percent),np.log(group.absolute_copies_ml)])
        y=scores.loc[ids].to_numpy(dtype=float)
        if np.linalg.matrix_rank(x)<3:
            raise ValueError('Nonidentifiable fraction/absolute model')
        beta=np.linalg.lstsq(x,y,rcond=None)[0]
        blocks={p:np.flatnonzero(group.patient_id.to_numpy()==p) for p in patients}
        draws=[]
        for _ in range(replicates):
            ix=np.concatenate([blocks[p] for p in rng.choice(patients,len(patients),replace=True)])
            if np.linalg.matrix_rank(x[ix])==3:
                draws.append(np.linalg.lstsq(x[ix],y[ix],rcond=None)[0])
        if len(draws)<.95*replicates:
            raise ValueError('Too many rank-deficient resamples')
        limits=np.quantile(draws,[tail,1-tail],axis=0)
        for j,name in enumerate(scores.columns):
            for k,predictor in [(1,'log_fraction'),(2,'log_absolute')]:
                rows.append(dict(partition=partition,module=name,predictor=predictor,
                    estimate=float(beta[k,j]),lower=float(limits[0,k,j]),upper=float(limits[1,k,j]),
                    patient_clusters=len(patients),successful_resamples=len(draws),family_size=family,
                    interpretation='association; no causal or clinical validation claim'))
    return pd.DataFrame(rows)
