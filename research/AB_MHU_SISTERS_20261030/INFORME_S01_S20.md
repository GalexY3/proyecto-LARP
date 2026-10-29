# LARP · Propiedades matemáticas de MHU, LOCAL, CVT y modelos hermanos

**Fecha de trabajo:** 30 de octubre de 2026. **Método:** AB 3.2.1/O1–O7; lote S01–S20 (20 cuestiones deductivas). **Código prospectivo congelado antes de ejecutar:** `research/AB_MHU_SISTERS_20261030/audit_20.py`, commit `e4a3605e0fad53418d7ca08f187c4d3ce1c440ce`, Git blob `56ec9c33fbb92f09fafac46270c48c1d6a6e7b7d`, SHA256 `78751d1064d5dffcdff06669748be641e9f2a7a70df0410e460a3241ee1c6296`. **Contrato A–J congelado:** commit `f2c86270196df6eda87533953cc0169df81ec5a0`.

**Estado:** 20 preguntas matemáticas examinadas y 20 comprobaciones auxiliares PASS. Ningún chequeo numérico finito demuestra por sí mismo una proposición general; las demostraciones algebraicas son las indicadas abajo. No se ejecutó geometría neuronal nueva, datos multiespectrales, Wei original ni validación externa. Ni la clasificación A–J ni la exactitud matemática convierten un resultado conocido en un descubrimiento 2/3.

## Inventario real de modelos investigados

- **LOCAL original** (LARP Scale3D): minimiza un coste de organización espacial que combina término total y promedio de cinco subpoblaciones, construido en el código mediante densidad CIC, FFT y penalización local suavizada. `spectral=False` quita la penalización adicional baja-k, no convierte el proceso en un CVT auténtico.
- **MHU-v1 original:** mismo coste local y mismo comienzo que LOCAL, más penalización espectral finita baja-k de la unión y cinco tipos. Su validación es FINITA, no hiperuniformidad asintótica.
- **MHU-v2:** altera los pesos del objetivo espectral a proporcionalidad `1/|k|²`, normalizando por separado cada población; no cambia la naturaleza finita de la prueba.
- **SUB-ONLY / JOINT / UNION-ONLY / REPEL:** variantes de proyectos anteriores, sobre todo AB30 DISCOVERY, que separan supresión intratipo, conjunta, solo unión y repulsión local. No son necesariamente implementaciones del optimizador Scale3D original.
- **CVT por tipo:** método de cobertura/cuadratura próximo a Lloyd, un rival convencional competente; depende de cómo se haya refinado y del kernel de reconstrucción. **Retícula**, **Sobol**, **IID** y **Poisson/blue-noise** son otras familias que no deben llamarse MHU.
- **Grafos sobre posiciones:** las topologías kNN, Delaunay y enlaces aprendidos son una DECISIÓN ADICIONAL a la geometría. No atribuir propiedades de un grafo a un patrón de puntos sin fijar el constructor de aristas.

### Convenciones comunes

En el toro plano, para un conjunto de puntos de la especie `c`, `n_c` y frecuencia recíproca entera `k≠0`, defínase `a_c(k)=n_c^{-1} Σ_{x∈X_c} exp(2πi k·x)`, `S_c(k)=n_c |a_c(k)|²` y proporción `f_c=n_c/N`. La amplitud conjunta normalizada por `√N` es `Z(k)=Σ_c √f_c z_c(k)` con `z_c=√n_c a_c`, de modo que `S_total=|Z|²`. Cualquier equivalente con convención fija vale. *Hiperuniformidad estricta* es una propiedad de límite termodinámico, no se deduce de unos pocos modos de un archivo con N finito.

## Rama B01 — Coordinación espectral y cinco especies (S01–S05)

### S01. ¿Qué diferencia matemáticamente LOCAL, MHU-v1 y MHU-v2?

**Resultado:** en el código recuperado, la pérdida es `J_LOCAL=λ L`, `J_MHUv1=λ L+S_w` con `λ=0.15` habitual. Tanto L como S contienen `0.5·(union + mean(types))`. En MHU-v2, cada peso de modo `w(k)` se sustituye por `w(k)/|k|²` y vuelve a normalizarse dentro de cada componente. Para modos con cuadrados de frecuencia `(1,4,9,16)`, el objetivo uniforme les da `(25%,25%,25%,25%)`, mientras que el objetivo inverso al cuadrado da `(70.24%,17.56%,7.80%,4.39%)`. Es un ejemplo de perfil, **no** el espectro real completo del generador 3D.

