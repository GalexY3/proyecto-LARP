# Suplemento oracle-band del ensayo de muestreo

Este suplemento **post hoc** califica la interpretación de `spatial_sampling_probe_v1`; no constituye una confirmación MHU. Pregunta si las diferencias entre geometrías persisten al usar un estimador lineal fuerte con conocimiento común de la banda generadora y del nivel de ruido. No representa información universal disponible en una retina o una red neuronal. No se entrena ningún modelo, no hay HPO y no se actualizan priors de arquitectura.

La configuración nueva `configs/sampling_oracle_v1.json` se congela con SHA-256 canónico `8f82daecac091c7f580cb5966680dcdbf9306ba43a6a40536d951f631ca1b038`; `src/larp/sampling_oracle.py` es independiente y no modifica v1. La preregistración del suplemento se escribe antes de calcular sus scores. Se reutilizan exactamente el banco Fourier, queries, nueve geometrías, marcas y ruido del v1, verificando sus hashes. La propuesta se formula después de observar los estimadores locales originales y debe describirse como tal.

Hay **72 celdas nuevas únicas**: tres familias × tres semillas × dos asignaciones de marcas × dos bandas × dos niveles de ruido × un estimador fijado para cada nivel. Se comparan con las **144 celdas originales** de vecino próximo y kernel gaussiano. Las 144 filas de cotejo comparten resultados oracle y no se presentan como réplicas independientes ni 144 nuevos experimentos.

## Estimador congelado

Para cada canal y población de sensores se construye `A=[cos(2π x·n/L),sin(2π x·n/L)]`, con los modos exactos del campo generador. El número de coeficientes es `D=2M`. Se predice en la misma matriz de queries Q.

Con σ=0 se usa pseudoinversa SVD de mínima norma, cutoff relativo `rcond=1e-10`, sin tuning. Si A tiene rango completo de columnas y los datos siguen exactamente la banda, los campos sin ruido son recuperables salvo error numérico. Si hay menos sensores que coeficientes, el informe registra nullity positiva y condicionamiento infinito del problema de columnas; no confunde el menor singular devuelto por SVD compacta con ausencia de direcciones nulas.

Con σ=0,1 se usa ridge `λ=Mσ²`. Los coeficientes del banco están normalizados sobre una esfera con norma cuadrada 2, por lo que su covarianza isotrópica es `I/M`. La regla es el estimador de menor error medio cuadrático **lineal** para esa covarianza y ruido independiente conocido; no es el posterior exacto de una prior gaussiana, ni el posterior no lineal exacto de la esfera. Los parámetros no se optimizan por geometría, semilla ni score. La banda y σ se conocen como información oracle del benchmark, igual para todas las familias.

En smooth, seis pares de modos dan doce coeficientes por canal, por debajo de los 34 sensores del tipo más raro. Esto permite comprobar si diferencias grandes de los interpoladores locales desaparecen con reconstrucción global. Fine contiene 28 pares de modos y 56 coeficientes; deja poblaciones D/E submuestreadas con 50/34 sensores y exige inspeccionar rangos, condicionamiento y errores por canal, sin inferir ventaja universal a partir de la media macro.

La métrica mantiene igual peso de los cinco canales y varianza analítica del campo uno. Se guardan rango, valores singulares, σmin, nullity, condición, λ, errores por canal/mundo, MSE macro y hashes de targets/marcas/ruido/predicción. Las diferencias entre geometrías siguen siendo descriptivas con tres realizaciones; los 128 mundos promedian dentro de cada geometría. Full/local continúan difiriendo en coordenadas y microestructura, por lo que no identifican una mediación de ondas largas.

## Ejecución y verificación

Presupuesto 30 s en proceso CPU separado con BLAS/OMP cuatro hilos; no se regeneran geometrías ni campos y no se amplían factores. Una omisión o entrada cambiada se declara, sin imputarla como fallo científico. No se sobrescribe una serie con distinta procedencia.

