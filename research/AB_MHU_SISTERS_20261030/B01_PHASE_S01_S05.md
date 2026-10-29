# Subrama AB — MHU y coordinación espectral

Hereda el prerregistro de 20 hipótesis congelado en commit f2c86270196df6eda87533953cc0169df81ec5a0 y el auditor completo de commit e4a3605e0fad53418d7ca08f187c4d3ce1c440ce (ambos anteriores a ejecutar resultados). Extracto de la auditoría matemática completa; no representa nuevos ciclos adicionales.

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



Las demostraciones son deducciones bajo supuestos, no descubrimientos publicados originales ni réplicas externas. La inferencia específica sobre LARP se limita a los modelos documentados en la rama padre.
