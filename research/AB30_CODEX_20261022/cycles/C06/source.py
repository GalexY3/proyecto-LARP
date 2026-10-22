from common import *
def run():
    im,y,tr,va,te=dataset();x=im.reshape(-1,64).astype('float32');ext={k:v.reshape(-1,64).astype('float32') for k,v in corrupt(im[te]).items()};rows=[]
    std=x[tr].std(0)
    for center in [False,True]:
        mu=x[tr].mean(0) if center else np.zeros(64,dtype='float32')
        for scale in ['unit','global','guard','floor.2']:
            sd={'unit':np.ones(64),'global':np.full(64,x[tr].std()),'guard':np.where(std<1e-5,1,std),'floor.2':np.maximum(std,.2)}[scale]
            for seed in [991,992]:
                z=train((x-mu)/sd,y,tr,va,te,{k:(v-mu)/sd for k,v in ext.items()},seed=seed,mode='fixed')
                rows.append({'center':center,'scale':scale,'model_seed':seed,**z})
    summary={str(c)+'_'+s:{k:float(np.mean([r['accuracy'][k] for r in rows if r['center']==c and r['scale']==s])) for k in ext} for c in [False,True] for s in ['unit','global','guard','floor.2']}
    return {'rows':rows,'summary':summary}

