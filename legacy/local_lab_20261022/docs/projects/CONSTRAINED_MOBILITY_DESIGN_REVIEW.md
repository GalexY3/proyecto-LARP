# Constrained Mobility Diagnostics — revisión prospectiva

Fecha: 2026-10-09. Rol: arquitecto/revisor. **Recomendación de diseño; no se han ejecutado calibraciones, propuestas ni cadenas.** Este documento es nuevo y no modifica protocolos, configuraciones, resultados o hashes históricos. Se han leído AGENTS.md, la carta AB 2.1, el adjunto de evaluación v2, `configs/spectral_matching_v2.json`, la decisión v2 y su informe de cierre.

## Recomendación concreta

Abrir un único diagnóstico exploratorio de **swaps de dos sitios frente a ciclos de tres sitios con etiquetas distintas**, partiendo siempre de la referencia nativa. Usar las tres geometrías históricas g1101/g1102/g1103, dos semillas nuevas por geometría y operador: doce cadenas. No aumentar el techo global de **360 s**, no cambiar ninguna de las **130 guardas locales**, no incorporar campos, decoders, tareas o redes. Las etiquetas continúan siendo funciones y los radios físicos permanecen ligados a sus nodos.

La nueva pregunta es: **¿un ciclo de tres etiquetas permite desplazarse dentro de la región localmente admisible con más eficiencia que un swap, bajo estos kernels y este presupuesto?** Su alcance es movilidad alcanzable desde estas referencias. No es una prueba de conectividad global ni de existencia o inexistencia del control espectral v2.

La aceptación debe ser neutral: **aceptar si y sólo si las 130 guardas locales pasan respecto de la nativa congelada**. No recocido, temperatura, energía ni espectro en la decisión de aceptación. Evaluar la propuesta completa y directa; un ciclo no requiere que sus posibles descomposiciones en swaps sean admisibles. Las propuestas descartadas no alteran el estado. Todas las cadenas comienzan con el mismo hash nativo de su geometría.

## Preservación y cambios explícitos

Conservar X, orden de nodos, E dirigido, puertos, distancias, radios, conteos, los 10.000 centros y su namespace, los bins, las escalas por tipo, la precisión float64 y todos los denominadores y tolerancias v2. En particular, conservar la varianza continua por intersecciones de discos a ±5% para cada tipo en R1,25/R2,5. No sustituirla por Monte Carlo o Fourier truncado.

Las 130 restricciones son: cinco tipos × 21 restricciones por tipo, más 25 celdas dirigidas de arcos. En cada tipo: 4 cobertura, 6 ventanas incluida varianza, 5 vecinos homotípicos, 5 bins físicos y 1 outdegree. Guardar identificadores estables que distingan tipo, radio, cuantil, bin y tipo destino.

El mínimo histórico de 500 propuestas/start y el máximo de seis starts pertenecen a la **búsqueda espectral v2**, ya cerrada. Doce cadenas de ≤20 s son una **reasignación prospectiva para otra pregunta**, adoptada explícitamente por la raíz de la tarea dentro de la autorización vigente. Con el máximo coste v2 de 0,0488032 s, la fórmula conservadora sólo permitiría aproximadamente 194 propuestas en 20 s. La nueva regla es **mínimo100 y máximo500 propuestas completas por cadena**, sin alegar potencia estadística ni garantía de ver movilidad rara. El presupuesto sobrante de v2 no se transfiere a este diagnóstico: dispone de su propio techo global360s.

El suelo espectral .25 y los seis modos de v2 se mantienen como **referencias descriptivas**, no como guardas de movilidad. El contraste .50+varianza±5% sigue excluido en estas referencias; no se reabre. La historia v2 conserva NOT_IDENTIFIED.

## Kernel y comparación

Congelar el kernel completo antes de medir resultados. Una opción sencilla conserva el estilo de propuesta v2:

- Swap: par no ordenado de tipos uniforme entre los diez, orientación fuente/destino equiprobable, primer sitio uniforme entre el tipo fuente; destino con mezcla 80% entre los cuatro sitios más próximos del tipo destino y 20% uniforme global. Distancia toroidal y desempate por índice, como v2.
- Ciclo: triple no ordenado de tipos uniforme entre los diez; orden de los tres tipos uniforme entre las seis permutaciones. Elegir un ancla uniforme del primer tipo. Elegir los otros dos sitios, de sus tipos respectivos, con la misma rama near/global sorteada una vez por propuesta: near usa los cuatro sitios más próximos al ancla de cada tipo; global usa selección uniforme por tipo. Aplicar una de las dos orientaciones del ciclo con probabilidad1/2.
- Comprobar tres índices diferentes y tres etiquetas diferentes. Los conteos se conservan exactamente y todos los dos/tres sitios cambian. No denominar «compensación» a una conservación de guardas no comprobada: el ciclo propone una compensación posible y el verificador decide.

Este kernel mantiene conjuntos de tipos y la mezcla espacial comparables, pero tiene vecindarios dependientes de las etiquetas. **No se asume reversibilidad ni distribución estacionaria uniforme**. Las dos orientaciones del ciclo no bastan para demostrar esas propiedades. La comparación caracteriza operador+kernel. Si el objetivo futuro requiere muestreo uniforme o conectividad matemática, hará falta un kernel simétrico o un ajuste Hastings y un protocolo distinto. No añadirlo después de ver qué operador gana.

