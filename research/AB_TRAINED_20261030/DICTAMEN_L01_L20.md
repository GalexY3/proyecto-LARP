# Dictamen LARP L01–L20 — Redes entrenadas y enrutamiento espacial

**30 de octubre de 2026 · AB3.2.1 O1–O7 · BRANCHING/PIVOT 20 ciclos autorizado.**

## Resumen ejecutivo

Se ejecutaron **20 condiciones funcionales preregistradas**, producto de 5 familias de señales espaciales × 4 perturbaciones, con **90 decodificadores neuronales entrenados**, 9 métodos de conexiones, 2 geometrías, 24 semillas de campos de entrenamiento, 6 de validación, 16 de evaluación. Total: **5.760 registros** (16 campos × 2 geometrías × 9 métodos × 20 condiciones). Todas las unidades inferenciales pertenecen a **un solo generador sintético**: no son 5.760 escenas reales ni 20 replicaciones independientes.

**Resultado adverso:** CVT por tipos promedio **0,2211 NMSE**, frente a MHU finita proxy por tipos **0,2873**. La diferencia MHU−CVT **+0,0662** favorece CVT en los **20/20 contrastes**. Con un enrutador supervisado entrenado con objetivos de TRAIN, CVT obtiene 0,5316 frente a MHU 0,5493; este enrutamiento aprendido concreto suele ser peor que enrutamiento por tipos o kNN competente. La política aprendida usa enlaces aproximadamente 3× más largos y puede perder continuidad local; no se ha demostrado que la longitud cause por sí sola el efecto.

**GRAN LIMITACIÓN:** Los seis NPZ N400 aviares originales **NO se descargaron**, aunque fueron localizados en GitHub y leídos sus certificados JSON. GitHub connector rechaza binarios NPZ y la red del contenedor no resuelve GitHub. Se evalúan exclusivamente geometrías proxy creadas por `ab30_functional.py`; no identificar estos resultados con retina aviar original ni con original LOCAL. Tampoco hay MoE de atención plenamente entrenado, Wei 2010 ejecutado ni dataset visual real. Un positivo no habría validado originalidad 2/3.

## A–J: diseño y freeze–run

A: contrato de verdad = reconstrucción de señal combinada de 5 modalidades por nodo bajo presupuesto de 400 lecturas escalares, seis enlaces dirigidos y comparadores equiparados en salidas y MLP. B: H1 modelo learned routing y/o geometría MHU aporta mejora diferencial; H0 competidores kNN/type CVT/grid no inferiores. C: 20 clases de estimandos contextual/perturbación, no 20 muestras externas. D: código congelado **antes** de resultados: SHA256 `320bab4445e5e381b9378b681940ada89fe6df74086c4c0f9a1b8e51b2d7b031`, commit GitHub `daee73553a74e0155962a186bb372cddc7e1289f`; prerregistro `PREREG_L01_L20.md`, commit `0ce03f7dd55dd37f33fa952e27ba44a344e38ab0`. E: 90 entrenamientos neuronales (mismos 1009 parámetros, 12 épocas, validación independiente de test); 5760 observaciones. F: auditoría de validez, autocrítica adversarial y ausencia de permisos/datos originales. G: las **10/10 celdas** se reprodujeron byte a byte **descontando exclusivamente `elapsed_sec`**; no hay réplica externa ni clon limpio. H: priors perjudiciales para MHU transmitidos sin borrado. I: nivel 0/3 para novedad causal o matemática; **N1 nuevos = N2 = N3 = 0**. J: STOP_LOCAL sobre generador ya usado y ruta supervisada ingenua; PIVOT condicionado a NPZ nativos y un learned attention/rewiring fuerte, y datos multicanal nuevos.

**Errata:** la primera ejecución continua terminó prematuramente por un límite de tiempo, no produjo JSON final ni se contó; el wrapper por celdas fue congelado ANTES del primer outcome completo en commit `30fbed674a641281577d9cfc0239966d1b84fb6f` y documentado en `ERRATA_RESOURCE_CAP.md` antes de la ejecución final. No se alteraron métodos ni seeds.

