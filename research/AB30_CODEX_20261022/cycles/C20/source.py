from common import *
def run():
 rows=[];Q=finite_modes(3,1,2)
 for g in GSEEDS:
  for method in METHODS:
   p,l=geometry(g,method);n=np.bincount(l);ranks=[]
   for c in range(5):
    t=2*np.pi*np.asarray(p,dtype=float)[l==c]@Q.T;ranks.append(int(np.linalg.matrix_rank(np.column_stack([np.ones(n[c]),np.cos(t),np.sin(t)]))))
   for rho in [0,1]:
    R=node_covariance(p,l,Q,rho,.03)
    for name,alpha in [('balanced',np.ones(5)/5),('counts',n/n.sum())]:
     bm=mean_weights(l,alpha);bg=gls_weights(R,l,alpha);vm=float(bm@R@bm);vg=float(bg@R@bg);assert vg<=vm*(1+1e-6)+1e-12
     rows.append({'geometry':g,'method':method,'rho':rho,'weights':name,'mean_risk':vm,'gls_risk':vg,'ranks':ranks,'columns':1+2*len(Q)})
 return {'rows':rows,'summary':{f'rho{rho}':{m:{k:float(np.mean([r[k] for r in rows if r['method']==m and r['rho']==rho and r['weights']=='balanced'])) for k in ['mean_risk','gls_risk']} for m in METHODS} for rho in [0,1]},'scope':'Native3D quadrature only; no trained neural network.'}
