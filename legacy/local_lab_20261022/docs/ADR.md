# Registro de decisiones de implementación — LARP v0.1

Fecha: 2026-10-08. Este registro conserva decisiones del contrato y completa detalles operativos. No constituye resultados ni permiso para cambiar el experimento. La auditoría científica está en [SPEC_AUDIT.md](SPEC_AUDIT.md); el estado ejecutado se mantiene en [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md).

## ADR-001 — Autoridad documental

**Aceptada.** `LARP_SOL61_ULTRACODE_IMPLEMENTATION_PROMPT.md` determina cómo implementar, auditar y ejecutar. `LARP_v0_1_RESEARCH_ARCHITECTURE_REVIEW.md`, incluidos E–M, Q y R, determina qué experimento implementar. `LARP_ASTRA_ARCHITECTURE_REVIEW_v2.md` conserva contexto subordinado; v1 conserva procedencia histórica. El campo `production_code_requested:false` del review pertenece al encargo previo y no invalida la implementación ahora autorizada. Las discrepancias científicas se registran antes de ejecutar la rama afectada.

## ADR-002 — Tratamiento nominal y figura aviar

**Aceptada; decisión científica conservada.** El tratamiento nominal usa coordenadas colectivas multicomponente, repulsión común de radio 0,30, bandas y optimización exactamente fijadas en E/F/R. Se mantiene N400, L20, densidad uno, conteos Hamilton `[163,85,68,50,34]`. N1600 y N6400 conservan densidad y cutoff físico.

`LARP_NETWORK_PREVIEW.py`, su PNG y sus arrays/diagnósticos representan una visualización posterior inspirada en retina, con tamaños y espaciado por tipo. La imagen no genera sustratos científicos ni acredita MHU. Adoptar esa distribución como factor exigiría una nueva versión, certificado completo y comparación propia; no se sustituye silenciosamente el objetivo nominal. Los archivos `LOW_K_ONLY` conservan la visualización anterior.

## ADR-003 — Certificado y admisión

**Aceptada; decisión científica conservada.** El certificado aplica a cinco componentes y unión: media S≤0,05, máximo S≤0,10, distancia mínima≥0,299, media de cocientes de varianza R4/R5≤0,65 y máximo S/N<0,50 fuera de banda hasta π. Se utilizan 10.000 centros y radios 0,5/1/2/3/4/5. La anisotropía>0,30 es una bandera descriptiva, no rechazo automático. Los detalles descriptivos no se convierten en requisitos adicionales después de ver datos.

Se admite el primer intento certificado, entre cuatro como máximo, con registro de todos los intentos. Los parámetros reducidos de tests se marcan `test_only`: un test rápido no puede acreditar el tratamiento científico. Los artefactos se cargan y verifican por hash. Un fallo de certificado detiene entrenamiento científico; no se escoge la geometría que mejor aprende.

## ADR-004 — Aristas y propagación

**Aceptada; decisión científica conservada.** En régimen causal se representan arcos como `[source,target]`. Cada destino tiene seis orígenes kNN periódicos: exactamente 6N arcos, sin self loops, duplicados, simetrización ni reparación. Out-degree, reciprocidad y SCC se miden. Delaunay periódico es un régimen ecológico independiente, con selección por circuncentro y prueba de traslación; una construcción ambigua falla, no se poda para igualar E.

La agregación divide por vecinos entrantes vivos y produce cero si no quedan. Los pasos son síncronos y locales; no existe pooling global. La accesibilidad dirigida a T16 se calcula sin filtrar el dataset. La pérdida de acceso es un diagnóstico de transporte y no una incapacidad de razonamiento inferida.

## ADR-005 — Mundo externo y puertos

**Aceptada; decisión científica conservada con detalle operativo.** XOR/copy/fill se generan sin recibir el grafo neuronal. Fill usa BFS8 sobre el mundo lógico toroidal de cuatro adyacencias. Hungarian registra puertos mediante distancia periódica cuadrada y perturbación determinista independiente de marcas/targets. Se preserva el mapa para nativa/shuffle.

Todos los sitios registrados existen como direcciones y reciben coordenadas lógicas; sólo los roles activos tienen mask=1. Nodos internos reciben coordenadas físicas. Esta interpretación operativa de J0 se mantiene idéntica entre condiciones y se prueba contra leakage. La reubicación conjunta conserva un registro único; entradas/salidas por separado quedan sujetas a `B_SEPARATE_PORT_RELOCATION`.

## ADR-006 — Núcleo y matching

**Aceptada; decisión científica conservada.** d32, encoder25→32, LayerNorm afín, mensaje tanh con log1p(distancia), update100→64→32, residual0,1 y T16 ligado. G usa q común y adaptador rank10, T embedding5×4 y rank10 compartido, F embedding5×4 y cinco rank2 seleccionados. Ningún parámetro ficticio iguala las cuentas.

G tiene `12228+33o`; T/F `12244+33o`. Los 16 parámetros adicionales y los 512 MAC/nodo de diferencia activa T–F se informan. Inicialización por streams con nombres mantiene pesos compartidos iguales a training seed igual, sin depender del orden de construcción. El control positivo de recursos tiene 29 canales y +128 parámetros; no se mezcla con endpoints principales.

## ADR-007 — Semillas y datasets

