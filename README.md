# LARP — branching AB 3.2.1, 30 condiciones de contraste (2026-10-21)

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
