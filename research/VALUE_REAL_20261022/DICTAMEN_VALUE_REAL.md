# LARP — valor práctico en muestreo multicanal con pocos datos piloto

**Fecha:** 2026-10-22. **Tipo:** exploración post hoc sobre escenas reales 2D; NO confirmación externa ni descubrimiento 2/3. **Repositorio objetivo:** `GalexY3/proyecto-LARP`, rama `research/ab4-cosi-branch30-20261022`. **Separación:** se conserva el AB30 sintético anterior y no se modifica Scale3D original ni sus experimentos.

## Pregunta y estimando

**Pregunta:** ¿puede una aproximación COSI superar disposiciones geométricas sencillas para estimar la media global de un campo espacial multicanal, especialmente cuando existe una muestra piloto limitada?

Estimando observado: RMSE de la **media ponderada de tres canales RGB** sobre parches 24×24 píxeles, usando **24 lecturas puntuales** en posiciones fijas, distribuidas por tipos (R/G/B). Pesos (0.2126, 0.7152, 0.0722), utilizados como **índice ponderado de canales en coordenadas RGB tal cual**; no corresponde estrictamente a luminancia fotométrica, porque no se linealizaron los valores sRGB.

Los datos proceden de `scikit-image` (`astronaut`, `coffee`, `chelsea`, `immunohistochemistry`: diseño; `rocket`, `hubble_deep_field`: transferencia entre escenas). De las primeras cuatro escenas se tomaron 1.800 parches de entrenamiento y 600 parches nuevos para prueba interna; cada escena de transferencia aporta 800 parches. Los parches dentro de cada imagen se solapan y **no son replicaciones independientes**; los dos orígenes de transferencia son dos únicas unidades de generalización al nivel de imagen. No se realizaron observaciones 3D, mediciones ambientales, comprobación en cámaras físicas ni reconstrucción 3D.

**Advertencia esencial:** los ensayos de presupuesto pequeño, cuota variable y diseño directo se planificaron progresivamente tras observar resultados anteriores. Incluso los resultados de escenas reservadas están expuestos a selección post hoc. Considerarlos evidencia exploratoria y no confirmación independiente, aunque los diseños individuales no utilizaron los píxeles de las escenas reservadas durante su optimización.

## Procedimiento

- Tipos naturales: R/G/B, tres funciones de medida originales, no cinco roles Scale3D. Cada lectura mide un único canal en una coordenada espacial. Una posición puede coincidir entre canales, porque se permiten lecturas de diferentes tipos en el mismo lugar; **no** se implementó una matriz física de filtros Bayer con exclusión intercanal.
- COSI en 2D nativo: estimar la matriz de covarianza *compleja* entre coeficientes Fourier de los tres canales en 40 modos no nulos, y minimizar la forma cuadrática espectral con regularización de separación local por tipo. Coordenadas optimizadas con L-BFGS-B y ajustadas a centros de píxel.
- Controles: aleatorio, estratificado, farthest-point sampling (FPS), Sobol, MHU-espectral-proxy (regularización isotrópica), POWER-DIAG (potencia por canal/frecuencia sin covarianza cruzada), COSI-FULL y COSI-SHRINK (50% covarianza cruzada; 50% diagonal), diseño empírico directo con barrido de swaps minimizando RMSE de la muestra de entrenamiento.
- Mismo dataset y cantidad de lecturas para las comparaciones relevantes; tiempo de construcción no pareado (registrado). El diseño empírico ve el objetivo de entrenamiento directamente; COSI ve covarianzas Fourier. No existe comparación con el muestreador original de Wei ni con GP/A-optimal design profesional implementado y ajustado: **ausencia de baseline del estado del arte**.
- 7 inicializaciones por método en el ensayo principal; en estudio de escasez, 5 pilotos × 3 inicializaciones, con tamaños efectivos 12, 28, 88, 300 y 1.800. Gradiente analítico de COSI verificado con diferencias finitas.

## Resultados: 24 lecturas, cuota fija [8,8,8]

| Método | RMSE rocket | RMSE hubble |
|---|---:|---:|
| IID | 0.016154 | 0.023893 |
| Estratificado | 0.012574 | 0.019192 |
| Sobol | 0.011687 | 0.016866 |
| MHU-espectral proxy | 0.011607 | 0.017575 |
| POWER-DIAG | 0.010753 | 0.015527 |
| COSI-SHRINK | 0.010594 | 0.014956 |
| Empírico directo | 0.011342 | 0.013785 |

En el promedio descriptivo de estas dos escenas, el diseño de espectro condicionado mejora sobre Sobol, MHU-proxy e IID. Sin embargo, la ablación diagonal casi iguala COSI: la correlación cruzada aporta una ganancia incremental modesta, no todo el efecto. El método empírico directo es mejor en una escena, demostrando que no hay dominancia general.

## Resultados: decisión sobre cuotas de tipos a presupuesto fijo

Se exploraron ocho cuotas con 24 lecturas totales. Entre las exploradas, [6,16,2] produjo la menor media en los datos vistos, tanto en Sobol como en COSI-SHRINK. **No es un óptimo universal ni una selección confirmatoria**. La selección con resultados de test invalida usar ese mismo test como confirmación posterior.

