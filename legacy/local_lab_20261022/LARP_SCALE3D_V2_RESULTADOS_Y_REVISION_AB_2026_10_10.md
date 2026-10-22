# LARP — Resultados finales de Scale3D v2 y revisión de creencias

**Fecha:** 10 de octubre de 2026, Europe/Madrid. **Estado:** entrenamiento COMPLETO; comparación exploratoria de densidad sensorial, con dos semillas por tamaño. **Endpoint:** update1800, común a las ocho tríadas. **Conclusión:** aumentar densidad permite aprender parcialmente la tarea difícil y las geometrías relajadas superan al patrón aleatorio; no aparece una ventaja consistente de la penalización MHU adicional frente a LOCAL. No se prueba una ley universal de escala ni se refuta MHU en todos sus posibles usos.

## 1. Terminación y verificación

El guardian inició a las **04:12:11** y terminó a las **05:48:58 de Madrid**, con `FINISHED`, código de salida0. El entrenamiento registró **5803,689 s: 96,73 minutos**; el guardian completo, 5806,950 s. Se completaron cuatro tamaños × dos semillas × tres brazos: **24 redes**, 1800 updates cada una, 43.200 updates de red en total. Hay32 checkpoints de tríada —cuatro por caso— que contienen los tres modelos y sus optimizadores.

Verificamos los13 hashes congelados de fuentes/config/protocolo/calificación, ocho resultados individuales contra el agregado, cuatro checkpoints de evaluación por tríada y la existencia de sus pesos. Recalculamos **288 medias** desde **18.432 errores de mundo** y contrastamos las12 filas del CSV automático. Comprobamos forma, coordenadas periódicas finitas y conteos de los24 arrays geométricos; reconstruimos las puertas desde sus métricas almacenadas. Todas esas comprobaciones pasan.

**Alcance de la auditoría:** aritmética, integridad, coherencia de artefactos y lectura del código; no se regeneraron todas las geometrías ni se recalcularon logits desde los pesos. Los18.432 errores no son18.432 réplicas independientes. El pico registrado de memoria asignada por Torch fue **7,645 GiB**, para el proceso con los tres brazos; no es una medición del consumo total del sistema. La suma de temporizadores de entrenamiento fue5229,567 s; generación, evaluación, guardado y overhead explican parte del tiempo restante, sin una descomposición exhaustiva.

Fuentes: `runs/scale3d_v2/{results,runner,protocol}.json`, resultados/evaluaciones por tríada y `comparison.csv`. Cálculo reproducible y recibo: `artifacts/scale3d_v2_analysis_20261010/{analyze.py,analysis.json,learning_curve.csv}`. El script es análisis de lectura; no entrena.

## 2. Qué se comparó

Cada red tiene **4.827.415 parámetros**, ocho bloques residuales diferentes, anchura256 y16 vecinos por nodo. Es una GNN espacial; no es Transformer ni el GGNN pequeño de los experimentos b0/XOR. Los brazos comparten pesos iniciales, mundos, targets, currículo y número de pasos dentro de cada tríada. Se entrenaron desde cero para cada tamaño: esta prueba **no evalúa transferencia de una red entrenada en N pequeño a N grande**.

- **RANDOM:** posiciones uniformes iniciales, sin relajación.
- **LOCAL:**600 pasos de repulsión de densidad suavizada mediante CIC/FFT, sin término espectral adicional.
- **MHU:** mismo término local más penalización de Fourier para unión y cinco tipos, con peso inverso de norma cuadrada.

N toma1024/4096/16384/32768, seeds3201/3202. Campos de tarea y queries viven en el mismo toro unitario. Subir N añade sensores, cambia posiciones/conexiones/puertos y reduce el radio físico por capa en ese dominio; mantiene parámetros, grado y profundidad. Igualar parámetros y pasos no iguala FLOPs ni tiempo. La semilla geométrica también determina la inicialización neuronal y los mundos de train: dos semillas son **dos realizaciones compuestas**, no factores geométricos y neuronales replicados por separado.

