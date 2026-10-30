# RECIBO FINAL S01–S03 — LARP / MHU, cinco plazas AB-R concedidas (2026-10-30)

## Balance y alcance de la evidencia
**3 ciclos A–J ejecutados / 5 autorizados**, como tareas exploratorias y diagnóstico empírico de un archivo externo con mediciones físicas; **2 plazas nuevas restantes**. Además **1 intento inicial inválido** (S01 parser), preservado y reparado sin sumar otro válido; 0 ciclos solo planificación. **9 plazas históricas anteriores** siguen separadas. No se han ejecutado 3 experimentos científicos independientes: S01/S02/S03 dependen de un mismo dataset Sentinel-2 y S03 es auditoría post-S02. Nuevos hallazgos 1/3: **0**; 2/3: **0**; 3/3: **0**. CT2 LARP matemática 24/100 y funcional 18/100, sin movimiento.

## Objetivo original y límite de ejecución
Comparador original Li-Yi Wei `1iyiwei/noise@0d1be2030518517199dff5c7e7514ee072037d59` con licencia MIT verificada (upstream LICENSE blob 799260fde190f9bcfec38003c4d67f09915c935a). En el entorno local, `git ls-remote` falló con `Could not resolve host: github.com`; el conector GitHub permitió leer código y crear commits, no transportar todo el checkout para compilar. El `wei-build.log` de Windows aún no está en la sesión. **No se ha compilado ni ejecutado Wei auténtico, ni producido salida con cuotas exactas N400.** El guion `wei_windows_source_pinned.ps1` es solamente una herramienta lista para inspeccionar el log o lanzar compilación local con intervención humana, marcada `PREPARED_NOT_EXECUTED`. No cuenta como ciclo.

El archivo de Harvard/CAVE/ICVL de escenas 2D multibanda no se ha descargado ni evaluado. Se localizó, sí, una clase nueva de observación física: un conjunto de coincidencias de producto Sentinel-2 con muestras georreferenciadas y siete bandas, que **no son imágenes espaciales bidimensionales completas**. Fuente `chuishun-kong/id-dbo` commit `26b8f243bdf3574ea2bb25eee927c720fa309dcb`, CSV `data/matchup/satellite_rrs_gee_full.csv` Git blob `4e6e5794d7c8f78b607fb7aa48b71edd918bd28a`. Los propietarios del repositorio declaran que los registros in-situ GLORIA se solapan con el desarrollo, por lo que no autorizan a presentar estos resultados como validación satelital independiente de su propio modelo. No se han republished CSV, coordenadas originales ni geometrías N400 en esta rama.

## S01: filtro empírico de calidad de siete bandas, con errata visible
Contrato A–J `S01_PREREG_AJ.md` commit `3fc4b71888b662f6326cf571a738053a948a7059`. Código congelado `S01_AUDIT.js` commit `2fc407de56ba22a0bc42576b0fe3c14f80e49613`. Intento inicial `S01_RESULTS.json` commit `96fc59f4dc2e83a1b30cb6636ca411b86b3609a8` INVALID: el parser `line.split(',')` rechazó dos filas donde el nombre `"Gulf of Mexico, FL"` tiene una coma entre comillas. Errata comprometida `4dfd7f0c0d148cff38a14bcecdc1f00ed073180e`, reparación de lector CSV comprometida `431e9cd428672657d0e86e216d7f1224a88b2a84` antes del nuevo resultado `2e8068f2772479013161ee519fb01b067139277c`. Clasificación: `POST_EXPOSURE_REPAIR_EXPLORATORY`, no confirmación independiente.

Resultados reparados: **397** registros, **63** sitios, 4 filas con cero píxeles válidos, 0 duplicados exactos; **388** registros y 57 sitios con al menos 10 píxeles; **329** registros y 52 sitios bajo filtro final de nubosidad ≤20% y desfase temporal ≤5 días. Cumple preregistro para S02. Resultado de factibilidad, no validación MHU.

