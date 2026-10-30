# W01 — Auditoría AB-R de fuente primaria del comparador Wei (congelada antes de los outcomes de auditoría)

Fecha: 2026-10-30. Concesión nueva: 10 ciclos AB-R (W01 es el primer candidato). Rama base e9c25783faf75aa4ecbad6ef11fd34d4fef9e883, sin cambios a main.
**Exposición preexistente**: README, CMakeLists raíz/src y las líneas 1–180 de DartThrowing.cpp del código Wei ya vistos antes del freeze; no es prueba ciega ni confirmación independiente. No hay wei-build.log de Windows en la sesión. Resultado de compilación sigue NO_EJECUTADO.
**Fuente externa fijada**: 1iyiwei/noise @ 0d1be2030518517199dff5c7e7514ee072037d59, archivos RainbowNoise/src/Main/CMakeLists.txt, RainbowNoise/src/Library/CMakeLists.txt, RainbowNoise/src/Main/DartThrowing.cpp, RainbowNoise/CMakeLists.txt, RainbowNoise/src/CMakeLists.txt.
**Estado**: prereg y script primero; la auditoría de contenido de Main/Library se ejecutará después de congelar este código.

A — Pregunta y contrato de verdad: ¿expone la fuente original un objetivo DartThrowing y una CLI multiclase orientada a cuotas? ¿Qué dependencias y rutas de CMake condicionan el build? Unidad: cinco ficheros congelados de un commit, NO rendimiento neuronal ni efectividad de Wei.
B — Rivales: H1 objetivo y CLI presentes sin barreras obvias; H0 objetivo ausente/incongruente; H2 objetivo presente, pero otros subdirectorios/bibliotecas o CMake legado bloquean configuración/compilación. Nada de esto prueba que Wei supere o iguale MHU.
C — Contraste: leer los cinco archivos primarios completos por el conector GitHub y ejecutar verificador estático sobre patrones anunciados: declaración de target, referencia a DartThrowing.cpp, mínimos CMake 2.6, indicadores de parámetros multiclase y k/target, subdirectorios. Cada puerta tiene PASS/FAIL/UNKNOWN; compilación/build/salida científica obligatoriamente NOT_RUN.
D — Instrumentación y freeze: este preregistro más w01_source_audit.mjs versionados en GitHub antes del fetch de Main CMake; el SHA de commit del script es el único code_sha relevante. Verificador Node reproducible sobre checkout original y salida JSON.
E — Ejecución: inspección textual primaria efectiva, no simulación experimental. Una vez obtenido código, registrar resultados explícitos e incidencias y versión fuente.
F — Auditoría adversarial: PASS de patrones de código no es prueba de compilación ni de compatibilidad Windows/versión CMake; buscar guardas de compilación/dependencias y diferencias entre algoritmo dart/soft-disk/multi-class. El historial de W01 no es un nuevo dataset empírico.
G — Confirmación: ninguna externa prevista; requerir clon auténtico con CMake compilado y 5 clases/conteos reales, log y hashes, fuera de esta auditoría.
H — Priors: actualizar únicamente operabilidad del comparador, no reivindicación de que MHU sea mejor. Conservar bloqueos por falta de logs.
I — Dictamen: grado científico <= 0/3 por auditoría documental, CT2 geometría matemática 24/100 y CT2 funcional 18/100 inalterados; no atribuir novedad metodológica.
J — Decisión: si no se puede demostrar build/CLI real con fuente y logs, STOP_WEI_BUILD y reservar otros 9; no ejecutar más GP/Fourier N400 bajo STOP_LOCAL.

Reglas: R1–R5, AB 3.2.1 O1–O7; no modificar fuentes originales, no fusionar, no CI, no publicar datos originales privados. 