Cada sensor mide exclusivamente el canal de su tipo. Hay cinco campos gaussianos independientes, varianza marginal1 y media0. T0 reconstruye los campos suaves; T1 los de frecuencia media; T2 requiere los productos `f0f1`, `f1f2`, `f2f3`, `f3f4`, `f0f2f4` de campos de frecuencia alta. MSE menor es mejor. Predecir cero tiene riesgo esperado1 en cada tarea; esa cifra poblacional no es el score exacto de una muestra finita ni un umbral preregistrado de competencia.

Test:64 mundos nuevos y256 queries reservadas; los mismos mundos y queries se reutilizan entre brazos, tamaños y checkpoints. Se eligió previamente1800 como endpoint completo común; los checkpoints anteriores sirven para diagnóstico. No se selecciona el mejor mirando test.

## 3. Resultados finales agregados

Media aritmética de las dos semillas. **R_L** es cociente de medias MHU/LOCAL y **R_R**, MHU/RANDOM: valores menores que1 favorecen MHU. El informe automático original usa, en sus columnas de cocientes, **media de cocientes emparejados**; ambas definiciones son legítimas descriptivamente pero diferentes. Aquí se explicita la elegida.

| N | Tarea | MHU | LOCAL | RANDOM | R_L | R_R |
|---:|---:|---:|---:|---:|---:|---:|
|1024|0|0.111238|0.141024|0.307722|0.7888|0.3615|
|1024|1|0.556071|0.547430|0.646422|1.0158|0.8602|
|1024|2|1.008393|1.008511|1.008606|0.9999|0.9998|
|4096|0|0.076617|0.054768|0.094195|1.3989|0.8134|
|4096|1|0.147812|0.134466|0.274833|1.0993|0.5378|
|4096|2|1.008422|1.008167|1.008026|1.0003|1.0004|
|16384|0|0.037646|0.046509|0.067419|0.8094|0.5584|
|16384|1|0.038437|0.042334|0.108651|0.9080|0.3538|
|16384|2|0.510446|0.491302|0.736578|1.0390|0.6930|
|32768|0|0.060835|0.046142|0.086500|1.3184|0.7033|
|32768|1|0.048966|0.030098|0.084469|1.6269|0.5797|
|32768|2|0.239350|0.220206|0.513564|1.0869|0.4661|

![MSE final por densidad; bandas son rangos de dos semillas](C:/Programación/LARP/artifacts/scale3d_v2_analysis_20261010/endpoint_MSE.png)

La línea1 es el riesgo poblacional del predictor cero. Las bandas muestran mínimos/máximos de dos semillas, **no intervalos de confianza**.

### 3.1 Tarea difícil: la mejora con densidad existe, pero LOCAL conserva la ventaja

A N1024/4096, los tres brazos permanecen alrededor de1,008: aprendizaje útil de productos no establecido por esos scores. A N16384, MHU/LOCAL/RANDOM alcanzan0,510446/0,491302/0,736578. A N32768,0,239350/0,220206/0,513564. Las redes grandes han aprendido algo sustancial sobre los productos; la lectura «ninguna de estas redes puede aprender T2» queda descartada para este régimen y presupuesto.

A N32768, MHU reduce MSE frente a RANDOM en **53,4%**; LOCAL la reduce en **57,1%**. Frente a LOCAL, MHU tiene **8,7% más error**. A N16384 tiene3,9% más error. LOCAL gana las dos semillas de T2 en ambos tamaños grandes. Esto es evidencia descriptiva contraria a una ventaja específica del término MHU en esa tarea, bajo este protocolo. No identifica por qué gana LOCAL ni una inferioridad universal de MHU.

La mayor parte de la mejora de escala también aparece en LOCAL y RANDOM. Un beneficio de aumentar sensores no implica que la **ventaja relativa de MHU** crezca. En T2 el cociente MHU/LOCAL crece de≈1 a≈1,039 y1,087: la predicción simple «más grande hace que MHU gane más frente a un rival relajado fuerte» no recibe apoyo aquí.

### 3.2 Reconstrucción: hay una ventana favorable y un tamaño grande inestable