## S02: contraste real multibanda separado por sitio/producto
Contrato `S02_PREREG_AJ.md` `f73c3faa16d59f1a416005b9c7ec20293c5211c4`, código congelado `S02_MODEL.js` `a813f0dc636f3dccfcf6d9849f7a4721c7f2929e`, resultado `S02_RESULTS.json` `1d6ffe5f6ee7a819958993b7381699267861a6d2`. Estimando: MSE de dos bandas B4 y B6 a partir de cinco B1,B2,B3,B5,B7, con unidades de evaluación independientes por nombre de sitio, exclusión adicional de TODOS los productos satelitales compartidos con ese test. 34 sitios (≥2 observaciones), conjunto de 329 filas, 71 bloqueos adicionales de productos repetidos a través de folds. Interpolación por índice ordinal como control sencillo; regresión ridge con lambda=1.0, variables z-score entrenadas solo con train, no ajuste post-outcomes; media de train como control nulo.
- MSE promedio igualando peso por sitio: ridge **0.00007003631319400662**, interpolación ordinal **0.00023420490566524287**, constante train **0.0025933438165327465**.
- Ridge MSE relativo ordinal **0.29904**, menor **70.1%**; 31 de 34 sitios gana ridge.
- Límites: el ordinal de banda no equivale a separación física real, fuente GLORIA con dependencias, muchos registros de mismo sensor y fecha, posible diferencia conceptual entre reflectancia de superficie S2_SR_HARMONIZED y reflectancia de agua Rrs científicamente calibrada. NO demuestra causalidad ni mejora MHU.

## S03: control más fuerte por longitud de onda física
Disparada por anomalía/posible debilidad S02. Contrato previo a sus propios outcomes `S03_PREREG_AJ.md` commit `b0a47295db6c6f3dc861dd9ed5183cb5a08d1398`, código `S03_WAVELENGTH.js` `2385f6acd05ed2392648e56ede8e75491041c132`, resultado `S03_RESULTS.json` `1bc26f8252d2bc9d1ce532b331904b2644cb72ba`.
Fuentes de centros de banda por sensor: `chuishun-kong/id-dbo/src/data/gloria_loader.py` SHA `284f9cc05bce08a0cb214d9e7e6d6490a2c5a7a5`, `tools/satellite/run_acolite_batch.py` SHA `e45a249114324eeda0bb71d1fbada44619cd4ab0`. S2A [443,490,560,665,705,740,783] nm; S2B [442,492,559,665,704,739,780] nm. Interpolación con fracciones físicas entre B3-B5 para B4 y B5-B7 para B6. Mismos 34 folds, no reentrenamiento del ridge ni exposición al dato target del test.
- Interpolación física site-MSE **0.00023276954140307455**, casi igual a ordinal **0.00023420490566524287**; ridge **0.00007003631319400662**, ratio ridge/física **0.30088** (aprox 69.9% menos MSE).
- Ridge gana ahora **26/34** sitios, no 31/34. La función lineal por centro de banda NO equivale a convolution SRF; `assets/srf/srf_manifest.json` del upstream indica SRF S2B como placeholder. Análisis exploratorio adaptativo, no confirmatorio ciego.

## Replay, decisiones y no-hallazgos
`REPLAY_S01_S03.json` commit `e71dc75580ef0e4ea6737669e4737b87e96e1697`: **12/12** invariantes PASS, incluidas equivalencia JSON de los tres resultados tras recuperar de nuevo fuente y código original congelados. Esto acredita repetibilidad técnica sobre la misma fuente, no replicación científica independiente ni validación en clon limpio de todos los entornos.

Priorización R5:
- `STOP_LOCAL`: no repetir GP/Fourier N400 y gráficos simulados ya agotados.
- `STOP_SATELLITE_MATCHUP_SOURCE`: no consumir más ciclos con cambios de semillas o modelos ligeros sobre el mismo CSV; S02 y S03 resolvieron su comparación concreta.
- `STOP_WEI_BUILD`: permanece hasta recibir `wei-build.log` Windows o conseguir clonar y compilar el SHA auténtico con control de cuotas y semilla.
- Si se adquieren escenas 2D multiespectrales genuinas con permisos, preregistrar controles MHU/LOCAL/CVT/Wei, preservando densidad, radios, semillas, tiempo y splits por escena.

**Protección:** no se ha aceptado licencia alguna en nombre del usuario, no se han contactado autores, no se han publicado datos crudos, no se ha iniciado CI costosa, no se ha hecho merge. Balance final de concesión: 3 ejecutados exploratorios, 1 intento inválido, 0 planificación, 2 restantes; más 9 históricos en saldo separado.
