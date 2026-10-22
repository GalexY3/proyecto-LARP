# Priors nuevos LARP — drift AB30, 23-10-2026

APÉNDICE acumulativo. No elimina ni corrige silenciosamente los priors anteriores. Todos los resultados son exploratorios; no hay posteriors numéricas inventadas ni evidencia 2/3.

## DRIFT-P01 — Dependencia relevante para la selección
**Claim:** seleccionar observaciones con matriz de correlación completa puede superar tratarlas como independientes. **Procedencia:** T01/T12/T13/T17, bloques B01–B03. **A favor:** T13 nominal−diagonal -0.03676, IC95 [-0.05898,-0.01454]; T12 diagonal−nominal +0.07949, IC95 [0.00957,0.14941]. **Contra:** T01/T17 no establecen mejora concluyente en todos los escenarios, diseño Gaussiano artificial. **Estado:** SINTÉTICO; principio conocido en diseño de experimentos. **Falsador:** nuevos sistemas y decoder no lineal sin valor adicional de covariance-aware design.

## DRIFT-P02 — Robustez no se obtiene automáticamente por minimax/CVaR
**Procedencia:** T02–T04, T07–T11, T14–T16. **A favor:** los métodos robustos no baten establemente al nominal y algunas diferencias están a favor del competidor simple. **Contra:** escenarios artificiales y familia de incertidumbre deliberadamente incompleta, algunos promedios favorecen CVaR/shrinkage. **Estado:** SINTÉTICO, extrapolación prohibida. **Falsador:** escenarios calibrados con dato externo donde los métodos robustos venzan de forma reproducible.

## DRIFT-P03 — Modelo completo como baseline crítico
**Procedencia:** T20,T23,T26,T29. **A favor:** en Breast Cancer wrapper k3 vence filtro k3 T26 por 0.01434 puntos de error de balanced accuracy; sin embargo full-feature logistic vence a wrapper k5 T29 por 0.01990 puntos. En Diabetes la selección wrapper no supera concluyentemente a Ridge con todas las variables. **Contra:** presupuestos de variables distintos por construcción y costes no igualados. **Estado:** EMPÍRICO_OBSERVACIONAL_EXPLORATORIO, dos datasets compartidos. **Falsador:** presupuesto de adquisición realmente vinculante en dato independiente, ganancia por coste.

## DRIFT-P04 — Estabilidad no equivale a utilidad de decisión
**Procedencia:** T19/T21/T24/T25/T27/T30. **A favor:** selector basado en mínimo de correlación entre mitades no supera consistentemente al filtro, y pierde frente al baseline completo en T24/T30. **Contra:** estabilidad operacionalizada de modo simple, no compara con todas las variantes SOTA. **Estado:** EMPÍRICO_EXPLORATORIO. **Falsador:** versiones de selección estable competentes en grupos externos con impacto.

## DRIFT-P05 — El cambio de covarianza dañino está proyectado en la tarea
**Proposición:** para K fijo y pérdida cuadrática, el cambio de riesgo ante perturbación ΔΣ es tr(K ΔΣ Kᵀ). **Procedencia:** auditoría AUD01 pre-registrada commit 11b8c53 y 50 mundos; máximo residuo nulo 5.55e-17; incremento promedio dirección principal 0.09658 con perturbaciones igual Frobenius. **Contra/limitación:** identidad algebraica CLÁSICA, depende de K fijo, prior/ruido con segundos momentos y pérdida cuadrática; no constituye nueva teoría ni aplicación validada. **Estado:** MATEMÁTICO_CONOCIDO y SINTÉTICO. **Falsador fuera del supuesto:** decoder entrenable o cambio de etiquetas donde no basta la fórmula.

## DRIFT-P06 — Hipótesis nueva, NO testeada
**Conjetura:** un detector que estima perturbaciones relevantes para el predictor podrá producir menos falsas alarmas que medidas globales de drift con etiquetas tardías. **Procedencia:** abstracción tras AUD01. **Apoyo:** identidad de riesgo bajo hipótesis lineales. **Contra:** literatura de task-aware drift, error monitoring, shift detection y score de decisión posiblemente cubre la idea; aún no revisada exhaustivamente. **Estado:** NO_VALIDADO; no reivindicar 2/3. **Falsador futuro:** datasets longitudinales externos, detectores PSI/KS/MMD y loss-aware adversarios, el mismo presupuesto e indicadores de costo de falsa alarma.

Reparación: T19 intentó ejecutarse con B04 inválido y abortó sin ajuste; errata y compromiso B04_REPAIR de GitHub antes de rerun; no confundir con una prueba adicional válida.
