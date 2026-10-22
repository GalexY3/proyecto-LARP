# Diagnóstico de movilidad bajo restricciones, v1

9 de octubre de 2026. Autorización: el investigador encargó seguir las instrucciones del texto adjunto, que aprueba comparar swaps de dos sitios con ciclos de tres y exige registrar los rechazos. Se permite explorar alternativas justificadas. El texto recibido se conserva íntegro en `artifacts/constrained_mobility/source_user_instructions.txt`; su hash está en la configuración. No se reclama una aprobación de nuevos límites por parte del documento: la asignación concreta siguiente es una decisión prospectiva del laboratorio dentro del encargo.

## Pregunta y alcance

¿Cuál de los dos operadores permite desplazarse bajo las 130 guardas locales v2 sobre los tres sustratos históricos? Se compara un operador junto con su kernel geométrico. No se demuestra conectividad global ni se muestrea uniformemente el espacio factible.

Se preservan X/E, centros, radios físicos por nodo, conteos, seis modos y todas las tolerancias v2, incluida la varianza continua ±5%. Aceptar un candidato si y sólo si pasa las 130 guardas locales, comparadas siempre con la referencia nativa. **No hay objetivo espectral ni recocido en la aceptación.** Una cadena neutral separa movilidad local de dirección espectral; el espectro final y por propuesta es descriptivo. Un control espectral encontrado por azar exigiría recertificación y otro protocolo antes de utilidad.

## Operadores congelados

- `swap2`: subconjunto uniforme de dos tipos distintos, orden aleatorio, nodo ancla uniforme del primer tipo y segundo nodo del otro tipo.
- `cycle3`: subconjunto uniforme de tres tipos distintos, orden aleatorio, ancla uniforme y otros dos nodos de sus tipos. Rotación uniforme ±1 de las tres marcas.
- Kernel común: una elección near/global por propuesta; probabilidad near .8. Near selecciona uniformemente entre los cuatro nodos más próximos al ancla de cada tipo destino; global selecciona uniformemente entre todos sus nodos. Distancias periódicas; desempate por índice estable. Los tipos presentes y el tamaño del movimiento difieren por definición; medir cambios por sitio y distancia de transporte, sin fingir una comparación de alcance idéntico.
- Ciclos conservan conteos globales. No contienen un procedimiento que garantice compensación de cada guarda local. Sus beneficios son una hipótesis, no una propiedad impuesta.

Cada geometría × dos semillas nuevas × dos operadores = doce cadenas. Comienzan en la misma nativa; namespace `[20261009,9924,geometry_seed,seed_index,operator_index]`, sin reutilizar RNG de v2. Orden dentro de cada referencia: seed0 A/B, seed1 B/A. La vecindad dependiente de marcas no autoriza afirmaciones de reversibilidad o equilibrio uniforme.

## Cómputo y puertas

Nuevo presupuesto independiente de **360 s**, que incluye imports, calibración, preparación y ejecución. No es extensión ni transferencia del saldo de v2. Calibración: veinte propuestas descartadas, máximo60 s; preparación: máximo30 s; doce cadenas de máximo20 s, sin reintento o traslado de presupuesto. Desarrollo y auditoría se cuentan aparte.

Se recalculan todas las features de todos los tipos en ambos operadores; misma ruta de evaluación. Calibración alterna operadores y sustratos, near/global según plan fijo, siempre desde nativa. El cap común es `min(500,floor((20−1)/(2·máximo_coste_observado)))`, fijado una vez antes de cadenas. El mínimo informativo operativo es100 propuestas completas por cadena. Es un diagnóstico nuevo: no se traslada el mínimo500/start de la búsqueda v2. Si la calibración no admite100, cerrar por recursos sin modificar el plan. El cap común iguala oportunidades; los límites temporales igualan la asignación máxima, no garantizan gasto real idéntico. Reportar ambos costes y medidas por segundo.

Las puertas exigen tests pertinentes, auditoría del sampler/evaluador, hashes de fuentes y referencias, PID/PPID reales y deadlines enteros. Fallos de infraestructura se conservan como tales, sin reinterpretarlos como inmovilidad. Los estados de calibración no cuentan como cadenas ni evidencia del operador.

## Registro y endpoints

Todas las propuestas, incluso rechazadas: RNG/índice, nodos/marcas, kernel y orientación, hashes antes/candidato/después, las 130 desigualdades con ratios y resultado, IDs/familias fallidas, aceptación, espectro candidato/actual, tiempo y distancia Hamming a nativa. Los rechazos no modifican el estado. Conservar trazas completas y resumen pequeño, sin duplicar arrays descriptivos masivos.

Endpoints principales por cadena: admisibilidad, aceptados, Hamming máximo/final, estados únicos aceptados y distancia por coste. Informar sitios alterados y transporte geométrico. Registrar cofallos; las familias no son causas independientes ni se suman como evidencia. El espectro firmado final respecto de nativa y cambio por coste son secundarios; sin selección del mejor estado por score neuronal.

Viabilidad operativa para una futura búsqueda: al menos cinco aceptados y Hamming máximo≥20 nodos en ambas semillas de al menos dos geometrías. Estos umbrales son criterios de ingeniería prospectivos, no potencia estadística ni prueba de conectividad. Ganancia considerable de B: B viable y Hamming final/segundo≥2 veces A en ambas semillas de al menos dos geometrías. El endpoint final evita recompensar deshacer movimientos; el máximo conserva información sobre estados accesibles visitados. Si A tiene movilidad cero y B positiva, declarar la razón no definida y usar la comparación cualitativa, sin fabricar infinito. Propuestas dentro de una cadena y semillas dentro de una geometría no son réplicas de sustratos independientes.

## Stop / pivot / continue

Si un operador es viable, preparar una búsqueda dirigida nueva, con presupuesto y admisión explícitos; no lanzarla automáticamente. Si ambos fallan, cerrar esta secuencia de buscadores y preparar exploración del compromiso local/espectral. Si hay movilidad pero poco contraste espectral, investigar compatibilidad estructural; la deriva neutral no prueba ausencia de caminos dirigidos. No relajar guardas mirando estos resultados.

La frontera de compromiso queda preparada como propuesta separada: efectos totales y residuales se distinguen; superficies logradas no se denominan frontera Pareto verdadera sin garantías. Encontrar ventaja total y no residual no identifica por sí solo mediación: podrían cambiar estimandos, soportes, potencia y otras propiedades. Sería necesaria una intervención adicional sobre el mecanismo.

H-MOVE1 recibe como máximo actualización ordinal específica del operador+kernel en estas referencias. H1–H6/C/H-R no se actualizan; no hay tareas, adquisición o entrenamiento. Una desviación sugerida por resultados exige hipótesis y datos nuevos, conservando este registro.
