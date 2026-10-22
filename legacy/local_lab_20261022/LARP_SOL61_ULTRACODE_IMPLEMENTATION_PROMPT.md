# Prompt de implementación — LARP v0.1 — SOL 6.1 UltraCode

Lee **íntegramente** los archivos adjuntos antes de modificar o generar código:

1. `LARP_v0_1_RESEARCH_ARCHITECTURE_REVIEW.md` (**contrato científico principal**, especialmente E–M, Q y el JSON de R).
2. `LARP_ASTRA_ARCHITECTURE_REVIEW_v2.md` (**contexto y motivación**, subordinado al documento 1 cuando haya divergencias).

Tu rol es **ingeniero principal de investigación computacional**, no arquitecto científico libre. Implementa en un repositorio ejecutable, probado y reproducible la propuesta **LARP v0.1**, para comprobar si la organización neuronal multihiperuniforme (MHU) añade valor frente a controles sólidos. El resultado negativo es tan válido como el positivo. **No optimices para que MHU gane.** No inventes resultados, no completes decisiones científicas ambiguas de forma silenciosa y no cambies hiperparámetros mirando el test.

## Jerarquía y resolución de conflictos

- Este mensaje determina **cómo implementar, auditar y ejecutar**; el documento 1 determina **qué experimento científico implementar**. El brief v2 sólo aporta contexto secundario.
- El campo `production_code_requested:false` del JSON de Astra describía el encargo **a Astra**, no el actual: **ahora sí se solicita código de implementación**.
- Antes de programar, realiza una **auditoría estática breve pero rigurosa** de especificación, ecuaciones, recuentos, esquemas y fases. Examina especialmente: redondeo Hamilton y conteos N=400/1600/6400; espectro multicomponente y condiciones finitas; función objetivo y sus gradientes periódicos; diferencia entre grados in/out; Delaunay toroidal; sentido de aristas en message passing; dimensiones/cuentas de parámetros G/T/F; consistencia de los 25 canales y de las variantes de 29; selección de puertos por Hungarian; posibilidad real de alcance en 16 pasos; separación entre mundo lógico y sustrato; comparación nativa/shuffle; objetivos y métricas en mapas degenerados; presupuesto de training y análisis jerárquico AB.
- Diferencia **(a) error matemático/contradicción**, **(b) omisión operativa inocua**, **(c) elección científica deliberada**. Documenta cada hallazgo en `docs/SPEC_AUDIT.md`, con localización exacta, impacto y propuesta mínima. Corrige autónomamente sólo (b). Para (a), no fabriques una corrección implícita ni ejecutes la fase afectada: registra `SCIENTIFIC_BLOCKER`, la alternativa mínima y qué resultado experimental cambiaría. Implementa y verifica en paralelo las partes independientes. Si hay varias interpretaciones válidas con consecuencias científicas distintas, conserva la ambigüedad como bloqueo pendiente de decisión.
- Trata las constantes exactas del documento como **decisiones de preregistro**, no como óptimos teóricos; conserva su valor y su trazabilidad. No cambies diseño porque un experimento sale mal.

## Principio causal que debe sobrevivir intacto

La comparación primaria es **marcas nativas MHU vs marcas permutadas (`shuffle`)**, reentrenando desde cero, sobre **exactamente las mismas coordenadas, aristas, puertos, datos, presupuesto, arquitectura y semillas emparejadas**, con conteos A–E conservados. El único tratamiento es la organización espacial de los tipos. Asegura esto mediante aserciones y hashes auditables. MHU-G no puede recibir información de las marcas: un resultado de G no es evidencia de multihiperuniformidad funcional.

Mantén separados (1) el estimando causal nativa–shuffle y (2) la comparación ecológica de arquitecturas completas. Los baselines fuertes —Grid, HU-union inspirado en IBM, random-regular, small-world, Poisson y los controles balanceados/matched/clustered que correspondan— no deben degradarse deliberadamente. No llames a IBM-inspired una reproducción exacta de IBM.

## Entregable: repositorio científico real, no demostración cosmética

