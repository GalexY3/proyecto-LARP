# Orientación de roles con soporte físico fijo — propuesta de fase 4

**Estado: DRAFT / NOT_RUN. Fecha: 2026-10-08.** Propuesta para revisión humana; no es un preregistro congelado ni autorización de entrenamiento. No se han creado modelos, hecho forwards, abierto optimizadores o producido resultados de aprendizaje para esta propuesta. No adopta otra fase ni modifica puertas, priors, H1–H6, C o artefactos históricos.

## Pregunta y motivo

¿Cambiar la orientación fuente→rol, conservando exactamente las exposiciones físicas, cambia el aprendizaje de selección local b0 y su transferencia bajo el presupuesto vigente?

[Los resultados de fase 3](../../LARP_PHASE_3_RESULTS_AND_NEXT.md) motivan la pregunta: BALANCED pasó su puerta y UNIFORM condicionado falló, pero también cambiaban fuentes, queries, contextos y motivos. BALANCED no tenía más cobertura física. El fallo conocido de query61 impide declarar selección universal. Esta hipótesis nace después de esos resultados; la fase 3 no la confirma independientemente.

Rige [AB 2.1](../charter/LARP_RESEARCH_CHARTER_AB_2_1.md), conforme a AGENTS.md. El [manifest histórico](../../artifacts/role_coverage/v1/preregistration.json) se usa como fuente de contextos, calendario y geometría, sin modificarlo. Se recomienda una intervención mínima factible, con controles adicionales de motivos y grados. Su factor identificado sería la **asignación de orientación**, que incluye el soporte fuente×rol y la diversidad de contextos marcados; no un efecto aislado del escalar de desequilibrio.

## Restricciones y comprobación efectuada

Se ejecutaron cuatro comprobaciones pequeñas, de sólo lectura, con el Python existente y opción -B. Se reutilizaron Geometry.load, graph_context, geometry_features y funciones de hash existentes; no se llamó a prepare, execute, predictions, measure ni a un modelo u optimizador. No se guardaron nuevos artefactos de cálculo. Los temporizadores internos, iniciados antes de los imports de NumPy/Torch/LARP, registraron **16,563 + 1,610 + 1,669 + 1,653 = 21,494 s**. Es la suma medida de esas comprobaciones, inferior al máximo de 60 s; no es el coste de un futuro entrenamiento ni una medición externa continua. Esta auditoría de preparación no es auditoría independiente de aprendizaje.

Resultados geométricos reales:

- Grid N400/g1101, puertos y arcos conservan los hashes del manifest histórico. Hay **2.086 triples ordenados / 1.043 contextos físicos**, todos con hops ordenados (2,2).
- El currículo BALANCED tiene **12 slots**, **7 contextos físicos únicos**, **6 parejas físicas de fuentes**, **12 fuentes distintas** y **7 queries distintas**. Cada fuente aparece en dos slots.
- Restringir SS a las cuatro fuentes de anclaje sólo permite **una pareja inédita**, {19,39}, en query29, con las exclusiones históricas. Cuatro recombinaciones no son factibles con ese soporte; cambiar sólo queries no resuelve esta limitación.
- Con las doce fuentes BALANCED aparecen **9 contextos SS elegibles / 9 queries / 7 parejas inéditas**, al retener queries de entrenamiento y excluir los destinos antiguos 20/21/26/61 y fuente11 de la validación nueva.
- Se enumeraron las **4.096 orientaciones** de los doce slots. Para I = Σfuente(n0−n1)², el rango es 0–48 y hay 64 asignaciones con I=0. Mantener todas las fuentes en ambos roles fuerza I=0: con exposición total dos, cualquier desequilibrio elimina un rol para alguna fuente.
- Igualar además el histograma histórico de motivos **ordenados** deja 256 asignaciones, con I∈{0,8,16}. Igualar también los histogramas de outdegree por rol deja 128, con I∈{0,8}. Estos conteos son factibilidad, no evidencia de utilidad de la intervención.

La última comprobación aprobó once invariantes: admisibilidad de todos los triples propuestos, conteos físicos por fuente y query iguales, cuatro parejas SS distintas e inéditas, queries SS retenidas, fuentes SS en ambos roles en ambos brazos, U excluido de todos los roles activos de train y de las queries de validación, queries/hops comunes SS–UU y hashes geométricos históricos iguales. No se comprobaron inputs neuronales mediante forwards ni resultados futuros.

La raíz reconstruyó independientemente la matriz B/D8 y los paneles publicados debajo: igualdad del multiset físico y del histograma de firmas ordenadas, I=0/8, 12/11 triples orientados únicos, admisibilidad, parejas SS inéditas, soporte común en ambos roles y exclusiones U. Estas comprobaciones pasaron sin modelo ni optimizador; el proceso de revisión duró 2,005 s según la herramienta. No se repitió la enumeración exhaustiva ni se suman ambas revisiones como evidencia de aprendizaje.

