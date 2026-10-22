# BJ45 — datos de estaciones reales, 45 decisiones AB adaptativas
Fecha 2026-10-22. Estado: EXPLORATORIO, novedad científica NO acreditada (1/3).

- `weekly_observed.json`: 12 estaciones × 209 semanas × [PM2.5, PM10, NO2, O3], con valores faltantes nulos y recuentos de horas. Agregados de CSV UCI/Beijing 2013–2017, CC BY 4.0; incluye blobs fuente.
- `run_campaign.mjs`: fuente congelada antes de ejecutar; 45 decisiones secuenciales y test solo al cerrar el bloque. Node.js 20+, sin bibliotecas externas.
- `campaign_results.json`: condiciones, evidencia de validación, siguiente decisión, todas las selecciones por brazo y cinco evaluaciones temporales finales.
- `verify_results.mjs`: invariantes de cadena, identidad de las condiciones, presupuesto por selección y semántica de test.
- `simple_mean_posthoc_audit.json`: control básico adicional sobre un test YA ABIERTO; no confirmatorio.
- `DICTAMEN.md`: resultados, limitaciones, crítica bibliográfica y decisión AB.
- `PRIORS.md`: BJ45-R01 a R05, sin alterar priors anteriores.

En un clon: `node research/AB45_BEIJING_20261022/run_campaign.mjs` y `node research/AB45_BEIJING_20261022/verify_results.mjs` (ejecutar verificaciones después de generar archivo).
Para reconstruir el CSV semanal desde fuentes externas: las cabeceras del CSV llevan comillas; fechas UTC; medias por semana desde 2013-03-01, mínimo 84 horas válidas por estación-canal-semana. El repositorio incluye el agregado y SHA de los orígenes; NO afirma reejecución independiente sobre hardware distinto.