**Aceptada; resolución operativa `O_SEED_KEYS`.** `src/larp/config.py` fija `SeedSequence([20261008, task_key, stage_key, split_key])`. Tareas: xor=1, copy=2, fill=3, resource=4. Fases: pilot=10, screen=10, confirmation=20, calibration=30, smoke=40, integration=50. Pilot y screen comparten deliberadamente namespace10 para comparar los mismos mundos a500updates, también en el screen ecológico. Splits: train=5001, validation=5002, test=5003. Estas claves derivan un entero uint32; no se usa `hash()` de Python.

Los datasets de un namespace/tarea/split son comunes a geometrías, marcas e inicializaciones. Confirmación tiene mundos nuevos frente a piloto/screen; calibración, smoke e integración tienen namespaces separados. Geometrías piloto1101–1103, inicializaciones2101/2102, confirmación3101–3108 y4101/4102, extensión3109–3116, centinelas6101–6103 y claves7101/7201 se conservan. HPO/calibración no se suman como réplicas confirmatorias. Orden de minibatch sin reemplazo y estado RNG se guardan en checkpoints.

## ADR-008 — Preregistro, procedencia y escritura

**Aceptada; resolución operativa.** Los siete presets y su índice SHA256 son inmutables. Un cambio de bytes exige nuevo protocolo/versionado, no editar el archivo para saltar un gate. La identidad de código agrega los hashes de fuentes Python, tests, pyproject, lock de dependencias, JSON de configuración y review científico principal, además de las versiones efectivas de Python/NumPy/SciPy/PyTorch/Matplotlib/NetworkX/psutil; los gates se invalidan si cambia esa identidad. Cada corrida guarda config resuelta, source hash/commit, hashes X/E/puertos/splits/optimizer/budget/init y labels separadas. Nativa/shuffle debe coincidir en todos los primeros hashes.

No se sobrescribe un directorio con configuración o código incompatibles; se crea una serie nueva. Guardados JSON/checkpoint se realizan mediante reemplazo atómico del archivo temporal. Reanudar utiliza el checkpoint y semillas originales; no reemplaza una seed desfavorable. Un checkpoint propio no se importa de fuentes externas. El checkpoint final del presupuesto es el endpoint; no se selecciona por test.

## ADR-009 — Dependencias y CPU

**Aceptada; resolución operativa.** El entorno reproducible inicial usa CPython3.13, PyTorch CPU y NumPy/SciPy/Matplotlib/NetworkX/psutil, sin frameworks de tracking o Graph ML. `requirements-lock.txt` congela versiones concretas, incluida la build CPU de torch; `scripts/install.ps1` crea/reutiliza `.venv` sin borrar datos, instala el lock y luego el paquete editable sin resolver dependencias adicionales. `pip check` y un manifest fechado verifican versiones realmente instaladas.

Este lock fija versiones, no hashes criptográficos de cada wheel ni el runtime completo del sistema. Un cambio de Python, SO/BLAS o acelerador crea otro entorno y debe registrarse. CPU tiene cuatro threads y float32; geometría float64. Coste extrapolado se etiqueta como estimación y se separa de mediciones.

## ADR-010 — Puertas y presupuesto

**Aceptada; decisión científica conservada.** Secuencia: auditoría→certificado/tests→núcleo/integración→200 updates copy de calibración→XOR de validación→copy focal. Antes de test se fija el presupuesto común:1000 updates, o500 para todas las condiciones si se activa el límite30min/run u8h/tanda. Si no aprende XOR accesible, se detiene la interpretación y la etapa posterior; no se cambia arquitectura para rescatar MHU.

Screen/fill/confirmación/lesiones/escalado/AB tienen interfaces y dry-runs, pero confirmación larga no se inicia automáticamente. Confirmación requiere datos/geometrías nuevos, rival fuerte seleccionado por validación, HPO común y preregistro congelado. Resolver un bloqueo de una rama no cambia por sí solo el presupuesto o el tratamiento.

## ADR-011 — Fallos y evidencia

**Aceptada; resolución operativa.** Un primer NaN/Inf se registra `NUMERICAL_FAILURE_UNVERIFIED`; no se imputa como evidencia científica. Sólo reproducción con mismo seed y exclusión de infraestructura permiten `TRAINING_DIVERGENCE` y score de sistema cero. Infraestructura se reanuda; invalidez de implementación detiene y se repara/versiona. Pruebas, certificados, calibración, smoke y piloto seleccionado no actualizan H1–H6 ni producen un posterior confirmatorio.

## ADR-012 — AB y ramas bloqueadas

**Aceptada con bloqueos localizados.** Se conserva Δ por geometría/init, prior μNormal(0,0,05²), sigmasHalfNormal(0,05), ROPE±0,02, cuadratura96×96 y sensibilidades especificadas. Bootstrap resamplea geometrías completas. H1–H6 son marginales y permanecen separadas del prior de μ; no se renormalizan ni se fabrican likelihoods de mecanismo.

`B_MATCHED_PAIR_DOMAIN` bloquea C3/mecanismo de ondas largas; `B_SEPARATE_PORT_RELOCATION` bloquea traslado separado; `B_D4_INTERVENTION` se activa ante anisotropía sistemática; `B_AB_ZERO_RESIDUAL` bloquea decisión cuantitativa ante residuos idénticamente cero. Se conserva cálculo diagnóstico cuando corresponde, con `architecture_decision_eligible=false`. El contraste primario nativa–shuffle no hereda automáticamente los dos primeros bloqueos. Las alternativas mínimas y sus efectos están en SPEC_AUDIT; ninguna queda aprobada por este ADR.
