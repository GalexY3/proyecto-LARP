# AB 3.2.1 C04 — PREREG ANTES DE OUTCOMES — 2026-10-29

## Estado y fuente congelada
Autorización vigente: bloque branching 20, C02 consumió 1; C03 planificación no consume; C04 candidato a segunda plaza. Fuente íntegra `vision_c04.py` con SHA256 de ejecución objetivo `d57d21ce76d4513419fbf38df9ec62b771872a4d50f1856a3a16133b268b31ae`; depositar y comprobar código completo en GitHub antes de obtener cualquier métrica. Estado al preregistrar: NO RESULTADOS. N1 y 2/3 no asumidos.

### A. Pregunta, estimando
En 200 imágenes reales distintas de 25×25 píxeles (100 rostros y 100 no rostros, `skimage.data.lfw_subset`), ¿qué rendimiento tiene un clasificador SVM-RBF entrenado usando solo 160 lecturas espaciales escalares, con patrón MHU espectral optimizado (no certificado), frente a distribuciones competentes? Unidad = imagen original, no muestra geométrica ni fold. Outcome primario: exactitud balanceada clean en CV; outcomes secundarios: exactitud con ruido gaussiano σ=.13 y oclusión negra 6×6, con entrenamiento SOLO limpio. Proxy de “inteligencia visual”: clasificabilidad rostro/fondo limitada; NO reconocer objetos generales ni vista humana.

### B. Hipótesis rivales
H1: optimización espectral conjunta ayuda a clasificar más que optimización por tipo sola (mismo modelo, mismo presupuesto). H2: regularidad geométrica ya explica efecto; grid / Poisson / Sobol no inferiores. H3: si el problema depende de información discriminante, selección supervisada de 160 píxeles por ANOVA, con SOLO TRAIN, podría ganar; baseline con 625 píxeles como referencia no estrictamente emparejada. H0: no mejora robusta de MHU sobre mejor control competente.

### C. Comparadores y diseño
Semillas geométricas predefinidas 4101,4109,4127; splits 5-fold estratificados repetidos con shuffle random states 13,29. Métodos `grid`, `sobol`, `poisson_disk` (SciPy PoissonDisk radius=.061, fill_space + farthest-point thinning a 160), `spectral_joint`, `spectral_sub`, `joint_phase_broken` (traslaciones independientes preservando espectros individuales), `random`, `supervised_kbest` (top-160 ANOVA pixel usando TRAIN solamente) y `full_pixels` (625; control ecológico, no paridad). Optimización geométrica sobre los mismos 5 tipos de 32 sensores, 70 iteraciones Adam, lr=.014, potencia k²<=10 y repulsión local .15. Lecturas son intensidad gris bilineal, etiquetas de cinco tipos solo geometría, NO cinco modalidades.

### D. Instrumentación
SVM-RBF `C=2, gamma=scale, class_weight=balanced`, fit solo training clean en cada fold; ruido y oclusión generados con semilla fija 240301 independientemente de y, evaluados OOD. ANOVA selecciona con cada train; prohibido selección mirando tests. Reconstrucción y preprocesado NO: clasificación directa de 160 lecturas, innovación funcional distinta a C01/C02. Invariantes N, coordenadas 0..1, labels 32 por tipo, 200 imágenes, hashes de entrada, exactitud por imagen (dos predicciones por repetición *3 semillas). Sensores aprendidos tienen acceso extra a etiquetas TRAIN; reportar por separado.

### E. Ejecución
Una sola ejecución del código fuente congelado; preservar bruto por imagen, fold, semilla, método, condición; no cambio de arquitectura/hyperparams a posteriori.

### F. Auditoría adversarial
LFW subset en skimage es dataset público preexistente, pero no se ha demostrado originalidad del material respecto historial LARP; 200 recortes del mismo origen, dependencia/duplicados posibles, no se evalúa fairness de demografía; sin pval confirmatorio, seeds/folds repetidos no aumentan n=200. Poisson debe comprobar cobertura. ANOVA supervisado usa datos adicionales, y full-pixel usa más lecturas. Comparación Wei original y vision transformers NO ejecutada.

### G. Confirmación
Ninguna réplica externa; dataset nuevo para esta línea respecto a Digits y reconstrucción de muestras pero procedencia LFW; una sola biblioteca no acredita transporte a ImageNet o cámaras. Intervalos descriptivos por imagen y no seed. MHU geométrica finita, nunca certificar hiperuniformidad asintótica.

### H. Priors
MHU no mejoró RGB reconstructivo C02; probabilidad cualitativa baja para beneficio visual general. Clasificación puede identificar excepción si espectro ayuda a preservar contornos. Priors negativos se conservan.

### I. Dictamen
Separar utilidad de 160 lecturas, ventaja del acoplamiento, robustez OOD, coste computacional, novedad 2/3. Un resultado positivo puede ser efecto del filtro bilineal.

### J. Decisión
Si no supera el mejor control competente bajo matching, STOP_LOCAL; si mejora, exigir nuevo benchmark independiente (modalidades reales, Wei auténtico, modelo neuronal) antes de 2/3. CT2 anterior línea 13/100 (ordinal); no modificar hasta auditoría. 1 ciclo experimental solo si ejecutado y auditado; si fallo invalidar y conservar logs. Ningún CI, ningún merge a main.

R5: nueva clase de evidencia relevante (clasificación visual con ground truth y control supervisado), por eso permitido frente a repetir MSE sintético. CLEAN_CLONE_NOT_VERIFIED hasta prueba.
