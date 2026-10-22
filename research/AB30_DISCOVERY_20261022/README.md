# LARP — AB30 novelty: 30 ciclos buscando una contribución 2/3

**Fecha:** 2026-10-22. **Resultado:** no hay 2/3 acreditado. Se hicieron 30 contrastes D01–D30, en cinco bloques de seis cada uno, y seis auditorías V01–V06 posteriores NO contadas en el cupo.

## Por dónde leer

- [Dictamen científico](reports/DICTAMEN.md): resultado, anomalías, límites y decisión.
- [Ledger A–J, 30 ciclos](reports/LEDGER_D01_D30.md): contratos individuales, hipótesis rivales, datos, actualización cualitativa y decisión.
- [Priors acumulativos, ocho entradas nuevas](reports/PRIORS_DELTA.md): procedencia, evidencia a favor y en contra, falsadores; NO reemplazan priors históricos.
- [Estimaciones D01–D30](results/RESULTS_30_ROUNDED.csv) y [auditoría V01–V06](results/AUDIT01_ROUNDED.csv). Cifras **redondeadas**, no raw exacto por semilla.

## Congelaciones GitHub previas a cada etapa

- Fuente: [compromiso de SHA previo](SOURCE_LOCK.md), commit e782483. SHA256 del motor exacto: `df7e95fa9bb96c8d65b9634b5188dc9ea587d364f6257dcaa8ba8d7d6a42e443`.
- B01: 79be1a2, B02: 0247871, B03: 2f042e1, B04: 0335b86, B05: f50e603.
- AUDIT01 (no contabilizada): 5ffe0db.
- [Código completo comprimido gzip+base64](src/experiment.py.gz.b64) incorporado DESPUÉS de ejecutar, commit 0c72aaf; su descompresión produce exactamente el SHA256 comprometido previamente. Diferenciar compromiso criptográfico temprano y disponibilidad del contenido.

## Clon y código

Para recuperar el motor en un clon:

```bash
cd research/AB30_DISCOVERY_20261022
base64 -d src/experiment.py.gz.b64 | gunzip > src/experiment.py
sha256sum src/experiment.py
python -m pip install numpy==2.3.5 scipy==1.17.0 scikit-learn==1.8.0
OPENBLAS_NUM_THREADS=1 python src/experiment.py prereg/B01.json results/B01_replayed.json
```

Repetir para B02–B05 y AUDIT01. El script reconstruye datos brutos por semilla y estadísticas desde especificación. **CLEAN_CLONE_NOT_VERIFIED**; las ejecuciones originales y los JSON completos brutos se encuentran en el ZIP del chat, NO en GitHub. Guardar el archivo por SHA, no presentar resúmenes redondeados como raw.

## Límites epistémicos

Diseños 2D toroidales con 5×12 nodos, optimizadores espectrales de un número FINITO de frecuencias. **No** se certifica HU asintótica. No se ejecutó el método multi-class blue-noise auténtico de Wei. Digits es dataset reutilizado adaptativamente en LARP. Los intervalos son exploratorios y los varios contrastes no generan control del error confirmatorio. Las 30 entradas A–J no constituyen replicaciones externas.

**Árbol:** B01 espectro → B02 covarianza → B03 OOD/no-periodicidad → B04 fallos → B05 downstream → AUDIT01 contra rivales fuertes. En esta rama GitHub se ha cometido protocolo, fuente identificada por hash, pruebas, estimaciones y lecciones; en el ZIP se conserva el expediente completo.