## Opciones analizadas y recomendación

| Opción | Ventaja | Límite / decisión propuesta |
|---|---|---|
| Reorientar UNIFORM histórico | Conserva su lista física entre brazos | Sus fuentes con exposición total uno no admiten balance exacto; no es una comparación equilibrado/desequilibrado equivalente. No recomendar ahora. |
| BALANCED físico, I=0 frente a I=48 | Contraste máximo de soporte por rol | Todas las fuentes pierden un rol; cambian motivos ordenados y grados por rol. No recomendar como primera prueba. |
| BALANCED físico, I=0 frente a I=16 | Más fuentes sesgadas; motivos ordenados iguales | Cambia el histograma de grados por rol. Mantener como alternativa declarada, no ejecutar junto a la opción principal. |
| **BALANCED físico, I=0 frente a I=8** | Igualdad física, de motivos ordenados y de grados por rol | Sólo se sesgan dos fuentes en un slot. **Recomendación inicial.** |
| Nuevo esqueleto con exposición ≥4 por fuente | Puede comparar 2/2 frente a 3/1 conservando ambos roles | Cambia el protocolo y sus totales respecto del histórico; factibilidad no comprobada. Requiere otro diseño, presupuesto y validación previos. |

La opción recomendada copia como **B** la orientación BALANCED histórica. **D8** cambia únicamente el último slot de (77,86,68) a (77,68,86). No deduplicar ni reordenar slots tras asignar orientación:

| Slot, índice 0 | Query | Pareja física sin orden | B: fuente0, fuente1 | D8: fuente0, fuente1 |
|---:|---:|---|---|---|
| 0 | 18 | {8,19} | 19,8 | 19,8 |
| 1 | 18 | {8,19} | 8,19 | 8,19 |
| 2 | 40 | {39,49} | 49,39 | 49,39 |
| 3 | 40 | {39,49} | 39,49 | 39,49 |
| 4 | 3 | {4,13} | 4,13 | 4,13 |
| 5 | 14 | {4,13} | 13,4 | 13,4 |
| 6 | 36 | {35,46} | 35,46 | 35,46 |
| 7 | 36 | {35,46} | 46,35 | 46,35 |
| 8 | 68 | {57,69} | 57,69 | 57,69 |
| 9 | 68 | {57,69} | 69,57 | 69,57 |
| 10 | 77 | {68,86} | 68,86 | 68,86 |
| 11 | 77 | {68,86} | 86,68 | **68,86** |

El multiset físico de doce slots es idéntico, incluidos sus duplicados, con la misma multiplicidad por fuente/query y los mismos motivos sin orden. En query77 ambas fuentes tienen motivo (hop=2, paths2=1, r²=8) y outdegree8; el intercambio conserva también esos resúmenes ordenados, incluso al ponderar por calendario.

B tiene **12 triples orientados únicos / 48 ejemplos marcados únicos**; D8 tiene **11 / 44**, aunque ambos contienen 12 slots / 48 casos. En D8 el triple (77,68,86) se repite: es parte de la intervención de orientación, no un error a eliminar. Un guard antiguo que exigiera doce triples orientados distintos sería incompatible con este diseño y no debe aplicarse silenciosamente ni modificarse retrospectivamente.

Nominalmente, todas las fuentes B tienen 1/1 exposiciones por rol. D8 cambia 68 a 2/0 y 86 a 0/2; las otras diez permanecen 1/1. El primer objetivo histórico Σfuente,rol n² cambia 24→28. Esto es **información y soporte de orientación**, no más cobertura física.

El calendario histórico es de cuartetos completos. Cada slot recibe 20 o 21 visitas, por lo que B no es exactamente equilibrado en las exposiciones realizadas: I ponderado por visitas es 4 en ambos calendarios. D8 da I=3.364. Para 68/86, B tiene 21/20 y 20/21 con calendario2101, y 20/21 y 21/20 con calendario2102; D8 tiene 41/0 y 0/41 en ambos. Estas cifras cuentan visitas de cuarteto; multiplicarlas por cuatro da apariciones en casos y multiplica I por dieciséis. Los conteos físicos ponderados siguen iguales entre brazos. No llamar al 1/1 nominal balance exacto de updates.

## Validación común propuesta

Definición SS principal: cada fuente apareció **en ambos roles en ambos brazos**, query no usada como query de train, y pareja **sin orden inédita** en todo train. Se aplica una definición única mediante la intersección de soporte de B y D8. Esa intersección contiene diez fuentes; excluye 68/86. El panel propuesto tiene cuatro parejas diferentes, no cuatro variaciones de una pareja.

