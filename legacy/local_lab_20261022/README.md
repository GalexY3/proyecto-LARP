# LARP v0.1

**Estado vigente — 17 de octubre de 2026: investigación activa archivada por decisión del investigador.** Se conservan resultados, código, checkpoints y materiales reutilizables. Las propuestas y comandos que siguen son documentación histórica; no constituyen trabajo pendiente autorizado. [Cierre, aprendizajes e índice de reutilización](docs/ARCHIVE_AND_REUSE_2026_10_17.md).

**Literatura incorporada el 17 de octubre:** [usos científicos de MHU/HU y límites de la evidencia](docs/literature/MHU_HU_APPLICATIONS_2026_10_17.md), con [fuentes estructuradas](docs/literature/MHU_HU_APPLICATIONS_2026_10_17.sources.json) y [tres oportunidades candidatas de reutilización](docs/projects/MHU_ALTERNATIVE_USES_CANDIDATES_2026_10_17.md). Estado: documental y PROPOSED_NOT_RUN. [Decisión y procedencia](docs/decisions/ADR_2026_10_17_APPLICATIONS_LITERATURE_INCORPORATION.md).

Banco experimental CPU para separar la organización espacial de marcas MHU de la geometría de unión, el wiring, la interfaz y la parametrización. El contrato científico es [LARP_v0_1_RESEARCH_ARCHITECTURE_REVIEW.md](LARP_v0_1_RESEARCH_ARCHITECTURE_REVIEW.md). El prompt de implementación gobierna las puertas de ejecución; el brief v2 aporta contexto.

