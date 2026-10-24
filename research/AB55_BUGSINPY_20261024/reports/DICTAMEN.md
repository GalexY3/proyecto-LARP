# LARP AB55 BugsInPy — Dictamen de investigación, 24/10/2026

## Contrato y clasificación correcta

Autorizados 20 ciclos AB de auditoría de defectos reales, 5 ciclos AB de planificación intensiva y 30 ciclos AB de exploración. El material obtenido consiste en **50 expedientes A–J documentales y 5 expedientes A–J de planificación**. **CERO defectos reproducidos dinámicamente y CERO pruebas metamórficas ejecutadas sobre esas versiones históricas**. Los registros sí contienen commits originales y análisis de sus archivos modificados. No llamar a esto 55 ensayos experimentales de detección. La puerta de evidencia para el objetivo original sigue pendiente.

## Fuentes y selección

Dataset original: BugsInPy (soarsmu/BugsInPy), Widyasari et al., ESEC/FSE 2020, DOI 10.1145/3368089.3417943. 
Q01–Q20: PySnooper 3, Cookiecutter 4, tqdm 5, Black 4 y Matplotlib 4; se conocieron los archivos de algunos fixes antes del preregistro, por tanto POST-EXPOSURE.
X01–X30: pandas 6, FastAPI 6, spaCy 6, Matplotlib 6 y Black 6, identificadores congelados antes de inspeccionar sus arreglos.

Para cada caso se verificaron los SHA buggy/fixed, la versión histórica Python 3.6.9–3.8.3, el archivo de prueba declarado, el asunto del commit upstream, su lista de archivos y líneas modificadas. Los registros completos están en results/. Un commit reparador no prueba que el defecto falle o que nuestro método lo detecte localmente.

## Resultados de las 50 auditorías de procedencia

Los 50/50 commits de corrección incluyen cambios en rutas de tests. La mediana de líneas modificadas de código Python de implementación es 6, con rango 1–159. Esta selección es curada, NO una muestra aleatoria de bugs del mundo; la co-modificación de tests es esperable y no es una contribución científica original ni una tasa de detección. No calcular p de significación ingenuo o reclamar 2/3. Véase results/AGGREGATED_50.json.

## Error de instrumentación y reparación

El extractor consultó FastAPI bajo la URL histórica tiangolo/fastapi, que ahora devuelve Moved Permanently sin arreglo de archivos. El código inicial interpretó erróneamente la ausencia como cero modificaciones. Los resultados X07–X12 originales son INVALID y están preservados. Antes de repetir se registró prereg/REPAIR_R1_FASTAPI_REDIRECT.md; se verificó el SHA del commit contra la URL canónica fastapi/fastapi y se generó results/X07_X12_FASTAPI_R1.json. Los seis contienen cambios de tests. La reparación es POST-EXPOSURE y NO equivale a confirmación externa.

## Cinco planes intensivos AB (P01–P05)

P01, D1,2: encapsulado reproducible de Python/dependencias históricos y prueba de paridad buggy/fixed. No ejecutado.
P02, D2,1: ceguera del diseñador ante el commit arreglado; SHA de propiedades antes de desvelarlo. No ejecutado.
P03, D2,4: presupuesto de diseño, llamadas de programa, CPU y falsos positivos frente a tests profesionales. No ejecutado.
P04, D3,7: DRIFT hacia clases de equivalencia de relaciones metamórficas y minimización de tests; propuesta combinatoria, con antecedentes de mutant subsumption y test-suite reduction; CT2 hipotética de esa rama 12/100, no validada.
P05, D1,8: transferencia documental a 30 nuevos identificadores preseleccionados; los metadatos se auditaron, ninguna ejecución dinámica.

Cada plan contiene A–J, hipótesis rivales, falsador, requerimientos de evidencia y decisión en planning/P01_P05_INTENSIVE_AB.json. No son hallazgos 1/3.

## CT2, registros y estado científico

CT2 de la línea principal QuixBugs→BugsInPy: inicial 11/100, final 8/100, por no haber logrado reproducción histórica, una comparación ejecutada y un descubrimiento discriminante original. Rama alternativa P04 D3,7: CT2 12/100 de planificación únicamente; no sumar con la principal.

Hallazgos 1/3 nuevos: 0. Registro permanente auditado previo: 6 hallazgos distintos en research/FINDINGS_1_3/LEDGER.json de main. N2=0 y N3=0. No crear hallazgos por extracción de Git, corregir URL o proponer un diseño sin ejecutarlo.

Para 2/3 faltan: una predicción nueva tras literatura, bug reproduciéndose en dos revisiones bajo entorno verificable, pruebas diseñadas sin leer el arreglo, presupuesto comparable y validación externa independiente. Los 50 metadatos no satisfacen estas puertas.

## Auditoría documental y decisión

GitHub conserva el preregistro de 55 expedientes, contrato de medición, cuatro archivos Q, cinco archivos X corregidos, el archivo inválido y su errata, cinco planes, resumen y este dictamen. No está demostrado un clon limpio ni ejecución histórica; no prometerlo. Decision AB: STOP_LOCAL de inferencias de detección sin ejecución; PIVOT a reproducir defectos bajo entornos reales antes de pedir más metadata. Cualquier solicitud nueva de ciclos debe seguir O6, entre 20 y 45.
