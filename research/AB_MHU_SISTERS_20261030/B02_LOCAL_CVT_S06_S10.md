# Subrama AB — LOCAL, CVT y cobertura

Hereda el prerregistro de 20 hipótesis congelado en commit f2c86270196df6eda87533953cc0169df81ec5a0 y el auditor completo de commit e4a3605e0fad53418d7ca08f187c4d3ce1c440ce (ambos anteriores a ejecutar resultados). Extracto de la auditoría matemática completa; no representa nuevos ciclos adicionales.

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



Las demostraciones son deducciones bajo supuestos, no descubrimientos publicados originales ni réplicas externas. La inferencia específica sobre LARP se limita a los modelos documentados en la rama padre.