A N16384, MHU supera LOCAL en T0 y T1 **en ambas semillas**: medias menores un19,1% y9,2%, respectivamente. Es una señal condicional que merece conservarse; no se deben borrar los resultados favorables porque el contraste difícil haya sido negativo.

A N32768, LOCAL tiene menor media en las tres tareas. En T0 y T1 el ganador cambia entre semillas; no es una derrota uniforme de MHU por realización. T0 es especialmente dispersa: una semilla da MHU/LOCAL≈4,100 y la otra≈0,233. El cociente de medias es1,318; la media de cocientes del informe automático es2,167. Ninguno autoriza decir que «MHU es exactamente el doble de peor» en una población de redes.

T0 MHU no mejora monótonamente: media0,111238→0,076617→0,037646→0,060835. T1 mejora entre los extremos para los tres brazos, pero MHU también sube de0,038437 a0,048966 entre N16384 y N32768 (+27,4%); LOCAL y RANDOM sí descienden en los cuatro tamaños. T2 cambia mucho entre los dos tamaños menores y los mayores. Estas diferencias por tarea son incompatibles con una narración de superioridad uniforme de una geometría.

## 4. Todas las realizaciones, sin ocultar dispersión

Valores en update1800. Cada celda contiene **T0 / T1 / T2**.

| N | Seed | MHU T0/T1/T2 | LOCAL T0/T1/T2 | RANDOM T0/T1/T2 |
|---:|---:|---|---|---|
|1024|3201|0.101739 / 0.554302 / 1.008402|0.178555 / 0.554752 / 1.008500|0.243615 / 0.632574 / 1.008596|
|1024|3202|0.120738 / 0.557840 / 1.008385|0.103493 / 0.540107 / 1.008521|0.371830 / 0.660271 / 1.008616|
|4096|3201|0.096171 / 0.161321 / 1.008102|0.047700 / 0.125966 / 1.007364|0.092392 / 0.269586 / 1.007834|
|4096|3202|0.057064 / 0.134303 / 1.008742|0.061837 / 0.142966 / 1.008970|0.095997 / 0.280080 / 1.008218|
|16384|3201|0.040764 / 0.036181 / 0.503211|0.045313 / 0.043077 / 0.487797|0.061858 / 0.109640 / 0.734180|
|16384|3202|0.034528 / 0.040693 / 0.517680|0.047705 / 0.041590 / 0.494806|0.072980 / 0.107662 / 0.738977|
|32768|3201|0.106188 / 0.076062 / 0.244393|0.025898 / 0.031625 / 0.221817|0.079017 / 0.079310 / 0.511230|
|32768|3202|0.015482 / 0.021869 / 0.234307|0.066387 / 0.028571 / 0.218596|0.093984 / 0.089628 / 0.515897|

No sumar victorias como si las24 comparaciones tarea×caso fueran24 ensayos independientes. Las tareas comparten modelo y los tamaños de una misma semilla comparten inicialización/mundos; el mismo panel test aparece repetidamente. Con dos semillas no ajustamos una ley de escala, no hacemos pruebas de significación poblacional y no inventamos probabilidades posteriores estrechas.

## 5. La geometría pasa la puerta, pero conserva un artefacto

Las **ocho MHU** pasan el certificado finito. Su peor media de banda completa entre componentes está entre0,001539 y0,002197, muy por debajo del límite0,20. La media de la unión está entre0,000332 y0,000697. La reparación espectral v2 resolvió el bloqueo técnico observado en las semillas grandes v1; no demuestra que todo generador v1 falle ni que este constructor esté ya listo como retina desordenada.

LOCAL pasa en **3/8**: ambas N1024 y N4096/3201. Las otras fallan por alguna primera shell, aunque su media completa de banda es pequeña. Su peor media por componente queda0,032184–0,040111 y su media de unión0,008435–0,011585. RANDOM falla8/8; su media de unión está alrededor1. Por tanto LOCAL también suprime notablemente potencia baja, aun cuando no supera cada requisito de la puerta. No es un contrafactual universal «sin hiperuniformidad» por llamarse LOCAL.

