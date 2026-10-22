# Ledger AB 3.2.1 — 6 ciclos focalizados LARP, 22-10-2026

**Evidencia exploratoria:** todas las comparaciones neuronales son pruebas sobre un dataset real de 1797 imágenes, pero las cuatro geometrías son réplicas de construcción, no cuatro datasets. Los controles C06 adicionales son REPAIR dentro de C06, no C07. Cada próximo paso se seleccionó después de inspeccionar el anterior; los scripts para ciclos posteriores fueron escritos progresivamente.

### C01 — ¿Existe un comparador Wei original ejecutable aquí?
**Observación:** El repositorio público original 1iyiwei/noise/RainbowNoise contiene fuentes y CMake, README indica VS .NET 2003; el acceso disponible permite inspeccionar código pero no ha proporcionado un ejecutable validado para Linux/3D/5 tipos/N comparable.

**Rival/falsador:** Implementación propia o CVT podrían hacerse pasar por Wei.

**Decisión AB:** BARRERA_DE_EJECUCIÓN_WEI / PIVOT. **Siguiente pregunta:** Probar transferencia a datos reales, manteniendo Wei como comparador pendiente.

**Límites:** Auditoría fuente: https://github.com/1iyiwei/noise/tree/master/RainbowNoise/src ; no afirmar que Wei sea imposible en general; únicamente no ejecutado ni validado en esta sesión.

### C02 — ¿Podemos generar realizaciones independientes sin reutilizar las cuatro antiguas?
**Observación:** Cuatro semillas nuevas 8101–8104, N128, 600 iteraciones auténticas por LOCAL/MHU, init/labels pareadas y verificadas con modo 0 iteraciones. Bajo proyectar a plano, la cobertura de cinco tipos k=8 varía y CVT/Sobol a menudo mejoran MHU. Auditoría Fourier de 40 modos 3D sí comprueba supresión en MHU.

**Rival/falsador:** El hallazgo Fourier procede solo del objetivo; proyectar 3D a 2D puede destruirlo.

**Decisión AB:** CONTINUE_CON_LIMITACION. **Siguiente pregunta:** Fijar benchmark no Fourier sobre estas geometrías independientes.

**Límites:** N reducido frente a N4096 histórico; optimizador v2 original archivado, validate=False, espectro exacto añadido ex post; CVT construido y declarado no equivale a Wei.

### C03 — ¿Produce la distribución MHU un muestreo espacial útil sobre imágenes reales?
**Observación:** UCI Digits 1797 imágenes 8×8; 5 roles intensidad/blur/dx/dy/Laplaciano suavizado, lectura en coordenadas geométricas y RBF a grid 4×4. Reconstrucción de gris N128 sin ganador sistemático MHU.

**Rival/falsador:** Quizá la red aprende diferencia que MSE de reconstrucción no capta.

**Decisión AB:** CONTINUE. **Siguiente pregunta:** Entrenar MLP equiparados con píxeles y validar convergencia.

**Límites:** No se entrenó geometría usando etiquetas ni imágenes; imputación por RBF e interpolación son decisiones comunes, pero no CVT/Wei igualados en coste.

### C04 — ¿Supera LARP a redes convencionales en clasificación real con parámetros semejantes?
**Observación:** 20 MLP sobre geometrías y cuatro MLP pixel baseline. Mejora MHU no demostrada: MHU 94.94% vs LOCAL 95.06%, Sobol 96.11%, píxeles 96.78%.

**Rival/falsador:** Diferencias de operator de los roles, no solo geometría.

**Decisión AB:** PIVOT_TO_ROLE_ABLATION. **Siguiente pregunta:** Mantener mismas nubes y sustituir roles diferentes por intensidad común.

**Límites:** ~5834 parámetros geométricos vs ~5860 píxel (0.45% diferencia); 240 pasos máximos y early stopping val; algunas carreras seleccionan último paso, por lo que no afirmar convergencia completa; solo 4 geometrías.

### C05 — ¿Aporta ventaja la especialización funcional de tipos frente a roles redundantes?
**Observación:** Cada muestra preserva las mismas posiciones, etiquetas, canales y parámetros; reemplazar funciones diferentes por intensidad en los cinco tipos mejora MHU en 1.56 puntos de media y LOCAL en 1.11; para Sobol diferencias pequeñas.

**Rival/falsador:** El conjunto de transformaciones no necesariamente aporta información discriminante independiente.

**Decisión AB:** PIVOT_TO_ROBUSTNESS. **Siguiente pregunta:** Probar intensidad común y comparadores de preprocesado bajo corrupción nueva.

**Límites:** Ablación altera simultáneamente la información disponible y la semántica de roles; no prueba que la especialización sea inútil para otras tareas.

### C06 — ¿Sobreviven diferencias de aprendizaje a desplazamientos de distribución y baselines de preprocesado?
**Observación:** Con intensidad y modelos congelados, LOCAL 73.17% vs MHU 71.39% en rotación ±12°, LOCAL 91.00% vs MHU 90.39% con ruido. Pixel MLP raw 33.33% rotación, pero blur64 controla parte de diferencia (48.72%); rol de representación vs geometría no identificado completamente.

**Rival/falsador:** Los filtros y el pooling, no la hiperuniformidad, podrían explicar toda la robustez.

**Decisión AB:** CLOSE_NO_NOVELTY_REQUEST_CONDITIONAL. **Siguiente pregunta:** Exigir 2D nativo, Wei ejecutable y un problema con múltiples canales realmente informativos antes de ampliar.

**Límites:** Dataset test original y perturbaciones no son datasets independientes; tamaño e inductive bias no totalmente pareados; comparador blur usa todos los píxeles, no igual presupuesto sensores. No prueba 2/3 ni 3/3.

