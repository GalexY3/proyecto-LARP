# LARP / AB 3.2.1 — seis ciclos con UCI Digits (22-10-2026)

Investigación exploratoria. **No confirma 2/3 ni 3/3**. No equipara a Wei, Transformer ni GPT.

Ejecutar desde directorio raíz:

```bash
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle2_geometry
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle3_digits
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle4_train
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle5_roles
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle6_robust
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.cycle6_controls
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python -m src.build_dossier
```

Deps: numpy scipy scikit-learn torch matplotlib. GPU no requerida. Fuente `src/scale3d_geometry.py` y v2 recuperada de archivo LARP anterior; se conserva intacta. Dataset UCI Digits se puede redistribuir aquí desde sklearn; labels por muestra, splits y features cacheadas. 4 geometrías originales independientes y 4 semillas de modelo en baseline. Estadística de geometría n=4, no 1797.

Ver `docs/02_DICTAMEN_AB06.md` para interpretación, `docs/01_LEDGER_AB06.md` decisiones, `docs/03_PRIORS_AB06.md` priors.
