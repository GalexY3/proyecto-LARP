# Dictamen LARP — 30 ciclos AB completos sobre auditoría del riesgo (23-10-2026)

**Estado:** 30 ciclos contables, dos INVALID (C03,C20) sustituidos prospectivamente por C03R/C20R. Se han documentado fases A–J y seis decisiones adaptativas. **No hay descubrimiento 2/3, prueba causal de despliegue ni replicación externa independiente.** El ledger A–J y 32 JSON brutos por adquisición están en el ZIP archivado en la conversación; GitHub conserva la fuente, contratos, errores, lecturas por bloque y tabla de 30 estimaciones (redondeadas).

## Estimando y diseño
Población finita = filas de evaluación de cada partición de Digits, Wine, Breast Cancer e Iris (datasets reales, previamente utilizados en LARP). Objetivo = MSE al estimar la tasa de error 0–1 de un clasificador logístico fijo entrenado solo en train, con proxy de incertidumbre calibrado solo en validation. Los métodos acceden a idénticas predicciones sin etiqueta, y reciben exactamente el mismo presupuesto de etiquetas únicas, salvo los controles explícitos que emplean cero etiquetas. Cuatro particiones de modelo por ciclo y 96 consultas aleatorias anidadas en C01–C25; doce particiones nuevas y 120 consultas anidadas para C26–C30. **Las particiones de un mismo dataset comparten observaciones, no son poblaciones externas independientes.**

Estadístico: Δ=MSE(A)−MSE(B), menor es mejor. Intervenciones `flip_all`, `flip_confident`, `flip_uncertain` y `rare_error` modifican etiquetas de evaluación artificialmente: no equivalen a drift observado de campo. IC95 t descriptivos por seed de partición, no confirmación múltiple independiente.

## Árbol de investigación
1. **B01 (C01–C05; reemplazo C03R):** separar adquirir ejemplos inciertos para aprendizaje de estimar error global; SRS mejora frente a media ingenua top-uncertainty C01 (Δ=-0.07226), estratificación mejora inicialmente C02 (-0.000134) pero no claramente en C26. C03 igual/proporcional tenía exactamente la misma asignación y se invalidó antes de C03R. AIPW vs HT C04 inconcluso; Hájek empeora HT C05.
2. **B02 (C06–C10):** calibración y focalización. C06/C07 calibración sin diferencia clara, control deliberado C08 proxy invertido perjudica AIPW (Δ=-0.010055 a favor constante), C09 PPS intensa mejora AIPW en Wine (-0.000470), HT C10 inconcluso.
3. **B03 (C11–C15):** drift construido de etiquetas. C11 encuesta aleatoria vence proxy sin etiquetas en flip total (límite conocido); C12 AIPW peor que SRS bajo inversión de etiquetas de ejemplos confiados (Δ=+0.040353), C13 gana AIPW cuando error se localiza en inciertos, C14 estratificación ayuda bajo cambio en confiados, C15 empeora asignación Neyman.
4. **B04 (C16–C20, reemplazo C20R):** estimar riesgo de clase **predicha**, subgrupo conocido antes de etiquetar, sin alegar dimensiones demográficas. C16–C19 sin conclusiones claras; C20 pérdida identicamente 0 en ambos brazos, INVALID; C20R falla AIPW bajo flip confiado en Iris (Δ=+0.027978).
5. **B05 (C21–C25):** corrección muestral. C21 Horvitz–Thompson reduce el MSE frente a muestra intencional ingenua (-0.030121), C22 postestratificación mejora frente a media de asignación sesgada (-0.000274), C24 HT mejora Hájek bajo PPS alto (-0.000291); C23/C25 no concluyentes.
6. **B06 (C26–C30):** cinco recontrastes seleccionados y congelados en GitHub antes de correr, con semillas `107,109,113,127,131,137,139,149,151,157,163,167` y 120 adquisiciones/seed. C26 no reproduce la mejora de C02; C27 mejora PPS fuerte, C28 reproduce la derrota de AIPW bajo drift confiado, C29 HT vence media sesgada y C30 HT supera Hájek. Los cinco están reportados, con Holm solo ilustrativo; no validar hipótesis externamente por remuestrear datasets conocidos.

## Mecánica — no es un descubrimiento nuevo
R=Σℓ_i/N. Con probabilidad de inclusión conocida π_i>0, HT=(1/N)Σ_{i∈S}ℓ_i/π_i. Estimador aumentado = media(q_i)+(1/N)Σ_{i∈S}(ℓ_i−q_i)/π_i. Ambos son **insesgados bajo el diseño** con q fijo y π correcta; cuando el proxy queda desactualizado puede crecer drásticamente la **varianza/MSE**, no necesariamente el sesgo de diseño. Muestreo determinista top-k deja π=0 fuera del subconjunto y no identifica el riesgo global sin otros supuestos. Reproducción de teoría estadística clásica.

## Reparaciones y controles
- C03 diseño alias INVALID y C20 outcome sin variación INVALID, ambos archivados, reemplazos precommitted; **no cuentan**.
- B04 anomalía: TSV local inicialmente omitió `group=true`, aunque Github prereg original lo tenía. Al reparar metadata y reejecutar C16–C20, **los cinco JSON conservaron SHA256 exactamente idénticos**. La historia y hashes previos están en `errors/`.
- Se verificó montecarlo de inclusión sistemática PPS con 6000 extracciones N30 B8: riesgo 0.33333, media HT 0.33308, media AIPW 0.33343; propensiones positivas y exactamente B etiquetas por extracción.
- Fuente v1 SHA256 `41a7ffe9b64a6eb4694969f6bd08bc5fcd401f3d79372990c67725cb0e310ee7` publicada en tres fragmentos `source/engine.py.gz.b64.part1..3` ANTES de ejecutar. Patch B02 archivado `source/PATCH_B02.diff` ANTES de ejecutarlo, SHA v2 `20e0c44f5bf813be9e6516fd2b3de00501c6034e028f7b8bfbc126eb912516fc`; restaurador con hashes `source/reconstruct_engine.py`. Los TSV por bloque salvo B06 estuvieron en GitHub antes de cada ejecución. B06 `prereg/B06_FROZEN.md` fijó métodos, seeds y signos antes de las pruebas; cualquier TSV de B06 incorporado luego es **archival**, no un segundo preregistro.
- **Deuda:** raw de 32 pruebas y ledger completo A–J se distribuyen en el ZIP de conversación, no dentro de GitHub. `CLEAN_CLONE_NOT_VERIFIED`. No declarar conformidad total del requisito O3 de publicación remota de resultados brutos mientras no se suban.

## Priors y próxima puerta R5
Los ocho priors nuevos se conservan en `reports/PRIORS_DELTA.md`, sin borrar registros previos. El programa no demostró superioridad de MHU, de AB o de un detector de drift. La próxima fuente de evidencia debe ser **un flujo temporal externo** con etiquetas realmente demoradas y costes observados; evaluar frente a PPRM y esquemas de muestreo activo insesgado con mismo presupuesto, con protocolo preregistrado y holdout no consumido. No se justifica repetir 30 seeds del mismo dataset.

**AB-DECIDE:** CLOSE_QUOTA_30, no 2/3 ni confirmación externa.

Literatura: Imberg et al. (2020) https://proceedings.mlr.press/v108/imberg20a.html ; Zhang et al. (2026) https://proceedings.mlr.press/v306/zhang26g.html ; survey 2026 https://doi.org/10.1016/j.dsp.2026.106325 .