**Demostración:** sustitución y normalización de pesos positivos; identidad directa del código fuente, no un teorema físico nuevo. **Adversario:** LOCAL puede tener excelentes distancias mínimas sin optimizar explícitamente la energía de los modos escogidos. **J:** distinción entre fines de optimización, no ranking de calidad.

### S02. ¿Cuánta cancelación conjunta permiten las fases relativas?

Para un modo, escribe las contribuciones como `q_c exp(iθ_c)`, `q_c=√f_c·√S_c`. Si sus magnitudes son fijas, el valor máximo de `|Σ q_c exp(iθ_c)|` es `Σq_c` (alinear fases) y el mínimo es `max(0,2 max q_c−Σq_c)` (desigualdad poligonal: si el mayor lado no supera la suma restante, puede cerrarse un polígono). Por tanto el espectro de unión ocupa exactamente el intervalo entre los **cuadrados** de ambos extremos, al permitir variar libremente fases de ese modo.

**Demostración:** desigualdad triangular para cotas; igualdad superior por alineación; igualdad inferior construyendo antiparalelo si domina un segmento, o cerrando un polígono si no. Las traslaciones por especie permiten orientar amplitudes de un modo recíproco en el toro. **Límite:** no se garantiza cancelar SIMULTÁNEAMENTE todos los modos. **J:** las fases son un recurso de optimización real, sin ventaja universal.

### S03. ¿Podemos cancelar todas las parejas de especies sin cancelar cada especie?

Para tres contribuciones complejas `a,b,c`, exigir `a+b=a+c=b+c=0` obliga a `a=b=c=0`, porque `a+b=0` y `a+c=0` implican `b=c=−a` y `b+c=−2a=0`. Esto refuta la existencia de una cancelación exacta en TODAS las uniones de pares de tres especies no nulas en un modo compartido.

**Interpretación:** mantener una unión de cinco impecable no equivale a que todas sus 10 uniones de parejas lo sean. **Límite:** exige las tres parejas de una triple, no solo algunas parejas ni correlaciones promedio. **J:** incompatibilidad combinatoria exacta, sin afirmar que LARP alcance esos límites.

### S04. ¿Qué hace desplazar cada especie independientemente?

Para un modo no nulo `k` y traslaciones uniformes independientes `t_c`, `a_c→a_c exp(2πi k·t_c)`. Se conserva `S_c`, pero para `c≠d` se tiene `E exp(2πi k·(t_c−t_d))=0`. En consecuencia, `E S_total=Σ_c f_c S_c`. El término cruzado desaparece en promedio, pudiendo aumentar el error si las fases originales cancelaban beneficiosamente o reducirlo si se reforzaban.

**Límite:** promedio sobre traslaciones, no resultado determinista para cada movimiento; un modo k=0 no cumple. **J:** conecta directamente con la ablación de fases histórica AB08; no es un nuevo resultado causal neuronal.

### S05. ¿Permiten las proporciones de cinco especies del generador una cancelación exacta?

Con proporciones programadas `(163,85,68,50,34)/400` y factores espectrales por especie iguales `S_c`, las longitudes relativas son `√f_c`. La mayor es `√(163/400)≈0.63836`, menor que la suma de las otras cuatro `≈1.51839`. Por la cota S02 el mínimo conjunto por fases es cero para un modo. **Esto revela compatibilidad algebraica, no demuestra que el generador obtenga tal fase, ni que el valor sea cero en todas las frecuencias.**

**J:** las proporciones desiguales no impiden por sí mismas coordinación espectral fuerte.

## Rama B02 — LOCAL, CVT y cobertura (S06–S10)

### S06. ¿Existe un patrón simultáneamente óptimo para todos los tipos y su unión?

**Sí, bajo presupuestos iguales en un círculo unidimensional.** Si hay `m` clases con `n` puntos cada una, coloca los `mn` puntos de la retícula circular uniforme de paso `1/(mn)` y asigna clases por residuo del índice módulo `m`. Cada clase forma por sí sola una retícula de paso `1/n`. Como un radio de cobertura `r` de n puntos debe cubrir longitud total 1 mediante n arcos de longitud 2r, `r≥1/(2n)`; ambas escalas alcanzan sus respectivas cotas. **Resultado:** un diseño intercalado tiene minimax de cobertura global y de cada tipo simultáneamente. **J:** no hay incompatibilidad inevitable de cobertura en el caso equilibrado 1D.