| Query común | SS: query, fuente0, fuente1 | Pareja SS inédita | UU: query, fuente0, fuente1 |
|---:|---|---|---|
| 24 | (24,13,35) | {13,35} | (24,23,25) |
| 46 | (46,35,57) | {35,57} | (46,45,56) |
| 47 | (47,46,57) | {46,57} | (47,37,48) |
| 59 | (59,49,69) | {49,69} | (59,48,50) |

UU se tomó como la primera pareja física lexicográfica admisible por query, excluyendo todos los puertos activos de train, las cuatro queries de validación y fuente11. U={23,25,37,45,48,50,56}. Sus neuronas y caminos permanecen en la misma Grid: no son neuronas nuevas. Las queries de validación están retenidas en su función de query, pero query46 sí apareció como fuente de train; no hay holdout de todos los roles activos para las queries SS.

Cada triple enumera 00/01/10/11: 16 casos SS y 16 UU comunes. Hops SS–UU coinciden exactamente (2,2), pero no todas las otras propiedades. Las firmas (paths2_0,paths2_1;r0²,r1²) de SS son (1,1;8,8), (1,1;8,8), (2,2;4,4), (1,1;4,4); las de UU son (1,2;4,4), (1,1;4,4), (1,1;4,4), (1,2;8,4). Los grados por rol SS son (8,7),(7,8),(7,8),(6,4), frente a (4,7),(4,6),(4,7),(7,5) en UU. SS–UU no aísla causalmente novedad de fuentes. La comparación B–D8 utiliza exactamente esos mismos paneles y conserva estas diferencias entre estratos.

Alternativa secundaria analizada, **no añadida al panel principal**: (58,68,57) y (79,68,69) son parejas inéditas admisibles, con fuentes vistas en el rol evaluado en ambos brazos. Incluirlas permitiría evaluar una fuente manipulada, pero 68 no fue visto en ambos roles en D8. Requeriría otro estrato y definición prospectiva; no mezclarlo silenciosamente con SS principal. El SS principal prueba recombinación entre fuentes con soporte común completo; no prueba directamente transferencia de los dos puertos sesgados.

Conservar AUX_OLD con los cuatro contextos conocidos de fase 3, incluido **(61,62,60)** y sus cuatro bits, midiendo sólo al final. Ningún puerto de ese contexto61 se activa en B/D8 train. AUX es conocido, no ciego, y debe reportarse por contexto, con su soporte; no selecciona pesos ni corridas. Los paneles nuevos son nuevos respecto del train propuesto, sin garantía de novedad respecto de todo el historial del laboratorio.

## Ejecución y lectura futuras, pendientes de decisión

Proponer **dos inicializaciones nuevas 2103/2104**, comunes entre B y D8, sin usar checkpoints entrenados. Reutilizar, respectivamente, los calendarios históricos identificados como 2101/2102, declarando esa asociación antes de resultados. Propuesta de orden: D8/2103, B/2103, B/2104, D8/2104. Semillas, asignación, orden y paneles siguen siendo borradores, no están congelados.

Mantener GGNNLikeModel/COORDS_OFF en todos los nodos, 12.481 parámetros, d32, T16, B4, 250 updates por corrida, AdamW .003, betas(.9,.999), eps1e−8, weight_decay1e−4, clip1, CPU4 y float32. Máximo **cuatro corridas y 120 s globales**, desde entrada del comando, incluidos imports, preparación, verificaciones y todas las medidas. La configuración/código históricos no se editarían: una implementación nueva debe declarar el protocolo propio y reutilizar componentes existentes. No construir infraestructura en esta propuesta.

Los cuartetos aseguran iguales distribuciones de bits físicos y etiquetas por slot, pero intercambiar roles cambia cuál fuente determina la etiqueta en los patrones mixtos. El calendario empareja slots físicos y cuartetos; no implica igualdad caso por caso de inputs marcados o targets. Verificar ese contrato al construir los datos.

Puerta técnica propuesta: B fijado como candidato primario; **ambas inicializaciones COMPLETE, finitas, exactamente 250 updates y accuracy final train/SS/UU≥98%**. Con 48/16/16 casos exige 48/48, 16/16 y 16/16, contando los slots repetidos de D8 de forma explícita. Reportar además la misma puerta para D8 y diferencias B−D8 por inicialización; nunca elegir el ganador después de scores. Una diferencia SS/UU≥0,10 en ambos pares puede proponerse como señal exploratoria direccional, sin fabricar probabilidades o Bayes factors. BCE y resultados por contexto son diagnósticos secundarios; flips derivados de los mismos cuartetos no son evidencia independiente.

