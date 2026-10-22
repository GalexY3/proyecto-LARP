"""Ablation of task/role-covariance spectral design on synthetic periodic 3D five-channel fields.
Not historical Scale3D, not a novel published method. All test coefficient draws independent of pilot.
"""
import json
import numpy as np
from pathlib import Path
from laboratorio_ab4 import N,A,M,local_opt,sobol_type,fps_type,distvec
# WARNING: avoid import side-effect of evaluar_bandas_ab4 that executes experiment at import.
K=np.array([p for x in range(-2,3) for y in range(-2,3) for z in range(-2,3)
            if (p:=(x,y,z))!=(0,0,0) and p>(0,0,0)],float)
B=len(K)
W=np.ones(A)/A
O=Path(__file__).resolve().parent/'ab4_data'

def true_covariances():
    rng=np.random.default_rng(20261022)
    C=[]
    for t,k in enumerate(K):
        b=rng.normal(size=A)
        b/=np.linalg.norm(b)
        amplitude=0.35+2.5*(int(sum(k*k)>2)) + 3.5*(int(t%7==0))
        C.append(amplitude*(np.outer(b,b)+0.13*np.eye(A)))
    return np.array(C)

def pilot_cov(C,seed,pilot_size=60):
    rng=np.random.default_rng(seed)
    Z=np.array([rng.multivariate_normal(np.zeros(A),c,size=pilot_size) for c in C])
    S=np.einsum('btj,btk->bjk',Z,Z)/pilot_size
    # same global shrinkage policy every geometry; estimated from pilot only.
    return .87*S + .13*np.eye(A)[None,:,:]*np.trace(S,axis1=1,axis2=2)[:,None,None]/A

def phasors(P):
    return np.stack([np.exp(2j*np.pi*P[a*M:(a+1)*M]@K.T).mean(axis=0) for a in range(A)],axis=0)

def risk(P,C):
    V=phasors(P)
    return float(np.real(np.einsum('ak,kab,bk->',np.conj(V)*W[:,None],C,V*W[:,None]))/(2*B))

def grad(P,C):
    V=phasors(P); Aweight=W[:,None]
    target=np.einsum('kab,bk->ak',C,V*Aweight)
    g=np.zeros((N,3))
    for a in range(A):
        ix=slice(a*M,(a+1)*M)
        zz=np.exp(2j*np.pi*P[ix]@K.T)
        g[ix]=-(2*np.pi*W[a]/(M*B))* (np.imag(np.conj(target[a])[None,:]*zz)@K)
    return g

def opt(P,C,steps=185,lr=13.):
    P=P.copy()
    for t in range(steps):
        g=grad(P,C)
        P=(P-lr*np.clip(g,-.08,.08))%1
        if t%4==0:P=local_opt(P,1)
    return P

def validate_grad():
    rng=np.random.default_rng(45);P=rng.random((N,3)); C=true_covariances()
    G=grad(P,C)
    for ix,j in [(0,0),(32,1),(111,2)]:
        eps=1e-6; Q=P.copy();Q[ix,j]+=eps;v1=risk(Q,C)
        Q[ix,j]-=2*eps;v0=risk(Q,C)
        delta=(v1-v0)/(2*eps)
        print('gradient',ix,j,'numeric',delta,'computed',G[ix,j], 'relative_err',abs(delta-G[ix,j])/(1e-9+abs(delta)))


def run():
    validate_grad()
    C=true_covariances(); Cuniform=np.repeat(np.eye(A)[None,:,:],B,axis=0) # equal per-role spectral
    Cmixed=np.repeat((np.eye(A)*.75+np.ones((A,A))*.25/A)[None,:,:],B,axis=0)
    # covariate shift: unexpected role mixing and amplitude distribution
    rng=np.random.default_rng(512)
    Shift=[]
    for j,c in enumerate(C):
        h=(j+17)%len(C); R=c*.2 + C[h]*1.35
        Shift.append(R)
    Shift=np.array(Shift)
    entries=[]
    for seed in range(701,709):
        r=np.random.default_rng(seed); init=r.random((N,3)); loc=local_opt(init,100)
        Chat=pilot_cov(C,seed+19000,pilot_size=60)
        p={'IID':init,'SOBOL':sobol_type(seed),'FPS':fps_type(r),'LOCAL-proxy':loc,
           'MHU-wide-proxy':opt(loc,Cmixed), 'COSI-pilot-proxy':opt(loc,Chat)}
        for name,Q in p.items():
            entries.append({'seed':seed,'method':name,'risk_id':risk(Q,C),'risk_shift':risk(Q,Shift),
                'risk_pilot':risk(Q,Chat)})
        print('completed',seed,flush=True)
    (O/'covariance.json').write_text(json.dumps(entries,indent=2))
    for name in sorted({v['method'] for v in entries}):
        Z=[v for v in entries if v['method']==name]
        print(name,'in_RMSE',np.mean([np.sqrt(z['risk_id']) for z in Z]),'shift_RMSE',np.mean([np.sqrt(z['risk_shift']) for z in Z]),flush=True)

if __name__=='__main__':run()
