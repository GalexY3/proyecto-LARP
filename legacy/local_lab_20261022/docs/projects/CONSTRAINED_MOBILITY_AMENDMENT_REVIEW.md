# Revisión del suplemento por fallo de escritura

2026-10-09. Rol: arquitecto/revisor. **Dictamen prospectivo: defendible como suplemento exploratorio de dos cadenas no iniciadas**, sujeto a las condiciones siguientes. No se ejecutan propuestas ni se modifica historia con esta revisión.

## Evidencia del incidente

El recibo `v1/search/supervision.json` registra BUG_INVALID, retorno1 y 87,9074383s. `worker_failure.json` sitúa el error WinError5 en `os.replace` al escribir `active_trajectory.json`. En el runner congelado esa escritura ocurre **antes de llamar a run_chain**. El último marcador conservado dice `active=false`, `last_id=g1103_s0_cycle3`; `partial_results.json` identifica diez cadenas completas, cada una con190propuestas, hashes de traza/resultado/etiquetas y PROPOSAL_LIMIT.

No aparecen trazas de g1103/seed1. Estos artefactos sustentan que sus dos trayectorias aún no se iniciaron; verificar su ausencia y los hashes antes del suplemento. El error de escritura no se interpreta como inmovilidad geométrica. El experimento v1 permanece **INVALID_EXPERIMENT**. Las diez cadenas pueden conservar valor diagnóstico individual si pasan auditoría, sin convertir el experimento original incompleto en una corrida completa válida.

## Condiciones para adoptar antes de ejecutar

1. Nuevo ADR, runner/manifiesto y carpeta suplementaria; preservar cápsula, core, config y recibos v1. Adoptar la enmienda antes de lanzar, motivada exclusivamente por el incidente técnico y por completar las dos oportunidades originalmente previstas, independientemente de los resultados de las diez cadenas.
2. Allowlist cerrada: g1103/seed1/cycle3 y después g1103/seed1/swap2, con los mismos namespaces,190propuestas,20s completos, reserva1s, sustrato, centros,130guardas, sampler, float64 y recomputación completa. Comenzar cada una desde nativa. No regenerar ni prolongar las diez anteriores, añadir semillas, recalibrar cap o guardas ni cambiar aceptación.
3. Reparar sólo transporte de estado del supervisor: registros de inicio/fin con nombres únicos y creación exclusiva, inmutables; lectura tolerante a archivo aún incompleto; ninguna sustitución de un archivo que otro proceso mantiene abierto. Probar escritura/supervisión con payloads dummy, no propuestas geométricas nuevas. Sellar diff/hash para acreditar que la ruta matemática y RNG no cambia.
4. Contabilizar el suplemento, imports, cargas y cierre dentro del saldo original. Gasto probado:2,4167939+1,6772587+87,9074383=**92,0014909s**; saldo **267,9985091s**, sin otorgar otro techo360s. Las dos cadenas conservan su máximo40s conjunto; trabajo científico adicional de preparación/cierre también se descuenta. Desarrollo/auditoría se contabilizan aparte como antes.
5. Un solo intento del suplemento. Un nuevo fallo, corte global o cadena incompleta termina esa oportunidad; no reanudarla ni sustituirla. Conservar parciales y estado preciso. Ningún resultado permite abrir adquisición, redes o búsqueda dirigida automáticamente.

## Interpretación del agregado

Clasificar cualquier agregado de doce trayectorias como **AMENDED_EXPLORATORY_OPERATOR_DIAGNOSTIC**, con batch original/suplemento por cadena y enlace al incidente. No llamarlo ejecución confirmatoria original ni réplica independiente. El análisis puede conservar los umbrales operativos fijados, explicitando la enmienda.

Aceptación, Hamming final/máximo y estados por190evaluaciones son comparables si core, RNG e integridad se verifican. La reparación I/O y el batch temporal pueden alterar segundos de escritura y carga: **Hamming final/segundo y el criterio2× quedan descriptivos y afectados por ese confusor**. No corregir tiempos post hoc ni atribuir a operadores una diferencia causada por transporte o batch. Informar también coste de evaluación registrado, sin reemplazar retrospectivamente el endpoint primario.

La auditoría valida lo salvado; no transforma el fallo en evidencia contra MHU ni añade oportunidades de selección. Si ambas alternativas incumplen viabilidad, procede preparar el [borrador de compromisos](LOCAL_SPECTRAL_TRADEOFF_NEXT_DRAFT.md), sin ejecutarlo. No hay actualización arquitectónica automática.
