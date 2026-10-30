"""LARP AB30: finite proxy MHU-vs-CVT-vs-grid under matched-edge functional sensing.
Frozen full source must be committed before outcomes. No native LARP 400-geometry,
no proof of thermodynamic multihyperuniformity, and no learned MoE baseline.
"""
from __future__ import annotations
import os, sys, json, hashlib, platform
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import qmc
import torch

N=400; DEGREE=6
COUNTS=[163,85,68,50,34]
GEOM_SEEDS=[1103,1109,1117]
FIELD_SEEDS=[12013,12037,12041,12049,12073,12097,12101,12109]
CONTEXTS=['low','high','correlated','anticorrelated','rare','localized']
SHIFTS=['clean','random_drop15','random_drop40','rare_drop40','noise25']
METHODS=['grid_knn','cvt_knn','mhu_knn','random_deg6','expander_deg6','grid_type','cvt_type','mhu_type','mhu_hybrid']
MODES=np.array([(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2),(2,1),(1,2)],float)

def shajson(obj):return hashlib.sha256(json.dumps(obj,sort_keys=True).encode()).hexdigest()
def labels_for_seed(seed):
    arr=np.repeat(np.arange(5),COUNTS);np.random.default_rng(seed+4).shuffle(arr)
    return arr

def optimize_mhu(seed,lab):
    # finite spectral proxy. No claim of native Scale3D, MHU certification or original avian packing
    rng=np.random.default_rng(seed+16)
    coords=qmc.Sobol(2,scramble=True,seed=seed+8).random_base2(9)[:N]
    torch.manual_seed(seed)
    x=torch.tensor(coords,dtype=torch.float64,requires_grad=True)
    ks=torch.tensor(MODES,dtype=torch.float64)
    groups=[torch.tensor(np.flatnonzero(lab==c),dtype=torch.long) for c in range(5)]
    opt=torch.optim.Adam([x],lr=.014)
    for step in range(65):
        opt.zero_grad();ph=torch.exp((2j*np.pi)*(x@ks.T))
        union=(ph.mean(0).abs()**2).mean()
        own=torch.stack([(ph[idx].mean(0).abs()**2).mean() for idx in groups]).mean()
        delta=x[:,None,:]-x[None,:,:];delta=delta-torch.round(delta.detach())
        # pairwise repulsion finite gaussian kernel, non-identical to original native code
        rep=(torch.exp(-(delta**2).sum(-1)/.00065).sum()-N)/(N*N)
        loss=.55*union+.45*own+.20*rep
        loss.backward();opt.step()
        with torch.no_grad():x.remainder_(1.)
    return x.detach().numpy()

def cvt_geometry(seed,lab):
    """Type-conditional periodic Lloyd approximation with a fixed position budget."""
    rng=np.random.default_rng(seed+2)
    pts=qmc.Sobol(2,scramble=True,seed=seed+3).random_base2(9)[:N]
    sample=qmc.Sobol(2,scramble=True,seed=seed+5).random_base2(13)
    for c in range(5):
        idx=np.flatnonzero(lab==c);p=pts[idx].copy()
        for _ in range(9):
            _, owner=cKDTree(p,boxsize=1.).query(sample)
            for j in range(len(p)):
                group=sample[owner==j]
                if len(group):
                    diff=(group-p[j]+.5)%1-.5
                    p[j]=(p[j]+diff.mean(0))%1
        pts[idx]=p
    return pts

def distance(src,dst):
    d=src[:,None,:]-dst[None,:,:]
    d=(d+.5)%1-.5
    return (d*d).sum(axis=2)

