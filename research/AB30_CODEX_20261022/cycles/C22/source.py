from common import *
def run():
 rows=[];Q=finite_modes(3,1,2);alpha=np.ones(5)/5
 for g in GSEEDS:
  _,l=geometry(g,'mhu');rng=np.random.default_rng(60222+g);n=np.bincount(l);m=n//2;masks=[np.concatenate([rng.choice(np.where(l==c)[0],m[c],replace=False) for c in range(5)]) for _ in range(32)]
  for method in METHODS:
   p,l=geometry(g,method);R=node_covariance(p,l,Q,1,.03);full=gls_weights(R,l,alpha)
   for i,keep in enumerate(masks):
    pp=p[keep];ll=l[keep];RR=R[np.ix_(keep,keep)];H=np.eye(5)[ll];tic=time.perf_counter();refit=gls_weights(RR,ll,alpha);elapsed=time.perf_counter()-tic
    metrics={}
    for name,b in [('frozen_zero_fill',full[keep]),('adapted_mean',mean_weights(ll,alpha)),('adapted_gls',refit)]:
     bias=float(np.sum((H.T@b-alpha)**2));var=float(b@RR@b);metrics[name]={'bias2':bias,'variance':var,'mse':bias+var}
    rows.append({'geometry':g,'method':method,'mask':i,'kept_indices':keep.tolist(),'readouts':metrics,'refit_seconds':elapsed})
 return {'rows':rows,'summary':{m:{r:{k:float(np.mean([x['readouts'][r][k] for x in rows if x['method']==m])) for k in ['bias2','variance','mse']} for r in ['frozen_zero_fill','adapted_mean','adapted_gls']} for m in METHODS}}
