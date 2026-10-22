"""C04: preregistered here as λ=.50 regularization to broad isotropic spectral risk.
Independent geometry seeds 801..808, task covariance code as C03; new test spatial outages.
"""
import numpy as np,json
from pathlib import Path
from laboratorio_ab4 import A,M,N,local_opt,sobol_type,fps_type
from covarianza_ab4 import K,B,W,true_covariances,pilot_cov,phasors,grad,risk,opt
OUT=Path(__file__).resolve().parent/'ab4_data'
C=true_covariances()
Cg=np.repeat(np.eye(A)[None,:,:],B,axis=0)
Cm=np.repeat((.75*np.eye(A)+.25*np.ones((A,A))/A)[None,:,:],B,axis=0)
SHIFT=np.array([.2*C[j]+1.35*C[(j+17)%B] for j in range(B)])

def dropout_risk(P,C,seed,nt=18):
    rng=np.random.default_rng(seed)
    out=[]
    for ctr in rng.random((nt,3)):
        V=[]
        for a in range(A):
            X=P[a*M:(a+1)*M]
            d=X-ctr; d-=np.round(d)
            X=X[(d*d).sum(axis=1)>(.18**2)]
            if len(X):V.append(np.exp(2j*np.pi*X@K.T).mean(axis=0))
            else:V.append(np.zeros(B,complex))
        V=np.array(V)
        out.append(float(np.real(np.einsum('ak,kab,bk->',np.conj(V)*W[:,None],C,V*W[:,None]))/(2*B)))
    return float(np.mean(out))

def run():
    rows=[]
    for seed in range(801,809):
        rng=np.random.default_rng(seed)
        P=rng.random((N,3));L=local_opt(P,100)
        chat=pilot_cov(C,seed+19000,60)
        # convex shrink toward broad isotropic baseline; pilot statistics unchanged
        csh=.50*chat+.50*np.trace(chat,axis1=1,axis2=2).mean()/A*Cg
        schemes={'IID':P,'SOBOL':sobol_type(seed),'FPS':fps_type(rng),'LOCAL-proxy':L,
                 'MHU-wide-proxy':opt(L,Cm), 'COSI-pilot-proxy':opt(L,chat),
                 'COSI-shrink50-proxy':opt(L,csh)}
        for name,Z in schemes.items():
            rows.append({'seed':seed,'method':name,'test_risk':risk(Z,C),'shift_risk':risk(Z,SHIFT),
                         'drop_risk':dropout_risk(Z,C,seed+3000)})
        print('seed',seed, 'done',flush=True)
    (OUT/'robustness.json').write_text(json.dumps(rows,indent=2))
    methods=sorted({r['method'] for r in rows})
    for method in methods:
        items=[r for r in rows if r['method']==method]
        print(method,*[f'{np.mean([np.sqrt(x[q]) for x in items]):.5f}' for q in ['test_risk','shift_risk','drop_risk']],flush=True)
    return rows

if __name__=='__main__':run()
