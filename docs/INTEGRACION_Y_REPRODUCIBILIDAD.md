# LARP — política de integración y reproducibilidad

**Estado:** política documental del proyecto, 23-10-2026. Deriva de [AB 3.2.1/O1/O2/O3](https://github.com/GalexY3/Metodologia-AB); no declara eficacia causal de esta gobernanza.

## Fuente de verdad y estatus
GitHub guarda el registro versionado. Un merge documenta procedencia, NO acredita un mecanismo ni un descubrimiento. Mantener separados:
- `PROPOSAL`: hipótesis/protocolo sin ejecución.
- `ARCHIVED_EXPLORATORY`: datos y resultados condicionados; multiplicidad, incompletitud o baseline pendiente.
- `REPRODUCED_COMPUTATIONALLY`: ejecución desde clon limpio, con entradas y hashes verificables; no equivale a replicación externa.
- `EXTERNALLY_CONFIRMED`: contraste preregistrado en fuente independiente, paridad de controles y auditoría de selección; solo aplicable a la afirmación precisa.
- `INVALID_OR_REPAIRED`: fallo/errata mantenida en historia; no borrar sus versiones previas.

## Merge gate para cada campaña

1. **Identidad:** `campaign_id`, fecha, propietario, rama original, PR, fuente exacta, hash y versión de método AB.
2. **Contrato:** pregunta, estimando, hipótesis nula y rivales, controles competentes, código congelado y tiempos de commits. Distinguir freeze remoto previo de compromiso SHA local o commit retrospectivo.
3. **Datos y derechos:** procedencia/licencia, unit of analysis, preprocesado, NA, split, seeds, generador; no subir secretos ni información privada. `data not vendored` explícito cuando corresponda.
4. **Artefactos:** fuente, specs/preregs, JSON legibles por máquina, negativos, fallos, `AB-DECIDE`, actualización acumulativa de priors. Si solo hay ZIP del chat, registrarlo como **pendiente de archivado remoto**; el usuario no puede clonarlo desde GitHub.
5. **Invariantes y replay:** tests del instrumento, registros de fallos y reparaciones, pinning mínimo; prueba en clon limpio o `CLEAN_CLONE_NOT_VERIFIED`. Evaluación científica requiere más que `python -m py_compile`.
6. **Inferencia:** separar exploratorio y confirmatorio, reutilización de holdout, multiplicidad, tamaño del efecto, no confundir n seeds con réplicas externas.
7. **Mecanismo y novedad:** controles fuertes reales, no equivalentes nominales; nivel 2/3 solo tras contraste nuevo y replicación externa. Mantener `NO_VALIDADO` por defecto.
8. **Merges:** no sobreescribir `README.md`, priors o ledgers cuando una rama histórica esté divergiendo. Preferir **trasplante selectivo de blobs íntegros** con origen declarado, commits auditables, y cerrar/identificar PR obsoleto solo después de verificar que su aportación se conservó.

## Estrategia para ramas actuales
- PR #6 y #7: directorios propios, fusionados como archivo exploratorio; faltan algunos brutos versionados y clon limpio.
- Beijing: integrar solo el paquete observacional `research/AB45_BEIJING_20261022/` (nueve blobs del original), sin fusionar las versiones divergentes de `README` ni `docs/02_PRIORS_LARP.md`.
- PR #8 y #9: conservar en borrador; antes de merge, recuperar registros exactos desde ZIP, corregir árbol de artefactos y comprobar ejecutabilidad; en #9 preservar fallo de freeze remoto, irreparable retrospectivamente.
- PR #1–#4: cadena ancestral cerrada **sin merge**, con las ramas originales conservadas para rescate selectivo. No hacer `force merge` ni borrar ramas. El PR #5 quedó íntegramente trasplantado a `main` por PR #10 y cerrado como redundante. Rescatar evidencias y mejoras metodológicas aisladas, manteniendo autoría y procedencia.

## Comprobación y mantenimiento continuo
Tras cada integración: leer los archivos desde `main`, cotejar los SHA de los blobs originales y revisar `research/INDEX.md`. Actualizar el índice y el ledger de priors sin eliminar hipótesis desmentidas. Registrar un PR como fusionado solo si GitHub confirma `merged:true`.
