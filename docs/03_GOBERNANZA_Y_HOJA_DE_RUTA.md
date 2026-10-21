# AB 3.2.1 · BR30 — Síntesis estratégica, procedencia y próximo criterio de decisión
**Fecha:** 21-10-2026. **Repositorio privado:** GalexY3/proyecto-LARP.

## Registro verificable
- Prerregistro congelado **antes del primer experimento**: commit `c6a6e3fcedb717e3e2faee5f8f5fd38d7be463f4`.
- Bloqueo de huella del código previo al piloto: `eea8e364efe6d8c9b5d49d2d83493d3c2292d01e`, SHA-256 `6ba3d7347c087bdf71c7de800312866c4f10dbf0f9da5ba26b499a33957284c5`.
- Selección de una única afirmación antes de abrir seeds 901–920: `76b332002d0a6c047976359ccf124b7dd3eafeac`.
- Commit que incorpora 19 archivos verificables, incluidas tres geometrías NPZ, scripts íntegros, 30 decisiones, resultados y manifest SHA-256: `6f301ee911902cd751237c654e7066818c3e8c7f`.
- Google Drive (archivo documental): https://drive.google.com/drive/folders/1s6J-oFQbqN_xohn-cr5118II9l7PS4t2
- ZIP íntegro con reporte, figuras y código: https://drive.google.com/file/d/1Cg8NBgp4bDR2ntvOaggaJKg7w_XfrF0k/view?usp=drivesdk

## Qué se hizo realmente
Un bloque de **30 decisiones científicas condición-específicas** en seis ramas: cinco presupuestos k de vecinos; cinco cuantiles de radio; cinco frecuencias de señal; cinco tasas de dropout; cinco bandwidths del kernel; y cinco controles de intervención/identidad. 880 observaciones tabuladas del piloto comparten semillas y geometrías, NO son independientes; una sola afirmación (C11, f=1, LOCAL vs STRATIFIED, k=24, bandwidth=.11) se confirmó después de seleccionar con 20 mundos nuevos. **NO se hicieron 30 estudios independientes ni 30 experimentos con nuevas geometrías**.

## Resultado y mecanismo defendible
C11 confirmatorio: MSE LOCAL **0.125812**, MHU 0.132306, STRATIFIED 0.200838, RANDOM 0.319897, usando interpolación gaussiana por tipo y la misma función de composición. Diferencia LOCAL−STRATIFIED **−0.075026**; IC95 por mundo **[−0.091196,−0.058856]**, 20 mundos de Fourier con 512 consultas cada uno. Resulta una **reducción descriptiva del MSE de 37.4%** vs un estratificado geométrico simple.

Con k=16 y 8192 consultas uniformes sobre las mismas geometrías: LOCAL 96.20%, MHU 94.91%, STRATIFIED 80.88%, RANDOM 62.32% con los cinco tipos disponibles. La separación por tipo explica plausiblemente mejor **disponibilidad espacial de canales complementarios**.

La ventaja **no es universal**: al subir la frecuencia del campo de f=1 a f=6 el MSE absoluto sube y LOCAL apenas aventaja al estratificado. En dropout .60 las prestaciones caen. Permutar etiquetas o destruir la correspondencia espacial degrada. La penalización espectral de MHU **no** mostró incremento fiable frente a LOCAL. Con bandwidth más estrecho mejora el kernel (exploratorio), prueba de que aún hay competencia de estimadores clásicos.

## Qué no se hizo y qué NO puede inferirse
No se entrenó aquí ningún Transformer, LLM o MoE; los sensores son valores Fourier sintéticos observados por tipo. **Este experimento no demuestra que LARP sea mejor que GPT**. El interpolador por canal es un algoritmo RBF convencional que ya incorpora conocimiento del tipo y la suavidad. No hay replicación externa con retinas medidas ni geometrías independientes generadas por el optimizador original. No se ha comparado con **Multi-Class Blue Noise** de Li-Yi Wei (SIGGRAPH 2010), una alternativa especializada fuerte. Una muestra finita de puntos con espectro reducido tampoco certifica multihiperuniformidad asintótica.

## Bibliografía que limita reivindicaciones
- Li-Yi Wei, *Multi-Class Blue Noise Sampling*, SIGGRAPH 2010: https://www.liyiwei.org/papers/noise-sig10/
- Jiao et al., *Avian photoreceptor patterns represent a disordered hyperuniform solution to a multiscale packing problem*, PRE 2014: https://doi.org/10.1103/PhysRevE.89.022721
- Lomba et al., *Minimal statistical-mechanical model for multihyperuniform patterns in avian retina*, PRE 2020: https://doi.org/10.1103/PhysRevE.102.012134
- Los controles futuros de aprendizaje deben incluir PointNet++, Set Transformer y estructuras MoE, con FLOPs iguales y acceso idéntico a entradas.

## Capitalización: próximo estudio causal prioritario
**Estimando**: interacción entre geometría (RANDOM, STRATIFIED, LOCAL, MHU y baseline Multi-Class Blue Noise genuino) y heterogeneidad funcional (tipos fijados, tipos aprendidos, sin tipos), sobre la diferencia de pérdida de evaluación FUERA DE DISTRIBUCIÓN con presupuesto igual de información, vecinos y FLOPs efectivos. Separar tareas multicanal **suaves** de tareas de alta frecuencia, puramente simbólicas y semánticas. El mecanismo hipotético es la *cobertura heterotípica con escasa comunicación*, no "MHU gana siempre". Evitar confundir el efecto de proporcionar a la arquitectura etiquetas correctas de tipo con un hallazgo emergente.

**Fase 1 (evidencia nueva):** regenerar al menos 10 geometrías independientes por método con cuotas pareadas y mismo coste de generación; introducir Multi-Class Blue Noise de 2010 o aproximación competente auditada. Confirmar/descartar la mejora por geometría **sobre varias geometrías**, no sólo nuevos mundos sobre las mismas posiciones.

**Fase 2 (factorial neuronal):** original Scale3D-LARP kNN con cinco tipos y ablación de tipos; GNN homogénea equivalente; Set Transformer y PointNet++ equiparados en cómputo y acceso a sensores; MoE con routing. Tareas de composición novedosa y perturbaciones; evaluar diferencias en parámetros, FLOPs de entrenamiento/inferencia, velocidad y calibración, junto con coste de generar geometría.

**Fase 3 (transferencia):** datasets no inventados para corroborar si geometría y especialización útiles en datos sensoriales irregulares, y sólo después código/lenguaje si hay mecanismos sólidos. Retener un test nuevo e independiente durante la selección.

**Fase 4 (originalidad):** demostrar efecto que no se reduzca a cobertura de muestras, kernels clásicos ni multi-class blue noise; confrontar teoría geométrica y complejidad. Sin eso, NO 2/3.

## Dictamen AB-DECIDE
**PIVOT condicional** a investigar **muestreo multiclase funcional** con evidencias diferentes; **STOP** a nuevas semillas de idéntico Fourier. No hay derecho automático a más ciclos: los 30 autorizados se han utilizado como decisiones en seis ramas. No se afirma descubrimiento 2/3 ni 3/3. El método AB es protocolo de auditoría, no superioridad end-to-end demostrada.

## Notas sobre trazabilidad
El trabajo de ejecución y el ledger principal están en los 19 archivos con SHA verificados. Este documento sirve como índice de GitHub→Drive, no sustituye el código y CSV. Los errores se reparan con commit de errata separado, no borrando el histórico.