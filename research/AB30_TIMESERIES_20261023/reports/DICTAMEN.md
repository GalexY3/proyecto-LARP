# Dictamen de LARP AB30-TS — 23 de octubre de 2026

## Pregunta y resultado

**¿Hasta qué punto las formas de otorgar mayor valor a observaciones recientes generalizan entre procesos temporales reales?** Se ejecutaron **30 ciclos A–J (5 problemas de forecasting × 6 fuentes históricas reales)**. Los ciclos constituyen preguntas/contrastes individuales, con protocolo y validación registrados antes de test; no equivalen a 30 estudios empíricos independientes. Los modelos de pronóstico son convencionales y **no hay descubrimiento original 2/3 ni efecto causal identificado**.

Datos reales de `statsmodels.datasets`: caudal del Nilo (100 años), manchas solares (309 años), CO₂ atmosférico Mauna Loa (2284 semanas), PIB real estadounidense (203 trimestres, modelado en log), series mensuales del conjunto El Niño (732 meses) y tipo de interés (107 trimestres). Los procesos difieren en periodicidad, ruido y tendencias. El tramo de desarrollo [35%,50%] se utilizó exclusivamente para elegir al experto fijo del bloque B05; validación [50%,75%] para las decisiones AB; el **test [75%,100%] permaneció físicamente truncado** durante la exploración y se abrió una vez tras congelar los 30 diseños.

## Matriz de contrastes

| Bloque y ciclos | A | B | Fuentes donde A reduce MAE en test | Interpretación |
|---|---|---|---|---|
| B01 C01–C06 | Persistencia | Media 16 | 5/6 | La media larga suele estar desfasada en series dinámicas o crecientes; Nilo no concluyente |
| B02 C07–C12 | Media 4 | Media 16 | 3/6 | Ganancias heterogéneas; CO₂, PIB e intereses, no Nilo/Sunspots/El Niño |
| B03 C13–C18 | EMA α=.3 | Media 4 | 3/6 | La memoria exponencial ayuda en manchas solares/El Niño y perjudica PIB/CO₂ |
| B04 C19–C24 | Trend lineal lag8 | Persistencia | 2/6 | Extrapolación perjudica claramente ciclos; la ventaja en Nile/PIB es incierta |
| B05 C25–C30 | Ensamble adaptativo (t-12) | Mejor experto fijo elegido en desarrollo | 0/6 | Adaptarse puede diluir un buen pronosticador fijo; efecto condicionado a pesos y pool |

La dirección del efecto validación→test coincide **29 de 30 veces**. Única inversión: C19, tendencia del Nilo, con incertidumbre grande en ambos segmentos. **13 de 30** efectos en test tienen signo favorable a A. Los resultados, tamaños, denominadores, IC bootstrap, errores HAC y p Holm descriptivos están en `SUMMARY_30.csv`, `AUDIT_SUMMARY.json` y el ledger individual. **20/30** contrastes tienen p descriptiva Holm inferior a 0,05 bajo aproximación HAC; esto **NO** equivale a 20 hallazgos independientes por dependencia compartida, autocorrelación, cambios históricos y controles incompletos.

## Auditoría F: anticipación, dependencia y baselines fuertes

