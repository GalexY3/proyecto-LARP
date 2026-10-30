"""POST-HOC audit; descriptive clustering by image, NOT extra AB cycle."""
import json, hashlib, collections
import numpy as np
from pathlib import Path
from scipy.spatial import cKDTree
P=Path(__file__).resolve().parent
r=json.loads((P/'c04_results.json').read_text())
obs=r['observations']; assert len(obs)==32400,len(obs)
methods=r['methods']; cond=['clean','noise13','occlusion6']
agg=collections.defaultdict(list)
for a in obs:
 agg[a['method'],a['condition'],a['image_id']].append(a['correct'])
assert len(agg)==len(methods)*len(cond)*200
assert {len(v) for v in agg.values()}=={6}, {len(v) for v in agg.values()}
means={m:{c:float(np.mean([np.mean(agg[m,c,i]) for i in range(200)])) for c in cond} for m in methods}
rng=np.random.default_rng(20261029);indices=rng.integers(0,200,size=(8000,200))
contrasts=[]
for c in cond:
 for opponent in ['grid','poisson_disk','sobol','spectral_sub','joint_phase_broken','random','supervised_kbest','full_pixels']:
  d=np.asarray([np.mean(agg['spectral_joint',c,i])-np.mean(agg[opponent,c,i]) for i in range(200)])
  bs=d[indices].mean(1)
  contrasts.append({'condition':c,'opponent':opponent,'mhu_minus_rival_pp':float(100*d.mean()),
                   'bootstrap_95_pp':list(np.percentile(100*bs,[2.5,97.5])),
                   'per_image_positive':int((d>0).sum()),'per_image_negative':int((d<0).sum()),
                   'per_image_equal':int((d==0).sum())})
out={'metrics':means,'contrasts':contrasts,'n_independent_images_upper_bound':200,'observations':len(obs),
     'geometric_seeds':r['seeds'],'folds':r['fold_random_states'],'bootstrap_reps':8000,
     'notes':['CI descriptive and unadjusted for multiple contrasts','LFW 100 faces and 100 nonfaces from same wider source; nonindependence possible',
              'The 160 bilinear samples may involve up to four nearby pixels each; not 160 original pixels',
              'No independent external replication or geometric MHU certification','Grid already near accuracy ceiling; classification insensitive to sampling placement',
              'ANOVA KBest is not a powerful modern learned sparse sampling rival',
              'All methods use identical SVC except full_pixels (625 original pixels), supervised_kbest (training label-selected 160 exact original pixels)']}
(P/'c04_audit.json').write_text(json.dumps(out,indent=2))
print('SourceSHA',r['source_image_sha256'])
print('Coverage',len(obs),'expected',len(methods)*len(cond)*200*6)
for c in cond:
 print('\n',c)
 for m in methods:print(f'{m:25} {means[m][c]*100:.3f}')
 for o in ['grid','poisson_disk','spectral_sub','joint_phase_broken','full_pixels']:
  x=next(x for x in contrasts if x['condition']==c and x['opponent']==o)
  print(' DELTA joint-',o,round(x['mhu_minus_rival_pp'],3),'pp',tuple(round(z,3) for z in x['bootstrap_95_pp']))
print('RESULTS-SHA',hashlib.sha256((P/'c04_results.json').read_bytes()).hexdigest())
