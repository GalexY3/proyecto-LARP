# LARP | AB 3.2.1 | 45 ciclos de branching adaptativo, 22-10-2026

**DICTAMEN: 1/3; no demostrado 2/3.** Esta campaña **no implementó** la geometría MHU original de Scale3D ni el COSI histórico. Evaluó la *hipótesis transferible de selección de mediciones* con datos observados y presupuestos restringidos. No se declara novedad científica, arquitectura neuronal ni utilidad comercial validada.

## Pregunta y motivación

Tras varios estudios sintéticos y de imagen, se investigó si diversificación geométrica/estadística y estimación de covarianzas podían mejorar la selección restringida de observaciones en cuatro conjuntos de datos independientes de scikit-learn: Digits (1797 muestras, 64 píxeles), Wine (178, 13 variables), Breast Cancer (569, 30 variables) y Diabetes (442, 10 variables; regresión). El objetivo no es diagnóstico clínico. Fuentes incluidas en `sklearn.datasets`, con particiones train/valid/test deterministas por dataset.

La línea multisitio física Beijing Air Quality no se pudo materializar en el entorno; no hay prueba de redes físicas. Esto es un **pivot limitado** a adquisición de características estáticas con observación completa retrospectiva. Las perturbaciones y los costos no representan adquisiciones reales.

## Protocolo y branching REALMENTE hecho

45 decisiones preceden a sus experimentos respectivos, documentadas en `decision_events.jsonl`, y resultados en `cycles.jsonl`. Tras cada condición, se determinó la siguiente familia y dominio por ganador de VALIDACIÓN, margen, contadores de exploración y política explícita en `campaign.py::propose`. Las familias BASE, FEWSHOT, BUDGET, NOISE, DROPOUT, RIDGE_ALPHA y TRANSFER_DOMAIN se fijaron antes de ejecutar; **la secuencia y parámetros sí dependen de resultados anteriores**, pero no hubo 45 reformulaciones teóricas independientes. 22/45 condiciones pertenecen a TRANSFER_DOMAIN, interpretado como alternancia de cuatro datasets, no como experimentos externos independientes. El conjunto de validación fue reutilizado adaptativamente 45 veces. Los TEST de cada dominio permanecieron sin consultarse durante los 45 ciclos.

Métodos con presupuesto por condición: TARGET = selección greedy usando covarianza empírica y covarianza objetivo, SHRINK = covarianza regularizada (preexistente estadísticamente), RANK = scoring supervisado individual, FPS = selección de características descorrelacionadas (en Dígitos cobertura espacial auténtica de una retícula de píxeles), RANDOM, e híbrido espacial para Dígitos (núcleo gaussiano a priori). En otros datasets no se atribuye geometría a los índices de variables. Misma predicción Ridge y mismos ejemplos de entrenamiento por brazo.

**GANADORES VAL:** {"TARGET": 15, "SHRINK": 11, "RANK": 2, "FPS": 9, "RANDOM": 5, "SPATIAL_HYBRID": 3}. Estadística descriptiva, sin significación global defendible dada la adaptación.

## TEST final: una sola evaluación congelada por dominio

Se eligió por dominio el brazo con RMSE de validación promedio más bajo entre sus últimas cinco condiciones. Se aplicaron cuatro configuraciones limpias idénticas por dominio a cada brazo, fijadas antes de abrir el test final. El estimando es RMSE de predicción usando las variables seleccionadas, no RMSE de campo físico ni coste monetario.

| Dataset | Brazo elegido | RMSE elegido | TARGET control | Reducción vs TARGET |
|---|---|---:|---:|---:|
| digits | SHRINK | 0.24374 | 0.24047 | -1.36% |
| wine | TARGET | 0.19240 | 0.19240 | +0.00% |
| breast | SHRINK | 0.25101 | 0.25675 | +2.24% |
| diabetes | FPS | 1.08305 | 1.16836 | +7.30% |

Bootstrap posterior emparejado del diferencial RMSE TARGET−elegido sobre casos del mismo TEST: Digits [-0.006624695907357383, 0.00020978378761359214]; Breast [-0.011669979945777594, 0.02478819943722166]; Diabetes [0.06764401858654316, 0.10462392914301258]. Estos intervalos son **diagnóstico post hoc**, no procedimientos preregistrados con garantías causales, y no representan replicación sobre nuevos dominios.

### Hallazgos a favor / en contra

- FAVOR: la elección contextual es plausible; SHRINK gana sobre TARGET por ~2.2% en Breast con incertidumbre elevada; FPS por descorrelación gana ~7.3% en Diabetes bajo configuración final. Ambas técnicas son conocidas y no confirman MHU.
- CONTRA: en Dígitos, SHRINK elegida con validación pierde ~1.36% ante TARGET en test; el híbrido espacial tampoco supera TARGET. En Wine TARGET sigue mejor. No hay superioridad universal, ninguna ventaja significativa de geometría MHU observada.
- Riesgo técnico: la primera campaña usó una **segunda normalización indebida** de evaluación. Se guardaron `INVALID_DOUBLE_SCALE_*`; tras descubrir el error se modificó `fit_eval`, se reiniciaron decisiones desde C01 y se volvió a ejecutar todo. Los resultados anteriores no sustentan inferencias.
- Riesgo estadístico: los cuatro tests finales se han abierto; ninguna repetición adicional sobre ellos sería confirmación. La escala de RMSE depende del número de clases y de la estandarización de la regresión: no promediar comparaciones absolutas entre dominios. Entrenar un Ridge de salida one-hot también difiere de optimizar exactitud de clasificación.

## Literatura que reduce posibilidad de novedad

- Von Kleist et al. (JMLR 2025) analizan evaluación de adquisición activa de variables y los problemas de cambio de distribución.
- Aronsson, Rahbar y Chehreghani (IJCAI 2026) unifican métodos de adquisición secuencial en una formulación POMDP.
- Valancius et al. (ICML 2024) estudian selección no greedy condicionada al conjunto adquirido.
- CAAF (Communications AI & Computing 2026) describe colocación de sensores dependiente de correlaciones y objetivos. Esta campaña no lo implementa ni lo supera.

## AB-DECIDE

**STOP la rama de feature selection estática como candidata a 2/3.** Continuar requiere una nueva clase de evidencia y una hipótesis específica irreducible a selección supervisada, shrinkage, métodos de diseño bayesiano o adquisición activa existentes. El usuario autorizó un máximo de 45: se ejecutaron 45, pero el número no fortalece su independencia estadística. Las variantes geométricas no merecen interpretación biológica ni el título MHU sin certificados espectrales y código original.

**Candidato futura rama (sin autorización automática de originalidad):** comunicaciones escasas y heterogeneidad funcional de verdaderos sensores distribuidos, con datos reales de paquetes y medidas, pérdidas por desconexión, coste de energía y comparación de métodos convencionales de diseño de redes. Antes de levantar experimentos, obtener observaciones reales y congelar la prueba.

## Reproducción y archivo

`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python campaign.py 45`; `python verify.py`; `python audit.py`; `python build_report.py`. Dependencias: numpy, scipy, scikit-learn, matplotlib. Se preserva el historial fallido como archivo `INVALID_DOUBLE_SCALE_*` y no se reutilizan esos números en el análisis. Ver `MANIFEST_SHA256.json` para huellas y `README.md` para el alcance.
