"""AB LARP repeatable experiment engine. Freeze before execution; exploratory evidence."""
import argparse, hashlib, json, math, platform, sys
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import qmc
from sklearn.datasets import load_digits
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import balanced_accuracy_score
from scipy.ndimage import rotate, shift, gaussian_filter

ROOT=Path(__file__).resolve().parents[1]
TYPES=5; PER=20; N=TYPES*PER
GENERATORS=('iid','sobol_global','sobol_types','cvt_global','cvt_types','shift_types','jitter_lattice','type_lattice')

def stamp(d):
    return hashlib.sha256(json.dumps(d,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def samples(name,seed):
    rg=np.random.default_rng(seed); typ=np.tile(np.arange(TYPES),PER)
    if name=='iid': pts=rg.random((N,2))
    elif name=='sobol_global': pts=qmc.Sobol(2,scramble=True,seed=seed).random_base2(7)[:N]
    elif name=='sobol_types': pts=np.vstack([qmc.Sobol(2,scramble=True,seed=seed*17+t).random_base2(5)[:PER] for t in range(TYPES)])
    elif name=='jitter_lattice':
        grid=np.array([(i,j) for i in range(10) for j in range(10)],float)
        pts=(grid+.5+rg.uniform(-.34,.34,(N,2)))/10
    elif name=='type_lattice':
        base=np.array([(i,j) for i in range(4) for j in range(5)],float)
        pts=np.vstack([((base+np.array([.5,.5])+rg.random(2))/np.array([4,5]))%1 for _ in range(TYPES)])
    elif name in ('cvt_types','shift_types'):
        parts=[]
        for t in range(TYPES):
            g=np.random.default_rng(seed*101+t)
            p=g.random((PER,2))
            for _ in range(5):
                u=g.random((1024,2)); ids=cKDTree(p,boxsize=1).query(u)[1]
                for j in range(PER):
                    m=ids==j
                    if np.any(m): p[j]=(p[j]+np.mean(((u[m]-p[j]+.5)%1)-.5,axis=0))%1
            if name=='shift_types':p=(p+rg.random(2))%1
            parts.append(p)
        pts=np.vstack(parts)
    elif name=='cvt_global':
        p=rg.random((N,2))
        for _ in range(5):
            u=rg.random((4096,2)); ids=cKDTree(p,boxsize=1).query(u)[1]
            for j in range(N):
                m=ids==j
                if np.any(m):p[j]=(p[j]+np.mean(((u[m]-p[j]+.5)%1)-.5,axis=0))%1
        pts=p
    else:raise ValueError(name)
    if name in ('sobol_types','type_lattice','cvt_types','shift_types'):
        typ=np.repeat(np.arange(TYPES),PER)
    return pts,typ

def coverage(pos,typ,seed,quantile=.95):
    r=np.random.default_rng(seed); u=r.random((768,2))
    ds=np.stack([cKDTree(pos[typ==t],boxsize=1).query(u)[0] for t in range(TYPES)],axis=1).max(axis=1)
    return float(ds.mean()) if quantile==0 else float(np.quantile(ds,quantile))

def spectral(pos,typ,band,mode):
    K=np.array([(a,b) for a in range(-12,13) for b in range(-12,13) if a*a+b*b>0 and ((a*a+b*b<=8) if band=='low' else (40<=a*a+b*b<=100))],float)
    # normalized relative to iid expected 1/N
    if mode=='union':
        z=np.exp(2j*np.pi*(pos@K.T)).sum(axis=0)/N
        return float((np.abs(z)**2).mean())
    z=np.array([np.exp(2j*np.pi*(pos[typ==t]@K.T)).mean(axis=0) for t in range(TYPES)])
    return float((np.abs(z)**2).mean())

def field(pos,kind,freq,seed,types):
    # shared smooth or independent components, all periodic; zero analytic mean
    rg=np.random.default_rng(seed); y=np.zeros(len(pos));
    for t in range(TYPES):
        ii=np.where(types==t)[0]
        if kind=='shared': ph0=0.7; ph1=1.2
        else: ph0,ph1=rg.uniform(0,2*np.pi,2)
        y[ii]=np.sin(2*np.pi*freq*pos[ii,0]+ph0)+.7*np.cos(2*np.pi*freq*pos[ii,1]+ph1)
    return y

def integrate(pos,typ,freq,shared,seed):
    # target 0 by construction, field coefficients random but zero DC
    kind='shared' if shared else 'independent'; return float((field(pos,kind,freq,seed,typ).mean())**2)

def reconstruct(pos,typ,freq,shared,seed,dropout=0,noise=0):
    rg=np.random.default_rng(seed); q=rg.random((256,2)); err=[]
    for t in range(TYPES):
        mask=(typ==t)&(rg.random(N)>=dropout)
        if not mask.any():return np.nan
        pt=pos[mask]; obs=field(pt,'shared' if shared else 'independent',freq,seed+101,np.full(len(pt),t))
        obs=obs+rg.normal(0,noise,len(obs)); target=field(q,'shared' if shared else 'independent',freq,seed+101,np.full(len(q),t))
        dist,ids=cKDTree(pt,boxsize=1).query(q,k=min(6,len(pt)))
        dist=np.atleast_2d(dist);ids=np.atleast_2d(ids)
        if len(q)!=len(dist):dist=dist.T;ids=ids.T
        w=np.exp(-dist**2/(2*(.095)**2));w=w/np.maximum(w.sum(axis=1,keepdims=True),1e-15)
        pred=(obs[ids]*w).sum(axis=1);err.append(np.mean((pred-target)**2))
    return float(np.mean(err))

def digits_data(case):
    ds=load_digits();x=ds.images/16.;y=ds.target
    if case=='orig':target=x
    elif case=='rot15':target=np.array([rotate(z,15,reshape=False,order=1,mode='constant') for z in x])
    elif case=='rot30':target=np.array([rotate(z,30,reshape=False,order=1,mode='constant') for z in x])
    elif case=='blur':target=np.array([gaussian_filter(z,1) for z in x])
    elif case=='shift':target=np.array([shift(z,(1,0),order=1,mode='constant') for z in x])
    else:raise ValueError(case)
    return x,target,y

def im_features(images,pos,typ):
    # five role-specific views, same source image information, bilinear samples
    from scipy.ndimage import map_coordinates, sobel
    feats=[]
    for img in images:
        views=(img, gaussian_filter(img,.7),sobel(img,axis=0)/8,sobel(img,axis=1)/8,gaussian_filter(img,.6)-gaussian_filter(img,1.4))
        z=np.empty(N)
        for t in range(TYPES):
            m=typ==t; p=pos[m];z[m]=map_coordinates(views[t],np.stack([p[:,1]*7,p[:,0]*7]),order=1,mode='nearest')
        feats.append(z)
    return np.array(feats)

def classification(pos,typ,case,seed,base='same'):
    x,tx,y=digits_data(case)
    split=StratifiedShuffleSplit(n_splits=1,test_size=.28,random_state=seed+42)
    train,test=next(split.split(x,y))
    X=im_features(x[train],pos,typ)
    Xt=im_features(tx[test],pos,typ)
    model=RidgeClassifier(alpha=10.)
    model.fit(X,y[train]);pred=model.predict(Xt)
    return float(balanced_accuracy_score(y[test],pred))

def graph_stat(pos,seed,mode='gap',dropout=0,rewire=0):
    rg=np.random.default_rng(seed)
    if dropout:
        p=pos[rg.random(len(pos))>=dropout]
    else:p=pos
    m=len(p);dist=np.sqrt(((p[:,None,:]-p[None,:,:]+.5)%1-.5).__pow__(2).sum(axis=2));np.fill_diagonal(dist,np.inf)
    idx=np.argsort(dist,axis=1)[:,:min(6,m-1)]; A=np.zeros((m,m),float)
    for i in range(m):A[i,idx[i]]=1
    A=np.maximum(A,A.T)
    if rewire:
        edges=np.array(np.where(np.triu(A,1))).T
        cutoff=int(rewire*len(edges)); chosen=rg.choice(len(edges),cutoff,replace=False)
        # same edge budget, reroute to random nonedges
        for k in chosen:A[edges[k,0],edges[k,1]]=A[edges[k,1],edges[k,0]]=0
        while (A.sum()/2)<len(edges):
            i,j=rg.integers(m,size=2)
            if i!=j and A[i,j]==0:A[i,j]=A[j,i]=1
    degree=A.sum(axis=1); inv=np.diag(1/np.sqrt(np.maximum(degree,1)))
    P=inv@A@inv
    eig=np.linalg.eigvalsh(P)
    gap=float(1-np.sort(eig)[-2])
    if mode=='gap':return gap
    if mode=='mix':return float(np.mean(eig[:-1]**12))
    return float((degree.std()/degree.mean()) if degree.mean() else np.nan)

def observation(spec,which,seed):
    p,t=samples(spec[which],seed)
    kind=spec['kind']
    if kind=='cover':return coverage(p,t,seed+900,spec.get('quantile',.95))
    if kind=='spectral':return spectral(p,t,spec.get('band','low'),spec.get('mode','union'))
    if kind=='integrate':
        return float(np.mean([integrate(p,t,spec['freq'],spec['shared'],seed*1000+k) for k in range(64)]))
    if kind=='reconstruct':
        return float(np.mean([reconstruct(p,t,spec['freq'],spec['shared'],seed*100+k,spec.get('dropout',0),spec.get('noise',0)) for k in range(4)]))
    if kind=='classify':return classification(p,t,spec['case'],seed)
    if kind=='graph':return graph_stat(p,seed,spec.get('measure','gap'),spec.get('dropout',0),spec.get('rewire',0))
    raise ValueError(kind)

def run(spec):
    assert spec['a'] in GENERATORS and spec['b'] in GENERATORS
    assert len(spec['seeds'])>=4 and spec['direction'] in ('lower','higher')
    vals=[]
    for seed in spec['seeds']:
        a=observation(spec,'a',seed);b=observation(spec,'b',seed)
        vals.append([a,b,a-b])
    v=np.array(vals)
    from scipy.stats import t
    dif=v[:,2];mean=float(dif.mean());ci=t.ppf(.975,len(dif)-1)*dif.std(ddof=1)/np.sqrt(len(dif))
    out={'id':spec['id'],'spec_sha256':stamp(spec),'n_independent_layout_seeds':len(dif),'a_mean':float(v[:,0].mean()),'b_mean':float(v[:,1].mean()),'paired_delta_a_minus_b':mean,'paired_ci95': [float(mean-ci),float(mean+ci)],'by_seed':v.tolist(), 'favors_a': bool(mean<0 if spec['direction']=='lower' else mean>0),'status':'RUN_EXPLORATORY','independence_note':'Pairs share deterministic generator families and task distributions; data reused across cycles; not external replication.','machine':platform.platform(),'python':sys.version.split()[0]}
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('spec');a=parser.parse_args()
    source=Path(a.spec);spec=json.loads(source.read_text());dest=ROOT/'results'/f"{spec['id']}.json"
    result=run(spec); dest.write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print(json.dumps({k:v for k,v in result.items() if k not in ('by_seed','machine')},ensure_ascii=False))
