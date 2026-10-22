# LARP — AB 3.2.1: hasta 30 ciclos para utilidad del muestreo adaptativo

**Fecha:** 22-10-2026. **Estado:** 30 condiciones evaluadas, exploración parcialmente adaptativa, C30 prueba de una escena nueva no utilizada en el diseño. **Originalidad demostrada: 1/3.** No hay una contribución nueva de nivel 2/3 ni una mejora neuronal 3/3 acreditada.

## Síntesis ejecutiva y decisión

Se conserva la propuesta **COSI-SHRINK** como método de integración espacial RGB de bajo presupuesto cuando hay pocos parches piloto, pero **STOP** a proclamar que reemplaza diseño de sensores GP, cuadratura bayesiana o colocación multiclase especializados. Su ventaja real en la única imagen de retina reservada es **2.97%** menos RMSE que la alternativa espectral por canal y **9.34%** menos que Sobol, con 24 lecturas en el mismo vector fijo de cuotas [6,16,2]. Con una sola imagen externa nueva no pueden atribuirse intervalos de generalización entre dominios. El conjunto de 1.100 recortes no equivale a 1.100 escenarios independientes: pertenecen todos a esa imagen.

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

Victorias por mínimo RMSE fijo, sobre 29 condiciones **heterogéneas y dependientes**: {"SOBOL": 1, "DIRECT": 7, "GP": 0, "POWER_DIAG": 6, "COSI_SHRINK": 15}. La media sobre el subconjunto de condiciones con índice y cuota iniciales, y piloto hasta 64, fue:

| Método | RMSE medio en desarrollo, subconjunto elegido |
|---|---:|
| SOBOL | 0.010359 |
| DIRECT | 0.010387 |
| GP | 0.012697 |
| POWER_DIAG | 0.009806 |
| COSI_SHRINK | 0.009260 |

Estas medias no constituyen un estimando poblacional: son combinaciones de semillas, shrinkage y exposición previa a escenas, sin replicación por dominio.

## C30 — escena nueva, diseño congelado

| Método | RMSE retina (promedio de 1.100 recortes dependientes) |
|---|---:|
| SOBOL | 0.001850 |
| DIRECT | 0.001831 |
| GP | 0.003039 |
| POWER_DIAG | 0.001729 |
| COSI_SHRINK | 0.001677 |

La ventaja COSI vs POWER_DIAG es 2.97% en la retina. En absolutos, la separación es 0.000051; no hay IC entre escenas posible con una escena. **El nuevo test está consumido** y no debe reutilizarse para pretender confirmación de mejoras posteriores.

## Auditoría adversarial (reparación, no ciclos adicionales)

El primer comparador GP fue diseñado para reducir varianza condicional del objetivo bajo un **estimador lineal aprendido**, mientras el ranking principal lo juzgaba con **media fija**. Eso mezcla tratamiento con función de pérdida. Se preservan los valores primarios y se añade una auditoría con readouts Ridge comunes, y un GP con 576 posiciones posibles en cada uno de los tres canales (frente a las 72 iniciales), usando n=28 y n=180 datos piloto. Se registran riesgos de los dos estimadores en desarrollo y retina, **todos los nuevos análisis en retina son post hoc** tras C30.

| n piloto | Método | RMSE desarrollo (media fija) | RMSE desarrollo (Ridge) | RMSE desarrollo (posterior gaussiano) |
|---|---|---:|---:|---:|
| 28 | GP_FULL | 0.015772 | 0.016803 | 0.015390 |
| 28 | COSI_SHRINK | 0.007752 | 0.008391 | 0.014325 |
| 28 | POWER_DIAG | 0.008771 | 0.008949 | 0.015086 |
| 180 | GP_FULL | 0.010267 | 0.010886 | 0.010771 |
| 180 | COSI_SHRINK | 0.009424 | 0.009427 | 0.009417 |
| 180 | POWER_DIAG | 0.010231 | 0.010340 | 0.010319 |

Ni esta implementación de GP exhaustivo ni el Ridge elegido han recibido una búsqueda profunda de hiperparámetros y están muy condicionados por n pequeño; **no constituye reproducción del algoritmo de Krause ni de un método de estado del arte**. Se probó que el control original era desfavorable para GP por desalineación objetivo/evaluación: no usar sus pérdidas en la media fija como demostración de superioridad COSI sobre diseño GP.

## Robustez posterior C29 (mismo desarrollo; no confirmación)

