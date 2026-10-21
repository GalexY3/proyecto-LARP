# Dictamen científico del branching 30 — LARP / AB 3.2.1

**Fecha:** 21-10-2026. **Autorización:** 30 ciclos con branching; ejecutados 30 contrastes condición-específicos bajo seis ramas, con registro A–J (no 30 estudios independientes). **Conclusión:** evidencia *intra-modelo* de una ventaja para cobertura funcional de campos suaves, no descubrimiento 2/3.

## Hallazgo confirmado de forma limitada
Una única afirmación elegida tras piloto y preregistrada *antes* de los nuevos mundos sintéticos: MSE de interpolación multicanal en f=1, LOCAL frente STRATIFIED, mismos 24 vecinos, mismo kernel y mismas consultas y coeficientes por mundo, 20 mundos × 512 queries. Resultados: {'local': 0.12581194998789172, 'stratified': 0.2008379313017517, 'random': 0.319896997920874, 'mhu': 0.13230639770242908}; diferencia (LOCAL−STRATIFIED) **-0.075026**; IC95 pareado por mundo **[-0.091196, -0.058856]**, t19=-9.711, p bilateral=8.42e-09. 20 mundos independientes de señales **sobre las mismas geometrías fijas**, no 20 replicaciones de un generador espacial.

## Qué sí explica la ventaja
LOCAL y MHU, optimizados para separación dentro de cada uno de los cinco grupos, elevan disponibilidad cercana de canales complementarios. En nuestro control de 8.192 consultas uniformes sobre los originales, k=16: LOCAL 96.20%, MHU 94.91%, STRATIFIED 80.88%, RANDOM 62.32%. Esto es un beneficio de **muestreo funcional/espacial** bajo cargas conocidas, no una propiedad neuronal universal.

## Qué la limita
* C11 f1: LOCAL MSE≈0.134 vs STRATIFIED≈0.208; C15 f6: LOCAL≈2.106 vs STRATIFIED≈2.149. La ventaja pierde relevancia al subir la frecuencia (todos empeoran).
* Permutar etiquetas degrada; eliminar cuatro tipos hace la tarea irresoluble por el interpolador: resultado parcialmente impuesto por mecanismo del simulador.
* MHU y LOCAL empatan aproximadamente en esta tarea. Penalización espectral no aporta una mejora inequívoca.
* Bandwidth 0.3×distancia k24 da mucho menos error que el bandwidth base (pilot LOCAL f2 MSE .608 vs .813), lo que indica sensibilidad al estimador; optimización de bandwidth sólo exploratoria (no retune del confirmatorio).
* El algoritmo predictor es **un interpolador gaussiano clásico por tipo**, NO un nuevo entrenamiento de LARP neuronal. No resolver código/matemáticas/lenguaje.
* F27/F30 son invariantes algebraicas de renombrado/reordenación y no intervenciones geométricas; confundirlas con ablación invalida argumento.
* Comparator STRATIFIED está basado en una rejilla perturbada por tipo, **no** es el mejor algoritmo de multi-class blue noise; no es correcto afirmar SOTA.

## Auditoría de originalidad
Antecedentes verificables: Wei (2010), *Multi-Class Blue Noise Sampling*, https://www.liyiwei.org/papers/noise-sig10/; Jiao et al. (2014), https://doi.org/10.1103/PhysRevE.89.022721; Lomba et al. (2020), https://doi.org/10.1103/PhysRevE.102.012134. Tienen mecanismos de muestreo espacial multiclase, heterocoordinación y supresión de fluctuaciones. LOCAL no constituye por sí sola una clase matemática novedosa. Una extensión a equipos de expertos semánticos sigue sin probar.

## Procedencia y auditabilidad
Prerregistro github: c6a6e3fcedb717e3e2faee5f8f5fd38d7be463f4. Bloqueo SHA del script antes de ejecutar: eea8e364efe6d8c9b5d49d2d83493d3c2292d01e. Selección confirmatoria: 76b332002d0a6c047976359ccf124b7dd3eafeac. Fuente local congelada SHA256 6ba3d7347c087bdf71c7de800312866c4f10dbf0f9da5ba26b499a33957284c5. El intento inicial de ejecutar `--phase confirm` con 30 condiciones agotó el tiempo y no generó CSV completo; se ejecutó **exclusivamente** la afirmación congelada con `src/confirm_focus.py`. No presentar experimentos no ejecutados como ejecutados.

## AB-DECIDE
**PIVOT condicional hacia muestreo de sensores multiclase y especialización funcional**, sólo si se accede a nuevos generadores de geometrías, simulaciones físicas o expertos ML con comparadores competentes Multi-Class Blue Noise / PointNet++ / Set Transformer. **STOP** en repetir el mismo Fourier sintético: no aumenta evidencia de novedad. **Ninguna contribución de nivel 2/3 ni 3/3 acreditada.**