def make_edges(p,lab,kind,seed):
    rng=np.random.default_rng(seed+33)
    all_d=distance(p,p)
    np.fill_diagonal(all_d,np.inf)
    neighbors=np.argsort(all_d,axis=1,kind='stable')[:,:DEGREE]
    if kind=='knn':return neighbors
    if kind=='random':
        return np.array([rng.choice(np.delete(np.arange(N),i),size=DEGREE,replace=False) for i in range(N)],int)
    if kind=='expander':
        # random relabeling of 6-shift degree-regular circulant (not a verified expander family)
        perm=rng.permutation(N);rev=np.empty(N,int);rev[perm]=np.arange(N)
        offsets=rng.choice(np.arange(1,N),size=DEGREE,replace=False)
        return np.array([perm[(rev[i]+offsets)%N] for i in range(N)],int)
    if kind not in ('type','hybrid'):raise ValueError(kind)
    out=[]
    for i in range(N):
        nearest=list(np.argsort(all_d[i],kind='stable'))
        selected=[]
        if kind=='hybrid':selected.extend(nearest[:2])
        for c in range(5):
            if c!=lab[i] and not any(lab[j]==c for j in selected):
                j=next(j for j in nearest if lab[j]==c and j not in selected)
                selected.append(j)
        for j in nearest:
            if len(selected)>=DEGREE:break
            if j not in selected:selected.append(j)
        assert len(selected)==DEGREE
        out.append(selected)
    return np.array(out,int)

def reach(edges,hop):
    n=len(edges);A=np.zeros((n,n),dtype=bool)
    A[np.arange(n)[:,None],edges]=True
    np.fill_diagonal(A,True)
    if hop==1:return A
    # Boolean matrix square; includes self at each hop.
    return (A.astype(np.uint8)@A.astype(np.uint8))>0

def build_selectors(edges,p,lab,hop):
    mask=reach(edges,hop)
    dist=distance(p,p)
    nearest=np.full((N,5),-1,dtype=np.int32)
    for c in range(5):
        d=np.where(mask & (lab[None,:]==c),dist,np.inf)
        arg=d.argmin(axis=1)
        nearest[:,c]=np.where(np.isfinite(d[np.arange(N),arg]),arg,-1)
    return nearest

def field(p,context,seed):
    """Finite Fourier/task oracle; target available only for evaluation."""
    rng=np.random.default_rng(seed+39); n=len(p)
    if context in ('low','correlated','anticorrelated','rare'):
        freq=[(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2)]
    else:
        freq=[(3,0),(0,3),(3,2),(2,-3),(4,1),(1,4),(5,0),(0,5)]
    f=np.array(freq,float)
    if context=='localized':
        centers=rng.uniform(size=(5,2));sigma=.09
        fields=np.array([np.exp(-np.sum(((p-center+.5)%1-.5)**2,axis=1)/(2*sigma*sigma)) for center in centers]).T
        fields=(fields-fields.mean(0))/(fields.std(0)+1e-8)
    else:
        phase=rng.uniform(0,2*np.pi,size=len(f))
        common=np.cos((p@f.T)*2*np.pi+phase).sum(1)
        fields=[]
        for c in range(5):
            ph=rng.uniform(0,2*np.pi,size=len(f));z=np.cos(p@f.T*2*np.pi+ph).sum(1)
            if context=='correlated':z=.88*common+.12*z
            if context=='anticorrelated':z=(1 if c%2==0 else -1)*.92*common+.08*z
            fields.append(z)
        fields=np.stack(fields,1)
        fields-=fields.mean(axis=0);fields/=fields.std(axis=0)+1e-8
    if context=='rare':
        weights=np.array([.025,.025,.025,.025,.9]);weights/=weights.sum()
    else:weights=np.full(5,.2)
    target=fields@weights
    truth=np.var(target)
    return fields,weights,target,truth

def score_one(p,lab,selector,context,shift,geom_seed,field_seed):
    fields,w,target,var=field(p,context,field_seed)
    rng=np.random.default_rng(field_seed*101+geom_seed*17+SHIFTS.index(shift))
    y=fields[np.arange(N),lab].copy()
    seen=np.ones(N,dtype=bool)
    if shift=='random_drop15':seen=rng.random(N)>.15
    elif shift=='random_drop40':seen=rng.random(N)>.40
    elif shift=='rare_drop40':seen[(lab==4)]=rng.random(np.sum(lab==4))>.4
    elif shift=='noise25':y=y+rng.normal(size=N)*.25
    inds=np.maximum(selector,0)
    vals=np.where((selector>=0)&seen[inds],y[inds],0.0)
    pred=vals@w
    coverage=((selector>=0)&seen[inds]).mean()
    # nearest per target source is chosen *before* random dropout, a deliberate limitation.
    mse=np.mean((pred-target)**2)
    return float(mse/(var+1e-12)),float(coverage)

