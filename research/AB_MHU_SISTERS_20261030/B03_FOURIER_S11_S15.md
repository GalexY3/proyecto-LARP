# Subrama AB — Muestreo, aliasing, jitter y grafos

Hereda el prerregistro de 20 hipótesis congelado en commit f2c86270196df6eda87533953cc0169df81ec5a0 y el auditor completo de commit e4a3605e0fad53418d7ca08f187c4d3ce1c440ce (ambos anteriores a ejecutar resultados). Extracto de la auditoría matemática completa; no representa nuevos ciclos adicionales.

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



Las demostraciones son deducciones bajo supuestos, no descubrimientos publicados originales ni réplicas externas. La inferencia específica sobre LARP se limita a los modelos documentados en la rama padre.
