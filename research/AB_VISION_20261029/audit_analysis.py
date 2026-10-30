"""Post-exposure descriptive audit; not preregistered statistical inference."""
from pathlib import Path
import json, hashlib
import pandas as pd,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
r=json.loads((ROOT/'results_repaired.json').read_text());d=pd.DataFrame(r['results']);g=pd.DataFrame(r['geometry']);
t=d[d.split=='TEST'].copy()
metrics=t.groupby(['condition','method'])['mse'].mean().unstack()
metrics.to_csv(ROOT/'MSE_TEST_TABLE.csv')
comparisons=[];rng=np.random.default_rng(4224)
for cond in ['clean','drop30','noise08']:
 p=t[t.condition==cond].pivot_table(index=['image','seed'],columns='method',values='mse')
 for b in ['mhu_subtypes','grid','sobol','poisson_disk','cvt_subtypes']:
  df=(p['mhu_joint']-p[b]).groupby(level='image').mean().reindex(r['test']).to_numpy()
  # Resample images, the only plausible independent clusters: descriptive, not CI confirmed.
  ix=rng.integers(0,len(df),(20000,len(df)))
  boot=np.mean(df[ix],axis=1)
  comparisons.append({'condition':cond,'contrast':'mhu_joint - '+b,'effect_mean_mse':float(np.mean(df)),
                      'pct_relative':float(np.mean(df)/metrics.loc[cond,b]*100),
                      'images_joint_better':int((df<0).sum()),
                      'n_images':len(df),'bootstrap_p025':float(np.quantile(boot,.025)),
                      'bootstrap_p975':float(np.quantile(boot,.975))})
(ROOT/'CONTRASTS_CLUSTER_BOOTSTRAP.csv').write_text(pd.DataFrame(comparisons).to_csv(index=False))
fig,ax=plt.subplots(figsize=(11,5.2)); labels=['Cuadrícula','Poisson-disk reparado','MHU espectral conjunta','Espectral por tipos','Sobol','CVT por tipos'];methods=['grid','poisson_disk','mhu_joint','mhu_subtypes','sobol','cvt_subtypes']
x=np.arange(6);width=.25
for i,(c,cn) in enumerate([('clean','Normal'),('drop30','30 % lecturas perdidas'),('noise08','Ruido')]):
    ax.bar(x+(i-1)*width,[metrics.loc[c,m] for m in methods],width,label=cn)
ax.set_xticks(x,labels,rotation=18,ha='right');ax.set_ylim(0,.021)
ax.set_ylabel('MSE de reconstrucción (menor = mejor)');ax.set_title('LARP VISIÓN: contraste exploratorio (nueve imágenes de origen)');ax.legend(frameon=False,loc='upper left');fig.tight_layout();fig.savefig(ROOT/'RESULTADOS_MSE.png',dpi=180);plt.close(fig)
# O6: plot true ordinal records only, before/after as expert judgment not discovered score
fig,ax=plt.subplots(figsize=(7,3.8));ax.plot(['Diseño','Auditoría'],[22,17],'-o');ax.set_ylim(0,100);ax.set_yticks([0,20,40,60,80,100]);ax.set_title('CT2 — línea LARP visión (escala 0–100)');ax.set_ylabel('Juicio ordinal, NO probabilidad');fig.tight_layout();fig.savefig(ROOT/'CT2_COMPLETA.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(7,3.8));ax.plot(['Diseño','Auditoría'],[22,17],'-o');ax.set_ylim(14,25);ax.set_title('CT2 — detalle ampliado (14–25)');ax.set_ylabel('Juicio ordinal, NO probabilidad');fig.tight_layout();fig.savefig(ROOT/'CT2_ZOOM.png',dpi=180);plt.close(fig)
(ROOT/'CT2_TRAJECTORY.json').write_text(json.dumps({'branch':'VISION_C01','ordinal_nonprobabilistic':True,'points':[{'stage':'BEFORE','score':22,'evidence':'Initial prior-art burden; clear hypothesis but no independent dataset'},{'stage':'AFTER','score':17,'evidence':'No material improvement over grid/Poisson; no genuine multicolor sensing or neural downstream; current proxy fails novelty gate'}]},indent=2))
print('hashes',[(v,hashlib.sha256((ROOT/v).read_bytes()).hexdigest()) for v in ['vision_ab_c01.py','results_original.json','repair_poisson.py','results_repaired.json']]);
print(pd.DataFrame(comparisons).to_string(index=False,float_format=lambda x:f'{x:.7f}'))