Gobernanza prospectiva: [carta de investigación AB 2.1](docs/charter/LARP_RESEARCH_CHARTER_AB_2_1.md), adoptada el 8 de octubre de 2026. MHU es el punto de partida de un laboratorio de descubrimiento abierto; las especificaciones experimentales congeladas conservan su autoridad. [Sol's Corner](sols_corner/README.md) es un espacio opcional, ligero y aislado. [Decisión de adopción y límites](docs/decisions/ADR_2026_10_08_AB_2_1_ADOPTION.md).

**Cartera vigente (9 de octubre):** [decisión delegada de prioridad](docs/decisions/ADR_2026_10_09_MHU_PORTFOLIO_PIVOT.md). MHU pasa a candidato secundario; la pista principal estudia adquisición/comunicación multicanal con mecanismo y riesgo definidos. [Lote de 32 hipótesis y estrategia](LARP_HYPOTHESIS_BATCH_2026_10_09.md). La síntesis no ejecuta nuevos experimentos ni altera contratos, resultados o priors históricos.

**Inicio de la pista multicanal:** [diagnóstico de información y decoder](LARP_INFORMATION_DIAGNOSTIC_RESULTS.md) completo: 180 diseños, 216 celdas retrospectivas, 0,546 s numéricos; 20 pruebas relevantes aprobadas. Fine tiene un suelo oracle continuo sin ruido de 0,10 bajo el prior/conteos históricos, y la rejilla antigua distingue 54 de sus 56 coeficientes. Sin nuevos campos, geometrías, entrenamiento ni actualización de priors. [Próximo piloto con información/alcance separados](docs/projects/MULTICHANNEL_INFORMATION_PILOT_NEXT.md), especificación en preparación y NOT_RUN. La suite completa histórica de 294 pruebas no se repitió por esta ampliación aislada.

La figura `LARP_NETWORK_PREVIEW.png` ilustra una variante aviar posterior. Su generador no sustituye al tratamiento nominal preregistrado. La serie neuronal original usa `larp.geometry`; la continuación aviar y los ensayos de muestreo tienen módulos, protocolos y artefactos separados.

La continuación del 8 de octubre está en [LARP_CONTINUATION_RESEARCH_RESPONSE.md](LARP_CONTINUATION_RESEARCH_RESPONSE.md). La [fase 3](LARP_PHASE_3_RESULTS_AND_NEXT.md) añade cuatro corridas: BALANCED alcanza 100% en train/SS/UU con ambas semillas y supera su puerta local en 38,912 segundos de proceso completo. El panel antiguo conserva un fallo auxiliar en destino61; XOR sigue pendiente. H-R se actualiza débilmente; H1–H6/C permanecen intactos. Su suite histórica conserva **232 pruebas aprobadas**.

La [factibilidad espectral v2](LARP_SPECTRAL_FEASIBILITY_V2_RESULTS.md) cerró **NOT_IDENTIFIED**, seis inicios, 3.012 propuestas y cero controles admitidos en 126,728 segundos. La cota de varianza excluye el contraste espectral .50 con la nueva guarda ±5%; el contraste .25 no queda excluido por esa cota, pero no se construyó. La baja movilidad del buscador impide inferir imposibilidad geométrica o inutilidad neuronal de MHU.

La fase anterior, [movilidad y censo de exclusión](LARP_CONSTRAINED_MOBILITY_RESULTS.md), cerró sin operador viable: 2.280 propuestas neutrales, cinco swaps aceptados y cero ciclos. Un fallo de I/O dejó diez cadenas completas y dos sin iniciar; un suplemento explícito ejecutó sólo las dos pendientes. La colección es exploratoria con enmienda y conserva el estado inválido original. El censo exacto posterior halló13/10/2 ciclos que pasan sólo los cinco mínimos NN, con masa muy baja bajo el kernel. Coste científico conjunto111,093s de360s. Suite: **286 pruebas aprobadas**, con IPC final verificado aparte. No se abrieron scores ni se actualizaron H1–H6/C/H-R. La [auditoría completa y el piloto local/espectral](LARP_NATIVE_NEIGHBORHOOD_AND_TRADEOFF_RESULTS.md) se ejecutaron después: 95 vecinos cumplen todas las guardas (77 swaps, 18 ciclos), y el constructor de 18 cadenas/130 swaps se cerró. Suite actual: 294 PASS. El plan MIN-conditioned permanece NOT_RUN y ahora es contingente a una pregunta funcional; el nuevo orden prioriza Gram/riesgo/nulidad.

## Instalación

Windows, CPython 3.13, cuatro threads CPU. CUDA no es necesaria. El lock instalado y el hardware real se registran en `artifacts/installation/` y manifests. Para N400 se recomienda al menos 4 GB de RAM disponible; las fases grandes deben medir su propio consumo. N1600/6400 no se lanzan al instalar.

```powershell
Set-Location 'C:\Programación\LARP'
.\scripts\install.ps1
.\.venv\Scripts\python.exe -m larp --help
```

El instalador acepta `-PythonExe 'ruta\python.exe'` y `-Offline -Wheelhouse 'ruta'`; comprueba versiones exactas y `pip check`. Utiliza wheels CPU de PyTorch. Conserva entornos existentes compatibles.

## Puertas y comandos exactos

Los comandos de entrenamiento muestran un plan salvo que se especifique `--execute`. Cada puerta incluye hash de código, configs y contrato: cambiar cualquiera invalida puertas anteriores. Los presets están congelados en `configs/preset_hashes.json`. No modificar un preset para rescatar un resultado.

```powershell
.\.venv\Scripts\python.exe -m larp test
.\.venv\Scripts\python.exe -m larp validate-geometry --N 400 --seed 1101
.\.venv\Scripts\python.exe -m larp calibrate --execute --directory runs/series_cli_exitfix/calibration
.\.venv\Scripts\python.exe -m larp smoke --execute --directory runs/series_cli_exitfix/smoke
.\.venv\Scripts\python.exe -m larp pilot --task copy
.\.venv\Scripts\python.exe -m larp pilot --task copy --execute
.\.venv\Scripts\python.exe -m larp analyze --output artifacts/AB_initial.json
.\.venv\Scripts\python.exe -m larp report --run-root runs/series_cli_exitfix --output artifacts/report_current
```

`test` ejecuta toda la suite acotada, incluidas integraciones, y guarda JUnit/log. `validate-geometry` recertifica el patrón completo, sin reducir optimización ni límites. `calibrate` ejecuta cinco updates de warmup y 200 medidos de copy; sus tiempos extrapolados se etiquetan como estimaciones. `smoke` ejecuta cuatro corridas XOR G, consulta exclusivamente train/validación y registra accesibilidad dirigida a T16. Su umbral en validación accesible es .98 en todas las corridas. Si falla, copy/fill permanecen cerrados; cualquier revisión GRU/T32 requiere v0.1b.

`pilot` ejecuta doce corridas T, tres geometrías × dos inicializaciones × nativa/shuffle, con presupuesto común 1000/500 fijado por calibración antes de test. Un preflight verifica X, E, puertos, datasets, optimizer, presupuesto e inicialización común antes de entrenar. La única diferencia es la organización de marcas, con Hamilton conservado. El resultado del piloto es diagnóstico y no actualiza priors de arquitectura.

```powershell
.\.venv\Scripts\python.exe -m larp pilot --execute --resume
.\.venv\Scripts\python.exe -m larp resume --run 'runs\series_cli_exitfix\calibration\copy_native_T_g9001_s9002_u205_lr0.003_causal'
.\.venv\Scripts\python.exe -m larp verify-failure --run 'ruta\corrida' --execute
```

Reanudar conserva pesos, optimizer, RNG y cursor de datos. Una corrida completa con test abierto es inmutable. Un fallo numérico inicial queda `NUMERICAL_FAILURE_UNVERIFIED`; sólo reproducirlo con el mismo código/seed/data y descartar infraestructura autoriza score de sistema cero. Una interrupción o un límite de recursos no es evidencia contra MHU. No sustituir semillas desfavorables.

Las corridas ya ejecutadas requieren `--resume` al repetir el comando de su suite; para una ejecución nueva usar otra carpeta. `runs/calibration` y `runs/smoke` conservan la primera serie. `runs/series_cli_exitfix` es la serie actual, repetida con las mismas semillas tras corregir exclusivamente el código de salida del wrapper CLI. No suma geometrías ni inicializaciones independientes. La puerta XOR de ambas series falla; el piloto permanece bloqueado.

## Suite posterior, sin ejecución automática

```powershell
.\.venv\Scripts\python.exe -m larp fill
.\.venv\Scripts\python.exe -m larp screen --task copy
.\.venv\Scripts\python.exe -m larp screen --task fill --ecological
.\.venv\Scripts\python.exe -m larp freeze-confirmation --task copy
.\.venv\Scripts\python.exe -m larp confirm --task copy
.\.venv\Scripts\python.exe -m larp robustness --run 'ruta\corrida' --output artifacts/robustness --kind lesion
.\.venv\Scripts\python.exe -m larp scale --run 'ruta\corrida' --output artifacts/scale
```

Añadir `--execute` sólo cuando las puertas pertinentes estén abiertas. Fill/screen exigen completar primero copy. Screen causal incluye los cinco rivales T y G-MHU/G-HU, dos inicializaciones a 500 updates; comparte mundos con los checkpoints focales. El rival se elige por validación por tarea, con empate .005 por MAC y orden fijo. El screen ecológico fill es otro estimando: incluye NCA100 G en sitios lógicos exactos, cuatro vecinos, con coste declarado.

`freeze-confirmation --execute` ejecuta HPO igualada de tres lr, 300 updates, una geometría y dos inicializaciones por condición. Promedia nativa/shuffle como un grupo y el rival como otro; congela una lr común por tarea sin abrir test. `confirm --execute` ejecuta ocho geometrías nuevas × dos inicializaciones × tres condiciones a 3000 updates. La extensión única necesita análisis inicial inconcluso; usar `confirm --extension --execute --resume`, no reanudar su corrida individual fuera del plan ampliado. Ambas tareas y las guardas del contrato son necesarias para decidir stop/pivot/continue.

Robustez usa checkpoints congelados, ejemplos elegidos por hash, sin fine-tuning/reconexión. `--kind` admite random, lesion, radius, type, edge, relocation, m1 y functions; `--unprotected` separa el endpoint end-to-end. Las máscaras protegen puertos activos por ejemplo. La media neuronal se renormaliza por vecinos vivos; puertos retirados no fabrican predicciones. M1 colapsa funciones completas; relocalizarlas con pesos fijos es OOD y no identifica mediación natural.

```powershell
.\.venv\Scripts\python.exe -m larp analyze --records runs/confirmation_copy/results.json --output runs/confirmation_copy/analysis.json
.\.venv\Scripts\python.exe -m larp analyze --records runs/confirmation_copy/results.json --control grid_balanced --estimand architecture --output artifacts/rival_copy_analysis.json
```

AB exige panel preregistrado completo, hashes auditados y endpoint test. Usa efectos por geometría/inicialización, cuadratura y sensibilidad; mapas/bits/máscaras no son réplicas. Un efecto de una tarea no ejecuta automáticamente la decisión conjunta ni la actualización H1–H6. `artifacts/report/AB_history.json` conserva los priors iniciales mientras falte evidencia pertinente.

## Archivos y estado verificable

```text
configs/       siete perfiles inmutables, contrato y hashes
src/larp/      geometría/grafos, tareas/puertos, G/T/F, baselines,
               entrenamiento, runner/CLI, intervenciones, análisis/reportes
tests/         unitarios e integraciones acotadas
scripts/       instalación reproducible
docs/          auditoría, ADR, desviaciones, priors y estado real
artifacts/     certificados, logs, tablas/figuras y puertas
runs/          preregistros, manifests, mundos, curvas y checkpoints locales
```

El detalle ejecutado/pendiente y los resultados negativos están en [docs/IMPLEMENTATION_STATUS.md](docs/IMPLEMENTATION_STATUS.md). Los bloqueos de C3, puertos parciales, D4 condicional y posterior singular se documentan en [docs/SPEC_AUDIT.md](docs/SPEC_AUDIT.md); no se corrigen silenciosamente. Los ensayos de recursos tienen encoder29 y targets NMSE congelados, separados de copy/fill; no sustituyen sus endpoints.

## Continuación independiente y reproducibilidad

La evaluación previa está en [LARP_NEXT_PHASE_3D_MULTILAYER_AND_RESULTS.md](LARP_NEXT_PHASE_3D_MULTILAYER_AND_RESULTS.md): prioriza identificación espectral emparejada, preflight geométrico 3D y atención dispersa 2D antes de aumentar nodos/capas. El intento único de orientación de fase 4 quedó `INVALID_EXPERIMENT` por infraestructura antes de optimizar, con cuatro `NOT_RUN` y cero updates; no modifica resultados ni priors anteriores. Su remedio se verificó con procesos stdlib, sin reintento científico.

Los módulos posteriores tienen configuración, manifest y carpeta propios. Sus resultados no abren las puertas v0.1. Añadir módulos cambia la identidad global usada por aquellas puertas; los artefactos históricos se preservan. Para verificar la suite actual sin sobrescribirlas:

```powershell
$larpVerificationDir = 'artifacts/next_phase/tests_check_' + (Get-Date -Format 'yyyyMMdd_HHmmss')
.\.venv\Scripts\python.exe -B -m pytest -q --junitxml "$larpVerificationDir/junit.xml"
```

| Módulo / entrada | Evidencia existente | Informe |
|---|---|---|
| `learning_diagnostics` | `artifacts/learning_diagnostics/v1` | [Capacidad y distancia](docs/LEARNING_DIAGNOSTICS.md) |
| `transmission_probe` | `artifacts/transmission_probe/v1` | [Target e intensidad](docs/TRANSMISSION_PROBE.md) |
| `balanced_batch_probe` | `artifacts/balanced_batch_probe/v1` | [Política de minibatches](docs/BALANCED_BATCH_PROBE.md) |
| `gru_baseline` | `artifacts/gru_baseline/v1` | [GRU de referencia](docs/GRU_BASELINE.md) |
| `role_generalization` | `artifacts/role_generalization/v1` | [Ablación de coordenadas](docs/ROLE_GENERALIZATION.md) |
| `role_coverage` | `artifacts/role_coverage/v1` | [Currículo y validación común](docs/PHASE_3_ROLE_COVERAGE.md) |
| `role_orientation` | `artifacts/role_orientation/v1`, intento inválido cerrado | [Orientación con soporte físico fijo](docs/ROLE_ORIENTATION_PROTOCOL.md) |
| `avian` / `avian_local` | `artifacts/avian_v1` | [Generación y ablación](docs/AVIAN_GENERATOR_REPORT.md) |
| `sampling_probe` | `artifacts/sampling_probe/v1` | [Adquisición multicanal](docs/SAMPLING_PROBE.md) |
| `sampling_oracle` | `artifacts/sampling_oracle/v1` | [Estimador fuerte](docs/SAMPLING_ORACLE.md) |
| `sampling_grid` | `artifacts/sampling_grid/v1` | [Grid y consultas continuas](docs/SAMPLING_GRID_RESULTS.md) |
| `spectral_matching` (API; supervisor separado) | `artifacts/spectral_matching/v2`, búsqueda cerrada | [Factibilidad espectral v2](LARP_SPECTRAL_FEASIBILITY_V2_RESULTS.md) |
| `constrained_mobility` (API; supervisores separados) | `artifacts/constrained_mobility`, original inválido + suplemento + censo | [Movilidad y exclusión](LARP_CONSTRAINED_MOBILITY_RESULTS.md) |
| Vecindario nativo completo + piloto local/espectral | `artifacts/native_neighborhood`, `artifacts/local_tradeoff`; 136 vecinos/18 construcciones, cerrados | [Resultados auditados](LARP_NATIVE_NEIGHBORHOOD_AND_TRADEOFF_RESULTS.md) |

Los módulos de entrenamiento rechazan sobrescribir la ruta existente. `role_coverage` además exige preparación previa y rechaza una segunda ejecución de la misma cápsula; las cuatro corridas aprobadas están terminadas. No reanudar ni duplicar esta fase. Los módulos aviares y de muestreo verifican procedencia antes de reutilizar evidencia; cambiar una config congelada exige versión nueva. El control determinista especializado se ejecuta con `artifacts/diagnostics/role_transport_oracle.py` y se describe en [ROLE_TRANSPORT_CONTROL.md](docs/ROLE_TRANSPORT_CONTROL.md).

`artifacts/spectral_matching/tests_v2/` conserva 274PASS; `artifacts/next_phase/tests_v4/` conserva 256PASS y las tandas anteriores permanecen intactas. Para una comprobación adicional, usar una carpeta distinta. La [auditoría v4 registrada](artifacts/next_phase/provenance_audit_v4.json) verifica 17 manifests, 165 comprobaciones congeladas y 391 archivos históricos sin cambios; no entrenó ni reinterpretó el intento inválido como resultado científico. No reejecutar auditores que escriben esas evidencias históricas. El protocolo original de controles espectrales está en [INDEPENDENT_SPECTRAL_MATCHING_NEXT.md](docs/INDEPENDENT_SPECTRAL_MATCHING_NEXT.md), sin ejecución. La [decisión v2](docs/decisions/ADR_2026_10_09_SPECTRAL_LOCAL_VARIANCE_V2.md) añade una guarda de varianza continua y registra otro estimando; su [auditoría final](artifacts/spectral_matching/final_independent_metric_audit.json) preserva 435 archivos anteriores y verifica los seis estados diagnósticos. Las revisiones prospectivas de [3D/escalado](docs/projects/MHU_3D_SCALE_REVIEW.md) y [multicapa/atención](docs/projects/MHU_MULTILAYER_REVIEW.md) tampoco lanzan experimentos.

El supervisor geométrico `artifacts/spectral_matching/run_bounded.py` conserva calibración, preparación y búsqueda en cápsulas separadas. La cápsula v2 está terminada; no repetirla ni transferir su presupuesto restante. No hay controles admitidos que evaluar. La auditoría de métricas usa una implementación escrita por otro revisor; su ejecución final y el cierre de procedencia los realizó el agente principal. Las fórmulas, presupuestos y límites están en el informe v2.

El diagnóstico de movilidad conserva todas las propuestas rechazadas y sus130 desigualdades. Su cápsula `v1/search` sigue `BUG_INVALID`; `v1_io_supplement` contiene sólo las dos identidades no iniciadas, con código matemático y semillas originales. No repetir ni extender estos experimentos. La [auditoría combinada](artifacts/constrained_mobility/independent_combined_trace_audit_v1.json) valida los doce registros sin reclasificar el fallo; el [censo independiente](artifacts/constrained_mobility/independent_native_exclusion_census_v1.json) comprueba conteos y masa para sólo la familia de mínimos. Las reparaciones de I/O fueron probadas con workers stdlib, sin cómputo científico adicional.

Arrays y checkpoints grandes, extracción completa de la conversación y PDF consultado se conservan localmente y no se incluyen en Git. Los generadores/comandos y manifiestos permiten reconstruir y verificar su procedencia. [NEXT_PHASE_EXECUTION_SPEC.md](docs/NEXT_PHASE_EXECUTION_SPEC.md) conserva las decisiones y estados actualizados de las últimas series. Literatura y estatus de fuentes: [LITERATURE_NEXT_PHASE.md](docs/LITERATURE_NEXT_PHASE.md).

## Exploración GPU 3D y multicapa, 10 de octubre

Por encargo explícito se añade una rama de escalado de densidad: 1024–32768 nodos, ocho capas y 4.827.415 parámetros por modelo, comparando MHU, relajación local y geometría convencional aleatoria. El [protocolo independiente](docs/experiments/SCALE3D_V1_PROTOCOL.md) conserva el alcance y las limitaciones; la [calificación de memoria](artifacts/scale3d_v1/hardware_qualification.json) comprueba la mayor escala en CUDA. No modifica las fases antiguas. La rama usa `.venv-scale` (PyTorch CUDA), separada del entorno histórico.

La ejecución autorizada guarda estado en [progress.json](runs/scale3d_v1/progress.json), recibo del supervisor en [runner.json](runs/scale3d_v1/runner.json), y generará `SUMMARY.md`, `comparison.csv` y una figura al completar. Checkpoints y geometrías grandes permanecen locales. El supervisor detiene únicamente su worker tras un máximo de seis horas; no es una tarea recurrente.

V1 terminó en 578 s, con entrenamiento completo en 1024/4096 y cuatro geometrías grandes rechazadas por primera capa: [resultado parcial](runs/scale3d_v1/SUMMARY.md). La reparación expresamente autorizada abre [v2](docs/experiments/SCALE3D_V2_PROTOCOL.md), ponderando los modos por `1/|k|²` y auditando la banda completa sin cambiar el umbral. Su [calificación técnica](artifacts/scale3d_v2/qualification/result.json) usa semillas independientes. El nuevo estado de entrenamiento es [progress v2](runs/scale3d_v2/progress.json), y conserva fuente/modelo/tareas v1, con semillas nuevas y la mayor escala primero. La impronta CIC sigue siendo una limitación explícita para cualquier interpretación de retina desordenada.
