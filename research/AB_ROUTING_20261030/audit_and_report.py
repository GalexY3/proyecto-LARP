"""POST-OUTCOME descriptive audit for preregistered F01-F30. No new cycle."""
from pathlib import Path
import numpy as np, pandas as pd, json, hashlib, importlib.util
ROOT=Path(__file__).resolve().parent
raw=json.loads((ROOT/'run1/results.json').read_text())
r=pd.DataFrame(raw['records']);g=pd.DataFrame(raw['graph_diagnostics'])
assert len(r)==12960 and r[['cycle_id','seed','field_seed','method','hop']].duplicated().sum()==0
assert r.groupby(['cycle_id','method','hop']).size().eq(24).all()
assert sorted(r.cycle_id.unique())==[f'R{i:02d}' for i in range(1,31)]
assert sorted(r.method.unique())==sorted(raw['methods'])
assert r.nmse.notna().all() and np.isfinite(r.nmse).all() and r.nmse.ge(0).all()
assert r.coverage.between(0,1).all()
a=r.pivot(index=['cycle_id','seed','field_seed','hop'],columns='method',values='nmse')
assert np.array_equal(a['mhu_type'].to_numpy(),a['mhu_hybrid'].to_numpy())
paired=a.reset_index().query('hop==1').groupby('cycle_id').agg(mhu=('mhu_type','mean'),mhu_local=('mhu_knn','mean'),cvt=('cvt_type','mean'),cvtlocal=('cvt_knn','mean'),grid=('grid_type','mean'),expander=('expander_deg6','mean'))
paired['gain_routing_mhu']=paired.mhu_local-paired.mhu
paired['difference_mhu_cvt']=paired.mhu-paired.cvt
paired['winner']=paired[['mhu','mhu_local','cvt','cvtlocal','grid','expander']].idxmin(1)
assert (paired.difference_mhu_cvt>0).all()
contexts=r[['cycle_id','context','shift']].drop_duplicates().set_index('cycle_id')
paired=contexts.join(paired)
# graph structural diagnostics and Fourier/cover posthoc
spec=importlib.util.spec_from_file_location('ab30',ROOT/'ab30_functional.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
params=[]
for seed in m.GEOM_SEEDS:
    lab=m.labels_for_seed(seed)
    p0=np.column_stack(np.meshgrid((np.arange(20)+.5)/20,(np.arange(20)+.5)/20)).reshape(2,-1).T # not used
    xx,yy=np.meshgrid((np.arange(20)+.5)/20,(np.arange(20)+.5)/20)
    P={'grid':np.column_stack([xx.ravel(),yy.ravel()]),'cvt':m.cvt_geometry(seed,lab),'mhu_proxy':m.optimize_mhu(seed,lab)}
    sample=np.random.default_rng(seed+101).random((3000,2))
    for name,p in P.items():
        z=np.exp(2j*np.pi*(p@m.MODES.T))
        u=N=len(p)
        union=float(N*np.mean(np.abs(z.mean(0))**2))
        typ=float(np.mean([len(z[lab==c])*np.mean(np.abs(z[lab==c].mean(0))**2) for c in range(5)]))
        q=[];rc=[]
        from scipy.spatial import cKDTree
        for c in range(5):
            dd,_=cKDTree(p[lab==c],boxsize=1).query(sample)
            q.append(float(np.mean(dd*dd)));rc.append(float(np.quantile(dd,.95)))
        params.append(dict(seed=seed,geometry=name,S_union=union,S_type_mean=typ,CVT_class_Q=float(np.mean(q)),class_r95=float(np.mean(rc))))
params=pd.DataFrame(params)
# audit exact redundancy edges not merely same MSE
for seed in m.GEOM_SEEDS:
    lab=m.labels_for_seed(seed);p=m.optimize_mhu(seed,lab)
    a1=m.make_edges(p,lab,'type',seed);a2=m.make_edges(p,lab,'hybrid',seed)
    assert all(set(x)==set(y) for x,y in zip(a1,a2))
result={
 'source_code_sha256':hashlib.sha256((ROOT/'ab30_functional.py').read_bytes()).hexdigest(),
 'prereg_commit':'4bb177d378eb12fe3f376c58a574cd0d75939f34',
 'source_frozen_commit':'a620c5c912cf1c34e7f898287451439c28908157',
 'raw_results_sha256':hashlib.sha256((ROOT/'run1/results.json').read_bytes()).hexdigest(),
 'exact_replay_match':(ROOT/'run1/results.json').read_bytes()==(ROOT/'run2/results.json').read_bytes(),
 'data_rows':len(r),'total_cells':30,'n_geom_seeds':3,'n_field_seeds':8,
 'mhu_routing_better_than_knn_cells':int((paired.gain_routing_mhu>0).sum()),
 'mhu_routing_worse_than_knn_cells':int((paired.gain_routing_mhu<0).sum()),
 'mhu_type_beats_cvt_type_cells':int((paired.difference_mhu_cvt<0).sum()),
 'cvt_type_wins_all_methods_cells':int((paired.winner=='cvt').sum()),
 'cell_winners':paired.winner.value_counts().to_dict(),
 'nmse_means_hop1':r[r.hop==1].groupby('method').nmse.mean().to_dict(),
 'nmse_means_hop2':r[r.hop==2].groupby('method').nmse.mean().to_dict(),
 'structural':g.groupby(['method','hop']).agg(availability=('availability','mean'),edge_dist=('edge_dist','mean')).reset_index().to_dict('records'),
 'geometry_audit':params.to_dict('records'),
 'adversarial_flags':[
 'mhu_type and mhu_hybrid have EXACTLY identical unordered neighbor sets for all 1200 nodes, although row ordering differs: remove independent-hybrid claim',
 'MHU is optimized finite spectral SURROGATE, not LARP native Scale3D MHU geometry',
 'CVT is type-Lloyd proxy; LOCAL original was not executed',
 'degree-regular randomly-relabeled circulant is not a validated expander',
 'all fields, targets, shifts are synthetic and scripted; no independent replication',
 'same estimator used in all arms, but no trainable learned routing baseline or hardware-equated link geometry',
 'each context/shift cell uses identical geometry/field seeds: 30 related contrasts not 30 independent datasets',
 'dropout nearest accessible class chosen BEFORE failure, so algorithms do not recover by trying alternate reachable sources',
 '5 modality weights known to all estimators; anti-correlated targets can have small variance and relatively high NMSE',
 'geometry optimization and link-construction costs differ and are not budget matched'
 ]}
(ROOT/'audit.json').write_text(json.dumps(result,indent=2))
paired.reset_index().to_csv(ROOT/'all30.csv',index=False)
params.to_csv(ROOT/'geometry_diagnostics.csv',index=False)
print(json.dumps({k:result[k] for k in ['data_rows','total_cells','mhu_routing_better_than_knn_cells','mhu_routing_worse_than_knn_cells','mhu_type_beats_cvt_type_cells','cvt_type_wins_all_methods_cells','cell_winners','exact_replay_match']},indent=2))
print('\nGEOMETRY AUDIT')
print(params.groupby('geometry')[['S_union','S_type_mean','CVT_class_Q','class_r95']].mean().round(5))
