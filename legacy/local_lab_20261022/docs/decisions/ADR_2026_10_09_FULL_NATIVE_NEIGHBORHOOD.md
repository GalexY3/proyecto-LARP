# Auditoría exhaustiva del vecindario nativo, v1

2026-10-09. Decisión prospectiva bajo AB 2.1 y autorización del usuario: «Sigue. Y luego siguiente fase de exploración. Puedes usar mi pc para automatizar procesos». Padre: 4f2f9a1. No altera Constrained Mobility ni spectral v2.

## Pregunta y estimando

En cada g1101/g1102/g1103, enumerar todos los swaps entre dos tipos y ciclos orientados de tres tipos distintos que satisfacen las cinco guardas de mínimo homotípico en el estado NATIVO. El censo anterior cuenta 24/53/34 swaps y 13/10/2 ciclos: 136 candidatos. Comprobar en cada uno las 130 desigualdades históricas, sin cambiar tolerancias, radios, centros, arcos ni etiquetas físicas por nodo. Las marcas funcionales se transportan; los radios físicos no.

Este es un cálculo determinista sobre datos ya examinados, no una réplica empírica. El grafo D es necesario y suficiente para la familia MIN en estos movimientos (cada tipo pierde e incorpora un solo nodo). Un ciclo i→j→k→i se materializa trasladando esas tres marcas en esa dirección; rotaciones equivalentes se cuentan una vez, ambas orientaciones por separado.

## Endpoints y discriminación

Publicar todos los candidatos, todas las 130 restricciones, hashes de etiquetas, fallos por familia y diagnóstico espectral. Sumar exactamente con fracciones la masa de cada movimiento aceptable bajo el kernel histórico: swap global 1/(10 n_a n_b), near suma sobre anclas válidas de 1/(80 n_ancla); ciclo global 1/(20 n_a n_b n_c), near suma sobre tres anclas cuyos otros dos nodos están entre los cuatro vecinos respectivos de 1/(960 n_ancla). Mezcla 4/5 near + 1/5 global. Esto es una probabilidad de propuesta condicional al estado nativo, no likelihood de MHU ni probabilidad de éxito de una cadena que cambia de estado.

Comprobar las primeras aceptaciones históricas desde nativo contra la lista exhaustiva. Sabemos por esos datos que existe al menos un swap completo por sustrato; contradicción implica fallo de auditoría/software. Cero ciclos completos demuestra aislamiento nativo para ESTE operador y restricciones, no imposibilidad de controles espectrales, conectividad global, ausencia de ciclos mayores o inutilidad de MHU. Una masa positiva distingue rareza de ausencia; tampoco garantiza desplazamiento sostenido.

## Recursos e integridad

Una ejecución, presupuesto global 60 s desde entrada del supervisor, incluye importaciones, preparación, evaluación y escritura. Sin calibración, búsqueda, reintentos ni ampliaciones. Supervisor stdlib usa CPython real, handshake PID/PPID, deadline absoluto entero, archivos exclusivos cerrados y marcador ready posterior. Si falla o expira: conservar parcial, cerrar INVALID/INCOMPLETE, no convertirlo en resultado científico negativo.

Antes de lanzar, sellar configuración, fuentes, sustratos y archivos científicos históricos. Auditoría posterior por fórmulas alternativas sobre TODOS los 136 candidatos y lista enumerada alternativa; sus costes son validación y se declaran aparte. Se trata de autoauditoría con código alternativo: no confundir con laboratorio o investigador independiente. Tests sintéticos de orientación, unicidad, masas y deadline antes de ejecución.

## Registro AB y decisión

belief_revision: pendiente de resultados del vecindario; hypothesis_generation: distinguir bloqueo completo de rareza del kernel; objective_revision: ninguna; decision: ejecutar auditoría y después el piloto local/espectral separado que el usuario autoriza. Ninguna actualización numérica H1–H6, C o hipótesis de roles. Prioridad: información alta por coste muy bajo; novedad algorítmica no reclamada, confianza limitada a tres sustratos fijos.
