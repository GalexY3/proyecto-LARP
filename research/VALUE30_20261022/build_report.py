from pathlib import Path
import json,hashlib,zipfile,numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).parent
z=json.loads((P/'summary.json').read_text());L=[json.loads(x) for x in (P/'ledger.jsonl').read_text().splitlines()]
A=json.loads((P/'audit.json').read_text());T=json.loads((P/'temporal_pivot.json').read_text());S=json.loads((P/'stress_audit.json').read_text())
methods=[x['method'] for x in z['holdout_retina']]; vals=[x['retina_fixed_RMSE'] for x in z['holdout_retina']]
fig,ax=plt.subplots(figsize=(8.8,4.8));ax.barh(methods,vals);ax.set_xlabel('RMSE (menor es mejor)');ax.set_title('C30: retina (única nueva escena reservada)');ax.invert_yaxis();fig.tight_layout();fig.savefig(P/'fig_holdout_retina.png',dpi=150);plt.close(fig)
counts=z['c1_to_c29_dev_win_counts'];fig,ax=plt.subplots(figsize=(8.8,4.8));ax.bar(list(counts),list(counts.values()));ax.set_ylabel('Condiciones con mejor RMSE');ax.set_title('C01–C29: victorias de desarrollo; no independientes');ax.tick_params(axis='x',rotation=18);fig.tight_layout();fig.savefig(P/'fig_dev_wins.png',dpi=150);plt.close(fig)
sub=[x for x in L[:29] if x['params']['branch'].startswith('LOW_PILOT')]
# branch name is under entry decision_event, not params; corrected below
sub=[x for x in L[:29] if x['decision_event'].startswith('LOW_PILOT')]
fig,ax=plt.subplots(figsize=(8.8,4.8))
for m in ['COSI_SHRINK','DIRECT','POWER_DIAG','GP','SOBOL']:
 ax.plot([x['params']['pilot'] for x in sub],[x['comparison']['rmses'][m] for x in sub],marker='o',label=m)
ax.set_xscale('log');ax.set_xlabel('Regiones piloto');ax.set_ylabel('RMSE desarrollo');ax.set_title('Sensibilidad al número de datos piloto (una semilla/condición)');ax.legend(ncol=2,fontsize=8);fig.tight_layout();fig.savefig(P/'fig_pilot.png',dpi=150);plt.close(fig)

