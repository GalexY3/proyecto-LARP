"""POST-OUTCOME audit LARP trained graph benchmark L01-L20. Exploratory descriptive analysis only."""
import json,glob,hashlib,platform,sys,collections
from pathlib import Path
import numpy as np,pandas as pd

DIR=Path(__file__).resolve().parent
CELLS=DIR/'cells';REPLAY=DIR/'replay'
CONTEXTS=['low','high','correlated','anticorrelated','localized'];SHIFTS=['clean','drop20','rare_drop40','noise15']
GSEEDS=[3011,3023]; FSEEDS=list(range(52101,52117))
METHODS=['grid_knn','cvt_knn','mhu_knn','grid_type','cvt_type','mhu_type','grid_learned','cvt_learned','mhu_learned']

allrows=[];alltrain=[];alledge=[];hashes=[]
for g in GSEEDS:
 for c in CONTEXTS:
  path=CELLS/f'cell_{g}_{c}.json';replay=REPLAY/path.name
  a=json.loads(path.read_bytes());b=json.loads(replay.read_bytes())
  elapsed=a.pop('elapsed_sec');b.pop('elapsed_sec')
  assert a==b, 'replay mismatch '+str(path)
  assert len(a['records'])==len(FSEEDS)*len(SHIFTS)*len(METHODS)==576
  assert len(a['training_diagnostics'])==len(METHODS)
  assert len(a['geometry_diagnostics'])==len(METHODS)
  assert all(row['geometry_seed']==g and row['context']==c for row in a['records'])
  assert set(row['field_seed'] for row in a['records'])==set(FSEEDS)
  assert set(row['method'] for row in a['records'])==set(METHODS)
  assert set(row['shift'] for row in a['records'])==set(SHIFTS)
  assert len(set((row['field_seed'],row['method'],row['shift']) for row in a['records']))==576
  assert len(set(x['parameters'] for x in a['training_diagnostics']))==1
  assert all(0<=x['best_epoch']<12 for x in a['training_diagnostics'])
  assert all(0<x['mean_type_coverage']<=1 and 0<x['mean_edge_length']<.71 for x in a['geometry_diagnostics'])
  allrows.extend(a['records']);alltrain.extend(a['training_diagnostics']);alledge.extend(a['geometry_diagnostics'])
  hashes.append(dict(name=path.name,first_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),replay_sha256=hashlib.sha256(replay.read_bytes()).hexdigest(),same_except_elapsed=True,
                     first_elapsed_sec=elapsed,replay_elapsed_sec=b.get('elapsed_sec')))
df=pd.DataFrame(allrows)
assert len(df)==5760 and np.isfinite(df.nmse).all() and (df.nmse>=0).all()
assert df.groupby(['cycle','method']).size().eq(32).all()
assert len(df.groupby(['cycle']).size())==20
assert len(alltrain)==90 and len(alledge)==90

base=df.groupby(['cycle','context','shift','method'],as_index=False).nmse.mean()
wide=base.pivot_table(index=['cycle','context','shift'],columns='method',values='nmse').reset_index()
pairs=[('mhu_type','cvt_type'),('mhu_learned','cvt_learned'),('mhu_learned','mhu_type'),('mhu_type','mhu_knn'),('cvt_type','cvt_knn')]
for a,b in pairs:
 wide[f'diff_{a}_minus_{b}']=wide[a]-wide[b]

# Cluster field seed (two geometry seeds averaged for each field seed); bootstrap illustrative, no confirmatory p-values.
rng=np.random.default_rng(20261030)
contrasts=[]
for a,b in pairs:
 d=df[df.method.isin((a,b))].pivot_table(index=['cycle','field_seed','geometry_seed'],columns='method',values='nmse').reset_index()
 diffs=(d[a]-d[b]).groupby(d['field_seed']).mean().reindex(FSEEDS).to_numpy()
 draws=rng.integers(0,len(diffs),size=(4000,len(diffs)))
 means=diffs[draws].mean(axis=1)
 contrasts.append(dict(preference=f'{a} minus {b}',mean_delta=float(diffs.mean()),ci95_descriptive=[float(np.quantile(means,.025)),float(np.quantile(means,.975))],n_distinct_field_seeds=16,n_geometry_seeds=2,
    favorable_conditions=int((wide[a]<wide[b]).sum()),unfavorable_conditions=int((wide[a]>wide[b]).sum()),ties=int((wide[a]==wide[b]).sum())))

