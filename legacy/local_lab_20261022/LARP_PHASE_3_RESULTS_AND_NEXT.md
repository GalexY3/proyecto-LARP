# LARP: resultado de la fase 3 y siguiente decisión

Fecha: 8 de octubre de 2026. Estado: **cuatro corridas terminadas; puerta primaria BALANCED aprobada; sin extensiones**. El protocolo, los paneles y H-R1–H-R3 quedaron registrados antes de optimizar. El resultado corresponde a selección de `b0` en Grid local con una segunda fuente distractora. XOR, MHU y remoto no se ejecutaron.

## Resultado y alcance de la puerta

Las cuatro corridas completaron exactamente 250 updates, sin divergencia ni reintentos. El proceso completo consumió **38,912 segundos**, incluyendo Python/imports, frente al límite externo de 120 segundos. El temporizador interno registró 37,036 segundos; no se confunden ambos tiempos. RSS máximo muestreado: 428.290.048 bytes. El modelo conserva 12.481 parámetros, GRU compartida de 32 dimensiones, T16, B4, AdamW .003 y encoder con coordenadas absolutas anuladas.

| Panel | Semilla | Train: 48 casos | SS: 16 casos | UU: 16 casos | AUX antiguo: 16 casos |
|---|---:|---:|---:|---:|---:|
| UNIFORM condicionado | 2101 | 93,75% | 93,75% | 87,50% | 87,50% |
| BALANCED | 2101 | **100%** | **100%** | **100%** | 100% |
| BALANCED | 2102 | **100%** | **100%** | **100%** | 87,50% |
| UNIFORM condicionado | 2102 | 75,00% | 62,50% | 56,25% | 68,75% |

La puerta registrada exige train, SS y UU finales ≥98% en las dos semillas del candidato BALANCED, fijado antes de resultados. Por granularidad exige 48/48, 16/16 y 16/16. **BALANCED la supera; UNIFORM no.** No se eligió el mejor checkpoint, panel o semilla después de observar scores.

AUX se congeló como medición secundaria de los cuatro contextos antiguos, conocida y fuera de puerta/H-R. Su fallo merece conservarse: BALANCED2102 responde siempre cero en `[query=61, source0=62, source1=60]`, acertando 2/4 patrones. Los destinos antiguos 20, 21 y 26 sí pasan en ambas semillas. Ningún puerto activo de los cuatro contextos antiguos participó en entrenamiento BALANCED. El éxito nuevo **no establece selección universal ni resuelve el smoke original de XOR**. Tampoco se convierte retrospectivamente AUX en una puerta distinta de la aprobada.

## Qué cambió realmente

La intervención principal es construir el currículo. Se conservan X, arcos, distancias, puertos, arquitectura, inicialización por semilla, optimizer, calendario 250×4 y presupuesto. Ambos paneles contienen cuatro anclajes comunes —dos triples y sus intercambios de roles— más ocho extras. Se seleccionó la primera construcción geométricamente factible: intento índice 14, la 15.ª propuesta, con rechazos preservados y cero consulta a resultados neuronales.

Los cuatro destinos comunes de validación son `[30,48,29,9]`. SS utiliza las cuatro fuentes de anclaje, activadas en ambos roles en ambos entrenamientos. UU utiliza fuentes reservadas, excluidas de todos los roles activos de entrenamiento; sus neuronas y caminos siguen presentes en la misma Grid. Las queries de validación no se usaron como queries de entrenamiento. Cada triple enumera los cuatro patrones binarios completos.

**Restricción de novedad SS:** los cuatro triples son nuevos, pero tres reutilizan una pareja ordenada de fuentes que ya apareció en los anclajes, con otro destino. Sólo `[query29, source19, source39]` recombina una pareja inédita; ese contexto también alcanza 4/4 en ambas semillas BALANCED. El protocolo congeló ausencia de triples exactos y queries retenidas, no ausencia de todas las parejas de fuentes. SS acredita principalmente transferencia a queries/contextos nuevos y una única recombinación limpia; no cuatro recombinaciones independientes. La redacción amplia de «combinaciones nuevas» en H-R2/H-R3 debe leerse con esta limitación. Se conserva el gate y la actualización registrados, sin endurecerlos ni cambiarlos después de los scores.

