from pathlib import Path
import json,numpy as np,hashlib,datetime
D=Path(__file__).resolve().parent
rows=[json.loads(s) for s in (D/'ledger.jsonl').read_text().splitlines()]
fix=json.loads((D/'repair_optim.json').read_text())['comparisons']
summary=json.loads((D/'summary.json').read_text())
labels={'pilot_samples':'Precisión de pilotos','role_correlation':'Correlación entre tipos','spectral_shift':'Desplazamiento espectral','spatial_outage':'Fallo regional','role_heterogeneity':'Heterogeneidad de roles','shrinkage':'Regularización'}
intro='''# LARP — BR30, experimento adaptativo de 30 ciclos sobre COSI, MHU y Local SI

**Fecha:** 22/10/2026. **Proyecto:** GalexY3/proyecto-LARP, repositorio privado. **Método:** AB 3.2.1 con O1/O2. **Estado:** EXPLORATORIO_SINTETICO, sin confirmación externa. **Prioridad:** preservar todos los negativos, no promover una novedad no acreditada.

## Alcance exacto
Se ejecutaron **30 decisiones computacionales consecutivas**, cada una con una pregunta concreta, tres geometrías nuevas (seeds deterministas) y un cambio de condición elegido por un scheduler que lee los resultados acumulados. El siguiente evento `branch` y su `reason_from_prior` están registrados con el SHA-256 del runner en `ledger.jsonl`. No se hicieron 30 investigaciones independientes ni se ejecutó el algoritmo original Scale3D: todas las pruebas comparten un mismo generador de campos Fourier 3D periódicos, N=60 nodos con 5 roles de 12 nodos. El esquema hace variar piloto de covarianza, correlación intertipo, desplazamiento espectral, fallos locales, heterogeneidad y contracción isotrópica. El scheduler tiene seis familias de prueba predefinidas y prioriza familias poco exploradas; su orden cambia con la observación anterior, pero su espacio de posibles preguntas estaba limitado desde el inicio. Es **branching adaptativo acotado**, no libertad de investigación ilimitada.

## Diseño y objetivos
Por condición se construye una covarianza PSD de cinco señales sobre 62 modos Fourier 3D positivos. Un piloto de n observaciones por modo estima la covarianza; los modelos adaptados únicamente ven esa estimación, mientras el oráculo tiene acceso artificial a la covarianza verdadera. Todos los algoritmos utilizan las mismas realizaciones de campos y el mismo número de nodos; el presupuesto de optimización, número de operaciones, convergencia y coste de creación **no están completamente equiparados**. Controles: IID, Sobol, proxy de repulsión local, CVT-proxy, MHU espectral-proxy, COSI piloto, COSI shrink, oráculo informacional. **Ninguno** de estos proxies sustituye a Scale3D original ni a Li-Yi Wei (2010). COSI corresponde matemáticamente a una discrepancia de kernels matriciales, por lo que su novedad general está **NO_ACREDITADA**.

Resultado primario: RMSE teórico de integración sobre la distribución sintética generativa (no accuracy de clasificación). Dos variantes adversariales: covarianza desplazada entre bandas/roles y desaparición de sensores en regiones esféricas. Solo se contrastan familias conocidas por el generador. La reutilización de condiciones para decidir el siguiente ciclo descarta inferencia confirmatoria; no se presentan p-valores ni Bayes factors.

## Auditoría numérica y REPAIR
El gradiente analítico pasó tres comparaciones por diferencias finitas. La primera ejecución (`ledger.jsonl`, inmutable) utilizaba descenso con paso constante y reordenamiento local intercalado, lo que **no garantiza descenso del objetivo**. En el C27, con heterogeneidad de roles extrema 1.8, el oráculo con covarianza verdadera rindió peor que MHU, señal de fallo potencial del optimizador o mínimo pobre. El resultado original 29/30 es SOLO una descripción del artefacto original y **NO se usa para afirmar robustez**.

Se ejecutó una auditoría posterior **fuera del cupo de 30**: 90 iteraciones de descenso con backtracking monótono y chequeo de pérdida no creciente, en las mismas 30 condiciones y tres semillas; se conserva como `repair_optim.py` y `repair_optim.json`, sin sobrescribir logs iniciales. Esta reparación cambia tanto el optimizador como el número de pasos, por lo que **no equivale a repetir con un único factor fijo ni es confirmación preregistrada**. Un oráculo no necesariamente gana para cada semilla por no convexidad; las medidas de este ensayo son limitadas.

## Resultados resumidos

| Método / solver post hoc | Fuente RMSE medio | Shift RMSE medio | Outage RMSE medio |
|---|---:|---:|---:|
'''
for arm in ['MHU-monotone','COSI-monotone','COSI-shrink-monotone','Oracle-monotone']:
 values=[np.mean([r['aggregate'][arm][key] for r in fix]) for key in ['source_RMSE','shift_RMSE','outage_RMSE']]
 intro+='| '+arm+' | '+' | '.join(f'{x:.5f}' for x in values)+' |\n'
