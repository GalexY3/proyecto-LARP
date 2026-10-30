# LARP — Dictamen AB-R N01–N20 sobre certificados NATIVOS N400

**Fecha:** 2026-10-30. Fuente: seis certificados originales N400 de LARP, tres semillas emparejadas 1101–1103, junto con sus resúmenes y auditoría histórica. **20 verificaciones A–J documentales completadas; NO son 20 experimentos independientes ni nuevas simulaciones**. Resultados históricos ya conocidos parcialmente antes del protocolo de esta campaña. No se puede inferir validación neuronal.

## Resultado cuantitativo fundamental

Potencia media del conjunto en seis modos de Fourier optimizados: **MHU 0.0000579301047** y **LOCAL 0.02659735552**. MHU reduce el objetivo un **99.78 %** de media; el signo es favorable en 3/3 semillas. Era parte del objetivo explícito del optimizador, no validación externa.

Fluctuaciones de conteos en ventanas de radio 5: MHU/LOCAL **0.6760**, reducción media **32.40 %**; en radio 0,5 la razón **1.0170**, ligeramente desfavorable a MHU. La ventaja del control espectral es dependiente de escala.

El máximo del espectro fuera de banda optimizada tiene razón MHU/LOCAL **1.1421** (desventaja MHU), mientras que en la media de la banda inmediatamente posterior al corte es **0.7154** (ventaja MHU). Son métricas diferentes; no cabe afirmar mejoría en todas las frecuencias.

La varianza del área de Voronoi MHU/LOCAL es **1.0177**, sin dominancia local inequívoca. Los p95 de distancia hasta cada tipo muestran ganancias pequeñas y heterogéneas.

## Auditoría de las veinte cuestiones

| ID | Cuestión | Evidencia primaria / razón MHU:LOCAL |
|---|---|---|
| N01 | Centro y configuración de conteos | same window-center hash, class counts, code identity |
| N02 | Identidad inicial | 3/3 paired initial and class-label hashes |
| N03 | Puertas de admisión | full 3/3 admitted; LOCAL 3/3 packed, 0/3 finite-certified |
| N04 | No asintótico | asymptotic proof false, anisotropy audits NOT_RUN |
| N05 | Baja frecuencia del conjunto | MHU 0.0000579301047, LOCAL 0.02659735552; ratio 0.002178040018; wins 3/3 |
| N06 | Baja frecuencia de especie A | MHU 0.001490792066, LOCAL 0.1107008549; ratio 0.01346685232; wins 3/3 |
| N07 | Baja frecuencia de especie B | MHU 0.001514667989, LOCAL 0.1546243868; ratio 0.009795789791; wins 3/3 |
| N08 | Baja frecuencia de especie C | MHU 0.000935387887, LOCAL 0.05901872373; ratio 0.01584900228; wins 3/3 |
| N09 | Baja frecuencia de especie D | MHU 0.003415196978, LOCAL 0.06378197664; ratio 0.05354485951; wins 3/3 |
| N10 | Baja frecuencia de especie E | MHU 0.001957848922, LOCAL 0.03601933177; ratio 0.05435550372; wins 3/3 |
| N11 | Modos no optimizados | A ratio 0.6888 (3/3), B ratio 1.2954 (1/3), C ratio 0.5954 (3/3), D ratio 0.9939 (2/3), E ratio 1.0336 (1/3), union ratio 1.1421 (1/3) |
| N12 | Rebote post-corte | A ratio 1.0160 (1/3), B ratio 0.5691 (3/3), C ratio 0.6740 (3/3), D ratio 1.1275 (1/3), E ratio 0.7820 (2/3), union ratio 0.7154 (3/3) |
| N13 | Ventana conteo R=0.5 | A ratio 1.0112 (0/3), B ratio 1.0095 (1/3), C ratio 0.9916 (2/3), D ratio 1.0286 (1/3), E ratio 0.9891 (2/3), union ratio 1.0170 (1/3) |
| N14 | Ventana conteo R=2 | A ratio 0.8186 (3/3), B ratio 0.7840 (3/3), C ratio 0.9275 (3/3), D ratio 0.9071 (3/3), E ratio 0.9360 (2/3), union ratio 0.9629 (3/3) |
| N15 | Ventana conteo R=4 | A ratio 0.4058 (3/3), B ratio 0.4321 (3/3), C ratio 0.6828 (3/3), D ratio 0.7088 (3/3), E ratio 0.8237 (3/3), union ratio 0.7554 (3/3) |
| N16 | Ventana conteo R=5 | A ratio 0.3245 (3/3), B ratio 0.3355 (3/3), C ratio 0.6248 (3/3), D ratio 0.6216 (3/3), E ratio 0.7216 (3/3), union ratio 0.6760 (3/3) |
| N17 | Vecinos de tipo próximo | A ratio 1.0012 (2/3), B ratio 0.9458 (3/3), C ratio 0.9780 (3/3), D ratio 0.9799 (2/3), E ratio 0.9866 (2/3) |
| N18 | Voronoi y orden angular | Voronoi 1.017661245; q6 0.9975354884 |
| N19 | Grafo nativo documental | all SCC=1, unequal port digests between treatments |
| N20 | Puerta de evidencia independiente | NPZ original not accessible; original Wei not run; independent 5-band data missing |

