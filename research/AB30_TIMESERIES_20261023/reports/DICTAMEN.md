# LARP AB30-TS — dictamen provisional auditado (23-10-2026)

**30 ciclos A–J documentados; 5 bloques de 6 comparaciones; 6 series temporales reales históricas:** Nile annual (100), Sunspots annual (309), Mauna Loa CO2 weekly (2284), US real GDP quarterly log (203), El Niño monthly temperatures (732), quarterly interest rate (107). **Nivel científico 2/3: NO ACREDITADO. Replicación externa: NINGUNA.**

## Estimando y protocolo
Diferencia de MAE de predicción causal a un paso entre dos algoritmos con igual información pasada. Desarrollo 35–50% de cada serie; validación 50–75% para elegir la rama siguiente; tramo cronológico **final 75–100% no consultado ni computado durante validación**, abierto una sola vez tras publicar las cinco familias de contratos y cinco lecturas de validación. Todos los 30 outcomes G se comunicaron simultáneamente, negativos incluidos. El test es un **recontraste interno**, no observación futura independiente ni confirmación externa.

## Resultado de 30 contrastes
| Rama | A | B | Ciclos con ΔMAE(A−B)<0 en test |
|---|---|---|---:|
| B01 | Último valor (persistencia) | Media16 | 5/6 |
| B02 | Media4 | Media16 | 3/6 |
| B03 | Memoria exponencial α=.3 | Media4 | 3/6 |
| B04 | Tendencia lineal lag8 | Persistencia | 2/6 |
| B05 | Conjunto de tres expertos ponderado por últimos 12 errores | Mejor experto único elegido solo en desarrollo | **0/6** |

**13/30** comparaciones favorecen A; **29/30** mantienen el signo de validación en el último tramo; la única inversión ocurre en tendencia sobre Nile (inconclusa). Hay **20/30 p-values Holm descriptivos** inferiores a .05 calculados a partir de errores HAC por serie, pero esto NO implica veinte descubrimientos ni garantiza p válidos con ciclos/datos dependientes y efectivo N menor. Los intervalos bootstrap por bloques (1499) tampoco son una confirmación externa. Especialmente débiles: media16 no es un baseline profesional para PIB con tendencia, CO₂ o series estacionales.

## Auditoría adversarial
El código produjo las mismas predicciones en validación si se calculaban con series físicamente truncadas o completas. Cambiar adversarialmente todos los datos posteriores al instante t no modificó ninguna predicción hecha en t. El script posterior de informe tuvo un error en la asignación del ciclo frontera al bloque; el control de 6 ciclos por rama lo detectó y se reparó, sin alterar el motor ni los resultados.

Posteriormente se probaron controles AR(1) causal con últimos 32 pares y predicción seasonal naive lag52 CO2 / lag12 El Niño, seleccionados por resultados de desarrollo. Son **exploratorios post-test**: un baseline enriquecido mejoró a la referencia original en Nile (MAE 94.58 vs 95.97) y log PIB (0.00498 vs 0.00779), empató en tres series y perdió ligeramente en interés. El ensemble siguió siendo peor. No se implementaron ni compararon exhaustivamente ARIMA/ETS o expert-advice profesional, de modo que no declarar originalidad de mecanismo.

## Fases AB y gobernanza
Para cada C01–C30: A estimando, B hipótesis/rivales, C prueba antes del resultado, D anti-leak e invariantes, E validación+test numérico, F auditoría de causalidad y strong baseline, G recontraste interno cronológico, H actualización cualitativa de priors, I dictamen diferenciado, J decisión. El ledger A–J completo y vectores por observación están en el ZIP; nunca considerar otro estudio independiente a las seis fuentes entrecruzadas.

Fuente `src/engine.py` Git blob `756d9e5568571c6985298719938c3ca5b717b793`, SHA256 `cfc0a2d1097df213a09d33188bce6a265a2bf68b7876bcca5ef4140c829daa23`, registrada antes del primer ciclo tras una enmienda de prevención de filtración anterior a la ejecución. Preregistros `B01.md`, `B01_AMENDMENT.md`, `B02.md`…`B05.md`, `G_HOLDOUT_UNSEAL.md`, leídos cronológicamente. Un import retrospectivo de los vectores brutos no cambia la fecha de preregistro original; indicar si falta raw en el repo. Ambiente statsmodels 0.14.6, numpy 2.3.5, scipy 1.17.0, pandas 2.2.3, matplotlib 3.10.8. **CLEAN_CLONE_NOT_VERIFIED**.

## Decisión
**AB-DECIDE: CLOSE_QUOTA_30 / STOP_LOCAL.** El principal efecto es que la utilidad de información reciente depende del proceso físico/temporal, y un conjunto adaptativo mal calibrado puede diluir un baseline fuerte. Son principios conocidos y *dependientes de la tarea*. El siguiente tipo de evidencia, si se autoriza, debe ser flujo prospectivo externo y comparación con estacionales, ARIMA/ETS y agregación online competitiva, no otra batería de semillas históricas.

Archivo completo de la conversación: `LARP_AB30_TIMESERIES_20261023.zip` SHA256 `639d9efaac01f1679479c4db57a208c887419604a54abedb1cf9258a3ee45921`. **171 archivos**; incluye los 30 resultados exactos, series de pérdidas por fecha y A–J completo. GitHub archiva compromisos previos, resultados seleccionados y dictamen; si la serie temporal bruta permanece solo en el ZIP se mantiene ese déficit documental explícito.

## Antecedentes
Predicción temporal clásica (persistencia, smoothing, AR1, seasonality), previsión por combinación online; los resultados no introducen una teoría nueva. Datasets observados reutilizados de statsmodels y limitados al periodo histórico disponible.
