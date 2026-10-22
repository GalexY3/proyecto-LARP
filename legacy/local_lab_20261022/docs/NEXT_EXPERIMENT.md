# Siguiente ensayo permitido tras el fallo de smoke

Fecha: 2026-10-08. Estado del protocolo propuesto: **NOT_RUN**. Su objeto es diagnosticar capacidad local frente a transmisión remota; no es una revisión ya aprobada del núcleo ni un experimento de superioridad MHU. Referencias: contrato principal J1 y M; resultados conservados en `runs/smoke/diagnostics.json` y `artifacts/diagnostics/xor_influence.json`.

## Qué se ha observado y qué permite concluir

Los cuatro entrenamientos G completaron 250 updates. Accuracy de validación: Grid/2101=0,48046875, Grid/2102=0,5, MHU/2101=0,517578125 y MHU/2102=0,5; train=0,51025390625/0,5/0,51416015625/0,5. Todos los ejemplos train/val tienen ambas fuentes accesibles a T16; mediana de hops 8 en Grid y 9 en MHU. El gate ≥0,98 falla y copy/fill/screens/confirmación permanecen cerrados.

En 20 ejemplos de validación por checkpoint, fijados por clave 9911, la mediana de |∂logit/∂bit_fuente| es 2,90e−14/1,11e−13/1,12e−13/2,34e−13. El gradiente sobre un bit hipotético en el receptor es 0,0265/0,0127/0,0190/0,0301. Cambiar el primer bit fuente altera el logit aproximadamente 1e−8 de mediana y no cambia ninguna de las 80 predicciones binarias. Las cifras pequeñas de diferencias en float32 pueden incluir redondeo; el gradiente no demuestra por sí solo la causa del fracaso.

La **inferencia de trabajo** es una transmisión efectiva o un condicionamiento desfavorable del bloque, aunque existan caminos. Quedan alternativas: dificultad de integrar XOR, optimización, señal diluida por media/residual, saturación y representación de roles/interfaz. El gradiente hipotético del receptor no prueba que el bloque aprenda XOR local. Ambas geometrías fallan y G no recibe marcas: estos resultados no son evidencia contra multihiperuniformidad funcional. H1–H6 permanecen sin actualizar.

## Protocolo diagnóstico propuesto

Conservar los cuatro checkpoints y sus hashes. Crear una serie técnica nueva, con sus propios datos/manifests; no sobrescribir smoke ni abrir test. Fijar antes de entrenar: N400/L20, G original, T16, mismos grafos/puertos, inicializaciones 2101/2102, AdamW original lr 0,003/B4 y 250 updates finales por condición. No barrer lr, escoger checkpoint ni extender presupuesto según scores. Registrar loss/accuracy final, gradientes y respuesta a flips. Un éxito técnico requiere ≥0,98 en los cuatro patrones de XOR y resultados finitos; un diagnóstico parcial no abre el piloto original.

1. **Control de optimización centralizado.** Un MLP 2→32→1 con SiLU recibe explícitamente los dos bits; enumerar 00/01/10/11 como batch 4, con las dos inicializaciones y 250 updates. Comprueba que etiquetas, loss y optimizer pueden aprender la relación cuando no hay transporte. Es un control técnico separado, sin matching de parámetros ni afirmación arquitectónica. Si falla, detener el diagnóstico y revisar el pipeline.
2. **Capacidad local del bloque original.** En cada geometría G, inyectar ambos bits en payload slots 1/2 del puerto de salida; source/query IDs cero, mask sólo en salida, coordenadas y resto de canales según interfaz. Un destino fijo común como sitio lógico (0,0), los cuatro patrones como batch 4 y dos inicializaciones. Se cambia explícitamente la tarea para eliminar transporte; no se presenta como un XOR remoto corregido. Si falla, detener antes de entrenar el diagnóstico de distancia.
3. **Local frente a remoto con interfaces separadas.** Congelar 16 destinos comunes y 16 triples por condición: 12 train/4 val, cada triple con las cuatro combinaciones. Para el local, dos fuentes distintas del destino con 1–2 hops dirigidos en **ambos** sustratos; para el remoto, ambas fuentes a distancia física ≥L/4, conservando los destinos, roles y número de ejemplos. Enumerar el pool común y seleccionarlo mediante SeedSequence(master 20261008, clave 9912); asignar roles mediante clave 9913. Si no existen 16 destinos admisibles, registrar `DIAGNOSTIC_UNAVAILABLE`, sin ampliar hops silenciosamente. Entrenar local/remoto desde el mismo estado inicial, para Grid/MHU y ambas seeds. La selección por hops es propia de este diagnóstico y nunca modifica datasets primarios.

