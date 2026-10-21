# LARP — Nuevo branching dinámico AB 3.2.1 (octubre de 2026)

Estado: **8 ciclos documentados de 30 autorizados**; todos los contrastes sustantivos son EXPLORATORIOS. No hay inferencia de novedad 2/3 ni 3/3.

Se recuperaron exactamente los dos generadores archivados `scale3d_geometry.py` y `scale3d_geometry_v2.py` del ZIP histórico `LARP_LOCAL_MHU_DISTRIBUCIONES_REALES.zip`. En `scale3d/` permanecen sin alterar. Repetición de optimización N=4096, 600 iteraciones, semillas 5201–5204, con LOCAL (sin término espectral) y MHU (con término espectral inversamente ponderado por norma²) desde **idéntica inicialización y labels** por semilla. No se eligieron semillas en función del resultado.

El comparador CVT es Lloyd independiente **por tipo** refinado en el bloque AB anterior, con tres geometrías de referencia 1701–1703. Se reutiliza el mismo conjunto de tres referencias en las cuatro evaluaciones; **no son cuatro réplicas nuevas de CVT**, ni un emparejamiento causal de condiciones iniciales. Es distinto de *Multi-Class Blue Noise Sampling* de Wei (2010), que no se ha ejecutado. El generador `LOCAL_derived` usado en el bloque anterior tampoco forma parte de las nuevas simulaciones.

## Archivos
- `prereg/BR30_DYNAMIC_20261021.md` del repositorio es el prerregistro original de proceso, escrito antes de la evaluación.
- `scale3d/scale3d_geometry*.py` son fuentes originales byte a byte.
- `generate_original.py`/`generate_arm.py`: generación por tratamiento (el segundo separa procesos por fallo de temporización del primer script; **no modifica** el optimizador).
- `evaluate_orig.py`, `summarize.py`, `graph_topology.py`: código de cobertura, espectro, reconstrucción y grafos.
- `larp/scale3d_train.py`: código original de clase `SpatialNetwork` y `Block`, sin cambios. `larp/scale3d_report.py` contiene solo un *stub* para satisfacer el import en la prueba CPU: **no es el reporter del experimento CUDA original** y nunca se invoca.
- `scale3d_cpu_probe.py`: adaptación experimental de tamaño reducido, ancho 48, 4 bloques, 90.119 parámetros. En la versión GPU original el ancho era 256 y 8 bloques, unos 4,8 millones de parámetros. No afirmar equivalencia de escala.
- `data/orig_520{1..4}.npz`: inicialización y posiciones con etiquetas por semilla.
- `data/{geometry_eval,predictive_eval}_*.json`: mediciones crudas por condición y mundo; `combined_summary.json`: resúmenes y contrastes pareados por semilla original.
- `data/topology_summary.json`, `data/mhu_validate_*.json`: observaciones de conectividad y auditoría finita de supresión espectral.
- `data/probe_*.json`: curvas reales de entrenamiento, evaluación reservada y tiempos.
- `docs/AB_LEDGER_DYNAMIC_C01_C08.md` y `docs/PRIORS_DYNAMIC.md` documentan las decisiones sucesivas y sus limitaciones.

## Reproducción (Python, NumPy, SciPy, PyTorch, Matplotlib)

```
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python generate_arm.py 5201 local 600
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python generate_arm.py 5201 mhu 600
# combinar .npz de cada brazo como en generate_original.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python evaluate_orig.py 5201
python summarize.py
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python graph_topology.py 5201 5202 5203 5204
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2 python scale3d_cpu_probe.py --name local --geom-seed 5201 --steps 220
```

**Nota:** el CPU probe requiere las referencias CVT archivadas del bloque previo y los `orig_*.npz`. Los tests usan datos Fourier sintéticos, sin sensores reales, sin evaluación neuronal OOD de lenguaje y sin comparación con GPT. Se conservaron resultados adversos y el baseline cero.