La potencia continua coherente en ejes de la malla, `S(G e_d)/N`, permanece aproximadamente **0,073–0,110 en MHU** y **0,177–0,203 en LOCAL**. Es coherencia de modos particulares, **no porcentaje de varianza total**. Un patrón puede pasar bajas frecuencias y mostrar orden de celda a otras frecuencias. Tampoco basta esta medida para clasificarlo completamente como cristal: falta auditoría más amplia de desorden, angularidad y ventanas.

El estudio nuevo de ChatGPT aporta precisamente una explicación y una intervención sobre ese problema; se describe en§9. Sus resultados no alteran retrospectivamente las nubes ni los scores neuronales v2.

## 6. Dos explicaciones nuevas que merecen discriminación

### 6.1 Umbral de información disponible por canal

Los conjuntos de modos contienen16/115/512 pares complejos: **32/230/1024 coeficientes reales por campo**. Las observaciones son sin ruido y lineales en esos coeficientes, antes del target de productos. Conteos por tipo:

| N | Tipo0 | Tipo1 | Tipo2 | Tipo3 | Tipo4 | Coeficientes por campo difícil |
|---:|---:|---:|---:|---:|---:|---:|
|1024|417|218|174|128|87|1024|
|4096|1669|871|696|512|348|1024|
|16384|6676|3482|2785|2048|1393|1024|
|32768|13353|6963|5571|4096|2785|1024|

El tipo raro pasa de348 a1393 observaciones justamente cuando T2 mejora mucho. A N1024 todos los canales son globalmente submuestreados para esos1024 coeficientes; a N4096 lo son cuatro de cinco. Una matriz de adquisición con n_c filas tiene rango≤n_c: el déficit dimensional es real. Tener n_c≥1024 permite rango completo, **no lo garantiza ni asegura buen condicionamiento o acceso local**. No hemos medido todavía esos rangos, sus espectros singulares ni un riesgo Bayes global exacto para estas nubes.

Esto genera una hipótesis post hoc: parte importante del salto puede venir de identificabilidad y cobertura sensorial. No es prueba de capacidad computacional emergente ni mecanismo ya establecido. Una red puede inferir productos parcialmente sin reconstruir cada campo entero; el oráculo pertinente es el riesgo del target en queries, no sólo el rank de coeficientes. La prueba barata siguiente es comparar posterior/reconstructor global fuerte con posterior basado en observaciones accesibles al grafo, antes de otra batería de entrenamiento.

### 6.2 Interferencia al cambiar el currículo

El calendario usado dio exactamente **492/464/844 updates** a T0/T1/T2; todos los brazos comparten esa secuencia. Los productos entran después del paso600. En MHU, T0 media de semillas600→1800:

- N16384:0,009586→0,037646, **×3,93**.
- N32768:0,006905→0,060835, **×8,81**; en1200 llega a0,177684 y después recupera parte.
- N32768/3201:0,006579→0,106188, **×16,14**; seed3202 también empeora, ×2,14.

LOCAL y RANDOM muestran deterioro de T0 a escalas grandes. Es compatible con interferencia/olvido curricular o inestabilidad de optimización, pero no demuestra mediación causal: cambian tareas y trayectoria conjuntamente y no hay un control T0-only continuado ni tarea-mixture constante emparejado.

![Evolución de T0; escala logarítmica y rangos descriptivos](C:/Programación/LARP/artifacts/scale3d_v2_analysis_20261010/task0_curriculum.png)

No sustituimos el endpoint final por600 para salvar un ganador. Registramos una limitación del entrenamiento y una hipótesis nueva. Para probarla, una intervención principal de currículo debe mantener tarea, geometría, pasos y evaluación comparables; no sumar a la vez más profundidad, global attention, LR distinto y pérdidas auxiliares.

## 7. Qué cambian mis creencias

Es una **revisión cualitativa**, sin probabilidades numéricas ni Bayes factors. Las etiquetas siguientes son nuevas y retrospectivas; no son priors preregistrados ni hipótesis confirmadas usando su mismo dato motivador.

