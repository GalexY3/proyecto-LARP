import json,hashlib,platform,sys,pathlib
import numpy as np,pandas as pd,matplotlib.pyplot as plt
R=pathlib.Path(__file__).resolve().parent
raw=(R/'results_c02.json').read_bytes();r=json.loads(raw)
df=pd.DataFrame(r['observations']);g=pd.DataFrame(r['geometry']);
assert len(df)==4*6*9*3, len(df)
assert set(df.condition)=={'clean','drop20','noise03'}
assert len(g)==4*6
means=df.groupby(['split','method','condition']).agg(mse=('mse','mean'),mae=('mae','mean'),n=('mse','size')).reset_index()
means.to_csv(R/'C02_MEANS.csv',index=False)
novel=df[df.image.isin(['retina','stereo_motorcycle'])]
summary={'code_sha256':hashlib.sha256((R/'vision_ab_c02.py').read_bytes()).hexdigest(),
         'results_sha256':hashlib.sha256(raw).hexdigest(),
         'count_rows':len(df),'measured_scenes':len(set(df.image)),
         'test_scenes':r['test'],'genuinely_novel_to_C01':['retina','stereo_motorcycle'],
         'spectral_pair_ablation_exact':bool(np.allclose(
             g[g.method=='spectral_joint'].sort_values('seed').low_k_sub.to_numpy(),
             g[g.method=='joint_phase_broken'].sort_values('seed').low_k_sub.to_numpy(),rtol=1.e-9,atol=1e-12)),
        'mse_means':{},'relative_performance_clean':{}}
for split in ['TEST','DEV','STRESS']:
  z=means[means.split==split].pivot(index='method',columns='condition',values='mse')
  summary['mse_means'][split]={method:{k:float(row[k]) for k in z.columns} for method,row in z.iterrows()}
for group,names in [('test_all',r['test']),('test_new2',['retina','stereo_motorcycle'])]:
  z=df[(df.image.isin(names)) & (df.condition=='clean')].pivot_table(index='image',columns='method',values='mse')
  for rival in ['spectral_sub','joint_phase_broken','grid_balanced','poisson_multiclass_proxy','sobol_balanced']:
    delta=z['spectral_joint']-z[rival]
    summary['relative_performance_clean'][group+'_'+rival]={'delta_abs':float(delta.mean()),'delta_pct':float(delta.mean()/z[rival].mean()*100),'image_wins':int((delta<0).sum()),'n_images':int(len(delta))}
(R/'C02_AUDIT.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
fig,ax=plt.subplots(figsize=(11,5.4))
methods=['poisson_multiclass_proxy','grid_balanced','sobol_balanced','spectral_sub','joint_phase_broken','spectral_joint']
cols=['clean','drop20','noise03'];z=means[means.split=='TEST'].pivot(index='method',columns='condition',values='mse')
x=np.arange(6);w=.26
for i,c in enumerate(cols):ax.bar(x+(i-1)*w,[z.loc[m,c] for m in methods],w,label=c)
ax.set_xticks(x,[m.replace('poisson_multiclass_proxy','Poisson multi').replace('grid_balanced','Cuadrícula').replace('sobol_balanced','Sobol').replace('spectral_sub','Espectral por tipo').replace('joint_phase_broken','Fases rotas').replace('spectral_joint','Espectral conjunta') for m in methods],rotation=15,ha='right')
ax.set_ylabel('MSE RGB medio (menor es mejor)');ax.set_title('C02 · cinco filtros virtuales RGB · 160 lecturas · cuatro imágenes TEST');ax.legend();fig.tight_layout();fig.savefig(R/'C02_COMPARACIONES.png',dpi=180);plt.close(fig)
# CT2 same branch continuation: C01 22->17; C02 17->13. Ordinal internal score, not probability.
xs=[0,1,2];y=[22,17,13]
for fn,ylim in [('C02_CT2_ESCALA_100.png',(0,100)),('C02_CT2_ZOOM.png',(8,26))]:
 fig,ax=plt.subplots(figsize=(7.5,4));ax.plot(xs,y,marker='o');ax.set(xticks=xs,xticklabels=['Diseño C01','Tras C01','Tras C02'],ylabel='CT2 ordinal (1–100)',ylim=ylim,title='LARP visión · Trayectoria CT2, no probabilidad');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(R/fn,dpi=170);plt.close(fig)
print(json.dumps(summary,ensure_ascii=False,indent=2)[:6600])
