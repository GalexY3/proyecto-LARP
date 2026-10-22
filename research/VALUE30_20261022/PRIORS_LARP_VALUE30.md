# Priors acumulativos LARP — nuevo bloque VALUE30 (no reemplazan los anteriores)

Fecha 22-10-2026. Procedencia `DICTAMEN_AB30_VALUE.md`, scripts/JSON de este paquete. Todos son cualitativos; no son Bayes factors ni posteriores numéricos.

| ID | Proposición / alcance | A favor | En contra / límites | Falsador / siguiente prueba | Estado |
|---|---|---|---|---|---|
| VAL30-R01 | COSI-SHRINK mejora la estimación espacial media RGB con pocas lecturas en escenas nuevas | C30 retina .001677 vs POWER-DIAG .001729 y SOBOL .001850 | Una sola escena nueva; cuota/objetivo adaptados antes a otros test; diferencias pequeñas | Múltiples escenas adicionales y comparadores KQ/GP equiparados | EXPLORATORIO_APOYO_ESTRECHO |
| VAL30-R02 | La covarianza CRUZADA entre tipos explica casi toda la ganancia | Algunos C20 y C29 favorecen COSI vs diagonal | C19 iguala con shrink0 y C21–C23 POWER-DIAG gana; efecto marginal modesto | Ablaciones cruzadas con roles naturales, costo y geometría aislados | DEBILITADO |
| VAL30-R03 | COSI domina al diseño bayesiano de sensores | 29 condiciones score medio fijo favorable a COSI | GP inicial optimizado para readout aprendido pero evaluado con media fija; el control no era pertinente; auditoría GP_FULL solo en dos escenarios | Implementar KQ/GP/column subset y optimizar al mismo estimador/budget | NO_VALIDADO |
| VAL30-R04 | COSI supera diseño empírico directo con escasos pilotos | C02-C03 frente a DIRECT, y estudio RGB previo con pilotos pequeños | DIRECT gana en C05–C07 a tamaños mayores; riesgos de leakage entre escenas | Validar en nuevas fuentes físicas y sobre varias semillas/repartos | APOYO_CONDICIONAL |
| VAL30-R05 | Regularidad espectral es universalmente útil en fenómenos físicos | Alguna evidencia sobre imágenes | En Niño 1+2, muestreo temporal trimestral .242 °C frente a cov/full .085 °C en periodo final; otro problema, pero falsador de universalidad | Replicar temporal multivariado/sistema de lectura real | UNIVERSALIDAD_REFUTADA |
| VAL30-R06 | Conteos de ganadores de 29 ciclos aportan 29 replicaciones | Ninguna | Mismos conjuntos de imágenes, grilla programada, parámetros adaptados | Replicación por escenarios verdaderamente distintos con unidades correctas | RECHAZADO |
