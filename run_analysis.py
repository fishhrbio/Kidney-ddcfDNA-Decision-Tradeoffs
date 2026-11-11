"""Published aggregate reanalysis of Nie et al. 2025, DOI 10.3390/diagnostics15030237."""
from pathlib import Path
from decimal import Decimal
import hashlib, json, platform
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
ROOT=Path(__file__).resolve().parent
RULES=['Fraction alone','Absolute alone','Either positive (OR)','Both positive (AND)']
METRICS=['sensitivity','specificity','ppv','npv']

def unique_count(rate,n,tolerance='0.005'):
    """Enumerate all integer numerators compatible with rounded percentages; fail closed."""
    if n<1 or int(n)!=n: raise ValueError('Invalid denominator')
    target,tol=Decimal(str(rate)),Decimal(str(tolerance))
    if not 0<=target<=100 or tol<0: raise ValueError('Invalid rate or tolerance')
    matches=[k for k in range(int(n)+1) if abs(Decimal(100)*k/int(n)-target)<=tol]
    if len(matches)!=1: raise ValueError(f'Nonunique/impossible count: {matches}')
    return matches[0]

def load_inputs(root=ROOT):
    for entry in json.loads((root/'INPUT_MANIFEST.json').read_text())['files']:
        if hashlib.sha256((root/entry['path']).read_bytes()).hexdigest()!=entry['sha256']:
            raise ValueError('Input checksum mismatch: '+entry['path'])
    d=pd.read_csv(root/'data/published_summary/diagnostic_performance.csv')
    p=pd.read_csv(root/'data/published_summary/biopsy_phenotype_summaries.csv')
    if d.rule.tolist()!=RULES or len(p)!=6: raise ValueError('Unexpected source rows')
    if d.duplicated('rule').any() or p.duplicated('phenotype').any(): raise ValueError('Duplicate key')
    if d[[m+'_percent' for m in METRICS]+['n_rejection','n_nonrejection']].isna().any().any():
        raise ValueError('Missing rate or denominator')
    if not d.n_rejection.eq(15).all() or not d.n_nonrejection.eq(35).all(): raise ValueError('Wrong denominators')
    if p.n.sum()!=50 or p.iloc[:2].n.sum()!=15: raise ValueError('Phenotype total mismatch')
    missing={(r.phenotype,c) for _,r in p.iterrows() for c in p.columns if pd.isna(r[c])}
    expected={('TCMR',c) for c in ['fraction_q1_percent','fraction_q3_percent','absolute_q1_copies_ml','absolute_q3_copies_ml']}
    if missing!=expected: raise ValueError('Unexpected phenotype missingness')
    qc=dict(input_rule_rows=4,included_rule_rows=4,input_phenotype_rows=6,included_phenotype_rows=6,
        excluded_rows=0,duplicate_rule_keys=int(d.duplicated('rule').sum()),duplicate_phenotype_keys=int(p.duplicated('phenotype').sum()),
        missing_diagnostic_cells=int(d.isna().sum().sum()),missing_phenotype_cells=int(p.isna().sum().sum()),
        missingness='Two inapplicable cutoffs; four unreported TCMR quartiles (n=1). No imputation.',
        recipients=50,rejection=15,comparator=35,rejection_prevalence_percent=30,
        unit='One rule or phenotype summary, never a patient',patient_level_QC='Not assessable',source_hashes_verified=True)
    return d,p,qc

def validate_rule_logic(d):
    indexed=d.set_index('rule')
    for c in ['TP','FP']:
        f,a,e,b=indexed.loc[RULES,c].tolist()
        if e!=f+a-b or not 0<=b<=min(f,a) or e<max(f,a): raise ValueError('Combined rule inconsistency')

def reconstruct(d,tolerance='0.005'):
    rows,checks=[],[]
    for _,r in d.iterrows():
        n,m=int(r.n_rejection),int(r.n_nonrejection)
        tp,tn=unique_count(r.sensitivity_percent,n,tolerance),unique_count(r.specificity_percent,m,tolerance)
        fn,fp=n-tp,m-tn
        rates=dict(sensitivity=100*tp/n,specificity=100*tn/m,ppv=100*tp/(tp+fp),npv=100*tn/(tn+fn))
        row=dict(rule=r.rule,TP=tp,FN=fn,TN=tn,FP=fp,n_rejection=n,n_nonrejection=m,provenance='reconstructed from published summaries',source_doi='10.3390/diagnostics15030237',source_table='Table 3; denominators Table 1')
        for metric,value in rates.items():
            reported=float(r[metric+'_percent']); delta=value-reported; match=abs(delta)<=0.005+1e-10
            checks.append(dict(rule=r.rule,metric=metric,reported_percent=reported,recalculated_percent=value,difference_percentage_points=delta,matches_rounding=match))
            if not match: raise ValueError(f'{metric} discrepancy for {r.rule}')
            row[metric+'_percent']=value
        rows.append(row)
    derived=pd.DataFrame(rows); validate_rule_logic(derived)
    return derived,pd.DataFrame(checks)

