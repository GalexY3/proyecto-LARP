# LARP — Dictamen del rescate T2 y siguiente prueba

**Fecha:** 11 de octubre de 2026. **Estado:** revisión local y especificación prospectiva; **ningún replay neuronal ejecutado** en esta revisión. El archivo adjunto se trata como evidencia recibida y propuesta, no como autorización automática para sus experimentos.

## 1. Qué se salvó

El rescate es honesto sobre su alcance: reconstruye mensajes y aporta dos verificadores nuevos; no recupera la corrida perdida. Se conservaron el ZIP y sus diez archivos íntegros en `docs/external_research/chatgpt_rescue_t2_2026_10_11/`. El MD externo es byte-idéntico al interno. Se verificaron los nueve archivos del manifiesto, CRC y el kit anidado: éste es exactamente nuestro kit previo, con sus 76 archivos de payload verificados. No constituye nueva evidencia experimental.

Los hashes del audit de pesos coinciden con nuestra exportación: tres **estados de modelo**, sin optimizer ni RNG; no tres checkpoints completos para reanudar entrenamiento. La carga estricta ya se comprobó al exportarlos. El rescate no incluye esos pesos ni realiza un nuevo forward.

Faltan scripts originales de A/F/B, datos y predicciones por mundo, semillas de splits, ajustes de probes y recibo de tiempo. Las mejoras neuronales, el toy de interferencia y el piloto de adquisición son **resultados reportados en conversación**. No se pueden reconstruir intervalos de confianza ni acreditar la hora original. Su pérdida no refuta el hallazgo, pero impide verificarlo.

| Afirmación | Estado tras revisión local |
|---|---|
| Inversión T2 y unicidad real fuera de factores cero | Verificada algebraica y numéricamente |
| Triple 024 mejor condicionada entre diez matrices de exponentes | Verificada; alcance limitado a esa matriz |
| Riesgo infinito de inversión ingenua bajo el ruido aditivo especificado | Argumento analítico válido |
| Mejoras MHU/LOCAL del decoder factorizado | Reportadas, pendientes de replay |
| Robustez de probes a ruido de etiquetas | Reportada; faltan escala, umbral y datos |
| Causa curricular del deterioro de Scale3D | No identificada; el resultado F es un toy |
| Ventaja neuronal causal de MHU | No probada |

El audit recibido de 512 vectores usa gaussianos sintéticos nuevos. **No verifica las 512 etiquetas reales** que se mencionaban en la captura. El agregado y el panel T2-only tampoco preservan cifras completas de RANDOM; no se debe excluir ese brazo en el replay.

## 2. Qué cambia científicamente

Las etiquetas son

\[
y=(f_0f_1,f_1f_2,f_2f_3,f_3f_4,f_0f_2f_4).
\]

La matriz de exponentes tiene determinante 3 y rango cinco módulo 2. Magnitudes y signos determinan unívocamente los cinco factores reales no nulos. Por ejemplo:

\[
f_0=\operatorname{cbrt}\left(\frac{t p_{23}p_{01}^{2}}{p_{34}p_{12}^{2}}\right),
\quad f_1=p_{01}/f_0,\quad f_2=p_{12}/f_1,
\quad f_3=p_{23}/f_2,\quad f_4=p_{34}/f_3.
\]

Para campos continuos gaussianos, los ceros exactos tienen probabilidad cero en el modelo ideal. Por ello, **etiquetas T2 exactas y campos proporcionan la misma información supervisora casi seguramente**. Corrijo nuestra precaución inicial: recuperar los campos desde esas etiquetas no añade un canal de información privilegiado. Sí aporta conocimiento del mapa generativo, un objetivo de aprendizaje distinto y composición explícita. Igualar información no iguala gradientes, condicionamiento, cómputo ni oportunidades de ajuste.

La auditoría local añadió 100.000 vectores con semilla distinta: MSE de reconstrucción `1,161×10⁻³²` con productos en doble precisión; `6,853×10⁻¹⁶` con productos float32 promovidos a double. Esto explica por qué una cifra próxima a `10⁻¹⁵` puede ser perfectamente plausible, sin verificar ninguna mejora neuronal perdida.

