# LARP — Cierre e índice de reutilización

**Fecha:** 17 de octubre de 2026, Europe/Madrid. **Estado operativo: ARCHIVED.**

## Decisión humana y alcance

El investigador aceptó la recomendación de cerrar la investigación activa sobre una ventaja neuronal general de MHU y encargó: «Elimina lo que no merezca conservarse […] pero todo lo reutilizable y cosas que hemos aprendido, que se quede. Simplemente la basurilla».

Se archiva la cartera activa de LARP, incluidas sus continuaciones propuestas. La razón es la ausencia de una ventaja específica suficientemente consistente para justificar más inversión abierta, frente al coste de identificarla y la disponibilidad de rivales simples. Es una decisión de asignación de recursos, no una demostración de imposibilidad ni una refutación universal de MHU.

No se ha ejecutado ningún entrenamiento, generación de geometrías, replay T2 o benchmark científico durante este cierre. Los documentos anteriores conservan sus estados históricos; sus expresiones «siguiente fase», «prioridad» o «rama activa» describen su fecha de redacción. Ninguna propuesta NOT_RUN queda activada por este archivo.

## Conocimiento que conservamos

| Pregunta | Qué aprendimos y con qué límite | Evidencia conservada |
|---|---|---|
| ¿Escalar hace crecer una ventaja MHU? | Scale3D v2 no muestra esa tendencia frente a LOCAL. En T2 a N32768: MHU 0,239350 y LOCAL 0,220206; MHU tiene 8,7 % más error. Hay ventanas favorables en otras tareas/tamaños; dos semillas no determinan una ley poblacional. | [Resultados Scale3D v2](../LARP_SCALE3D_V2_RESULTADOS_Y_REVISION_AB_2026_10_10.md), `runs/scale3d_v2/` y `artifacts/scale3d_v2_analysis_20261010/` |
| ¿Qué aporta organizar sensores? | La geometría aviar favoreció ciertos decoders locales; LOCAL retuvo buena parte de la mejora. Cambiar decoder y conocimiento del modelo puede reducir o invertir rankings. Full/local identifica procedimientos completos, no un efecto espectral residual puro. | [Muestreo](SAMPLING_PROBE.md), [oracle](SAMPLING_ORACLE.md), [rejilla y queries](SAMPLING_GRID_RESULTS.md) |
| ¿Información o decoder? | Rango, nulidad, conteos por canal y sesgo del decoder permiten explicar limitaciones. El suelo 0,10 es específico del modelo, conteos y queries continuas del diagnóstico; no es universal. Detectamos además aliasing en las queries históricas. | [Diagnóstico de información](../LARP_INFORMATION_DIAGNOSTIC_RESULTS.md), `artifacts/sampling_information/` |
| ¿Se aisló causalmente el espectro? | La búsqueda espectral v2 terminó NOT_IDENTIFIED, sin controles admitidos. Límites del constructor y restricciones incompatibles en un contraste no prueban imposibilidad geométrica ni inutilidad neuronal de HU. | [Factibilidad espectral](../LARP_SPECTRAL_FEASIBILITY_V2_RESULTS.md), [movilidad](../LARP_CONSTRAINED_MOBILITY_RESULTS.md), [vecindario y trade-off](../LARP_NATIVE_NEIGHBORHOOD_AND_TRADEOFF_RESULTS.md) |
| ¿Qué enseñó el fallo XOR? | Arquitectura, interfaz, disponibilidad de roles y entrenamiento pueden dominar un benchmark. La fase BALANCED superó su puerta local con dos semillas, con límites de generalización registrados; no demuestra una ventaja MHU. | [Fase 3](../LARP_PHASE_3_RESULTS_AND_NEXT.md), `docs/LEARNING_DIAGNOSTICS.md` y `docs/ROLE_GENERALIZATION.md` |
| ¿Qué aportó el rescate T2? | Las etiquetas exactas permiten invertir los factores reales no nulos; el ruido y los ceros cambian la estabilidad. Las mejoras de lectura narradas en el rescate no están verificadas por replay. El diagnóstico de composición es distinto de una prueba MHU. | [Dictamen del rescate](../LARP_RESCATE_T2_REVISION_Y_SIGUIENTE_PRUEBA_2026_10_11.md), `artifacts/rescue_review_20261011/` |

