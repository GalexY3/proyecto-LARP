# LARP — Archivo de campañas y auditoría AB-P (2026-10-30)

Rama de conservación: `research/ab-archive-audit-20261030`. Es derivada de `research/ab-mhu-sisters-math-20261030`; **no está fusionada a `main`**. Los cinco ZIP son instantáneas históricas originales y no deben sobrescribirse para corregir resultados post hoc.

## Archivo recuperado

En `packages/` están los paquetes íntegros de MHU formal M01–M18, MHU hermanas S01–S20 y Visión C01, C02, C04. El `ARCHIVE_INVENTORY.json` guarda las huellas SHA256, blobs Git y rutas exactas. Los originales se han conservado con igualdad criptográfica de byte a byte. El código, los JSON y los CSV principales también pueden consultarse directamente en las carpetas de investigación.

## Comprobar conservación sin nuevas ejecuciones científicas

Con Python 3.10+ (únicamente biblioteca estándar), desde la raíz de un checkout de esta rama:

```bash
python research/AB_ARCHIVE_20261030/verify_repo_archives.py
```

El script comprueba hashes de los cinco ZIP, CRC, manifiestos internos y el número esperado de registros. La comprobación se ejecutó en una estructura local equivalente con **5/5** paquetes. No se ha validado un checkout limpio descargado desde GitHub en un ordenador independiente: `CLEAN_CLONE_NOT_VERIFIED`.

Para reproducir las comprobaciones de integridad del estudio usando NumPy y pandas y con los ZIP disponibles en las rutas de trabajo históricas, consultar `archive_audit_20.py` y `INFORME_ARCHIVO_AB20.md`. El archivo histórico original depende de rutas `/mnt/data`, por eso se incorporó el verificador portable anterior.

## Historial de auditoría

El auditor tenía una errata de esquema en A17 y obtuvo inicialmente **19/20 PASS**. Ambas fuentes y resultados están conservados en `RESULTS_FIRST_RUN_19_PASS_1_FAIL.json`, `ERRATA_A17.md` y el historial Git. Tras corregir A17 y congelar nuevo código, 20/20 PASS. **Son verificaciones AB-P de ingeniería, no 20 pruebas científicas ni 20 descubrimientos MHU.** El `LEDGER_A01_A20.json` registra A–J individual.

No hay nuevas conclusiones 1/3, 2/3 o 3/3, ni incremento de CT2. No se usó CI costosa, no se descargaron datos externos, ni se alteró ninguna fuente experimental histórica.

## Historial relacionado

- `research/AB_MHU_FORMAL_20261029/`: 18 preguntas matemáticas con informe y ledger íntegro recuperados.
- `research/AB_MHU_SISTERS_20261030/`: 20 cuestiones sobre MHU/LOCAL/CVT, informes, auditor, ledger íntegro.
- `research/AB_VISION_20261029/`: fuentes congeladas C01/C02/C04, JSON y análisis. C01 Poisson corregido post hoc explícitamente; no reescribirlo como confirmación.
