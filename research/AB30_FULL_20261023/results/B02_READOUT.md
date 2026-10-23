# B02 — Resultados exploratorios y decisión AB
Prereg GitHub 91942e3fc9e015d2775ba99b049c3c7145cf9aee; motor B02 SHA256 20e0c44f5bf813be9e6516fd2b3de00501c6034e028f7b8bfbc126eb912516fc, patch fuente commit 5b47dd4. Cuatro splits por ciclo, 96 consultas aleatorias anidadas/split, 0-1 loss, igual presupuesto de etiquetas reales por par. Todos los tests reutilizan datasets públicos históricamente expuestos.
| Ciclo | Mecanismo y rival | Δ MSE A−B | IC95 descriptivo cluster |
|--|--|--:|--|
| C06 | AIPW calibrated vs raw, mismos índices PPS | -0.0000031887 | [-0.0000188671,+0.0000124897] |
| C07 | AIPW raw vs constant, breast | -0.0000063572 | [-0.0000160689,+0.00000335445] |
| C08 | AIPW constant vs **inverted** proxy, breast | -0.0100553 | [-0.0133228,-0.00678772] |
| C09 | AIPW PPS focus 0.95 vs 0.30, wine | -0.000470168 | [-0.000932079,-0.00000825715] |
| C10 | HT PPS focus 0.95 vs 0.30, wine | -0.000474866 | [-0.00120769,+0.000257962] |
C06/07/10 inconclusos; C08 demuestra el negativo diseñado; C09 favorece focalizar acquisition en este dataset, sin separar el efecto general del modelo. Ningún ciclo acredita novedad 2/3. Contrastes seleccionados adaptativamente tras B01, comparaciones múltiples sin procedimiento confirmatorio.
**AB-DECIDE DRIFT02:** pivot a cambio de relación P(Y|X): intervenciones de etiquetas sobre registros observados; auditar si adquisición/calibración sobrevive error anti-correlacionado. Conservar los cambios de etiqueta como SINTÉTICOS y no replicación empírica.
