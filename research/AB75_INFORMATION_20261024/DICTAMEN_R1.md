# AB75 — Dictamen R1 corregido, 24 octubre 2026

**Estado:** 30+45 ciclos AB A–J ejecutados, 14 bloques y seis fuentes Statsmodels históricas. Primera tanda 30 sin descubrimiento 2/3, activó otros 45. **CT2 inicial 12/100; final 10/100 (ordinal no probabilístico). N1 nuevo provisional=1, N2=0, N3=0.** Los tres hallazgos 1/3 anteriores siguen conservados en main y uno nuevo, TEMPO-COST-04, se añade allí con evidencia adversarial.

## RESULTADOS REPARADOS: 75 CICLOS (dos series Monte Carlo por ciclo)

| Bloque | Nº ciclos | E signo ΔMSE favorable A | G signo ΔMSE favorable A | CT2 al cierre |
|---|---:|---:|---:|---:|
| B01 | 6 | 6 | 6 | 11/100 |
| B02 | 6 | 0 | 0 | 10/100 |
| B03 | 6 | 2 | 1 | 10/100 |
| B04 | 6 | 6 | 6 | 12/100 |
| B05 | 6 | 1 | 1 | 9/100 |
| B06 | 5 | 5 | 5 | 9/100 |
| B07 | 5 | 1 | 2 | 9/100 |
| B08 | 5 | 1 | 1 | 8/100 |
| B09 | 5 | 1 | 2 | 7/100 |
| B10 | 5 | 5 | 5 | 13/100 |
| B11 | 5 | 0 | 0 | 11/100 |
| B12 | 5 | 2 | 2 | 11/100 |
| B13 | 5 | 2 | 4 | 10/100 |
| B14 | 5 | 5 | 5 | 10/100 |

- B01/B02: corregir el sesgo bajo adquisición adaptativa no asegura menor MSE; el promedio ingenuo puede superar al estimador condicional en varianza total, teoría conocida de bias–variance.
- B03: asignación por varianza piloto no domina al reparto proporcional.
- B04: shrinkage estabiliza el piloto frente a variancias crudas en 6/6 fuentes, pero B05 demuestra que falla frente a una única fase con presupuesto completo en 5/6.
- B06: control de asignación proporcional fija; B07–B09: variaciones de decisiones piloto, sin ganancia universal.
- B10: cambio ARTIFICIAL de etiquetas después del piloto produce mayor sesgo absoluto si conservamos sus observaciones antiguas en 5/5 fuentes E y 4/5 G, pero menor MSE en 5/5 E/G. B11: volver a medir 6 etiquetas pagando su coste empeora el MSE en 5/5 E/G.
- B12: IPW con MAR x-conocido mejora MSE 2/5 E/G; B13: propensión MNAR oráculo basada en y no observado reduce sesgo pero NO es aplicable en el mundo real; B14: reversión artificial completa post-piloto.
- **1/3 único nuevo LARP-1-004:** temporalidad válida de etiqueta y coste de refresco, ilustración operativa, no nueva teoría. N1 explícito en el inventario permanente=4 incluyendo tres anteriores; otros históricos anteriores a O4 no auditados.

## ERROR Y REPARACIÓN (no ocultar)
Las 150 ejecuciones originales E/G tenían una **fuga de información del y poblacional** por utilizar sus cuantiles, media y SD para transformar las etiquetas *antes* de asignar la segunda muestra. Los 75 ciclos de aquella versión se preservan **INVALIDADOS**. La reparación R1 cambió el estimando explícitamente a una transformación asinh con constantes fijas por fuente que no consulta momentos y completos en tiempo de ejecución. Sus hashes se comprometieron en [REPAIR_R1_NO_FULL_Y_PREPROCESSING](prereg/REPAIR_R1_NO_FULL_Y_PREPROCESSING.md) antes de realizar las 75 repeticiones. R1 es post-exposición y **solo exploratoria**, no confirmación ciega, y los datos originales no son 75 ciclos adicionales válidos.

Fuente v3 SHA `949a9e4497fce1818633674fbc8d289cf6acb2622daa2a59afd9115683162f96` y v4 SHA `1f82bd3b43853e8b7484f543e2aad86d947d398b6fb00e71e370a90be76a20ab`. El instrumento prueba invarianza de decisiones al sustituir y no observado, igualdad de presupuestos, sin duplicar etiquetas y comprobación de promedio condicional por Monte Carlo.

## Estado de los brutos y replicación
El ZIP de conversación `LARP_AB75_20261024_COMPLETO.zip` contiene **426 ficheros**, incluido `MANIFEST.json` SHA256, 150 resultados R1 E/G por adquisición, 150 resultados v1/v2 inválidos, los cuatro motores completos, 75 contratos, ledger A–J de 183KB, lecturas por bloque y gráfico CT2; SHA256 del ZIP `04ce6a444c07f2cf27f83c9a67a5b852330cf985190dfeb285b27b2db68e6d1b`. GitHub guarda source SHA y preregs previos, esta síntesis y dictamen, pero raw completo aún está fuera de GitHub; **no fusionar hasta backfill exacto y prueba de clon limpio**.

Seis datasets son paquetes históricos, no nuevas poblaciones de validación. E y G usan trayectorias aleatorias nuevas y presupuestos 30 y 48 sobre las mismas filas; no representan replicación externa. Los cambios de etiquetas y faltantes son artificiales. La literatura de diseño adaptativo e IPW antecede a los principios. **Ningún 2/3 ni 3/3 acreditado.**

**AB-DECIDE:** CLOSE_75, DRIFT hacia fuente prospectiva con etiquetas realmente demoradas y precios observados. **SOLICITO BRANCHING 30 CICLOS** para la próxima campaña bajo hipótesis verdaderamente nueva.
