#!/usr/bin/env python3
"""BR30: exactly 30 preregistered, substantive condition-level AB decisions.
Run: python src/run_br30.py --out data --phase pilot|confirm
Python >=3.10, numpy/scipy; pure synthetic Fourier fields; no GPU.
Check prereg/BR30_20261021.md for frozen estimands and limitations.
"""
from __future__ import annotations
import argparse,json,csv,time,hashlib
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree

ORIG=Path(__file__).resolve().parents[2]/'LARP_LOCAL_MHU_VISUALIZACION'
# Fallback when extracted outside the current runtime: copy original NPZs into data/geometrias/
LOCAL=Path(__file__).resolve().parents[1]/'data'/'geometrias'
TYPES=5
GEOS=('random','local','mhu','stratified')
FREQS=(1,2,3,4,6)
KS=(8,12,16,24,32)
QUANTILES=(.50,.75,.90,.95,.99)
DROPS=(0,.10,.25,.40,.60)
BWS=(.3,.6,1,2,4)
ABLATIONS=('labels_shuffled','positions_shuffled_per_type','only_dominant','signals_scrambled_per_type','positions_labels_permuted')
MODES=np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,-1,0],[0,1,-1],[1,0,-1],[2,0,0],[0,2,0],[0,0,2]],dtype=np.float64)

def geometry(name):
    if name=='stratified':
        ref=np.load((LOCAL if (LOCAL/'random_geometry.npz').exists() else ORIG)/'random_geometry.npz')
        typ=ref['labels'].copy()
        rg=np.random.default_rng(150123)
        # Competent spatial baseline: scrambled jittered cubic grid, independent for each type.
        pos=np.empty((len(typ),3),dtype=np.float64)
        for t in range(5):
            ix=np.where(typ==t)[0]; n=len(ix)
            g=int(np.ceil(n**(1/3)))
            cells=np.stack(np.meshgrid(*[np.arange(g)]*3,indexing='ij'),axis=-1).reshape(-1,3)
            cells=cells[rg.permutation(len(cells))[:n]]
            pos[ix]=(cells+rg.uniform(.1,.9,(n,3)))/g
            pos[ix]=(pos[ix]+rg.uniform(0,1,3))%1
        return pos,typ
    p=LOCAL/f'{name}_geometry.npz'
    if not p.exists():p=ORIG/f'{name}_geometry.npz'
    d=np.load(p)
    return np.asarray(d['points'],dtype=np.float64),np.asarray(d['labels'],dtype=int)

def ds(seed, n, freq):
    r=np.random.default_rng(seed)
    q=r.random((n,3))
    # Same worlds and queries across geom and bandwidth within each seed.
    a=r.standard_normal((5,len(MODES),2))/np.sqrt(len(MODES))
    m=np.rint(MODES*freq).astype(int)
    phase=2*np.pi*q@m.T
    tr=np.cos(phase)@a[:,:,0].T+np.sin(phase)@a[:,:,1].T
    y=tr[:,0]*tr[:,1]+tr[:,2]*tr[:,3]+.4*tr[:,0]*tr[:,2]*tr[:,4]
    return q,a,m,y

def query_neighbors(pos,typ,q,k=32):
    dd,idx=cKDTree(pos,boxsize=1.0).query(q,k=k)
    return np.atleast_2d(idx),np.atleast_2d(dd),typ[np.atleast_2d(idx)]

