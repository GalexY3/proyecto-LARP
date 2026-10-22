from common import *
def run():
    im,y,tr,va,te=dataset();cor=corrupt(im[te]);rows=[]
    for g in GSEEDS:
        for method in ['mhu','cvt']:
            M=encoder_matrix(g,method);A=M.reshape(64,5,16).mean(1)
            for rep,T in [('original',M),('mean16',A),('mean80',np.tile(A,(1,5)))]:
                X=im.reshape(-1,64)@T;ext={k:v.reshape(-1,64)@T for k,v in cor.items()}
                z=train(X,y,tr,va,te,ext,mode='global',hidden=216 if rep=='mean16' else 64)
                rows.append({'geometry':g,'method':method,'representation':rep,'rank':int(np.linalg.matrix_rank(T)),**z})
    summary={m+'_'+p:{k:float(np.mean([r['accuracy'][k] for r in rows if r['method']==m and r['representation']==p])) for k in cor} for m in ['mhu','cvt'] for p in ['original','mean16','mean80']}
    return {'rows':rows,'summary':summary}