Los ciclos alteran tres sitios y los swaps dos; la comparación por aceptación cruda puede favorecer movimientos de distinta amplitud. Publicar también costes y resultados por sitio alterado. Reportar near/global separadamente; no confundir que un kernel alcanza más distancia física con una ventaja universal del operador.

## Calibración y límites

Usar veinte mediciones de propuestas descartadas, diez por operador, sin cambiar nunca el estado nativo. Plan prefijado: para k=0..9, medir ambos operadores sobre geometría k módulo3; ocho parejas near y dos global, fijando global en k=4,9. Tipos, sitios y orientaciones se resuelven con el namespace de calibración congelado. La comprobación de identidad y del supervisor se hace antes; no cuenta como éxito ni se recicla como dato de movilidad.

Cada medición incluye propuesta, las 130 guardas completas, las métricas espectrales descriptivas que se registrarán y el coste de escritura correspondiente. No aprovechar la calibración para seleccionar tipos, kernel, geometrías, tolerancias o semillas favorables. Se usa únicamente para resolver el cap y verificar implementación.

Techos recomendados: preparación≤30 s; calibración≤60 s; doce cadenas≤20 s cada una; reservar≤30 s para reconstrucciones finales y escritura. **360 s globales absolutos domina todos los techos**, incluye imports, cargas, calibración, propuestas, métricas y escrituras científicas. Desarrollo y auditoría independiente se contabilizan aparte. Sin reintentos, sin transferencia de tiempo sobrante, sin seeds adicionales y sin ampliación tras ver resultados.

Resolver un cap común por operador y geometría:

`C = min(500, floor((20 - 1)/(2 * max_coste_de_propuesta_de_ambos_operadores)))`

con reserva fija1s por cadena y un factor conservador2 sobre el máximo coste observado en ambos operadores. Si C<100 o no cabe el plan completo con sus reservas, cerrar preparación como RESOURCE_LIMIT; no rebajar el mínimo después de ver movilidad. Verificar antes de congelar que la reserva y el cierre global cubren reconstrucciones finales/escrituras. Congelar C, runtime, código, config, entradas, centros, arcos y seeds antes de las cadenas. Las calibraciones permiten estimar coste, no garantizan que todas las cadenas lleguen al cap: conservar cualquier corte y emparejar por propuestas completadas al comparar admisibilidad.

Namespace adoptado en la decisión prospectiva: búsqueda `[20261009, 9924, geometry_seed, seed_index, operator_index]`; calibración en otro namespace. Verificar ausencia de colisión con artefactos anteriores antes de congelar. Emparejar los dos operadores por geometría y réplica; esto es emparejamiento del diseño, no promesa de números aleatorios comunes equivalentes. Orden prefijado dentro de cada referencia: seed0 A/B, seed1 B/A, para reducir confusión por deriva de coste.

## Registro mínimo que hace informativo el fracaso

Por cada propuesta, aceptada o rechazada, guardar: cadena y ordinal; operador; near/global; índices y etiquetas antes/después; tiempo completo; hash del estado previo y del candidato; las **130 razones normalizadas**, sus valores/tolerancias y flags; número de fallos; decisión y hash posterior. Evaluar todas las restricciones sin detenerse en el primer fallo. Un JSONL comprimible y acotado basta; no hace falta infraestructura nueva compleja.

Cada rechazo puede incumplir varias guardas. Publicar frecuencia marginal por guarda y familia, frecuencia de guarda que falla sola y coocurrencias; **no sumar los porcentajes marginales como si fueran categorías excluyentes**. Distinguir «se incumplió en la propuesta» de «es un obstáculo causal necesario»: el ranking de rechazos no demuestra que retirar una guarda habilitaría el objetivo espectral.

Métricas por cadena y agregadas primero por geometría:

1. Propuestas completas y fracción localmente admisible, con near/global separado.
2. Sitios aceptados acumulados, distancia Hamming final y máxima desde la nativa, sitios distintos tocados y hashes no nativos distintos. Los sitios aceptados acumulados cuentan también movimientos que luego se deshacen; por eso no sustituyen al desplazamiento ni a los estados únicos.
3. **Hamming final desde la nativa por segundo de coste completo** como eficiencia primaria del desplazamiento; estados únicos por segundo y por evaluación; sitios aceptados por segundo y por sitio propuesto. Registrar también distancias físicas de las propuestas para interpretar alcance espacial. El máximo Hamming es una puerta de alcance adicional, no sustituye a la distancia final en la comparación de eficiencia.
4. Por tipo, los seis S, sus medias y mínimos; medias y mínimos finales con **cambios firmados** desde nativa, por coste. Medir B/U y varianza en los dos radios, usando las definiciones históricas, para que la compensación fuera de banda siga visible. Conservar máximas como diagnóstico secundario sin usarlas para escoger el ganador.

