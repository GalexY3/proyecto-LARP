# LARP / AB 3.2.1 — F01–F30 · Dictamen de transporte multiespecialista

Fecha: 2026-10-30. Rama `research/ab-r-functional-routing-20261030`. **30 contrastes A–J ejecutados dentro de un diseño factorial, no 30 estudios independientes**. Diseño y código congelados en GitHub *antes* de outcomes: protocolo `4bb177d378eb12fe3f376c58a574cd0d75939f34`, fuente completa `a620c5c912cf1c34e7f898287451439c28908157`, SHA256 fuente `cf187e6a367239dd46e2e25351158f5c1d8020423750987c4b8dc3fdcd9118d2`. Conservar `main`. Sin CI costosa.

## Problema y origen de datos
N=400 nodos con conteos de tipos originales (163,85,68,50,34), una observación escalar por nodo, seis conexiones **dirigidas** salientes. Se reconstruye una media ponderada de cinco campos no observados directamente en cada nodo, buscando la lectura del mismo tipo más próxima dentro de 1 o 2 saltos, imputando 0 si falta. No hay entrenamiento de parámetros: es una evaluación de *adquisición de información funcional*, no de aprendizaje neuronal. Tres semillas geométricas y ocho realizaciones de campos para 6 contextos ×5 perturbaciones. **12.960 registros** que usan de forma correlacionada las mismas fuentes sintéticas; n efectivo NO 12.960 mundos independientes. Condiciones: limpio, drop aleatorio 15/40%, pérdida 40% del tipo raro, ruido σ=.25. Contextos: baja frecuencia, alta frecuencia, fuerte correlación, anticorrelación, señal rara dominante, manchas locales.

## Comparadores
Misma salida de grado seis: grafos espacialmente próximos sobre retícula, CVT condicionada por clase, MHU espectral aproximada; grafos de selección de tipos sobre cada geometría, aleatorio 6-grado y circulante aleatorio 6-grado. El último **no es un expansor certificado**. El optimizador MHU de estos ensayos es un **proxy finito**, no las geometrías nativas Scale3D del repositorio, cuya NPZ original no se descargó desde el conector. CVT tampoco es el algoritmo original LOCAL. No se ha entrenado MoE ni un router aprendido; tiempo, construcción y longitud de aristas no están equiparados.

## Resultados completos por familia (NMSE: menor es mejor)

| Método | NMSE un salto | NMSE dos saltos | Disponibilidad tipos un salto | Distancia arista media |
|---|---:|---:|---:|---:|
| cvt_type | 0.4355 | 0.4355 | 1.000 | 0.0546 |
| cvt_knn | 0.4938 | 0.4368 | 0.904 | 0.0535 |
| mhu_type | 0.5767 | 0.5767 | 1.000 | 0.0626 |
| mhu_knn | 0.6490 | 0.5785 | 0.747 | 0.0551 |
| grid_type | 0.6033 | 0.6033 | 1.000 | 0.0647 |
| grid_knn | 0.6645 | 0.5999 | 0.734 | 0.0569 |
| expander_deg6 | 1.5259 | 1.5897 | 0.713 | 0.3841 |
| random_deg6 | 1.5181 | 1.4592 | 0.720 | 0.3834 |

- **CVT con selección por tipo domina MHU con selección por tipo en 30/30 condiciones**, diferencia media NMSE (MHU−CVT): 0.1413. Los resultados son relativos a estos dos **proxies** sobre datos simulados, no a las geometrías aviares originales.
- Seleccionar vecinos por tipo sobre la misma MHU aproximada mejora MHU kNN en **24/30** condiciones y la empeora en 6/30. La media de ganancia NMSE kNN−tipo: 0.0723.
- En 24/30 condiciones el ganador de las políticas principales es CVT + selección por tipo, en 5/30 CVT kNN y en 1/30 MHU kNN. Ninguno de los 30 produce una victoria general de la MHU aproximada frente a CVT.
- Disponibilidad de los cinco tipos por nodo con selección explícita alcanza 100% **antes del dropout** con seis aristas + señal propia; con vecinos MHU locales es 74.7%. Esto identifica una ventaja del enrutamiento, pero no demuestra mejora de aprendizaje neuronal ni de coste físico.

## Diagnóstico geométrico adversarial

| Geometría | Media espectral de unión S sobre 8 modos | Media espectral por tipos S | Cuantización media Q por tipos | Radio percentil95 |
|---|---:|---:|---:|---:|
| cvt | 0.033012 | 0.068713 | 0.002768 | 0.074697 |
| grid | 0.000000 | 0.585019 | 0.004507 | 0.110366 |
| mhu_proxy | 0.000024 | 0.000089 | 0.004085 | 0.102287 |

El proxy MHU sí reduce drásticamente su energía espectral objetivo: su pérdida contra CVT no procede de que se haya olvidado ejecutar el término de Fourier. Sin embargo, CVT consigue distancias de cuantización por clase considerablemente menores, que son directamente útiles para recuperar campos espaciales con vecinos próximos. Las métricas geométricas de este cuadro son un análisis descriptivo **posterior a outcomes** y no forman una nueva confirmación preregistrada.

## Incidencia de instrumentación / falso rival
Las políticas llamadas `mhu_type` y `mhu_hybrid` producen **exactamente los mismos conjuntos de vecinos** para todos los 400 nodos y las 3 geometrías (1.200/1.200), aunque difiere el orden. En consecuencia todas las 1.440 predicciones emparejadas por modalidad y perturbación son exactamente iguales: el híbrido no constituye un comparador independiente. **Eliminar cualquier interpretación de comparación MHU_TYPE vs MHU_HYBRID.** Conservar ambos outputs en el raw por auditoría, no reescribirlos.

## A–J, validación y límites
Todos los 30 contratos individuales F01–F30 constan en `LEDGER_F01_F30.json` (escenario, rival, estimando, ejecución, resultados por condición, auditoría, priors, dictamen y decisión). Fuente de outcomes raw: `results.json` del ZIP archivado con hash SHA256 `c968c85880b16e1cf8caf5ca41104c49683ff601a54be8b3e5be1d51790c057a`. Reejecución con el mismo código/datos/entorno produce **coincidencia de bytes exacta**; esto es reproducibilidad técnica, no réplica externa.

**Una limitación científica sustantiva:** el estimador escoge el vecino observable más cercano ANTES del fallo. No sustituye sensores caídos por otros candidatos; esto puede sesgar a la baja condiciones con abandono. Los pesos entre modalidades son conocidos y no se aprenden. El benchmark es un único generador sintético con seis tareas parametrizadas; no hay variedad independiente de datasets ni holdout real.

**R5:** STOP_LOCAL en este generador, puesto que seguir añadiendo semillas o perturbaciones no resolvería el bloqueo causal. PIVOT a descifrar las geometrías nativas NPZ, entrenar un enrutador fuerte (tipo MoE/GraphGPS/expansor real), igualar coste de construcción y distancia/comunicación y obtener fuentes multicanal independientes. No conceder N1 nuevos por información repetida/puesta por diseño; N2=N3=0. CT2 línea matemática condicionada 24/100 sin incremento (ordinal, no probabilidad). Ninguna conclusión sobre supremacía general MHU.

Fuentes de contexto: Jiao et al. PRE 2014 DOI 10.1103/PhysRevE.89.022721; Wei SIGGRAPH 2010 https://www.liyiwei.org/papers/noise-sig10/; Black et al. ICML2023 https://proceedings.mlr.press/v202/black23a.html; las fuentes no validan este experimento automáticamente.
