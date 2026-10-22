# Archivo local LARP — importación curada del 22 de octubre de 2026

**Estado: ARCHIVED_CURATED_IMPORT.** Se conserva una instantánea del laboratorio local hasta el cierre del 17 de octubre y la incorporación bibliográfica posterior. Importar estos archivos **no ejecuta ni autoriza sus comandos históricos, planes NOT_RUN o entrenamientos**. La campaña actual del repositorio mantiene sus propios protocolos y versión de AB.

Selección: **539 archivos copiados byte a byte; 25,845,075 bytes**. Hay un [manifiesto](IMPORT_MANIFEST.json) por archivo con SHA-256, tamaños, origen relativo, criterio de selección e inventario de exclusiones. El source worktree tenía cambios propios sin commitear: su commit no representa por sí solo toda la instantánea; los hashes importados son la identidad de los contenidos.

| Grupo | Archivos | Bytes |
|---|---:|---:|
| `(root)` | 29 | 1,701,203 |
| `artifacts` | 191 | 12,902,870 |
| `configs` | 30 | 84,237 |
| `docs` | 67 | 628,810 |
| `runs` | 141 | 9,651,930 |
| `scripts` | 2 | 6,178 |
| `src` | 40 | 652,881 |
| `tests` | 39 | 216,966 |

Se preservan código propio, tests, configuración, locks, especificaciones, literatura, decisiones científicas y métricas compactas, incluidas observaciones negativas. Las seis geometrías aviares y las geometrías Scale3D seleccionadas son construcciones sintéticas propias, no datos biológicos. Se conserva una única excepción de tamaño justificada para el diagnóstico de información central; no se incluyen checkpoints.

**Puntos de entrada:**

- [Cierre y conocimientos reutilizables](docs/ARCHIVE_AND_REUSE_2026_10_17.md), cuando esté incluido.
- [Resultados y límites de Scale3D v2](LARP_SCALE3D_V2_RESULTADOS_Y_REVISION_AB_2026_10_10.md).
- [Diagnóstico de adquisición frente a decoder](LARP_INFORMATION_DIAGNOSTIC_RESULTS.md).
- [Revisión de aplicaciones MHU/HU](docs/literature/MHU_HU_APPLICATIONS_2026_10_17.md).
- [Código histórico](src/larp/) y [pruebas](tests/).

**Alcance:** no se reinterpretan resultados al copiarlos. Algunos informes preservan enlaces a archivos grandes, paquetes de terceros o rutas locales omitidos; no se afirma que todos sus comandos sean portables. Los scripts se inspeccionan y adaptan en una rama nueva antes de usarlos. La carta AB 2.1 se conserva como historia, no como sustitución de la metodología AB vigente.

**Excluidos y recuperables localmente:** `.git`, `.venv*`, caches, pesos/modelos, datasets grandes, trazas completas, paquetes ZIP/PDF recibidos y textos completos de artículos, piezas del Corner y correspondencia. Se copian revisiones locales de paquetes externos y sus referencias, sin redistribuir los paquetes originales. Los archivos de texto con coincidencias de datos personales o secretos obvios se omiten completos y constan por ruta y categoría en el manifiesto, sin publicar el contenido detectado. Los originales no se borraron ni modificaron.

Esta importación no cambia licencias ni autorías de las fuentes. No se aplican retroactivamente las garantías de un protocolo a datos previos ni se presenta un plan como experimento realizado. [Proveniencia de la selección](IMPORT_MANIFEST.json).