LOCAL también reduce potencia espectral baja en varios ensayos: su nombre no lo convierte en un control universal «sin HU». El generador grande CIC conserva una impronta de celda que limita la analogía con retina desordenada. Ambos límites permanecen explícitos en el informe Scale3D v2.

### Revisión de Argon del 17 de octubre

El material recibido se conserva en [external_research/argon_review_2026_10_17/received.txt](external_research/argon_review_2026_10_17/received.txt), junto con su recibo SHA-256. Su salida numérica es **reportada, no reproducida localmente**.

La inspección matemática detectó signo invertido en el estimador de gradiente: usa `diff = X0-X1`, `dp = p1-p0` y `+dp*diff`. En el límite local lineal e isótropo estima el gradiente negativo, cuyo error relativo ideal es 4; el predictor de gradiente cero tiene error 1. Los scores publicados alrededor de 3,2–3,6 no identifican precisión del gradiente correcto. No se recalcularon scores corregidos.

Tampoco se calcula una constante LBB ni se resuelve Stokes; la tarea de ondas selecciona una resonancia exacta contra la rejilla, y la cuadratura reutiliza modos optimizados por el generador. Una unión de especies HU independientes también puede ser MHU: la exclusión heterotípica es una propiedad adicional. La posible utilidad de coordinar especies y la utilidad específica de la supresión espectral son preguntas distintas. Esta revisión no actualiza numéricamente H1–H6 ni abre una nueva rama.

Antecedentes primarios consultados en esa revisión, todos revisados por pares:

