"""Post-outcome report formatter. All claims bounded to prereg synthetic L01-L20."""
import json,hashlib
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
D=Path(__file__).parent
x=json.loads((D/'audit.json').read_text())
mean=pd.DataFrame(x['method_means']);geom=pd.DataFrame(x['geometry_means'])
labels={'cvt_type':'CVT | tipos','cvt_knn':'CVT | vecinos','mhu_type':'MHU proxy | tipos','grid_type':'Retícula | tipos','mhu_knn':'MHU proxy | vecinos','grid_knn':'Retícula | vecinos','cvt_learned':'CVT | ruta entrenada','mhu_learned':'MHU proxy | ruta entrenada','grid_learned':'Retícula | ruta entrenada'}
fig,ax=plt.subplots(figsize=(12,5));ax.bar(range(len(mean)),mean['mean']);ax.set_xticks(range(len(mean)));ax.set_xticklabels([labels[v] for v in mean.method],rotation=35,ha='right');ax.set_ylabel('NMSE medio (menor = mejor)');ax.set_title('LARP L01–L20: cinco modalidades sintéticas y decodificador neuronal común');fig.tight_layout();fig.savefig(D/'NMSE_METHODS_TRAINED.png',dpi=155);plt.close(fig)
for typ in ('full','zoom'):
 fig,ax=plt.subplots(figsize=(7,3));ax.plot(['Matemática condicional anterior','Tras L01–L20'],[24,18],marker='o');ax.set_ylim((0,100) if typ=='full' else (14,28));ax.set_ylabel('CT2 ordinal, no probabilidad');ax.set_title('LARP: valoración provisional por línea / evidencia');fig.tight_layout();fig.savefig(D/f'CT2_{typ}.png',dpi=130);plt.close(fig)

