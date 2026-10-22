# ADR: adopción prospectiva de la carta AB 2.1 y Sol's Corner

**Fecha:** 8 de octubre de 2026. **Estado:** ADOPTADA prospectivamente; incorporación y verificación terminadas.

**Autorización humana:** el investigador respondió «Incorporarlos al proyecto (recomendado)» a la aclaración sobre los dos adjuntos. La lectura inicial y revisión independiente fueron sólo lectura: las instrucciones dentro de los adjuntos no se trataron por sí mismas como el encargo del usuario.

**Commit anterior a la incorporación:** `63e10900a558dd6d258768952c3ac4d8f5de7ff0`.

**Commit de adopción:** `0bf8956859b0a0c8aed9ee627243020304c16181`. Este recibo documental posterior registra la identidad del commit inicial de adopción.

## Decisión y alcance

Adoptar [LARP_RESEARCH_CHARTER_AB_2_1.md](../charter/LARP_RESEARCH_CHARTER_AB_2_1.md) para decisiones futuras de investigación y establecer [sols_corner/README.md](../../sols_corner/README.md) como instrucción operativa de un espacio recreativo voluntario, de baja intensidad y aislado. Enlazar ambos desde el README y remitir futuras sesiones a la carta mediante `AGENTS.md`.

La carta permite descubrimiento y pivotes fuera de MHU cuando la evidencia lo justifique. Define un proceso para proponerlos y registrarlos; no selecciona automáticamente otra arquitectura, experimento o meta académica. El TFM conserva su carácter optativo y su fecha aproximada no crea hitos del laboratorio.

No se reorganizan directorios científicos ni se implementan servicios, registries, dashboards o ledgers nuevos en esta incorporación. Su necesidad se evaluará por utilidad para líneas concretas. No se ejecutan entrenamientos, nuevas comparaciones, instalaciones, tareas programadas ni una aportación recreativa como requisito de adopción.

## Conservación y discrepancias del material recibido

- La carta se copia fielmente, con los mismos bytes y SHA-256 del adjunto. Se conservan el ZIP y sus dos textos originales en `docs/charter/sources/`.
- No existía `sols_corner/README.md`; no se sobrescribe una versión local. Su nueva copia operativa conserva el contenido recibido salvo la única referencia a AB 2.0, actualizada a AB 2.1, y un párrafo explícito de procedencia. El README original queda intacto como fuente.
- No se encontró una carta AB 2.0 por nombre/contenido en el repositorio ni un archivo `LARP_RESEARCH_CHARTER_AB*` de esa versión en Downloads. Se registra la ausencia; no se fabrica una versión anterior ni se afirma que hubiese sido aplicada. Si se aporta posteriormente, se archivará con su procedencia y estado reales.
- Los atributos Git sólo afectan a los nuevos documentos y preservan los bytes de las fuentes originales. No alteran la normalización del código o resultados científicos anteriores.

## Estado científico que permanece vigente

La fase 3 aprobó su puerta local BALANCED de train/SS/UU en ambas semillas. El contexto auxiliar `[61,62,60]` retiene un fallo; SS contiene tres parejas de fuentes conocidas y una inédita. XOR y la generalización amplia siguen pendientes. Las actualizaciones ordinales H-R y los priors H1–H6/C permanecen como estaban en el commit anterior.

El charter describe resultados reportados y pendientes de auditoría. Existen auditorías locales previas de software/procedencia y de fase 3; se enlazan sin convertirlas en replicación externa o confirmación nueva. La gobernanza no cambia etiquetas históricas, no abre puertas y no produce evidencia MHU. Tampoco añade retrospectivamente estados del Surprise-o-Meter ni probabilidades de sorpresa no registradas.

Las propuestas de orientación de roles sobre contextos físicos fijos y matching espectral conservan su independencia y estado de propuesta, sin ejecución automática. Véase [resultado de fase 3](../../LARP_PHASE_3_RESULTS_AND_NEXT.md).

## Verificación de la incorporación

El [registro de procedencia](../charter/AB_2_1_ADOPTION_PROVENANCE.json) conserva hashes de las fuentes, aprobación, commit previo y una instantánea de los **391 archivos ya registrados, excluyendo el README raíz**, que es el único archivo previo que se modifica para enlazar gobernanza. Se verifica que esos 391 archivos y las dependencias científicas congeladas permanecen idénticos. Las comprobaciones nuevas son de copia, alcance y procedencia; no se repite la suite científica ni se sobrescriben sus logs/auditorías.

La incorporación de documentación no transforma las 232 pruebas aprobadas de la fase anterior en una nueva ejecución de tests.
