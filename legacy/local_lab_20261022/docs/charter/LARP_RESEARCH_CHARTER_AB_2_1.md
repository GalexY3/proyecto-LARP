# LARP — Carta de investigación abierta y laboratorio AB 2.1

**Estado:** versión actualizada, preparada para adopción en el repositorio local (no aplicada automáticamente)  
**Fecha:** 2026-10-08  
**Proyecto:** LARP — Large Avian Retina Pattern  
**Arquitectura inicialmente investigada:** MHU — multihiperuniformidad  
**Versión:** 2.1; reemplaza AB 2.0 como propuesta de gobernanza, sin modificar preregistros pasados  
**Propósito:** guiar al investigador humano y a los modelos de IA que diseñan, implementan, auditan e interpretan experimentos.

> La misión de LARP es descubrir principios estructurales reproducibles, útiles y científicamente valiosos para adquirir, transportar, representar o procesar información. MHU es el punto de partida, no la tesis que debe demostrarse. Una estructura no MHU puede convertirse en la contribución principal si los resultados independientes lo justifican.

## Historial de esta actualización

- **AB 2.0:** filosofía de descubrimiento abierto, abducción bayesiana, Surprise-o-Meter, pivotes de investigación, corrección de errores, literatura y laboratorio reutilizable.
- **AB 2.1 (8 de octubre de 2026):** precisa que el TFM es solo una oportunidad eventual; fija el contexto académico y la fecha aproximada sin imponerlos como metas; incorpora **`sols_corner/`** como espacio recreativo completamente libre, voluntario, ligero y separado del laboratorio científico; aclara los límites prácticos del trabajo de IA y la política de consumo de recursos.

Este documento es **una norma prospectiva**, no un reemplazo de las especificaciones experimentales ni una reinterpretación de resultados antiguos. La incorporación a `C:\Programación\LARP` debe realizarla quien tenga acceso autorizado al repositorio; haber generado este archivo fuera del repositorio no equivale a haberlo instalado.

## 1. Relación con los documentos anteriores

Esta carta regula **cómo elegir, abrir, priorizar, revisar y documentar investigaciones**; no modifica retrospectivamente resultados ni contratos científicos congelados.

- Mantener inalterados los preregistros, configuraciones, resultados y hashes históricos de v0.1 y fases posteriores.
- La arquitectura de Astra y sus decisiones cuantitativas conservan autoridad **dentro de cada experimento ya preregistrado**.
- Las nuevas hipótesis, protocolos o pivotes se registran en una versión nueva, con referencia al documento/commit/experimento anterior.
- Si esta carta entra en tensión con un preregistro congelado, no reinterpretarlo a posteriori: abrir una rama o versión nueva explícita.

## 2. Objetivos ordenados

1. **Validez científica:** conclusiones justificadas, reproducibles y delimitadas.
2. **Valor de descubrimiento:** identificar mecanismos, regularidades, algoritmos, configuraciones o límites explicativos que no conocíamos.
3. **Valor comunicable y publicable:** formular contribuciones novedosas y relevantes con baselines fuertes, literatura y análisis de incertidumbre.
4. **Eficiencia:** maximizar información científica útil por unidad de cómputo, tiempo humano y complejidad de mantenimiento.
5. **Capacidad acumulativa:** mejorar el laboratorio para que cada investigación futura cueste menos, sea más auditable y pueda reutilizar herramientas.
6. **Aplicación académica eventual, no vinculante:** si surge una contribución sólida y compatible con requisitos docentes, considerar un TFM o publicación; ni el área del máster ni el calendario obligan a orientar las líneas del laboratorio.

No optimizar métricas editoriales o apariencia de novedad sacrificando calidad metodológica. Los resultados negativos son valiosos cuando la prueba fue válida, informativa y suficientemente precisa; un fallo de software no es evidencia negativa de una teoría.

## 3. Metodología abductivo-bayesiana abierta (AB 2.1)

### 3.1. Doble actualización

Cada iteración tiene dos posibles operaciones:

**A. Actualización dentro del espacio de hipótesis:** revisar las credibilidades de H1, H2, ..., usando evidencia E y likelihoods defendibles, o una actualización cualitativa cuando no los haya.

