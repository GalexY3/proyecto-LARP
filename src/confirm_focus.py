#!/usr/bin/env python3
"""BR30 one-claim confirmation: prereg/SELECCION_CONFIRMACION_BR30.md."""
import csv,json,sys,time
from pathlib import Path
import numpy as np
from scipy import stats
from run_br30 import geometry,ds,infer
out=Path(__file__).resolve().parents[1]/'data';out.mkdir(exist_ok=True)
geo={g:geometry(g) for g in ('local','stratified','random','mhu')}
rows=[];start=time.time()
for seed in range(901,921):
    q,a,m,y=ds(seed,512,1)
    for g,(p,t) in geo.items():
        yh=infer(p,t,q,a,m,k=24,band=.11)
        rows.append({'seed':seed,'geometry':g,'mse':float(np.mean((yh-y)**2))})
    print(seed,'done',flush=True)
with (out/'confirm_focus_raw.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
v={(r['seed'],r['geometry']):r['mse'] for r in rows}
diff=np.array([v[(s,'local')]-v[(s,'stratified')] for s in range(901,921)])
ci=stats.t.interval(.95,len(diff)-1,loc=float(diff.mean()),scale=float(stats.sem(diff)))
result={'estimand':'MSE_LOCAL-MSE_STRATIFIED at frequency 1, 24 nearest fixed, Gaussian bandwidth 0.11','seeds':list(range(901,921)),'n_worlds':20,'queries_per_world':512,'n_unique_geometries_per_algorithm':1,'means':{g:float(np.mean([v[(s,g)] for s in range(901,921)])) for g in geo},'diff_mean':float(diff.mean()),'diff_sd':float(diff.std(ddof=1)),'ci_95_two_sided_t':list(map(float,ci)),'t_statistic':float(stats.ttest_1samp(diff,0).statistic),'p_two_sided':float(stats.ttest_1samp(diff,0).pvalue),'within_model_confirmatory':bool(ci[1]<0),'external_replication':False,'elapsed_seconds':time.time()-start}
(out/'confirm_focus_summary.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
