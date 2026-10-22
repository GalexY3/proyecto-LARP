"""LARP AB4, independent exploratory proxy experiment, not original Scale3D implementation.
All positions reside in periodic 3D unit cube; N=160, 5 types*32.
Controls: iid, Sobol per-type, FPS per-type, LOCAL-proxy, MHU-proxy,
Hybrid (MHU+coverage refinement). Evaluation fields independent of geometry.
"""
import json, time, argparse
import numpy as np
from scipy.stats import qmc
from scipy.spatial import cKDTree
from scipy.special import expit
from pathlib import Path

OUT=Path(__file__).resolve().parent/'ab4_data'; OUT.mkdir(exist_ok=True)
N=160; A=5; M=N//A
rng_global=np.random.default_rng(418)

# Periodic spatial separation, unlike Euclidean domain boundary conditions.
def distvec(X):
    d=X[:,None,:]-X[None,:,:]; d-=np.round(d)
    return d

def local_opt(P, rounds=100):
    P=P.copy(); n=len(P)
    for t in range(rounds):
        d=distvec(P); r=np.linalg.norm(d,axis=-1)+np.eye(n)
        mask=np.eye(n,dtype=bool)
        # global repulsion plus stronger per-role repulsion: two constraints
        same=np.equal(np.arange(n)[:,None]//M,np.arange(n)[None,:]//M)
        strength=np.where(same,1.0,0.25)
        thresh=np.where(same,0.225,0.115)
        c=np.maximum(thresh-r,0)*strength/(r+1e-8)
        c[mask]=0
        force=np.einsum('ij,ijk->ik',c,d)
        P=(P+0.12*force)%1.0
    return P

k_all=np.array([ (x,y,z) for x in (-1,0,1) for y in (-1,0,1) for z in (-1,0,1) if (x,y,z)!=(0,0,0) and (x,y,z)>(0,0,0)],dtype=float)
# 13 positive modes; 26 including conjugates. Note lexicographic tuple comparison.
def spectral(P):
    power=[]
    for ix in [np.arange(N)]+[np.arange(a*M,(a+1)*M) for a in range(A)]:
        ph=np.exp(-2j*np.pi*(P[ix]@k_all.T))
        power.append(float(np.mean(np.abs(ph.mean(axis=0))**2)))
    return np.array(power)

def spectral_grad(P):
    grad=np.zeros_like(P)
    for idx,ww in [(np.arange(N),0.65)]+[(np.arange(a*M,(a+1)*M),1.0) for a in range(A)]:
        Z=np.exp(-2j*np.pi*(P[idx]@k_all.T)); S=Z.mean(axis=0)
        # derivative of mean |S|^2: 4pi * Imag(conj(S)*Z)*k / (len(idx)*modes)
        g=(4*np.pi/(len(idx)*len(k_all)))*(np.imag(Z*np.conj(S)[None,:])@k_all)
        grad[idx]+=ww*g
    return grad

def mhu_proxy(P,steps=180,lr=0.52):
    P=P.copy()
    for i in range(steps):
        g=spectral_grad(P)
        # bounded Fourier motion + local repulsion every 3 steps
        P=(P-lr*g)%1.0
        if i%3==0:
            P=local_opt(P,1)
    return P

def fps_type(rng):
    results=[]; candidates=rng.random((4500,3))
    for a in range(A):
        first=rng.integers(len(candidates)); chosen=[first]
        diff=candidates-candidates[first]; diff-=np.round(diff)
        mind=np.sum(diff**2,axis=1)
        for i in range(M-1):
            nxt=int(np.argmax(mind)); chosen.append(nxt)
            dif=candidates-candidates[nxt]; dif-=np.round(dif)
            mind=np.minimum(mind,np.sum(dif**2,axis=1))
        results.append(candidates[chosen])
    return np.concatenate(results)

def sobol_type(seed):
    return np.concatenate([qmc.Sobol(3,scramble=True,seed=seed+97*a).random_base2(5) for a in range(A)])

def cvt_refine(P,rounds=16,weight=0.5,seed=0):
    # diffuse coverage local constraint at each type; a textbook CVT refinement ingredient.
    rng=np.random.default_rng(seed)
    Q=qmc.Sobol(3,scramble=True,seed=seed).random_base2(12)
    P=P.copy()
    for _ in range(rounds):
        for a in range(A):
            pp=P[a*M:(a+1)*M]; d=Q[:,None,:]-pp[None,:,:]; d-=np.round(d)
            ix=np.argmin((d*d).sum(axis=2),axis=1)
            delta=np.zeros_like(pp); counts=np.bincount(ix,minlength=M)
            np.add.at(delta,ix,d[np.arange(len(Q)),ix])
            delta=delta/(np.maximum(counts,1))[:,None]
            P[a*M:(a+1)*M]=(pp+weight*delta)%1
    return P

def build(seed):
    rng=np.random.default_rng(seed)
    P=rng.random((N,3))
    local=local_opt(P,100)
    mhu=mhu_proxy(local,180,0.52)
    # Hybrid refinement alternates task-independent coverage + spectral regularization
    hybrid=cvt_refine(mhu,rounds=10,weight=0.55,seed=seed+40)
    hybrid=mhu_proxy(hybrid,steps=42,lr=0.2)
    return {'IID':P, 'SOBOL':sobol_type(seed), 'FPS':fps_type(rng),
            'LOCAL-proxy':local,'MHU-proxy':mhu,'HYBRID-proxy':hybrid}

Q=qmc.Sobol(3,scramble=True,seed=904).random_base2(12)

def metrics(P,seed):
    ans={}; ans['spectral_total']=float(spectral(P)[0]);ans['spectral_types']=float(spectral(P)[1:].mean())
    cover=[]; cover_max=[]; cov_drop=[]
    rng=np.random.default_rng(seed+10000)
    # Four shared out-of-sample radial outages center and radius .18
    drops=rng.random((4,3))
    for a in range(A):
        pp=P[a*M:(a+1)*M]; d,_=cKDTree(pp,boxsize=1).query(Q,k=1)
        cover.append(float(np.mean(d)));cover_max.append(float(np.quantile(d,.95)))
        for ctr in drops:
            dr=pp-ctr;dr-=np.round(dr); mask=(dr*dr).sum(axis=1)>.18**2
            if np.any(mask):
                dd,_=cKDTree(pp[mask],boxsize=1).query(Q,k=1)
                cov_drop.append(float(np.quantile(dd,.95)))
    ans['cover_mean']=float(np.mean(cover));ans['cover_p95']=float(np.mean(cover_max));ans['drop_p95']=float(np.mean(cov_drop))
    return ans

def fields(X, params):
    # Two independent, correlated spatial channels per role: three global Fourier waves and 2 local bumps.
    # Independent coefficients for every sample; target is mean of field across unit cube.
    k=params['k']; weights=params['w']; ctr=params['ctr']; widths=params['widths']; height=params['height']
    phi=2*np.pi*X@k.T
    Y=np.cos(phi)@weights[:3]+np.sin(phi)@weights[3:6]
    # Periodic Gaussian radial bumps
    d=X[:,None,:]-ctr[None,:,:];d-=np.round(d)
    Y+=np.exp(-np.sum(d*d,axis=2)/(2*widths[None,:]**2))@height
    return Y

def field_trial(P,seed=42,nfield=50,outage=False):
    rng=np.random.default_rng(seed)
    # all methods receive same fields when seed matched; base surfaces identical for all types (5 roles)
    # For each role independent smooth+sharp field. Reference integral computed on fixed Q (4096)
    meanerr=[]
    for j in range(nfield):
        errs=[]
        for a in range(A):
            params={'k':np.array([[1,0,0],[0,1,1],[1,1,0.]]),
                    'w':rng.normal(size=6),'ctr':rng.random((2,3)),
                    'widths':rng.uniform(.07,.24,2),'height':rng.normal(0,1.4,2)}
            xx=P[a*M:(a+1)*M]
            if outage:
                ctr=rng.random(3);d=xx-ctr;d-=np.round(d)
                xx=xx[(d*d).sum(axis=1)>.18**2]
            v=fields(xx,params).mean() if len(xx) else 0
            ref=fields(Q,params).mean()
            errs.append((v-ref)**2)
        meanerr.append(np.mean(errs))
    return float(np.sqrt(np.mean(meanerr)))

def run(seeds,quick):
    records=[]
    for seed in seeds:
        print('seed',seed,flush=True)
        for name,P in build(seed).items():
            mm=metrics(P,seed)
            mm['rmse_smoothsharp']=field_trial(P,seed=2000+seed,nfield=10 if quick else 30,outage=False)
            mm['rmse_outage']=field_trial(P,seed=3000+seed,nfield=10 if quick else 30,outage=True)
            records.append({'seed':seed,'method':name,**mm})
    (OUT/'metrics.json').write_text(json.dumps(records,indent=2))
    from collections import defaultdict
    agg=defaultdict(list)
    for z in records:agg[z['method']].append(z)
    metrics_keys=['spectral_total','spectral_types','cover_mean','cover_p95','drop_p95','rmse_smoothsharp','rmse_outage']
    summaries={m:{k:{'mean':float(np.mean([x[k] for x in vv])), 'std':float(np.std([x[k] for x in vv],ddof=1))} for k in metrics_keys} for m,vv in agg.items()}
    (OUT/'summary.json').write_text(json.dumps(summaries,indent=2))
    for m,v in summaries.items():print(m, ' '.join(f'{k}={v[k]["mean"]:.4f}' for k in ['spectral_types','cover_p95','drop_p95','rmse_smoothsharp','rmse_outage']),flush=True)
    return records,summaries

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');args=parser.parse_args()
    run(seeds=range(701,705) if args.quick else range(701,713),quick=args.quick)
