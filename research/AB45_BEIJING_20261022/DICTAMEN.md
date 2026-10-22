# LARP / AB 3.2.1 — 45 ciclos secuenciales sobre datos físicos multisitio (22-10-2026)

**Dictamen:** NOVEDAD 1/3; **2/3 NO DEMOSTRADO**. Estudio EXPLORATORIO. Por primera vez en esta línea se utilizaron mediciones originales de doce estaciones de calidad del aire, pero **no** se ejecutó el generador Scale3D ni el COSI original y no se entrenó ninguna arquitectura neuronal LARP.

## Procedencia, observaciones y separación temporal
Fuente primaria: UCI *Beijing Multi-Site Air Quality*, DOI 10.24432/C5RK5G, CC BY 4.0. Los doce CSV horarios, alojados en `KM-drago/Beijing-Multi-Site-Air-Quality-Data`, contienen 35.064 filas por estación: 420.768 observaciones horarias en total, del 1-3-2013 al 28-2-2017. `weekly_observed.json` conserva los nombres de estación, SHA exactos de los blobs originales, recuentos de horas observadas y cuatro medias semanales: PM2.5, PM10, NO2 y O3. Un valor semanal se admite solo con al menos 84 horas válidas; lo demás es nulo, **sin interpolación en el archivo**.

209 semanas consecutivas y partición temporal fija: entrenamiento semanas 0–129 (1-3-2013 a 27-8-2015), validación 130–169 (28-8-2015 a 2-6-2016) y TEST 170–208 (3-6-2016 a 28-2-2017). Los métodos imputan entradas incompletas mediante medias del **entrenamiento** y estandarizan desde ese mismo conjunto; no utilizan el test para fijar estos parámetros. Objetivos urbanos derivados de las doce estaciones: PM2.5 medio, NO2 medio, O3 medio, promedio de las tres estaciones de mayor PM2.5 y diferencia PM10−PM2.5. Exigen al menos diez estaciones válidas para definir el objetivo. Sus estimaciones son indicadores propios del conjunto, no exposición poblacional ponderada.

## Hipótesis y competidores
Se pregunta si una selección de pocas lecturas de estación × contaminante condicionada por tipos, diversidad y correlación supera, con **el mismo predictor Ridge**, alternativas supervisadas sólidas. Ocho brazos en el código:
- GREEDY: ganancia condicional supervisada sobre covarianza estimada (shrinking leve);
- SHRINK: ganancia condicional supervisada con covarianza fuertemente contraída;
- RANK: correlación individual con el objetivo;
- MAXMIN: mezcla de relevancia y descorrelación;
- TYPE: priorización explícita de tipos y estaciones nuevos;
- COSI_PROXY: mezcla heurística de ganancia condicional, cobertura por tipos y diversidad;
- DOPT: aproximación greedy de diversidad de covarianza, sin objetivo;
- RANDOM: selección seudoaleatoria controlada.

**COSI_PROXY NO equivale al COSI original ni a MHU**, y TYPE tampoco tiene certificados multihiperuniformes. Los costes de lectura son unitarios ficticios: no se midió hardware, energía, comunicación ni localización espacial. Los métodos supervisados usan el valor del objetivo durante la fase histórica de entrenamiento, no durante la evaluación.

## Instrumentación del branching
La fuente `run_campaign.mjs` se versionó antes de abrir el test. Ejecuta 45 pruebas consecutivas de VALIDACIÓN; la condición siguiente se determina usando exclusivamente ganador/margen del ciclo previo, evitando repetir la misma combinación, y registrando `selection_justification`, `result_winner`, `next_design` y `next_reason`. Las familias son un catálogo conocido: TARGET_SHIFT, BUDGET_SHIFT, DATA_SCARCITY, REGULARIZATION, DOMAIN_TRANSFER y PILOT_COUNTEREXAMPLE. Por ello es branching genuino **de decisiones entre alternativas predefinidas**, no 45 teorías nuevas ni 45 replicaciones independientes. La validación se reutiliza 45 veces: los márgenes están sujetos a selección adaptativa.

Ganadores por VALIDACIÓN: GREEDY **15**; SHRINK **14**; RANK **11**; MAXMIN **3**; TYPE **1**; RANDOM **1**; COSI_PROXY **0** y DOPT **0**. No calcular p-valores sobre la distribución de victorias: las condiciones son heterogéneas, dependientes y elegidas adaptativamente.

## TEST cronológico abierto una sola vez después de C45
Cada objetivo tiene seis lecturas y un Ridge común; en cada objetivo se eligió un método por validación con protocolo final fijo. Unidades RMSE: µg/m³ (PM25, NO2, O3, TOP3, diferencia PM10−PM25). Todos tienen 39 semanas evaluables.