### S07. ¿Qué cambia con presupuestos de tipos desiguales?

**Existe una obstrucción aritmética.** Si la unión óptima en círculo son N puntos equidistantes, una subespecie de n puntos exactamente equidistantes debe seleccionar puntos a saltos de tamaño `N/n` de la rejilla base; por tanto `N/n` ha de ser un entero. Para N=3 y tipos de tamaños 1 y 2, ninguna pareja de los tres vértices equidistantes es antipodal, así que no pueden ser óptimas a la vez unión y especie de dos puntos. Las cuotas originales con N=400 incluyen 163,85,68,34, que no dividen 400: esa construcción exacta de retícula única no puede cumplir todas las especies a la vez.

**Límite:** es 1D, rejilla óptima y cuotas exactas; NO prohíbe buenos patrones irregulares ni traslada automáticamente una incompatibilidad a 3D. **J:** el desbalance hace relevantes compromisos entre objetivos.

### S08. ¿Qué minimiza exactamente CVT en el círculo 1D?

Sea `g_i` la longitud del intervalo entre dos sensores consecutivos, suma de gaps 1. El error de cuantización cuadrático integrado por distancia al punto más próximo en ese intervalo es `∫_0^{g_i} min(t,g_i−t)² dt=g_i³/12`. Globalmente `E=Σg_i³/12≥1/(12n²)` por convexidad de x³, con igualdad en gaps iguales. Por su parte el máximo hueco/cobertura también se minimiza en gaps iguales. **Así la retícula es óptima a la vez para cobertura y cuantización L2 en 1D homogénea.**

**Límite:** no se deduce optimalidad de CVT en 3D o en problemas funcionales de varias modalidades. Antecedente directo: literatura clásica de centroidal Voronoi y cuantización. **J:** rival fuerte con óptimos exactos bajo hipótesis explícitas.

### S09. ¿Puede una geometría con espectro baja-k perfecto tener huecos peores?

Sí. Para un número par de puntos `n`, construye `x_j=j/n+(-1)^j ε` módulo 1 con `0<ε<1/(2n)`. Los puntos pares e impares forman sendas retículas de tamaño n/2, cuyas amplitudes se anulan en todo modo entero `1≤|k|<n/2`. Pero los huecos alternan entre `1/n−2ε` y `1/n+2ε`: el radio máximo pasa de `1/(2n)` a `1/(2n)+ε`. **Ejemplo verificado:** con ocho puntos y `ε=.017`, primeras tres potencias espectrales cero dentro de precisión flotante, pero radio máximo `.0795` frente a `.0625` de la rejilla original.

**J:** reducir una banda espectral no garantiza mejor cobertura local, incluso sin ruido ni optimizador imperfecto. Este es un contraejemplo formal al uso de S_low como único indicador de cobertura.

### S10. ¿Qué garantía básica ofrece un muestreo IID por especie?

Para n sensores colocados IID uniformemente y una región fija de volumen relativo `v∈[0,1]`, la probabilidad de no encontrar ninguno es `(1−v)^n`. Para `m` especies y `q` consultas/regiones predeterminadas, por unión de eventos adversos, `P(existe región sin algún tipo)≤Σ_c q(1−v)^{n_c}≤mq exp(−n_min v)`. Esto aporta un control probabilístico para disponibilidad de especies, a diferencia de una cobertura minimax determinista.

**Límite:** q regiones fijas antes de observar, no garantiza un continuo infinito de posiciones ni toma en cuenta restricciones repulsivas. **J:** un control IID tiene garantías explícitas, pero no óptimos deterministas.

## Rama B03 — Fourier, ruido y grafos (S11–S15)

### S11. ¿Cuál es el espectro esperado de puntos IID?

Con n puntos IID uniformes sobre el toro, `A(k)=Σ_j exp(2πikx_j)` tiene `E|A|²=Σ_j1+Σ_{i≠j}E exp(ik(x_i−x_j))=n` para k entero distinto de cero. Luego `E S(k)=E|A|²/n=1`. **Consecuencia:** el valor 1 es la referencia de potencia blanca esperada para un conjunto desestructurado, no una cota inferior para todas las geometrías. **J:** confirma el significado de los scores espectrales bajos en LARP.