Los factores cero sí permiten ambigüedad: `(0,1,2,3,4)` y `(0,2,1,6,2)` producen las mismas etiquetas. No extrapolar unicidad a toda la recta real ni a etiquetas ruidosas.

### Estabilidad: dos nociones diferentes

La condición de la matriz de exponentes es 3,726, menor que la de las otras nueve triples consideradas. Pero el Jacobiano real es

\[
J=\operatorname{diag}(y)E\operatorname{diag}(1/f),
\qquad\det J=3f_0f_1f_2^2f_3f_4.
\]

| Factores: todos uno, salvo f₂ | Condición 2-norma del Jacobiano |
|---|---:|
| f₂=1 | 3,726 |
| f₂=10⁻³ | 2.449,49 |
| f₂=10⁻⁶ | 2.449.489,74 |

La buena condición en log-magnitudes no garantiza recuperación uniforme con ruido aditivo. Con ruido gaussiano independiente de varianza positiva en la etiqueta `p12`, y restantes etiquetas observadas fijas y no nulas, la reconstrucción satisface \(\hat f_0^2=C|p_{12,obs}|^{-4/3}\). La densidad del denominador es positiva cerca de cero; la integral diverge. Un Monte Carlo finito no puede acreditar finitud del riesgo. Esta conclusión es sobre inversión ruidosa de **etiquetas**, no automáticamente sobre ruido de sensores ni sobre un readout ridge ya ajustado con etiquetas limpias.

### Un rival que debe quedar abierto

Multiplicar estimaciones de campos no suele ser el predictor Bayes óptimo de productos. Para dos factores:

\[
E[f_if_j\mid h]=\mu_i(h)\mu_j(h)+\operatorname{Cov}(f_i,f_j\mid h).
\]

La triple añade términos media-covarianza y el momento central de orden tres. Aunque el prior de campos sea independiente, la representación comprimida `h` puede inducir dependencia condicional. Una mejora de la lectura factorizada sería un resultado útil dentro de un régimen; no una demostración de que reconstruir medias y multiplicar siempre basta.

## 3. Interpretación provisional y decisión

El agregado comunicado MHU `0,2423→0,2117` y LOCAL `0,2111→0,1961` equivale aproximadamente a mejoras del 12,6% y 7,1%. **Estas cuentas solo comprueban la aritmética del reporte**, no las pérdidas, sus incertidumbres ni la independencia de paneles. LOCAL conserva menor MSE final. No hay motivo para actualizar H1–H6 numéricas o declarar una recuperación de la tesis MHU.

La hipótesis que merece la próxima prueba es **H-READOUT-T2**: una parte del error de estos backbones congelados se reduce con una lectura que usa la composición conocida de la tarea. Rival **H-OPT-T2**: basta ajustar una cabeza convencional específicamente en T2 con datos y presupuesto nuevos. Rival **H-REPORT**: el signo depende de selección, splits o ajustes no conservados. Una representación con información decodificable no prueba que el transporte sea suficiente ni identifica oversquashing.

**Recomendación:** sustituir temporalmente otra hora de búsqueda amplia por un replay pequeño, completo y auditable. Si el efecto sobrevive, replicar en la segunda tríada geométrica existente. No reentrenar el backbone ni regenerar geometrías para esta pregunta.

## 4. Especificación recomendada del replay

### Alcance, datos y presupuesto

Primera etapa: N32768, g3201, u1800, los tres brazos MHU/LOCAL/RANDOM. Usar fuente y geometrías originales con hashes verificados. Tarea 2 en todo forward, ancho 256, ocho bloques, grado 16. Hook **antes del primer LayerNorm de la cabeza**, con sus 265 features exactas. No seleccionar capas ni sustituir pooling por los dieciséis estados vecinos.

Fijar antes de ejecutar 64/16/64 mundos train/validation/test y 16 queries nuevas por mundo. Propuesta de namespaces de mundos: `2026110100+i`, `2026110200+i`, `2026110300+i`; queries mediante NumPy con `2026110400+i`, `2026110500+i`, `2026110600+i`, respectivamente, con `i` dentro de cada split. Es una elección nueva local: no se conocen las semillas perdidas y no se promete ausencia absoluta de solapamiento con ellas. Coeficientes y queries deben coincidir entre brazos; ningún mundo comparte coeficientes entre splits. Se conservan bandas y modo-seed históricos.

