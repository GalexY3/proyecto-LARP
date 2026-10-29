# LARP / AB3.2.1 O1–O7 — Prerregistro prospectivo VISION C01
Fecha: 2026-10-29. Estado al crear: DESIGNED, NO RESULTS EXPOSED. Un ciclo experimental A–J, presupuesto 1. Rama propia, sin merge a main ni CI.
Código fuente local congelado antes de resultados: SHA256 `5e47f6e63e98dd14655f8eeec0e8d826d97eb750fd24c099ea4b6aa3e50ea993` del fichero `vision_ab_c01.py`. Este prerregistro debe verificarse en GitHub antes de iniciar ejecución. El código se incorporará después con el mismo hash y constará esa cronología.
## A. Contrato de verdad
Fenómeno: selección espacial de 160 muestras de imágenes con cinco etiquetas geométricas iguales. Unidad inferencial: imagen de origen; seeds geométricas son submuestras dependientes. Población de conveniencia: 13 imágenes públicas empaquetadas en skimage.data, sin asegurar independencia histórica de campañas LARP; no extrapolar a visión artificial, fotorreceptores reales, reconocimiento visual ni MHU asintótica. Outcomes primarios: MSE de reconstrucción con interpolación lineal triangular + nearest fuera de convex hull, usando 160 lecturas por imagen, en condición clean y 30% pérdidas aleatorias. Secundario: ruido gaussiano sigma 0.08, energía estructural baja k.
## B. Rivales
H1: optimización espectral conjunta de los 5 tipos (MHU_PROXY_FINITE) mejora MSE bajo pérdidas frente a optimización de espectros de subtipo (SUB_ONLY). Nula: ninguna mejora. Rivales fuertes: retícula 16x10, Sobol scrambled, scipy PoissonDisk y CVT optimizada por subtipo. Multi-class blue noise auténtico Wei 2010 y un modelo visual entrenado NO se ejecutan, y no pueden ser reemplazados nominativamente por esos baselines.
## C. Diseño discriminante
- Geometrías N=160, 5 tipos=32, seeds fijadas [1103,1109,1117,1123,1129,1151].
- Imágenes: DEV astronaut/coffee/chelsea/rocket, TEST camera/coins/page/hubble_deep_field/immunohistochemistry/cell/brick/gravel/grass. Se usarán todos los nombres, sin seleccionar posteriormente. Redimensionar crop central a 128x128 grayscale anti-aliasing sin entrenamiento. Estos TEST no están garantizados vírgenes en el historial LARP; se declaran new-to-this-code only.
- Condiciones: clean, dropout 30% de lecturas, ruido gaussiano sigma 0.08; mismo número de lecturas y misma interpolación en todos los brazos. Los sensores miden la misma modalidad: los cinco tipos son etiquetas de construcción geométrica, no cinco funciones ópticas.
- Comparaciones específicas: (i) mhu_joint - mhu_subtypes, (ii) mhu_joint - grid, (iii) mhu_joint - poisson_disk, (iv) mhu_joint - cvt_subtypes. Fijar signo negativo de delta MSE favorable a joint. No usar tests para seleccionar baselines o tuning.
- Inseguridad inferencial: 9 imágenes test no representan población amplia. Reportar diferencia media por imagen (promediando seeds), signos y dispersión, sin p-valores confirmatorios si hay reuse histórico.
## D. Instrumentación
SHA del código 5e47f6e63e98dd14655f8eeec0e8d826d97eb750fd24c099ea4b6aa3e50ea993. Optimizador Torch 95 pasos Adam LR .014 y regularizador local fijo para both joint/sub; mismas condiciones salvo término unión en objetivo. Loss FINITE k=(i,j), 0< i²+j²<=10, una mitad del espectro. Imágenes SHA en JSON resultados, números CPU. Pruebas: 160 puntos, 5 cuotas exactas, ausencia NaN; Fase de reparación si se detectan bugs antes de outcomes: registrar errata y nuevo SHA antes de resultado, no sobrescribir.
## E. Exploración
Ejecutar un único código congelado; conservar resultados por imagen/semilla/perturbación, sin excluir negativas.
## F. Auditoría
Auditar optimización directa del proxy, sesgo a banda Fourier, periodicidad frente a imágenes con bordes, mismatch RGB/grayscale, interpolación, cobertura exterior, dificultad de igualar coste de generación y la falta de Wei auténtico; el método puede favorecer retícula o CVT.
## G. Confirmación
TEST independiente del diseño de este script pero no necesariamente de campañas anteriores. Sin confirmación externa. No elevar a 2/3.
## H. Priors
Prior 1: mejora de joint sobre subtype poco probable en imágenes naturales sin modalidades diferenciadas; evidencia heredada AB30N y AB08. Prior 2: grid/CVT/PoissonDisk rivales fuertes. Registrar actualización cualitativa según signo y tamaño de efectos y límites.
## I. Dictamen
Validez interna, validez externa, identificación del mecanismo MHU, originalidad, paridad informativa/cómputo y rendimiento en imágenes: independientes.
## J. Decisión
STOP o PIVOT si el resultado solo repite que uniformidad geométrica ayuda o falla contra rivales competentes. No ampliar ciclos sin fuente nueva, benchmark de visión real y ejecución Wei/ViT. Sin afirmación de 2/3.
## Gobernanza
CT2 inicial SOLO nueva rama VISION_C01=22/100, juicio ordinal provisional (NO probabilidad); no heredar CT2 de otras líneas. Riesgo de imágenes ya conocidas en LARP: alto/no auditado. Grado nuevo 0/3 hasta auditoría. R5: esta prueba no basta como novedad; está motivada por la pregunta específica del usuario, como ensayo controlado preliminar. CLEAN_CLONE_NOT_VERIFIED.
