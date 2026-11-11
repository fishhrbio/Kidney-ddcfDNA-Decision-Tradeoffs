"""Bounded scenario analysis; no patient-level clinical claims or calibrated error probabilities."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
STATES = ['both_low', 'fraction_only_high', 'absolute_only_high', 'both_high']

def validate(f, d, tf, td, a, b):
    values = np.array([f, d, tf, td, a, b], dtype=float)
    if not np.isfinite(values).all() or not 0 < f <= 100 or not 0 < tf <= 100 or min(d, td) <= 0 or min(a, b) < 0:
        raise ValueError('Require finite positive concentrations/thresholds, fraction in (0,100], and nonnegative log-error bounds.')

def classify(fraction_percent, absolute, fraction_threshold, absolute_threshold):
    return (np.asarray(fraction_percent) >= fraction_threshold).astype(int) + 2*(np.asarray(absolute) >= absolute_threshold).astype(int)

def reachable_states(f, d, tf, td, a=0., b=0.):
    """Exact feasible states for F'=F exp(eF), T'=T exp(eT), D'=D exp(eF+eT).

    eF in [-a,a], eT in [-b,b]. F'<=100 is enforced. High includes equality;
    low excludes equality. Bounds describe a scenario, not an assay specification.
    """
    validate(f,d,tf,td,a,b)
    if a == b == 0:
        return [STATES[int(classify(f,d,tf,td))]]
    u,v = np.log(tf)-np.log(f), np.log(td)-np.log(d)
    lower,upper = -a, min(a,np.log(100/f))
    feasible=[]
    for state in range(4):
        fhigh,dhigh = bool(state & 1),bool(state & 2)
        lo = max(lower,u) if fhigh else lower
        hi = upper if fhigh else min(upper,u)
        # The upper endpoint of the low-fraction region is open at u.
        closed = fhigh or upper < u
        if lo > hi or (lo == hi and not closed):
            continue
        if dhigh:
            possible = hi+b >= v if closed else hi+b > v
        else:
            possible = lo-b < v
        if possible:
            feasible.append(STATES[state])
    return feasible

def simulate(f,d,tf,td,a,b,n=20000,seed=20261110):
    """Uniform draws over the allowed (eF,eT) rectangle; conditional scenario frequencies."""
    validate(f,d,tf,td,a,b)
    if not isinstance(n,int) or n < 1:
        raise ValueError('n must be a positive integer')
    rng=np.random.default_rng(seed)
    ef=rng.uniform(-a,min(a,np.log(100/f)),n)
    et=rng.uniform(-b,b,n)
    states=classify(f*np.exp(ef),d*np.exp(ef+et),tf,td)
    return {name:float(np.mean(states==i)) for i,name in enumerate(STATES)}

def audit_samples(frame,tf,td,a,b):
    required={'sample_id','fraction_percent','absolute_copies_ml'}
    if not required <= set(frame) or frame.empty or frame[list(required)].isna().any().any() or frame.sample_id.duplicated().any():
        raise ValueError('Require nonempty, unique sample IDs and complete paired measurements')
    rows=[]
    for r in frame.itertuples():
        reachable=reachable_states(r.fraction_percent,r.absolute_copies_ml,tf,td,a,b)
        baseline=STATES[int(classify(r.fraction_percent,r.absolute_copies_ml,tf,td))]
        rows.append(dict(sample_id=r.sample_id,baseline=baseline,reachable=';'.join(reachable),stable=len(reachable)==1))
    return pd.DataFrame(rows)

def independent_envelope_states(f,d,tf,td,a,b):
    """Comparator: same marginal log bounds, but ignores shared-error coupling."""
    validate(f,d,tf,td,a,b)
    fs=[False]*int(np.log(f)-a<np.log(tf))+[True]*int(min(np.log(100),np.log(f)+a)>=np.log(tf))
    ds=[False]*int(np.log(d)-(a+b)<np.log(td))+[True]*int(np.log(d)+a+b>=np.log(td))
    return [STATES[int(x)+2*int(y)] for x in fs for y in ds]

def run_demo(root=ROOT):
    """A fixed design grid, explicitly not simulated patients or a clinical cohort."""
    rows=[]
    for fr in [.5,.8,1.,1.2,2.]:
        for dr in [.5,.8,1.,1.2,2.]:
            for bound in [0.,.05,.1,.2]:
                states=reachable_states(fr,dr,1.,1.,bound,bound)
                independent=independent_envelope_states(fr,dr,1.,1.,bound,bound)
                rows.append(dict(fraction_threshold_ratio=fr,absolute_threshold_ratio=dr,
                                 log_bound=bound,stable=len(states)==1,reachable=';'.join(states),
                                 independent_reachable=';'.join(independent),extra_states_ignoring_coupling=len(set(independent)-set(states))))
    out=root/'results'; out.mkdir(exist_ok=True)
    df=pd.DataFrame(rows); df.to_csv(out/'synthetic_stability_grid.csv',index=False)
    summary={'evidence':'hypothetical design grid, not patient observations',
             'error_model':'bounded additive errors on log fraction and log total cfDNA; calculated D shares fraction error',
             'high_boundary':'greater than or equal; illustrative convention, not asserted for all assays',
             'bounds_are':'illustrative natural-log half-widths, not validated assay CVs',
             'grid_points':len(df),'stable_counts_by_bound':{str(k):int(g.stable.sum()) for k,g in df.groupby('log_bound')},
             'molecular_analysis_status':'not run: matched clinical and molecular dataset unavailable'}
    (out/'stability_summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    (root/'docs/stability-results.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(10,4.8))
    g=df[df.log_bound.eq(.2)]
    for ax,column,title,vmax in [(axes[0],'stable','Certified stable state',1),(axes[1],'extra_states_ignoring_coupling','Extra states in independent envelope',3)]:
        table=g.pivot(index='absolute_threshold_ratio',columns='fraction_threshold_ratio',values=column).astype(float)
        im=ax.imshow(table.values,origin='lower',vmin=0,vmax=vmax,cmap='Blues',aspect='auto')
        ax.set(xticks=range(5),xticklabels=table.columns,yticks=range(5),yticklabels=table.index,xlabel='Fraction / threshold',ylabel='Absolute / threshold',title=title)
        for i in range(5):
            for j in range(5):ax.text(j,i,str(int(table.iloc[i,j])),ha='center',va='center',color='white' if table.iloc[i,j]>vmax/2 else '#172f3e')
    fig.suptitle('Synthetic design grid: coupled log-error bounds ±0.2',fontsize=13)
    fig.text(.02,.015,'Illustrative scenarios only; no patient observations, assay calibration or clinical performance estimates.',fontsize=9)
    fig.tight_layout(rect=(0,.055,1,.93));fig.savefig(root/'figures/03_stability_scenarios.png',dpi=160)
    fig.savefig(root/'docs/stability-grid.png',dpi=160);plt.close(fig)
    print(json.dumps(summary,indent=2))
    return df

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path)
    parser.add_argument('--fraction-threshold',type=float,default=1.)
    parser.add_argument('--absolute-threshold',type=float,default=1.)
    parser.add_argument('--fraction-log-bound',type=float,default=.1)
    parser.add_argument('--total-log-bound',type=float,default=.1)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.input:
        if args.output is None or args.fraction_threshold==1. and args.absolute_threshold==1.:
            parser.error('Provide --output and explicitly chosen assay thresholds; illustrative 1/1 defaults are for demo only.')
        result=audit_samples(pd.read_csv(args.input),args.fraction_threshold,args.absolute_threshold,args.fraction_log_bound,args.total_log_bound)
        result.to_csv(args.output,index=False)
    else:
        run_demo()
