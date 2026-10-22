# LARP — BR30, experimento adaptativo de 30 ciclos sobre COSI, MHU y Local SI

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
| MHU-monotone | 0.07345 | 0.07471 | 0.07490 |
| COSI-monotone | 0.06104 | 0.06835 | 0.06285 |
| COSI-shrink-monotone | 0.06042 | 0.06561 | 0.06195 |
| Oracle-monotone | 0.05679 | 0.06466 | 0.05878 |

La reducción media fuente de `COSI-shrink-monotone` respecto a `MHU-monotone` es **~17,7 %** en RMSE (cálculo descriptivo sobre 30 condiciones adaptativamente elegidas). COSI-shrink vence en la comparación pareada de fuente en 30/30 y de covarianza desplazada en 29/30; la igualdad de información y tiempo de preparación con un método clásico de kernel quadrature adaptado NO está acreditada. El oráculo es una referencia informacional inalcanzable para los métodos realistas: no presentarlo como baseline justo. Ni estos 30 ciclos ni la reparación tienen datasets 3D reales, GNN/Transformer entrenadas o un muestreador multiclase Wei verificado.

La observación `COSI > MHU` se explica de forma suficiente, como mínimo, porque COSI utiliza una estimación de la estructura verdadera de la tarea y MHU no. No podemos identificar una aportación geométrica diferencial, pues COSI comparte el objetivo funcional de selección de muestras de cuadratura con kernels. La respuesta a la pregunta de originalidad sigue siendo **NO_ACREDITADO_2/3**, **NO_ACREDITADO_3/3**.

## Historial de los 30 ciclos (tal como se ejecutó el primer solver)

| Ciclo | Familia elegida por estado previo | Ganador original | Δ RMSE compuesto COSI-shrink − MHU | Interpretación / precaución |
|---|---|---|---:|---|
| C01 | Precisión de pilotos | COSI-shrink | -0.01253 | COSI mejor en proxy original |
| C02 | Correlación entre tipos | COSI-shrink | -0.00505 | COSI mejor en proxy original |
| C03 | Desplazamiento espectral | COSI-shrink | -0.01447 | COSI mejor en proxy original |
| C04 | Fallo regional | COSI-shrink | -0.01213 | COSI mejor en proxy original |
| C05 | Heterogeneidad de roles | COSI-pilot | -0.01208 | COSI mejor en proxy original |
| C06 | Regularización | COSI-pilot | -0.01252 | COSI mejor en proxy original |
| C07 | Correlación entre tipos | COSI-shrink | -0.00711 | COSI mejor en proxy original |
| C08 | Regularización | COSI-shrink | -0.01128 | COSI mejor en proxy original |
| C09 | Heterogeneidad de roles | COSI-pilot | -0.01086 | COSI mejor en proxy original |
| C10 | Precisión de pilotos | COSI-shrink | -0.01333 | COSI mejor en proxy original |
| C11 | Desplazamiento espectral | COSI-shrink | -0.01384 | COSI mejor en proxy original |
| C12 | Fallo regional | COSI-shrink | -0.01250 | COSI mejor en proxy original |
| C13 | Correlación entre tipos | COSI-shrink | -0.00855 | COSI mejor en proxy original |
| C14 | Regularización | COSI-pilot | -0.01526 | COSI mejor en proxy original |
| C15 | Heterogeneidad de roles | COSI-shrink | -0.01346 | COSI mejor en proxy original |
| C16 | Precisión de pilotos | COSI-shrink | -0.01273 | COSI mejor en proxy original |
| C17 | Desplazamiento espectral | COSI-shrink | -0.00998 | COSI mejor en proxy original |
| C18 | Fallo regional | COSI-shrink | -0.01317 | COSI mejor en proxy original |
| C19 | Correlación entre tipos | COSI-shrink | -0.01805 | COSI mejor en proxy original |
| C20 | Regularización | COSI-pilot | -0.01203 | COSI mejor en proxy original |
| C21 | Heterogeneidad de roles | COSI-shrink | -0.00263 | COSI mejor en proxy original |
| C22 | Precisión de pilotos | COSI-shrink | -0.01266 | COSI mejor en proxy original |
| C23 | Desplazamiento espectral | COSI-shrink | -0.01374 | COSI mejor en proxy original |
| C24 | Fallo regional | COSI-shrink | -0.01424 | COSI mejor en proxy original |
| C25 | Correlación entre tipos | COSI-pilot | -0.03899 | COSI mejor en proxy original |
| C26 | Regularización | COSI-pilot | -0.00328 | COSI mejor en proxy original |
| C27 | Heterogeneidad de roles | MHU-proxy | +0.03067 | **ALERTA**: optimización inestable |
| C28 | Desplazamiento espectral | COSI-shrink | -0.00951 | COSI mejor en proxy original |
| C29 | Precisión de pilotos | COSI-pilot | -0.01611 | COSI mejor en proxy original |
| C30 | Fallo regional | COSI-shrink | -0.01402 | COSI mejor en proxy original |

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
