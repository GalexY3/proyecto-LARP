"""Post-outcome report generator. Not pre-outcome code; retains original bytes."""
from pathlib import Path
import pandas as pd, json, hashlib, numpy as np, matplotlib.pyplot as plt, zipfile, platform
ROOT=Path(__file__).resolve().parent
cases=pd.read_csv(ROOT/'all30.csv');audit=json.loads((ROOT/'audit.json').read_text());raw=json.loads((ROOT/'run1/results.json').read_text());
ledger=[]
for _,r in cases.iterrows():
    claim=(f"At {r['context']} field mechanism under {r['shift']} intervention, a six-edge type-aware routing policy improves a "+
           "finite spectral MHU proxy's local kNN access to distinct sensor modalities")
    x={
       'id':r.cycle_id,'parent':'AB_ROUTING_20261030','mode':'AB-R','status':'RUN_VALID_SYNTHETIC',
       'A':{'question':claim,'unit':'one synthetic field realization and one geometry seed (paired)','population':'scripted five-modal torus fields; no physical/human data','truth':'five latent fields over all nodes; observable only to simulation for loss calculation','primary':'normalized MSE at one hop','secondary':'two-hop normalized MSE and geometric coverage'},
       'B':{'preferred':'mhu_type < mhu_knn','null':'mhu_type >= mhu_knn','rivals':['cvt_type','grid_type','cvt_knn','grid_knn','expander_deg6','random_deg6','mhu_hybrid (DUPLICATE GRAPH)'],'hypothesis_status':'operational, not presumed causal'},
       'C':{'design':'fixed 3 geometries ×8 field realizations ×9 method labels ×2 hops; exact outdegree 6','scenario':r.context,'intervention':r['shift'],'falsifier':'type routing worse than purely geometric MHU or matched CVT/grid stronger'},
       'D':{'prereg_commit':'4bb177d378eb12fe3f376c58a574cd0d75939f34','full_code_commit':'a620c5c912cf1c34e7f898287451439c28908157','full_code_git_blob':'bad703f26481a4a9b0b935f5602cf2cb6321b07d','full_code_sha256':audit['source_code_sha256'],'data_origin':'synthetic parameters precommitted; finite geometry MHU proxy'},
       'E':{'executed':True,'paired_blocks':24,'hop1_nmse':{'mhu_type':float(r.mhu),'mhu_knn':float(r.mhu_local),'cvt_type':float(r.cvt),'cvt_knn':float(r.cvtlocal),'grid_type':float(r.grid),'pseudo_expander':float(r.expander)},'mhu_type_minus_cvt_type':float(r.difference_mhu_cvt),'mhu_knn_minus_mhu_type':float(r.gain_routing_mhu),'winner':r.winner,'negative_outcome_logged':True},
       'F':{'audit':'same 6 directed out edges and estimator, but CVT has different geometry/coverage; MHU only finite spectral surrogate; duplicate mhu_hybrid must be removed as independent comparison','adversarial_result':'cvt_type superior to mhu_type in this cell' if r.difference_mhu_cvt>0 else 'MHU type competitive with CVT type'},
       'G':{'exact_same_environment_replay':audit['exact_replay_match'],'independent_dataset':False,'independent_scientific_replication':False,'holdout':'No external holdout; 8 fixed seeds reused across cells'},
       'H':{'prior':'low-frequency spectral suppression alone is insufficient to guarantee cross-modal delivery','update':'supports class routing vs MHU kNN for this generator' if r.gain_routing_mhu>0 else 'opposes class routing vs MHU kNN in this generator; high-frequency or severe dropout can reverse gains','CVT_vs_MHU':'negative for finite MHU proxy; no inference to native certified avian MHU'},
       'I':{'internal_validity':'conditional on exact synthetic generator and nearest class decoder','transportability':'NOT_ESTABLISHED','scientific_novelty':'UNVERIFIED, likely known geometric design tradeoffs','grade_0_3':0,'N1_new':0,'N2_new':0,'N3_new':0,'CT2_before':24,'CT2_after':24,'external_replication':False},
       'J':{'decision':'STOP_LOCAL after complete factorial audit; pivot to native multi-type geometry/learned router and independent modalities','next_evidence':'native 400-point original MHU data (NPZ unavailable through connector), then trained task-aware router and independent labels','no_new_cycle_from_seed_replay':True}
    }
    ledger.append(x)
