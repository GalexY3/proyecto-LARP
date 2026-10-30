# H04 — Sensibilidad post hoc al grado de conectividad (NO nuevo ciclo)

**Estado:** análisis exploratorio posterior al resultado H04; no estaba preregistrado como endpoint y NO cuenta como ciclo AB adicional. Único supuesto: seis o más vecinos distintos elegidos uniformemente sin reemplazo entre los otros 399 nodos de cuotas n=(163,85,68,50,34), condicionando el tipo focal; no aplica a la topología real kNN, a routing aprendido o a redes dirigidas con grados distintos.

Mediante la misma fórmula exacta de inclusión-exclusión de H04, usando denominador `binom(399,d)` y promedio por clase focal, se obtienen:

| Vecinos d | P(tener al menos uno de los cinco tipos) |
|---:|---:|
| 5 | 1,9246 % |
| 6 | 5,7738 % |
| 8 | 17,0115 % |
| 10 | 29,8580 % |
| 12 | 42,1590 % |
| 15 | 57,7704 % |
| 20 | 75,6527 % |
| 30 | 91,9220 % |
| 40 | 97,2518 % |
| 50 | 99,0553 % |

Primer grado d que supera umbral: **50 % en d=14**, **90 % en d=29**, **95 % en d=35**, **99 % en d=50**.

Esto NO recomienda usar 50 enlaces ni demuestra que las cinco modalidades sean necesarias. Es una advertencia: si se persigue cobertura completa de roles, el cableado aleatorio con d=6 es un adversario débil; un diseño con etiquetas podría garantizar presencia de las cinco clases usando cinco enlaces por nodo, a costa de controlar cargas y rutas. La comparación justa debe contabilizar el grado de entrada, los grados de salida, el coste de selección y la distancia de enlaces. Este análisis no añade N1 ni cambia CT2.
