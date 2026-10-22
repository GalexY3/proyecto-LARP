# Fase 3: autorización, hipótesis y alcance

La aprobación del usuario autoriza ejecutar **cuatro corridas, como máximo120 segundos y umbral .98 sin cambios**. La intervención es la política de construir el conjunto de entrenamiento; modelo, encoder sin coordenadas, grafo, puertos, target b0, optimizador, B4, T16, 250 updates e inicializaciones permanecen iguales. Se crea una serie nueva; los resultados previos son inmutables.

## Validación común sin fuga

La factibilidad requiere cuatro anchors compartidos: dos triples y sus intercambios de fuentes. Garantizan exposición de las cuatro fuentes en ambos roles en ambos paneles. Los otros ocho contextos se seleccionan uniformemente o mediante un objetivo de cobertura fijado, sin consultar logits, pérdidas ni accuracy. Por tanto, el control se denomina **uniforme condicionado**, no doce muestras IID globales.

La validación usa cuatro destinos nuevos comunes a SS y UU, fuera de los destinos de entrenamiento. SS contiene combinaciones nuevas de fuentes expuestas en el mismo rol en ambos paneles; UU contiene fuentes reservadas que no participan como puertos activos en ningún entrenamiento. Cada contexto enumera los cuatro patrones, con target externo b0. No se reutilizan triples exactos de train como validación. Los cuatro destinos antiguos20/21/26/61 y la fuente11 quedan fuera de la validación nueva, evitando elegir la evaluación por el fallo conocido.

Se fija la primera construcción geométricamente factible, preservando rechazos. Si no existe bajo los criterios, registrar DIAGNOSTIC_UNAVAILABLE; no relajar restricciones tras observar resultados. El matching de hops es grueso: en esta rejilla todos los candidatos tienen perfil(2,2). No existe garantía de igualar distancia, número de caminos de dos pasos ni grados. Se publican esas distribuciones; la comparación identifica el paquete curricular para este panel, no una mediación exclusiva por cobertura marginal.

## H-R1, H-R2 y H-R3

No había definiciones registradas con estos nombres. Se operacionalizan antes de entrenar en `configs/role_coverage_hypotheses_v1.json`:

- **H-R1:** cobertura insuficiente de fuentes/roles/contextos limita transferencia. Una mejora UU≥10 puntos en ambas seeds, con train/SS≥.98 del panel equilibrado, aporta apoyo débil.
- **H-R2:** nueva combinación de fuentes expuestas se resuelve, pero fuentes reservadas no. SS aprobado y UU fallido en ambas seeds del panel equilibrado aporta apoyo débil; la geometría residual impide atribuir una causa única.
- **H-R3:** el régimen actual no consigue selección reproducible incluso en combinaciones nuevas de fuentes expuestas. Un fallo SS del candidato aporta apoyo débil, distinguiendo inestabilidad de una seed de fallo concordante en dos. No implica incapacidad intrínseca ni localiza por sí solo arquitectura frente a interfaz.

Los priors son ordinales subjetivos moderados, marginales y no excluyentes. Se actualizan ordinalmente con un único paquete correlacionado de resultados. No se fabrican probabilidades posteriores ni Bayes factors; cuatro corridas no representan cuatro geometrías ni cuatro currículos independientes. Falta de recursos, datos inválidos o corridas incompletas no aportan evidencia para actualizar.

**BALANCED es el candidato primario fijado antes de scores**. Su puerta exige ambas inicializaciones finitas y train/SS/UU finales≥.98. Se muestran también todas las corridas UNIFORM; no se selecciona posteriormente el panel ganador. Si la puerta falla, esta intervención se cierra y el trabajo vuelve al diagnóstico de arquitectura e interfaz. No se prolonga entrenamiento, no se cambia una seed y no se abre XOR, remoto o MHU durante estas cuatro corridas.

## Línea espectral independiente

En esta fase no se construye ni evalúa un nuevo control MHU. La futura prueba debe igualar cobertura, separación homotípica, vacíos y otras estadísticas locales fijadas, variando la supresión espectral. Su factibilidad, matching, semillas, presupuesto y criterios necesitan su propio preregistro. La selección será geométrica, nunca por MSE neuronal o de reconstrucción.

H1–H6 y C conservan sus registros anteriores. Las observaciones de generalización de roles no son evidencia causal sobre MHU. Se conservarán las referencias y hashes de los ledgers de arquitectura para verificar que no cambiaron.