## A–J, calidad y controles adversariales

Cada ficha tiene pregunta A, rival LOCAL B, falsador y cálculo emparejado C, hashes de nueve archivos fuente y protocolo/code D, ejecución E, límites F, reproducción G, priors H, novedad I y AB-DECIDE J. El ledger completo está en LEDGER_N01_N20_AJ.json. La repetición exacta de los 20 resultados ocurrió en un segundo entorno de ejecución, no con geometrías independientes.

Los 10.000 centros empleados en la certificación original son evaluaciones correlacionadas de una misma geometría; no equivalen a 10.000 unidades independientes. Las tres semillas usan el mismo generador y la misma familia de datos. No hay demostración termodinámica MHU, y la auditoría adicional de anisotropía figura NOT_RUN. La diferencia en baja frecuencia era esperable por la función objetivo, no acredita mejor precisión, consumo o enrutamiento neuronal.

**Errata:** la primera versión del analizador tenía un error sintáctico y no produjo resultados. Fue registrada y corregida antes de la primera extracción completa. El código fuente corregido y su replay están en GitHub. No hay selección retrospectiva de las tres semillas en esta campaña, pero los originales eran conocidos.

## Decisión

**R5 STOP_LOCAL** en nuevos análisis de los mismos nueve JSON. **N1 nuevo=0, N2=N3=0**. CT2 previo de la rama funcional entrenada 18/100 y matemático condicionado 24/100, sin subida por número de auditorías. DRIFT D2 a documentación geométrica nativa.

**Bloqueo no resuelto:** los seis NPZ originales existen en GitHub, pero el conector rechaza bytes no UTF-8. No se ha ejecutado la geometría N400 original con una red entrenada, ni el código auténtico del método de Wei, ni sensores de cinco bandas ópticas originales. El archivo export_native_n400.py prepara una exportación privada con floats exactos y hashes para un ejecutor independiente; no se ha ejecutado todavía sobre los NPZ. Un resultado funcional requiere recuperar bytes, congelar nuevo código A–J y confrontar con rivales fuertes.

## Fuentes externas de contexto

Jiao et al. (2014), Physical Review E 89, 022721, DOI 10.1103/PhysRevE.89.022721; Li-Yi Wei (2010), Multi-Class Blue Noise Sampling, https://www.liyiwei.org/papers/noise-sig10/; Micheli y Tortorella (2025), Pattern Recognition Letters, DOI 10.1016/j.patrec.2025.05.021. Antecedentes, no resultados ejecutados aquí.
