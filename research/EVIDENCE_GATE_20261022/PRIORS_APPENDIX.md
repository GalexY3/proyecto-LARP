# Priors LARP — apéndice E-GATE, 22-10-2026

Nuevas entradas sustantivas, **no** priors normativos ni posteriores bayesianos cuantificados. Preservar el ledger acumulado.

| ID | Proposición | Evidencia favorable | Evidencia adversa | Procedencia y límite | Estado |
|---|---|---|---|---|---|
| EG-R01 | COSI logra menor error que POWER_DIAG con Ridge en nuevos tipos de escenas monocromas. | 4/4 escenas reservadas, macro RMSE 0.012409 vs 0.013268 (−6.47%). | n=4 escenas; los roles derivan de un solo campo; sólo una familia de tarea artificial. | `bench.py`, `HOLDOUT_FREEZE.json`, `SUMMARY.json`, 6 diseños con datos piloto independientes dentro de 2 escenas de entrenamiento. | APOYO EXPLORATORIO LIMITADO |
| EG-R02 | COSI proporciona mejora de cuadratura frente a POWER_DIAG sin readout. | Evidencia anterior sobre RGB en otras escenas. | Nuevo gate: RMSE promedio fijo 0.016821 COSI vs 0.016716 POWER_DIAG y 0.016818 Sobol. | Transferencia monocroma de filtros; no superioridad sistemática. | DEBILITADA |
| EG-R03 | La supresión de covarianzas cruzadas entre tipos es el mecanismo causal único de utilidad. | Algunas ganancias COSI frente POWER_DIAG con Ridge. | No se ha aislado la mediación: varios términos geométricos, misma regularización/operador y efecto del readout. | Modelo matemático reducible a kernel objetivo adaptado, literatura previa. | NO_IDENTIFICADO |
| EG-R04 | Selección gaussiana es inferior en general a COSI. | GP aproximado muestra peor RMSE en este gate. | Comparador no reproduce algoritmos publicados; reparación ex post con candidatos totales también desfavorable, sin tuning robusto. | `repair_gp.py`, `GP_ALL_POSTHOC.json`. | NO_VALIDADO |
| EG-R05 | El objetivo prioritario práctico puede estudiarse sobre redes ambientales reales ya obtenidas. | Fuente oficial UCI verificada como multisitio y multivariable. | Los bytes y las coordenadas originales no son accesibles aquí; no hay experimento. | `SOURCE_ACQUISITION_GATE.md`. | BARRERA_DE_EJECUCIÓN |

**Decisión:** STOP de series sintéticas y de imagen sin una fuente externa adicional; FOCUS pendiente en datos espaciales nativos 3D/2D con distintas variables físicas y baseline GP entrenado pareado. No se acredita originalidad 2/3 o utilidad neuronal 3/3.
