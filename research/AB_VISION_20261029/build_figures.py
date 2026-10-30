import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
p=Path(__file__).parent
m=json.loads((p/'c04_means.json').read_text())
methods=['grid','poisson_disk','sobol','spectral_joint','spectral_sub','joint_phase_broken','supervised_kbest','full_pixels']
labels=['Cuadrícula','Poisson-disk','Sobol','MHU conjunta','MHU por tipos','Fases alteradas','Selección ANOVA','Imagen completa']
cond=['clean','noise13','occlusion6']
condlab=['Normal','Ruido','Oclusión']
fig,ax=plt.subplots(figsize=(10,5))
x=np.arange(len(methods));w=.25
for j,c in enumerate(cond):
 v=[100*next(q['accuracy'] for q in m if q['method']==me and q['condition']==c) for me in methods]
 ax.bar(x+(j-1)*w,v,w,label=condlab[j])
ax.set_xticks(x,labels,rotation=30,ha='right');ax.set_ylim(85,100)
ax.set_ylabel('Aciertos (%)');ax.set_title('LARP-Visión C04 · 200 imágenes LFW, 160 lecturas (excepto imagen completa)')
ax.legend();fig.tight_layout();fig.savefig(p/'C04_RESULTADOS.png',dpi=160);plt.close(fig)
points=[('Inicio C01',22),('Tras C01',17),('Tras C02',13),('Tras C04',11)]
for name,ylim in [('CT2_0_100',(0,100)),('CT2_ZOOM',(8,25))]:
 fig,ax=plt.subplots(figsize=(8,4))
 ax.plot([i for i,(s,v) in enumerate(points)],[v for s,v in points],marker='o',lw=2)
 ax.set_xticks(np.arange(len(points)),[p[0] for p in points]);ax.set_ylim(*ylim);ax.set_ylabel('CT2 ordinal');ax.set_title('LARP-Visión · confianza en trayectoria a 2/3')
 for i,(_,v) in enumerate(points): ax.annotate(str(v), (i,v),xytext=(0,10),textcoords='offset points',ha='center')
 ax.grid(alpha=.25);fig.tight_layout();fig.savefig(p/(name+'.png'),dpi=160);plt.close(fig)
(p/'CT2_TRAJECTORY.json').write_text(json.dumps([{'stage':s,'ct2':v,'scale':'ordinal, not probability'} for s,v in points],indent=2))
