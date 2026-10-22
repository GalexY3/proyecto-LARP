from common import *
def run():
 rows=[];Q=finite_modes(3,1,2);std=.02;noise=.03;alpha=np.ones(5)/5
 for g in GSEEDS:
  jitter=np.random.default_rng(60223+g).normal(0,std,size=(24,128,3))
  for method in ['local','mhu','cvt']:
   p,l=geometry(g,method);p=np.asarray(p,dtype=float);t=2*np.pi*p@Q.T;d=np.exp(-4*np.pi**2*std**2*np.sum(Q**2,axis=1));K=((np.cos(t)*d)@np.cos(t).T+(np.sin(t)*d)@np.sin(t).T)/len(Q);np.fill_diagonal(K,1.)
   for rho in [0,1]:
    Rbar=K*((1-rho)*(l[:,None]==l[None,:])+rho)+noise**2*np.eye(len(l));nom=gls_weights(node_covariance(p,l,Q,rho,noise),l,alpha);aware=gls_weights(Rbar,l,alpha);expected={'nominal':float(nom@Rbar@nom),'aware':float(aware@Rbar@aware)};assert expected['aware']<=expected['nominal']*(1+1e-6)+1e-12
    obs=[]
    for j in jitter:
     R=node_covariance((p+j)%1,l,Q,rho,noise);oracle=gls_weights(R,l,alpha);v={k:float(w@R@w) for k,w in [('nominal',nom),('aware',aware),('recalibrated',oracle)]};assert v['recalibrated']<=min(v.values())*(1+1e-6)+1e-12;obs.append(v)
    rows.append({'geometry':g,'method':method,'rho':rho,'expected':expected,'observed_mean':{k:float(np.mean([r[k] for r in obs])) for k in obs[0]},'all_jitters':obs})
 return {'rows':rows,'summary':{f'rho{rho}':{m:{k:float(np.mean([r['observed_mean'][k] for r in rows if r['method']==m and r['rho']==rho])) for k in ['nominal','aware','recalibrated']} for m in ['local','mhu','cvt']} for rho in [0,1]}}
