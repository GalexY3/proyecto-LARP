# Priors LARP — apéndice LC30 (no sustituye entradas previas)

**LC30-01 · PROPOSICIÓN:** diseño dirigido al objetivo suele superar a geometría fija si el estimando es conocido. **Apoyo:** TARGET_GREEDY gana 18/30 condiciones simuladas corregidas. **En contra:** únicos 54 nodos físicos, generador sintético, otros diseños no optimizados exhaustivamente. **Falsador:** comparador GP y selección robusta con datos reales y presupuesto equiparado. **Estado:** SINTÉTICO_EXPLORATORIO.

**LC30-02 · PROPOSICIÓN:** regularización espacial y covarianza de roles pueden ayudar en casos particulares. **Apoyo:** COSI_PROXY gana 6/30; en auditorías post hoc de ruido y campos suaves logra resultados favorables. **En contra:** inferioridad media agregada frente al greedy dirigido, sensibilidad a hiperparámetros y comparadores conocidos. **Falsador:** nuevas estaciones, nuevos targets, hiperparámetros igualados. **Estado:** SINTÉTICO_EXPLORATORIO.

**LC30-03 · PROPOSICIÓN:** un selector de algoritmos sobre validación puede mejorar una estrategia fija. **Apoyo:** RMSE medio 0.149708 frente a 0.163876 de target-greedy, y 0.105493 frente a 0.117319 en 56 ejecuciones auxiliares elegidas post hoc. **En contra:** técnica de model selection conocida, objetivos heterogéneos, selección adaptativa sin holdout independiente. **Falsador:** nuevo estudio físico con cartera y políticas congeladas antes de abrir test. **Estado:** SINTÉTICO_EXPLORATORIO, sin novedad científica acreditada.

**LC30-04 · PROPOSICIÓN:** las bases latentes estructurales deben mantenerse si no se interviene un cambio de distribución. **Apoyo:** defecto del runner invalidado y reparación íntegra con separación de semillas. **En contra:** auditoría de correlación sólo es un smoke test. **Falsador:** prueba externa de invariantes en cada generador. **Estado:** ERROR_DE_INSTRUMENTACIÓN_REPARADO.

**LC30-05 · PROPOSICIÓN:** la distancia euclídea al nodo elegido refleja coste real de comunicación. **Apoyo:** únicamente proxy geométrico de distancias. **En contra:** no hay potencias de enlace ni tasas de retransmisión observadas. **Falsador:** calibración de consumo/routing sobre conexiones reales. **Estado:** NO_VALIDADO.

No convertir ningún posterior cualitativo en probabilidad numérica calibrada. Preservar registros anteriores y sus resultados adversos.
