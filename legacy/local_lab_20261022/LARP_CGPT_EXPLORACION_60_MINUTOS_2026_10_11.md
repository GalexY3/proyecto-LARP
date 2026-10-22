# LARP — Encargo a Sol/ChatGPT: una hora de exploración con bifurcaciones reales

**Fecha:** 11 de octubre de 2026. **Autor:** SOL/Codex, revisión del batch externo. **Destino:** una nueva sesión activa de Sol/ChatGPT, con sus herramientas disponibles. Este texto es el encargo que debe copiarse a esa sesión; no acredita que ya se haya ejecutado.

## 1. Objetivo y libertad de investigación

Investiga durante aproximadamente **60 minutos de tiempo real**, incluyendo preparación, cálculo, revisión y entrega. Busca principios estructurales útiles para adquirir, transportar, representar o procesar información. MHU es una candidata; puedes encontrar una vía mejor fuera de ella. La meta es cambiar una decisión científica mediante evidencia interpretable, no producir muchos ciclos, una narración extensa ni un resultado positivo.

Quiero **más amplitud que en la sesión anterior**: considera seis vías distintas, descarta pronto las redundantes y profundiza en las dos con mayor información esperada por coste. Una debe conectar con una incertidumbre concreta del LARP actual; la otra debe cuestionar una elección estructural más amplia. Esta distribución es una recomendación, no una obligación de ejecutar un experimento malo. Puedes sustituir cualquier vía si explicas en dos frases la predicción nueva, el rival fuerte y por qué su prueba cabe en el tiempo restante.

Tienes autorización en este encargo para literatura, derivaciones, scripts exploratorios y microexperimentos acotados en tu entorno de ejecución. No presupongas acceso al PC del investigador ni a su GPU. No lances un nuevo entrenamiento completo, una instalación larga o un proceso persistente. Trabaja con copias; conserva los archivos recibidos y los resultados históricos. No hagas preguntas rutinarias: decide, registra la incertidumbre o cambia de vía cuando falte una capacidad.

No hay cuota de novedad «2/3» o «3/3». Una refutación limpia, un rival que explica toda la mejora o una prueba que evita gastar una noche de GPU pueden ser el mejor resultado de la hora. Tampoco se exige defender un pivote definitivo: propone la próxima prueba; una revisión importante de objetivos se decidirá posteriormente con el investigador.

## 2. Qué aporta el batch anterior y qué queda abierto

La parte exacta se ha recalculado localmente. En el grupo circular de 103 posiciones:

\[
A=\{0,5,20,50,60,85\},\qquad B=\{0,5,40,55,65,85\}.
\]

Los cinco tipos son las traslaciones por \(c=0,\ldots,4\) de cada conjunto. Los 25 histogramas cruzados de diferencias coinciden exactamente; A y B no son equivalentes por traslación o reflexión. Con radio circular inclusivo 9, la cobertura individual es 86/103 en ambos, los cuatro pares adyacentes tienen 84/103 y la cobertura conjunta de los tipos 0,2,4 es **78/103 frente a 80/103**. Son 30 incidencias marcadas; no se ha demostrado que sean 30 posiciones físicas distintas ni una retina desordenada admisible.

Esto refuta la suficiencia universal de las estadísticas completas de segundo orden para ese modelo de disponibilidad multicomponente. La diferencia ideal de riesgo 2/103 corresponde al modelo definido en el testigo; **no es una MSE medida de nuestras redes**. El ejemplo de covarianza triangular tiene otro acceso y otro kernel; su signo a ruido alto no contradice el testigo de cobertura.

