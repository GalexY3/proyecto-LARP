# CIERRE DE LA CAMPAÑA AB-R: 15/15 ciclos ejecutados válidos · MHU / LARP · 30-10-2026

## Resumen ejecutivo y contabilidad exacta

**Se agotaron las quince plazas ya concedidas** en tres bolsas que se mantuvieron independientes: 4 recientes R02–R05, 2 recientes anteriores S04–S05, y 9 históricas. **15 ciclos AB-R efectivamente ejecutados como contrastes técnicos/empíricos exploratorios**, **1 intento inválido** (IP03, por instrumentación incompleta, excluido) y **0 ciclos exclusivamente de planificación**. IP16 posterior y explícitamente exploratorio sustituye al inválido IP03, sin crear un decimosexto válido. Contratos y code SHA antes de las observaciones, todos los resultados adversos conservados. Ningún hallazgo nuevo con grado científico 1/3, 2/3 o 3/3; CT2 matemática **24/100** y CT2 funcional **18/100** sin cambios. Estas quince tareas son estimandos dependientes de **una escena física** y **tres geometrías originales pareadas**, NO quince experimentos humanos/espaciales científicamente independientes.

## Primera evaluación ejecutada con un cubo 2D real completo

Fuente externa `helmenov/IndianPines@7b334bb459c5e91c5667e146a56548983b166bb2`, `IndianPines/data/IndianPines.csv`, Git blob `0ed4500533a7c27e479944ce01996e676cabff1d`, 23.274.397 bytes de texto; imagen original AVIRIS de Indian Pines (1992), **145×145 píxeles, 220 bandas crudas** y GT de 17 categorías (incluida la clase 0 sin etiqueta). 21.025 posiciones examinadas, 4.625.500 valores de banda válidos, 0 NaN/negativos detectados; ningún valor del raster original publicado o copiado a la rama. El CSV original deriva de TIFF del proyecto Purdue y fue convertido por un tercero; derechos específicos de redistribución originales **no verificados**. Se procesó exclusivamente como fuente en memoria mediante el conector GitHub UTF-8.

Geometrías de entrada: **seis exportaciones originales de los experimentos N400 de LARP**: 3 semillas `g1101–g1103` × MHU `avian_full_spectral` y LOCAL `avian_local_only`, geometrías float64 serializadas en hex y con 400 puntos reales cada una de `L=20`, cuotas exactamente `[163,85,68,50,34]`. Se congelaron seis Git blob SHA/NPZ metadata en `SOURCE_MANIFEST_PRE_OUTCOME.json`. ESTE experimento **no abrió independientemente los binarios .npz**, por lo que se refiere a geometrías exportadas y a su procedencia declarada, no a una nueva validación del byte source. Se trasladaron al grid 145×145 por suelo del escalado 145/20 y reserva del píxel más próximo libre; en las 12 configuraciones MHU/LOCAL/RANDOM/CVT no se produjo ninguna colisión ni desplazamiento extra. El acto de escalado y discretización siempre modifica la geometría continua.

Controles: un muestreador uniforme de 400 posiciones distintas y un **CVT aproximado** generado con 8 iteraciones de Lloyd en la misma cuadrícula; cuotas por tipo repartidas con permutación de etiquetas independiente de los valores espectrales. NO se ha compilado ni ejecutado el comparador original de Li-Yi Wei 2010; CVT no se presenta como implementación original o como sustituto de Wei. Todos los controles compartieron **4289 píxeles de test** predefinidos en rejilla de paridad, con exclusión de los puntos muestreados por cualquiera de las 12 geometrías. Cinco canales `[20,60,90,130,190]` (base cero), uno por clase de receptor. La métrica MSE normalizado usa promedio de cuadrados de la banda en test, idéntico entre métodos. Tres semillas pareadas no permiten p-valores robustos ni constituyen tres escenas.

## Resultados adversariales nuevos, sin selección de ganadores

**400 puntos, interpolación espacial IDW de 4 vecinos (IP04)**, MSE normalizado menor es mejor: LOCAL `0.009737476503482239`, MHU `0.009771378837888587`, CVT aproximado `0.010198071210583215`, RANDOM `0.010902940787317164`. MHU un **0,35 % peor** que LOCAL en el promedio; MHU ganó en solo 1/3 pares. No hay superioridad funcional robusta de MHU.

**Dependencia del decodificador (IP05–IP07):**
- NN1: LOCAL `0.01376729` vs MHU `0.01399329` (LOCAL gana 3/3 pares).
- IDW8: MHU `0.00936338` vs LOCAL `0.00938839` (MHU gana 2/3).
- Gauss `h=18`: MHU `0.01106681` vs LOCAL `0.01110708` (MHU gana 2/3).
Se invierte el orden por una decisión de interpolación fijada antes de resultados, de forma adversa a cualquier ventaja universal.

**Heterogeneidad contextual (IP08–IP12)**: gradientes altos MHU `0.0114391` vs LOCAL `0.0114744` (MHU ligeramente mejor); gradientes bajos MHU `0.0081044` vs LOCAL `0.0080014` (LOCAL). Sobre GT etiquetado MHU `0.0089326` vs LOCAL `0.0090705`; en GT=0 (sin etiqueta, NO oscuridad) MHU `0.0105627` vs LOCAL `0.0103667`. Los efectos por tipo/banda también se cruzan; nueve coberturas con n>=100 se reportan sin ocultar clases pequeñas o fabricar independencia.