UNIFORM es **uniforme condicionado**: ocho extras sin reemplazo después de reservar anclajes/validación; no doce muestras IID globales. BALANCED minimiza lexicográficamente exposición por fuente/rol al cuadrado, desequilibrio entre roles y repetición de firmas geométricas. El primer objetivo empata:

| Estadística del currículo | UNIFORM | BALANCED |
|---|---:|---:|
| Fuentes distintas por rol | 12 / 12 | 12 / 12 |
| Fuentes físicas distintas en total | 19 | 12 |
| Queries distintas | 9 | 7 |
| Objetivo: exposición / desequilibrio / repetición | 24 / 14 / 24 | 24 / 0 / 14 |

Por tanto, describir la mejora como «más cobertura» sería impreciso. El tratamiento combina balance entre roles, diversidad de firmas, selección de contextos y menor diversidad de fuentes/queries. La diferencia también aparece en train: no identifica un mecanismo exclusivo de transferencia. Con los mismos recursos, este paquete favorece aprendizaje y transferencia en el panel congelado; no demuestra cuál de sus propiedades es necesaria.

SS y UU consultan los mismos destinos y tienen hops ordenados `(2,2)`. Persisten diferencias en distancias, multiplicidad de caminos y grados de salida. Se publican esas distribuciones. Dos inicializaciones de una única Grid y un único par de currículos no son réplicas de geometría o de política de muestreo.

## Evidencia mecanística y actualización separada

En BALANCED, train/SS/UU tienen fracción de cambios de clase por flip `[fuente0=1, fuente1=0]` en ambas semillas. Es selección binaria correcta dentro de esas enumeraciones. Flips y accuracy provienen de los mismos cuatro patrones; no se multiplican como evidencias independientes. La pérdida SS/UU es aproximadamente 0,000077/0,000071 en 2101 y 0,001625/0,001710 en 2102.

El contraejemplo antiguo limita interpretar los Jacobianos como mecanismo suficiente. En 2102, el contexto61 mantiene logits entre −5,65 y −5,54; voltear fuente0 cambia sólo 0,017–0,109 el logit y ninguna clase, aunque sus derivadas locales no son cero. Una sensibilidad diferencial grande en algún punto no acredita selección ante el cambio binario completo. No se ejecutaron nuevas intervenciones ni forwards para producir esta lectura: se tabularon medidas guardadas dentro del presupuesto.

Las reglas ordinales registradas producen:

| Hipótesis diagnóstica | Actualización de este paquete |
|---|---|
| **H-R1:** soporte de fuentes/roles/contextos insuficiente limita el régimen | **Apoyo débil**: UU mejora 12,5 y 43,75 puntos; BALANCED train/SS pasa en ambas semillas. El mediador específico sigue sin identificar. |
| **H-R2:** transferencia depende de fuentes expuestas aunque SS se resuelva | **Contraevidencia débil**: BALANCED también resuelve el UU nuevo en ambas semillas. AUX impide extrapolarlo a todos los contextos reservados. |
| **H-R3:** el régimen falla reproduciblemente incluso en combinaciones nuevas de fuentes expuestas | **Contraevidencia débil**: SS y train pasan en ambas semillas. Esto tiene el alcance estrecho preregistrado. |

Los tres priors de trabajo eran ordinales moderados, marginales y solapados. No se asignaron probabilidades posteriores ni Bayes factors. **H1–H6 y C permanecen intactos**, comprobado contra sus bytes anteriores al entrenamiento y su contenido en Git. Esta fase no compara MHU causalmente.

## Siguiente decisión recomendada

