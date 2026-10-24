# AB20 — PIVOT instrumental a fragmentos ejecutables de defectos upstream reales

Fecha 2026-10-24. Autorización del usuario: **PIVOT 20 CICLOS** desde AB30 P04 PR #21 y AB55 BugsInPy. Esta investigación NO promete reproducir veinte proyectos enteros ni defectos de producción íntegros. Restricción detectada ANTES de ejecutar: no hay red/Docker/conda históricos en el ejecutor Python 3.13.5. El objetivo medible viable es **ejecutar fielmente el hunk mínimo buggy/fixed** de diez correcciones upstream identificadas por SHAs inmutables, en dos entradas cada una, dentro de una envoltura Python moderna. Es evidencia real del cambio de código, pero NO evidencia de que una instalación histórica del proyecto funcione. Cuando el origen estuvo ya inspeccionado para elegir el test, estado POST_EXPOSURE, no ciego.

## Diez reparaciones históricas (20 ciclos = 10 defectos × 2 estímulos; dependencia intra-defecto explícita)

C01–C02 tqdm BugsInPy #1 `tqdm/tqdm@c0dcf39b046d1b4ff6de14ac99ad9a1b10487512`: `tenumerate` start 42 / -3, comprobar enumeración inicial.

C03–C04 tqdm #3 `73962a47026dd980ac0758820efc9c41cbf938e0`: valor booleano de iterables generadores no dimensionables, no vacío / vacío.

C05–C06 tqdm #4 `964dee631d0ed30e2f799b42fc58ba5e73795a08`: `unit_scale` sobre `total=None`, escalas 10 / 0.5.

C07–C08 tqdm #5 `4f340697af69b71850aad496387c9c5aa1904136`: `disable=True` y ausencia de `total`, lista de longitud uno / vacía.

C09–C10 PySnooper #1 `cool-RR/PySnooper@56f22f8ffe1c6b2be4d2cf3ad1987fdb66113da2`: decodificación por defecto del fuente sin cabecera de encoding, `失败` / `mañana`; el antiguo codec ASCII usa errors=replace, por tanto debe generar sustituciones, no necesariamente excepción.

C11–C12 PySnooper #2 `814abc34a098c1b98cb327105ac396f985d2413e`: `custom_repr` par único `(list, fn)` / `(dict, fn)` y normalización a secuencia de reglas.

C13–C14 PySnooper #3 `15555ed760000b049aff8fecc79d29339c1224c3`: función `write` cerrada sobre ruta, `output_path` indeterminado antiguamente versus `output` correctamente; dos rutas temporales.

C15–C16 youtube-dl #1 `ytdl-org/youtube-dl@1cc47c667419e0eadc0a6989256ab7b276852adf`: operadores booleanos en `match_str`, `False` sin negación / `False` negado.

C17–C18 youtube-dl #3 `95f3f7c20a05e7ac490e768b8470b20538ef8581`: entidad HTML malformada `&a&quot;` / `&q&amp;`, patrón regex viejo/repair.

C19–C20 Cookiecutter #2 `cookiecutter/cookiecutter@90434ff4ea4477941444f1e83313beb414838535`: detectar 2 / 3 hooks válidos coexistentes con `find_hook` antiguo que retorna primero versus nueva lista. El orden explícito se fija; ejecutar solo la selección de rutas en wrapper, no la creación íntegra del proyecto.

## A–J por unidad

A: diferencia causada por la reparación upstream para un estímulo definido y las condiciones de un wrapper. B: H1 el hunk corregido produce salida esperada frente al buggy; H0 ambos equivalentes; rival fuerte comportamiento del paquete completo (NO se ejecuta), y test oficial añadido al fix (test oracle preexpuesto). C: congelar casos C01..20 con dos variantes por bug, 1 null benigno adicional por bug donde sea viable; comparadores old, fixed, null. D: Python 3.13, solo stdlib, sin red; fuente GitHub hunk y SHA de commit, wrapper declarado. E: ejecutar old/fixed en proceso aislado de manera determinista, guardar estado de excepción, salidas y logs completos por caso. F: auditar si cada wrapper replica realmente *todas* las condiciones del cambio; la ceguera es imposible porque el patch upstream ya ha sido leído al diseñar casos. G: prueba de repetición exacta en mismo host, no replicación independiente. H: prior de que 'metadatos != ejecución' actualizado solamente a 'hunk ejecutado', no a 'proyecto históricamente instalado'. I: grado 0 general por demostración regresiva de bug conocido; CT2 de rama instrumental comienza en 8, no suma al P04 10/100 ni a la hipotética CT2 del pivote. J: detener reivindicación 2/3, recomendar full historical runtime.

## Resultado esperado y límites

Métricas: `old_fails_or_diff`, `fixed_passes`, `null_old_eq_fixed`, `hunk_source_transcribed`, `full_repo_runtime`. Recuento válido = ciclos con hunk ejecutado para ambas revisiones; si falla paridad, marcar INVALID y reparación versionada, sin inventar. Los 20 son contrastes experimentales **de fragmentos de código real, NO 20 defectos independientes**.

No hay comparación justa de coste entre testing metamórfico, propiedad y tests profesionales ni oráculo ciego. No hay estimación causal de rendimiento para software de producción. Sin novedad N1 por defecto; N2=N3=0.

**Congelación O3:** este prerregistro GitHub precede a las ejecuciones. El código ejecutable completo aún no está comprometido antes del run, por lo que se etiqueta una brecha O3 hasta archivarlo; no atribuir a este prerregistro congelación remota de bytes.