**Presupuestos reducidos (IP13–IP14)**, submuestreo por clase, no nueva optimización: 200 muestras, MHU `0.0121652` vs LOCAL `0.0122716` (MHU ligeramente mejor); 100 muestras, MHU `0.0151069` vs LOCAL `0.0146430` (LOCAL mejor). La ventaja depende de la densidad y la forma de adaptar una geometría preoptimizada.

**Control nulo espacial (IP15)**: permutación bijectiva de los valores de la escena con índice `(97i+1337)%21025`, mismo campo permutado para todos. Errores `CVT=0.0216827 < RANDOM=0.0223112 < LOCAL=0.0226513 < MHU=0.0226561`. Al destruir estructura espacial real, cambia el orden de los rivales y desaparece cualquier ventaja consistente de MHU. El placebo es sintético y **no** se presenta como una segunda escena física.

**Control de competencia CVT (IP16)**: se descubrió que IP03 había calculado solo *desplazamiento de snapping* aunque prometía energía Voronoi, por tanto se declaró INVALID **después de ejecutar los quince originales**, antes de contabilizarlos. IP16 nuevo, con código propio y A–J congelados tras reconocer exposición, midió en tres semillas el error cuadrático de cuantización píxel→sitio más cercano. Tras Lloyd8, energía CVT relativa a inicio `0.9380` y a RANDOM `0.5298`, menor en las tres semillas. El proxy CVT es competente para cuantización **global** aunque no necesariamente para asignaciones multiclase ni reconstrucción espectral; nunca equivalerlo con Wei auténtico. IP16 es validación instrumental EXPLORATORIA, no nueva confirmación externa.

## Archivo de fuentes y reproducción trazable

Todos los análisis son **ejecuciones efectivas**, no promesas a Codex:
- **Pre-registro IP01–IP15:** `4b9dd26385b9cb641f8bd6693d3e37ad10460ebd`.
- **Manifiesto de fuentes SHA:** `4c4dc612655b3e9b7ac0f6c9d779e04712a293e7`.
- **Código completo congelado antes de outcomes:** `9adb7ecb742d39acddb8dda86d35623537797364`, Git blob `773096dc8f95c6247fd0cdd96cd759387df86bfb`.
- **Primer resultado 15 tareas:** `58faddfcdecac349ccc68919ae1721755b0bc362`, `RESULTS_IP01_IP15.json`. Duración observada ~39,6 segundos de cómputo en V8, no estimación de CI.
- **Replay verificable 12/12:** `4840f9032cb28270b1f663737f414872127cdcbc`; fuente y exportaciones refetch, código congelado, igualdad JSON exacta en otra ejecución ~39,9 s. No es replicación científica externa.
- **Errata IP03 invalid:** `3c14c7121032e0f553d0d074b61a2c08fa2eeab5`, `E01_INVALID_IP03.md`. No borrar ni reinterpretar el control incompleto.
- **IP16 nuevo prereg:** `824dc7bdeacf6c7837336c7dd8e22bbc04422b3e`; **IP16 code freeze** `6b6def74ae22c5b8524dfd89b7126a88f76d7a1f`, Git blob `8845356624e261b0b2c055c68a9d4a74d52000b5`; **IP16 resultado** `cc1c63fd341c2f64576f0fd88777960d0a2df852`; **IP16 replay 9/9:** `e85c9fa43b4409d52f264b64fe9168e80ab2d203`, ~31,4s, misma fuente, no replicación externa.
- **Ledger A–J:** `5453229153ecea1538fbb158ac7609c2563aa9c2` `LEDGER_IP01_IP16_AJ.json`, quince entradas válidas y una inválida, sin ciclo de planificación.

## CT2, R5 y siguientes puertas causales

**CT2 N400 matemática 24/100 y funcional 18/100**, ordinales, no probabilidad de verdad; nuevos grados N1, N2, N3: **0**. Ni quince estimandos correlacionados ni una imagen real elevan por sí solos la validez causal/neurobiológica.

**R5**: STOP_LOCAL viejo GP/Fourier/N400 certificado; STOP_HSI_SPARSE antigua cebada; **STOP_AVIRIS_SINGLE_SCENE** para no reoptimizar post outcomes en Indian Pines; STOP_WEI_BUILD hasta compilación auténtica de `1iyiwei/noise@0d1be2030518517199dff5c7e7514ee072037d59`, control semilla y cuotas exactas. Requisitos de avance: **al menos una escena independiente** físicamente calibrada con 5+ bandas, prerregistro de escena/splits antes del score y **comparador Wei auténtico**; además aprendizaje neuronal si se pretende validez funcional retinal. No aceptar licencias ajenas ni contactar autores sin autorización. Ningún dato crudo ni posición individual redistribuida en este proyecto, ningún merge a `main`, ninguna CI costosa activada.

**Balance final:** concesiones agotadas **4/4 + 2/2 + 9/9 = 15/15 válidos**, 1 instrumental inválido conservado, 0 planificación, 0 plazas de esas concesiones pendientes. Solicitar una nueva concesión **solo para evidencia verdaderamente independiente o fuente Wei ejecutable**.
