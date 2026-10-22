# Otra formulación del bloqueo: exclusión y reconfiguración

9 de octubre de 2026. Nota exploratoria, no experimento ni descubrimiento confirmado.

Una parte de las guardas se puede describir exactamente sin lenguaje de hiperuniformidad. Para el tipo c, sea m_c el mínimo NN homotípico nativo y a_c=L/√n_c. La guarda de déficit mínimo exige que ningún par de posiciones marcado c esté a distancia menor que r_c=m_c−.05a_c. Construir un grafo G_c con aristas entre posiciones a distancia<r_c: los sitios de cada tipo deben formar un conjunto independiente de su grafo. Los cinco grafos comparten sitios y tienen umbrales diferentes; además, cada sitio recibe una sola marca y cada tipo conserva n_c sitios.

Esta equivalencia sólo representa la guarda de mínimo NN. CDF de NN, cobertura, pares, varianza y mezcla de arcos añaden restricciones. No identifica el conjunto factible completo ni demuestra que esté desconectado. La nativa demuestra que existe una asignación válida; lo abierto es acceder a otras suficientemente diferentes y espectralmente contrastantes.

## Antecedentes cercanos

La reconfiguración de coloraciones válidas mediante cambios locales tiene una literatura extensa. [Feghali, Johnson y Paulusma, European Journal of Combinatorics59, 2017](https://www.sciencedirect.com/science/article/pii/S0195669816300488), artículo revisado por pares, estudia equivalencia mediante cambios de Kempe en grafos cúbicos. Sus garantías no se transfieren a estos grafos de exclusión ni a nuestras guardas.

[Fuchs et al., ISAAC2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ISAAC.2025.33), publicación en actas de congreso revisado por pares, estudia reconfiguración mediante intercambio de colores en vértices adyacentes manteniendo coloración válida. [arXiv2511.06473](https://arxiv.org/abs/2511.06473) es la versión preprint del mismo trabajo; no es otra réplica. Es un antecedente cercano del problema de acceso entre asignaciones con conteos conservados, aunque nuestro kernel no exige adyacencia en un único grafo común y usa restricciones dependientes del tipo. Su clasificación de complejidad no demuestra dificultad formal de LARP.

## Consecuencia para decisiones futuras

No sería original afirmar que movimientos pequeños pueden quedar atrapados entre asignaciones válidas. La aportación potencial estaría en caracterizar las restricciones geométricas concretas y su relación con adquisición, no en renombrar reconfiguración de colores.

Si el diagnóstico señala exclusión como bloqueo frecuente, usar la formulación de cinco grafos para obtener cotas o certificados de subproblemas antes de inventar otro kernel. Un cambio de Kempe ordinario puede modificar conteos de tipos; incluso uno balanceado no garantiza nuestras otras guardas ni la validez con umbrales distintos. No se propone ejecutarlo como tercer optimizador automático. Una exploración de compromisos local/espectral sigue siendo una línea diferente, con nuevo estimando y comparación de utilidad posterior.

La equivalencia de la guarda con grafos es derivación propia elemental; los antecedentes son publicaciones existentes. No se reclama prioridad ni se actualizan hipótesis neuronales.
