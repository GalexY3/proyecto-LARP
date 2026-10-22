from common import *
def run():
 rows=[]
 for g in GSEEDS:
  for method in METHODS:
   p,l=geometry(g,method);n=np.bincount(l);H=np.eye(5)[l]
   for rho in [0,1]:
    A=node_covariance(p,l,finite_modes(2,1,2),rho);B=node_covariance(p,l,finite_modes(2,4,9),rho);noise=.03
    assert np.max(abs(np.diag(A)-np.diag(B)))<1e-12
    for name,alpha in [('balanced',np.ones(5)/5),('counts',n/n.sum())]:
     wm=mean_weights(l,alpha);wl=gls_weights(A+noise**2*np.eye(len(l)),l,alpha)
     for eps in [.1,1.]:
      R=(1-eps)*A+eps*B+noise**2*np.eye(len(l));wo=gls_weights(R,l,alpha);ws=.5*(wl+wm)
      risk={k:float(w@R@w) for k,w in [('mean',wm),('wrong_gls',wl),('shrink',ws),('oracle',wo)]}
      assert risk['oracle']<=min(risk.values())*(1+1e-6)+1e-12
      rows.append({'geometry':g,'method':method,'rho':rho,'weights':name,'epsilon':eps,'risk':risk,'wrong_to_mean':risk['wrong_gls']/risk['mean'],'wrong_to_oracle':risk['wrong_gls']/risk['oracle']})
 summary={}
 for rho in [0,1]:
  for eps in [.1,1.]:
   summary[f'rho{rho}_shift{eps}']={m:{k:float(np.mean([r['risk'][k] for r in rows if r['method']==m and r['rho']==rho and r['epsilon']==eps and r['weights']=='balanced'])) for k in ['mean','wrong_gls','shrink','oracle']} for m in ['local','mhu','cvt','random']}
 return {'rows':rows,'summary':summary,'wrong_worse_than_mean':sum(r['wrong_to_mean']>1 for r in rows)}
