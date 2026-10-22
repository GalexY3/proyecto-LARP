# LARP VALUE30 — exploración adaptativa parcialmente programada (2026-10-22)

## Reproducir (Python 3.10+, numpy, scipy, sklearn, scikit-image, statsmodels, matplotlib)

Desde esta carpeta: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python experiment.py` **en una carpeta limpia o tras borrar `ledger.jsonl`**; los archivos existentes ya contienen la corrida histórica y se preservan. Para auditar sin reabrir el conjunto externo: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python tests.py`. Los experimentos de reparación `audit.py`, `stress_audit.py`, `temporal_pivot.py` son EXPLORATORIOS posteriores y pueden regenerarse separadamente.

El detector de una nueva escena en `experiment.py` abre `skimage.data.retina()` solo en C30, después de escribir `holdout_freeze.json`. La misma escena NO vuelve a ser desconocida en un segundo run de este mismo protocolo. Los reportes de auditoría que usan retina son post hoc.

Entrada: escenas de scikit-image disponibles localmente y el archivo de NOAA Niño 1+2 incluido en `statsmodels.datasets.elnino`. No distribuir ni reclamar licencia comercial de imágenes sin comprobar condiciones del proveedor.

**CLEAN_CLONE_NOT_VERIFIED**, experimentos GPU no ejecutados, ninguna validación en datos 3D. Ver dictamen completo y priors por estado.