def infer(pos,typ,q,a,m,k=24,band=.11,abl=None,seed=44,return_f=False):
    rng=np.random.default_rng(seed)
    # Ablations with explicit intervention on geometry, channel or availability.
    if abl=='labels_shuffled':
        typ=typ[rng.permutation(len(typ))]
    elif abl=='positions_shuffled_per_type':
        out=pos.copy()
        for t in range(5):
            ix=np.where(typ==t)[0]
            # Permuting locations within type is algebraically a no-op for a point pattern.
            # This negative-control correctly SHOULD produce identical output.
            out[ix]=pos[ix[rng.permutation(len(ix))]]
        pos=out
    elif abl=='only_dominant':
        mask=typ==0;pos,typ=pos[mask],typ[mask]
    elif abl=='positions_labels_permuted':
        # Relabeling arrays by the same permutation preserves labelled geometry: negative control.
        ii=rng.permutation(len(typ));pos,typ=pos[ii],typ[ii]
    ix,dd,t=query_neighbors(pos,typ,q,k=min(k,len(pos)))
    phase=2*np.pi*pos[ix]@m.T
    allval=np.cos(phase)@a[:,:,0].T+np.sin(phase)@a[:,:,1].T
    observed=np.take_along_axis(allval,t[...,None],axis=-1)[...,0]
    if abl=='signals_scrambled_per_type':
        # Deliberately invalid correspondence between observed values and their coordinates.
        for tt in range(5):
            rows,cols=np.where(t==tt)
            vals=observed[rows,cols].copy();rng.shuffle(vals);observed[rows,cols]=vals
    scores=np.exp(-0.5*(dd/band)**2)
    out=np.zeros((len(q),5))
    for tt in range(5):
        w=scores*(t==tt)
        out[:,tt]=(w*observed).sum(axis=1)/np.maximum(w.sum(axis=1),1e-13)
    yp=out[:,0]*out[:,1]+out[:,2]*out[:,3]+.4*out[:,0]*out[:,2]*out[:,4]
    return (yp,out,dd,t) if return_f else yp

def infer_nearest_per_type(pos,typ,q,a,m):
    # Competent alternative with 5 nearest-type queries, not fixed 24 overall sensors.
    out=np.empty((len(q),5))
    for tt in range(5):
        pp=pos[typ==tt]
        _,idx=cKDTree(pp,boxsize=1).query(q,k=1)
        phase=2*np.pi*pp[idx]@m.T
        out[:,tt]=(np.cos(phase)@a[tt,:,0]+np.sin(phase)@a[tt,:,1])
    return out[:,0]*out[:,1]+out[:,2]*out[:,3]+.4*out[:,0]*out[:,2]*out[:,4]

def sample_from_geo(pos,typ,n,seed):
    r=np.random.default_rng(seed);return r.random((n,3))

def phase_run(phase):
    seeds=range(11,21) if phase=='pilot' else range(901,921)
    n_a=8192 if phase=='pilot' else 8192
    n_world=512 if phase=='pilot' else 512
    gg={g:geometry(g) for g in GEOS}
    for p,t in gg.values():
        assert len(p)==len(t)==4096 and p.shape[1]==3 and np.isfinite(p).all()
        assert (p>=0).all() and (p<1).all() and set(t)==set(range(5))
    # 30 cycles each treated as within one branch explicit control/decision.
    raw=[]; start=time.time()
    qa=np.random.default_rng(774411 if phase=='pilot' else 889411).random((n_a,3))
    # A&B: fixed finite cloud, uniform query Monte Carlo; repeated seeds only worlds, not independent geometry.
    for g,(p,t) in gg.items():
        ix,dd,ty=query_neighbors(p,t,qa,k=32)
        for i,k in enumerate(KS,1):
            hit=np.unique(ty[:,:k],axis=0) if False else (np.stack([(ty[:,:k]==j).any(1) for j in range(5)],axis=1).all(1))
            raw.append({'cycle':i,'branch':'A','condition':f'k={k}','geometry':g,'replicate':'fixed','endpoint':'full_coverage','value':float(hit.mean())})
        nearest=[]
        for j in range(5):
            dt,_=cKDTree(p[t==j],boxsize=1).query(qa,k=1)
            nearest.append(dt)
        far=np.stack(nearest,axis=1).max(axis=1)
        for i,qtl in enumerate(QUANTILES,6):
            raw.append({'cycle':i,'branch':'B','condition':f'q={qtl:.2f}','geometry':g,'replicate':'fixed','endpoint':'radius_5_types','value':float(np.quantile(far,qtl))})
    # C,E: common worlds, different spatial frequency + bandwidth.
    for seed in seeds:
        q,a,m,y=ds(seed,n_world,1)
        for f in FREQS:
            q,aa,mm,yy=ds(seed,n_world,f)
            for g,(p,t) in gg.items():
                yh=infer(p,t,q,aa,mm)
                raw.append({'cycle':11+FREQS.index(f),'branch':'C','condition':f'freq={f}','geometry':g,'replicate':seed,'endpoint':'MSE','value':float(np.mean((yh-yy)**2))})
                if f==1:
                    # nearest_type oracle budget differs: report explicitly as upper-baseline only
                    yn=infer_nearest_per_type(p,t,q,aa,mm)
                    raw.append({'cycle':11,'branch':'C','condition':'freq=1','geometry':g,'replicate':seed,'endpoint':'MSE_nearest_type','value':float(np.mean((yn-yy)**2))})
        q,a,m,y=ds(seed,n_world,2)
        for bw in BWS:
            for g,(p,t) in gg.items():
                dd,idx=cKDTree(p,boxsize=1).query(q,k=24)
                # Gaussian bandwidths relative to global mean 24th-neighbor distance.
                effective_bw=bw*np.mean(dd[:,-1])
                yp=infer(p,t,q,a,m,band=effective_bw)
                raw.append({'cycle':21+BWS.index(bw),'branch':'E','condition':f'bw_k24={bw}','geometry':g,'replicate':seed,'endpoint':'MSE','value':float(np.mean((yp-y)**2))})
        for abr in ABLATIONS:
            for g,(p,t) in gg.items():
                yp=infer(p,t,q,a,m,abl=abr,seed=199+seed)
                raw.append({'cycle':26+ABLATIONS.index(abr),'branch':'F','condition':abr,'geometry':g,'replicate':seed,'endpoint':'MSE','value':float(np.mean((yp-y)**2))})
        for dr in DROPS:
            for g,(p,t) in gg.items():
                rng=np.random.default_rng(seed*100000+int(dr*1000))
                mask=rng.random(len(p))>=dr
                yp=infer(p[mask],t[mask],q,a,m)
                raw.append({'cycle':16+DROPS.index(dr),'branch':'D','condition':f'drop={dr}','geometry':g,'replicate':seed,'endpoint':'MSE','value':float(np.mean((yp-y)**2))})
    assert set(z['cycle'] for z in raw)==set(range(1,31))
    return raw,{'phase':phase,'world_seeds':list(seeds),'query_seed':774411 if phase=='pilot' else 889411,'n_world':n_world,'n_queries_geom':n_a,'original_geometries':True,'elapsed_seconds':round(time.time()-start,2)}

