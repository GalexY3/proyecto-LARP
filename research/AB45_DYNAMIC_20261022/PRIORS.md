# Priors acumulativos LARP · AB45 (apéndice no calibrado)

| ID | Hipótesis | Evidencia favorable | Evidencia adversa | Estado y falsador |
|---|---|---|---|---|
| AB45-P01 | Un solo selector supervisado domina a los competidores estáticos | TARGET gana 15/45 validaciones y Wine test | SHRINK gana 11/45, FPS 9/45; Breast y Diabetes favorecen variantes | Universalidad REFUTADA en este banco; replicar en datasets nuevos |
| AB45-P02 | Regularizar covarianzas puede mejorar con pocos datos | SHRINK mejora RMSE de Breast (0.2510 vs .2568) | IC bootstrap posthoc del diferencial incluye 0; Digits deteriora | ABIERTO contextual; hacer prueba independiente y competidores elastic net |
| AB45-P03 | Diversidad de variables puede mejorar adquisición bajo presupuesto | Diabetes FPS 1.0831 vs TARGET 1.1684 | Variables no poseen geometría espacial; los efectos dependen de modelo y única partición | CONDITIONAL; comprobar estabilidad por replicación externa |
| AB45-P04 | La geometría MHU proporciona mejora específica en imagen | Ninguna evidencia directa | Híbrido espacial de Digits no gana test; ni generador ni certificados MHU implementados | NO PROBADO; no inferir de esta campaña |
| AB45-P05 | Una política de selección por validación nunca empeora respecto al control fijo | Breast y Diabetes favorables; Wine empata | Digits pierde tras selección; validación 45x adaptativa | FALSE como principio universal; probar meta-selección sobre dominios externos |

**Procedencia:** `campaign.py`, `cycles.jsonl` (45), `decision_events.jsonl` (45), `SUMMARY.json`, `AUDIT_TEST.json`; última fecha 2026-10-22. Ningún posterior bayesiano numérico calculado. Etiquetas: exploratorio sobre datos observados; no efecto causal ni novedad científica demostrada. Conserva todos los priors LARP precedentes.