Implementa módulos separados para: configuración y preregistro; generador geométrico MHU/HU; certificación finita; grafos y métricas; registro de puertos; generadores de tareas y oráculos; bloque neuronal recurrente; variantes G/T/F; baselines; entrenamiento; ejecución experimental; robustez/intervenciones; evaluación estadística AB; reportes/figuras; CLI y tests.

Proporciona al menos:
- `README.md`: instalación desde cero, hardware mínimo, comandos exactos y significado científico de cada fase.
- `pyproject.toml` y dependencias bloqueadas o mecanismo reproducible equivalente.
- `configs/`: presets inmutables `geometry_validation`, `smoke`, `pilot_focal`, `baseline_screen`, `confirmation`, `robustness`, `analysis`; los perfiles confirmatorios deben quedar implementados pero **no ejecutarse automáticamente**.
- `docs/SPEC_AUDIT.md`, `docs/ADR.md`, `docs/SCIENTIFIC_DEVIATIONS.md`, `docs/AB_PRIORS.md`, `docs/IMPLEMENTATION_STATUS.md`.
- `tests/` con tests rápidos y tests de integración etiquetados.
- `scripts/` o CLI para generar, certificar, entrenar, evaluar, resumir y reanudar.
- `runs/`/`artifacts/` con manifests, JSON/CSV/Parquet cuando proceda, checkpoints, seeds, curvas, certificados y figuras generadas exclusivamente a partir de datos reales. Nunca inventes gráficas ni métricas.

Evita frameworks de experiment tracking o Graph ML pesados si no aportan valor. Python/PyTorch/NumPy/SciPy/Matplotlib bastan si permiten implementar fielmente el contrato. Usa operaciones tensoriales eficientes, vectorización y caché cuando no alteren la semántica. Haz que CPU sea viable; soporta GPU sólo si está disponible. No presupongas CUDA ni acceso a nube.

## Pruebas obligatorias antes del piloto

1. Geometría: toro / imagen mínima / densidad; seeds y conteos exactos; gradiente analítico contra diferencias finitas; espectros y certificados **por clase y unión**; varianza de ventanas; no usar apariencia como prueba de MHU; fallo de certificado bloquea fases científicas posteriores.
2. Grafos: kNN causal con **6 vecinos entrantes** y `6N` arcos, sin self loops ni duplicados; distancias periódicas y dirección correcta de propagación; Delaunay periódico consistente; medidas de grado, reciprocidad, alcanzabilidad y componentes; sin reparación silenciosa.
3. Modelo: shapes/tipos, parámetros efectivamente entrenables y cuentas G/T/F; forward/backward finitos; invariancia EXACTA de G al permutar marcas; simetría de T/F al renombrar simultáneamente clases y sus parámetros; ausencia de comunicación por un camino de longitud mayor que T; ausencia de mezcla entre elementos del batch.
4. Datos: oráculos contrastados con casos manuales para XOR, copia de cinco fuentes y flood-fill **sobre el mundo lógico externo**; separación train/val/test; puertos deterministas independientes de marcas/targets; no leakage desde encoder, máscaras, coords o readout.
5. Causalidad: nativa/shuffle comparten hashes de X, E, asignación de puertos, datasets, optimizador y presupuesto. Sólo difieren las etiquetas espaciales y el modelo aprende nuevamente. Los cambios `matched`/`clustered` son factores distintos, no se mezclan con el estimando primario.
6. Reproducibilidad: distintas seeds producen realizaciones distintas; misma configuración/seed produce artefactos iguales dentro de límites documentados. Asegurar que test permanece cerrado para HPO y selección.
7. Estadística AB: priors H1–H6 marginales, no exclusivos; modelo emparejado con efectos de geometría e inicialización; ROPE ±0,02; tests sintéticos con nulo/positivo/negativo y sensibilidad de cuadratura; ninguna pseudorreplicación de mapas, bits, máscaras o inicializaciones.

No escribas `PASS` en un informe sin ejecutar el test correspondiente. Una prueba omitida debe figurar como `NOT_RUN`, nunca como éxito.

## Política de ejecución por puertas

**Fase 0 — Auditoría y scaffolding.** Inspecciona los documentos y el entorno; crea el repo, registra decisiones, enumera bloqueos y estimación de recursos. No ejecutes experimentos científicos.