La fase termina aquí con PASS local y un fallo auxiliar explícito. No se añaden corridas, epochs, cambios de núcleo o pruebas XOR en esta intervención.

La siguiente pregunta neuronal debe separar el efecto del **balance de roles** del resto del paquete antes de modificar la recurrencia otra vez. Recomendación concreta para un protocolo futuro: mantener la misma lista de contextos físicos `(query,{sourceA,sourceB})`, los conteos totales por fuente/query y las firmas geométricas sin orden; variar únicamente la orientación fuente→rol entre una asignación equilibrada y otra desequilibrada. Conservar cuartetos, calendario, parámetros y dos inicializaciones comunes, con máximo cuatro corridas, 120 segundos y umbral del 98%. Así, la cantidad de fuentes y el soporte físico dejan de cambiar con el tratamiento. Su validación debe incluir contextos nuevos fijados sin scores y conservar el caso61 como desafío conocido, identificado como tal. Si se denomina a SS «recombinación de fuentes», exigir además parejas de fuentes inéditas; comprobar su factibilidad geométrica antes de optimizar, sin sustituir esa exigencia por queries nuevas tras ver resultados. Se requiere un preregistro propio: **esta comparación no está implementada ni ejecutada**.

Antes de adoptar un núcleo para cómputo multicomponente habrá que resolver el smoke XOR local y remoto con criterios registrados y un panel más amplio. El fallo auxiliar hace prematuro declarar una regla general. El presente éxito permite investigar el currículo con el núcleo intacto; no abre el piloto histórico.

La línea MHU permanece independiente: primero comprobar factibilidad de controles que igualen cobertura local, separación homotípica y vacíos mientras difieren en supresión espectral. La propuesta concreta está en [INDEPENDENT_SPECTRAL_MATCHING_NEXT.md](C:/Programación/LARP/docs/INDEPENDENT_SPECTRAL_MATCHING_NEXT.md), **NOT_RUN**. Recomienda marcas funcionales sobre X/grafo/radios físicos fijos, tolerancias por componente y selección del primer control admitido sin consultar MSE. Si el matching y la manipulación no son simultáneamente factibles, el resultado es no identificación; no se relajan tolerancias según rendimiento. Esta comparación se refiere inicialmente a adquisición y no sustituye una comparación neuronal causal.

## Registro y verificación

Protocolo y resultados: [PHASE_3_ROLE_COVERAGE.md](C:/Programación/LARP/docs/PHASE_3_ROLE_COVERAGE.md). Datos: [results.json](C:/Programación/LARP/artifacts/role_coverage/v1/results.json). Hipótesis: [H_R_ordinal_updates.json](C:/Programación/LARP/artifacts/role_coverage/v1/H_R_ordinal_updates.json). Identidad congelada: `60b883ddaf3f5c99d26f73f89003a766397b0607e9be74d89dc26f451f38ae8f`.

Auditoría independiente anterior: 24 comprobaciones aprobadas antes de optimizar; posterior: 13 comprobaciones aprobadas, con reconstrucción de accuracy/puertas y verificación de checkpoints. Suite global: **232 PASS en 8,98 segundos**, sin sobrescribir las tandas históricas. Procedencia global: **16 manifests, 139 hashes de archivos congelados y 27 archivos científicos originales intactos**, en [provenance_audit_v3.json](C:/Programación/LARP/artifacts/next_phase/provenance_audit_v3.json).

Se conserva una advertencia técnica sin cambiar el código congelado: el resumen superior `COMPLETE` es demasiado permisivo ante algunos estados de fallo. La inferencia usa exclusivamente los cuatro estados individuales COMPLETE, finitos y de 250 updates, como exigen las puertas/H-R; los cuatro cumplen en esta ejecución. Los checkpoints grandes permanecen locales, con hashes en los resultados. No se abrió test, no hubo CUDA ni escalado y no se sustituyeron resultados desfavorables.