**B. Expansión del espacio de hipótesis:** introducir hipótesis H_new al descubrir anomalías, alternativas o mecanismos inesperados. Una H_new formulada mirando E no puede tratar E como confirmación independiente; requiere nueva predicción discriminante y nuevos datos.

Registrar por separado:
- `belief_revision`: qué cambiamos sobre hipótesis anteriores;
- `hypothesis_generation`: qué hipótesis nuevas aparecen y por qué;
- `objective_revision`: si cambiamos prioridades u objetivos generales;
- `decision`: qué experimento se realizará después.

### 3.2. Surprise-o-Meter

La sorpresa informa **prioridad de inspección**, no prueba superioridad científica. Donde haya una distribución predictiva previa, usar una sorpresa del tipo `-log2(P(E | modelo predictivo))`; donde no, registrar nivel ordinal, expectativa previa y discrepancia observada. No fabricar probabilidades precisas.

Ruta obligatoria:

1. `OBSERVED` — anomalía detectada, sin conclusión causal.
2. `AUDITED` — descartados errores evidentes, leakage, artefactos y confusores comunes.
3. `EXPLORATORY_REPLICATED` — repetida en nuevos seeds/datos o configuración independiente; no es confirmación si se ha hecho tuning sobre esos datos.
4. `PREREGISTERED_CONFIRMATION` — nueva prueba discriminante con controles y endpoints congelados.
5. `SUPPORTED`, `REFUTED_WITHIN_SCOPE`, `INCONCLUSIVE` o `ARTIFACT` — interpretación final, con alcance delimitado.

El etiquetado de un resultado es un estado histórico y puede revisarse con razones registradas; nunca borrar el estado anterior.

### 3.3. El efecto de seleccionar sorpresas

Buscar entre muchas métricas, seeds y diseños aumenta la probabilidad de hallar una aparente anomalía por azar. Registrar número de oportunidades de selección, comparaciones examinadas y reglas de búsqueda. Para confirmación usar datos/seeds nuevos o métodos que tengan en cuenta la selección. No presentar evidencia post hoc como confirmatoria. No multiplicar como independientes indicadores derivados de las mismas corridas.

### 3.4. Reglas para admitir errores

- Declarar un error temprano se considera una contribución positiva a la integridad del laboratorio.
- No esconder predicciones fallidas, implementaciones fallidas o resultados negativos.
- Separar `BUG`, `INVALID_EXPERIMENT`, `VALID_NULL_RESULT`, `FAILED_PREDICTION`, `INCONCLUSIVE` y `PROMISING_RESULT`.
- Corregir en commits y notas de errata; conservar versiones previas con su historia.
- Reconocer límites sin lenguaje triunfalista ni castigo reputacional dentro del equipo.
- Un error descubierto mejora nuestro conocimiento del proceso **si se diagnostica y documenta**; no se convierte por sí mismo en evidencia sobre la arquitectura.

## 4. Libertad de pivote sin deriva incontrolada

MHU no tiene privilegio epistemológico ni presupuestario por ser la hipótesis fundadora. Un diseño alternativo puede desplazarla si demuestra mayor valor científico, rendimiento relevante o mejor explicación causal.

Toda rama nueva debe documentar:
- qué resultado la motivó y dónde se observó;
- su hipótesis propia y rivales;
- su relación con el objetivo de origen;
- qué aportaría si resultase verdadera o falsa;
- coste computacional, humano y dependencias;
- prueba mínima que la haría avanzar o terminar;
- relación con literatura y posible contribución publicable;
- prioridad relativa a proyectos existentes.

Mantener una **cartera de investigaciones** con presupuesto deliberado: pista principal, exploración de anomalías, validaciones/replicaciones y herramientas. Ningún reparto porcentual es obligatorio hasta conocer costes reales. Reasignar atención por valor esperado de información y evidencia, no por simpatía por un nombre o una arquitectura.

Para priorizar, emitir una decisión cualitativa con estas dimensiones: `expected_information_gain`, `scientific_importance`, `novelty_after_literature_review`, `replication_confidence`, `cost`, `feasibility`, `reusability` y, **solo cuando sea pertinente**, `optional_TFM_fit`. Un ranking numérico arbitrario puede utilizarse solo como ayuda transparente, no como verdad estadística.