assert len(ledger)==30 and len(set(x['id'] for x in ledger))==30
(ROOT/'LEDGER_F01_F30.json').write_text(json.dumps({'schema':'AB3.2.1_O1_O7_ROUTING','grant':30,'completed_contrasts':30,'invalid':0,'planning':0,'new_n1':0,'new_n2':0,'new_n3':0,'warnings':['Thirty pre-registered task×failure contrasts all rely on the same simulator: not thirty independent source samples or novel mechanisms','Do not claim native Scale3D MHU, authentic CVT LOCAL or trained MoE','mhu_type and mhu_hybrid are the same underlying neighbor sets'],'cycles':ledger},indent=2,ensure_ascii=False)+'\n')
geom=pd.DataFrame(audit['geometry_audit']);mat=pd.DataFrame(audit['structural']);m=mat.query('hop==1').set_index('method')
meanm=audit['nmse_means_hop1'];
report=f'''# LARP / AB 3.2.1 — F01–F30 · Dictamen de transporte multiespecialista

Fecha: 2026-10-30. Rama `research/ab-r-functional-routing-20261030`. **30 contrastes A–J ejecutados dentro de un diseño factorial, no 30 estudios independientes**. Diseño y código congelados en GitHub *antes* de outcomes: protocolo `4bb177d378eb12fe3f376c58a574cd0d75939f34`, fuente completa `a620c5c912cf1c34e7f898287451439c28908157`, SHA256 fuente `{audit['source_code_sha256']}`. Conservar `main`. Sin CI costosa.

## Problema y origen de datos
N=400 nodos con conteos de tipos originales (163,85,68,50,34), una observación escalar por nodo, seis conexiones **dirigidas** salientes. Se reconstruye una media ponderada de cinco campos no observados directamente en cada nodo, buscando la lectura del mismo tipo más próxima dentro de 1 o 2 saltos, imputando 0 si falta. No hay entrenamiento de parámetros: es una evaluación de *adquisición de información funcional*, no de aprendizaje neuronal. Tres semillas geométricas y ocho realizaciones de campos para 6 contextos ×5 perturbaciones. **12.960 registros** que usan de forma correlacionada las mismas fuentes sintéticas; n efectivo NO 12.960 mundos independientes. Condiciones: limpio, drop aleatorio 15/40%, pérdida 40% del tipo raro, ruido σ=.25. Contextos: baja frecuencia, alta frecuencia, fuerte correlación, anticorrelación, señal rara dominante, manchas locales.

## Comparadores
Misma salida de grado seis: grafos espacialmente próximos sobre retícula, CVT condicionada por clase, MHU espectral aproximada; grafos de selección de tipos sobre cada geometría, aleatorio 6-grado y circulante aleatorio 6-grado. El último **no es un expansor certificado**. El optimizador MHU de estos ensayos es un **proxy finito**, no las geometrías nativas Scale3D del repositorio, cuya NPZ original no se descargó desde el conector. CVT tampoco es el algoritmo original LOCAL. No se ha entrenado MoE ni un router aprendido; tiempo, construcción y longitud de aristas no están equiparados.

## Resultados completos por familia (NMSE: menor es mejor)

| Método | NMSE un salto | NMSE dos saltos | Disponibilidad tipos un salto | Distancia arista media |
|---|---:|---:|---:|---:|
'''
for method in ['cvt_type','cvt_knn','mhu_type','mhu_knn','grid_type','grid_knn','expander_deg6','random_deg6']:
    report+=f"| {method} | {meanm[method]:.4f} | {audit['nmse_means_hop2'][method]:.4f} | {float(m.loc[method,'availability']):.3f} | {float(m.loc[method,'edge_dist']):.4f} |\n"
report+=f'''
- **CVT con selección por tipo domina MHU con selección por tipo en 30/30 condiciones**, diferencia media NMSE (MHU−CVT): {cases.difference_mhu_cvt.mean():.4f}. Los resultados son relativos a estos dos **proxies** sobre datos simulados, no a las geometrías aviares originales.
- Seleccionar vecinos por tipo sobre la misma MHU aproximada mejora MHU kNN en **{audit['mhu_routing_better_than_knn_cells']}/30** condiciones y la empeora en {audit['mhu_routing_worse_than_knn_cells']}/30. La media de ganancia NMSE kNN−tipo: {cases.gain_routing_mhu.mean():.4f}.
- En 24/30 condiciones el ganador de las políticas principales es CVT + selección por tipo, en 5/30 CVT kNN y en 1/30 MHU kNN. Ninguno de los 30 produce una victoria general de la MHU aproximada frente a CVT.
- Disponibilidad de los cinco tipos por nodo con selección explícita alcanza 100% **antes del dropout** con seis aristas + señal propia; con vecinos MHU locales es {float(m.loc['mhu_knn','availability']):.1%}. Esto identifica una ventaja del enrutamiento, pero no demuestra mejora de aprendizaje neuronal ni de coste físico.

## Diagnóstico geométrico adversarial

| Geometría | Media espectral de unión S sobre 8 modos | Media espectral por tipos S | Cuantización media Q por tipos | Radio percentil95 |
|---|---:|---:|---:|---:|
'''
for name,rows in geom.groupby('geometry'):
    vals=rows[['S_union','S_type_mean','CVT_class_Q','class_r95']].mean()
    report+=f"| {name} | {vals.S_union:.6f} | {vals.S_type_mean:.6f} | {vals.CVT_class_Q:.6f} | {vals.class_r95:.6f} |\n"