El tercero iguala cantidad de triples, patrones, destinos, inicialización y presupuesto; cambia separación/ruta, no elimina diferencias en detalle de los caminos. Su objetivo es localizar el fallo del ensayo, no estimar una ventaja de geometría. Reportar gradiente respecto a ambos bits, cambio de logit y fracción de flips que producen el cambio correcto de XOR, distribuidos por hops. No contar patrones/gradientes como réplicas de arquitectura. Establecer un techo técnico de 5 minutos para toda la serie; si se supera, conservar parciales y marcar los restantes `NOT_RUN`.

## Regla de decisión previa

| Diagnóstico | Acción permitida |
|---|---|
| Control centralizado falla o hay inconsistencia de labels/inputs | Revisar pipeline/loss/optimizer; tratarlo como invalidez o diagnóstico incompleto, sin cambiar geometría ni actualizar priors. |
| Control centralizado aprende, bloque local falla | Revisar normas, saturación y gradientes locales. Sólo después considerar preregistrar v0.1b con GRU compartido, nuevo matching y presupuesto común, conforme M. No sustituirlo en estas corridas. |
| Bloque local aprende; local separado aprende; remoto falla | Priorizar transporte efectivo/condicionamiento. Los datos actuales no justifican T32 por falta de accesibilidad: T16 ya alcanza todas las fuentes. Una intervención futura sobre profundidad, residual o agregación necesita nueva hipótesis y preregistro, cambiando un factor por vez. |
| Ambos problemas separados aprenden pero smoke original falla | Investigar variedad de puertos, complejidad del dataset y generalización de roles. El diagnóstico pequeño no acredita aprendizaje del smoke original ni autoriza HPO sobre su test. |
| Resultado mixto entre inicializaciones o ninguna causa aislada | Conservarlo como inconcluso; no elegir el diagnóstico favorable ni lanzar v0.1b automáticamente. |

**Siguiente acción concreta recomendada:** congelar y ejecutar primero los controles centralizado y local del bloque, antes de decidir GRU, T32 o cambios de optimizer. Este archivo especifica esa acción; no afirma que se haya ejecutado. La calibración actual de 200 updates reales demuestra viabilidad de CPU (mediana 32,6 ms por update y RSS 430.686.208 bytes), pero viabilidad no revoca el gate de aprendizaje. Los 163 tests aprobados acreditan comprobaciones de software, no capacidad algorítmica ni utilidad MHU.

## Preferencia aviar y planificación de la siguiente versión

El usuario ha reiterado su interés por una distribución como el mosaico retiniano de la gallina. La geometría entrenada hasta ahora es la MHU espectral original del contrato; la variante aviar `LARP_NETWORK_PREVIEW_GEOMETRY.npz` no entró en el entrenamiento. Su preview combina tamaños por tipo, empaquetamiento, repulsión homotípica y control espectral; no reproduce una retina empírica ni posee todavía un certificado científico emitido por el pipeline completo.

Recomendación para la siguiente versión: hacer de la variante aviar la candidata de interés, conservar la MHU nominal como control del generador y mantener los resultados anteriores intactos. Esta recomendación es planificación, no autorización para cambiar retrospectivamente v0.1 ni afirmación de ventaja biológica.

1. Resolver primero la capacidad/transmisión del bloque con los diagnósticos técnicos anteriores, sin cambiar geometría. Si se necesita modificar el bloque, aislar una modificación y versionar matching, presupuesto y puerta XOR.
2. En paralelo, convertir el generador aviar en una implementación reproducible con parámetros/semillas congelados. Certificar cada tipo y unión, desorden, ventanas, exclusión local y conectividad en tres semillas fijadas antes de resultados. Las comprobaciones del preview no se presentan como certificado del nuevo pipeline.
3. Con un bloque que supere el smoke remoto, compararlo sin ajustes por condición sobre Grid, MHU nominal y variante aviar. Los cambios de coordenadas/puertos/grafo se declaran como comparación de arquitectura completa.
4. Para el efecto funcional de marcas, reentrenar nativa frente a shuffle dentro de cada geometría conservando exactamente X, E, puertos, datos e inicializaciones; usar T/F, porque G no recibe marcas. Una mejora aviar frente al nominal no aislaría por sí sola hiperuniformidad, empaquetamiento o separación local; la atribución de ondas largas sigue limitada por C3.

No bajar el umbral .98 para abrir el piloto ni cambiar a la vez recurrencia y generador y atribuirles después una mejora. El coste del diagnóstico técnico está acotado a cinco minutos; certificación aviar y entrenamientos posteriores deben medir su coste antes de abrir la siguiente tanda. Todo este añadido permanece **NOT_RUN**.