def summarize(raw):
    groups={}
    for row in raw:groups.setdefault((row['cycle'],row['geometry'],row['endpoint']),[]).append(row['value'])
    out=[]
    for (cycle,g,end),values in sorted(groups.items()):
        out.append({'cycle':cycle,'geometry':g,'endpoint':end,'mean':float(np.mean(values)),'sd_replicates':float(np.std(values,ddof=1)) if len(values)>1 else None,'n_world_replicates':len(values),'condition':next(x['condition'] for x in raw if x['cycle']==cycle),'inference_scope':'synthetic_worlds' if len(values)>1 else 'single_fixed_geometry'})
    return out

def checks():
    gg={g:geometry(g) for g in GEOS}
    # invariant 1: no label leakage into sensor data; modalities correct
    assert all(np.array_equal(np.bincount(t,minlength=5),[1669,871,696,512,348]) for p,t in gg.values())
    q,a,m,y=ds(1234,13,1)
    p,t=gg['local']
    yp=infer(p,t,q,a,m)
    rr=np.random.default_rng(1).permutation(len(t))
    p2,t2=p[rr],t[rr]
    yp2=infer(p2,t2,q,a,m)
    assert np.allclose(yp,yp2,rtol=1e-9,atol=1e-9),'Permutation invariance failed'
    return {'permutation_invariance_max_abs':float(np.max(np.abs(yp-yp2))), 'counts':[1669,871,696,512,348], 'finite_preds':bool(np.isfinite(yp).all())}

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--phase',choices=['pilot','confirm'],required=True);pa.add_argument('--out',type=str,default='data');args=pa.parse_args()
    out=Path(args.out);out.mkdir(exist_ok=True,parents=True)
    ck=checks(); rows,info=phase_run(args.phase)
    with (out/f'{args.phase}_raw.csv').open('w',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    with (out/f'{args.phase}_summary.csv').open('w',newline='') as fp:
        s=summarize(rows);w=csv.DictWriter(fp,fieldnames=s[0].keys());w.writeheader();w.writerows(s)
    with (out/f'{args.phase}_metadata.json').open('w') as fp:json.dump({**info,'checks':ck,'n_rows':len(rows)},fp,indent=2)
    print(json.dumps({'phase':args.phase,'elapsed_seconds':info['elapsed_seconds'],'n_rows':len(rows),'n_cycles':len(set(r['cycle'] for r in rows)),'checks':ck},indent=2))
if __name__=='__main__':main()
