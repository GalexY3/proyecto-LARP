# Priors acumulativos nuevos LARP — AB45 DRIFT (2026-10-23)

Preservar todos los priors históricos. Estos son delta de la campaña, no confirmaciones externas.

**LARP-DR45-P01 [SINTÉTICO/EMPÍRICO EXPLORATORIO]:** Ningún score unlabeled supera todos los competidores entre datasets y shifts. A favor: E01/E02/E32/E33. En contra de generalidad: E03/E05/E31/E35. Falsador: benchmarks WATCH/CTM en stream real con FPR calibrada.

**P02 [MATEMÁTICO CONOCIDO]:** Cambio en P(Y|X) sin cambio en X no es identificable desde X y f(X) solos. Pruebas E06–E10: diferencia de señales respecto a nulo cero; daño etiquetado positivo. Límite: etiquetas o instrumentación adicional pueden detectarlo.

**P03 [EXPLORATORIO]:** Etiquetado por incertidumbre para aprender no es automáticamente un muestreo representativo para estimar riesgo. Evidencia E11/E16/E28/E38/E43; contra E30/E40. Falsador: evaluación aleatorizada con propensidades y datos prospectivos.

**P04 [EXPLORATORIO]:** Estratificar por incertidumbre puede mejorar cobertura frente a seleccionar una sola cola (E25/E37). Contra E14/E24/E29/E39. No existe una ventaja universal.

**P05 [EXPLORATORIO]:** Aumentar a 32 etiquetas reduce brechas en ciertos escenarios (E26/E27/E29), pero persisten excepciones fuertes (E28/E30). Demanda curvas coste-beneficio en flujo distinto.

**P06 [NO_VALIDADO]:** Distinguir etiquetas para estimar riesgo de etiquetas para reentrenar. Hallazgos en estimación E11–E45; NO se realizó un experimento de reentrenamiento activo que confirme la segunda mitad.

**P07 [ANTECEDENTES]:** Detección task-aware y con etiquetas demoradas ya existe (WATCH, CTM 2025–26). Nueva reivindicación 2/3 exige mecanismo discriminante y comparador ejecutado, no rebautizar.

**P08 [NORMATIVO]:** O3 requiere freeze GitHub previo. B01 sí; B02–B09 no (bloqueo de conector), aunque archivos congelados localmente. Prohibido reescribir cronología; subir raw retrospectivamente si corresponde, con errata.

Cada prior se conserva con procedencia, evidencia contraria, alcance e incertidumbre. Sin Bayes numérico artificial.