- Jiao et al. (2014), *Avian photoreceptor patterns represent a disordered hyperuniform solution to a multiscale packing problem*, Physical Review E. [DOI](https://doi.org/10.1103/PhysRevE.89.022721). Define el fenómeno biológico; no acredita utilidad neuronal de nuestros modelos.
- Wei (2010), *Multi-Class Blue Noise Sampling*, SIGGRAPH / ACM TOG. [Página del autor](https://www.liyiwei.org/papers/noise-sig10/). Antecedente para uniformidad de clases y uniones; blue noise no equivale automáticamente a HU asintótica.
- Trask, Maxey y Hu (2018), *A compatible high-order meshless method for the Stokes equations with applications to suspension flows*, JCP. [DOI](https://doi.org/10.1016/j.jcp.2017.10.039). Antecedente para operadores compatibles sin malla; no evalúa nuestro tratamiento MHU.

## Herramientas disponibles para otras investigaciones

Se conservan en su ubicación actual para respetar imports, rutas y manifiestos. El siguiente inventario identifica componentes, no certifica su idoneidad para cualquier tarea nueva.

| Uso | Puntos de entrada | Precaución de reutilización |
|---|---|---|
| Geometrías tipadas, distancias periódicas y grafos | `src/larp/geometry.py`, `graphs.py`, `avian.py`, `avian_local.py` | Distinguir constructores nominal, aviar y CIC; un certificado finito no demuestra un límite asintótico. |
| Campos sintéticos y adquisición multicanal | `src/larp/sampling_probe.py`, `sampling_grid.py`, `data.py` | Revisar prior, normalización, bandas y queries antes de trasladarlos a otra tarea. |
| Reconstrucción fuerte, riesgo, rango y nulidad | `src/larp/sampling_oracle.py`, `sampling_information.py` | Separar información privilegiada del modelo, alcance del decoder y capacidad de adquisición. |
| Componentes multicanal en preparación | `src/larp/multichannel_decoder.py`, `tests/test_multichannel_decoder.py`, `configs/multichannel_pilot_v1.json` | Material sin seguimiento en Git al comenzar la limpieza. Conservarlo como trabajo en preparación, sin atribuirle un piloto completado. |
| Modelos, controles y ablaciones | `src/larp/model.py`, `baselines.py`, `interventions.py`, `robustness.py` | Mantener inicializaciones, mundos, presupuesto e interfaz comparables. |
| Supervisión y entrenamiento con presupuesto | `src/larp/runner.py`, `training.py`, `scale3d_runner_v2.py` | Comprobar ownership de procesos y rutas de salida; no reanudar cápsulas históricas completas. |
| Identidad, recibos y análisis | `src/larp/artifacts.py`, `analysis.py`, `reporting.py`, `artifacts/next_phase/` | Algunos auditores escriben en rutas históricas: inspeccionarlos antes de invocarlos. |
| Método científico y pruebas de software | `docs/charter/`, `docs/decisions/`, `tests/` | Preservar la diferencia entre fallo técnico, resultado nulo válido, exploración y confirmación. |

Los checkpoints y arrays de `runs/`, los estados exportados y los paquetes externos se conservan aunque estén ignorados por Git. Permiten revisar resultados sin repetir entrenamientos. Los resultados inválidos y logs de fallo también contienen aprendizaje.

`sols_corner/` se conserva completo como archivo creativo. Su utilidad científica no es criterio de descarte.

### Entornos e instalación

Se conservan `.venv` (CPU) y `.venv-scale` (CUDA), `requirements-lock.txt`, `scripts/install.ps1`, `scripts/setup_scale3d_cuda.ps1` y recibos de instalación/hardware. **El entorno CUDA depende del entorno CPU** mediante un archivo `.pth`: no retirar uno suponiendo que el otro es autónomo.

La limpieza propuesta comprende solamente cachés de bytecode y pytest. Pueden regenerarse al importar o ejecutar pruebas; los paquetes, fuentes y binarios permanecen instalados. La revisión automática bloqueó tanto el borrado recursivo como el borrado individual antes de lanzar los procesos, con el único motivo comunicado «blocked by policy». No se borró ningún archivo de caché. No se ejecutó una batería científica o de tests durante el cierre.

## Registro de limpieza y conservación

Inventario y comprobaciones en `artifacts/maintenance/2026_10_17_archive_cleanup/`:

- `cleanup_plan.json`: lista exacta de cachés autorizadas, archivos, tamaños y estado Git anterior.
- `preserved_before.json`: hashes de los archivos científicos, fuentes, documentos, tests y Corner existentes antes de intervenir; incluye archivos ignorados y sin seguimiento. Excluye `.git`, los entornos instalados y las cachés.
- `cleanup_result.json`: estado BLOCKED_BY_AUTOMATIC_REVIEW, cero archivos borrados y motivos comunicados por la herramienta.
- `verification.json`: comprobación posterior de integridad y de las únicas ediciones previstas en archivos existentes (`README.md` y `AGENTS.md`, para indicar el cierre).
- `cleanup_caches.ps1`: procedimiento revisable para ejecutar manualmente la lista exacta; sin `-Execute` solamente valida y muestra el plan. No fue ejecutado por el agente y no modifica resultados científicos.

Se conserva expresamente `artifacts/constrained_mobility/v1/search/active_trajectory.json.tmp`: sus 83 bytes registran un fallo histórico de I/O. Su campo `active: true` es un estado viejo, no prueba de un proceso ejecutándose ahora.

No se deduplican importaciones ni se recortan checkpoints: sus rutas pueden formar parte de evidencia y recibos. No se vacían carpetas externas al proyecto ni cachés globales del equipo.

## Cómo iniciar algo nuevo

Una nueva investigación puede reutilizar estos componentes con su propia pregunta, baseline, predicción discriminante, presupuesto y regla de cierre. No necesita conservar MHU como tema ni abrir todas las propuestas pendientes. Reabrir la hipótesis MHU requerirá un encargo nuevo y un contraste concreto que justifique su coste.

## Literatura y oportunidades incorporadas después del cierre

El investigador autorizó incorporar la revisión de aplicaciones científicas de MHU/HU del 17 de octubre. Se conservan la [recopilación](literature/MHU_HU_APPLICATIONS_2026_10_17.md), las [notas de muestreo y arrays](literature/MHU_HU_SAMPLING_AND_ARRAYS_NOTES_2026_10_17.md) y el [registro de fuentes](literature/MHU_HU_APPLICATIONS_2026_10_17.sources.json). Hay prototipos MHU publicados en imagen RGB y antenas compartidas; su evidencia no se traslada a las hipótesis neuronales de LARP.

La [ficha de oportunidades](projects/MHU_ALTERNATIVE_USES_CANDIDATES_2026_10_17.md) conserva tres candidatos PROPOSED_NOT_RUN: adquisición multicanal, arrays compartidos y diseño espectral de ondas. Incluye mecanismos, rivales, costes preliminares y reglas de cierre para una selección posterior. La [decisión de incorporación](decisions/ADR_2026_10_17_APPLICATIONS_LITERATURE_INCORPORATION.md) mantiene el archivo de la investigación activa y no reclasifica ningún resultado histórico.