### S12. ¿Por qué la retícula puede ser simultáneamente excepcional y peligrosa?

Para los n puntos equiespaciados `x_j=j/n`, la suma geométrica cumple `Σ exp(2πik j/n)=0` cuando `n` NO divide k, y n cuando sí. Así, `S(k)=0` en todos los modos no resonantes y `S(k)=n` en los resonantes (la potencia de amplitud media es 1). **En un problema condicionado a frecuencias no resonantes, vence exactamente; para modos resonantes puede producir aliasing máximo.** No existe orden total de calidad sin distribución de frecuencias de la señal.

### S13. ¿Qué mejora pretende conseguir MHU-v2 al ponderar por 1/|k|²?

Para un campo estacionario periódico con modos de Fourier no correlacionados, la varianza del error de la media de muestras es una suma de la forma `R(P)=Σ_{k≠0} V_f(k) |a_P(k)|²`, donde `V_f(k)` es la energía esperada de cada modo. Por tanto, minimizar `Σ|k|^{-2}|a_P(k)|²` se alinea exactamente con una familia cuyo espectro tenga `V_f(k)∝|k|^{-2}` dentro de la banda. La ponderación uniforme de v1 se alinea con espectro plano dentro de banda. **No es una prueba de mejora de v2 sin especificar la señal**.

**Límite:** no confundir el perfil del código con la densidad espectral real de fotos o entradas neuronales; la suma puede requerir normalizaciones distintas por especie y dimensión. **J:** garantía de adecuación a una familia de señales, no de supremacía de v2.

### S14. ¿Cuál es el daño matemático de desplazar sensores aleatoriamente?

Sea `p_j` una nube fija y añade desplazamientos IID `U_j`, con función característica `φ(k)=E exp(2πikU_j)`. Para la amplitud media `a=n^{-1}Σe^{2πik(p_j+U_j)}`, por expansión diagonal/cruzada se demuestra `E|a'|²=|φ|² |a|²+(1−|φ|²)/n`. En convención factor estructura S=n|a|², `E S'=|φ|² S+(1−|φ|²)`. Así aparece un piso de ruido aunque el S original se anule. Ejemplo de dos puntos con desplazamiento ±.12 verifica exactamente ambos lados de la ecuación.

**Límite:** IID de desplazamientos, no errores correlacionados ni cambios de coordenadas globales. **J:** robustez espectral depende del perfil de jitter.

### S15. ¿Determina la geometría el rendimiento de un grafo neuronal?

No sin fijar constructor de aristas. Sobre las mismas cuatro coordenadas circulares puede construirse un camino de cuatro vértices con autovalor de Fiedler del Laplaciano combinatorio `2−√2≈.585786`, o un ciclo de cuatro con Fiedler `2`. Ambos conservan coordenadas, pero alteran las aristas (y el presupuesto de conexiones). **Esto prueba no-identificación entre geometría y capacidad de mezcla del grafo; NO que la segunda arquitectura tenga mejor aprendizaje ni que los FLOPs estén igualados.**

**J:** para comparar LOCAL/MHU como red hay que fijar kNN/Delaunay/routing y coste, no basta con espectro de posiciones.

## Rama B04 — Marcas, presupuesto y objetivos (S16–S20)

### S16. ¿Cuánta heterocoordinación se obtiene gratis de las proporciones?

Si las etiquetas con cuotas fijas `n_c` se permutan uniformemente entre N posiciones, para cualquiera de las aristas fijas entre dos nodos diferentes, `P(mismo tipo)=Σn_c(n_c−1)/[N(N−1)]`. Por tanto, `P(tipo distinto)=1−Σn_c(n_c−1)/[N(N−1)]`. Para cuotas `(163,85,68,50,34)` el nulo exacto es **0.7388847118** o **73.89%** aristas heterotípicas. Una medición del 85% no debe interpretarse como organización extraordinaria sin descontar que el nulo ya alcanza 74%; tampoco podemos atribuir el residuo al mecanismo MHU sin controlar el grafo.

**Límite:** aristas fijadas previamente y etiquetas aleatorias sin alterar posiciones; con dependencias por posición cambia el nulo. **J:** baseline combinatorio adecuado para LOCAL y otras variantes.