## Resultados globales

| Modelo | NMSE medio ↓ | Mediana ↓ |
|---|---:|---:|
| CVT | tipos | 0.2211 | 0.1315 |
| CVT | vecinos | 0.2360 | 0.1680 |
| MHU proxy | tipos | 0.2873 | 0.1879 |
| Retícula | tipos | 0.3024 | 0.2041 |
| MHU proxy | vecinos | 0.3266 | 0.2970 |
| Retícula | vecinos | 0.3443 | 0.3171 |
| CVT | ruta entrenada | 0.5316 | 0.6453 |
| MHU proxy | ruta entrenada | 0.5493 | 0.6834 |
| Retícula | ruta entrenada | 0.5553 | 0.6849 |

**Diferencias pareadas** (intervalos bootstrap **descriptivos**, remuestreando solo los 16 IDs de campos sintéticos; geometrías tratadas como sensibilidad fija, sin inferencia poblacional externa ni ajuste de multiplicidad):

| Comparación (primer método − segundo) | Media | IC95 descriptivo | Condiciones favorables al primero |
|---|---:|---:|---:|
| mhu_type minus cvt_type | +0.0662 | [+0.0613, +0.0718] | 0/20 |
| mhu_learned minus cvt_learned | +0.0177 | [+0.0078, +0.0273] | 1/20 |
| mhu_learned minus mhu_type | +0.2620 | [+0.2438, +0.2820] | 4/20 |
| mhu_type minus mhu_knn | -0.0393 | [-0.0491, -0.0304] | 10/20 |
| cvt_type minus cvt_knn | -0.0149 | [-0.0195, -0.0108] | 12/20 |

**Los mejores por celda:** CVT por tipos 10/20, CVT kNN 5/20, CVT trained routing 3/20, MHU proxy kNN 2/20. La ventaja funcional es de CVT en los escenarios de reconstrucción estudiados, no de los bajos valores de energía Fourier por sí solos. En señales correlacionadas, algunos métodos aprendidos sí son competitivos; no justificar reclasificación positiva general.

## Resultados por condición

| Ciclo | Campo | Perturbación | CVT tipo | MHU tipo | CVT aprendida | MHU aprendida |
|---|---|---|---:|---:|---:|---:|
| L01 | low | clean | 0.122 | 0.192 | 0.776 | 0.798 |
| L02 | low | drop20 | 0.262 | 0.331 | 0.841 | 0.847 |
| L03 | low | rare_drop40 | 0.199 | 0.249 | 0.808 | 0.810 |
| L04 | low | noise15 | 0.147 | 0.212 | 0.784 | 0.802 |
| L05 | high | clean | 0.544 | 0.725 | 0.931 | 0.966 |
| L06 | high | drop20 | 0.653 | 0.777 | 0.965 | 0.984 |
| L07 | high | rare_drop40 | 0.564 | 0.732 | 0.932 | 0.967 |
| L08 | high | noise15 | 0.557 | 0.734 | 0.932 | 0.969 |
| L09 | correlated | clean | 0.018 | 0.027 | 0.021 | 0.029 |
| L10 | correlated | drop20 | 0.077 | 0.083 | 0.068 | 0.050 |
| L11 | correlated | rare_drop40 | 0.031 | 0.036 | 0.023 | 0.032 |
| L12 | correlated | noise15 | 0.023 | 0.033 | 0.026 | 0.036 |
| L13 | anticorrelated | clean | 0.058 | 0.065 | 0.057 | 0.071 |
| L14 | anticorrelated | drop20 | 0.110 | 0.120 | 0.100 | 0.103 |
| L15 | anticorrelated | rare_drop40 | 0.074 | 0.079 | 0.063 | 0.076 |
| L16 | anticorrelated | noise15 | 0.064 | 0.070 | 0.062 | 0.077 |
| L17 | localized | clean | 0.173 | 0.271 | 0.795 | 0.832 |
| L18 | localized | drop20 | 0.317 | 0.396 | 0.841 | 0.866 |
| L19 | localized | rare_drop40 | 0.236 | 0.326 | 0.805 | 0.832 |
| L20 | localized | noise15 | 0.193 | 0.288 | 0.802 | 0.837 |