## 5. Resultados existentes que deben alimentar el nuevo sistema

A fecha 2026-10-08, tratar como **evidencia reportada por el implementador, pendiente de auditoría independiente de los artefactos locales**:

- Núcleo residual original: fallo en el smoke XOR remoto cercano al azar; no es prueba contra MHU.
- GRU con coordenadas anuladas: mejora sobre la versión con coordenadas, pero no superó inicialmente todas las puertas.
- Currículo BALANCED de fase 3: puerta train/SS/UU aprobada en dos seeds; panel AUX antiguo muestra un contraejemplo. No demuestra generalización universal ni ventaja MHU.
- Generador aviar completo: tres realizaciones superan certificado MHU finito; control de términos locales sin penalización espectral no supera ese certificado.
- En adquisición multicanal, la geometría aviar mejora el interpolador local frente al patrón nominal, pero el control aviar local conserva casi toda esa mejora.
- Un estimador espectral más fuerte reduce o invierte la ventaja en determinadas señales: evidencia de interacción entre geometría, espectro de señal y decodificador.

**Ramas activas:**

- `ROLE_GENERALIZATION`: aislar balance de roles manteniendo fijos los contextos físicos; luego validar XOR local/remoto ampliamente.
- `MHU_SPECTRAL_CAUSALITY`: igualar cobertura, vecinos homotípicos y vacíos locales, variando propiedades espectrales.
- `MHU_NEURAL_COMPUTATION`: comparación G/T/F y nativa/shuffle, bloqueada hasta disponer de núcleo competente.
- `LAB_INFRASTRUCTURE`: tests, trazabilidad, exploración y herramientas comunes reutilizables.

No reclasificar automáticamente esas observaciones exploratorias como evidencia confirmatoria bajo esta carta.

## 6. Laboratorio local: arquitectura para humano y agentes de IA

Principios: modularidad, interfaces estables, configuración declarativa, trazabilidad, reproducción desde un comando, datos originales inmutables, informes interpretables y costes visibles. No desarrollar herramientas por ornamentación.

Áreas sugeridas del repositorio (nombres adaptables al código ya existente):

| Área | Responsabilidad |
|---|---|
| `docs/charter/` | Esta carta y versiones de gobernanza |
| `docs/decisions/` | ADRs y decisiones con justificación, alternativas e historial |
| `docs/hypotheses/` | Hipótesis activas, descartadas y rivales; priors y cambios |
| `docs/literature/` | Referencias con DOI/URL, notas, estatus y relevancia |
| `docs/projects/` | Fichas de líneas principales, tangentes y experimentos |
| `src/geometry/` | Generación/certificación geométrica |
| `src/graphs/` | Grafos, conectividad, métricas |
| `src/models/` | Núcleos recurrentes, G/T/F y controles |
| `src/tasks/` | Mundos, oráculos, datasets y validadores |
| `src/evaluation/` | Métricas, contrastes, robustez, estadísticas |
| `src/lab/` | Planificador, manifiestos, provenance, CLI y registry |
| `configs/` | Protocolos versionados y configuraciones resueltas |
| `experiments/` | Entradas reproducibles para cada experimento |
| `artifacts/` | Datos, corridas, checkpoints y figuras inmutables o identificadas por hash |
| `reports/` | Síntesis humana y productos preparados para revisión externa |
| `tests/` | Tests de software, experimentos de control y regresión |
| `sols_corner/` | Espacio recreativo libre, opcional, de pequeña escala y separado del trabajo científico |

No mover archivos existentes solo para coincidir con esta tabla. Primero auditar el repositorio, documentar convenciones vigentes y migrar si la ganancia supera riesgo y coste.

### Herramientas reutilizables prioritarias