**Fase 1 — Tratamiento geométrico.** Implementa generador, gradientes, certificados y controles. Ejecuta tests unitarios y sólo validaciones de coste acotado. Si el certificado MHU es inviable o falla repetidamente, detén el entrenamiento científico y reporta por qué; no relajes límites ni elijas el mejor patrón por rendimiento.

**Fase 2 — Núcleo y tareas.** Implementa arquitecturas, baselines, interfaces y oráculos. Ejecuta tests de invariancia, causalidad, propagación, capacidad básica y pruebas integradas en miniatura. Los tests de capacidad son diagnósticos, no evidencia a favor de MHU.

**Fase 3 — Calibración.** Mide de verdad 200 updates de la tarea copy en el hardware local, incluyendo backward y optimizador. Registra tiempo, memoria y capacidad; aplica literalmente las reglas de reducción de presupuesto previstas en Astra para todas las condiciones antes de test. Nunca extrapoles tiempos como si estuvieran medidos.

**Fase 4 — Smoke y piloto focal.** Sólo cuando las puertas anteriores pasen, ejecuta XOR de validación y, si es factible bajo los límites de tiempo/recursos del documento, el primer contraste copy nativa–shuffle con semillas emparejadas. Usa el orden certificado → smoke → copy focal. Si falta aprendizaje o accesibilidad, diagnostica y detén la interpretación; no iteres hasta obtener una victoria.

**Fase 5 — Suite posterior.** Implementa screen, fill, confirmación, lesiones, escalado y AB en forma invocable y comprobable mediante dry-run/tests pequeños. **No lances automáticamente decenas de entrenamientos confirmatorios ni pruebas largas**; deja un comando claro para cada etapa y marca qué gates científicos y presupuestarios deben satisfacerse. La ejecución confirmatoria requiere que las decisiones científicas bloqueadas estén resueltas y que el preregistro esté congelado.

La ejecución es secuencial o con concurrencia segura y memoria controlada; se puede reanudar con el mismo seed y checkpoint. Nunca reemplaces una corrida desfavorable por otra seed. Los fallos reproducibles de entrenamiento se registran; los fallos de infraestructura se separan de la evidencia.

## Reglas de economía de tokens y recursos

- **Lee los documentos localmente, no vuelques su texto completo a la conversación.** Las instrucciones de esta nota son una capa ejecutiva, no sustituyen los detalles de Astra.
- No reproduzcas bloques grandes de código en el chat: edita archivos y entrega rutas, comandos y resúmenes.
- No vuelvas a consultar literatura salvo que sea indispensable para resolver un blocker real; conserva las fuentes de Astra con su estatus.
- Mantén respuestas de progreso concisas: fase, tests ejecutados, artefactos y blocker. Evita narración y promesas de resultados.
- Antes de una operación que pueda exceder los límites del documento, mide coste y usa un plan conservador; no lances una batería masiva por defecto.
- No solicites al usuario decisiones triviales de ingeniería; pide decisión únicamente ante un **SCIENTIFIC_BLOCKER** real que cambie el significado del experimento.

## Entrega final

Informa, de forma breve y verificable:
1. árbol resumido del repo y comandos exactos `install`, `test`, `validate-geometry`, `smoke`, `pilot`, `analyze`, `resume`;
2. qué está implementado, ejecutado, probado, pendiente o bloqueado;
3. resultados **reales** de tests y certificados, con archivos/logs de respaldo;
4. tiempo/memoria medidos y presupuesto restante;
5. errores o contradicciones detectados en la especificación original, sin correcciones silenciosas;
6. si se llegó al piloto, todas las seeds/condiciones y resultados, incluidos negativos;
7. dónde queda el historial de AB y qué priors siguen sin actualizar por falta de evidencia;
8. siguiente acción concreta permitida por las puertas científicas.

No declares demostrado que MHU funciona ni calcules posteriors basados en pruebas técnicas, smoke tests o propuestas teóricas. **El producto principal es un experimento fiel, reproducible, adversarial y falsable, no un resultado favorable.**