### S17. ¿Puede un patrón unido con S(k)=0 seguir teniendo especies mal distribuidas?

Para N puntos fijos con fases complejas `z_i` de módulo 1 y una especie de n puntos elegidos sin reemplazo, la esperanza exacta del factor de estructura de la especie es `E S_tipo=(N−n)/(N−1)+[(n−1)/(N−1)] S_union`. Se deduce expandiendo los productos y usando probabilidad de inclusión `n(n−1)/(N(N−1))` para cada par distinto. Incluso cuando `S_union=0`, queda **(N−n)/(N−1)>0** si n<N. Ejemplo N=4, n=2, unión cuadrada con S_total=0: `E S_tipo=2/3`.

**J:** imponer espectro bajo únicamente a la unión NO garantiza multihiperuniformidad marcada; las clases deben organizarse también. Relación matemática con S02–S04 y con el experimento `UNION-ONLY`.

### S18. ¿Qué podemos afirmar, de verdad, al añadir un término espectral a LOCAL?

Sea `x_L` un **mínimo global** de `L(x)` y `x_J` un **mínimo global** de `J(x)=λ L(x)+S(x)` con λ>0 en el mismo dominio de geometrías admisibles. De `L(x_L)≤L(x_J)` y `J(x_J)≤J(x_L)` resulta `S(x_J)≤S(x_L)−λ[L(x_J)−L(x_L)]≤S(x_L)`. **Teorema:** frente al mínimo global de LOCAL, el óptimo conjunto no puede mejorar L, pero sí tiene que mejorar/no empeorar S. Es un compromiso de optimización, no una contradicción.

**Límite fundamental:** Adam/L-BFGS-B en un paisaje no convexo NO garantiza mínimos globales, y el término λ local y el conjunto factible tienen que ser idénticos. Esto explica por qué resultados locales empíricos pueden violar un orden que se esperaba de los óptimos matemáticos. **J:** separar comparación de objetivos vs comparación de salidas de algoritmo.

### S19. ¿Qué tipo protege más el objetivo de Scale3D?

El código aplica `mean(types)` con el mismo coeficiente para los cinco tipos, aunque `n_c` y sus cortes espectrales son diferentes. Frente a un promedio ponderado por cuota de especie `Σf_c S_c`, el peso de un coste individual de especie es `1/5` y su peso proporcional por población sería f_c. El cociente relativo entre la clase de 34 sensores y la de 163 es `(163/34)≈4.7941`. **Es la prioridad relativa de los TÉRMINOS agregados POR TIPO, no 4.79 veces la derivada por sensor ni una ganancia neuronal demostrada.**

**J:** posible sesgo normativo arquitectónico a favor de especies escasas, útil en problemas que exigen presencia de todas las modalidades; perjudicial si el coste real crece con el número de sensores.

### S20. ¿Qué estabilidad espectral garantiza desplazar poco cada punto?

Si cada punto cambia a lo sumo una distancia δ, para un modo k, `|e^{2πik·(p+Δ)}−e^{2πik·p}|≤2π||k||δ`. Promediando, `|a'_k−a_k|≤b=2π||k||δ`. Como `|a_k|≤1`, el cambio de potencia normalizada satisface `||a'_k|²−|a_k|²|≤2b+b²`. Así las frecuencias bajas son relativamente más estables frente a perturbaciones pequeñas, mientras que la cota crece con frecuencia. No es una garantía de desempeño downstream ni evita efectos de aliasing.

**J:** existe una garantía analítica local de estabilidad del score, condicionada a error posicional pequeño.

## Integración, priors, controles adversariales y madurez