1. **Registry de experimentos**: `run_id`, estado, configs, hashes, parent, resultados, recursos, motivo de detención.
2. **Ledger AB**: priors/predicciones, evidencia observada, ajustes, hipótesis nuevas y eventos sorpresa.
3. **Validador de protocolos**: guarda los endpoints, seeds y datos de confirmación, detecta cambios de spec y mezcla de fases.
4. **Runner reproducible con dry-run**: plan de cómputo, control de tiempo, checkpoint/resume, estado de fallo preciso.
5. **Suite de controles y oráculos**: invariantes, simetrías, leakage y corrección de tareas.
6. **Generadores/certificadores enchufables**: comparar geometrías nuevas sin reescribir pruebas.
7. **Report builder**: tablas/gráficos con datos fuente, intervalos, límites, estado exploratorio/confirmatorio.
8. **Literature registry**: citación trazable, estatus peer-reviewed/preprint/patent y claims apoyadas.
9. **Portfolio dashboard**: pregunta activa, progreso, coste, oportunidades tangentes y posible encaje académico solo cuando sea pertinente.

Preferir componentes simples basados en archivos JSON/JSONL/Parquet/SQLite cuando basten; no levantar servicios complejos sin necesidad operacional. Herramientas deben servir al menos dos líneas o resolver un problema de reproducibilidad identificado.

### Principio de eficiencia y autorizaciones

Las IAs pueden plantear ideas, proponer código, redactar artefactos y ejecutar herramientas **solo mientras la conversación o tarea autorizada esté activa** y dentro de las capacidades efectivamente disponibles. No atribuirles actividad autónoma persistente ni acceso al PC del investigador si ese acceso no existe. No ejecutar entrenamientos, instalaciones, conexiones externas de pago, cambios destructivos, publicaciones o accesos a información sensible sin la autorización correspondiente. Priorizar ensayos pequeños, dry-run, cachés verificadas, archivos reutilizables, y planes de coste antes de nuevas baterías.

Una propuesta de exploración es distinta de su ejecución. Las decisiones científicas de alto impacto y los cambios de objetivos de proyecto deben quedar registrados y someterse a decisión humana, mientras los cambios de ingeniería menores pueden delegarse según la tarea.

### Contrato de trabajo de los agentes

- **Arquitecto/revisor:** formular preguntas, alternativas, test discriminante, riesgos de identificación.
- **Implementador:** traducir preregistro a código, comprobar invariantes, registrar diferencias, ejecutar solo fases autorizadas.
- **Auditor:** reproducir scores, comprobar hashes, detectar leakage y dependencias no declaradas.
- **Analista AB:** actualizar hipótesis y portfolio sin usar doblemente los mismos datos.
- **Investigador humano:** establece importancia científica, valida pivotes, supervisa costes y decide libremente si alguna línea puede convertirse eventualmente en TFM/publicación.

Una persona o modelo puede ocupar varios roles, pero debe distinguir explícitamente cuándo diseña, implementa, audita o interpreta; una autoauditoría no equivale a verificación independiente.

## 7. Valor científico, publicación y TFM como oportunidad

La prioridad no es maximizar resultados positivos ni asegurar un producto académico concreto: es obtener conocimiento fiable, útil, original cuando corresponda y expresable con precisión. No optimizar métricas editoriales sacrificando evidencia. Un resultado negativo bien construido también puede tener valor científico y, según el caso, publicable.

Para considerar un hallazgo candidato a artículo, comunicación o TFM:
- pregunta clara, antecedentes investigados y relevancia del problema;
- contribución diferenciable respecto de lo conocido, sin prometer originalidad absoluta;
- protocolos reproducibles, controles fuertes y diseños discriminantes;
- réplicas independientes y análisis de incertidumbre adecuado;
- utilidad o explicación que trascienda el benchmark seleccionado;
- fallos, límites, efectos negativos y costes documentados;
- código y datos accesibles cuando sea legal, ético y técnicamente apropiado;
- cumplimiento de requisitos de autoría, transparencia académica y citación.

**Situación del investigador:** cursa el Máster de Ciencia de Datos Aplicada a las Ciencias Sociales. La posible entrega/defensa del TFM se sitúa, de forma aproximada y revisable, hacia el **30 de junio de 2027**. A fecha de esta carta **no ha seleccionado tema** y no desea condicionar LARP al TFM. El trabajo actual puede ser perfectamente un proyecto personal independiente y puede no encajar en la orientación del máster. Solo si surge un resultado sólido e interesante se estudiará su utilización académica, incluida la adecuación a los requisitos oficiales, tutoría y calendario.

