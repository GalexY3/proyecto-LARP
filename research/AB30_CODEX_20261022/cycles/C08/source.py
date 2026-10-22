from common import *
def run():
    im,y,tr,va,te=dataset();cor=corrupt(im[te]);rows=[]
    grid=np.array([[a/7,b/7] for a in range(8) for b in range(8)])
    B16=basis(grid,CENTRES);B64=basis(grid,grid)
    for method,M in [('rbf16',B16),('rbf64',B64),('rbf16x5',np.tile(B16,(1,5)))]:
        X=im.reshape(-1,64)@M;ext={k:v.reshape(-1,64)@M for k,v in cor.items()}
        for seed in [991,992]:
            z=train(X,y,tr,va,te,ext,mode='global',seed=seed,hidden=216 if method=='rbf16' else None)
            rows.append({'method':method,'model_seed':seed,**z})
    summary={m:{k:float(np.mean([r['accuracy'][k] for r in rows if r['method']==m])) for k in cor} for m in ['rbf16','rbf64','rbf16x5']}
    return {'rows':rows,'summary':summary}

