# Matching local y fluctuaciones de concentración: protocolo independiente

**NOT_RUN.** Especificación futura, separada de fase3coverage y sus cuatro entrenamientos. No autoriza generar geometrías, construir controles, evaluar campos o entrenar redes ahora. No modifica v0.1, sus bloqueos ni H1–H6/C. Las tolerancias siguientes son decisiones propuestas que deberán congelarse junto con semillas, costes y código antes de ejecutar esta línea.

## Pregunta y estimando

¿Añade utilidad la supresión de fluctuaciones multicomponente a ondas largas cuando se mantienen las estadísticas locales relevantes para adquisición? Comparar etiquetas nativas con alternativas sobre **los mismos X, arcos E, distancias, puertos y conteos** `[163,85,68,50,34]`. Mantener algoritmos de observación y decoder; cambiar etiquetas cambia qué canal observa cada sensor. Este estimando corresponde inicialmente a adquisición, no a procesamiento neuronal aprendido.

Con X fijo, la unión de puntos, su espectro, ventanas y grafo permanecen invariantes. Nunca llamar a esta intervención «cambiar la hiperuniformidad de la unión». Se condiciona al mismo sustrato de unión y se manipulan componentes/concentraciones. Los cinco tipos A–E se eligen conjuntamente antes del matching; no seleccionar después el tipo que produzca mayor efecto o resulte más fácil alterar.

## Semántica física previamente fijada

Recomendación: tratar etiquetas como **asignaciones funcionales**, conservando radios físicos originales por nodo. Así, permutar funciones conserva el empaquetamiento del sustrato. Este control no reproduce una retina donde color celular y tamaño estén inseparablemente vinculados.

Si se exige que cada etiqueta lleve su radio polidisperso, especificar otra línea: al reasignar etiquetas, discos grandes pueden quedar en posiciones reservadas a discos pequeños y solaparse. Mantener simultáneamente X, empaquetamiento, conteos y estadísticas locales podría impedir destruir el espectro. No elegir retrospectivamente entre esas semánticas por factibilidad o rendimiento. La imposibilidad de un control admitido implica **identificabilidad pendiente**, no licencia para mover X o relajar restricciones.

## Matching geométrico local

Fijar densidad uno, longitud L20 y escala de normalización por tipo `a_c=L/sqrt(n_c)`. Usar 10.000 centros comunes U(toro), SeedSequence `[20261008,8841]`, idénticos para referencia y candidatos. No usar targets, MSE, logits o gradientes para aceptar controles. Priorizar las escalas del decoder actual: **ℓ=1,25 y soporte r=2,5**.

Tolerancias primarias propuestas, verificadas para cada tipo por separado:

- Distancia del centro al sensor del tipo más próximo: diferencia máxima de CDF ≤0,02; cuantiles p50/p90/p95 con diferencia absoluta dividida por `a_c` ≤0,03.
- Conteos por ventana a R1,25/R2,5: diferencia máxima de CDF ≤0,02 y diferencia absoluta de fracción vacía ≤0,02. Registrar soporte ocupado y residuales, no sólo medias.
- Separación homotípica: CDF de distancia al vecino del mismo tipo con diferencia ≤`max(0,05,2/n_c)`; cuantiles p10/p50/p90 normalizados por `a_c` con diferencia ≤0,05; mínimo candidato ≥mínimo nativo−`0,05*a_c`.
- Histogramas homotípicos en bins físicos `[0,.5,1,1.5,2,2.5]`: **todas las parejas no ordenadas i<j**, usando distancia periódica. Si el conteo nativo de un bin es ≥20, diferencia ≤`max(2,ceil(.05*conteo))`; con menos de20, diferencia absoluta ≤2. Evitar porcentajes inestables o divisiones por cero en la población E de34 nodos.
- Separadamente, matriz **dirigida de tipos de arco**, que cuenta E y no parejas físicas: misma regla entera por celda. Diferencia de outdegree medio por tipo dividida por grado entrante6 ≤0,02.

Estas características no igualan toda la microestructura ni cada vecindario del query. Registrar todos los residuales; una mejora pequeña comparable a ellos conserva confounds locales. **No incluir R4/R5 en el matching:** son escalas largas cuya variación pertenece al mecanismo manipulado; se medirán después, sin condicionarlas a igualdad.

## Manipulación espectral

En los seis modos originales `|n|≤2`, calcular `S_c=|ρ_c|²/n_c`, medias y máximos por A–E y unión. Referencia: todos los componentes cumplen media≤0,05 y máximo≤0,10. Control alternativo: exigir **media S_c≥0,50 para los cinco tipos**, conservando matching local. Publicar también todos los máximos; no reemplazar ese criterio por «algún tipo cambió» si fracasa.

Para distinguir concentración de densidad total, registrar `η_c=ρ_c−(n_c/N)ρ_union` y `T_c=|η_c|²/[n_c*(1−n_c/N)]`, además de la matriz de espectros cruzados. La suma de concentraciones está restringida; no tratarlas como cinco réplicas independientes. La unión debe reproducir sus valores/hashes exactamente con X y orden de nodos constantes. Registrar espectros fuera de banda, picos por población y ventanas R4/R5 descriptivamente; no inferir comportamiento asintótico de N400.

## Admisión, límites y salida posterior

Antes de construir controles, calibrar coste sin scores y fijar semillas, propuestas, reinicios y techo. Seleccionar **primer control admitido**, conservar todos los intentos fallidos y no sustituir semillas. Si ninguna etiqueta satisface simultáneamente matching y manipulación, terminar con FAILED/NOT_IDENTIFIED; no rescatar mediante tolerancias elegidas después de ver scores.

La evaluación posterior exige controles admitidos y un protocolo congelado de campos/queries nuevos comunes, decoders locales y oracle-band declarado. La réplica es el sustrato geométrico, no centros, tipos, mundos ni inicializaciones. No añadir tratamientos dentro de fase3coverage ni actualizar automáticamente priors arquitectónicos. La conclusión máxima será un efecto condicionado a las estadísticas emparejadas y al decoder; la atribución exclusiva a ondas largas exigirá descartar residuales locales relevantes.
