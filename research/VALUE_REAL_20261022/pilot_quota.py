"""Matching quota + same pilot n control on real RGB fields; exploratory comparisons.
All methods see the same training patches; COSI is a spectral proxy, direct is empirical fit.
"""
import json
from pathlib import Path
import numpy as np
import real_rgb_sensors as m
import quota_ablations as q
import direct_quota_control as d
ROOT=Path(__file__).resolve().parent
QUOTA=[6,16,2]

def main():
 train,_,ext=m.get_data();rr=[]
 for n in [12,28,88,300,1800]:
  for ps in range(5):
   rng=np.random.default_rng(ps+8800)
   ix=np.concatenate([rng.choice(np.arange(a*450,(a+1)*450),n//4,replace=False) for a in range(4)]) if n<1800 else np.arange(1800)
   tr=train[ix];C=m.covariance_train(tr);Cdiag=np.stack([np.diag(np.real(np.diag(c))) for c in C]);Cs=.5*C+.5*Cdiag
   for seed in range(3):
    for method in ['COSI-SHRINK','POWER-DIAG','SOBOL','DIRECT-EMPIRICAL']:
     if method=='COSI-SHRINK':L=q.optimized_layout(QUOTA,Cs,seed+9100)
     if method=='POWER-DIAG':L=q.optimized_layout(QUOTA,Cdiag,seed+9100)
     if method=='SOBOL':L=q.init_ids(QUOTA,seed+9100)
     if method=='DIRECT-EMPIRICAL':L=d.direct(tr,QUOTA,seed+9100,passes=5)
     rr.append({'pilot':n,'pilot_seed':ps,'layout_seed':seed,'method':method,'train':q.eval(tr,L),'rocket':q.eval(ext['rocket'],L),'hubble':q.eval(ext['hubble_deep_field'],L)})
  print('done',n,flush=True)
 out={}
 for n in [12,28,88,300,1800]:
  out[n]={}
  for method in ['COSI-SHRINK','POWER-DIAG','SOBOL','DIRECT-EMPIRICAL']:
   a=[r for r in rr if r['pilot']==n and r['method']==method]
   out[n][method]={k:float(np.mean([r[k] for r in a])) for k in ['train','rocket','hubble']}
 (ROOT/'pilot_quota_results.json').write_text(json.dumps({'scope':'Exploratory, quota [6,16,2] chosen after inspecting previous runs, not new confirmation','summary':out,'rows':rr},indent=2))
 print(json.dumps(out,indent=2),flush=True)
if __name__=='__main__':main()
