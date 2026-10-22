# LARP · Evidence gate — 22 octubre 2026

**Estado:** prueba 2D de fuentes visuales observadas con tres canales derivados, no ensayo de sensores físicos heterogéneos. **STOP condicionado** respecto a la reivindicación ambiental, hasta disponer de datos auténticos de varias estaciones y comparadores pareados.

## Fuentes y límites

* Datos primarios: imágenes físicas reales incluidas con `scikit-image==0.26.0`. Entrenamiento: `camera`, `moon`; desarrollo: `grass`; evaluación abierta una vez: `gravel`, `brick`, `cell`, `microaneurysms`. Las regiones extraídas de una imagen **no son unidades experimentales independientes**.
* Cada uno de los tres roles procede de la misma imagen en escala de grises: intensidad, suavizado gaussiano (σ=1.3), gradiente Sobel escalado. **No existen tres sensores físicos independientes.**
* Estimando artificial del benchmark: combinación (0.5, 0.2, 0.3) de las tres medias completas del parche. Presupuesto: 16 lecturas en cuotas 4, 8, 4. Los modelos ven exactamente el mismo conjunto piloto y el mismo readout fijo o Ridge α=0.02.
* Entrenamiento: 160 parches por escena. Desarrollo: 160; cuatro escenas externas: 160 parches cada una. Diseños, semillas y roles están en `HOLDOUT_FREEZE.json`, producido antes de cargar los píxeles de test. Su hash figura en `TEST_RESULTS.json`.
* Se programaron seis condiciones (n piloto 16, 16, 32, 32, 96, 96), una apertura final y una reparación posterior del competidor GP. No hubo un branching de investigación completamente autónomo; ni se reivindican 30 ciclos.
* `GP` es una aproximación **propia** de selección avariciosa por covarianza de lecturas y objetivo. No es reproducción del algoritmo de Krause, de la selección CSSP GKS (2026) ni una comparación exhaustiva de parámetros. `repair_gp.py` amplía ex post el conjunto de candidatos a los 576 píxeles por rol.

## Reproducción

`python -m pip install numpy==2.3.5 scipy==1.17.0 scikit-learn==1.8.0 scikit-image==0.26.0`

Desde el directorio: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python bench.py`

Luego: `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python tests.py` (6 tests). La reparación no confirmatoria: `python repair_gp.py`.

`reference/value30_spectral.py` es la fuente original preservada de LARP VALUE30 y se incluye para que no dependamos de otra ruta o repositorio en el ordenador. No modificar para hacer que parezca prerregistrada.

**CLEAN_CLONE_NOT_VERIFIED**: comprobado en este entorno, no desde un segundo ordenador. Ver `DICTAMEN_EVIDENCE_GATE.md`, `PRIORS_APPENDIX.md` y `SOURCE_ACQUISITION_GATE.md`.
