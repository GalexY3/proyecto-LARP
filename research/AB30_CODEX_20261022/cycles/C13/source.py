from common import *
def run():
 rows=[]
 for g in GSEEDS:
  for method in METHODS:
   p,l=geometry(g,method);a,u=amplitudes(p[:,:2],l,finite_modes(2,1,2));C=(a@a.conj().T/len(u)).real;n=np.bincount(l)
   for name,alpha in [('balanced',np.ones(5)/5),('counts',n/n.sum())]:
    w=alpha/np.sqrt(n);rs={}
    for rho in [-.2,0,.5,1]:
     S=(1-rho)*np.eye(5)+rho*np.ones((5,5));assert np.linalg.eigvalsh(S)[0]>-1e-12
     risk=float(w@(C*S)@w);assert risk>=-1e-12;rs[str(rho)]=risk
    rows.append({'geometry':g,'method':method,'weights':name,'risk':rs})
 summary={}
 for name in ['balanced','counts']:
  vals={m:{r:float(np.mean([x['risk'][r] for x in rows if x['method']==m and x['weights']==name])) for r in ['-0.2','0','0.5','1']} for m in METHODS}
  d0=vals['mhu']['0']-vals['cvt']['0'];d1=vals['mhu']['1']-vals['cvt']['1'];cross=float(-d0/(d1-d0)) if abs(d1-d0)>1e-15 else None
  summary[name]={'mean_risk':vals,'mhu_cvt_rho_cross':cross if cross is not None and -.25<=cross<=1 else None}
 return {'rows':rows,'summary':summary,'claim':'Exact within finite Gaussian Fourier model, fixed mean readout; not dominance over competent learned estimators.'}