methodmeans=df.groupby('method').nmse.agg(['mean','median']).sort_values('mean').reset_index()
geometry=pd.DataFrame(alledge).groupby('method')[['mean_edge_length','mean_type_coverage']].mean().reset_index()
contextmeans=df.groupby(['context','method']).nmse.mean().reset_index()
model=pd.DataFrame(alltrain)
stat={
 'status':'COMPLETE_SYNTHETIC_WITH_DOCUMENTED_RESOURCE_REPAIR',
 'n_rows':len(df),'n_conditions':len(wide),'n_models_trained':len(alltrain),'n_geometry_diagnostics':len(alledge),
 'n_field_seeds_heldout':len(FSEEDS),'n_geometry_seeds':len(GSEEDS),'n_train_seeds':24,'n_validation_seeds':6,
 'methods':METHODS,'run_replay':{'exact_except_elapsed':all(v['same_except_elapsed'] for v in hashes),'cells':len(hashes),'file_checksums':hashes},
 'method_means':methodmeans.to_dict('records'),
 'geometry_means':geometry.to_dict('records'),
 'context_means':contextmeans.to_dict('records'),
 'paired_contrasts':contrasts,
 'best_per_condition':wide.set_index('cycle')[METHODS].idxmin(axis=1).value_counts().to_dict(),
 'parameter_counts':model.parameters.unique().tolist(),'best_val_epoch_range':[int(model.best_epoch.min()),int(model.best_epoch.max())],
 'scope_limitations':['Finite MHU/CVT proxies, original avian geometries not downloaded','Synthetic shared generator, not external data','No trained state-dependent graph attention','Learned graphs use supervised TRAIN targets, extra design compute','20 task cells dependent, 16 field draws from same generator','Software same-host replay only'],
 'versions':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__}}
(DIR/'audit.json').write_text(json.dumps(stat,indent=2,ensure_ascii=False)+'\n')
base.to_csv(DIR/'per_condition.csv',index=False)
wide.to_csv(DIR/'paired_conditions.csv',index=False)
methodmeans.to_csv(DIR/'method_means.csv',index=False)
geometry.to_csv(DIR/'geometry_means.csv',index=False)
model.to_csv(DIR/'training_diagnostics.csv',index=False)
df.to_csv(DIR/'all_predictions.csv',index=False)

ledger=[]
for _,r in wide.iterrows():
 task=str(r.cycle)
 d={key:float(r[key]) for key in METHODS}
 better=min(d,key=d.get)
 ledger.append(dict(id=task,mode='AB-R',status='RUN_VALID_SYNTHETIC_CONDITION',grade='0/3',new_n1=False,new_n2=False,new_n3=False,
    A=dict(estimand='heldout normalized MSE per field seed and geometry for five-mode distributed sensing',context=r.context,shift=r['shift'],primary_unit='synthetic field seed, not 400 node positions'),
    B=dict(rivals=METHODS,hypothesis='task-supervised router vs fixed-nearest and class-covered; finite MHU proxy vs CVT/grid'),
    C=dict(preregister='PREREG_L01_L20.md',predeclared_pairings=pairs,geometry_seeds=GSEEDS,heldout_field_seeds=FSEEDS),
    D=dict(freeze_code_sha256='320bab4445e5e381b9378b681940ada89fe6df74086c4c0f9a1b8e51b2d7b031',freeze_wrapper_sha256='4291e004a747718b0d30f3ca28d4a7dd8175960adee336c8ab56af55ccf6f634',resource_errata='ERRATA_RESOURCE_CAP.md'),
    E=dict(all_nmse=d,winner=better,primary_delta_mhu_learned_minus_cvt_learned=float(r.mhu_learned-r.cvt_learned),primary_delta_mhu_type_minus_cvt_type=float(r.mhu_type-r.cvt_type)),
    F=dict(adversarial='Same synthetic source and shared field seeds; graph design training cost differs; geometry families are proxies; long edges on learned graph; no actual trained MoE, no new external baseline implementation.'),
    G=dict(replay='IDENTICAL_AFTER_ELAPSED_SEC_REMOVAL',external_replication=False,holdout='new_field_seeds_same_generating_process'),
    H=dict(updated_prior='MHU geometric spectral criterion not transferred to superior learned network performance; learned correlation graph overfits and takes longer edges in this finite scenario.'),
    I=dict(internal_status='VALID_WITHIN_SIMULATOR',causal_external='NONE',novelty='NOT_ORIGINAL',information_parity='Same 1 scalar/sensor + six incoming edges; learned graph has additional supervised training and edge length not matched'),
    J=dict(decision='STOP_LOCAL_FOR_THIS_GENERATOR',next_evidence='native LARP NPZ and real five-channel dataset; compare learned graph attention strong baseline before novelty claim')))
(DIR/'LEDGER_L01_L20.json').write_text(json.dumps({'date':'2026-10-30','grant':20,'completed_condition_cycles':20,'invalid_scientific_cycles':0,'incomplete_runs_documented':1,'new_unique_N1':0,'N2':0,'N3':0,'dependent_design':True,'cycles':ledger},indent=2,ensure_ascii=False)+'\n')
print('AUDIT_PASS','records',len(df),'cells',len(hashes),'models',len(alltrain),'replay',stat['run_replay']['exact_except_elapsed'])
print('paired',[(r['preference'],round(r['mean_delta'],4),r['favorable_conditions']) for r in contrasts])
print('SHA',hashlib.sha256((DIR/'audit.json').read_bytes()).hexdigest())