El endpoint primario es admisibilidad+exploración; el cambio espectral es secundario descriptivo. No seleccionar el mejor estado como control ni detener una cadena por una excursión espectral favorable. Las máximas deben identificarse como máximas sobre oportunidades registradas. No sumar tipos, modos o métricas correlacionadas como evidencia independiente. Las tres geometrías son los tres bloques históricos; dos RNG por bloque no crean seis nuevas geometrías. No usar intervalos binomiales ingenuos ni p-values por propuesta: las cadenas son dependientes y pequeñas.

## Puertas, interpretación y siguiente decisión

**Integridad:** cualquier fallo de conteos, radios, hashes, identidad, equivalencia incremental/completa, registro de130guardas o supervisor invalida la parte afectada. Corregir software sin convertir el fallo en evidencia de restricciones geométricas. Toda cadena termina con reconstrucción completa; comparar guardas y espectro con su último registro. Si aparece por casualidad un candidato que satisface también v2, conservarlo como hallazgo exploratorio para auditoría, sin abrir automáticamente rendimiento.

**Stop por diseño:** terminar al cap común, al techo por cadena o al global; no prolongar por falta de éxitos. El plan no pretende alcanzar mezcla ni equilibrar una cadena. Un diagnóstico terminado puede ser informativo aunque no produzca un control.

**Regla operativa de avance adoptada, declarada como juicio de ingeniería:** un operador es viable si consigue **≥5 movimientos aceptados y máximo Hamming≥20 sitios (.05N)** en ambas réplicas de al menos dos de tres geometrías. Considerar la ganancia de ciclos considerable únicamente si ciclos es viable y su distancia Hamming final por segundo es **≥2×** la de swaps en ambas réplicas de al menos dos geometrías. Si swaps tiene distancia final cero, informar diferencia absoluta y ratio indefinido; exigir desplazamiento final positivo de ciclos y su puerta de viabilidad, sin fabricar un factor infinito como efecto estimado. Estas cifras son puertas de decisión transparentes, no umbrales de significación. Registrar near/global y composición por tipo para delimitar cualquier dependencia del kernel.

**Si ambos incumplen la puerta de viabilidad**, cerrar este diagnóstico y preparar una estrategia de compromisos local/espectral en estado **DRAFT**, sin ejecutarla. Puede incluir caracterización de restricciones, fronteras o cotas del conjunto factible y distinguir las guardas necesarias para adquisición de las relevantes para redes. No encadenar otros optimizadores ni retirar guardas sin nueva pregunta y presupuesto.

**Si hay exploración pero poco cambio espectral**, registrar que los caminos visitados no aportaron contraste dentro del coste; no declarar incompatibilidad. Puede justificar una futura prueba estructural de compensación B/U o una frontera de compromisos, pero esa revisión del estimando se registra por separado.

**Si sólo cambia una geometría o una semilla**, resultado dependiente del punto de partida/azar e INCONCLUSIVE para ventaja general del operador. Conservarlo como OBSERVED, auditarlo y proponer nueva réplica sin reutilizar este resultado como confirmación.

## Registro AB y valor esperado

- `belief_revision`: ninguna actualización arquitectónica ni de utilidad MHU. El resultado futuro sólo podrá actualizar movilidad bajo estos kernels y guardas; la ausencia de movimientos no prueba conjunto factible vacío.
- `hypothesis_generation`: H-MOVE1 procede de v2 y del adjunto; los nuevos RNG aportan nuevas trayectorias sobre sustratos históricos, una prueba prospectiva del diagnóstico pero exploratoria para generalización geométrica.
- `objective_revision`: ninguna en esta fase. Una frontera local/espectral es una alternativa que requiere ficha y decisión nueva; no sustituye silenciosamente el contraste causal existente.
- `decision`: ensayo único con límites congelados y registro de rechazos completos. Información esperada alta sobre el bloqueo, coste bajo y reutilización directa de las guardas; novedad científica/publicabilidad **no evaluada por literatura nueva**. Esta revisión no reclama originalidad del uso de ciclos.

**Innovación provisional1/3:** diagnóstico metodológico útil y trazable; la novedad de operadores no se ha establecido y todavía no existen datos del diagnóstico. Una mejora robusta o una estructura repetida de bloqueos podría justificar2/3 después de auditoría y antecedentes;3/3 requeriría una contribución nueva, general y confirmada. La escala es ordinal para comunicar prioridad, no una medida probabilística. Un recreo posterior permanece voluntario, pequeño y aislado en `sols_corner/`; este documento no lo inicia ni consume presupuesto de búsqueda.

Fuentes locales principales: [carta AB2.1](../charter/LARP_RESEARCH_CHARTER_AB_2_1.md), [decisión v2](../decisions/ADR_2026_10_09_SPECTRAL_LOCAL_VARIANCE_V2.md), [revisión causal v2](SPECTRAL_MATCHING_V2_DECISION_REVIEW.md), [config v2](../../configs/spectral_matching_v2.json) y [cierre v2](../../LARP_SPECTRAL_FEASIBILITY_V2_RESULTS.md). Las recomendaciones, kernels y puertas operativas anteriores son propuestas propias, no resultados ejecutados ni hechos de literatura.