1. La fuente Python y el código de validación quedaron congelados en GitHub antes de ejecutar. Un cambio **anterior a B01** eliminó cualquier cálculo del futuro durante la fase de validación, conservando la historia del commit y su SHA. Validación reconstruida a partir de datos truncados coincide exactamente con predicciones calculadas sobre series completas, y una corrupción adversarial de las observaciones posteriores a la fecha predicha no altera ningún pronóstico previo. Se verificó en seis fuentes y todos los algoritmos.
2. Se aplicó bootstrap circular por bloques (1499 remuestreos, longitud aprox n^(1/3)) y una prueba adicional HAC con lags de 52 semanas CO₂, 12 meses El Niño, 11 observaciones Sunspots, 5 Nilo, 4 PIB e interés. **Los intervalos y p-values son aproximaciones dependientes de modelar bien la estructura temporal**; Holm corrige por 30 hipótesis solo condicionalmente a p-valores válidos.
3. Una **auditoría de baselines fuertes posterior a abrir el test** incluyó AR(1) causal ajustado en ventana reciente de 32 pares y naive estacional lag52 para CO₂/lag12 para El Niño, con selección del mejor predictor únicamente sobre desarrollo. Ganó frente al antiguo experto fijo para Nilo (MAE 94,58 vs 95,97) y PIB log (0,00498 vs 0,00779), quedó igual para Sunspots, CO₂ y El Niño, y perdió ligeramente para intereses (0,00372 vs 0,00363). El ensemble adaptativo volvió a quedar por debajo de ambos en todos los dominios. Esta auditoría no es una confirmación independiente porque **el test ya estaba expuesto** cuando se planteó; sus resultados son controles exploratorios.
4. Los algoritmos fuertes de series temporales (ARIMA/ETS ajustados por estacionalidad, ensembles online bien calibrados y cambios de régimen) **no se han ejecutado exhaustivamente**. No se puede reivindicar universalidad ni superioridad sobre el estado del arte.
5. El auditor posterior al test tuvo un fallo de indexación en su propio resumen por bloque (duplicación del ciclo frontera). Falló una aserción y se corrigió la agrupación, sin modificar comparaciones ni resultados originales. Se conserva el diagnóstico `checks/AUDIT_SCRIPT_REPAIR.md`.

## G — Qué se ha confirmado realmente

Las observaciones del cuarto final cronológico de cada serie no se utilizaron para generar las comparaciones y se emplearon simultáneamente una sola vez para comprobar **todas** las 30 hipótesis congeladas. Esto es un **holdout cronológico interno de seis fuentes históricas**, no una observación posterior al 23/10/2026, replicación externa por laboratorio ajeno, evidencia de cambios reales recientes ni prueba de AB contra un método de investigación convencional. Las series están en el entorno de desarrollo de `statsmodels` y sus dependencias históricas no fueron objeto de recolección nueva.

## H–J: actualizaciones y decisión

Priors incrementales en `PRIORS_DELTA.md`. Los resultados sugieren que la estructura física y temporal del proceso, los ciclos y la calidad del pronosticador fijo determinan cuándo conviene actualizar rápidamente. Estas explicaciones son **abducciones**: no se han aislado experimentalmente mecanismos físicos. Nuevos estudios deberían incorporar tareas temporales externas no consultadas, baselines estadísticos profesionales, protocolo precommit íntegro y una sola evaluación futura.

**AB-DECIDE: CLOSE_30 / STOP_LOCAL** esta matriz. **PIVOT potencial**, no realizado aquí, hacia test prospectivo con datos posteriores y detección explícita de cambio de régimen; priorizar valor informativo sobre llenar nuevos cupos. **Originalidad 2/3 = NO_VALIDADA.**

## Procedencia y límites de GitHub

Rama `research/ab30-timeseries-20261023`, `prereg/B01.md` y su `B01_AMENDMENT.md`; `prereg/B02.md`…`B05.md`; `prereg/G_HOLDOUT_UNSEAL.md`. Código exacto y hashes versionados antes de ejecución. Salidas exactas val/test, pérdidas por observación, ledger, pruebas de auditoría y figura en ZIP descargable. **Los cinco paquetes comprimidos de resultados por fecha y los cinco documentos de ledger A–J están también depositados retrospectivamente en la rama de GitHub**, cada bloque contiene seis ciclos y material de test, validación, metadatos y pérdidas por fecha. Se mantiene el archivo ZIP íntegro, y las incorporaciones posteriores NO alteran la anterioridad de los prerregistros. **REPRODUCED_COMPUTATIONALLY_IN_ISOLATED_DIRECTORY:** 60 de 60 archivos de validación/test reejecutados bit-a-bit (SHA256), con la misma instalación de paquetes; NO se verificó instalación desde un clon Git limpio ni máquina externa. La primera ejecución aislada falló por una carpeta no creada en el script posterior de staging; reparación documentada y código científico original intacto.

**Antecedentes importantes:** literatura de forecasting/ETS/ARIMA, comparación de evaluación fuera de muestra, combinación de expertos y estudios de aprendizaje activo; no se presenta un método nuevo.