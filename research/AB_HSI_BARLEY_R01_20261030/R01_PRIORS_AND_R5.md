# R01 — priors, R5 y plan de evidencia física 2D (2026-10-30)

## Fuente inspeccionada, sin redistribución
- Estudio de cebada `szkymm/Gra_Desi@8157f619f11bef20564067d55450c53120d1a712`, nueve CSV de `results/1722..1730/reflectance_ID.csv`, 204 bandas cada uno y coordenadas X,Y. `image_tag.py` crea centroides de contornos verdes en HSV; `obtain_reflectance.py` consulta valores de raster en dichos centroides. No contiene el cubo hiperespectral de todos los píxeles.
- Al verificar los nueve archivos completos: **542 coordenadas finitas en total**, por archivo **60–61**, sin duplicados X/Y ni filas mal formadas. Extensión del bbox es 138.414–156.984 posiciones por escena; fracción cubierta 0.0003822–0.0004335 (0.0382–0.0433 %). **0/9 escenas ≥400 puntos**. Existen **644 observaciones espectrales >1** de 110.568 celdas, sin valores negativos, que no deben atribuirse automáticamente a fallos instrumentales.
- Primer código congelado contenía dos SHA truncados y abortó antes de producir outcomes. Archivo errata `R01_E01_ERRATA.md`. Código corregido congelado en `b7c9704956b5976ec7f27c70f85db238e8409b42` antes del primer análisis correcto. `R01_REPLAY.json` reproduce mismo JSON con 10/10 verificaciones. **Reproducibilidad técnica misma fuente**, no replicación independiente ni causalidad.

## Priors con falsadores
| Prior | Hipótesis | Evidencia (límites) | Conclusión |
|---|---|---|---|
| R01-P1 | Una colección de datos HSI reales de ≥5 bandas con coordenadas es suficiente para probar N400 | Nueve tablas con 204 bandas reales, pero no imágenes densas: a lo sumo 61 centroides por escena. El sesgo de selección por segmentación verde ya está en código fuente | **REFUTADA para esta fuente** (0/9 disponibles con 400 puntos). No extrapolar a cualquier otro HSI |
| R01-P2 | La geometría de centroides de plantas puede sustituir muestreo retinal optimizado | Coordenadas proceden de contornos de planta, no de proceso de puntos homogéneo. Todos los procesos alternativos requieren mismas oportunidades, matriz de muestras y calibración | **NO_TESTABLE** aquí sin cubo original; inventar 400 puntos del mismo cubo sería inválido |
| R01-P3 | Un cubo hiperespectral pequeño y genuino puede desbloquear un primer diseño N400 sin escena simulada | El repo `earthlab/neonhs` incluye `inst/extdata/ex.h5`, Git blob `b0768d9127de55b7c3064f65c906b5dd04401ebf`, **769924 bytes**. Su README describe imagen de **30×30 píxeles** con **426 bandas**; datos derivados de NEON. No se han leído bytes ni comprobado valores/canal/wavelength/máscaras | **CANDIDATO_DOCUMENTAL**. Falsador: H5 corrupto, dimensiones no esperadas, demasiado invalid pixels, ausencia de derechos o contaminación entre escenas |
| R01-P4 | Es posible ejecutar el comparador original Wei mediante conectividad actual | Git/curl en entorno devuelve `Could not resolve host` para github.com; el conector GitHub sólo permite texto UTF-8 y rechazó el blob binario TIFF/H5 con UnicodeDecodeError | **BLOQUEADO**, no se ha compilado ni ejecutado Wei |
Ningún aumento CT2: matemática 24/100, funcional 18/100, N1=0, N2=0, N3=0.

## R5 y siguiente acción que desbloquea la investigación
**STOP_HSI_SPARSE**: no repetir reconstrucción spectral en esta tabla, no extrapolar centroides para generar una falsa escena 2D, no aplicar MHU/LOCAL/CVT/Wei como si pudiéramos muestrear todos los píxeles.

El objetivo siguiente es obtener y verificar bytes de `ex.h5`, descargable desde `https://github.com/earthlab/neonhs/blob/master/inst/extdata/ex.h5`. Cuando estén disponibles, antes de abrir ciclo R02:
1. Congelar contrato A–J y código SHA; validar hash del archivo físico y dimensiones reales H5. Separar los bands afectados por absorción vapor de agua u otros invalid pixels.
2. Elegir métricas y splits, fijar 400 posiciones distintas en 30×30 y conteos [163,85,68,50,34], sin colisiones de redondeo. Separar original N400 matching de adaptación a resolución.
3. Comparar controles MHU original, LOCAL original, CVT y **Wei auténtico**, pareando oportunidades, presupuesto, semillas y todos los fallos. Wei sigue `NOT_RUN` hasta obtener log/binary real; sin Wei no afirmar paridad completa.
4. Preservar resultados negativos y reservar réplicas por escenas independientes, porque UN archivo 30×30 no prueba generalización.

**Derechos:** NEON publicó un producto de reflectancia pública bajo CC0 según documentación de su catálogo; esto no constituye verificación individual de redistribución de cualquier réplica específica. Código paquete neonhs GPL-3, no afirmar sin comprobar que archivos de muestra sean GPL ni copiar H5 al repositorio público. README Gra_Desi afirma GPL-3 para su proyecto, pero su enlace LICENSE no se encontró; no se han redistribuido sus originales.

**Presupuesto separado**: nueva concesión 5 = 1 ciclo técnico R01 ejecutado, 1 intento instrumental inválido preservado, 0 planificación consumida, 4 nuevas plazas restantes. Concesiones previas: 2 y 9 plazas sin modificar. Sin merge main ni CI costosa.