Si B y D8 pasan al techo, el contraste queda sin discriminación bajo este presupuesto. Si D8 falla también en train, el efecto concierne al aprendizaje/optimización y no sólo a transferencia. Si las semillas discrepan, registrar inestabilidad. Una diferencia coherente identifica el efecto de esta orientación concreta, no una ley general de balance. Cuatro contextos SS son cuatro contextos, no dieciséis réplicas independientes; dos inicializaciones no replican geometría ni selección de currículo.

**XOR no se abriría automáticamente al pasar la puerta técnica.** Si se pretende usar la fase como requisito para proponer una ampliación XOR, recomendar prospectivamente exigir además AUX_OLD≥98% en ambas inicializaciones B, con caso61≥98% explícito. Es una condición de robustez conocida y redundante dentro de AUX, no confirmación ciega ni suficiencia universal. Un eventual XOR local/remoto requiere decisión humana, preregistro y sus propias puertas amplias; nunca endurecer la puerta histórica de fase 3 con esta condición.

## Stop y condiciones previas

Antes de cualquier entrenamiento deben existir: decisión humana sobre este contraste y sus límites; protocolo nuevo registrado antes de resultados; validación independiente de slots, soporte SS común, novedad de parejas y exclusiones U; hashes propios de geometría/datos/código/runtime/calendario/pesos iniciales; declaración de conteos nominales y ponderados; y un deadline externo efectivo de 120 s. Revisar que ninguna ruta ejecuta el manifest de fase 3 como si fuese la fase nueva. No utilizar un resumen global COMPLETE sin comprobar los cuatro estados individuales, finitud, updates y paneles finales.

Detener preparación ante inviabilidad, alteración de identidad, deduplicación accidental, mezcla de definiciones SS o incumplimiento de matching. Registrar DIAGNOSTIC_UNAVAILABLE / INVALID_EXPERIMENT según corresponda, sin optimizar. Durante una eventual ejecución, agotamiento, fallo numérico o medida primaria ausente producen RESOURCE_LIMIT / NUMERICAL_FAILURE / INCOMPLETE y conservan parciales/NOT_RUN; no autorizar reintentos, nuevas semillas, extra updates o extensión. Si B no supera su puerta, cerrar esta intervención dentro del presupuesto; no rescatarla por AUX, otra orientación o el mejor checkpoint.

No actualizar priors históricos a partir de factibilidad. Separar los registros futuros de revisión de creencias, generación de hipótesis y decisión; no hay revisión de objetivos en este borrador. Falta literatura específica antes de reclamar novedad o escalar recursos.

## Prioridad en la cartera, sin cambio de objetivos

La ganancia de información esperada es moderada y diagnóstica: el contraste elimina cambios de soporte físico y de varios resúmenes geométricos, aunque no separa exposición por rol de diversidad de contextos marcados. La importancia científica es instrumental para disponer de un núcleo fiable; no estima utilidad MHU. La confianza de replicación permanece baja hasta ejecutar datos nuevos; el sustrato y el esqueleto siguen siendo únicos. La factibilidad geométrica está comprobada y la construcción de inputs aún pendiente. El coste propuesto es pequeño y acotado a cuatro corridas/120 s; los 38,912 s de fase 3 son una referencia histórica, no una medición del futuro ensayo. La representación por slots físicos podría reutilizarse en otras tareas, sin justificar nueva infraestructura por ahora. Novedad tras revisión de literatura: **no evaluada**; no se propone una contribución inédita ni encaje TFM.

Esta preparación no sustituye la línea `MHU_SPECTRAL_CAUSALITY`: igualar cobertura local, separación homotípica y vacíos mientras cambia la supresión espectral sigue siendo la próxima prueba específicamente pertinente a MHU. Su factibilidad y presupuesto tienen protocolo independiente; no deben quedar bloqueados por el ensayo neuronal ni mezclarse con sus cuatro corridas. No se ha ejecutado esa línea durante este turno.

Si la pregunta exige **desequilibrio sin perder ningún rol por fuente**, este soporte de dos exposiciones es algebraicamente insuficiente. Un protocolo futuro tendría que aumentar/reasignar exposiciones hasta al menos cuatro por fuente —por ejemplo 2/2 frente a 3/1—, diseñar nuevos slots físicos comunes y reservar de nuevo cuatro parejas SS inéditas y U. Ello cambia los conteos respecto del histórico y requiere comprobar geometría, calendario y presupuesto antes de congelar. No presentar ese diseño no comprobado como factible ni relajar novedad SS a queries nuevas.

**Resultado de este trabajo: propuesta geométricamente factible, DRAFT / NOT_RUN; ningún resultado de entrenamiento y ninguna nueva fase adoptada.**
