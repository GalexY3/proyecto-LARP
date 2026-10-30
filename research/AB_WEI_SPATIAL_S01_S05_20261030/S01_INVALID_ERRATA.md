# S01 — incidencia del instrumento, antes de reparación

Versión inicial congelada: prereg 3fc4b71888b662f6326cf571a738053a948a7059; código 2fc407de56ba22a0bc42576b0fe3c14f80e49613; resultado provisional 96fc59f4dc2e83a1b30cb6636ca411b86b3609a8.

El código usaba `row=line.split(',')` sobre CSV formal. **Error comprobado:** filas físicas 252 y 253 contienen `"Gulf of Mexico, FL"` como único Site_name, la coma dentro de comillas suma una columna falsa. Se reportaron `bad_shape=2`, `parsed_records=395` pese a 397 filas de observación. Es fallo del parser, no del conjunto de datos.

Estado del intento inicial: **INVALID_INSTRUMENTATION**, no usar sus contadores como definitivos. Registrar original sin modificar. **REPAIR** prospectiva y única tras exposición: introducir lector CSV RFC-style que admita comillas, doble comilla escapada y comas internas, cambiar solo la extracción de campos de encabezado y filas y conservar idénticos filtros A, B, C y umbrales. Congelar otro archivo con commit antes de reexaminar datos. Marcar resultado `POST_EXPOSURE_REPAIR_EXPLORATORY`, no confirmación independiente ni segundo ciclo. No lectura de outcomes de S02 aún.