report+='''
El proxy MHU sí reduce drásticamente su energía espectral objetivo: su pérdida contra CVT no procede de que se haya olvidado ejecutar el término de Fourier. Sin embargo, CVT consigue distancias de cuantización por clase considerablemente menores, que son directamente útiles para recuperar campos espaciales con vecinos próximos. Las métricas geométricas de este cuadro son un análisis descriptivo **posterior a outcomes** y no forman una nueva confirmación preregistrada.

## Incidencia de instrumentación / falso rival
Las políticas llamadas `mhu_type` y `mhu_hybrid` producen **exactamente los mismos conjuntos de vecinos** para todos los 400 nodos y las 3 geometrías (1.200/1.200), aunque difiere el orden. En consecuencia todas las 1.440 predicciones emparejadas por modalidad y perturbación son exactamente iguales: el híbrido no constituye un comparador independiente. **Eliminar cualquier interpretación de comparación MHU_TYPE vs MHU_HYBRID.** Conservar ambos outputs en el raw por auditoría, no reescribirlos.

## A–J, validación y límites
Todos los 30 contratos individuales F01–F30 constan en `LEDGER_F01_F30.json` (escenario, rival, estimando, ejecución, resultados por condición, auditoría, priors, dictamen y decisión). Fuente de outcomes raw: `results.json` del ZIP archivado con hash SHA256 `'''+audit['raw_results_sha256']+'''`. Reejecución con el mismo código/datos/entorno produce **coincidencia de bytes exacta**; esto es reproducibilidad técnica, no réplica externa.

**Una limitación científica sustantiva:** el estimador escoge el vecino observable más cercano ANTES del fallo. No sustituye sensores caídos por otros candidatos; esto puede sesgar a la baja condiciones con abandono. Los pesos entre modalidades son conocidos y no se aprenden. El benchmark es un único generador sintético con seis tareas parametrizadas; no hay variedad independiente de datasets ni holdout real.

**R5:** STOP_LOCAL en este generador, puesto que seguir añadiendo semillas o perturbaciones no resolvería el bloqueo causal. PIVOT a descifrar las geometrías nativas NPZ, entrenar un enrutador fuerte (tipo MoE/GraphGPS/expansor real), igualar coste de construcción y distancia/comunicación y obtener fuentes multicanal independientes. No conceder N1 nuevos por información repetida/puesta por diseño; N2=N3=0. CT2 línea matemática condicionada 24/100 sin incremento (ordinal, no probabilidad). Ninguna conclusión sobre supremacía general MHU.

Fuentes de contexto: Jiao et al. PRE 2014 DOI 10.1103/PhysRevE.89.022721; Wei SIGGRAPH 2010 https://www.liyiwei.org/papers/noise-sig10/; Black et al. ICML2023 https://proceedings.mlr.press/v202/black23a.html; las fuentes no validan este experimento automáticamente.
'''
(ROOT/'DICTAMEN_F01_F30.md').write_text(report)
prior='''# PRIORS DELTA — LARP Routing AB30
Fecha 2026-10-30. No sustituir priors históricos.
- P-ROUTE-01 [local synthetic]: seleccionar rutas por tipo mejora el MHU espectral finito frente al vecindario puramente local en 24/30 condiciones; alta frecuencia contradice la generalización. Esta ganancia es parcialmente tautológica bajo una tarea que exige recuperar modalidades ausentes.
- P-ROUTE-02 [adverse]: el rival CVT tipo-condicionado supera a MHU tipo-condicionado en 30/30 condiciones de este generador, con Q de cuantización menor. No refuta geometría aviar original (no ejecutada).
- P-ROUTE-03 [invalid comparator]: mhu_type y mhu_hybrid forman exactamente el mismo grafo, por lo que no son rivales independientes; no repetir ni puntuar el híbrido.
- P-ROUTE-04 [method limitation]: una red regular aleatorizada de 6 circulantes no constituye automáticamente un expansor; no confundir pobre rendimiento local con derrota de un rival expander real.
- P-ROUTE-05 [need real evidence]: código ejecutado y exactamente reproducible; 30 condiciones relacionadas del mismo generador sintético, sin entrenamiento, fuentes externas, paridad de distancias o réplica independiente. Fuente nativa original MHU ausente.
- H-conditional: como el error se rige por cuántas modalidades llegan y a qué distancia espacial, hay un compromiso coverage×proximity; no existe ventaja automática de energía Fourier si la tarea penaliza distancia a la observación.
- N1_unique_new=0; N2=0; N3=0. CT2 condicionado previo 24/100 sin subida; escala ordinal sin validación.
- R5 STOP_LOCAL, sólo PIVOT a fuentes externas y grafos aprendidos con rivales reales.
'''
(ROOT/'PRIORS_DELTA.md').write_text(prior)
# chart: use default matplotlib styles/colors
ax=None
fig,ax=plt.subplots(figsize=(10,5))
methods=['cvt_type','cvt_knn','mhu_type','mhu_knn','grid_type','grid_knn','random_deg6','expander_deg6']
ax.bar(methods,[meanm[k] for k in methods]);ax.set_ylabel('NMSE (lower is better)');ax.set_title('LARP AB30: 30 synthetic task×failure contexts, hop 1');ax.tick_params(axis='x',rotation=35);fig.tight_layout();fig.savefig(ROOT/'NMSE_METHODS.png',dpi=160);plt.close(fig)
# O7 typed branching graph
nodes=[{'id':'ROUTING_AB30','type':'research_line','status':'STOP_LOCAL'},{'id':'PARENT_H30','type':'prior_work','status':'CLOSED'}];edges=[{'from':'PARENT_H30','to':'ROUTING_AB30','relation':'pivots_to'}]
for x in ledger:
    nodes.append({'id':x['id'],'type':'AB-R_synthetic_contrast','status':'RUN_VALID_SYNTHETIC','grade':'0/3','context':x['C']['scenario'],'shift':x['C']['intervention']})
    edges.append({'from':'ROUTING_AB30','to':x['id'],'relation':'tests'})