intro+='''
La reducción media fuente de `COSI-shrink-monotone` respecto a `MHU-monotone` es **~17,7 %** en RMSE (cálculo descriptivo sobre 30 condiciones adaptativamente elegidas). COSI-shrink vence en la comparación pareada de fuente en 30/30 y de covarianza desplazada en 29/30; la igualdad de información y tiempo de preparación con un método clásico de kernel quadrature adaptado NO está acreditada. El oráculo es una referencia informacional inalcanzable para los métodos realistas: no presentarlo como baseline justo. Ni estos 30 ciclos ni la reparación tienen datasets 3D reales, GNN/Transformer entrenadas o un muestreador multiclase Wei verificado.

La observación `COSI > MHU` se explica de forma suficiente, como mínimo, porque COSI utiliza una estimación de la estructura verdadera de la tarea y MHU no. No podemos identificar una aportación geométrica diferencial, pues COSI comparte el objetivo funcional de selección de muestras de cuadratura con kernels. La respuesta a la pregunta de originalidad sigue siendo **NO_ACREDITADO_2/3**, **NO_ACREDITADO_3/3**.

## Historial de los 30 ciclos (tal como se ejecutó el primer solver)

| Ciclo | Familia elegida por estado previo | Ganador original | Δ RMSE compuesto COSI-shrink − MHU | Interpretación / precaución |
|---|---|---|---:|---|
'''
for r in rows:
 tag='**ALERTA**: optimización inestable' if r['cycle']==27 else ('COSI peora' if r['regret']>0 else 'COSI mejor en proxy original')
 intro+=f"| C{r['cycle']:02d} | {labels[r['branch']]} | {r['winner']} | {r['regret']:+.5f} | {tag} |\n"