| Diseño con 24 lecturas | Rocket | Hubble | Promedio descriptivo |
|---|---:|---:|---:|
| COSI-SHRINK, [8,8,8] | 0.010637 | 0.015010 | 0.012824 |
| Sobol, [6,16,2] | 0.008505 | 0.012283 | 0.010394 |
| POWER-DIAG, [6,16,2] | 0.008613 | 0.011511 | 0.010062 |
| **COSI-SHRINK, [6,16,2]** | **0.008091** | **0.010451** | **0.009271** |
| **EMPÍRICO DIRECTO, [6,16,2]** | **0.007830** | **0.009210** | **0.008520** |

En el selector empírico **con el mismo presupuesto y la misma cuota**, COSI PIERDE con muchos datos de entrenamiento. No ocultarlo. La optimización directa usa unas 0,5 s por disposición en estos scripts, frente a aproximadamente 0,01 s de optimización espectral, pero esta razón es una medida particular del código/hardware, NO una comparación de complejidad ni de ejecutables optimizados profesionalmente.

La cuota [6,16,2] es consistente con ponderar fuertemente verde en el índice elegido: el resultado favorable está parcialmente inducido por el estimando. No extrapolarlo a canales físico-químicos de igual relevancia, a cámaras de color reales o a identificación de detalles cromáticos.

## Resultados: escasez de datos piloto, cuota fija [6,16,2]

RMSE promediado descriptivamente entre las dos escenas externas. Cada método utiliza exactamente los mismos parches de piloto de su condición. Variación de semillas: 5 pilotos × 3 disposiciones.

| n piloto | COSI-SHRINK | POWER-DIAG | Sobol | Directo |
|---|---:|---:|---:|---:|
| 12 | **0.009156** | 0.009821 | 0.010301 | 0.011765 |
| 28 | **0.009336** | 0.009765 | 0.010301 | 0.011160 |
| 88 | **0.009170** | 0.009462 | 0.010301 | 0.009804 |
| 300 | **0.009173** | 0.009521 | 0.010301 | 0.009319 |
| 1.800 | 0.009245 | 0.009262 | 0.010301 | **0.008872** |

La optimización directa de posiciones con muestras muy pequeñas presenta error de **entrenamiento** mucho menor, por ejemplo 0.000883 a n=12, pero generaliza peor a las escenas distintas. Este es un ejemplo computacional de sobreajuste, no evidencia causal general. Con 1.800 datos, el rival directo pasa a ser más preciso.

## Aportación potencial y oportunidad práctica

[Inferencia] El nicho inmediato es **diseño de campañas de medición multicanal de un agregado espacial** cuando hay una muestra piloto pequeña y costes por medida limitados. COSI funciona como regularizador informacional: sacrifica ajuste directo a muestras particulares y aprovecha covarianzas Fourier y separación espacial. Podría servir en adquisición selectiva de imágenes, muestreo remoto o despliegues de campo con mediciones de distintos tipos, pero *NINGUNO de estos casos industriales ha sido probado*.

Un prototipo aplicable sería una herramienta que, a partir de históricos 2D o 3D por canal y un presupuesto de lecturas, proponga **cuotas, posiciones y estimación de incertidumbre**, comparando con Sobol/estratificado y diseño GP/empírico. Sin datos piloto para algunos canales, un modelo isotrópico podría ser preferible. La tasa de fallo de sensores, el coste de lectura por tipo y la accesibilidad física serían restricciones opcionales, todavía sin resultados empíricos.

**Originalidad:** no demostrada. COSI corresponde a diseño espectral dependiente de covarianza/kernels matriciales, y asignación óptima de sensores por información tiene amplia literatura. La mejora numérica es un candidato a eficiencia de ingeniería, no algoritmo original 2/3 ni capacidad neuronal 3/3.

## Prior art y falsadores

- Krause, Singh y Guestrin (2008), *Near-Optimal Sensor Placements in Gaussian Processes*, JMLR 9:235–284: https://jmlr.csail.mit.edu/papers/v9/krause08a.html (incluye robustez a fallo e incertidumbre).
- Li-Yi Wei (2010), *Multi-Class Blue Noise Sampling*, SIGGRAPH: https://www.liyiwei.org/papers/noise-sig10/.
- Krause et al. (2011), *Robust Sensor Placements at Informative and Communication-efficient Locations*: https://doi.org/10.1145/1921621.1921625.
- Uciński (2025), *A-optimal sensor location subject to correlated observations via a fast exchange algorithm*: https://doi.org/10.1016/j.measurement.2025.117794.

**Falsadores próximos:** replicar en datos físicos multi-rol (no RGB únicamente); comparar con A-optimal/KP/GP igualmente informadas; medir error, calibración, coste por sensor, tiempo total de optimización, repetibilidad entre entornos; hacer preregistro y seleccionar cuotas solo con train/val antes de abrir un tercer entorno totalmente nuevo. Si el baseline clásico empata o gana, valorar COSI solo como simplificación de ingeniería, no como descubrimiento.

## Decisión AB 3.2.1

**CONTINUE_CONDICIONAL HACIA UN PROTOTIPO DE DISEÑO DE MUESTREO DE BAJOS DATOS**, pero **STOP** a reivindicar MHU/COSI como superiores en general. Abrir la siguiente fase solo con datasets externos y un comparador GP o cuadratura con kernel de igual información. El método AB permanece 3.2.1: este registro no demuestra eficacia de la metodología.
