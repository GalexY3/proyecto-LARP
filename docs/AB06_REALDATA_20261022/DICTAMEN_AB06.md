# LARP/MHU — seis ciclos con datos reales y falsación de ventaja neuronal

**Fecha:** 22-10-2026. **Estado:** C01-C06 cerrados, exploratorios. **2/3:** no acreditado. **3/3:** no acreditado. **Evaluación nativa de Li-Yi Wei:** no realizada (BARRERA_DE_EJECUCIÓN).

## 1. Qué cambió

Se abandonaron los campos Fourier sintéticos: UCI Optical Recognition of Handwritten Digits (copia sklearn; 1797 imágenes de 8×8, 10 dígitos). Se generaron cuatro semillas **nuevas** de n=128, con funciones originales Scale3D LOCAL y MHU v2 durante 600 iteraciones; también CVT por tipo, Sobol por tipo y azar. Las geometrías 3D se proyectaron al espacio 2D de imagen. Ésta es deliberadamente una prueba de transferencia fuera del dominio geométrico de construcción, no un benchmark de point clouds 3D.

Una clase sensorial mide intensidad, otra suavizado, otra gradiente horizontal, otra gradiente vertical y otra Laplaciano suavizado. Se proyectan 128 lecturas por imagen en 80 características (5 tipos × 4×4 celdas por RBF). Un MLP con 5834 parámetros aprende la clase de dígito. Baseline: MLP directamente sobre 64 píxeles, 5860 parámetros. Mismos índices train/val/test estratificados, hasta 240 actualizaciones AdamW de lote completo; checkpoint escogido por val loss y test solamente evaluado después. Sin GPU y sin datos de entrenamiento derivados de Fourier.

## 2. Resultados observados

### Filtro espectral sigue funcionando sin predecir rendimiento neuronal

- MHU: potencia normalizada Fourier 3D media 4.61631e-06; cobertura proyectada de cinco tipos entre 8 vecinos 31.1%.
- LOCAL: potencia normalizada Fourier 3D media 7.23903e-05; cobertura proyectada de cinco tipos entre 8 vecinos 31.0%.
- Sobol: potencia normalizada Fourier 3D media 0.00518924; cobertura proyectada de cinco tipos entre 8 vecinos 38.1%.
- CVT: potencia normalizada Fourier 3D media 0.00207817; cobertura proyectada de cinco tipos entre 8 vecinos 36.4%.
- Aleatoria: potencia normalizada Fourier 3D media 0.00709165; cobertura proyectada de cinco tipos entre 8 vecinos 19.2%.

### Clasificación clean (test; media de cuatro geometrías, para pixel cuatro inicializaciones)

| Método | Exactitud media | Desviación estándar entre geometrías / inicializaciones |
|---|---:|---:|
| LOCAL | 95.06% | 1.56 puntos |
| MHU | 94.94% | 1.27 puntos |
| CVT | 95.17% | 0.64 puntos |
| Sobol | 96.11% | 0.29 puntos |
| Aleatoria | 95.17% | 0.90 puntos |
| MLP píxeles | 96.78% | 0.29 puntos |

**MHU frente a LOCAL:** diferencias pareadas por geometría +0.89 pp, -2.00 pp, -0.22 pp, +0.89 pp. n=4 pequeño; sin ventaja robusta ni equivalencia estadística acreditada. **Sobol** y los píxeles originales superan MHU en la media. Algunos modelos lograron mejor checkpoint en el paso 240: el presupuesto no garantiza convergencia final. No se igualaron el coste de generación ni los FLOPs de codificación sensorial.

### Ablación de roles: cinco operadores frente a cinco copias de intensidad

- MHU: especializados menos homogéneos = -1.56 puntos porcentuales.
- LOCAL: especializados menos homogéneos = -1.11 puntos porcentuales.
- CVT: especializados menos homogéneos = -1.44 puntos porcentuales.
- Sobol: especializados menos homogéneos = -0.11 puntos porcentuales.
- Aleatoria: especializados menos homogéneos = -1.22 puntos porcentuales.

La heterogeneidad funcional no genera una ventaja automática; el filtro puede eliminar señales discriminantes de la imagen.

### Robustez (solo intensidad, protocolo de entrenamiento cerrado)

