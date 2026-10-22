from common import *
def run():
 im,y,tr,va,te=dataset();flat=im.reshape(-1,64);ext={k:v.reshape(-1,64) for k,v in corrupt(im[te]).items()};shifts=np.array([[0,0,0],[.25,0,0],[0,.25,0],[.37,.19,.11]]);rows=[];maxerr=0.
 for g in GSEEDS:
  for method in ['mhu','cvt']:
   p,l=geometry(g,method);p=np.asarray(p,float);Q=finite_modes(2,1,9);ref=np.array(finite_spectrum(p[:,:2],l,Q))
   for phase,s in enumerate(shifts):
    pp=(p+s)%1;maxerr=max(maxerr,float(np.max(abs(np.array(finite_spectrum(pp[:,:2],l,Q))-ref))));M=encode(np.eye(64).reshape(64,8,8),pp,l);X=flat@M;ex={k:v@M for k,v in ext.items()}
    for seed in [991,992]:
     r=train(X,y,tr,va,te,ex,seed=seed,mode='global',hidden=64);r.pop('predictions');rows.append({'geometry':g,'method':method,'phase':phase,'seed':seed,'model':r})
 summary={}
 for method in ['mhu','cvt']:
  summary[method]={k:float(np.mean([max(r['model']['accuracy'][k] for r in rows if r['method']==method and r['geometry']==g and r['seed']==s)-min(r['model']['accuracy'][k] for r in rows if r['method']==method and r['geometry']==g and r['seed']==s) for g in GSEEDS for s in [991,992]])) for k in ['clean','noise','occlusion','rotation']}
 assert maxerr<1e-10
 return {'rows':rows,'summary':{'mean_phase_accuracy_ranges':summary,'max_spectrum_residual':maxerr,'selected_at_cap':sum(r['model']['best_step']==240 for r in rows),'training_fits':len(rows)},'inference':'Exposed historical dataset; no best phase selected.'}
