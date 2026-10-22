# LARP — laboratorio de investigación

## Estado actual, 22 de octubre de 2026

Se cerraron por indicación del investigador **10/30 ciclos dinámicos nuevos**, con veinte pendientes. No se encontró una ventaja específica de MHU en este bloque exploratorio. Se identificaron confounds de normalización y se probó un control de transporte del mismo clasificador entre representaciones lineales completas, con límites explícitos de presupuesto y condicionamiento.

- [Informe y decisión de cierre](research/AB30_CODEX_20261022/REPORT.md)
- [Diez ciclos: protocolos, evidencias y decisiones A–J](research/AB30_CODEX_20261022/LEDGER.md)
- [Importación verificada del laboratorio local: 539 archivos originales](legacy/local_lab_20261022/README_IMPORT.md)
- [Metodología AB y salvaguardas operativas O2](https://github.com/GalexY3/Metodologia-AB)

## Estudio anterior: 30 condiciones de contraste (2026-10-21)

## Lectura
- `docs/00_DICTAMEN.md`: principal; `docs/01_LEDGER_30_CICLOS.md`: auditoría A–J por condición; `docs/02_PRIORS_LARP.md`: priors nuevos y estado.
- `data/pilot_raw.csv` (880 filas); `data/pilot_summary.csv`; `data/confirm_focus_raw.csv` (80 filas); `data/confirm_focus_summary.json`.
- `src/run_br30.py` código del piloto (source lock en GitHub antes de experimentos); `src/confirm_focus.py` script confirmatorio; `data/geometrias/*.npz` entradas originales.

## Reproducción (Python 3.10+, numpy, scipy, pandas, matplotlib)
`OPENBLAS_NUM_THREADS=1 python src/run_br30.py --phase pilot --out data`
`OPENBLAS_NUM_THREADS=1 python src/confirm_focus.py`
`python src/build_report.py`

## Límites
Se usa un solo patrón geométrico original por algoritmo y nuevos mundos sintéticos Fourier. NO réplica biológica, NO inferencia sobre lenguaje, NO LLM, NO nueva arquitectura neuronal probada en este estudio. Tras la selección confirmatoria no se han abierto múltiples afirmaciones confirmatorias. Tres controles clásicos/espaciales (RANDOM, STRATIFIED, kernel por tipo) incluidos, pero falta Multi-Class Blue Noise optimizado, PNT++ y Set Transformer.

AB: https://github.com/GalexY3/Metodologia-AB
LARP privado: https://github.com/GalexY3/proyecto-LARP
