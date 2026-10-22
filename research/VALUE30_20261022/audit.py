"""Post hoc adversarial audit; NOT cycle 31, NO untouched holdout remaining.
Correctly distinguishes fixed quadrature readout vs trained GP/Ridge readout.
"""
import json, numpy as np, itertools, time
from pathlib import Path
from experiment import load_data,target,W0,SIDE,D,gp_greedy,spectral_layout,rmse,learned_rmse
from sklearn.linear_model import Ridge
P=Path(__file__).parent
train,dev,retina=load_data(with_heldout=True)
cycles=[json.loads(l) for l in (P/'ledger.jsonl').read_text().splitlines()]

# Re-evaluate the same frozen layouts with the same trained linear readout.
orig=[]
for row in cycles[:29]:
 p=row['params'];w=np.asarray(p['weights']);rng=np.random.default_rng((7000+row['cycle'])*19+19)
 samp=train[rng.choice(len(train),p['pilot'],replace=False)]
 for result in row['comparison']['results']:
  ids=[np.array(arr) for arr in result['ids']]
  assert abs(learned_rmse(samp,dev,ids,w,.25)-result['development_ridge_RMSE'])<1e-10
  orig.append({'cycle':row['cycle'],'method':result['method'],'ridge_RMSE':result['development_ridge_RMSE'],'fixed_RMSE':result['development_fixed_RMSE']})

# GP on full 576 candidates / channel instead of previous restricted 72.
# Evaluation with *learned* readout as intended. This is a stronger candidate baseline.
# Candidate pixels selectable anywhere, true GP posterior readout from pilot used at inference.
def gp_full(pilot,w,q,shrink=.35):
 x=pilot.reshape(len(pilot),3,D)
 xflat=x.reshape(len(x),3*D)
 xc=xflat-xflat.mean(axis=0);y=target(pilot,w);yc=y-y.mean()
 K=(xc.T@xc)/len(pilot);c=(xc.T@yc)/len(pilot)
 diag=np.diag(K).copy();K*=(1-shrink);K.flat[::len(diag)+1]+=shrink*diag + diag*.015 + 1e-5
 rem=np.array(q);chosen=[]
 for j in range(sum(q)):
  # ranks for each channel group; K updated rank-one
  valid=np.repeat(rem>0,D)
  if chosen:valid[chosen]=False
  scores=c**2/(np.diag(K)+1e-9);scores[~valid]=-np.inf
  best=int(np.argmax(scores));chosen.append(best);rem[best//D]-=1
  col=K[:,best].copy(); denom=K[best,best]
  if denom>1e-10:
   c-=col*(c[best]/denom)
   K-=np.outer(col,col)/denom
 # returned selection coordinates
 return [np.array([z%D for z in chosen if z//D==a],int) for a in range(3)]

def gp_readout(pilot,tst,ids,w,lam=.015):
 px=np.column_stack([pilot.reshape(len(pilot),3,D)[:,a,ids[a]] for a in range(3)])
 tx=np.column_stack([tst.reshape(len(tst),3,D)[:,a,ids[a]] for a in range(3)])
 pm=px.mean(0);xc=px-pm;y=target(pilot,w);ym=y.mean()
 K=xc.T@xc/len(pilot);c=xc.T@(y-ym)/len(pilot)
 diag=np.diag(K).copy();K.flat[::K.shape[0]+1]+=lam*np.maximum(diag,1e-5)+1e-5
 beta=np.linalg.solve(K,c)
 return float(np.sqrt(np.mean((ym+(tx-pm)@beta-target(tst,w))**2)))

# One small-pilot and one larger-pilot full pixel GP placement. Both are post-hoc audits.
more=[]
for pilotn in [28,180]:
 r=np.random.default_rng(4321+pilotn)
 sample=train[r.choice(len(train),pilotn,replace=False)]
 q=[6,16,2];w=W0
 for method in ['GP_FULL','COSI_SHRINK','POWER_DIAG']:
  t=time.time()
  if method=='GP_FULL':ids=gp_full(sample,w,q)
  else:ids,_=spectral_layout(sample,w,q,seed=803+pilotn,variant=method)
  more.append({'pilot_n':pilotn,'method':method,'layout_seconds':time.time()-t,
               'development_fixed':rmse(dev,ids,w),
               'development_ridge':learned_rmse(sample,dev,ids,w,.25),
               'development_GP_readout':gp_readout(sample,dev,ids,w),
               'retina_posthoc_fixed':rmse(retina,ids,w),
               'retina_posthoc_GP_readout':gp_readout(sample,retina,ids,w),
               'count':sum(len(i) for i in ids)})

from collections import defaultdict
summary=defaultdict(list)
for z in orig:summary[z['method']].append(z['ridge_RMSE'])
report={'status':'ADVERSARIAL_POSTHOC_NOT_31ST_CYCLE','total_original_records':len(orig),
        'mean_development_ridge_unpaired':{k:float(np.mean(v)) for k,v in summary.items()},
        'new_full_candidate_gp_controls':more,
        'limits':['GP_FULL covariance has 1728 candidate inputs; matches cost/reading, not construction CPU','New GP readout evaluated after revealing retina in original C30: contamination; report posthoc','Only one new external image: cannot infer transfer']}
(P/'audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