La homometría por convolución y los efectos multitype invisibles a segundo orden tienen antecedentes cercanos: [Rosenblatt y Seymour, 1982, artículo revisado](https://epubs.siam.org/doi/abs/10.1137/0603035), y [Lotwick, 1984, artículo revisado](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/some-models-for-multitype-spatial-point-processes-with-remarks-on-analysing-multitype-patterns/0FBC39D40B4F93BBDF5DB5A9E82F8D5E). El contraejemplo concreto es útil; repetir «pares insuficientes» con más tamaños no basta para una contribución nueva.

**Límite de la transferencia:** el informe describe paneles 2D/3D, GP de 512 modos, Monte Carlo y grafos, pero no entrega los 15 scripts nombrados ni las matrices y salidas correspondientes a esos paneles. Tampoco llega el recibo de tiempo de esa sesión. Los archivos históricos de oráculos y XL contenidos en los ZIP anidados pertenecen a otros estudios. Clasifica esos paneles como `REPORTED_NOT_REPRODUCIBLE_FROM_DELIVERY`, no como resultados negativos ni como réplicas verificadas. Si conservas sus archivos reales, recuperarlos tiene un máximo de **3 minutos dentro de la preparación**; entrega lo recuperado. Si no, continúa con una pregunta nueva y no reconstruyas resultados pasados como si fueran sus originales.

Correcciones que debes conservar:

- Para \(f_c\) independientes, centrados, gaussianos y de varianza uno, ruido conocido independiente y acceso no adaptativo a los valores, el riesgo del producto de tipos distintos es \(R_J(q)=1-\prod_{c\in J}(1-v_c(q))\). Campos correlacionados, tipos repetidos o acceso adaptativo exigen una derivación nueva.
- En la expansión de ruido alto, \(\lambda\) es varianza y la serie de Neumann exige \(\lambda>\|K\|\). No extrapoles el término dominante a ruido pequeño sin comprobarlo.
- En la familia positiva de factor común \(C*D*T_c\) frente a \(C*\widetilde D*T_c\), las masas enteras positivas implican un divisor común de los conteos. Los conteos aviares exactos de N=400 y N=32768 tienen MCD 1. **Añadir multiplicidades positivas dentro de la misma fórmula no elimina esa obstrucción.** Esto bloquea esa familia, no demuestra que cualquier patrón homométrico sea imposible.
- Una réplica sobre una rejilla 4³ puede conservar homometría y separación, pero introduce orden cristalino. No la describas como desorden aviar.
- Para un modo individual, la matriz \(FF^\dagger\) tiene rango como máximo uno. Cinco entradas diagonales no equivalen a cinco autovalores independientes.

## 3. Contexto mínimo del laboratorio real

Scale3D v2 terminó: **8 tríadas, 24 redes**, N=1024/4096/16384/32768, semillas geométricas 3201 y 3202, brazos MHU/LOCAL/RANDOM. Cada red tiene **4.827.415 parámetros, ancho 256, ocho bloques residuales, grado 16 y 1.800 actualizaciones**. Dentro de cada tríada se igualaron pesos iniciales, mundos y presupuesto. LOCAL conserva el término local del generador; no es una rejilla regular. El toro 3D tiene volumen fijo: aumenta la densidad con N, mientras parámetros, grado y capas permanecen fijos y el alcance físico cambia. No es escalado de capacidad ni una prueba causal aislada de supresión espectral.

T0/T1 reconstruyen cinco campos; T2 reconstruye cuatro productos adyacentes y el triple 0,2,4. Los modos realmente usados son 16/115/512, con 32/230/1024 coeficientes por campo. Cada nodo observa solo su canal. El currículo dio 492/464/844 actualizaciones a T0/T1/T2. T2 empieza después de la actualización 600.

MSE T2 final, media de dos semillas geométricas:

| N | MHU | LOCAL | RANDOM |
|---:|---:|---:|---:|
| 1.024 | 1,008393 | 1,008511 | 1,008606 |
| 4.096 | 1,008422 | 1,008167 | 1,008026 |
| 16.384 | 0,510446 | 0,491302 | 0,736578 |
| 32.768 | 0,239350 | 0,220206 | 0,513564 |

LOCAL gana T2 en ambas semillas de los dos tamaños grandes. Hay mejoras condicionales MHU en otras tareas, dispersión entre semillas y deterioro posterior de T0 compatible con interferencia curricular; su causa no está aislada. No conviertas estos ocho tamaños/semillas en ocho réplicas independientes del mismo efecto.

Los oráculos externos previos aportan scripts y resultados: reconstrucción global de T2 casi exacta a N≥16384 bajo su prior conocido; acceso local K=24 mucho peor; acceso de ancestros de ocho hops potencialmente mucho mejor que el resultado neuronal. **Información potencialmente accesible no implica que el message passing la transmita.** No llames a la brecha prueba de oversquashing ni de un bug de head. Las cifras de oráculos son estudios previos; no hay que repetir todas sus SVD en esta hora.

CIC v3 reduce una discrepancia de generación/evaluación y tiene evidencia CPU pequeña. Todavía no prueba una mejora neuronal a N32768. Los priors numéricos históricos H1–H6 no se han actualizado con esta revisión. Cualquier hipótesis nacida mirando estos resultados necesita datos nuevos para confirmación.

## 4. Material adjunto y preflight

El **kit ligero** incluye este encargo, reloj de sesión, fuente estática de LARP, configuración/protocolo v2, geometrías y resultados de la tríada N32768/3201, análisis final, el testigo exacto y el ZIP previo de oráculos. `READ_FIRST.md` identifica las rutas. No leas nuevamente el contexto maestro de 135 KB ni todos los 390 ciclos antes de empezar. Consulta historia adicional solo para resolver una dependencia concreta.

El **ZIP opcional de pesos**, separado del kit, contiene tres estados de modelo en un único `.pt`, actualización 1800, N32768, semilla 3201. Se exportó sin optimizadores ni RNG; se verificaron carga estricta y pesos finitos, sin entrenamiento ni inferencia. Su SHA256 es `36852d49684fd95e8a195cc8249ededce3e936e70043d3b447be52146669c214`; el `.pt` tiene SHA256 `ddc944a49198be0202e387158ce73f989bd5bdd134c9aaa696dcecc7fb05c598`. La selección fue la primera semilla configurada del mayor N completado, después de conocer resultados históricos y antes de nuevos probes: es diagnóstica, no una selección confirmatoria preregistrada.

Usa `torch.load(..., weights_only=True, map_location="cpu")`, `SpatialNetwork(256,8)` y carga estricta. No ejecutes el runner histórico CUDA: sus funciones auxiliares se pueden importar para reconstruir el forward. No sustituyas arquitectura, N, ruido, normalización o modos para que el diagnóstico quepa. Si los pesos no fueron adjuntados o PyTorch no está disponible, marca vía A `NOT_RUN_CAPABILITY` y trabaja en las otras; no bloquees la hora pidiendo otra vez checkpoints.

En el primer acceso a herramientas ejecuta **solo el comando `start`**. Los demás comandos se ejecutan cuando corresponda el evento, la consulta de estado o el cierre:

```text
python session_clock.py start --run-dir output/session
```

Más adelante, al terminar preparación, consultar presupuesto y cerrar respectivamente:

```text
python session_clock.py event PREFLIGHT_DONE --run-dir output/session
python session_clock.py status --run-dir output/session
python session_clock.py finish --run-dir output/session
```

Usa un directorio nuevo. El reloj mide tiempo transcurrido monotónico, no intensidad de razonamiento ni tiempo de CPU. Registra eventos al terminar cribado, elegir vías, obtener salidas y cerrar. No espera ni ejecuta en segundo plano. Si no tienes reloj/herramientas, declara `NO_VERIFIED_TIMER`; no inventes 60 minutos. No uses esperas artificiales para completar una hora. Si terminas antes, busca una prueba adversarial adicional que quepa; si no aporta información, entrega la duración real.

## 5. Distribución de la hora

| Minutos orientativos | Trabajo | Salida mínima |
|---|---|---|
| 0–6 | Leer este encargo, verificar materiales y capacidades; recuperar faltantes solo si ya existen | Inventario, reloj, dependencias y coste inicial |
| 6–24 | Cribar seis vías, unos tres minutos por vía | Predicción, rival, descarte o prueba mínima; fuentes que cambien la decisión |
| 24–48 | Dos investigaciones de unos doce minutos cada una | Cálculo/derivación o microexperimento con control fuerte y datos reales |
| 48–55 | Atacar el mejor resultado con otro seed, régimen o control fijado antes de mirarlo | Resultado adversarial, incluida la desaparición del efecto |
| 55–60 | Comprobar archivos, guardar salidas y empaquetar | Informe corto, scripts, datos, manifiesto y recibo final |

Es un presupuesto adaptable. Un cálculo ya en curso puede aprovecharse para cribar otra vía, pero no multipliques tareas hasta perder trazabilidad. Si en una vía profunda pasan cinco minutos sin una salida interpretable ni un camino creíble dentro del presupuesto, cambia de vía y registra el límite. Una demostración corta que resuelva la decisión puede sustituir un experimento. «No probado» y «refutado» son estados diferentes.

## 6. Cartera inicial: seis vías con pruebas distintas

### A. Representación congelada: ¿se pierde información antes de la cabeza o durante su lectura?

**Pregunta:** con el backbone real congelado y condicionado en T2, ¿sus features permiten reconstruir los cinco campos o los productos mediante un decodificador asequible? Una mejora tras refit puede proceder de entrenamiento específico de tarea, no de corregir un defecto intrínseco.

El acceso primario es exactamente el tensor que recibe la cabeza original: **pool ponderado de 16 vecinos de dimensión 256 + seis sin/cos de query + tres indicadores de tarea = 265 features**. Captúralo con un hook antes del primer LayerNorm de `model.head`, sin alterar el forward. La condición sigue siendo T2 aunque el probe use etiquetas de campo. Si comparas con features después de LayerNorm, es una intervención separada sobre información perdida en esa transformación.

Controles mínimos: salida de la cabeza original en los mismos mundos nuevos; ridge para campos; refit de una cabeza con la **misma arquitectura** original para productos, con inicialización, datos y pasos comunes a los tres brazos; producto analítico de los campos verdaderos como control algebraico. Entrenar una cabeza sobre campos verdaderos sirve además para diagnosticar presupuesto/capacidad del probe, y es un control privilegiado separado.

No des acceso a 16×256 estados vecinos a la prueba primaria. Puedes analizarlos después como diagnóstico privilegiado de agregación, manteniendo query y tipos explícitos, sin atribuir su mejora a la cabeza original. Ningún fallo del ridge o MLP demuestra por sí solo ausencia de información en la representación.

**Gate de coste:** `eval`, `torch.inference_mode`, B=1 y una inferencia por brazo; mide generación, forward y memoria. El forward usa `sparse.mm`; no presupongas un tensor E×256 de mensajes. El MLP de cada bloque opera en todos los N nodos. Estima el tiempo total antes de generar datos. Si no cabe el mismo presupuesto para los tres brazos, descarta la ejecución, conservando un protocolo concreto. No reduzcas N y llames al resultado probe del checkpoint real.

Si cabe, fija antes de ver pérdidas uno de dos pilotos: 64/16/32 mundos train/validation/test, o 32/8/16 si el coste lo exige, con 16 queries por mundo y particiones disjuntas. Genera mundos y queries nuevos con semillas registradas, idénticos entre brazos; los coeficientes de campo de un mundo no pueden cruzar particiones. Selecciona ridge y ajustes solo con validation, usando el mismo conjunto pequeño de opciones. Mantén targets en su escala original y normaliza features solo con train. Test se abre una vez. Congela número de pasos del refit según el tiempo medido, no según qué brazo mejore. Si solo cabe ridge, entrega esa prueba y deja el MLP como `NOT_RUN_BUDGET`.

Entrega MSE por mundo y componente y dispersión entre mundos; un bootstrap por mundo puede ser descriptivo. Las diferencias emparejadas frente a la cabeza original se calculan **solo para productos T2**: esa cabeza, condicionada en T2, no es un baseline de reconstrucción de campos. Para campos incluye el predictor cero. Como control barato de lectura, calcula además los productos de las predicciones del ridge de campos, etiquetados como decoder factorizado, sin asumir que sea Bayes óptimo. Una sola semilla geométrica no estima incertidumbre entre geometrías. Si campos se decodifican y productos no, prioriza interfaz/lectura; si el refit mejora productos, investiga también reparto de entrenamiento; si ninguno mejora, sigue abierta la disyuntiva representación/probe/datos. No declares causalidad neuronal MHU.

### B. Adquisición dirigida por tarea: ¿organizar el acceso supera organizar el espectro?

**Pregunta:** con igual número de observaciones y coste, ¿una política de acceso condicionada en query/tipo reduce el riesgo de producto más que la geometría global? El rival principal es una regla simple de distancia con cuota de tipos, no RANDOM solo.

Reutiliza el oráculo gaussiano; un piloto nuevo puede usar 128–512 sensores, cinco tipos con conteos fijos, 32–64 coeficientes por campo y 16 queries. Fija K=16 y compara vecinos más próximos, cuota por tipo y selección greedy de reducción de riesgo posterior. Usa el mismo conjunto de sensores, prior, ruido y queries. Para greedy, contabiliza búsqueda y cualquier conocimiento privilegiado del kernel; es un techo de adquisición, no una red con parameter matching. La cuota debe declararse: cuatro tipos reciben tres observaciones y uno cuatro, rotando el excedente por query sin usar valores de campo.

La prueba que cambia decisiones es una **inversión fuera del régimen ajustado**: elige políticas en un kernel/rango de ruido y evalúa en otro previamente apartado; incluye el triple 0,2,4 y las pérdidas por campo para evitar ganar un target a costa de ocultar otro. Con ruido cero añade un chequeo de rango/residuo antes de aceptar MSE≈0. Si investigas correlaciones entre campos, deriva primero la fórmula correcta y limita el piloto a una única matriz de covarianza; no reutilices indebidamente la factorización independiente.

No repitas el panel XL por rutina: el rival de radio ya explicó o empató muchas mejoras anteriores. Continúa solo si obtienes una diferencia residual frente a ese rival o un límite útil sobre cuándo la adaptación paga su coste. Si cambias nodos observados o alcance, reconoce que cambió la adquisición, no el mecanismo neuronal ni HU aisladamente.

### C. Orden superior útil: ¿hay un efecto físico que sobreviva a rivales locales?

**Pregunta:** ¿una propiedad de disponibilidad conjunta o fase de orden superior predice riesgo residual después de controlar acceso, separación, vacíos y cuotas, en patrones físicamente admisibles? El rival es la cobertura simultánea elemental, que puede explicar todo sin invocar una nueva propiedad espectral.

Da a la búsqueda de homometría con conteos aviares exactos **un máximo de tres minutos**: usa la obstrucción de MCD para descartar familias incompatibles antes de optimizar. No conviertas el resto de la hora en una búsqueda ciega. Puedes probar un panel sintético pequeño de tres tipos y conteos divisibles, con exclusión global y homotípica declaradas, o derivar un límite de imposibilidad. Es otro sistema y debe etiquetarse así.

Mide el riesgo exacto del oráculo y compara tres predictores previamente fijados: segundo orden; segundo orden + cobertura/vacíos/cuotas; lo anterior + una única estadística de orden superior motivada por la tarea. Ajuste y selección en patrones development, evaluación en semillas geométricas nuevas. Las traslaciones sirven como control de simetría, no como patrones independientes para dividir train/test. Con pocos patrones entrega una diferencia exploratoria, no un modelo universal. No basta un R² in-sample. Si no puedes igualar simultáneamente las variables locales, el contraste no identifica supresión espectral causal: devuelve el confound y el próximo diseño factible.

Desordena o perturba dentro de exclusiones como control adversarial, midiendo cuánto rompe homometría. No escondas las tolerancias espectrales ni controles que fallan packing. Cerrar una familia inviable o mostrar que cobertura basta sería más informativo que llamar MHU a una réplica cristalina.

### D. Comunicación funcional: jerarquía, rutas y resiliencia

**Pregunta:** ¿la colocación de rutas o comunidades mejora una tarea distribuida bajo un presupuesto explícito de mensajes? Esto explora un principio distinto del muestreo MHU.

Piloto sugerido: 128 nodos en las mismas posiciones, grado medio ocho y el mismo número de enlaces; grafos local, local con atajos y regular aleatorio. La demanda debe generarse independientemente del grafo. Usa como tarea recuperar un valor en una dirección remota o agregar una suma modular; un árbol de agregación/enrutamiento exacto es un baseline fuerte. Evalúa volumen total de bits, rondas, error y congestión. Si asignas mensajes de 8/32 bits, cuenta también identificación, encabezados y estado persistente, o declara un esquema síncrono donde esos costes sean idénticos.

**Separa estimandos:** igualdad de enlaces no iguala longitud de cable; muestra ambas o realiza una segunda comparación con coste espacial igualado. Si la ventaja se explica enteramente por diámetro, acota la conclusión a alcance. Una intervención en comunidad necesita el falsificador de permutar destinos/tipos de demanda respecto a comunidades. Para resiliencia, elige fallos iid o espacialmente correlacionados como factor antes de mirar resultados y compara el mismo número de fallos; no descartes selectivamente terminales desconectados.

Una mejora de un algoritmo clásico sobre otro es un resultado de comunicaciones, no evidencia de que nuestra red aprendió routing. No entrenes un GNN solo para dar apariencia neuronal a este piloto. Si ya hay una solución estándar que agota la hipótesis, atribúyela y busca un régimen donde los rivales realmente discrepen.

### E. Dinámica temporal: direccionalidad frente a geometría estática

**Pregunta:** ¿retención, dirección o no normalidad explican una ventaja que una geometría isotrópica no proporciona? Piloto CPU: reservorios lineales de 64 estados, mismo input/output y readout ridge, retardos de 1 a 16. Compara simétrico, ortogonal y dirigido, con una línea de retardos como baseline competente.

Iguala dimensión y presupuesto de readout; mide energía de estado, ganancia de entrada, norma y amplificación de ruido. Radio espectral igualado **no basta** para comparar sistemas no normales. Usa series train/validation/test independientes, calentamiento y separación temporal suficiente; no dividas ventanas solapadas al azar. Define error de reconstrucción de retardos y sensibilidad a un ruido de estado común antes de optimizar.

La capacidad de procesamiento depende de la representación y del readout; hay antecedentes directos en [Dambre et al., 2012, artículo revisado](https://www.nature.com/articles/srep00514). Una red lineal con ridge no puede servir de prueba competente de productos no lineales: si añades una no linealidad o un readout más potente, aplícalo como factor común a todos los brazos. Si la línea de retardos u ortogonal explica toda la mejora, termina la rama de «geometría temporal especial» con ese alcance.

### F. Modularidad e interferencia: ¿conviene compartir menos?

**Pregunta:** ¿el deterioro de tareas previas se puede provocar y eliminar por asignación de parámetros/entrenamiento incluso con información totalmente disponible? Este microexperimento es una analogía para generar una intervención de LARP, no un diagnóstico del checkpoint real.

Usa un problema pequeño de dos tareas con entradas completas: por ejemplo reconstruir un vector gaussiano de ocho componentes y predecir cuatro productos adyacentes. Comparación inicial: tronco compartido con dos heads frente a dos módulos independientes, **igual total de parámetros**, contando heads y embeddings. Alterna un currículo equilibrado y uno con transición de tareas como factor común. Fija pasos, ejemplos, optimizador y semillas emparejadas; la igualdad de parámetros no garantiza igualdad de FLOPs, que debes reportar. Usa al menos una solución analítica de los targets para verificar etiquetas.

El endpoint es retención de la primera tarea tras introducir la segunda, junto con rendimiento de ambas; no solo la mejor MSE final. El rival fuerte es la red compartida con muestreo equilibrado y heads separados. No busques cinco optimizadores hasta que aparezca una victoria. Si balancear elimina la diferencia, la propuesta útil será intervenir currículo antes de cambiar geometría. Si modularidad ayuda solo con mayor cómputo, registra ese intercambio y no una ventaja estructural gratuita.

## 7. Cómo elegir, atacar e interpretar

Durante el cribado escribe una ficha corta por vía: mecanismo, predicción que podría fallar, rival más fuerte, prueba mínima, coste medido/estimado y motivo para continuar o cerrar. Una búsqueda bibliográfica debe resolver una incertidumbre concreta. Prefiere artículos originales, documentación y pruebas; distingue revisión por pares, preprint, patente e inferencia propia. Una fecha de publicación reciente no implica novedad, y una cita sin leer su alcance no salva una hipótesis.

Selecciona dos vías por decisiones que podrían cambiar, factibilidad y divergencia entre rivales. No por el tamaño del efecto que ya viste en un piloto. En los minutos 48–55, fija el control adversarial antes de ejecutarlo: nuevo seed, kernel apartado, demanda permutada, presupuesto igualado o rival analítico. Guarda sus resultados aunque destruyan el hallazgo. Esto es réplica exploratoria tras selección, no confirmación preregistrada.

**STOP:** familia matemáticamente bloqueada; baseline fuerte absorbe la mejora; prueba nueva no identifica su estimando; o coste no permite una comparación válida. **PIVOT:** el resultado señala otra variable manipulable con un mecanismo y un contraste mejores. **CONTINUE:** existe una diferencia interpretable que sobrevive al rival principal y justifica una prueba nueva acotada. No confundir STOP por capacidad/tiempo con refutación científica.

Conserva una lista de configuraciones y endpoints examinados. Diferencias entre queries del mismo mundo no son réplicas independientes; patrones, mundos, semillas de entrenamiento y semillas geométricas son niveles distintos. No multipliques métricas correlacionadas como evidencia. Usa actualizaciones cualitativas donde no exista likelihood defendible; no inventes probabilidades posteriores ni Bayes factors. Separa `belief_revision`, `hypothesis_generation`, `objective_revision` y `decision` en un registro breve. H1–H6 numéricas permanecen intactas en esta hora.

## 8. Entrega: poco relato, evidencia completa

Empieza a guardar evidencia al ejecutar, no al terminar. No dediques más de los cinco minutos finales a ornamentar el informe. Entrega un ZIP que contenga:

1. `RESULTADOS_60_MIN.md`, idealmente 1.500–3.000 palabras: duración real, seis vías consideradas, dos decisiones de profundidad, resultados y límites; qué próxima intervención recomendarías y cuál evitarías.
2. `portfolio.json`: fichas cortas, selecciones, pivotes, costes y estados `DERIVED`, `RUN`, `NOT_RUN_CAPABILITY`, `NOT_RUN_BUDGET`, `INVALID`, `VALID_NULL` o `PROMISING_EXPLORATORY`.
3. Scripts **que efectivamente ejecutaste**, configs resueltas, semillas, versiones mínimas, comandos y logs. Una propuesta no ejecutada se guarda aparte y se etiqueta como tal.
4. Salidas numéricas y datos suficientes para recalcular endpoints, incluidos todos los brazos y controles fallidos. Si se reutilizan archivos previos, conserva su hash/ID y no los cuentes como una nueva corrida.
5. `claims.json`: cada afirmación importante ligada a un archivo/dato o derivación, alcance, confound residual y estatus. Literatura con enlaces y tipo de fuente.
6. `session_clock_trace.jsonl`, `SESSION_FINAL.json` y manifiesto SHA256 de los archivos entregados. Comprueba que el ZIP se puede abrir y que los scripts/resultados mencionados están dentro. El manifiesto puede excluirse a sí mismo; declara esa convención.

Si tu entorno no permite archivos o cómputo, entrega derivaciones comprobables y protocolos cerrados; di claramente qué no ejecutaste. No prometas paneles, redes o tiempos que no puedas transferir. No es necesario llenar seis carpetas: una cartera breve y dos pruebas bien delimitadas bastan. El objetivo de esta hora es abrir opciones y reducir incertidumbre, con libertad para descubrir que nuestra pregunta inicial estaba mal planteada.