Medir primero un forward B=1 por brazo. Presupuesto propuesto por etapa: **1.800 segundos, hasta 80% de VRAM y como máximo 8 GB de caché en RAM/disco para el nuevo estudio**. Si el coste previsto no cabe, detener antes de abrir test y registrar `NOT_RUN_BUDGET`; no reducir N, cambiar la red o evaluar solo los brazos rápidos. GPU o CPU efectivos y precisión quedan registrados. El replay comienza solo al ejecutar una fase autorizada; esta revisión no lo ha iniciado.

### Lecturas que deben compararse

| ID | Lectura sobre las mismas features | Qué permite distinguir |
|---|---|---|
| O | Cabeza histórica congelada | Error actual, sin nuevos ajustes |
| R-Y | Ridge directo para las cinco etiquetas T2 | Control lineal y objetivo directo |
| R-F | Ridge para factores obtenidos invirtiendo etiquetas T2; luego productos | Objetivo de factores y composición conocida |
| L-P | Cinco factores lineales y productos, entrenados directamente con pérdida T2 | Composición sin objetivo auxiliar de factores |
| M-R | Cabeza original refit con pérdida T2 | Optimización específica de tarea |
| M-S | Misma arquitectura de cabeza, desde cero y pérdida T2 | Efecto de la inicialización histórica |

R-Y, R-F y L-P tienen 1.330 coeficientes incluyendo interceptos. La cabeza MLP original tiene 69.911 parámetros. No se proclama parameter matching entre todas las familias: se reportan parámetros, pasos, tiempo y coste. La comparación identifica disponibilidad de distintos decoders, no capacidad abstracta igualada. El control L-P es esencial para evitar atribuir al objetivo de campos una mejora que procede simplemente de la función factorizada.

Para R-F se invierten **solo las etiquetas T2 del train**, en float64, sin leer los campos originales del generador. Comprobar recomposición y finitud; un fallo numérico invalida ese contraste hasta resolverlo prospectivamente, sin descartar silenciosamente ejemplos. El test de productos se evalúa entero, sin invertir sus etiquetas para predecir ni filtrar consultas por factores ocultos. Campos verdaderos pueden emplearse después como diagnóstico de test, separado del endpoint principal.

Estandarizar features para ridges/L-P usando únicamente train; intercepto no penalizado. Conservar las 265 columnas: si su desviación de train es ≤10⁻¹², fijar divisor a uno, centrar normalmente y registrar la columna como constante. Aplicar la misma regla a R-Y/R-F/L-P; los tres indicadores T2 son constantes. Ridge minimiza \(n^{-1}\|XW+b-Y\|_F^2+\lambda\|W\|_F^2\), con grid \(\{10^{-6},10^{-4},10^{-2},1\}\). Elegir por **MSE T2 de validation**, también para R-F; no usar pérdida de campos de validation como una ventaja de selección. Los brazos reciben el mismo grid y regla de desempate: mayor regularización.

M-R y M-S usan la arquitectura exacta original y sus features sin estandarización externa. L-P usa factores lineales sobre features estandarizadas. Para los tres aprendices por gradiente: Adam, lr=0,001, sin weight decay, batch=128, 500 pasos, MSE T2, permutaciones y semillas de optimización comunes entre brazos. Guardar candidato a 100/300/500 pasos y seleccionar por validation; desempatar por menos pasos. M-S comienza con una inicialización PyTorch común entre brazos, semilla 2026110800. L-P comienza **sin ajustar a campos ni inicializar desde R-F**: intercepto cero, coeficientes gaussianos independientes con desviación `1/sqrt(d)`, donde d es el número de features no constantes en train, semilla 2026110801 común entre brazos. Esto evita inicializar todos los factores a cero, que anularía gradientes de productos. Permutaciones de minibatches: semilla 2026110802, mismas muestras y orden entre brazos y aprendices. Una posterior variante de L-P inicializada desde R-F podría probar ajuste del objetivo después de supervisión de factores, pero sería otro control y otro presupuesto.

