from common import *
def run():
 rows=[];viol=[]
 for g in GSEEDS:
  for method in METHODS:
   p,l=geometry(g,method);Q=finite_modes(2,1,2);n=np.bincount(l);H=np.eye(5)[l]
   for rho in [0,1]:
    for noise in [.01,.1,.3]:
     R=node_covariance(p,l,Q,rho,noise)
     for wn,alpha in [('balanced',np.ones(5)/5),('counts',n/n.sum())]:
      b=mean_weights(l,alpha);bo,ranks=band_weights(p,l,Q,alpha);bg=gls_weights(R,l,alpha)
      v={k:float(w@R@w) for k,w in [('mean',b),('band',bo),('gls',bg)]};floor=float(noise**2*np.sum(alpha**2/n));err=float(max(abs(H.T@bg-alpha)))
      assert err<1e-8 and v['gls']<=min(v['mean'],v['band'])*(1+1e-6)+1e-12
      assert v['gls']>=floor*(1-1e-6)
      rows.append({'geometry':g,'method':method,'rho':rho,'noise':noise,'weights':wn,'risk':v,'noise_bound':floor,'gls_excess_over_bound':v['gls']/floor-1,'unbiased_residual':err})
 summary={}
 for rho in [0,1]:
  for noise in [.01,.1,.3]:
   summary[f'rho{rho}_sigma{noise}']={m:{'balanced_gls':float(np.mean([r['risk']['gls'] for r in rows if r['method']==m and r['rho']==rho and r['noise']==noise and r['weights']=='balanced'])),'counts_gls':float(np.mean([r['risk']['gls'] for r in rows if r['method']==m and r['rho']==rho and r['noise']==noise and r['weights']=='counts']))} for m in ['local','mhu','cvt','random']}
 return {'rows':rows,'summary':summary}
