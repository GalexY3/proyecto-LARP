"""Plots from frozen JSON only; no recomputation or model selection."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent
S=json.loads((P/'pilot_quota_results.json').read_text())['summary']
xx=np.array([12,28,88,300,1800]);fig,ax=plt.subplots(figsize=(9.6,5.7))
for name,label in [('COSI-SHRINK','COSI regularizado'),('DIRECT-EMPIRICAL','Optimización directa'),('POWER-DIAG','Espectro por canal'),('SOBOL','Sobol')]:
 yy=[.5*(S[str(n)][name]['rocket']+S[str(n)][name]['hubble']) for n in xx]
 ax.plot(xx,yy,'o-',label=label)
ax.set(xscale='log',xlabel='Parches piloto disponibles (escala logarítmica)',ylabel='RMSE medio descriptivo (dos escenas)',title='Baja disponibilidad de datos piloto · 24 sensores, cuotas 6/16/2')
ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(P/'fig_pilot_scarcity.png',dpi=175);plt.close(fig)
Q=json.loads((P/'quota_ablations_results.json').read_text())['summary']
fig,ax=plt.subplots(figsize=(10.6,5.8))
qorder=['8/8/8','6/12/6','4/16/4','4/12/8','10/12/2','6/16/2','4/18/2','2/20/2']
for name,label in [('SOBOL','Sobol'),('POWER-DIAG','Espectro por canal'),('COSI-SHRINK','COSI regularizado')]:
 yy=[next(v['mean_of_two_scenes'] for v in Q if '/'.join(map(str,v['quotas']))==q and v['method']==name) for q in qorder]
 ax.plot(qorder,yy,'o-',label=label)
ax.set(xlabel='Número de lecturas R / G / B (24 en total)',ylabel='RMSE descriptivo (dos escenas)',title='El presupuesto entre tipos importa más que una corrección geométrica pequeña')
ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(P/'fig_quotas.png',dpi=175);plt.close(fig)