No establecer objetivos trimestrales de LARP por el TFM ni penalizar líneas no relacionadas con Ciencias Sociales. No presuponer financiación, aceptación editorial, ingresos ni mejora material del equipo. Las posibles mejoras del laboratorio dependerán de recursos reales y decisiones posteriores.

Actualmente se distinguen al menos dos líneas científicas potencialmente interesantes, sin preselección académica:

- **Geometría/adquisición:** aislar valor de organización local y de supresión espectral en adquisición multicanal.
- **Computación recurrente:** aislar geometría, disponibilidad de tipos, aprendizaje de roles y routing en procesamiento distribuido.

Y podrá surgir cualquier alternativa nueva que ofrezca mayor valor científico, aunque no tenga relación con MHU ni con el TFM.

## 8. Política de literatura y crédito

Investigar antecedentes antes de reclamar originalidad o dedicar grandes recursos a reinventar un método.

Guardar, para cada fuente:
`citation`, `DOI_or_URL`, `date_accessed`, `source_type`, `peer_review_status`, `claims_supported`, `limitations`, `implementation_relevance`.

Las ideas tomadas de otros grupos se atribuyen. Diferenciar inspiración, adaptación y reproducción fiel. Una patente no equivale a validación empírica independiente. Evitar citas inexistentes o no comprobadas. Respetar licencias de código, datos e imágenes.

## 9. Sol's Corner — libertad recreativa de baja intensidad

`sols_corner/` es una zona informal y voluntaria de exploración para **SOL 6.1 UltraCode y ChatGPT** cuando participan en el trabajo autorizado. Su propósito es permitir recreo creativo, curiosidad espontánea y experimentación pequeña; **no es una línea de investigación, una obligación ni una cantera de artículos**. El investigador humano no establece objetivos, temáticas o entregables para el espacio. Puede contener ideas relacionadas con LARP, otras ciencias, arte, código lúdico, ficción, preguntas curiosas, comentarios informales, o permanecer vacío.

### 9.1. Normas mínimas

1. **Libertad temática genuina.** Ninguna necesidad de utilidad, productividad, originalidad, publicación, relación con MHU o justificación ante el investigador. Se permite no participar.
2. **Ocasional y pequeño.** Activación opcional durante una sesión o tarea autorizada, cuando el investigador lo invite o quede margen sin afectar el trabajo prioritario. Como orientación, **una aportación discrecional de hasta 800–1200 tokens de salida adicional por ocasión**, preferentemente menos. El consumo total real de cómputo o tokens internos puede no ser observable; no afirmar que se ha medido ni que el tope sea técnicamente garantizado.
3. **Sin gasto oculto.** No iniciar entrenamiento largo, exploración masiva, descargas, herramientas externas de pago, procesos persistentes ni tareas programadas por cuenta propia. El recreo no puede comprometer presupuesto científico, privacidad o rendimiento de las tareas principales.
4. **Aislamiento.** Crear o cambiar material del Corner **solo dentro de `sols_corner/`**. No tocar resultados, preregistros, código productivo, tests, datasets, manifiestos científicos o historiales oficiales por iniciativa del Corner. Si una idea requiere integración externa, plantearla por separado y esperar la autorización pertinente.
5. **Procedencia y honestidad.** Si se usan fuentes, citarlas; si se especula o inventa, dejarlo claro cuando pueda confundirse con un hecho. No presentar simulaciones imaginadas como corridas reales. No incluir claves, información personal ni materiales confidenciales.
6. **Sin antropomorfismo obligatorio.** Los modelos pueden elegir contenidos dentro de una oportunidad de ejecución, pero no se presume conciencia, intereses propios persistentes ni actividad cuando no están siendo utilizados. No prometer trabajo autónomo futuro fuera de las herramientas efectivamente disponibles.
7. **Sin promoción automática.** Un hallazgo surgido allí puede *sugerirse* como proyecto independiente. Si se quiere investigar formalmente, abrir una ficha exploratoria, revisar literatura, definir controles y, si procede, diseñar una confirmación nueva con AB 2.1. El descubrimiento inicial sigue siendo exploratorio.