| Método | Limpio | 25% lecturas aleatoriamente perdidas | Ruido de lectura σ=.03 (RMSE esperado) |
|---|---:|---:|---:|
| SOBOL | 0.009287 | 0.012416 | 0.011142 |
| DIRECT | 0.008870 | 0.012088 | 0.010797 |
| GP | 0.010829 | 0.013705 | 0.012457 |
| POWER_DIAG | 0.008846 | 0.012258 | 0.010777 |
| COSI_SHRINK | 0.008310 | 0.011804 | 0.010342 |

La mejora geométrica relativa puede perder relevancia cuando domina el ruido de lectura. El análisis de corrupción es posterior a la selección y no prueba robustez industrial.

## Pivot de transportabilidad a observación física temporal (NO C31)

Datos reales NOAA `statsmodels.datasets.elnino`, años 1950–2010, temperatura mensual de superficie del mar en Niño 1+2. Problema **univariado temporal**: estimar media anual observando solo 4 de los 12 meses. TRAIN 1950–1976, DEVELOPMENT 1977–1995, TEST temporal 1996–2010. Esta prueba no valida interacciones multiclase COSI: contrasta un principio análogo de regularizar muestreo por covarianza frente a un diseño temporal sencillo. Bajo 12 años piloto, muestreo trimestral en meses [1,4,7,10] obtiene RMSE TEST ~0.242 °C; ajuste empírico covarianza/full elige meses [2,5,8,11], RMSE ~0.085 °C. Ambos calendarios son trimestrales, separados por exactamente tres meses: **la diferencia NO refuta la utilidad del espaciamiento regular**, sino la elección de fase del muestreo. Un prior estacionario/circulante puede tratar como equivalentes configuraciones cuya fase con respecto al calendario importa para este proceso estacional. **Ejemplo adverso de no identificar la fase óptima**, no de que la regularidad sea perjudicial. Son 15 años test correlacionados temporalmente, no quince sitios.

Fuente de datos: `statsmodels.datasets.elnino` (NOAA ERSST.V3B): https://github.com/statsmodels/statsmodels/blob/main/statsmodels/datasets/elnino/data.py

## Estado del arte y originalidad

- Krause, Singh & Guestrin (2008), *Near-Optimal Sensor Placements in Gaussian Processes*: https://jmlr.org/papers/v9/krause08a.html; ya estudia selección de sensores robusta y aproximación bajo proceso gaussiano.
- Chen, Ji & Saibaba (2026), *Optimal Sensor Placement in Gaussian Processes via Column Subset Selection*: https://arxiv.org/abs/2601.20781; referencia adicional de métodos competitivos de selección por covarianza.
- Wei (2010), *Multi-Class Blue Noise Sampling*: https://www.liyiwei.org/papers/noise-sig10/; anterioridad de la organización multiclase.

Una forma cuadrática con matriz de covarianza empírica de coeficientes Fourier pertenece a discrepancia espectral/kernel adaptada al objetivo. La nueva etiqueta COSI no la convierte en ley inédita. **No hay transferencia 3D, aprendizaje LLM, eficiencia económica real calculada ni ventaja general verificada.**

## Decisión AB-DECIDE

**FOCUS estrecho condicionado** sobre diseño de lectura espacial de agregados con presupuesto fijo y n piloto pequeño; **STOP** a afirmar que COSI supera al estado del arte o que el efecto proviene íntegramente de las covarianzas cruzadas. El siguiente estudio solo merece ciclos si se consiguen al menos 4–6 escenas/ubicaciones físicas de test **sin uso previo**, cuotas y métricas fijadas por entrenamiento/validación, más controles de *kernel quadrature* y procesos gaussianos optimizados al mismo readout y la misma información. Si los clásicos ganan, reutilizar esta línea como herramienta de ingeniería o descartarla, no forzar originalidad.

**Trazabilidad:** `experiment.py` genera ledger C01–C30, `holdout_freeze.json` fija selección antes de lectura final, `audit.py` reevalúa GP, `temporal_pivot.py` transportabilidad, `stress_audit.py` estrés, `tests.py` invariantes, `summary.json`, `audit.json`, `stress_audit.json`, `temporal_pivot.json`, `run.log` y hashes en `MANIFEST_SHA256.json`. `CLEAN_CLONE_NOT_VERIFIED`: el entorno se probó localmente con dependencias instaladas; no se ha ejecutado sobre clon limpio ni en un segundo sistema.
