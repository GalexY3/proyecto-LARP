# Fase3: balance de roles y motivos, con validación común SS/UU

Estado final: **cuatro corridas completas; BALANCED aprueba la puerta primaria y UNIFORM falla**. Sólo se aprendió la tarea local b0 con el candidato GGNN/COORDS_OFF. No se ejecutaron XOR, MHU ni remoto, y el piloto original permanece cerrado.

## Protocolo registrado antes de resultados

`role_coverage_v1` compara dos paneles de12triples: cuatro anchors comunes y ocho extras. El modelo publicado GGNNLikeModel/COORDS_OFF permanece intacto: 12,481 parámetros, d32/T16, batch4, AdamW lr.003, betas(.9,.999), eps1e−8, wd1e−4, clip1 y250updates. Seeds2101/2102 y calendario BALANCED anterior idénticos por índice. Los anchors ocupan índices0–3; los extras se ordenan lexicográficamente antes de aplicar el calendario. El orden ABBA quedó fijado: U2101, B2101, B2102, U2102.

UNIFORM contiene cuatro anchors fijos y ocho draws sin reemplazo condicionados a elegibilidad, no12observaciones IID. BALANCED añade ocho triples greedy, minimizando lexicográficamente: Σsource,role n²; Σsource(n0−n1)²; Σbin hist². La signature geométrica es `(h0,h1,p2_0,p2_1,round(r0²,8),round(r1²,8))`; desempates por una permutación9944 constante de todo el pool. No se consultaron resultados de modelos para construir paneles.

La construcción usó namespaces9941–9944 con master20261008 y máximo1000propuestas. Admitió el índice14, la **15ª propuesta**, por elegibilidad geométrica. Todas las anteriores se conservaron como rechazadas. Los anchors fueron `(18,19,8)`, `(18,8,19)`, `(40,49,39)`, `(40,39,49)`; los swaps garantizan exposición de cada fuente de anchors en ambos roles y en ambas condiciones.

Antes de seleccionar extras se reservaron cuatro queries comunes y sus pares SS/UU, con cuatro patrones00/01/10/11 por triple. SS usa fuentes de anchors expuestas en ambos roles. UU usa fuentes de U, excluidas de todos los roles activos de train, incluyendo queries. Sus neuronas **sí siguen presentes en la misma Grid y pueden recibir/propagar estados durante train**: no son nuevas neuronas ni otra geometría. Las queries retenidas no se usan como queries de train.

| Query común | Triple SS | Triple UU |
|---:|---|---|
|30|(30,49,39)|(30,20,31)|
|48|(48,39,49)|(48,59,58)|
|29|(29,19,39)|(29,20,28)|
|9|(9,8,19)|(9,98,0)|

**Alcance combinatorio de SS:** tres de sus cuatro parejas ordenadas de fuentes ya aparecen en los anchors; sólo (19,39) es una pareja nueva. Las cuatro queries y los cuatro triples completos sí son nuevos. SS prueba principalmente transferencia a nuevos contextos/query, no cuatro recombinaciones inéditas de fuentes. La regla de admisión registrada exigía triples distintos y queries nuevas, por lo que la puerta sigue siendo válida; la lectura de H-R2/R3 sobre generalización combinatoria queda limitada.

U={0,20,28,31,58,59,98}. El pool tiene2086triples ordenados y1628extras admisibles después de reservar U/queries. Todos los perfiles hop son(2,2), por lo que este matching es coarse. Los destinos antiguos20/21/26/61 y fuente11 se excluyeron sólo de la validación primaria nueva; no se purgó train. Los cuatro contextos antiguos completos se congelaron como AUX final, fuera de puerta y actualización H-R, sin feedback al optimizer.

La condición primaria **BALANCED** se eligió antes de scores. La puerta exige que sus dos seeds sean COMPLETE y finitas, con train/SS/UU≥.98 en el estado final. Con48casos train y16por estrato esto exige **48/48 +16/16SS +16/16UU**. Se reporta también la puerta UNIFORM, sin elegir un ganador después.

## Auditoría, identidad y coste real

`--prepare-only` congeló código/config/hipótesis/runtime, paneles, hashes de inputs, pesos iniciales y calendarios, sin crear optimizer. Una auditoría independiente previa aprobó24checks y17hashes/identidades. `--execute-prepared` verificó esos mismos archivos e inputs antes de entrenar. La identidad permaneció `60b883ddaf3f5c99d26f73f89003a766397b0607e9be74d89dc26f451f38ae8f`.

Las cuatro corridas completaron250updates cada una: **1000updates en total**. El supervisor externo ejecutó el proceso una sola vez con timeout duro120s, incluyendo imports, preparación y medidas. Tiempo externo real **38.912s**, interno37.036s; returncode0, sin timeout, reintentos ni ampliación de presupuesto. RSS máximo muestreado428,290,048bytes. Las medianas de update fueron30.48–30.89ms. La supervisión consta en `execution_wall_supervision.json` y el código científico congelado no se modificó.

## Resultados finales completos

| Condición | Seed | Train, 48casos | SS, 16casos | UU, 16casos | AUX antiguo, 16casos |
|---|---:|---:|---:|---:|---:|
|UNIFORM|2101|93.75% (45/48)|93.75% (15/16)|87.50% (14/16)|87.50% (14/16)|
|BALANCED|2101|100% (48/48)|100% (16/16)|100% (16/16)|100% (16/16)|
|BALANCED|2102|100% (48/48)|100% (16/16)|100% (16/16)|87.50% (14/16)|
|UNIFORM|2102|75% (36/48)|62.50% (10/16)|56.25% (9/16)|68.75% (11/16)|

