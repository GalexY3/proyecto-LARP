# PRIORS DELTA — LARP Routing AB30
Fecha 2026-10-30. No sustituir priors históricos.
- P-ROUTE-01 [local synthetic]: seleccionar rutas por tipo mejora el MHU espectral finito frente al vecindario puramente local en 24/30 condiciones; alta frecuencia contradice la generalización. Esta ganancia es parcialmente tautológica bajo una tarea que exige recuperar modalidades ausentes.
- P-ROUTE-02 [adverse]: el rival CVT tipo-condicionado supera a MHU tipo-condicionado en 30/30 condiciones de este generador, con Q de cuantización menor. No refuta geometría aviar original (no ejecutada).
- P-ROUTE-03 [invalid comparator]: mhu_type y mhu_hybrid forman exactamente el mismo grafo, por lo que no son rivales independientes; no repetir ni puntuar el híbrido.
- P-ROUTE-04 [method limitation]: una red regular aleatorizada de 6 circulantes no constituye automáticamente un expansor; no confundir pobre rendimiento local con derrota de un rival expander real.
- P-ROUTE-05 [need real evidence]: código ejecutado y exactamente reproducible; 30 condiciones relacionadas del mismo generador sintético, sin entrenamiento, fuentes externas, paridad de distancias o réplica independiente. Fuente nativa original MHU ausente.
- H-conditional: como el error se rige por cuántas modalidades llegan y a qué distancia espacial, hay un compromiso coverage×proximity; no existe ventaja automática de energía Fourier si la tarea penaliza distancia a la observación.
- N1_unique_new=0; N2=0; N3=0. CT2 condicionado previo 24/100 sin subida; escala ordinal sin validación.
- R5 STOP_LOCAL, sólo PIVOT a fuentes externas y grafos aprendidos con rivales reales.