1. **MHU puede adquirir una ventaja exclusiva SOLO al definir un entorno funcional**: distribución espectral de las señales, covarianza entre modalidades y tipo de error. La cancelación de fases S02–S05 da grados de libertad, no una ventaja media obligatoria (S04).
2. **LOCAL/CVT tienen fundamentos fuertes de cobertura** S06/S08; S09 demuestra que espectro finito casi perfecto puede tener huecos peores. Los resultados históricos favorables a CVT no contradicen MHU, porque optimizan objetivos diferentes.
3. **El ruido importa**: S14 muestra un piso espectral de jitter y los resultados anteriores de fallos de sensores no pueden transferirse automáticamente entre mecanismos de daño.
4. **Las cuotas importan**: S07 y S19 señalan limitaciones reales de equilibrio cuando las cinco proporciones son distintas; S16 y S17 proporcionan nulos exactos antes de explicar la heterocoordinación por geometría.
5. **No existe nueva prueba de originalidad 2/3**. La base técnica combina Fourier, desigualdades poligonales, diseño óptimo 1D, cuantización, combinatoria sin reemplazo y propiedades de mínimos ponderados, con claros antecedentes. Algunas cuestiones son corolarios o versiones relacionadas. La clasificación de 20 cuestiones examinadas no equivale a 20 teoremas científicamente originales ni a 20 validaciones independientes.
6. **Auditoría interna:** fuente Python íntegra congelada en GitHub antes de ejecutar; `20/20 PASS` (ejemplos simbólicos o finitos), `checks_20.json` SHA256 `87a9e4d1fe9b3964aa13156376e3f47e9b0ef81c16c7a959392c1a4caa5e689e`. La auditoría verifica instancias/identidades concretas, no es un asistente de pruebas formal. El juicio general se sostiene en las demostraciones escritas. `CLEAN_CLONE_NOT_VERIFIED` (no se han descargado desde un clon privado limpio para replicación). No hay datos nuevos ni prueba neuronal.
7. **CT2:** trayectoria precedente VISION=11/100 y nueva rama matemática condicionada=24/100, valor inicial de la rama anterior formal; tras este lote conservamos **24/100**, porque no aparece un mecanismo nuevo con confirmación externa ni primacía sobre Wei/CVT. CT2 es ordinal, no probabilidad. 0 nuevos 1/3 no duplicados, 0 de nivel 2/3 y 0 de 3/3. Ningún resultado se agregará al inventario de 1/3 como original salvo auditoría de novedad adicional.

## AB-DECIDE y contabilidad

**20/20 preguntas matemáticas examinadas, 20/20 verificaciones auxiliares superadas**. En tanto que ciclos AB deductivos terminados con contrato individual A–J, se consume el cupo de 20 preguntas formales; **nuevos hallazgos originales cero**. No ha habido branching adaptativo entre las 20 verificaciones (el lote entero quedó congelado antes de ver resultados). Se han desarrollado cuatro subramas temáticas distintas para los modelos hermanos, pero no se han fusionado a main. Resultado: **STOP** respecto a proclamar superioridad universal; **BRANCH** hacia objetivos de diseño espectral-cobertura con restricciones explícitas; **PIVOT condicionado** a selección de distribución según densidad espectral observada y modalidades ópticas reales, con competidores originales Wei 2010 y CVT/farthest-first.

### Prior art y documentación primaria

- Generadores LARP originales: `GalexY3/proyecto-LARP/src/BR30_dynamic/original/scale3d_geometry.py` y `_v2.py`; informes `docs/00_DICTAMEN.md`, `docs/06_BR12_DICTAMEN.md`, `docs/AB08_CROSSPHASE_20261022/DICTAMEN_AB08.md`, `research/AB30_INTENSIVE_20261022/reports/DICTAMEN.md`, `research/AB30_DISCOVERY_20261022/reports/DICTAMEN.md`.
- Jiao et al. (2014), *Avian photoreceptor patterns...*, https://doi.org/10.1103/PhysRevE.89.022721.
- Lomba et al. (2020), *Minimal statistical-mechanical model for multihyperuniform patterns*, https://doi.org/10.1103/PhysRevE.102.012134.
- Wei (2010), *Multi-Class Blue Noise Sampling*, https://www.liyiwei.org/papers/noise-sig10/.
- Torquato (2016), *Hyperuniformity and its generalizations*, https://doi.org/10.1103/PhysRevE.94.022122.
- Du, Faber & Gunzburger (1999), *Centroidal Voronoi Tessellations: Applications and Algorithms*, https://doi.org/10.1137/S0036144599352836.
- Christogeorgos et al. (2024), *Computational model generating multihyperuniform antenna arrays and metasurfaces*, https://doi.org/10.1051/epjam/2024003.

**Siguiente objetivo lógico:** diseño robusto `min_P max_{C∈C_admisible} Tr(K(P) C)` sujeto a cobertura por especie y presupuesto de posiciones y cómputo, contra diseño convencional con el mismo conjunto de restricciones. Esa propuesta es diseño, NO un resultado ejecutado en este lote.