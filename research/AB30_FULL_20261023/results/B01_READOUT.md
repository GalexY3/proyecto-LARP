# B01 — Resultados exploratorios y decisión AB (posteriores a prerregistro 4fd5db6)
Seeds de partición 17,23,31,47; 96 adquisiciones aleatorias por seed, inferencia descriptiva con 4 clusters, datasets Digits previamente expuesto en LARP. Outcome MSE de estimación del riesgo poblacional, Δ=A−B (menor es mejor). No evidencia externa.
| Ciclo | A | B | ΔMSE | IC95 cluster |
|---|---|---|---:|---|
| C01 | SRS | top_uncertain naive | -0.0722632 | [-0.1333069,-0.0112196] |
| C02 | strat_prop | SRS | -0.000134051 | [-0.000259217,-0.000008886] |
| C03 | strat_equal | strat_prop | 0 EXACT | 0 EXACT; **INVALID, no contado** |
| C03R | strat_neyman | strat_prop | -0.000275759 | [-0.000564000,0.0000124814] |
| C04 | PPS AIPW calibrated | PPS HT | -0.00000677669 | [-0.000030218,0.000016664] |
| C05 | PPS Hájek | PPS HT | +0.0000674305 | [0.0000426525,0.0000922085] |
C03 se invalidó después del resultado porque la asignación igual/proporcional era la misma: se conserva error y nueva prereg C03R commit c1bd7b5 anterior a rerun. C01 confirma un sesgo conocido, no descubrimiento; C02 favorece estratificación sin extrapolar; C03R y C04 inconclusos, C05 refuta mejora esperada de Hájek en este contexto. No sobreinterpretar IC tras seis contrastes ni cuatro datasets semilla; múltiples dibujos de etiquetas comparten el mismo test.
**DRIFT 01 / AB-DECIDE:** pivotar del diseño muestral hacia CALIBRACIÓN DE PROXY y comparación entre estimadores usando iguales etiquetas; competir con control de media en validación e invertir el proxy. La rama B02 se congelará prospectivamente. JSON completo por adquisición se adjuntará al archivo reproducible; este commit es resumen auditable, no simulación de upload bruto.