def run(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    records=[]; geometries=[];invariants=[]
    for geom_seed in GEOM_SEEDS:
        lab=labels_for_seed(geom_seed)
        pts={'grid':(np.column_stack(np.meshgrid((np.arange(20)+.5)/20,(np.arange(20)+.5)/20)).reshape(2,-1).T)%1} # overwritten below for correctness
        xx,yy=np.meshgrid((np.arange(20)+.5)/20,(np.arange(20)+.5)/20)
        pts['grid']=np.column_stack([xx.ravel(),yy.ravel()])
        pts['cvt']=cvt_geometry(geom_seed,lab)
        pts['mhu']=optimize_mhu(geom_seed,lab)
        graphs={
            'grid_knn':('grid','knn'),'cvt_knn':('cvt','knn'),'mhu_knn':('mhu','knn'),
            'random_deg6':('mhu','random'),'expander_deg6':('mhu','expander'),
            'grid_type':('grid','type'),'cvt_type':('cvt','type'),
            'mhu_type':('mhu','type'),'mhu_hybrid':('mhu','hybrid')}
        for method,(pn,gkind) in graphs.items():
            p=pts[pn];edge=make_edges(p,lab,gkind,geom_seed)
            assert edge.shape==(N,DEGREE) and np.all(edge!=np.arange(N)[:,None])
            assert all(len(set(row))==DEGREE for row in edge)
            for hop in [1,2]:
                selector=build_selectors(edge,p,lab,hop)
                # save structural diagnostics separately
                observed=(selector>=0).mean(axis=1)
                geometries.append(dict(seed=geom_seed,method=method,hop=hop,availability=float(observed.mean()),min_availability=float(observed.min()),edge_dist=float(np.mean(np.sqrt(distance(p,p)[np.arange(N)[:,None],edge])))))
                for ci,context in enumerate(CONTEXTS):
                    for sj,shift in enumerate(SHIFTS):
                        for fs in FIELD_SEEDS:
                            mse,coverage=score_one(p,lab,selector,context,shift,geom_seed,fs)
                            records.append(dict(cycle_id=f"R{6*sj+ci+1:02d}",seed=geom_seed,field_seed=fs,method=method,hop=hop,context=context,shift=shift,nmse=mse,coverage=coverage))
        print('geometry',geom_seed,'records',len(records),flush=True)
    data={'protocol':'LARP_AB30_ROUTING_v1','status':'EXPLORATORY_SYNTHETIC','geometry_seed':GEOM_SEEDS,'field_seed':FIELD_SEEDS,'contexts':CONTEXTS,'shifts':SHIFTS,'methods':METHODS,'N':N,'degree':DEGREE,'counts':COUNTS,'records':records,'graph_diagnostics':geometries,'versions':{'python':platform.python_version(),'numpy':np.__version__,'torch':torch.__version__}}
    path=out/'results.json';path.write_text(json.dumps(data,separators=(',',':')))
    from collections import defaultdict
    dd=defaultdict(list)
    for r in records:dd[(r['cycle_id'],r['method'],r['hop'])].append(r['nmse'])
    summaries=[dict(cycle_id=k[0],method=k[1],hop=k[2],nmse_mean=float(np.mean(v)),n=len(v)) for k,v in dd.items()]
    (out/'summary.json').write_text(json.dumps(summaries,indent=2))
    print('FINISHED rows',len(records),'SHA256',hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)

if __name__=='__main__':
    torch.set_num_threads(2)
    run(sys.argv[1] if len(sys.argv)>1 else '.')