| Proposición de trabajo | Revisión razonada | Estado/alcance |
|---|---|---|
| H-SCALE-COMPETENCE: el sistema aprende productos en el régimen de suficiente densidad | Aumenta la confianza: hay errores finales muy inferiores al riesgo esperado cero en N grandes | Observación exploratoria; no se inventa una puerta de competencia |
| H-SCALE-MHU-ADDITIONAL: la penalización espectral adicional mejora consistentemente al subir N | Disminuye confianza en esa regla dentro de este ensayo: LOCAL gana T2 a ambos tamaños grandes; la señal favorable de T0/T1 a N16384 no persiste uniformemente | Utilidad condicional abierta; causalidad espectral no identificada |
| H-SCALE-LOCAL-PACKAGE: organización local y efectos de adquisición/wiring explican parte de la ventaja frente a RANDOM | Explicación de trabajo preferida: LOCAL conserva y supera beneficios relevantes | No es mediación aislada de cobertura ni de separación |
| H-SCALE-GENERATOR: inversa de norma cuadrada permite satisfacer la puerta finita en las escalas bloqueadas | Respaldada técnicamente en las realizaciones examinadas | Sin afirmación asintótica, retiniana o neuronal |
| H-SCALE-INFORMATION-THRESHOLD | Hipótesis generada al observar el salto y los counts; prioridad alta para oráculo global/local | Falta medir rango, condicionamiento y riesgo del target |
| H-SCALE-CURRICULUM-INTERFERENCE | Hipótesis generada por deterioro de T0 después de600 | Falta intervención prospectiva discriminante |

**Conservo H1–H6/C y sus priors históricos intactos.** H1 requiere separar posiciones/estructura de organización de marcas; H2, perturbaciones de robustez; H3, intervenciones sobre heterogeneidad funcional; H4, contrastes de transporte/routing; H5, plasticidad/warm starts; H6, aislamiento de multihiperuniformidad más allá de regularidad local. Esta batería no contiene esos estimandos y controles. Cinco tipos de sensor no equivalen a cinco funciones neuronales necesarias. La competencia aquí tampoco resuelve XOR ni abre las puertas históricas del GGNN32.

Se registra un evento nuevo bajo `docs/hypotheses/`, con `belief_revision` y `hypothesis_generation` separados. `objective_revision`: ninguna promoción automática de MHU ni cambio de misión. `decision`: diagnóstico siguiente y dossier externo, sin lanzar entrenamiento nuevo por este informe. La cartera del9 de octubre se conserva como historia; estos resultados no obligan a escalar otra vez ni restituyen la prioridad neuronal de MHU.

## 8. Decisión práctica

**Cerrar esta batería como completa e informativa.** No repetirla a mayor N por inercia. Ha demostrado aprendizaje parcial a densidad grande, una ventaja de geometrías relajadas sobre RANDOM y ausencia de ventaja MHU adicional consistente en la tarea difícil. Mantener el resultado favorable de reconstrucción a N16384 como pregunta condicional.

Antes de nuevo entrenamiento, dos frentes pueden avanzar en paralelo: **oráculos de información/decodificación** sobre las nubes ya recibidas y **reparación/auditoría del constructor**. Una nueva comparación neuronal deberá conservar un contraste espectral identificable, usar controles fuertes y evitar interpretar el ajuste de malla como biología.

Si el oráculo global ya explica el salto por adquisición, priorizar muestreo/reconstrucción. Si el global es competente y el local pierde información, investigar alcance/transporte. Si ambos tienen buen riesgo y la red queda lejos, investigar decodificación/optimización con una sola intervención. Si eliminar la malla vuelve indistinguibles espectralmente MHU y LOCAL, el contraste de interés debe rediseñarse; la etiqueta de brazo no lo rescata.

## 9. Qué aporta el estudio CIC recién recibido

Fuente aislada: `docs/external_research/chatgpt_cic_2026_10_10/`. ArchiveSHA256 `7440888d1ff370325b136ede2966d5ca9922d4f59b892012e8b34ceff2855aff`. Sus scripts y propuestas no se integran automáticamente en producción.

