# LARP — Priors acumulativos VAL-R01..R05 (apéndice exploratorio 2026-10-22)

Los siguientes registros NO sustituyen al ledger maestro ni son posteriores probabilísticos calibrados. **Fuente:** `research/VALUE_REAL_20261022/DICTAMEN_VALUE_REAL.md`, scripts y resultados. Estado post hoc y dos únicas escenas externas.

| ID | Proposición | Evidencia favorable | Adversa, incertidumbre | Falsador | Estado |
|---|---|---|---|---|---|
| VAL-R01 | Una penalización espectral condicionada puede mejorar la estimación de la media de campos RGB 2D con 24 lecturas | 7 diseños, COSI-SHRINK [8,8,8] supera Sobol/MHU/IID en dos escenas observadas | POWER-DIAG se acerca y directo gana en Hubble; no GP óptimo ni Wei; no medición 3D | GP/QMC y muestreo profesional con igual presupuesto e información | EMPIRICO_OBSERVACIONAL_EXPLORATORIO |
| VAL-R02 | Ventaja particular con pocos datos piloto y cuotas por rol fijadas | Con 12 o 28 parches piloto, COSI [6,16,2] supera al selector empírico entrenado directamente, en dos escenas externas | Solo dos escenas, cuota elegida post hoc, beneficios de regularización conocidos; heterogeneidad de imágenes | Distintas distribuciones físicas e intervalos a nivel escena, selección train/val | CONDICIONAL_NO_CONFIRMATORIO |
| VAL-R03 | Ajustar cuotas puede importar más que ajustes geométricos menores | [6,16,2] reduce RMSE mucho frente a [8,8,8] para índice dominado por G | Pesos del estimando inducen ese resultado; optimización de cuotas no nueva; elegido tras test | Metas físicas con pesos y costos variados, cuotas fijadas en validación | RESULTADO_CONDICIONADO |
| VAL-R04 | COSI vence incluso al diseño empírico con muchos datos | No | Directo [6,16,2] gana en ambas escenas con datos abundantes | Nuevas escenas y comparación competentes emparejadas | REFUTADO_EN_ENSAYO |
| VAL-R05 | COSI añade un principio neuronal o estadístico nuevo | Ninguna evidencia | Objetivo equivalente a discrepancia por kernel; no red neuronal; literatura de GP y muestreo multiclase | Novedad matemática y ventajas con información/costo igual | NO_VALIDADO |
