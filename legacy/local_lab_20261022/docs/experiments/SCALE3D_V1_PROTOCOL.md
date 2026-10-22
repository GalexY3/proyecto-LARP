# LARP — Exploración de MHU 3D y multicapa a gran densidad

**Fecha:** 2026-10-10. **Estado:** protocolo prospectivo de exploración autorizada; no contiene resultados. La configuración ejecutable es `configs/scale3d_v1.json`, con implementación en `src/larp/scale3d_train.py` y `src/larp/scale3d_geometry.py`. El manifiesto de ejecución guardará sus hashes antes de generar geometrías o entrenar.

El investigador ha solicitado expresamente MHU tridimensional, muchas capas, gran tamaño, entrenamiento local exigente, tareas progresivamente difíciles y comparación con una red convencional de la misma naturaleza. Esta autorización abre una rama exploratoria; no reemplaza el pivote del portfolio ni modifica experimentos anteriores. La pregunta es si la ventaja relativa del sistema con geometría MHU aumenta al incrementar el número de nodos.

## Diseño y significado de escala

Se fijan cuatro tamaños: **1024, 4096, 16384 y 32768 nodos**, y dos semillas geométricas, **3101 y 3102**. Cada combinación produce una tríada de brazos, ocho tríadas en total. Las coordenadas operativas viven en el mismo toro tridimensional unitario. Aumentar N incrementa la densidad y la cantidad de observaciones; no aumenta el número de parámetros entrenables. El generador también informa distancias en unidades de separación media mediante una caja física convencional de longitud (N^{1/3}); esta conversión no cambia el dominio de las tareas.

Todos los brazos usan la misma red: ocho bloques residuales de comunicación sobre grafo, anchura 256, agregación dispersa, MLP, LayerNorm y modulación FiLM por cinco tipos. Son aproximadamente 4,83 millones de parámetros por modelo; el manifiesto comprobará el conteo exacto. Cada nodo dispone de su observación de un único canal, tipo, coordenadas periódicas e identificador de tarea. La salida predice cinco valores en cada query. La lectura combina los 16 sensores próximos a la query. El grafo usa 16 vecinos periódicos por nodo, con pesos gaussianos normalizados.

Con grado y profundidad constantes, el alcance espacial típico de comunicación disminuye aproximadamente como (N^{-1/3}). Se registran radios de vecinos y lectura, y fracciones de queries sin cada tipo entre sus vecinos inmediatos. Este experimento estudia el efecto conjunto de adquisición, geometría, conexiones y aprendizaje; no identifica causalidad espectral residual ni escalado de capacidad paramétrica.

## Brazos y puerta geométrica

**RANDOM** conserva las posiciones uniformes independientes y la permutación inicial de etiquetas; es el convencional espacial. **LOCAL** aplica 600 pasos de relajación con el término local de densidad suavizada. **MHU** aplica los mismos 600 pasos y añade una penalización de potencia en bandas bajas, total y por componente. Comparten inicialización, conteos por Hamilton a partir de proporciones 163:85:68:50:34, término local y calendario del optimizador geométrico. Se fijan `chi=0.12` y peso local 0,15. El cutoff utiliza capas isotrópicas completas por componente; su extensión en coordenadas unitarias aumenta con N.

La optimización usa cloud-in-cell y FFT. Una auditoría independiente del cálculo FFT evalúa sumas de Fourier de las posiciones continuas en FP64: unión y cinco tipos, hasta 128 modos por banda, primera capa completa, bandas exteriores y posibles improntas de rejilla. La admisión exige media espectral baja y media de primera capa ≤0,20 en los seis componentes. Los máximos se conservan aunque no sean la puerta.

Esto certifica únicamente **supresión finita de los modos auditados**. No demuestra hiperuniformidad asintótica, isotropía completa, reproducción biológica ni ausencia de orden cristalino. LOCAL puede también suprimir esas bandas: se informará su auditoría y no se asumirá automáticamente un contraste MHU/no MHU. Si MHU falla la puerta, la tríada se conserva como `INVALID_MHU_CLAIM`, con cero actualizaciones de entrenamiento y sin reemplazar semilla o constructor.

## Tareas, datos y currículo

Se generan cinco campos gaussianos independientes mediante series reales seno/coseno en bandas de norma entera **1–2, 2–4 y 4–8**, con hasta 512 modos representativos por banda. Los coeficientes se normalizan para varianza marginal unitaria. Los sensores observan solamente el canal correspondiente a su tipo, sin ruido añadido. Las tareas 0 y 1 reconstruyen los cinco campos. La tarea 2 predice cuatro productos de dos canales y un producto de tres canales distintos; el target no es una observación directa de un sensor.

El currículo usa 1800 actualizaciones máximas: pasos 1–300 sólo tarea 0; 301–600 mezclan tareas 0/1 con probabilidades 0,2/0,8; 601–1800 mezclan 0/1/2 con probabilidades 0,1/0,2/0,7. Batch 2, AdamW, learning rate 0,0003, weight decay 0,0001 y clipping de norma 1. Los tres brazos comienzan con exactamente los mismos pesos y procesan los mismos mundos y targets en cada actualización. Sus observaciones numéricas difieren porque las posiciones de adquisición difieren: no se describirán como entradas idénticas.

Se fijan 256 queries continuas de entrenamiento con seed 47201 y un conjunto distinto de evaluación con seed **47204**. La selección de modos usa seed 47202. En cada checkpoint se evalúan las tres tareas sobre 64 mundos nuevos comunes, con seed base 47203, en las queries reservadas. Los coeficientes de esos mundos no se emplean para actualizar pesos. El orden de actualización de brazos se invierte entre semillas.

## Presupuesto, endpoints y fallos

Los checkpoints son 300, 600, 1200 y 1800 actualizaciones **completas para los tres brazos**. Se guardan modelos, estados del optimizador y evaluaciones; no se comparan últimos pasos desiguales. El límite por tríada es **2700 segundos, blando**, incluyendo construcción y evaluación: una operación ya iniciada puede sobrepasarlo. Un guardian externo limita el job completo a **seis horas**. Se usa CUDA, hasta 80% de VRAM, ocho threads CPU y entorno `.venv-scale` aislado; el entorno histórico CPU permanece intacto. FP32/TF32 en entrenamiento, FP64 en auditoría. La no determinación de scatter CUDA queda declarada.

OOM o pérdida no finita detienen el job global, conservando archivos completos anteriores y un registro del error. No se reduce batch o anchura para un único brazo, no se relanza una semilla fallida y no se ajustan hiperparámetros con el test. El error de software/recursos no constituye evidencia contra MHU.

La curva principal sólo existe si están presentes las ocho tríadas y todas tienen un checkpoint completo común. Se elige el mayor checkpoint común; de faltar cobertura, `common_scale_endpoint=null` y escala inconcluyente. Las comparaciones completas por tamaño siguen disponibles. Se reportan MSE por tarea y mundo, diferencias y cocientes MHU/LOCAL y MHU/RANDOM por semilla y N, tiempos, VRAM y costes de construcción. La tendencia respecto de log N es descriptiva: 64 mundos no equivalen a 64 réplicas geométricas. Dos semillas no permiten confirmación concluyente. Se mantienen intactos los priors históricos H1–H6/C y no se reclama novedad o superioridad general.
