# LARP · AB 3.2.1 · 30 ciclos libres (22 octubre 2026)

**Tipo:** investigación exploratoria matemática y computacional. 30 preguntas distintas, 4 geometrías originales pareadas de Scale3D y 7 familias de patrones. No son 30 experimentos independientes. **Sin evidencia de originalidad 2/3 o 3/3.**

- `docs/INFORME_Y_SOLICITUD.md`: síntesis, hallazgos y solicitud de ocho ciclos condicionados.
- `docs/LEDGER_30_CICLOS.md`: treinta preguntas, falsadores, decisiones y siguiente paso.
- `docs/AB_LEDGER_C01_C30.json`: pruebas numéricas por ciclo legibles por máquina.
- `docs/PRIORS_APENDICE.md`: priors acumulativos con evidencia favorable, contraria y límites.
- `src/ab30_live.py`: código íntegro del benchmark y controles (con corrección de factor gaussiano aplicada).
- `src/build_report.py`: genera reportes y gráficas desde JSON.
- `data/orig_*.npz`: cuatro muestras originales recuperadas del paquete archivado, anteriores a este bloque.
- `data/cvt_refined_*.npz`: tres comparadores CVT anteriores a este bloque, no independientes de la selección previa.
- `data/final_verified.log`: ejecución completa después de la reparación del factor de varianza.
- `MANIFEST_SHA256.json`: huellas SHA-256 de los archivos al montar el paquete.

## Ejecución

```bash
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python src/ab30_live.py
OPENBLAS_NUM_THREADS=1 python src/build_report.py
```

**Dependencias:** Python 3.10+, NumPy, SciPy, Matplotlib. CPU; no CUDA. El código genera Sobol, LHS y retículas con semillas fijas. No ejecuta la implementación original de Li-Yi Wei ni entrena un Transformer.

**Advertencia AB:** Las 30 preguntas y sus mediciones comparten las cuatro mismas geometrías originales; se implementó una secuencia extensa de pruebas en un script, con bifurcaciones conceptuales C06, reparaciones C11 y C22, pero no un compromiso de nueva rama enteramente recomputada y commiteada después de cada resultado. Esta limitación se registra en el observatorio AB; las inferencias son exploratorias.
