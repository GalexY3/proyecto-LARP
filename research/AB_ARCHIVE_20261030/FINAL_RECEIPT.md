# Recibo final de archivo y auditoría GitHub — 2026-10-30

**Repositorio:** GalexY3/proyecto-LARP. **Rama:** `research/ab-archive-audit-20261030`. **HEAD verificado antes del recibo:** `4605780440c5ff0a6cd354fd0467676d3000eb90`. La rama `main` no se ha fusionado ni modificado. Sin CI costosa.

## Igualdad remota con los originales
Con el árbol real de GitHub y el inventario local original se compararon **38/38 objetos Git**: 26 fuentes/CSV/JSON de archivo, 5 ZIP históricos completos y 7 archivos de estado/código/ledger. **38 iguales, 0 discrepancias** después de reparar los tres CSV. Los 5 ZIP son binarios idénticos por hash Git y SHA256.

Primer recorrido: 35/38. Las diferencias se produjeron únicamente en la conversión de CSV a texto:
- `CONTRASTS_CLUSTER_BOOTSTRAP.csv` (C01)
- `MSE_TEST_TABLE.csv` (C01)
- `C02_MEANS.csv` (C02)

Errata previa: `ERRATA_CSV_ENCODING.md`. Reparación con blobs Git creados desde base64 original y comprobación de hashes, commit `4605780440c5ff0a6cd354fd0467676d3000eb90`. No cambió ningún dato científico original.

## Auditoría AB-P A01–A20
**Primer run 19/20 PASS, A17 inválida por error de esquema del auditor**. Errata `ERRATA_A17.md`, código corregido y SHA congelado antes del segundo run. **Segundo run 20/20 PASS**. Los agregados de C01/C02/C04 y el tamaño de sus unidades originales cuadran. A14 registra que 32.400 predicciones C04 son 200 imágenes repetidas, no 32.400 observaciones independientes. A12 registra que los cinco filtros RGB virtuales forman una matriz de rango 3.

**La conservación es verificable; la validez científica externa no ha sido demostrada aquí.** Son 20 puertas de integridad AB-P postexposición, no 20 nuevos ciclos de investigación causal ni 20 teoremas originales. No hay nuevos hallazgos N1/N2/N3 ni cambios CT2.

## Comprobación portable
Ejecutar desde un checkout de esta rama:
```bash
python research/AB_ARCHIVE_20261030/verify_repo_archives.py
```
El script solo usa la biblioteca estándar de Python; comprueba ZIP, SHA256, CRC y manifiestos. Probado con una estructura de carpetas local equivalente: **5/5 PASS**. Descarga directa desde un clon de GitHub en un segundo equipo: **CLEAN_CLONE_NOT_VERIFIED**.

## Bibliografía y continuidad
Los archivos históricos conservan su procedencia y sus distinciones: MHU, LOCAL, CVT, versiones de geometría, controles de selección, modelos de cinco filtros y auditorías formales. La reparación de Poisson C01 sigue marcada `POST_EXPOSURE`; las pruebas de imagen no identifican ventaja universal MHU.

La rama contiene `packages/`, `ARCHIVE_INVENTORY.json`, `LEDGER_A01_A20.json`, `RESULTS_FIRST_RUN_19_PASS_1_FAIL.json`, `RESULTS_FINAL_20_PASS.json`, `INFORME_ARCHIVO_AB20.md`, `ERRATA_A17.md`, `ERRATA_CSV_ENCODING.md`, scripts y README. Ningún archivo original se ha reescrito silenciosamente.