| Objetivo | Seleccionado en validación | TEST seleccionado | GREEDY TEST | SHRINK TEST | COSI_PROXY TEST |
|---|---|---:|---:|---:|---:|
| PM2.5 urbano | GREEDY | 2.0625 | 2.0625 | 2.0625 | 2.7934 |
| NO2 urbano | SHRINK | 2.0269 | **1.8609** | 2.0269 | 2.5824 |
| O3 urbano | GREEDY | 3.1189 | 3.1189 | **2.2160** | 5.4176 |
| Media de las tres estaciones PM2.5 máximas | RANK | **2.7082** | 3.0694 | 3.0694 | 3.8096 |
| Media PM10−PM2.5 | GREEDY | 4.5326 | 4.5326 | 4.9547 | 5.8869 |

Ninguna diferencia es una estimación causal independiente ni implica generalización a otras ciudades. NO2 muestra un fallo de selección de método: SHRINK elegida en validación pierde frente a GREEDY en test. La aparente alternativa ganadora ex post en cada columna **no** fue seleccionada sin mirar test. Cinco objetivos comparten semanas, por lo que no son cinco réplicas independientes.

### Adversarial post hoc (no confirmatorio)
Tras abrir TEST se añadió un control simple: escoger seis estaciones fijas `[0,2,4,6,8,10]` y utilizar el promedio contemporáneo del contaminante, o TOP3 de seis valores. RMSE de esta regla: PM2.5 **6.4986**, NO2 **3.7698**, O3 **3.2026** y PM2.5-TOP3 **10.1399**. El predictor Ridge entrenado mejora este comparador en PM2.5 y NO2, pero apenas lo mejora en O3. Las seis posiciones no fueron optimizadas; no constituye el mejor baseline de muestreo uniforme ni una nueva confirmación.

## Valor científico / antecedente
La ganancia incremental de covarianza, D-óptimo, shrinkage, selección greedy, diseño robusto y modelos de colocación de sensores tienen antecedentes directos: Krause, Singh y Guestrin (JMLR 2008); Krause et al. (TOSN 2011); multi-type sensor placement en Gaussian spatial fields (2018); comparación POD/QR pivot/DEIM de estaciones PM2.5 publicada en ACS Environmental Au (2022); Li-Yi Wei (SIGGRAPH 2010) para multi-class blue noise. Esta campaña **no derrota estos controles competentes** ni presenta una fórmula nueva probada.

- https://www.jmlr.org/papers/v9/krause08a.html
- https://doi.org/10.1145/1921621.1921625
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6339194/
- https://doi.org/10.1021/acsenvironau.1c00051
- https://www.liyiwei.org/papers/noise-sig10/

## Riesgos, priors y decisión
Se instrumentó una corrección antes del experimento al detectar que el encabezado del CSV original llevaba comillas (sin la corrección se registraban falsamente 0 valores válidos). El fallo se detectó en el gate de adquisición, antes de cualquiera de los 45 ciclos; ningún resultado inválido se elevó a evidencia. La serie final no está interpolada; imputación posterior de las features en cada entrenamiento.

La reutilización del holdout de otros estudios LARP no alcanza esta nueva rama, pero este holdout de Pekín **queda consumido ahora**. Otras limitaciones: semanas temporalmente correlacionadas, un solo conjunto de estaciones, tarea derivada de observaciones contemporáneas, apenas 39 semanas test, no costes físicos ni observación de fallos reales, ausencia de comparadores GP/QR-DEIM fuertes, no grafo de comunicación y ausencia de prueba de Scale3D.

**AB-DECIDE: STOP a la reivindicación de novedad mediante COSI_PROXY/TYPE en selección estática del mismo conjunto.** Hallazgo útil: la selección de variables objetivo-consciente funciona bien frente a un control ingenuo, pero es una técnica existente. La hipótesis de que MHU ofrece ventaja arquitectónica general continúa NO VALIDADA.

**Propuesta de pivot que merezca 2/3:** aislamiento causal de la contribución de *coordinación multiclase* en computación local heterogénea y con límites de mensajes, comparada con multi-class blue noise real, grafos tipados aprendidos y diseños robustos de literatura, sobre paquetes/medidas físicos o datasets independientes. Exigir intervención que preserve cobertura, tipo, presupuesto y espectro individual pero altere solo fases cruzadas, con predicción que no sea consecuencia algebraica del propio objetivo de entrenamiento. No presumir originalidad antes de revisar trabajos anteriores.

## Reproducción
Node.js 20+; sin librerías externas en esta etapa:
`node research/AB45_BEIJING_20261022/run_campaign.mjs`
`node research/AB45_BEIJING_20261022/verify_results.mjs`

`campaign_results.json` conserva los resultados de 45 ciclos, las selecciones por brazo, el estado y motivo de la rama siguiente y los cinco tests finales. `simple_mean_posthoc_audit.json` conserva la comparación auxiliar etiquetada después de mirar TEST. `weekly_observed.json` referencia los doce blobs CSV originales y la licencia del dataset. La reconstrucción exacta de medias a partir de CSV puede hacerse usando las cuatro columnas, fecha UTC, semanas ancladas en 1-3-2013 y umbral de 84 horas por estación y semana; falta todavía un script descargador automatizado de CSVs compatible con entornos aislados.
