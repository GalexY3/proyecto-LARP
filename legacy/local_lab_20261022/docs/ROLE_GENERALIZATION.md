# Generalización de roles: ablar sólo coordenadas absolutas

Protocolo de la sección1 de `NEXT_PHASE_EXECUTION_SPEC.md`, estado al congelar **NOT_RUN**, 2026-10-08. La única intervención pone a cero todos los slots21:25 en copias de los inputs de todos los nodos, en train/validation y medidas. Distancias de aristas, X/E, puertos, roles, queries, payload, targets, readout y el código publicado GGNNLikeModel permanecen idénticos.

Dos únicas corridas nuevas COORDS_OFF: Grid N400 g1101, target b0, seeds2101/2102, 12481P, T16, B4, 250 updates, AdamW .003/betas .9/.999/eps1e-8/wd1e-4/clip1, CPU4, techo120s. COORDS_ON se reutiliza de GRUbaselinev1, sin contar nuevas réplicas. Verificar hashes de inputs ON, targets, inicialización, modelo/optimizer/budget y calendarios BALANCED byte por byte. Se congelan hashes de inputs OFF y referencias a controles antes del primer optimizer. Los pesos que reciben coordenadas se conservan en el mismo modelo/optimizer aunque su input sea cero; la capacidad nominal es idéntica y cambia la información disponible.

Sólo estado final: medir accuracy/BCE train/val, curvas/normas, logits por los cuatro patrones/destino, gradientes y cambios de clase por rol. Puerta: ambas seeds finitas, train+val≥.98, que con48/16casos exige acertarlos todos. No escoger checkpoint favorable ni extender250. XOR/MHU/remoto quedan NOT_RUN aunque pase; requieren otra serie congelada. No se abre piloto original ni test científico, ni se actualizan H1–H6.

El contraste elimina coordenadas absolutas del encoder, no toda información espacial porque los mensajes conservan distancias. Un éxito podría obedecer a simetría, condicionamiento o menor memorización y no demostraría una causa única. Una sola geometría y dos seeds no justifican adoptar un nuevo encoder por defecto. Un fallo cerrará este factor bajo el presupuesto sin borrar outputs desfavorables.

Comando: `.venv\Scripts\python.exe -m larp.role_generalization`. Directorio exclusivo `artifacts/role_generalization/v1`. Pruebas previas verifican copia/ablación en todos los nodos, preservación de canales/metadata y rechazo de target/pesos iniciales distintos al control reutilizado.

## Resultado observado

Dos corridas únicas completas de250updates, 20.200 s totales (CPU4), RSS máximo426,299,392bytes. No hubo divergencia, extensión, HPO ni reintentos. El preflight comprobó todos los factores preservados y la identidad del código GGNNLikeModel original. Identidad congelada: `00bba94bd0208fb164f89b8fed14b71bbb34635d114edbbc70acc344aaf23376`.

| Seed | COORDS_ON train/val reutilizado | COORDS_OFF train/val final | BCEval ON | BCEval OFF |
|---:|---:|---:|---:|---:|
|2101|1.0000/.7500|1.0000/.8750|1.558116|.377215|
|2102|.9375/.7500|1.0000/1.0000|1.670898|.000588|

**Resultado mixto; puerta conjunta fallida.** Ambas seeds mejoraron validación, pero el criterio previamente fijado exige que ambas superen .98. Seed2101 mantiene dos errores: destino20 responde0 a los cuatro patrones. Los destinos21/26/61 ya seleccionan b0 correctamente. Seed2102 acierta los16casos de validación. No se usa el resultado favorable de2102 para abrir otra rama, ni se borra el fallo2101.

| Destino val | COORDS_OFF2101 predicciones00/01/10/11 | COORDS_OFF2102 |
|---:|---|---|
|20|0,0,0,0|0,0,1,1|
|21|0,0,1,1|0,0,1,1|
|26|0,0,1,1|0,0,1,1|
|61|0,0,1,1|0,0,1,1|

La fracción de flips que cambia clase es .75/0 para fuente0/fuente1 en2101 y1/0 en2102, frente a .5/0 en ambos COORDS_ON. Para seleccionar b0 perfectamente, la fuente0 debe cambiar siempre la clase y la distractora nunca. Medianas de sensibilidad fuente0/fuente1: .553/.147 y .0157/.0252. La seed que aprende mejor tiene menor derivada local en los endpoints binarios: los gradientes diferenciales no sustituyen los cambios finitos ni prueban por sí solos causalidad del aprendizaje. La fracción correcta de flips sigue siendo redundante con accuracy al enumerar los cuatro patrones.

La intervención apoya que la entrada de coordenadas absolutas puede perjudicar este entrenamiento selectivo compartido. Pero eliminar features puede cambiar condicionamiento, saturación y simetría además de memorización; no se identificó una causa única. Mantener todos los pesos conserva12,481 parámetros nominales, aunque128pesos del encoder asociados a los cuatro canales no reciben gradiente de datos (siguen en optimizer/weightdecay). El mensajero conserva distancias espaciales; esto no convierte el modelo en completamente ciego a geometría.

Esta es una sola realización Grid y dos seeds; no hay comparación de arquitectura MHU ni evidencia de funciones celulares diferenciadas. La accuracy final sólo corresponde a b0 con48/16casos de este pool. No acredita XOR ni smoke remoto. **XOR/MHU/remoto permanecen NOT_RUN** bajo este protocolo. Piloto original cerrado, test no abierto y H1–H6 intactos.

Dos tests aprobados en1.65s. Manifest, hashes de inputs ON/OFF, calendarios completos, hashes iniciales compartidos, checkpoints y todos los patrones/flips se conservan en `artifacts/role_generalization/v1`. La figura `context_predictions.png` muestra todos los casos retenidos y el fallo residual; no selecciona checkpoints. El estado de la sección1 de NEXT_PHASE_EXECUTION_SPEC fue actualizado sin alterar decisiones del protocolo.
