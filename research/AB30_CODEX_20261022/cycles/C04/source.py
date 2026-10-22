from common import *
def run():
    im,y,tr,va,te=dataset();cor=corrupt(im[te]);rows=[]
    for g in GSEEDS:
        for method in METHODS:
            p,l=geometry(g,method);x=encode(im,p,l).astype('float32');ext={k:encode(v,p,l).astype('float32') for k,v in cor.items()}
            for seed in [991,992]:
                z=train(x,y,tr,va,te,ext,seed=seed,mode='global');rows.append({'geometry':g,'method':method,'model_seed':seed,**z})
    for seed in [991,992]:
        z=train(im.reshape(-1,64),y,tr,va,te,{k:v.reshape(-1,64) for k,v in cor.items()},seed=seed,mode='global')
        rows.append({'geometry':None,'method':'pixels','model_seed':seed,**z})
    summary={m:{k:float(np.mean([r['accuracy'][k] for r in rows if r['method']==m])) for k in cor} for m in METHODS+['pixels']}
    summary['selected_at_cap']=sum(r['best_step']==240 for r in rows)
    return {'rows':rows,'summary':summary}