(ROOT/'GRAFO_O7.json').write_text(json.dumps({'schema':'AB3.2.1-O7','nodes':nodes,'edges':edges,'warning':'Not 30 independent scientific replications or novel discoveries'},indent=2))
(ROOT/'CURRENT.md').write_text('''# CURRENT LARP ROUTING AB30 — 2026-10-30
Authorized 30. Executed 30 related preregistered task×failure contrasts (6 contexts ×5 interventions) under one synthetic functional design; audit PASS, exact repeat byte-identical. No extra unconsumed cycles. **No native LARP MHU / no real learned MoE / no external replication.**
Baseline HEAD research/ab-r-mhu-hybrids-20261030 = 282756c310bbe00afbb4a3c85e29d92bda21d19a. Source freeze a620c5c912cf1c34e7f898287451439c28908157; prereg 4bb177d378eb12fe3f376c58a574cd0d75939f34. SHA256 input code cf187e6a367239dd46e2e25351158f5c1d8020423750987c4b8dc3fdcd9118d2; raw outputs c968c85880b16e1cf8caf5ca41104c49683ff601a54be8b3e5be1d51790c057a.
Key audit: MHU proxy spectral near zero but CVT type has lower spatial quantization and lower NMSE across all 30 cells. mhu_type & mhu_hybrid same sets of 6 neighbors 1,200/1,200 nodes; duplicate rival invalidated. 30 contexts share seeds so not 30 independent experiments. N1 0, N2 0, N3 0, CT2 24 unchanged. R5 STOP_LOCAL, pivot to actual native 400 NPZ, learned router and matched costs. main unchanged, no CI.
''')
# ZIP with all inspectable original and derived artifacts; avoid enormous uncompressed raw file in Git directly
files=['ab30_functional.py','run1/results.json','run1/summary.json','run1.log','run2.log','audit.json','audit_and_report.py','audit.log','all30.csv','geometry_diagnostics.csv','LEDGER_F01_F30.json','DICTAMEN_F01_F30.md','PRIORS_DELTA.md','CURRENT.md','GRAFO_O7.json','NMSE_METHODS.png']
with zipfile.ZipFile(ROOT/'LARP_AB_ROUTING_F01_F30_20261030.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for f in files:z.write(ROOT/f,arcname=f)
print('WROTE',len(ledger),'cycles','zip bytes',(ROOT/'LARP_AB_ROUTING_F01_F30_20261030.zip').stat().st_size)
