"""AB06 C02: generate INDEPENDENT smaller original Scale3D geometries. Not Wei."""
from pathlib import Path
import sys,json,hashlib,time
import numpy as np
from scipy.spatial import cKDTree
from src.scale3d_geometry_v2 import generate
ROOT=Path(__file__).resolve().parents[1]; D=ROOT/'data'; D.mkdir(exist_ok=True)
SEEDS=[8101,8102,8103,8104]; N=128;ITERS=600

def cvt_per_type(p,lab,seed):
    rng=np.random.default_rng(seed+9000); q=p.copy()
    for t in range(5):
        idx=np.where(lab==t)[0]; centres=q[idx].copy()
        for _ in range(14):
            probes=rng.random((4000,3)); assigned=cKDTree(centres,boxsize=1).query(probes,k=1)[1]
            for j in range(len(idx)):
                ps=probes[assigned==j]
                if len(ps):
                    dif=((ps-centres[j]+.5)%1-.5)
                    centres[j]=(centres[j]+dif.mean(axis=0))%1
        q[idx]=centres
    return q

def coverage(p,l,queries):
    for plane,k in [('2d',8),('3d',12)]:
        coord=p[:,:2] if plane=='2d' else p
        ix=cKDTree(coord,boxsize=1).query(queries[:,:2] if plane=='2d' else queries,k=k)[1]
        yield plane,float(np.mean(np.all([np.any(l[ix]==t,axis=1) for t in range(5)],axis=0)))

if __name__=='__main__':
    results=[]
    for seed in SEEDS:
        t0=time.perf_counter()
        a=generate(seed,N,iterations=ITERS,spectral=False,validate=False)
        b=generate(seed,N,iterations=ITERS,spectral=True,validate=False)
        l=a['labels'].cpu().numpy(); assert np.array_equal(l,b['labels'].cpu().numpy());
        pa=a['coordinates'].cpu().numpy();pm=b['coordinates'].cpu().numpy()
        initial=np.random.default_rng(seed).random((N,3));
        zero=generate(seed,N,iterations=0,spectral=False,validate=False)
        assert np.allclose(initial,zero['coordinates'].cpu().numpy(),atol=1e-6) and np.array_equal(l,zero['labels'].cpu().numpy())
        rng=np.random.default_rng(seed*19)
        r=rng.random((N,3));cv=cvt_per_type(r,l,seed)
        sob=np.zeros_like(r)
        from scipy.stats import qmc
        for t in range(5):
            ix=np.where(l==t)[0];m=len(ix)
            sob[ix]=qmc.Sobol(d=3,scramble=True,seed=seed+t*11).random_base2(int(np.ceil(np.log2(m))))[:m]
        file=D/f'geo_{seed}.npz';np.savez_compressed(file,labels=l,local=pa,mhu=pm,random=r,cvt=cv,sobol=sob,initial=initial)
        qry=np.random.default_rng(seed+101).random((3000,3))
        cov={name:dict(coverage(arr,l,qry)) for name,arr in [('local',pa),('mhu',pm),('random',r),('cvt',cv),('sobol',sob)]}
        results.append({'seed':seed,'N':N,'counts':np.bincount(l,minlength=5).tolist(),'elapsed_sec':time.perf_counter()-t0,'coverage':cov,'file_sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'paired_initialization':True})
        print('C02 generated',seed,'time',round(results[-1]['elapsed_sec'],1),'coverage_2d', {k:round(v['2d'],3) for k,v in cov.items()},flush=True)
    (D/'C02.json').write_text(json.dumps(results,indent=2))