| Condición | Seed | BCE train | BCE SS | BCE UU | BCE AUX |
|---|---:|---:|---:|---:|---:|
|UNIFORM|2101|.273687|.412883|.452662|.674252|
|BALANCED|2101|.000084|.000077|.000071|.000071|
|BALANCED|2102|.002953|.001625|.001710|.716524|
|UNIFORM|2102|.614895|.696002|.627446|.588102|

**BALANCED pasa; UNIFORM falla.** En ambas seeds BALANCED, voltear fuente0 cambia siempre la clase y voltear fuente1 nunca la cambia, tanto en SS como en UU. Es el comportamiento selectivo requerido para b0. En UNIFORM esas fracciones fueron .875/.125 y .25/0 para SS, y .75/.25 y .125/.125 para UU. La fracción de predicciones correctas después de flips es redundante con accuracy al enumerar los cuatro patrones; no se contabiliza como evidencia independiente.

### AUX conserva los fallos conocidos

El fallo residual de BALANCED2102 ocurre en el antiguo destino61: responde0 a los cuatro patrones y acierta2/4. Sí resuelve20/21/26, incluidos los contextos con fuente11. BALANCED2101 resuelve los cuatro contextos antiguos. Por tanto la puerta primaria aprobada **no demuestra una regla universal sobre cualquier contexto local**.

Ningún puerto activo de esos cuatro contextos se activó en train BALANCED. En UNIFORM únicamente fuente22 del antiguo contexto21 apareció como role1; ninguno de los cuatro triples completos ni sus queries se usó como query de train. Estos detalles están registrados por condición en manifest/resultados. AUX es conocido y fuera de puerta; no es confirmación ciega ni se utilizó para seleccionar modelos o redefinir H-R.

## Qué componente cambió realmente

| Métrica de construcción | UNIFORM | BALANCED |
|---|---:|---:|
|Σsource,role n²|24|24|
|Σsource(n0−n1)²|14|0|
|Σbin hist² de signature|24|14|
|Queries únicas de train|9|7|
|Fuentes físicas únicas|19|12|
|Fuentes únicas por rol|12/12|12/12|

La primera componente de «cobertura fuente×rol» **empata24/24**. BALANCED tiene menos queries y fuentes físicas únicas; no aumenta cobertura total. El contraste informa sobre **balance entre roles y distribución de motivos**, dentro de un paquete de construcción curricular. También cambia qué contextos reciben las exposiciones20–21 del calendario. No se aisló una mediación de balance de roles frente a motivos, orden de contextos o ajuste de train. UNIFORM también falla en train, así que la diferencia no se atribuye exclusivamente a transferencia.

La signature es un proxy incompleto: omite orientación, outdegree, walks largos, mezcla source-query y estados de vecindario. Igualar hops/query no iguala todas esas propiedades. COORDS_OFF elimina coordenadas absolutas, pero conserva distancias de aristas y estructura residual del grafo. Sin embeddings por nodo, «fuente expuesta» describe activación contextual de puertos, no memoria explícita de IDs.

## Actualización ordinal registrada de H-R

Los tres priors eran **moderadamente plausibles**, marginales y solapados. Se aplicaron las reglas de `role_coverage_hypotheses_v1.json` a un único paquete conjunto, sin Bayes factors ni probabilidades numéricas fabricadas.

| Hipótesis técnica | Regla observada | Dirección ordinal |
|---|---|---|
|H-R1: el paquete de balance/cobertura limita transferencia bajo presupuesto fijo|BALANCED mejora UU en+.125 y+.4375; train/SS≥.98 en ambas seeds|Apoyo débil; sigue moderadamente plausible con apoyo limitado|
|H-R2: la regla resuelve fuentes expuestas pero depende del soporte para fuentes nuevas|BALANCED pasa train/SS/UU en ambas seeds|Contraevidencia débil dentro de este panel|
|H-R3: el régimen no aprende selección reproducible para nuevas combinaciones de fuentes expuestas|BALANCED pasa train/SS en ambas seeds|Contraevidencia débil dentro de este panel|

AUX no altera esas reglas fijadas antes de resultados, pero limita cualquier lectura universal. SS sólo contiene una pareja de fuentes inédita; no se presenta la contraevidencia ordinal como prueba amplia de recombinación. Dos inicializaciones comparten una geometría y un par fijo de paneles: no proporcionan efecto poblacional ni confirmación. Accuracy, BCE, gradientes y flips pertenecen al mismo paquete correlacionado, no se multiplican como pruebas independientes. H1–H6 y C permanecen **sin actualizar**.

## Cierre y archivos

La puerta de esta fase permite considerar una serie posterior congelada para XOR local; **no la ejecuta automáticamente**. Tampoco autoriza MHU/T/F, remoto, robustez, escalado o apertura del piloto original. La fase termina con los cuatro resultados preservados y sin elegir otra seed, aumentar250updates ni rescatar un resultado.

Cinco tests significativos aprobaron en1.69s antes de congelar; la suite global fue auditada por la raíz y no se repitió aquí. Verifican soporte común SS/UU, reserva de todos los roles activos U, swaps, selección por primera elegibilidad, objetivo greedy contra enumeración exhaustiva, puertas y reglas ordinales, incluidos parciales.

Archivos en `artifacts/role_coverage/v1`: `preregistration.json`, `pre_execution_independent_audit.json`, `execution_started.json`, `execution_wall_supervision.json`, `results.json`, `H_R_ordinal_updates.json`, cuatro subdirectorios con resultados/checkpoints finales y figura `role_coverage_summary.png`/SVG. Script de render sólo lectura: `artifacts/role_coverage/plot_summary.py`. Los módulos, configs, scope y tests congelados permanecieron intactos.