| Método | Clean | Ruido gaussiano σ=0,17 | Oclusión 2×2 | Rotación ±12° |
|---|---:|---:|---:|---:|
| LOCAL | 96.17% | 91.00% | 81.50% | 73.17% |
| MHU | 96.50% | 90.39% | 81.22% | 71.39% |
| CVT | 96.61% | 89.28% | 79.61% | 72.06% |
| Sobol | 96.22% | 89.83% | 80.28% | 69.44% |
| Aleatoria | 96.39% | 88.50% | 80.33% | 68.61% |
| MLP píxeles | 96.78% | 38.50% | 87.11% | 33.33% |
| MLP píxeles suavizados | 96.89% | 74.89% | 84.56% | 48.72% |
| MLP promedio 4×4 | 94.50% | 75.72% | 77.72% | 40.50% |

**Interpretación:** algunos codificadores basados en sensores tienen más tolerancia a ruido y rotación que el MLP de píxeles directos. Pero LOCAL suele superar MHU en esos shifts, Sobol cambia su posición y un MLP con píxeles suavizados recupera parte de la resistencia. No atribuir estas diferencias a MHU, porque los codificadores espaciales incluyen filtrado/RBF y el comparador suavizado utiliza píxeles completos. Son pruebas de *pipeline* con representación distinta, no una igualdad exhaustiva de FLOPs, información y lecturas.

## 3. Comparador clásico Wei y límites

El código original de **Li-Yi Wei, Multi-Class Blue Noise Sampling (SIGGRAPH 2010)** está público en https://github.com/1iyiwei/noise/tree/master/RainbowNoise/src; su README indica compilación histórica con Visual Studio .NET 2003 y ejemplo de DartThrowing. Se auditaron sus fuentes, pero **NO se obtuvo ni ejecutó una implementación Wei validada en 3D N=128 ni se compararon runtimes**. CVT/Sobol son comparadores clásicos ejecutados, pero no sustitutos etiquetables como Wei. Se conserva BARRERA_DE_EJECUCIÓN_WEI en el registro metodológico.

El benchmark de dígitos procede de observaciones reales, pero sigue siendo un único dataset pequeño; la lectura geométrica proyectada 3D→2D es inadecuada para inferir utilidad en 3D, y las 4 geometrías no bastan para inferir generalidad. Baselines de CPU con parámetros cercanos ≠ presupuesto total computacional exactamente igual. Los intentos de buscar ventaja de novedad 2/3/3/3 **fallan**.

## 4. Decisión y solicitud

**AB-DECIDE: STOP a la hipótesis de superioridad directa de la disposición MHU original en aprendizaje de dígitos y a seguir reciclando pruebas Fourier.** Conservar la propiedad de coordinación espectral intertipo como característica geométrica útil y conocida; de este bloque rescatar la utilidad potencial del *pipeline sensorial robusto*, que aparece en distintas geometrías y por tanto NO identifica una contribución específica de MHU.

**SOLICITO PIVOT 4 CICLOS**, condicionados a disponer de: (a) datos espaciales 3D reales o un benchmark point-cloud estable que no sea proyección 8×8; (b) entrenamiento convergido de al menos una red sobre esos datos; (c) implementación real de Wei o baseline equivalente **claramente etiquetado** y (d) igualación de sensores, información y FLOPs, no solo parámetros. El primer ciclo tendría que resolver disponibilidad técnica; si no, registrar STOP y no fabricar evidencia ni gastar ciclos vacíos.

## Trazabilidad

- C01: auditoría de fuentes públicas Wei y ejecutabilidad.
- C02: `src/cycle2_geometry.py`, `data/geo_8101..8104.npz` y `data/C02.json`.
- C03: `src/cycle3_digits.py`, dataset `digits_split.npz`, `digits_features_*`, `data/C03.json`.
- C04: `src/cycle4_train.py`, `data/C04.json`, test accuracy y curvas val completas.
- C05: `src/cycle5_roles.py`, `data/C05.json`.
- C06: `src/cycle6_robust.py`, `src/cycle6_controls.py`, `data/C06.json`, `data/C06_controls.json`; la segunda ejecución fue un REPAIR de confusión por preprocesado, no un séptimo ciclo.

- Fuente sobre dataset: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html
- Prior art: https://www.liyiwei.org/papers/noise-sig10/ y https://github.com/1iyiwei/noise
