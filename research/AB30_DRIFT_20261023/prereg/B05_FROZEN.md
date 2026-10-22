# AB30 drift B05 — preregistro antes de entrenar en Breast Cancer Wisconsin

AB3.2.1/O1/O2. SHA256 íntegro del manifiesto JSON generado y congelado ANTES de ejecución: 84f471fbf155bc2577bb7b3ce40808944b53807a85a79d1266b1df740e300e5f. Motor SHA256: 867e75309dfa81c8568bb2360d4cb4909560a338d7f16a587d03bba877f1deb6.
Razón del pivot: la búsqueda greedy por validación no superó de modo estable ni correlación ni Ridge con 10 variables en Diabetes; ahora se contrasta selección en clasificación (dataset distinto), no buscando MHU.

Datos: sklearn load_breast_cancer, 569 muestras, 30 predictores numéricos. 16 seeds 1500..1515, splits estratificados train/test 70/30, separación de subtrain/validación dentro del train, estandarización fit SOLO subtrain. LogisticRegression(C=1,max_iter=500) igual para todos; misma información a tiempo de selección, costo de wrapper mayor y cuantificación pendiente. Primary endpoint: 1-balanced-accuracy en test. Intervals descriptivos pareados, mismo dataset y múltiples pruebas, NO confirmación independiente.

T25 stable vs filter k3: estabilidad gana frente a correlación global.
T26 wrapper vs filter k3: greedy validation gana frente a filtro.
T27 wrapper vs stable k3: greedy gana frente a estabilidad.
T28 filter vs random k3: selección entrenada gana a selección aleatoria.
T29 wrapper vs full k5: cinco características greedy ganan a modelo regularizado de todas las 30.
T30 stable vs full k5: cinco características estables ganan a modelo completo.

Falsador para cada hipótesis: delta error A−B >=0 o intervalos con cero -> no sostener superioridad general. Riesgos: no se evalúa coste de selección, data test reutilizada entre condiciones, dataset clínico antiguo no constituye causalidad médica, selección greedy puede sobreajustar validación, full-feature logistic es baseline competente, broad novelty 2/3 requiere revisión y replicación independiente.
