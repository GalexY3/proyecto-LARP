# Subrama AB — Etiquetas, cuotas, objetivos

Hereda el prerregistro de 20 hipótesis congelado en commit f2c86270196df6eda87533953cc0169df81ec5a0 y el auditor completo de commit e4a3605e0fad53418d7ca08f187c4d3ce1c440ce (ambos anteriores a ejecutar resultados). Extracto de la auditoría matemática completa; no representa nuevos ciclos adicionales.

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



Las demostraciones son deducciones bajo supuestos, no descubrimientos publicados originales ni réplicas externas. La inferencia específica sobre LARP se limita a los modelos documentados en la rama padre.
