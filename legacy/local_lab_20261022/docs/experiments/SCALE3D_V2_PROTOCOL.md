# LARP — Reparación espectral y escalado 3D v2

Fecha: 2026-10-10. Autorización humana: «corrijamos», después de informar el fallo de admisión de las cuatro geometrías grandes de v1. Ésta es una versión prospectiva independiente. Conserva fuentes, configuración, resultados, clasificación y checkpoints v1; no reutiliza sus métricas neuronales como parte de una curva v2.

## Problema y reparación

En v1, los promedios muestreados de la banda eran pequeños, pero algunos tipos retenían medias de primera capa entre 0,245 y 0,420; el límite es 0,20. Promediar uniformemente O(N) modos diluye el peso de los tres modos de longitud máxima. El Jacobiano de la amplitud de Fourier contiene un factor de norma del vector de onda.

La única intervención sobre la construcción es sustituir el peso espectral constante por `w(m) ∝ h(m)/|m|²`, normalizado por separado para la unión y los cinco tipos, en los mismos shells isotrópicos completos. `h` conserva la multiplicidad hermítica rFFT. Es una heurística de acondicionamiento modal derivada analíticamente, no una garantía de convergencia de Adam. La [revisión adversarial](SCALE3D_V2_REPAIR_REVIEW.md) conserva justificación y riesgos.

Se mantienen χ=0,12, 600 iteraciones, inicialización uniforme con etiquetas Hamilton 163:85:68:50:34, término local con peso 0,15, resolución CIC y calendario Adam. RANDOM sigue siendo la inicialización uniforme sin relajación. LOCAL conserva exactamente el término local v1; una prueba exige igualdad numérica de sus coordenadas con v1 a igual semilla. Los brazos parten de las mismas posiciones y etiquetas por tríada.

## Calificación y admisión

Antes de entrenar se ejecuta un panel técnico fijo de tamaños 16384/32768 y semillas 9107/9108, disjuntas de las de entrenamiento. Para 9107 se calcula además el constructor v1 con la misma inicialización, como referencia de diagnóstico. No hay selección de semillas, búsqueda de exponentes ni entrenamiento neuronal en este panel. Presupuesto técnico máximo de 600 segundos, comprobado entre candidatos; una llamada iniciada puede excederlo. Si alguna de las cuatro geometrías v2 falla, se conserva y no se lanza la batería.

Se conserva la puerta v1: media muestreada de banda baja y media de primera capa ≤0,20 en los seis componentes, calculadas mediante sumas continuas FP64. Se añade la media **no ponderada de todos los modos** de la banda, también ≤0,20: la periferia no puede esconder un deterioro tras el nuevo objetivo ponderado. Se guardan máximos, perfil de shells, bandas externas, separación homotípica, p05/CV de vecinos e impronta CIC. No se aumenta el umbral ni se admite por el valor de la pérdida del optimizador. Los hashes del constructor y calificación se verifican antes del job principal.

La admisión es finita; no establece hiperuniformidad asintótica o equivalencia biológica. V1 mostró impronta coherente de rejilla CIC, `S/N≈0,075–0,10` para MHU y `0,18–0,21` para LOCAL. V2 la mide y la declara; esta reparación no intenta eliminarla. LOCAL ya pasó la puerta finita en tres de las cuatro realizaciones pequeñas de v1. El contraste MHU/LOCAL representa penalización espectral adicional, no HU frente a no-HU demostrado. RANDOM es un convencional espacial; su contraste también incorpora diferencias de cobertura y separación. Una interpretación sobre retina desordenada necesitaría resolver la impronta y auditar desorden por separado.

## Batería neuronal congelada

Se usan semillas nuevas 3201/3202, con tamaños 32768, 16384, 4096 y 1024, en ese orden para verificar primero la escala antes bloqueada. La curva se presenta por N ascendente; no se compara v1 con v2 usando datos distintos como si fuera un efecto causal del cambio. Modos y queries de entrenamiento/evaluación cambian a 48202/48201/48204; mundos de evaluación usan 48203, y master seed 20261020. La distribución de tareas permanece idéntica.

Red, grafo, datos, tareas y evaluador se importan directamente de v1: ocho capas residuales, anchura 256, grado 16, 4.827.415 parámetros por brazo, batch 2, AdamW LR 0,0003, weight decay 0,0001, clipping 1. Se mantienen las tres tareas: reconstrucción suave, reconstrucción de frecuencias medias y productos multicanal de frecuencias altas. Currículo original: tarea0 hasta300; mezcla 0/1 hasta600; mezcla 0/1/2 hasta1800. **No se corrige simultáneamente la incompetencia de la tarea2** observada en v1; cambiar ahora la arquitectura impediría atribuir diferencias al constructor.

Cada tríada MHU/LOCAL/RANDOM comparte pesos iniciales, mundos, targets y número de actualizaciones. Las observaciones difieren por sus posiciones de adquisición. Se evalúan 64 mundos nuevos sobre 256 queries reservadas en pasos 300/600/1200/1800 y se conservan pesos y optimizadores. FP32/TF32 para entrenamiento; FP64 para certificados.

Es escalado de densidad en un toro 3D fijo, con parámetros y profundidad constantes; el alcance físico del grafo disminuye. No identifica una ventaja espectral residual de computación neuronal. La prueba puede mostrar una interacción descriptiva entre adquisición, conectividad y aprendizaje.

## Presupuestos, cierre y resultados

Job principal nuevo: máximo seis horas mediante guardian propio; límite blando de 2700 s por tríada incluyendo generación/evaluación. CUDA de la RTX4070SUPER, hasta 80% de VRAM, ocho threads CPU. No se reutiliza el saldo de v1: el nuevo encargo autoriza esta versión y su presupuesto explícito. OOM/no finitos detienen el job global; una geometría inadmisible conserva cero updates sin reemplazo. No se cambia anchura, batch o LR para un solo brazo ni se hace HPO con test.

Se preservan v1 y priors H1–H6/C, auditando hashes de 1100 archivos históricos, incluidos arrays/checkpoints locales v1. El modelo MHU debe pasar la puerta en cada realización nueva, aunque la calificación técnica haya pasado. El endpoint global exige las ocho tríadas y el mayor checkpoint común completo. Si falta cobertura, la escala sigue inconcluyente; se retienen comparaciones por N válidas. Dos semillas dan rangos descriptivos, no confirmación concluyente. El informe automático conserva MSE y cocientes emparejados frente a ambos controles, sin selección favorable ni actualización bayesiana inventada.

## Antecedentes y alcance de la decisión

La optimización por coordenadas colectivas y la generación de sistemas hiperuniformes grandes tienen antecedentes revisados por pares: [Physical Review Research 5, 033190 (2023)](https://doi.org/10.1103/PhysRevResearch.5.033190). También existe un modelo computacional multihiperuniforme para antenas y metasuperficies en [EPJ Applied Metamaterials (2024)](https://doi.org/10.1051/epjam/2024003). Son antecedentes de construcción, no evidencia de utilidad neuronal ni validación del peso concreto aquí elegido. La ponderación inversa se registra como inferencia propia; no se reclama innovación por generar MHU grande.