```powershell
.\.venv\Scripts\python.exe -m larp.sampling_oracle --dry-run
.\.venv\Scripts\python.exe -m larp.sampling_oracle
.\.venv\Scripts\python.exe -m pytest tests/test_sampling_oracle.py -q
```

Nueve pruebas pasan, registro `artifacts/sampling_oracle/v1/test_sampling_oracle.xml`: recuperación exacta sin ruido con rango completo, equivalencia algebraica ridge/covarianza, mínima norma subdeterminada, singularidades conservadas, periodicidad, denominadores no duplicados, escala de covarianza consistente con la normalización real de ambos bancos y exclusión de observaciones de otros canales. Las pruebas técnicas no son evidencia de ventaja MHU.

## Resultado

Se ejecutaron **72/72 celdas únicas**, con **144 cotejos** contra v1, en **0,644 s** de ejecución medida, RSS máximo muestreado **88.784.896 bytes**. Los tiempos incluyen verificación de inputs, evaluación, SVD y agregación, después de cargar dependencias. Las versiones, coeficientes, queries, ruido, targets, marcas y bytes de geometría coinciden con el v1. No se cambió ningún estimador, lambda, cutoff o campo después de observar resultados.

**El ranking depende del decoder.** Sin ruido y en smooth, todas las familias y asignaciones de marcas reconstruyen los campos hasta precisión numérica: MSE máximo entre las 18 celdas `5,79e-30`. Los 90 diseños únicos de esa banda tienen rango 12, condición máxima 4,329 y menor singular mínimo 1,398. La ventaja grande vista con interpoladores locales no representa una incapacidad de reconstrucción de los otros sustratos cuando se conoce la banda y se puede usar un decoder global.

Con ruido σ=0,1:

| Familia | Smooth native | Smooth shuffle | Fine native | Fine shuffle |
|---|---:|---:|---:|---:|
| MHU nominal | 0,002397 | 0,002685 | 0,131384 | 0,140018 |
| Aviar full_spectral | 0,001994 | 0,002643 | 0,137279 | 0,129860 |
| Aviar local_only | 0,001997 | 0,002437 | 0,136919 | 0,126345 |

Smooth conserva una mejora descriptiva de native aviar frente a shuffle y nominal, pero full y local difieren solo ≈`−3,09e-6` de MSE medio: no identifica un beneficio específico del control espectral. Fine invierte la jerarquía native de las familias: nominal presenta menor MSE que ambas aviarias. Además, **shuffle mejora ambas familias aviarias en las tres semillas**, con native−shuffle full `[+0,007122,+0,013382,+0,001755]` y local `[+0,012321,+0,010332,+0,009067]`. Son contraejemplos conservados, no excluidos por perjudicar la hipótesis.

Sin ruido, fine presenta medias native aproximadamente 0,0991/0,1005/0,0992 para nominal/full/local. Los diseños ABC tienen rango 56, D rango 50 y E rango 34; nullities 0/6/22. La condición máxima entre diseños de rango completo es 27,561. La pérdida de dimensiones en D/E limita la recuperación incluso con oracle, sin permitir atribuir toda diferencia restante a multihiperuniformidad.

El oracle reduce MSE respecto a ambos interpoladores locales en **144/144 cotejos**, bajo su información privilegiada común. Esto califica la afirmación anterior: las geometrías aviarias facilitan algunos decoders locales simples, pero no muestran superioridad universal de adquisición/reconstrucción ni un efecto neuronal. Las diferencias finas bajo ruido muestran por qué importan aliasing, condicionamiento y el modelo del campo, además de vacíos locales.

Los resultados completos se conservan en `artifacts/sampling_oracle/v1/results.json` y `summary.csv`; la tabla anterior es descriptiva, con tres geometrías, sin p-values ni posteriors de arquitectura. El siguiente ensayo debe preregistrar un decoder competente, restringir qué información global posee, cubrir espectros y ruido distintos y controlar microestructura. Añadir capacidad de reconstrucción a posteriori no convierte este suplemento en confirmación de MHU.
