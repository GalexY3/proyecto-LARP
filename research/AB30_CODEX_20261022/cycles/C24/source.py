from common import *
def run():
 rows=[];shifts=np.array([[0,0,0],[.25,0,0],[0,.25,0],[.37,.19,.11]]);alpha=np.ones(5)/5;Q=finite_modes(3,1,9);maxerr=0.
 for g in GSEEDS:
  for method in METHODS:
   p,l=geometry(g,method);p=np.asarray(p,float);S0=np.array(finite_spectrum(p,l,Q));mask=l[:,None]==l[None,:]
   for i,s in enumerate(shifts):
    pp=(p+s)%1;maxerr=max(maxerr,float(np.max(abs(np.array(finite_spectrum(pp,l,Q))-S0))));T=pp-.5;R=(T@T.T)*mask+.03**2*np.eye(len(p));bm=mean_weights(l,alpha);bg=gls_weights(R,l,alpha)
    rows.append({'geometry':g,'method':method,'phase':i,'shift':s.tolist(),'mean_risk':float(bm@R@bm),'gls_risk':float(bg@R@bg)})
 summary={}
 for m in METHODS:
  ratios=[]
  for g in GSEEDS:
   rr=[r['mean_risk'] for r in rows if r['method']==m and r['geometry']==g];ratios.append(max(rr)/min(rr))
  summary[m]={'mean_phase_max_min_ratio':float(np.mean(ratios)),'phase_ratios':ratios,'average_mean_risk':float(np.mean([r['mean_risk'] for r in rows if r['method']==m])),'average_gls_risk':float(np.mean([r['gls_risk'] for r in rows if r['method']==m]))}
 assert maxerr<1e-10
 return {'rows':rows,'summary':summary,'max_spectrum_residual':maxerr}
