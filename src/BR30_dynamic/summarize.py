from pathlib import Path
import json, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import t
D=Path(__file__).resolve().parent/'data'; OUT=Path(__file__).resolve().parent
seeds=[5201,5202,5203,5204];rows=[]; georows=[]
for s in seeds:
 rows+=json.loads((D/f'predictive_eval_{s}.json').read_text())
 georows+=json.loads((D/f'geometry_eval_{s}.json').read_text())
names=['initial','local','mhu','cvt_refined_1701','cvt_refined_1702','cvt_refined_1703'];
summary={}
for d in ['none','iid40','hole18','hole28']:
 for f in [1,2,4]:
  k=f'{d}|f{f}';summary[k]={}
  for name in names:
   by=[]
   for s in seeds:
    scores=[x['mse'] for x in rows if x['seed']==s and x['deletion']==d and x['freq']==f and x['name']==name]
    by.append(float(np.mean(scores)))
   summary[k][name]={'seed_means':by,'mean':float(np.mean(by)),'sd_across_seeds':float(np.std(by,ddof=1))}
geom={}
for name in names:
 arr=[x for x in georows if x['name']==name]
 geom[name]={key:float(np.mean([r[key] for r in arr])) for key in ['cover_8','cover_12','cover_16','cover_24','S_union','r5_mean']}
contrasts={}
for d in ['none','iid40','hole18','hole28']:
 for f in [1,2,4]:
  key=f'{d}|f{f}';u=np.array(summary[key]['local']['seed_means']);v=np.array(summary[key]['mhu']['seed_means']);dd=v-u
  ci=t.interval(.95,len(dd)-1,loc=dd.mean(),scale=dd.std(ddof=1)/np.sqrt(len(dd)))
  contrasts[key]={'MHU_minus_LOCAL':float(dd.mean()),'CI95_across_4_geo_seed_means':list(map(float,ci)), 'individual_paired_differences':dd.tolist()}
report={'description':'Exploratory. Four paired original Scale3D seeds, six synthetic worlds per seed. CVT references are three geometries reused for each original seed; not independent of group-level repeated sampling. No Wei algorithm.', 'seeds':seeds,'geometry':geom,'predictions':summary,'pairwise_differences':contrasts}
(D/'combined_summary.json').write_text(json.dumps(report,indent=2))
for f in [1,2,4]:
 for d in ['none','hole28']:
  print('F',f,d,[(n,round(summary[f'{d}|f{f}'][n]['mean'],4)) for n in names])
print('Geom',[(n,round(x['cover_16'],4),round(x['S_union'],7)) for n,x in geom.items()]); print('pairwise',json.dumps(contrasts['hole28|f1']))

# One plot for each metric as separate figure: no subplots.
for d,filename,title in [('none','mse_smooth_baseline.png','Composición espacial suave, sin perturbación'),('hole28','mse_smooth_hole28.png','Composición espacial suave, agujero de radio 0,28')]:
 labels=['RANDOM','LOCAL','MHU','CVT-A','CVT-B','CVT-C']; vals=[summary[f'{d}|f1'][n]['mean'] for n in names]
 fig,ax=plt.subplots(figsize=(8,4.5))
 ax.bar(labels,vals,color=['#bbbbbb','#3c78a8','#916bc2','#d5a64c','#d5a64c','#d5a64c'])
 ax.set_title(title);ax.set_ylabel('Error cuadrático medio (MSE, menor mejor)');ax.grid(axis='y',alpha=.15)
 fig.tight_layout();fig.savefig(OUT/filename,dpi=160);plt.close(fig)
