from common import *
def run():
 rng=np.random.default_rng(60214);W=4096;Q=finite_modes(2,1,2);mu=rng.normal(size=(W,5));z=rng.normal(size=(2,W,5,len(Q)));rows=[]
 for rho in [0,1]:
  S=(1-rho)*np.eye(5)+rho*np.ones((5,5));ev,V=np.linalg.eigh(S);L=(V*np.sqrt(np.maximum(ev,0)))@V.T
  uv=np.einsum('awc q,dc->awd q',z,L) if False else np.einsum('awcq,dc->awdq',z,L)
  for g in GSEEDS:
   for method in METHODS:
    p,l=geometry(g,method);t=2*np.pi*p[:,:2]@Q.T
    Y=mu[:,l]+np.einsum('wnq,nq->wn',uv[0][:,l,:],np.cos(t))/np.sqrt(len(Q))+np.einsum('wnq,nq->wn',uv[1][:,l,:],np.sin(t))/np.sqrt(len(Q))
    R=node_covariance(p,l,Q,rho)
    for name,alpha in [('balanced',np.ones(5)/5),('counts',np.bincount(l)/len(l))]:
     truth=mu@alpha;b=mean_weights(l,alpha);v=float(b@R@b);e=Y@b-truth;mc=float(np.mean(e**2));bw,ranks=band_weights(p,l,Q,alpha);oe=Y@bw-truth
     rows.append({'geometry':g,'method':method,'rho':rho,'weights':name,'theory':v,'mean_mse':mc,'mc_z':float((mc/v-1)*np.sqrt(W/2)),'band_mse':float(np.mean(oe**2)),'rank':ranks,'band_weight_norm':float(np.linalg.norm(bw)),'zero_estimator_mse':float(np.mean(truth**2))})
 return {'rows':rows,'summary':{'max_abs_mc_z':max(abs(r['mc_z']) for r in rows),'max_band_mse':max(r['band_mse'] for r in rows),'minimum_type_design_rank':min(min(r['rank']) for r in rows),'mean_weight_norms':{m:float(np.mean([r['band_weight_norm'] for r in rows if r['method']==m])) for m in METHODS},'worlds':W,'world_seed':60214}}