c30={r['method']:r['retina_fixed_RMSE'] for r in z['holdout_retina']}
ratio=lambda x,y:100*(1-x/y)
pct_power=ratio(c30['COSI_SHRINK'],c30['POWER_DIAG'])
pct_sobol=ratio(c30['COSI_SHRINK'],c30['SOBOL'])
sec_a={r['method']:r['construction_s'] for r in L[28]['comparison']['results']}
report=f'''# LARP — AB 3.2.1: hasta 30 ciclos para utilidad del muestreo adaptativo

**Fecha:** 22-10-2026. **Estado:** 30 condiciones evaluadas, exploración parcialmente adaptativa, C30 prueba de una escena nueva no utilizada en el diseño. **Originalidad demostrada: 1/3.** No hay una contribución nueva de nivel 2/3 ni una mejora neuronal 3/3 acreditada.

## Síntesis ejecutiva y decisión

Se conserva la propuesta **COSI-SHRINK** como método de integración espacial RGB de bajo presupuesto cuando hay pocos parches piloto, pero **STOP** a proclamar que reemplaza diseño de sensores GP, cuadratura bayesiana o colocación multiclase especializados. Su ventaja real en la única imagen de retina reservada es **{pct_power:.2f}%** menos RMSE que la alternativa espectral por canal y **{pct_sobol:.2f}%** menos que Sobol, con 24 lecturas en el mismo vector fijo de cuotas [6,16,2]. Con una sola imagen externa nueva no pueden atribuirse intervalos de generalización entre dominios. El conjunto de 1.100 recortes no equivale a 1.100 escenarios independientes: pertenecen todos a esa imagen.

**Próximo cuello de botella de evidencia:** múltiples escenas/estaciones físicas realmente independientes, adquisiciones de señales multivariantes nativas, estimadores rivales competentes y control de coste/corrupciones. La mejora incremental atribuible a covarianzas entre canales sigue débil; una penalización POWER-DIAG obtiene resultados cercanos.

## Contrato A–J / estimando

- Variable verdadera: media espacial ponderada de canales RGB sRGB **sin linealización fotométrica**, sobre un recorte 24×24. Peso w=(0.2126, 0.7152, 0.0722), elegido antes de esta campaña en investigaciones previas (la cuota 6–16–2 también fue seleccionada con resultados de test previos, no es confirmatoria).
- Intervención: seleccionar posiciones fijas para 24 lecturas en 3 tipos; sensor a un canal/píxel; un tipo permite ubicaciones coincidentes con otro. Estimador común: promedio por tipo con pesos fijos. Se registra por separado readout lineal entrenado.
- Datos: train de `skimage.data` = astronaut, coffee, chelsea, immunohistochemistry (4 imágenes × 450 recortes); desarrollo = rocket y hubble_deep_field (2 × 240 recortes) **ya usados por LARP en fase anterior**; un único nuevo test = retina, 1.100 recortes sobre ROI predefinida `[300:1100,300:1100]`. Todo 2D, no red ambiental física ni retina de gallina.
- Rivales: SOBOL; DIRECT (minimiza directamente MSE piloto); GP (greedy condicional de covarianza de las lecturas al objetivo, con regularización, selección original restringida a 72 ubicaciones por canal); POWER_DIAG (potencia Fourier por tipo sin covarianzas cruzadas); COSI_SHRINK (50% diagonal, 50% matriz de covarianza cruzada de 40 modos). **GP inicial selecciona para readout aprendido, no para la media fija**: la tabla principal no constituye una comparación de GP en su objetivo propio. La auditoría lo corrige parcialmente.
- Unidad real de transferencia: imagen/escena. Semillas de recorte no son unidades de replicación independientes.
- Alcance epistemológico: 29 condiciones exploratorias que miraron resultados de desarrollo, una nueva escena C30 evaluada una sola vez. El planteamiento general, pesos y cuotas ya se habían desarrollado mirando dos escenas utilizadas de nuevo como desarrollo; ni siquiera el C30 constituye replicación multisite.

## Gobernanza del branching

C01 comienza con un contraste de cinco métodos. C02–C07 investigan número de parches piloto, C08–C13 presupuesto sensorial, C14–C18 sensibilidad al índice RGB, C19–C23 participación de covarianza cruzada, C24–C28 dependencia de regularización GP, C29 congela y selecciona, C30 abre la imagen externa. **Los valores de la rejilla de experimentos estaban programados antes de la corrida**; los nombres de estado FOCUS/PIVOT y la elección de rival dependieron del vencedor previo. No son treinta rediseños autónomos y creativos. El ledger guarda por condición parámetro, evidencia inmediatamente anterior, método ganador, lecturas, coste, diagnóstico. La frontera externa solo se abrió tras grabar `holdout_freeze.json` y su SHA-256 en la traza C30.

Hubo una incidencia de instrumentación en el primer intento, ANTES de obtener los resultados: multiplicación de covarianza con forma incompatible; se reparó `C@means` por `einsum('kab,bk->ak', ...)` y se ejecutó completa la batería. No se atribuye valor científico a esa incidencia.

## Resultados C01–C29 (solo selección dentro del desarrollo)

Victorias por mínimo RMSE fijo, sobre 29 condiciones **heterogéneas y dependientes**: {json.dumps(z['c1_to_c29_dev_win_counts'],ensure_ascii=False)}. La media sobre el subconjunto de condiciones con índice y cuota iniciales, y piloto hasta 64, fue:

| Método | RMSE medio en desarrollo, subconjunto elegido |
|---|---:|
'''
for k,v in z['eligible_dev_means'].items():report+=f'| {k} | {v:.6f} |\n'
report+='''
Estas medias no constituyen un estimando poblacional: son combinaciones de semillas, shrinkage y exposición previa a escenas, sin replicación por dominio.

## C30 — escena nueva, diseño congelado

| Método | RMSE retina (promedio de 1.100 recortes dependientes) |
|---|---:|
'''
for k,v in c30.items():report+=f'| {k} | {v:.6f} |\n'
report+=f'''
La ventaja COSI vs POWER_DIAG es {pct_power:.2f}% en la retina. En absolutos, la separación es {c30['POWER_DIAG']-c30['COSI_SHRINK']:.6f}; no hay IC entre escenas posible con una escena. **El nuevo test está consumido** y no debe reutilizarse para pretender confirmación de mejoras posteriores.

## Auditoría adversarial (reparación, no ciclos adicionales)

El primer comparador GP fue diseñado para reducir varianza condicional del objetivo bajo un **estimador lineal aprendido**, mientras el ranking principal lo juzgaba con **media fija**. Eso mezcla tratamiento con función de pérdida. Se preservan los valores primarios y se añade una auditoría con readouts Ridge comunes, y un GP con 576 posiciones posibles en cada uno de los tres canales (frente a las 72 iniciales), usando n=28 y n=180 datos piloto. Se registran riesgos de los dos estimadores en desarrollo y retina, **todos los nuevos análisis en retina son post hoc** tras C30.

| n piloto | Método | RMSE desarrollo (media fija) | RMSE desarrollo (Ridge) | RMSE desarrollo (posterior gaussiano) |
|---|---|---:|---:|---:|
'''
for q in A['new_full_candidate_gp_controls']:report+=f"| {q['pilot_n']} | {q['method']} | {q['development_fixed']:.6f} | {q['development_ridge']:.6f} | {q['development_GP_readout']:.6f} |\n"
report+='''
Ni esta implementación de GP exhaustivo ni el Ridge elegido han recibido una búsqueda profunda de hiperparámetros y están muy condicionados por n pequeño; **no constituye reproducción del algoritmo de Krause ni de un método de estado del arte**. Se probó que el control original era desfavorable para GP por desalineación objetivo/evaluación: no usar sus pérdidas en la media fija como demostración de superioridad COSI sobre diseño GP.

## Robustez posterior C29 (mismo desarrollo; no confirmación)

| Método | Limpio | 25% lecturas aleatoriamente perdidas | Ruido de lectura σ=.03 (RMSE esperado) |
|---|---:|---:|---:|
'''
for q in S['results']:report+=f"| {q['method']} | {q['clean']:.6f} | {q['mean_25pct_dropout']:.6f} | {q['noise_sigma_0p01_0p03_0p06_expected_rmse'][1]:.6f} |\n"
report+='''
La mejora geométrica relativa puede perder relevancia cuando domina el ruido de lectura. El análisis de corrupción es posterior a la selección y no prueba robustez industrial.

## Pivot de transportabilidad a observación física temporal (NO C31)

Datos reales NOAA `statsmodels.datasets.elnino`, años 1950–2010, temperatura mensual de superficie del mar en Niño 1+2. Problema **univariado temporal**: estimar media anual observando solo 4 de los 12 meses. TRAIN 1950–1976, DEVELOPMENT 1977–1995, TEST temporal 1996–2010. Esta prueba no valida interacciones multiclase COSI: contrasta un principio análogo de regularizar muestreo por covarianza frente a un diseño temporal sencillo. Bajo 12 años piloto, muestreo trimestral en meses [1,4,7,10] obtiene RMSE TEST ~0.242 °C; ajuste empírico covarianza/full elige meses [2,5,8,11], RMSE ~0.085 °C. El objetivo espectral estacionario/circulante se aferra al patrón trimestral subóptimo. **Ejemplo adverso de sesgo inductivo geométrico**: la regularidad no es la medida de calidad apropiada para todos los procesos físicos. Son 15 años test correlacionados temporalmente, no quince sitios.

Fuente de datos: `statsmodels.datasets.elnino` (NOAA ERSST.V3B): https://github.com/statsmodels/statsmodels/blob/main/statsmodels/datasets/elnino/data.py

## Estado del arte y originalidad

- Krause, Singh & Guestrin (2008), *Near-Optimal Sensor Placements in Gaussian Processes*: https://jmlr.org/papers/v9/krause08a.html; ya estudia selección de sensores robusta y aproximación bajo proceso gaussiano.
- Chen, Ji & Saibaba (2026), *Optimal Sensor Placement in Gaussian Processes via Column Subset Selection*: https://arxiv.org/abs/2601.20781; referencia adicional de métodos competitivos de selección por covarianza.
- Wei (2010), *Multi-Class Blue Noise Sampling*: https://www.liyiwei.org/papers/noise-sig10/; anterioridad de la organización multiclase.

Una forma cuadrática con matriz de covarianza empírica de coeficientes Fourier pertenece a discrepancia espectral/kernel adaptada al objetivo. La nueva etiqueta COSI no la convierte en ley inédita. **No hay transferencia 3D, aprendizaje LLM, eficiencia económica real calculada ni ventaja general verificada.**

## Decisión AB-DECIDE

**FOCUS estrecho condicionado** sobre diseño de lectura espacial de agregados con presupuesto fijo y n piloto pequeño; **STOP** a afirmar que COSI supera al estado del arte o que el efecto proviene íntegramente de las covarianzas cruzadas. El siguiente estudio solo merece ciclos si se consiguen al menos 4–6 escenas/ubicaciones físicas de test **sin uso previo**, cuotas y métricas fijadas por entrenamiento/validación, más controles de *kernel quadrature* y procesos gaussianos optimizados al mismo readout y la misma información. Si los clásicos ganan, reutilizar esta línea como herramienta de ingeniería o descartarla, no forzar originalidad.

**Trazabilidad:** `experiment.py` genera ledger C01–C30, `holdout_freeze.json` fija selección antes de lectura final, `audit.py` reevalúa GP, `temporal_pivot.py` transportabilidad, `stress_audit.py` estrés, `tests.py` invariantes, `summary.json`, `audit.json`, `stress_audit.json`, `temporal_pivot.json`, `run.log` y hashes en `MANIFEST_SHA256.json`. `CLEAN_CLONE_NOT_VERIFIED`: el entorno se probó localmente con dependencias instaladas; no se ha ejecutado sobre clon limpio ni en un segundo sistema.
'''
(P/'DICTAMEN_AB30_VALUE.md').write_text(report)
(P/'PRIORS_LARP_VALUE30.md').write_text('''# Priors acumulativos LARP — nuevo bloque VALUE30 (no reemplazan los anteriores)

Fecha 22-10-2026. Procedencia `DICTAMEN_AB30_VALUE.md`, scripts/JSON de este paquete. Todos son cualitativos; no son Bayes factors ni posteriores numéricos.

| ID | Proposición / alcance | A favor | En contra / límites | Falsador / siguiente prueba | Estado |
|---|---|---|---|---|---|
| VAL30-R01 | COSI-SHRINK mejora la estimación espacial media RGB con pocas lecturas en escenas nuevas | C30 retina .001677 vs POWER-DIAG .001729 y SOBOL .001850 | Una sola escena nueva; cuota/objetivo adaptados antes a otros test; diferencias pequeñas | Múltiples escenas adicionales y comparadores KQ/GP equiparados | EXPLORATORIO_APOYO_ESTRECHO |
| VAL30-R02 | La covarianza CRUZADA entre tipos explica casi toda la ganancia | Algunos C20 y C29 favorecen COSI vs diagonal | C19 iguala con shrink0 y C21–C23 POWER-DIAG gana; efecto marginal modesto | Ablaciones cruzadas con roles naturales, costo y geometría aislados | DEBILITADO |
| VAL30-R03 | COSI domina al diseño bayesiano de sensores | 29 condiciones score medio fijo favorable a COSI | GP inicial optimizado para readout aprendido pero evaluado con media fija; el control no era pertinente; auditoría GP_FULL solo en dos escenarios | Implementar KQ/GP/column subset y optimizar al mismo estimador/budget | NO_VALIDADO |
| VAL30-R04 | COSI supera diseño empírico directo con escasos pilotos | C02-C03 frente a DIRECT, y estudio RGB previo con pilotos pequeños | DIRECT gana en C05–C07 a tamaños mayores; riesgos de leakage entre escenas | Validar en nuevas fuentes físicas y sobre varias semillas/repartos | APOYO_CONDICIONAL |
| VAL30-R05 | Regularidad espectral es universalmente útil en fenómenos físicos | Alguna evidencia sobre imágenes | En Niño 1+2, muestreo temporal trimestral .242 °C frente a cov/full .085 °C en periodo final; otro problema, pero falsador de universalidad | Replicar temporal multivariado/sistema de lectura real | UNIVERSALIDAD_REFUTADA |
| VAL30-R06 | Conteos de ganadores de 29 ciclos aportan 29 replicaciones | Ninguna | Mismos conjuntos de imágenes, grilla programada, parámetros adaptados | Replicación por escenarios verdaderamente distintos con unidades correctas | RECHAZADO |
''')
(P/'NOTA_AB_M030.md').write_text('''# Propuesta metodológica AB-M030 — objetivo del estimador y comparador competente

**22-10-2026 · Estado:** PROPUESTA; no modificación normativa de AB 3.2.1/O1/O2. Procedencia: LARP VALUE30, `audit.json` y `DICTAMEN_AB30_VALUE.md`.

**Problema confirmado en el instrumento de comparación:** el selector inicial etiquetado GP escogía posiciones para maximizar reducción de varianza CONDICIONAL del estimando bajo un predictor aprendido, mientras la clasificación primaria le asignaba la media aritmética de lecturas con pesos fijos. En consecuencia, una cifra GP desfavorable NO identifica un fracaso de la colocación gaussiana en su tarea. También se le restringía a 72 candidatos por canal frente al espacio 576 de los rivales directos.

**Mejora candidata:** GATE `READOUT_OBJECTIVE_ALIGNMENT`: para comparar algoritmos de diseño de sensores, declarar de antemano qué predicción puede hacer cada uno (media fija, mínimo MSE lineal, posterior GP, estimador calibrado), y qué método de selección optimiza su pérdida. Igualar presupuesto de lecturas, acceso a datos, candidatos, preparación y recursos; evaluar con un readout común si el estimando es causalmente solo la geometría, y con el mejor readout propio si la pregunta es utilidad del pipeline. Si el control no comparte el mismo estimador, clasificar la comparación como **pipeline heterogénea**, nunca como superioridad geométrica específica.

**Coste y limitación:** entrenar y verificar estimadores adicionales tiene un coste real. Esta propuesta ya está parcialmente contenida en AB-M021/M024 y O2: registrar como operacionalización y reparación concreta, NO una nueva teoría metodológica ni eficacia general validada.

**Falsador:** si en varios problemas los distintos readouts son equivalentes bajo pruebas formales y empíricas, las comparaciones heterogéneas pueden ser pertinentes, pero esa equivalencia ha de mostrarse, no asumirse.
''')
(P/'README.md').write_text('''# LARP VALUE30 — exploración adaptativa parcialmente programada (2026-10-22)

## Reproducir (Python 3.10+, numpy, scipy, sklearn, scikit-image, statsmodels, matplotlib)

Desde esta carpeta: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiment.py` **en una carpeta limpia o tras borrar `ledger.jsonl`**; los archivos existentes ya contienen la corrida histórica y se preservan. Para auditar sin reabrir el conjunto externo: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python tests.py`. Los experimentos de reparación `audit.py`, `stress_audit.py`, `temporal_pivot.py` son EXPLORATORIOS posteriores y pueden regenerarse separadamente.

El detector de una nueva escena en `experiment.py` abre `skimage.data.retina()` solo en C30, después de escribir `holdout_freeze.json`. La misma escena NO vuelve a ser desconocida en un segundo run de este mismo protocolo. Los reportes de auditoría que usan retina son post hoc.

Entrada: escenas de scikit-image disponibles localmente y el archivo de NOAA Niño 1+2 incluido en `statsmodels.datasets.elnino`. No distribuir ni reclamar licencia comercial de imágenes sin comprobar condiciones del proveedor.

**CLEAN_CLONE_NOT_VERIFIED**, experimentos GPU no ejecutados, ninguna validación en datos 3D. Ver dictamen completo y priors por estado.
''')
manifest={}
for f in sorted(P.iterdir()):
 if f.is_file() and f.name not in ('MANIFEST_SHA256.json',):manifest[f.name]=hashlib.sha256(f.read_bytes()).hexdigest()
(P/'MANIFEST_SHA256.json').write_text(json.dumps(manifest,indent=2))
with zipfile.ZipFile('/mnt/data/LARP_AB30_VALUE_20261022.zip','w',zipfile.ZIP_DEFLATED) as zz:
 for f in sorted(P.iterdir()):
  if f.is_file():zz.write(f,f.name)
print('files',len(manifest),'zip bytes',Path('/mnt/data/LARP_AB30_VALUE_20261022.zip').stat().st_size)
print('retina advantage COSI over power',pct_power,'over Sobol',pct_sobol)