## Diagnóstico de mecanismos

| Método | Longitud media arista | Cobertura media de modalidades (incluido nodo propio) |
|---|---:|---:|
| cvt_knn | 0.054 | 0.909 |
| cvt_learned | 0.176 | 0.843 |
| cvt_type | 0.055 | 1.000 |
| grid_knn | 0.057 | 0.729 |
| grid_learned | 0.181 | 0.769 |
| grid_type | 0.065 | 1.000 |
| mhu_knn | 0.055 | 0.752 |
| mhu_learned | 0.180 | 0.779 |
| mhu_type | 0.062 | 1.000 |

La geometría CVT kNN obtiene cobertura de tipos ~0,909 con aristas cortas (~0,054), mientras que MHU proxy kNN ~0,752. Los métodos tipo forzado alcanzan 1,00 por construcción, pero la conexión aprendida utiliza información de TRAIN y aun así prefiere enlaces mucho más largos (~0,18). El enrutamiento aprendido no es un rival de *graph attention* moderno; sobreajuste y desajuste espacial son hipótesis explicativas, NO mecanismos causalmente identificados.

## Datos, validez y reproducibilidad

Los datos TRAIN/VAL/TEST utilizan semillas disjuntas, pero todos son del **mismo proceso sintético**. Comparaciones entre geometrías reutilizan semillas generadoras y el target se normaliza sobre los 400 nodos de cada geometría, por lo que no constituye la misma realización exacta sobre observaciones idénticas. Los supervisores entrenan **solo clean** y todos enfrentan las cuatro perturbaciones en TEST. El router aprendido accede a **targets TRAIN** además del diseño fijo y requiere cómputo adicional de selección de aristas: paridad de parámetros y número de edges no implica paridad de coste integral. No se comparó la implementación original Wei2010, ni un expansor espectral certificado, ni atención aprendida end-to-end.

La segunda corrida de las mismas 10 celdas confirma determinismo local. **CLEAN_CLONE_NOT_VERIFIED; EXTERNAL_REPLICATION_NOT_DONE; NATIVE_400_BENCHMARK_BLOCKED.** El ZIP contiene JSON sin modificar, código, certificados Git previos, informes y auditorías. Todo cambio de historial queda por commits inmutables.

## Evidencia pública y límites de originalidad

Wei, 2010, *Multi-Class Blue Noise Sampling*: https://www.liyiwei.org/papers/noise-sig10/ (modelo multiclase publicado). Attali et al., 2026, *Graph Rewiring in GNNs to Mitigate Over-Squashing and Over-Smoothing*, IJCAI-26: https://doi.org/10.24963/ijcai.2026/861 (antecedentes para métodos de enrutamiento/rewiring). Micheli & Tortorella, 2025, *An empirical evaluation of rewiring approaches in graph neural networks*, https://doi.org/10.1016/j.patrec.2025.05.021 (evidencia general de que rewiring no siempre mejora bajo condiciones equiparadas). Son antecedentes, NO resultados de ejecución de esos rivales en esta campaña.

## Gobernanza y decisión final

**20/20 condiciones AB-R de esta autorización ejecutadas y auditadas**, pero no 20 experimentos independientes ni hallazgos originales; 1 proceso inicial incompleto archivado. CT2 línea matemática previa 24/100; línea actual *functional trained proxy* 18/100 valoración ordinal interna, no probabilidad, por adversario CVT, rutas supervisadas débiles y ausencia de nativos. R5 STOP_LOCAL; no consumir más semillas de mismo generador. Mantener `main` sin modificar; la rama contiene informe/ledger/prereg/scripts y resultados. No solicitar autorización intermedia. Próxima necesidad: bytes NPZ de nativos y prueba con CAVE / datos multiespectrales con licencia, learned dynamic attention + CVT + Wei bajo coste igualado.
