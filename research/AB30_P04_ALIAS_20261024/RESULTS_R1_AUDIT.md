# LARP AB30 P04 — resultado R1 (24 octubre 2026)

Origen: AB55 BugsInPy P04, DRIFT D3.7. Se autorizaron 30 A–J. **30 contrastes sintéticos ejecutados** (5 bloques x 6 programas, 6 seeds pareadas por ciclo = 180 observaciones). Los defectos son inyectados artificialmente sobre sum, min, max, mean, range y unique; **ningún bug real de BugsInPy ha sido reproducido**. No son 30 hipótesis científicas independientes.

## Branching genuino entre bloques

- B01 C01-C06: INPUT→CONDITIONAL, mixed; alias-break=0.2274369; DEDUP−GREEDY=+0.107639; decidió B02 régimen 1.
- B02 C07-C12: OUTPUT→INPUT, mixed; alias-break=0.5703457; DEDUP−GREEDY=+0.079861; decidió B03 régimen 4.
- B03 C13-C18: CONDITIONAL→INPUT, mixed; alias-break=0.4491428; DEDUP−GREEDY=+0.250000; decidió B04 régimen 2.
- B04 C19-C24: CONDITIONAL→OUTPUT, nonnegative; alias-break=0.2645202; DEDUP−GREEDY=+0.333333; decidió B05 régimen 3.
- B05 C25-C30: INPUT→OUTPUT, nonnegative; alias-break=0.0303682; DEDUP−GREEDY=+0.041667; cuota cerrada.
La elección tras cada bloque siguió la regla preregistrada en PREREG_SOURCE_LOCK.md. Cada ciclo individual está A–J en JSON archivado, sin atribuir cinco cambios de rama a 30 hipótesis nuevas.

## Igualdad de presupuesto y resultados

Los cuatro procedimientos reciben idéntica matriz TRAIN de 8 defectos conocidos; seleccionan exactamente cuatro relaciones metamórficas del mismo catálogo de 14; evalúan 8 mutaciones no vistas de otra familia, 16 fuentes por MR, 6 seeds/ciclo. Se midieron (fracciones de los fallos inyectados detectados en holdout):
- GREEDY simple con desempate por índice: **0.683333**
- RANDOM: **0.816667**
- GREEDY + diversidad: **0.820139**
- DEDUP de firmas TRAIN + greedy: **0.845833**

DEDUP supera GREEDY simple +0.162500, pero este baseline sobreajusta empates y no es competente por sí solo. Frente a GREEDY+DIVERSITY la diferencia baja a +0.025694, con 7 de 30 celdas favorables, 3 negativas y 20 empatadas. Heterogeneidad por programa de DEDUP−DIVERSITY: sum 0, min +0.125, max +0.100, mean +0.125, range −0.100, unique −0.095833. Cualquier reivindicación universal queda desautorizada.

## Instrumentación y reparación

**V0 INVALIDADA para paridad:** 18 de 180 repeticiones DEDUP no llenaban las cuatro plazas. Fuente V0 SHA256 3324c4978699454fec6f5d69fb5e5ba952e897bf7895f5819f5ef38549d0bf7b; raw V0 SHA256 ad62e41ac472332427d7a44bc8b4a9df3b9e19cdab6f83d45dd881acc11ee700. R1 preregistrado después de observar V0 en REPAIR_R1_PRE_REPLAY.md, commit d8599cc; source local R1 SHA256 f78e5e07e3e0a68878d7cdb82b0328a01fa1ba010790cf30655afed28f84e9cf. Replay **POST-EXPOSURE exploratorio**, sin pretender holdout nuevo. Raw R1 SHA256 9149cfcad4d8a91118974381b56a1f0608bc5d1919f2a2feff444ad20c362583. 180/180 cuotas exactas, 0 falsos positivos de MR sobre funciones correctas, familia TRAIN y HOLDOUT disjuntas, ejecución idéntica bit a bit en el mismo entorno.

**Limitación documental O3:** fuente completa y raw por semilla del motor Python aún no están en GitHub; solo sus hashes congelados/remotos y esta síntesis. El ZIP de la conversación **LARP_AB30_P04_20261024.zip** (18 ficheros, SHA256 42d101be7080e0837978ea4792394bf9430c365666ecfc51b16d54b6cb50808e) es el archivo íntegro; debe backfillearse y probarse clon limpio antes de integrar. No afirmar reproducibilidad externa.

## CT2 y grados

Línea previa AB55 (reproducción dinámica de defectos históricos): 11→8/100. Rama P04 independiente: **12→10/100** en B01 tras evaluar antecedentes; B02–B05 10 constante. Las series no deben unirse como progreso continuo: pivot D3.7. CT2 es juicio ordinal y no probabilidad. Inventario histórico conservado: 6 N1 auditados; esta campaña **N1 nuevo=0, N2=0, N3=0**. No se modifica el ledger central.

Antecedentes fuertes: test-suite reduction, mutant subsumption, MR composition y riesgo de fallo real fuera de mutaciones. DOI 10.1002/smr.2656, 10.1109/ACCESS.2023.3289073, 10.1145/3213846.3213875, 10.1109/TSE.2020.3009698. No hay validación científica 2/3.

AB-DECIDE: CLOSE_QUOTA_30, STOP_LOCAL a reivindicación sintética, pivot a reproducción histórica con paridad buggy/fixed, tests diseñados sin conocer fix y controles profesionales bajo coste comparable. Si prosigue, ruta de 20 ciclos con evidencia real distinta. SOLICITO PIVOT 20 CICLOS.