ChatGPT muestra una identidad útil: con amplitudes por tipo F_c, amplitud unión Z y counts n_c, `D=Σ|F_c−(n_c/N)Z|²/n_c=ΣS_c−S_union`. Bajo barajado de marcas a posiciones fijas, `E[D]=(C−1)(N−S_union)/(N−1)`. Los picos por tipo pueden heredarse de una onda común de posiciones; máximos brutos no demuestran orden adicional de marcas. El control shuffle es un diagnóstico condicional, no un patrón admisible ni una ablación funcional justa.

La autoenergía de un punto CIC con pesos Fourier no negativos se minimiza en el centro de celda. Un origen uniforme independiente nuevo por paso anula su **gradiente propio esperado condicionado al estado**, sin anular necesariamente alias de pares ni el efecto no lineal de Adam. Hay datos exploratorios CPU:12 construcciones N400 —seis parejas, tres semillas— y8 N4096 —cuatro parejas, dos semillas—. En N4096:

| Seed/brazo | Potencia axial media fija→fresca | Puerta fija→fresca |
|---|---:|---|
|1041 LOCAL|0,1812→0,0470|falla→pasa|
|1041 MHU|0,0909→0,0088|pasa→pasa|
|1042 LOCAL|0,1944→0,0136|falla→pasa|
|1042 MHU|0,0941→0,0043|pasa→pasa|

También mejoran los máximos de39 modos y separación NN en esas parejas. Se verificaron localmente128/128 entradas del manifiesto,29/29 referencias declaradas, identidad de ambos generadores y6/6 arrays grandes contra nuestras nubes. Un recálculo desde los20 NPZ nuevos de métricas de39 modos, fases, separación global/homotípica y primera shell N4096 coincide, error máximo≈1,33e−14. Los12 tests CPU revisados pasan. **No se repitió el entrenamiento de construcción**; estos datos continúan siendo construcciones externas, no nuevas réplicas de nuestro PC. Los hashes acreditan integridad, no fecha previa independiente de preregistro.

El origen fresco es por ello un candidato técnico mejor fundamentado, con **2/3 de utilidad interna y1/3 de novedad acreditada** como valoración ordinal. No tiene aún comparación CUDA N32768 ni evidencia neuronal nueva. El salto de los scores v2 sigue siendo de las geometrías antiguas con origen fijo. No mezclamos ambos estudios para afirmar que una red entrenada con v3 ganó.

Un matiz de fidelidad: el runner externo utiliza semilla de auditoría muestreada0, mientras `generate_v2` usa `geometry_seed+99871`. Primera shell y banda completa siguen verificadas, pero la puerta muestreada no es idéntica por construcción; una transferencia local debe explicitar y congelar esa semilla. Sus auditores de seis métricas leían parte de los indicadores homotípicos/admisión del JSON; nuestro recálculo separado amplía la comprobación indicada arriba, sin convertirla en reproducción de la optimización. Además, `D/E_shuffle[D]` no debe interpretarse cuando el denominador se aproxima a cero: corresponde marcarlo indefinido.

La separación densidad/concentración tiene antecedentes clásicos en [Bhatia–Thornton, Physical Review B (1970)](https://doi.org/10.1103/PhysRevB.2.3004), cuyo abstract y metadatos se verificaron. No se reclama una nueva teoría por aplicar una proyección finita. Las fuentes particle-mesh del informe recibido necesitan revisión completa si se usan para escoger la reparación definitiva; el siguiente encargo pide precisamente esa tarea.

## 10. Transferencia

El MD anterior `LARP_CHATGPT_RESEARCH_HANDOFF_2026_10_10.md` y su ZIP conservan un corte de5/8 a las05:44:53 de Madrid. **No se reescriben:** este informe aporta el cierre8/8 y las hipótesis nuevas. El nuevo encargo para Sol/ChatGPT incorpora estos resultados y reconoce que las pruebas CPU N400/N4096 de origen fresco ya están hechas; no pide repetirlas por inercia.

Veredicto de validación: **compartible con los límites indicados**, dentro de la aritmética y procedencia revisadas. Son resultados científicos útiles de un experimento exploratorio; la atribución causal a multihiperuniformidad permanece abierta.
