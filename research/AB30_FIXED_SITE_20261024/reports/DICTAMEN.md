# Dictamen científico — AB30 Fixed-site Multicolor (24-10-2026)

## Hipótesis y diseño
¿Puede la recoloración de 100 posiciones fijas con cinco modalidades, optimizando energía Fourier de bajo número de onda por tipo, mejorar la cobertura y reconstrucción después de fallos de modalidades? Tres políticas, idénticas 100 posiciones y cuotas [40,24,16,12,8] por seed: recoloración espectral A, permutación aleatoria B, greedy-farthest-first C. La comparación primaria adversarial A−C y secundaria A−B. E 4 seeds, G 8 seeds sintéticas sin independencia de campo.

## Resultados reproducidos
| Bloque | Pregunta | A mejor que C, G | A mejor que B, G |
|--|--|--:|--:|
| B01 C01-C06 | estructura baja k | 4/6 | 6/6 |
| B02 C07-C12 | cobertura | 2/6 | 6/6 |
| B03 C13-C18 | reconstrucción IDW | 3/6 | 6/6 |
| B04 C19-C24 | Fourier ridge | 2/6 | 4/6 |
| B05 C25-C30 | transferencia a señales/bases diferentes | 2/6 | 6/6 |

La supresión espectral es funcionalmente insuficiente: supera el control aleatorio, pero suele perder frente a una asignación que prioriza cobertura espacial. La geometría de sensores está apareada por seed. El sexto campo de B04 tiene modo (3,0) **fuera** de la base fija, no llamarlo modelo correctamente especificado.

## Auditoría posterior en imágenes observadas (no pertenece a los treinta ciclos)
Camera, coins, moon, page, horse, text de scikit-image. Preespecificada en GitHub después del resultado de C30 pero antes de correr esta auditoría. IDW con solo unión de modalidades raras (20 sensores), spectral vence farthest-first **3/6** imágenes. Se probaron también ocho semillas, dos máscaras y dos estimadores, todos archivados en ZIP. No es réplica independiente ciega, imágenes públicas y borde artificialmente toroidal.

## Originalidad, certificación y confianza
Wei, SIGGRAPH 2010, ya publicó `Multi-Class Blue Noise Sampling` e incluyó disposición de sensores. Heck et al. 2013 estudia estructuras espectrales y aliasing. Retina aviar Jiao et al. 2014 tiene multihiperuniformidad certificada de especies biológicas. Nuestros patrones son **candidatos espectralmente balanceados a escala finita**, no MHU matemáticamente certificada ni red neuronal.
**CT2=10→11→9→12→9→8→7/100**, menor después del control geométrico y auditoría real. **N1+1** operacional por discrepancia espectro→calidad funcional (LARP-1-005), sin originalidad bibliográfica; N2=N3=0.
No p-values confirmatorios: nE4, nG8, semillas/layouts compartidos entre hipótesis, múltiples comparaciones y diseños sintéticos. Faltan contraste con implementación directa Wei 2010, tamaños crecientes, latencia/entrenamiento a paridad y aplicación sensórica real.

## Reproducibilidad y gobernanza
Código exacto SHA256 `cae397a9e83a88a807ad5b77faeec1cc5a3ffdd8c682c6ee5822851fe8d2b156` congelado en GitHub ANTES de ejecución y tres Git blobs comprobados. 30 contratos A–D también precomprometidos `503d2c9`. Desde ZIP original de 50 archivos se regeneraron exactamente los 30 JSON E/G y `SUMMARY_30.json`. Archivos brutos y ledger A–J completos en ZIP de conversación SHA256 `6851bc134613283d107de03e078bdeb81961d940fe25d0ae5f8aa8f8d5f49871`; backfill GitHub pendiente; clean clone separado NO comprobado.

**Veredicto: 1/3 operacional (uno), NO 2/3, NO 3/3.** No se requiere seguir cambiando el parámetro espectral con el mismo simulador. Buscar una reivindicación realmente distinta antes de nueva cuota.
Fuentes: https://www.liyiwei.org/papers/noise-sig10/ ; https://doi.org/10.1145/2487228.2487233 ; https://doi.org/10.1103/PhysRevE.89.022721 .
