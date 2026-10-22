# Incidencia retrospectiva de procedencia — LARP AB branching C01–C30 (22-10-2026)

**Naturaleza:** registro retrospectivo y errata de gobernanza, NO prerregistro ni certificación experimental.

**Protocolo aplicable:** AB 3.2.1 + O1 (A16) + O2 (freeze–run), repositorio `GalexY3/Metodologia-AB`.

## Qué ocurrió

En una campaña de LARP del 22-10-2026 se comunicó un cierre C01–C30: C01 procedía de un bloque previo y C02–C30 correspondían a 29 contrastes nuevos. Los artefactos se entregaron en la conversación como `LARP_AB_BRANCH30_COMPLETE_20261022.zip`. No se realizaron commits en GitHub durante los ciclos, aunque AB-O1 y AB-O2 los exigían para cambios informativos y trazabilidad de ejecución.

Este commit se hace **después** de las ejecuciones y NO remedia su ausencia de un bloqueo inmutable de protocolo/código anterior a cada prueba. Los `prereg/C02.json`–`prereg/C30.json` internos al ZIP son contratos **locales**, no compromisos temporales GitHub verificables.

## Identificación de artefacto local (no alojado aún en este repositorio)

- ZIP: `LARP_AB_BRANCH30_COMPLETE_20261022.zip`.
- SHA-256 del ZIP íntegro, calculado al registrar esta incidencia: `50827e21b1d06bd49fba584b558806b85ad49767269585c9babe3012ac3123e9`.
- 83 entradas en el ZIP; incluye `run_ab30.py`, contratos `prereg/`, resultados `cycles/`, `AB_LEDGER_C02_C30.md`, `DICTAMEN_C01_C30.md`, `PRIORS_CORRECTED.json`, `AUDIT_QC.json`, figuras e indicadores de integridad.
- Código principal (SHA-256 indicado por `AUDIT_QC.json` local): `f8c7202ddbab87cf7c25fd5c094885084704e3fec26caf28ed783650fadfa256`.
- Reparación C09 (SHA-256 indicado en el mismo archivo): `cef3c12a95c67e850a035b5a557b8c7e97b6e29abfb8bf1feb949c28b144b3c2`.

## Estado científico sin elevar indebidamente la evidencia

- `AUDIT_QC.json` informa de 29 ciclos nuevos y 30 intentos incluyendo el inicial inválido de C09.
- Se conservó C09_INITIAL_INVALID y la reparación posterior en el ZIP; la corrección no acredita que hubiera un preregistro remoto congelado.
- Sin confirmación externa; sin holdout genuinamente ciego; sin certificación MHU para nuevas geometrías; sin verificación de clon limpio.
- Los 30 ciclos contados y las cifras exploratorias comunicadas **no** son 30 estudios independientes ni un descubrimiento LARP 2/3.
- Antes de cualquier afirmación reproducible desde GitHub es preciso incorporar código, datos autorizados, contratos y resultados exactos en este repositorio, verificar hashes y ejecutar una reproducción de clon limpio.

## Incumplimiento y decisión

**INCUMPLIMIENTO:** código, contratos, decisiones, priors y resultados nuevos de la campaña no fueron depositados en GitHub a medida que surgían, como exigen O1 y O2. Se desautoriza presentar este commit como `freeze–run` anterior a la ejecución.

**Decisión AB-DECIDE:** `REPAIR_GOVERNANCE`. No alterar los resultados originales ni crear commits retrodatados; archivar los ficheros existentes de forma íntegra y realizar congelaciones verificables **antes** de futuras ejecuciones.

Este archivo es una **evidencia de auditoría de procedencia**, no un sustituto del expediente completo ni de la validación científica.
