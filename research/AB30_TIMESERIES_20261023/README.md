# LARP — 30 ciclos AB de forecasting temporal · 23-10-2026

- **30/30 ciclos A–J** completos en el sentido documental y experimental, con G como recontraste cronológico interno, NO como replicación externa.
- **Seis fuentes empíricas diferentes:** Nile, Sunspots, CO₂ Mauna Loa, PIB real EE. UU. en log, El Niño mensual, tipos de interés.
- **Cinco ramas por mecanismo**, seis ciclos cada una: persistencia, ventanas de memoria, EMA, tendencia y agregación adaptativa.
- Los 30 contratos quedaron bloqueados progresivamente antes de validación y todos antes de la primera apertura del 25 % final.
- **Sin descubrimiento 2/3; sin demostración de ventaja del método AB**.

Leer `reports/DICTAMEN.md`, `reports/LEDGER_AJ_30.md`, `reports/SUMMARY_30.csv`, `reports/PRIORS_DELTA.md` y `reports/AUDIT_SUMMARY.json`.

**Rastreabilidad y reproducción:** fuente congelada en GitHub `research/AB30_TIMESERIES_20261023/src/engine.py` (SHA256 cfc0a2d1097df213a09d33188bce6a265a2bf68b7876bcca5ef4140c829daa23); scripts `src/stage.py`, `src/finalize.py`, `src/adversarial.py` adicionales. Los scripts de instrumentación posteriores no se hacen pasar por prerregistro. Reproducir con `OPENBLAS_NUM_THREADS=1 python src/stage.py 1 validation`, ... bloques 2–5, luego `test` todos solo si no se busca confirmación nueva (holdout ya consumido), `python src/finalize.py` y `python src/adversarial.py`. Requiere bibliotecas según `requirements.txt` y los datasets que vienen empaquetados en `statsmodels`.

**Archivado:** el ZIP contiene 30 JSON de validación, 30 de test, 30 vectores por fecha, 30 resultados enriquecidos, 30 specs derivadas, 30 A-J y auditoría. GitHub original contiene fuente, contratos y lectura de los cinco bloques; GitHub puede incluir resúmenes posteriores pero los vectores de tiempo originales deben importarse conservando el SHA y sin inventar prerregistro retrospectivo.