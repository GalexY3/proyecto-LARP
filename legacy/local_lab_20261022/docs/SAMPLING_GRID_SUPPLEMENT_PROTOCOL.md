# Suplemento Grid: decisión y protocolo pendiente

Fecha2026-10-08. **NOT_RUN.** Este documento no modifica `sampling_probe_v1`, su configuración congelada ni sus resultados. Pregunta: cuánto de la ventaja de muestreo aviar permanece frente a un reparto de canales fuerte sobre una rejilla, con iguales conteos, mundos y estimadores.

## Decisión sobre la tanda de treinta segundos

**No recomiendo lanzar el Grid balanceado completo bajo un presupuesto total≤30s sin calibrar primero su construcción.** El código existente es reutilizable, pero no equivale a una coloración instantánea en nuestros conteos. No hay timing completo medido en el repositorio que garantice ese límite.

`larp.geometry.relabel_geometry(..., control="grid_balanced")` tiene dos ramas:

- Si todos los conteos son80, usa `(floor(x)+2 floor(y)) mod5`, una subrejilla exacta y barata. Nuestros conteos son163/85/68/50/34. Cambiarlos a80 por conveniencia introduciría densidades y relación señal/ruido diferentes, invalidando el contraste con v1.
- Para los conteos reales, realiza100000 propuestas de swaps por intento y hasta10 reinicios, con estadísticas espectrales cacheadas; emite un certificado después de cada intento. Tres semillas pueden requerir3 millones de propuestas y30 certificados. El coste peor no está medido. La admisión escoge el primer intento cuyos componentes cumplen los umbrales espectrales y de ventanas; no se filtra mediante MSE de campos. Si ninguno pasa, devuelve el candidato de menor objetivo como **Grid balanceada aproximada**, con fracaso de admisión explícito.

Pasar `proposals=10000,restarts=1` exige `test_only=True`: no es el baseline congelado original. Puede servir para medir tiempo, pero no debe llamarse el baseline fuerte de v0.1 ni escoger presupuesto a posteriori por sus errores de interpolación. El objetivo existente sólo equilibra pocos modos de ondas largas; no iguala necesariamente la exclusión homotípica del patrón aviar.

## Confound descubierto antes del ensayo

El Grid400 coloca puntos en `(a+.5,b+.5)`, mientras todas las queries v1 son `(2a+.5,2b+.5)`. Por tanto, **cada query coincide exactamente con un sensor Grid**, para el canal que tenga allí. Esto puede ser una ventaja legítima bajo esa interfaz discreta, pero una comparación sólo con esas queries mezclaría organización de poblaciones y alineación de entradas/salidas. El kernel fijo tampoco obliga a copiar exactamente esa observación porque promedia vecinos.

Para resolverlo sin seleccionar fases favorables, congelar dos estratos comunes antes de scores: las100queries originales de v1 como **aligned**, y100queries independientes `U([0,20)²)` como **continuous**, SeedSequence `[20261008,7814]`. Evaluar todas las familias en ambos estratos con los mismos campos/coeficientes, observaciones y ruido. No sustituir retrospectivamente la métrica v1 ni llamarlo replicación independiente: se reutilizan los mismos mundos y geometrías. Un Grid constante con tres semillas de marcas proporciona tres realizaciones de asignación, no tres geometrías espaciales independientes.

## Protocolo suplementario concreto

Crear serie `sampling_grid_supplement_v1`, config/manifests propios y resultados en carpeta nueva. Escribir freeze antes de construir Grid o calcular los nuevos scores.

1. **Calibración de ingeniería sin scores:** N400/L20, conteos nominales, Grid/seed9005,10000swaps/un reinicio/test_only, mismos términos y programación térmica del algoritmo. Medir segundos por propuesta y coste de un certificado separado. Guardar hashes/candidato, sin evaluar campos ni elegir hyperparameters. Techo5s para optimización; si no existe interrupción segura, medir sólo un segmento de1000propuestas y declarar la extrapolación. El resultado no entra en las comparaciones científicas.
2. **Construcción fuerte congelada:** `generate_geometry(400,seed,"grid")`, seguido del `relabel_geometry` original100000swaps/hasta10reinicios, seeds1101–1103. Primera admisión por los criterios existentes, sin nuevas tolerancias. Registrar todos los intentos, costes y estado ADMITTED/FAILED. Conservar un fallo como baseline aproximado señalado; no reemplazar la semilla. Reservar hasta180s CPU total de construcción, sin exceder la planificación mediante ajuste de presupuesto según scores. Si la estimación conservadora supera180s, parar antes de la tanda y dejarla NOT_RUN; optimizar el código sin cambiar objetivo/RNG sería otra actuación de ingeniería verificable.
3. **Evaluación común barata:** campos v1,128mundos por banda, cinco canales, σ0/.1, NN y kernelℓ1.25/cutoff2.5 ya fijados. Queries aligned y continuous comunes. Añadir Gridbalanced-native/shuffle; conservar nominal/full/local como rivales. Cuatro familias×tres realizaciones×dosmarcas×dosestimadores×dosbandas×dosruidos×dosqueries=384celdas. El suplemento recalcula el estrato aligned para comprobar igualdad de hashes/scores con v1; no registra esas celdas como nuevas réplicas. Techo30s sólo para evaluación/figura, separado de construcción.
4. **Salida:** MSE macro igual por canal, distancias/vacíos y fallback por estrato; medias/SD descriptivas y diferencias nativa−shuffle por realización. Costes de construcción y estimación separados y suma total de método. Admitir que una rejilla no necesita optimización de posiciones es parte de su eficiencia; no gastar cómputo artificialmente para igualarla al generador aviar.

No modificar estimadores por familia ni ajustarℓ/bandas con los resultados. Los campos son estacionarios por su distribución, pero el conjunto finito de128realizaciones no garantiza igualdad exacta entre fases: por eso ambos estratos se evalúan con mundos comunes y no se elige el más favorable.

## Interpretación prevista

- Si Grid iguala o supera aviar en continuous, la ventaja frente a shuffle/nominal no basta para justificar el sustrato aviar como mejor sensor.
- Si el resultado Grid cambia mucho entre aligned/continuous, informar dependencia de interfaz; no convertir uno de los estratos en resultado general.
- Si aviarfull y local_only siguen próximos y ambos superan Grid, priorizar investigar distribución local de canales y vacíos. No adjudicar la ventaja al espectro sin un rival que iguale esas estadísticas.
- Si Gridbalanced falla admisión, distinguir rendimiento del candidato aproximado de la pregunta aún pendiente frente a Grid fuertemente equilibrado. Nunca borrar sus errores ni proclamar baseline fuerte aprobado.

Este suplemento identifica utilidad de adquisición bajo un conjunto de señales y estimadores. No abre la puerta XOR, no demuestra procesamiento neuronal y no calcula posterior de arquitectura. Todos los priors permanecen sin actualizar.
