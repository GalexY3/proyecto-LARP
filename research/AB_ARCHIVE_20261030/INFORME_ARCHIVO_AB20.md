# Archivo e investigación de integridad — LARP, 30 de octubre de 2026

**Rama**: `research/ab-archive-audit-20261030` (derivada de MHU hermanas). No se ha fusionado a `main`. Autorización actual: hasta 20 ciclos. **20 puertas de auditoría AB-P A–J completadas, ninguna nueva validación científica MHU.**

## Qué se ha guardado

- Cinco archivos ZIP originales íntegros en `research/AB_ARCHIVE_20261030/packages/`: campañas C01, C02, C04, M01–M18 y S01–S20. Incluyen scripts y resultados brutos; por ejemplo C04 incluye 6,28 MB de predicciones originales dentro de su ZIP.
- Los dos ledgers matemáticos originales completos, además de los ledgers resumidos que ya existían, junto con el informe y auditoría M01–M18 y el informe S01–S20.
- C01 código original, reparación y auditor, JSON original y JSON reparado, CSV y resultados tabulados; C02 código, auditor, resultados originales, resúmenes y priors; C04 código congelado previamente, auditor, resumen y ZIP bruto.
- Manifiestos con SHA256 y huellas Git de los ZIP y fuentes. La identidad binaria de cada ZIP se verificó contra su versión local original.

## Auditoría nueva A01–A20

Primera ejecución: **19/20 PASS; A17 FAIL** por error del *auditor nuevo*, no del archivo original. La salida M01–M18 contiene las verificaciones en la clave `tests`; el código de auditoría buscaba los registros directamente en la raíz. El fallo se conservó y reparó prospectivamente para la segunda ejecución, sin alterar las pruebas ni datos originales. Segunda ejecución: **20/20 PASS**.

Hallazgos principales: los cinco ZIP tienen contenido íntegro y huellas correctas; los manifiestos M01–M18/S01–S20 coinciden con los miembros archivados; la reparación C01 modifica exclusivamente Poisson-disk; los resultados agregados de C01 y C02 se reconstruyen desde el JSON; C04 tiene 32.400 predicciones sobre **200 imágenes**, con seis repeticiones por imagen/método/condición; sus medias reportadas son consistentes; los cinco filtros de C02 tienen rango 3, por provenir de RGB; los dos verificadores matemáticos archivados tienen 18 y 20 controles respectivamente.

**Importante**: A16 auditó integridad y estructura del bootstrap C04, no ejecutó una nueva replicación estadística independiente. A17 y A18 comprobaron registros/identidades, no certificaron matemáticamente cada demostración. El control `verify_repo_archives.py` ejecutado sobre una estructura local análoga a un checkout pasó 5/5 ZIP; **CLEAN_CLONE_NOT_VERIFIED** para la descarga real de GitHub en otro equipo.

## Prerregistro y correcciones

- Contrato A–J: `467c5597b15d118dad68cd5f394ba1363798c1eb`.
- Fuente completa de auditoría antes del primer run: `b4d9c09e154a0139d1157107f32466a4141fc583`, SHA256 `cde86a8d56a3c2754d1d4933f4743ccf3e1db8228528e7766ea0db5f17de5264`. Existió un primer commit de transferencia errónea antes de este, documentado y corregido antes de ejecutar.
- Errata A17 tras los primeros resultados: `0f252940ac0027a1682313f49c3fea6e9f5a1004`.
- Fuente reparada antes de reejecutar: `bb5ab5b726c78d99ab459c509282e4cc98860184`, SHA256 `0ee43ff7e8b07ea925e1b2e5c4e3d83d6065d5ce7fd91afac52f37fc727dc6b3`.
- Primer resultado de 19/20 archivado: `26230613181f066009aa11471551203d77a4d2df`.

## Decisión y límites

**Resultado de archivado: CORRECTO en las comprobaciones delimitadas**. Se ha eliminado el problema principal de que archivos originales de esta conversación no estuvieran en GitHub. No se han cambiado resultados anteriores, y los dos intentos permanecen visibles.

**Resultado científico: sin cambios**. No se infiere superioridad universal de MHU, ni se modifica CT2 de las líneas experimentales por verificaciones de archivo. No se agregan N1/N2/N3. Los 20 controles son auditorías AB-P del mismo corpus, no veinte confirmaciones experimentales independientes. No he ejecutado entrenamiento o descargado datos externos de visión.

**Siguiente prioridad científicamente útil**: nuevos datos físicos de múltiples bandas y comparadores multiclass blue-noise reales; conservar la ruptura entre resultado de ingeniería y evidencia de utilidad funcional.