def rounding_sensitivity(d):
    baseline,_=reconstruct(d); rows=[]
    for tolerance in ['0.005','0.01','0.05']:
        candidate,_=reconstruct(d,tolerance)
        stable=candidate[['TP','FN','TN','FP']].equals(baseline[['TP','FN','TN','FP']])
        if not stable: raise ValueError('Rounding sensitivity changed counts')
        rows.append(dict(tolerance_percentage_points=float(tolerance),unique_counts_unchanged=stable))
    return pd.DataFrame(rows)

def export_figures(d,root=ROOT):
    out=root/'figures'; out.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.spines.left':False,'axes.axisbelow':True,'savefig.facecolor':'white'})
    labels=['Fraction\nalone','Absolute\nalone','Either positive\nOR','Both positive\nAND']; x=np.arange(4)
    fig,ax=plt.subplots(figsize=(10,6))
    for shift,key,color,label in [(-.19,'sensitivity','#176b87','Sensitivity: rejection n=15'),(.19,'specificity','#d07a29','Specificity: comparator n=35')]:
        bars=ax.bar(x+shift,d[key+'_percent'],width=.34,color=color,label=label)
        ax.bar_label(bars,labels=[f'{v:.2f}%' for v in d[key+'_percent']],padding=4,fontsize=10)
    ax.set(xticks=x,xticklabels=labels,ylim=(0,116),yticks=np.arange(0,101,20),ylabel='Diagnostic rate (%)',title='Combined positivity changes the tradeoff')
    ax.grid(axis='y',alpha=.18); ax.legend(loc='upper center',bbox_to_anchor=(.5,-.13),ncol=2,frameon=False,fontsize=10)
    fig.text(.075,.025,'Nie et al. (2025), Table 3. Same 50-recipient cohort. Cutoffs: 1.08%; 32 copies/mL.\nRates reproduced from published summaries; cutoffs selected in this cohort. No external validation.',fontsize=9,color='#44515b')
    fig.subplots_adjust(bottom=.26,top=.88,left=.09,right=.98); fig.savefig(out/'01_diagnostic_performance.png',dpi=180); plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11,5.7))
    for ax,c,title,color,denominator,upper in [(axes[0],'FN','Missed rejections','#176b87',15,5),(axes[1],'FP','False positives','#d07a29',35,14)]:
        bars=ax.bar(x,d[c],color=color,width=.62); ax.bar_label(bars,labels=[f'{v}/{denominator}' for v in d[c]],padding=5)
        ax.set(xticks=x,xticklabels=labels,ylim=(0,upper),title=title,ylabel=f'Recipients (out of {denominator})')
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True)); ax.grid(axis='y',alpha=.18); ax.tick_params(axis='x',labelsize=9)
    fig.suptitle('AND avoids 2 false positives but misses 3 additional rejections',fontsize=13)
    fig.text(.075,.035,'Relative to fraction alone, in this cohort only. Counts reconstructed from published summaries.\nPanels have different denominators and scales; they do not assign equal clinical costs.',fontsize=9,color='#44515b')
    fig.subplots_adjust(bottom=.22,top=.83,left=.075,right=.98,wspace=.24); fig.savefig(out/'02_diagnostic_errors.png',dpi=180); plt.close(fig)

def save_results(d,checks,qc,sensitivity,root=ROOT):
    out=root/'data/processed'; out.mkdir(parents=True,exist_ok=True)
    d.to_csv(out/'reconstructed_counts.csv',index=False,float_format='%.8f')
    checks.to_csv(out/'rate_checks.csv',index=False,float_format='%.8f')
    sensitivity.to_csv(out/'rounding_sensitivity.csv',index=False)
    (out/'quality_report.json').write_text(json.dumps(qc,indent=2)+'\n')
    env=dict(python=platform.python_version(),pandas=pd.__version__,numpy=np.__version__,matplotlib=matplotlib.__version__)
    (out/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
    docs=root/'docs'; docs.mkdir(exist_ok=True)
    (docs/'results.js').write_text('window.RESULTS = '+d.to_json(orient='records',indent=2)+';\n')

def main(root=ROOT):
    source,phenotype,qc=load_inputs(root); d,checks=reconstruct(source); sensitivity=rounding_sensitivity(source)
    export_figures(d,root); save_results(d,checks,qc,sensitivity,root)
    print(d[['rule','TP','FN','TN','FP']].to_string(index=False))
    print(f'\n{len(checks)}/16 rate checks pass. All 3 rounding tolerances agree.')
    print('Aggregate reconstruction only; not independent clinical validation.')
    return d

if __name__=='__main__': main()
