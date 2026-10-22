"""Fixed 24 readings total, varied quotas by RGB channel. Same training scene pool.
Follow-up exploratory ablation. Proxy method, NOT biological MHU nor hardware Bayer (channels may overlap).
"""
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import minimize
import real_rgb_sensors as m
O=Path(__file__).resolve().parent

def score(p,C,q,with_grad=True):
    counts=np.asarray(q); offsets=np.r_[0,np.cumsum(counts)];P=p.reshape(sum(q),2)
    es=np.exp(2j*np.pi*(P@m.K.T))
    z=np.stack([es[offsets[a]:offsets[a+1]].mean(0)*m.WT[a] for a in range(m.A)])
    t=np.einsum('kab,bk->ak',C,z)
    loss=float(np.real(np.einsum('ak,ak->',z.conj(),t)))
    gr=np.zeros_like(P)
    for a in range(m.A):
        ia=slice(offsets[a],offsets[a+1]);ee=es[ia]
        gr[ia]=-(4*np.pi*m.WT[a]/q[a])*(np.imag(np.conj(t[a])[None,:]*ee)@m.K)
        # local same-channel spacing at fixed packing weight
        d=P[ia,None,:]-P[None,ia,:]
        d-=np.round(d)
        zloc=np.exp(-np.sum(d*d,axis=-1)/.15**2)
        np.fill_diagonal(zloc,0)
        loss+=.000025*zloc.sum()
        gr[ia]+=-4*.000025/.15**2*np.einsum('ij,ijd->id',zloc,d)
    return (loss,gr.ravel()) if with_grad else loss

def init_ids(q,seed):
    from scipy.stats import qmc
    r=[]
    for a,n in enumerate(q):
        gen=qmc.Sobol(2,scramble=True,seed=seed+a*31)
        ps=gen.random_base2(int(np.ceil(np.log2(n))))[:n]
        ids=m.idx(ps)
        used=set()
        for j,t in enumerate(ids):
            if int(t) in used:
                d=m.coords(np.arange(m.PIX))-m.coords(np.array([t]))[0]
                ds=(d*d).sum(axis=1)
                ds[list(used)]=np.inf
                ids[j]=np.argmin(ds)
            used.add(int(ids[j]))
        r.append(ids)
    return r

def optimized_layout(q,C,seed):
    rng=np.random.default_rng(seed)
    start=np.vstack([m.coords(ids) for ids in init_ids(q,seed)])+rng.normal(0,.008,(24,2))
    res=minimize(score,np.clip(start,.001,.999).ravel(),args=(C,q,True),jac=True,method='L-BFGS-B',bounds=[(.0001,.9999)]*48,options={'maxiter':130,'ftol':1e-12})
    from scipy.spatial.distance import cdist
    P=res.x.reshape(24,2)
    idx=m.idx(P)
    offsets=np.r_[0,np.cumsum(q)]
    layouts=[]
    for a in range(m.A):
        group=idx[offsets[a]:offsets[a+1]].copy()
        # Nearest unused pixel if duplicates caused by snapping.
        used=set()
        for j,t in enumerate(group):
            if int(t) in used:
                Q=m.coords(np.arange(m.PIX)); d=np.sum((Q-P[offsets[a]+j])**2,axis=1)
                d[list(used)]=np.inf
                group[j]=int(np.argmin(d))
            used.add(int(group[j]))
        layouts.append(group)
    return layouts

def eval(x,L):
    X=x.reshape(len(x),m.A,m.PIX)
    target=(X.mean(2)*m.WT).sum(1)
    pred=sum(m.WT[a]*X[:,a,l].mean(1) for a,l in enumerate(L))
    return float(np.sqrt(np.mean((target-pred)**2)))

def run():
    train,val,ext=m.get_data();C=m.covariance_train(train)
    diag=np.stack([np.diag(np.real(np.diag(c))) for c in C]);sh=.5*C+.5*diag
    quotas=[[8,8,8],[6,12,6],[4,16,4],[4,12,8],[10,12,2],[6,16,2],[4,18,2],[2,20,2]]
    rows=[]
    for q in quotas:
        for method in ['SOBOL','POWER-DIAG','COSI-SHRINK']:
            for seed in range(7):
                L=init_ids(q,seed+5500) if method=='SOBOL' else optimized_layout(q,diag if method=='POWER-DIAG' else sh,seed+5500)
                rows.append({'quotas':q,'method':method,'seed':seed,'train':eval(train,L),'rocket':eval(ext['rocket'],L),'hubble':eval(ext['hubble_deep_field'],L)})
        print('quota',q,flush=True)
    summary=[]
    for q in quotas:
        for method in ['SOBOL','POWER-DIAG','COSI-SHRINK']:
            z=[v for v in rows if v['quotas']==q and v['method']==method]
            summary.append({'quotas':q,'method':method,'rocket':float(np.mean([v['rocket'] for v in z])),'hubble':float(np.mean([v['hubble'] for v in z])),'mean_of_two_scenes':float(np.mean([(v['rocket']+v['hubble'])/2 for v in z]))})
    (O/'quota_ablations_results.json').write_text(json.dumps({'scope':'Exploratory quota sweep, same data; selection on OOD would invalidate confirmation','summary':summary,'rows':rows},indent=2))
    print(json.dumps(sorted(summary,key=lambda v:v['mean_of_two_scenes']),indent=2))
if __name__=='__main__':run()