intro+='''
La secuencia completa, las semillas, parámetros, métricas individuales, selector causal de la rama y la SHA de fuente están en `ledger.jsonl`. Los números de la tabla de 30 ciclos deben leerse **junto con la reparación**, no como resultados definitivos.

## Priors y nuevos falsadores
- **BR30-A01:** el condicionamiento por covarianza puede ser útil para cuadratura sobre señales correlacionadas con distribución estable. Soporte: 30 condiciones sintéticas y solver monótono; contraevidencia: prior art de kernel quadrature, fidelidad a modelo generador, no igualdad total de costes. Estado `SINTETICO_EXPLORATORIO`.
- **BR30-A02:** una contracción isotrópica parcial mejora robustez de covarianza piloto bajo las familias evaluadas. Soporte: comparación COSI-shrink vs COSI; contra: no siempre gana, peso de regularización dependiente de estructura y presupuesto piloto. Estado `CONDICIONAL`.
- **BR30-A03:** descensos con paso fijo y repulsión intercalada pueden dar rankings engañosos en diseño espectral. Soporte: C27 oráculo pierde inicialmente y recupera el mejor error fuente en C27 con optimización monótona. Contra: no demuestra convergencia global del solver de reparación. Estado `REPAIR_DETECTADO`.
- **BR30-A04:** dinámica de selección de próxima pregunta puede registrarse con ledger de decisiones sin pretender 30 estudios independientes. Soporte: 30 filas secuenciales con parent+estado anterior. Contra: familias predefinidas y selección guiada en gran medida por cobertura de ramas. Estado `PROCEDIMENTAL_NO_VALIDADO`.
- **BR30-A05:** una reorganización espacial adaptativa puede originar una nueva arquitectura neuronal superior. Sin entrenamiento, sin Wei, sin acceso a datos reales: `ESPECULATIVO_NO_VALIDADO`.

## Decisión AB-DECIDE
**STOP** a continuar multiplicando condiciones del mismo generador periódico. **PIVOT CONDICIONAL** hacia datasets espaciales 3D observados, un estimador kernel cuadratura competente usando exactamente los mismos pilotos y recursos, Multi-Class Blue Noise original o implementación cualificada claramente rotulada, y experimento neuronal que aísle arquitectura de preprocesado. No reivindicar un descubrimiento original por un término de regularización ya representable en kernel quadrature.

## Fuentes que delimitan originalidad
- Wei, *Multi-Class Blue Noise Sampling* (SIGGRAPH 2010): https://www.liyiwei.org/papers/noise-sig10/
- Huszár y Duvenaud (2012), *Optimally-Weighted Herding is Bayesian Quadrature*: https://proceedings.mlr.press/r10/huszar12a.html
- Archivo LARP AB06: `docs/AB06_REALDATA_20261022/DICTAMEN_AB06.md`.

## Procedencia
`run_ab30.py`: ejecutó 30 filas de `ledger.jsonl`; `repair_optim.py`: repitió 30 como auditoría posterior (no C31–C60); `summary.json`: sumario original; `repair_optim.json`: datos del repair. Ningún archivo de ejecución anterior debe sobrescribirse y ningún nuevo commit debe proclamarse preregistro anterior a la ejecución.
'''
(D/'DICTAMEN.md').write_text(intro,encoding='utf-8')
prior='''# LARP BR30-A — adenda de priors, 22-10-2026

**Tipo:** priors sustantivos LARP. Son cualitativos; no sustituyen el ledger previo BR06/BR08/BR30 ni pasan a los A01–A21 metodológicos. **Origen:** 30 condiciones sintéticas adaptativas, más reparación post hoc.

| ID | Proposición y alcance | Evidencia favorable | Contraevidencia/límite | Falsador | Estado |
|---|---|---|---|---|---|
| BR30-A01 | Covarianza piloto puede mejorar cuadratura de campos 3D correlacionados | COSI-shrink-monotone RMSE .06042 frente MHU .07345 en 30 condiciones | Igualada tarea sintética; misma familia DGP; no se controló coste total ni kernel competente | Una cuadratura por kernels con mismo piloto iguala/supera el efecto | SINTETICO_EXPLORATORIO |
| BR30-A02 | Contracción isotrópica sirve contra especialización piloto | Mejora agregada media frente COSI-monotone (.06042 vs .06104 fuente; .06561 vs .06835 shift) | Selección de parámetros exploratoria; heterogeneidad y shift pueden invertir efectos | Comparador con shrink óptimo y holdout externo | CONDICIONAL |
| BR30-A03 | Rankings con fixed-step pueden invertirse por inestabilidad | C27 oráculo peor antes, mejor en solver monótono (.08820 vs MHU .10695 fuente) | Repair modifica pasos y update; no establece óptimo global | Reproducción con L-BFGS, gradiente y mismas condiciones | REPAIR_DETECTADO |
| BR30-A04 | Ledger parent+resultado permite verificar branching limitado | 30 entradas con reason_from_prior | Scheduler predefine familias y balancea aproximadamente 5 por familia; no 30 proyectos independientes | Testear decisiones de scheduler contrafactuales | METODOLOGICO_OBSERVACIONAL_LOCAL |
| BR30-A05 | COSI representa principio geométrico nuevo de orden neuronal | Ninguna | Kernel discrepancy matricial es antecedente, no se entrenó red | Superar rivales kernel y Wei y red baseline pareados en 3D real | NO_VALIDADO |
'''
(D/'PRIORS_BR30_A.md').write_text(prior,encoding='utf-8')
meta='''# Nota al observatorio AB — AB-M027/AB-M028 (22-10-2026)

**Fuente:** campaña sintética LARP BR30-A, `GalexY3/proyecto-LARP` (rama de investigación), `DICTAMEN.md`, `run_ab30.py`, `ledger.jsonl`, `repair_optim.json`. Estas observaciones **no modifican el núcleo AB 3.2.1 ni O1/O2** ni prueban superioridad metodológica.

### AB-M027 — GATE de comparador informacional y optimizador estable
**Problema confirmado dentro del código experimental:** en C27, el optimizador «oráculo» que conocía la covarianza verdadera obtuvo RMSE fuente peor que MHU por comportamiento de pasos y repulsión intercalada. Una reparación post hoc con descenso monótono recuperó el orden esperado en C27. **Propuesta:** antes de atribuir mejora a geometría, exigir control de descenso, sensibilidad al optimizador y comparador igualmente informado si el modelo candidato usa pilotos auxiliares. Preservar el resultado inicial y el repair sin renumerar sus ciclos. Falsador: problemas genuinamente no convexos donde oráculo local no domina sin multi-start; no exigir garantía universal de óptimo global. **Estado:** PROPUESTA — eficacia AB no validada.

### AB-M028 — BRANCHING adaptativo acotado, no exploración irrestricta
**Observación:** el scheduler eligió familias según regret y cobertura de seis alternativas predefinidas; 30 filas con parent, freeze hash y estado previo sí existen, pero las 30 pruebas reutilizan el mismo DGP sintético. **Propuesta:** además de contar ciclos, registrar espacio de decisiones disponible, contrafactuales no seleccionados, eventos de REPAIR fuera del cupo, y criterio explícito de detener la familia cuando falte evidencia nueva. Un scheduler adaptativo no crea nuevas fuentes empíricas por el mero orden secuencial. **Estado:** PROPUESTA — no implica AB 3.3 ni actualiza A01–A21.
'''
(D/'NOTA_AB_M027_M028.md').write_text(meta,encoding='utf-8')
files=['run_ab30.py','ledger.jsonl','summary.json','repair_optim.py','repair_optim.json','runner.log','repair.log','DICTAMEN.md','PRIORS_BR30_A.md','NOTA_AB_M027_M028.md','build_dossier.py']
manifest={f:hashlib.sha256((D/f).read_bytes()).hexdigest() for f in files}
(D/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('generated report',len(intro),'files',len(manifest))