raw=pd.read_csv(D/'all_predictions.csv');wide=pd.read_csv(D/'paired_conditions.csv');cond=wide[['cycle','context','shift','cvt_type','cvt_knn','mhu_type','mhu_knn','cvt_learned','mhu_learned']]
table='\n'.join('| '+ ' | '.join([str(r.cycle),str(r.context),str(r['shift'])]+[f'{r[v]:.3f}' for v in ['cvt_type','mhu_type','cvt_learned','mhu_learned']])+' |' for _,r in cond.iterrows())
means='\n'.join('| '+labels[r['method']]+' | '+f"{r['mean']:.4f}"+' | '+f"{r['median']:.4f}"+' |' for r in x['method_means'])
comp='\n'.join('| '+r['preference']+' | '+f"{r['mean_delta']:+.4f}"+' | '+f"[{r['ci95_descriptive'][0]:+.4f}, {r['ci95_descriptive'][1]:+.4f}]"+' | '+str(r['favorable_conditions'])+'/20 |' for r in x['paired_contrasts'])
text=f'''# Dictamen LARP L01–L20 — Redes entrenadas y enrutamiento espacial

**30 de octubre de 2026 · AB3.2.1 O1–O7 · BRANCHING/PIVOT 20 ciclos autorizado.**

## Resumen ejecutivo

Se ejecutaron **20 condiciones funcionales preregistradas**, producto de 5 familias de señales espaciales × 4 perturbaciones, con **90 decodificadores neuronales entrenados**, 9 métodos de conexiones, 2 geometrías, 24 semillas de campos de entrenamiento, 6 de validación, 16 de evaluación. Total: **5.760 registros** (16 campos × 2 geometrías × 9 métodos × 20 condiciones). Todas las unidades inferenciales pertenecen a **un solo generador sintético**: no son 5.760 escenas reales ni 20 replicaciones independientes.

**Resultado adverso:** CVT por tipos promedio **0,2211 NMSE**, frente a MHU finita proxy por tipos **0,2873**. La diferencia MHU−CVT **+0,0662** favorece CVT en los **20/20 contrastes**. Con un enrutador supervisado entrenado con objetivos de TRAIN, CVT obtiene 0,5316 frente a MHU 0,5493; este enrutamiento aprendido concreto suele ser peor que enrutamiento por tipos o kNN competente. La política aprendida usa enlaces aproximadamente 3× más largos y puede perder continuidad local; no se ha demostrado que la longitud cause por sí sola el efecto.

**GRAN LIMITACIÓN:** Los seis NPZ N400 aviares originales **NO se descargaron**, aunque fueron localizados en GitHub y leídos sus certificados JSON. GitHub connector rechaza binarios NPZ y la red del contenedor no resuelve GitHub. Se evalúan exclusivamente geometrías proxy creadas por [1mab30_functional.py[0m; no identificar estos resultados con retina aviar original ni con original LOCAL. Tampoco hay MoE de atención plenamente entrenado, Wei 2010 ejecutado ni dataset visual real. Un positivo no habría validado originalidad 2/3.

## A–J: diseño y freeze–run

A: contrato de verdad = reconstrucción de señal combinada de 5 modalidades por nodo bajo presupuesto de 400 lecturas escalares, seis enlaces dirigidos y comparadores equiparados en salidas y MLP. B: H1 modelo learned routing y/o geometría MHU aporta mejora diferencial; H0 competidores kNN/type CVT/grid no inferiores. C: 20 clases de estimandos contextual/perturbación, no 20 muestras externas. D: código congelado **antes** de resultados: SHA256 `320bab4445e5e381b9378b681940ada89fe6df74086c4c0f9a1b8e51b2d7b031`, commit GitHub `daee73553a74e0155962a186bb372cddc7e1289f`; prerregistro `PREREG_L01_L20.md`, commit `0ce03f7dd55dd37f33fa952e27ba44a344e38ab0`. E: 90 entrenamientos neuronales (mismos 1009 parámetros, 12 épocas, validación independiente de test); 5760 observaciones. F: auditoría de validez, autocrítica adversarial y ausencia de permisos/datos originales. G: las **10/10 celdas** se reprodujeron byte a byte **descontando exclusivamente `elapsed_sec`**; no hay réplica externa ni clon limpio. H: priors perjudiciales para MHU transmitidos sin borrado. I: nivel 0/3 para novedad causal o matemática; **N1 nuevos = N2 = N3 = 0**. J: STOP_LOCAL sobre generador ya usado y ruta supervisada ingenua; PIVOT condicionado a NPZ nativos y un learned attention/rewiring fuerte, y datos multicanal nuevos.

**Errata:** la primera ejecución continua terminó prematuramente por un límite de tiempo, no produjo JSON final ni se contó; el wrapper por celdas fue congelado ANTES del primer outcome completo en commit `30fbed674a641281577d9cfc0239966d1b84fb6f` y documentado en `ERRATA_RESOURCE_CAP.md` antes de la ejecución final. No se alteraron métodos ni seeds.

## Resultados globales

| Modelo | NMSE medio ↓ | Mediana ↓ |
|---|---:|---:|
{means}

**Diferencias pareadas** (intervalos bootstrap **descriptivos**, remuestreando solo los 16 IDs de campos sintéticos; geometrías tratadas como sensibilidad fija, sin inferencia poblacional externa ni ajuste de multiplicidad):

| Comparación (primer método − segundo) | Media | IC95 descriptivo | Condiciones favorables al primero |
|---|---:|---:|---:|
{comp}

**Los mejores por celda:** CVT por tipos 10/20, CVT kNN 5/20, CVT trained routing 3/20, MHU proxy kNN 2/20. La ventaja funcional es de CVT en los escenarios de reconstrucción estudiados, no de los bajos valores de energía Fourier por sí solos. En señales correlacionadas, algunos métodos aprendidos sí son competitivos; no justificar reclasificación positiva general.

## Resultados por condición

| Ciclo | Campo | Perturbación | CVT tipo | MHU tipo | CVT aprendida | MHU aprendida |
|---|---|---|---:|---:|---:|---:|
{table}

## Diagnóstico de mecanismos

| Método | Longitud media arista | Cobertura media de modalidades (incluido nodo propio) |
|---|---:|---:|
'''
for _,r in geom.sort_values('method').iterrows():text+=f"| {r['method']} | {r['mean_edge_length']:.3f} | {r['mean_type_coverage']:.3f} |\n"
text+='''
La geometría CVT kNN obtiene cobertura de tipos ~0,909 con aristas cortas (~0,054), mientras que MHU proxy kNN ~0,752. Los métodos tipo forzado alcanzan 1,00 por construcción, pero la conexión aprendida utiliza información de TRAIN y aun así prefiere enlaces mucho más largos (~0,18). El enrutamiento aprendido no es un rival de *graph attention* moderno; sobreajuste y desajuste espacial son hipótesis explicativas, NO mecanismos causalmente identificados.

## Datos, validez y reproducibilidad

Los datos TRAIN/VAL/TEST utilizan semillas disjuntas, pero todos son del **mismo proceso sintético**. Comparaciones entre geometrías reutilizan semillas generadoras y el target se normaliza sobre los 400 nodos de cada geometría, por lo que no constituye la misma realización exacta sobre observaciones idénticas. Los supervisores entrenan **solo clean** y todos enfrentan las cuatro perturbaciones en TEST. El router aprendido accede a **targets TRAIN** además del diseño fijo y requiere cómputo adicional de selección de aristas: paridad de parámetros y número de edges no implica paridad de coste integral. No se comparó la implementación original Wei2010, ni un expansor espectral certificado, ni atención aprendida end-to-end.

La segunda corrida de las mismas 10 celdas confirma determinismo local. **CLEAN_CLONE_NOT_VERIFIED; EXTERNAL_REPLICATION_NOT_DONE; NATIVE_400_BENCHMARK_BLOCKED.** El ZIP contiene JSON sin modificar, código, certificados Git previos, informes y auditorías. Todo cambio de historial queda por commits inmutables.

## Evidencia pública y límites de originalidad

Wei, 2010, *Multi-Class Blue Noise Sampling*: https://www.liyiwei.org/papers/noise-sig10/ (modelo multiclase publicado). Attali et al., 2026, *Graph Rewiring in GNNs to Mitigate Over-Squashing and Over-Smoothing*, IJCAI-26: https://doi.org/10.24963/ijcai.2026/861 (antecedentes para métodos de enrutamiento/rewiring). Micheli & Tortorella, 2025, *An empirical evaluation of rewiring approaches in graph neural networks*, https://doi.org/10.1016/j.patrec.2025.05.021 (evidencia general de que rewiring no siempre mejora bajo condiciones equiparadas). Son antecedentes, NO resultados de ejecución de esos rivales en esta campaña.

## Gobernanza y decisión final

**20/20 condiciones AB-R de esta autorización ejecutadas y auditadas**, pero no 20 experimentos independientes ni hallazgos originales; 1 proceso inicial incompleto archivado. CT2 línea matemática previa 24/100; línea actual *functional trained proxy* 18/100 valoración ordinal interna, no probabilidad, por adversario CVT, rutas supervisadas débiles y ausencia de nativos. R5 STOP_LOCAL; no consumir más semillas de mismo generador. Mantener `main` sin modificar; la rama contiene informe/ledger/prereg/scripts y resultados. No solicitar autorización intermedia. Próxima necesidad: bytes NPZ de nativos y prueba con CAVE / datos multiespectrales con licencia, learned dynamic attention + CVT + Wei bajo coste igualado.
'''
text=text.replace('\x1b[1m','`').replace('\x1b[0m','`')
(D/'DICTAMEN_L01_L20.md').write_text(text)
(D/'PRIORS_DELTA.md').write_text('''# Priors de LARP entrenado L01–L20 — 2026-10-30\n\n- P-TR01 [observación computacional condicionada]: CVT por tipos 0,2211 NMSE frente a MHU proxy tipos 0,2873. Las 20 condiciones comparten generador; no trasladar al aviar original. Actualización: prior contra superioridad general de MHU se refuerza.\n- P-TR02 [observación computacional condicionada]: rutas aprendidas por correlación de TRAIN tienen mayor longitud (~0,18) y peor media de NMSE que tipo o kNN en campos low/high/localized. Hipótesis explicativa de sobreajuste **NO demostrada causalmente**. Nueva prueba: router entrenado end-to-end con penalización por longitud e información, rival attention strong.\n- P-TR03 [estructura]: CVT kNN obtiene cobertura media de 0,909 frente a MHU proxy kNN 0,752; distancias similares. Posible mediador, requiere ablación que iguale cobertura/longitud sin cambiar geometría.\n- P-TR04 [bloqueo]: archivos nativos NPZ aviares de N400 disponibles en GitHub bajo ramas originales, pero conector no descarga binarios. No atribuir resultados proxy a ellos.\n- P-TR05 [evidencia de integración]: 90 modelos MLP de 1009 parámetros, train/val/test por semillas disjuntas, 10 celdas repetidas localmente 100% coincidentes. Dado que datos son sintéticos, no confirma mejora real.\n- N1 únicos nuevos: 0. N2=N3=0. CT2 rama matemática 24/100 histórico; rama trained proxy 18/100 (nuevo juicio ordinal, no probabilidad). R5 STOP_LOCAL.\n''')
(D/'CURRENT.md').write_text('''# CURRENT · LARP trained routing L01–L20 · 2026-10-30\n\nGrant: 20 AB-R flexible cycles; L01–L20 executed (20 factorial condition analyses, NOT 20 independent datasets), 0 scientific new N1/N2/N3, 1 earlier incomplete run documented. Model: 400 nodes, six directed edges, nine geometry/router combinations, 90 trained MLPs (1009 params), 5760 heldout NMSE rows. Ten cells rerun and records exact except elapsed_sec. All output synthetic finite proxies, **NOT native LARP N400**.\n\nPreregs and code frozen in GitHub before full outcomes: `PREREG_L01_L20.md` 0ce03f7d, `learned_followup.py` daee7355, repair `ERRATA_RESOURCE_CAP.md` 1c1b0d5 and `run_one_cell.py` 30fbed6. Parent latest branch `research/ab-r-functional-routing-20261030` commit 0138a307.\n\nAdverse results: CVT type NMSE .2211, MHU proxy type .2873, CVT learned .5316, MHU learned .5493. CVT type beats MHU type in 20/20 conditional scenarios. Learned routing selector itself performed poorly but not a modern trained attention baseline. Native assets inaccessible via GitHub connector (UTF-8 restriction), NATIVE_400_BENCHMARK_BLOCKED.\n\nCT2 provisional trained functional branch 18/100 ordinal, prior math 24/100 preserved. R5 STOP_LOCAL for same synthetic generator, future requires actual NPZ and independent multichannel data + stronger routing; no main merge, no costly CI. CLEAN_CLONE_NOT_VERIFIED; EXTERNAL_REPLICATION_NOT_DONE. No grant remaining; any new block requires explicit authorization.\n''')
(D/'README.md').write_text('''# LARP trained routing L01–L20: reproduction and provenance\n\nOriginal frozen research files in branch: `research/AB_ROUTING_20261030/learned_followup.py`, `research/AB_ROUTING_20261030/run_one_cell.py` and upstream `ab30_functional.py`; protocol in `research/AB_TRAINED_20261030/PREREG_L01_L20.md`. Resource-cap errata `ERRATA_RESOURCE_CAP.md` precedes full execution.\n\nTo replay on a machine with Python3.11+, NumPy, SciPy, PyTorch CPU, in a checked out copy of this branch, modify only output path; do not alter frozen source. `run_one_cell.py` currently infers the training source from local working-directory structure for the original execution; for a clean clone use the fully frozen `learned_followup.py` directly with a sufficiently long runtime, or place wrappers in compatible sibling directories. **Not verified on clean clone; wrapper has a known nonportable local path dependency.**\n\nResults archive contains 10 original per-cell JSON, 10 exact replays with only `elapsed_sec` varying, predeclared protocol, audit, CSV summary, 20 A–J ledgers, reports, plots. All synthetic and no original NPZ native geometries. Source model parent `ab30_functional.py` is part of repo. Field seeds are divided into disjoint train/validation/test sets. 400 nodes x 6 edges all methods.\n''')
print('REPORT',len(text),'chars', 'files',len(list(D.glob('*.png'))))