No ajustar ese grid, learning rate o presupuesto después de mirar test. Un refit fallido no prueba incapacidad universal de la cabeza; el alcance es esta receta y este presupuesto.

### Endpoint y puertas

Guardar predicciones por mundo/query/componente de todas las lecturas. Endpoint principal: diferencia emparejada de MSE T2 entre R-F y O, **promediada previamente sobre MHU y LOCAL**. RANDOM y cada brazo individual son endpoints secundarios explícitos. Reportar pares y triple por separado, predictor cero, errores por mundo y un intervalo bootstrap descriptivo por mundo (10.000 remuestreos, semilla 2026110700); las queries no son réplicas independientes.

**CONTINUE diagnóstico:** mejora relativa ≥3%, diferencia favorable en ambos brazos estructurados y límite inferior del intervalo de mejora absoluta >0. Definir la mejora relativa como `1 - mean_MSE_R-F / mean_MSE_O`, donde ambas medias promedian primero por mundo y después por igual sobre MHU/LOCAL; no promediar ratios por brazo. Cada remuestreo bootstrap conserva juntos los resultados de todas las lecturas y brazos de un mismo mundo. Es una puerta práctica, no una prueba de novedad ni un umbral HU. Si la precisión no discrimina, `INCONCLUSIVE`; no añadir paneles buscando el signo.

**PIVOT a optimización:** M-R o M-S iguala/supera R-F con presupuesto declarado. **CONTINUE mecanismo de composición:** R-F/L-P conserva una ventaja frente a esas cabezas, dentro del alcance del presupuesto; luego estudiar sensibilidad a datos, objetivo y calibración de momentos. **STOP dentro de este alcance:** el replay válido no reproduce una mejora relevante. Un error o presupuesto insuficiente no son evidencia negativa de la hipótesis.

Segunda etapa, si la puerta lo justifica: repetir en la tríada existente g3202, con nuevos namespaces de mundos/queries y sin modificar familias, reglas ni parámetros de selección. Es réplica en otra geometría entrenada ya existente, no una nueva realización prospectiva de generador. No hacer inferencia poblacional robusta sobre geometrías a partir de dos semillas. Una comparación causal de supresión espectral necesitaría otro diseño.

### Persistencia y ruido

El problema anterior fue perder evidencia. Guardar el protocolo/config resueltos y hashes **antes** de calcular; arrays y recibo parcial tras cada brazo/split, de forma atómica; logs, hardware, tiempos y estado incluso si se interrumpe. No sustituir resultados perdidos por mensajes narrativos. Una entrega parcial de datos vale más que otro relato sin archivos.

Ruido de etiquetas queda fuera del replay limpio. Solo después, abrir una fase nueva con distribución y escala fijadas, inversión regularizada definida en train/validation y evaluación sin excluir muestras difíciles. No añadir ruido a sensores y llamar a ello la misma intervención. Una comparación de riesgo ruidoso exige un baseline que opere directamente sobre T2 y reconocer la patología de momentos de la inversión ingenua.

## 5. Registro AB y artefactos de esta revisión

`belief_revision`: se corrige la supuesta información privilegiada de campos en el régimen T2 exacto; se valida la identidad y la advertencia de estabilidad. Los resultados empíricos conservan estado reportado. `hypothesis_generation`: H-READOUT-T2, H-OPT-T2 y rival de selección/reporte. `objective_revision`: ninguna revisión definitiva del objetivo LARP. `decision`: recomendar replay controlado como siguiente intervención, pendiente de ejecución. Priors numéricos H1–H6 intactos.

Auditorías locales: `artifacts/rescue_review_20261011/math_audit.json` y `evidence_audit.json`; script algebraico propio `math_audit.py`. Procedencia de entrada: `docs/external_research/chatgpt_rescue_t2_2026_10_11/IMPORT_RECEIPT.json`. Estas pruebas no incluyen forward ni entrenamiento de redes. La identidad algebraica y el diagnóstico potencial son útiles; no se reclama una contribución académica nueva de nivel 2/3 o 3/3.