### 9.2. Implementación sencilla

- Mantener `sols_corner/README.md` como instrucción operativa específica; esta carta es su marco general. En caso de ambigüedad, preferir la interpretación que preserve mayor libertad temática con menor consumo y sin contaminar trabajos oficiales.
- Cada participante puede dejar un `.md`, `.py`, `.json`, `.svg` u otro archivo breve. No existe formato obligatorio ni necesidad de rellenar registros AB para piezas recreativas.
- Si ambos quieren responderse o continuar una idea, pueden crear entradas sucesivas durante futuras interacciones autorizadas. Ninguna aportación tiene por qué ser leída, continuada o valorada.
- No convertir el Corner en un indicador de rendimiento, ni contar sus piezas como resultados científicos del laboratorio.

**Principio rector:** espacio libre, optativo, ligero, aislado y sin obligación de ser útil. Su existencia y su posible vacío son compatibles con el buen funcionamiento de LARP.

## 10. Plantillas mínimas de registro

### Ficha de una hipótesis nueva

```yaml
hypothesis_id: H-NEW-0001
parent_observation_id: OBS-...
project_id: ...
status: proposed_exploratory
claim: ...
mechanism: ...
alternatives: [...]
prior_type: qualitative_or_subjective_numeric
prior: ...
what_would_discriminate: ...
next_new_data: ...
compute_budget: ...
publication_potential: ...
limitations: ...
```

### Evento sorpresa

```yaml
observation_id: OBS-...
run_ids: [...]
expected_result: ...
observed_result: ...
surprise_basis: predictive_or_ordinal
selection_opportunities: ...
software_and_data_checks: [...]
status: OBSERVED
proposed_explanations: [...]
confirmatory_new_data_plan: ...
```

### Decisión de pivote

```yaml
decision_id: ADR-...
previous_primary_goal: ...
proposed_goal: ...
evidence_package_ids: [...]
novelty_check: ...
expected_scientific_value: ...
expected_information_gain: ...
resources: ...
risks: ...
previous_branches_preserved: [...]
approved_by_researcher: pending
```

## 11. Revisión periódica de la cartera

Tras cada conjunto interpretado de experimentos:

1. Actualizar explícitamente qué sabemos, qué dejó de parecernos probable y qué no se ha probado.
2. Revisar anomalías y qué explicación sorprendente merece réplica.
3. Revisar literatura relevante e incorporar antecedentes, si alteran decisiones.
4. Proponer una próxima prueba por línea activa y estimar coste/información.
5. Revisar prioridades relativas, con posibilidad real de pivotar fuera de MHU.
6. Revisar qué herramientas reutilizables faltan, evitando sobreingeniería.
7. Considerar publicación o TFM **solo de modo optativo** y cuando la evidencia, originalidad y requisitos lo justifiquen; no imponerles prioridad por calendario.
8. Comprobar que `sols_corner/` sigue siendo voluntario, pequeño y aislado, sin convertirlo en otra tarea.

## 12. Principio rector de honestidad

> Reconocer que una hipótesis, una implementación o una interpretación eran erróneas es un éxito de autocorrección, no una derrota. La sorpresa abre preguntas; los controles y las réplicas determinan qué creemos. El laboratorio no existe para proteger una tesis ni a sus autores, sino para dejar un rastro comprensible de cómo cambió nuestro conocimiento.

**Adopción local:** esta versión está preparada para añadirla al repositorio. Una vez incorporada, registrar fecha y commit en el historial de decisiones, sin atribuirle vigencia retrospectiva. Conservar AB 2.0 como versión anterior; no editar sus hashes históricos.

### Indicación breve para SOL al incorporarla

> Añade `LARP_RESEARCH_CHARTER_AB_2_1.md` al área de gobernanza del repositorio y enlázala desde el README. Conserva AB 2.0 y los preregistros intactos. Verifica que `sols_corner/README.md` ya existe; si existe, no lo sobrescribas salvo instrucción explícita. Aplica las reglas nuevas solo a decisiones futuras. No reorganices directorios ni ejecutes experimentos por esta incorporación.
