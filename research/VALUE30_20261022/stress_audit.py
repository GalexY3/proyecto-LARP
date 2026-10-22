"""Post-hoc robustness of C29 fixed estimators; not independent confirmation."""
import json, numpy as np
from pathlib import Path
from experiment import load_data,W0,D,target,rmse
p=Path(__file__).parent
tr,dev,retina=load_data(True)
row=[json.loads(z) for z in (p/'ledger.jsonl').read_text().splitlines()][28]
y=target(dev,W0);R=[]
for z in row['comparison']['results']:
 ids=[np.array(k) for k in z['ids']];x=dev.reshape(len(dev),3,D)
 # masks COMMON across designs; dropout exactly 25% per type with minimum 1 sample.
 rng=np.random.default_rng(5566); drop=[]
 for r in range(100):
  masks=[np.sort(rng.choice(len(a),max(1,int(np.ceil(len(a)*.75))),replace=False)) for a in ids]
  pred=sum(W0[a]*x[:,a,ids[a][masks[a]]].mean(axis=1) for a in range(3))
  drop.append(float(np.mean((pred-y)**2)**.5))
 # noise on selected pixels independent per readout; analytical variance added.
 noise_sd=[]
 for sigma in (0.01,.03,.06):
  noise_var=sum(W0[a]**2/len(ids[a]) for a in range(3))*sigma**2
  noise_sd.append(float(np.sqrt(rmse(dev,ids,W0)**2+noise_var)))
 R.append({'method':z['method'],'clean':rmse(dev,ids,W0),'mean_25pct_dropout':float(np.mean(drop)),
           'noise_sigma_0p01_0p03_0p06_expected_rmse':noise_sd})
(p/'stress_audit.json').write_text(json.dumps({'status':'POSTHOC_AUDIT_NOT_CYCLE','results':R},indent=2))
print(json.dumps(R,indent=2))
