# LARP — Información, nulidad y error del decoder

2026-10-09. **COMPLETE: diagnóstico retrospectivo B02+B06.** Innovación demostrada: **1/3**. Se verifica álgebra conocida y se explica mejor evidencia histórica; no se obtiene una confirmación nueva de utilidad MHU ni una nueva regla de diseño.

## Qué se ejecutó

Nueve geometrías, dos asignaciones de marcas, dos bandas, dos niveles de ruido y tres estimadores históricos. Son180 matrices de canal/SVD,216 celdas de riesgo y72 celdas oracle; comparten geometrías, campos y queries. No son216réplicas independientes. Ningún campo, geometría o red nuevo; ningún optimizador, instalación o cambio de priors. Código y configuración separados de las series anteriores.

Tiempo numérico **0,5455343 s**; proceso frío completo **1,4241847 s**, incluyendo imports, comprobaciones y escritura. El supervisor impuso30 s y verificó PID/PPID reales de CPython, evitando el redirector de la venv de Windows. La presentación se produjo después, sin scores nuevos, en0,245533 s una vez cargada la biblioteca gráfica.

Se conservaron los resultados de software iniciales, incluido un fallo técnico de una aserción demasiado estricta sobre procesos: Windows adjunta un `conhost.exe` oculto al CPython real. El test fue corregido para distinguir ese auxiliar de un worker de Python y comprobar su terminación. El registro final pasa **20/20 tests** en0,87 s: diez controles algebraicos nuevos, uno de ownership/timeout y nueve oracle anteriores. Una revisión independiente de otro agente pasó además los casos de queries ponderadas y singular value bajo cutoff en TEMP. Ninguna de estas comprobaciones cuenta como evidencia MHU.

## Estimandos

Para observaciones `y=A theta+epsilon`, targets `Q theta` y mapa lineal `H`, la covarianza del ensemble histórico es `C_theta=I/M`, porque los2Mcoeficientes se distribuyen sobre una esfera de norma cuadrada2. No se sustituye por la covarianza empírica de128 mundos ni se interpreta como posterior gaussiano exacto.

`R = ||H A-Q||_F²/(M*m) + sigma²||H||_F²/m`.

Se proyecta el sesgo sobre subespacio observado y nulo de A usando su misma SVD/cutoff histórico. Con ruido positivo el ridge utiliza **todos** los singular values retornados; el cutoff sólo afecta diagnóstico de rango. Se reconstruye Gram real a partir de amplitudes de densidad en sumas/diferencias de modos. Máxima discrepancia **7,9048e-14**; máxima discrepancia de descomposición del riesgo **1,5613e-15**, dentro de tolerancias congeladas.

Estas identidades describen expectativas sobre el ensemble, no una réplica empírica. Las medias realizadas antiguas incluyen ruido y campos finitos comunes. No exigirles igualdad exacta.

## Resultado1: conteos raros fijan un suelo en este régimen

Smooth tiene12 coeficientes por canal y todos los diseños alcanzan rango 12. Fine tiene56; los rangos observados son56/56/56/50/34 para A/B/C/D/E. Las nulidades6/22 de D/E son reales en todos los diseños históricos y condiciones inspeccionadas.

Para el oracle lineal sin ruido, prior isotrópico independiente entre canales, macro con igual peso y **queries uniformes continuas**, el riesgo es:

`(6+22)/(5*56)=0.10`.

Todas las18asignaciones históricas dan ese mismo valor, salvo redondeo. Cambiar posiciones/marcas manteniendo esos rangos y conteos no elimina este suelo dentro de ese modelo. No es una cota universal para priors correlacionados, tareas distintas, conteos diferentes o decoders arbitrarios; no sustituir la evaluación de un decoder local por esta cifra.

## Resultado2: las queries antiguas tienen dos direcciones ciegas

La matriz Q de smooth tiene rango 12 y segundo momento `Q.T Q/m=I/2` hasta error numérico. Fine tiene **rango54 de56**. Sus autovalores del segundo momento son dos≈0, cincuenta y dos≈0,5 y dos≈1. Los modos axiales de frecuencia5 caen en Nyquist de la rejilla10×10 y sus componentes seno/coseno quedan aliadas.

Esto no cambia la dimensión56 del campo ni el rango de los sensores. Cambia qué direcciones y pesos mide la evaluación. El suelo oracle sin ruido en esas queries varía entre aproximadamente0,09936y0,10048según la asignación, frente a0,10 en evaluación continua uniforme. Es un efecto diagnosticable del estimando; no explica por sí solo la gran ventaja aviar del kernel local. Las queries continuas del suplemento Grid ya indicaban que esa ventaja local no desaparecía al cambiar la interfaz.

## Resultado3: el kernel pierde mucha información recuperable por el oracle

La tabla muestra **riesgo esperado**, banda fine, marcas nativas y sigma 0,1; medias descriptivas de tres geometrías, sin CI ni afirmación de mediación causal.

| Estructura/decoder | Sesgo nulo | Sesgo observado | Ruido | Total |
|---|---:|---:|---:|---:|
| Nominal, oracle | 0,099852 | 0,009354 | 0,022752 | 0,131957 |
| Aviar full, oracle | 0,100285 | 0,013410 | 0,023199 | 0,136894 |
| Aviar local, oracle | 0,099414 | 0,014596 | 0,023040 | 0,137050 |
| Nominal, kernel local | 0,099852 | 0,859179 | 0,004490 | 0,963521 |
| Aviar full, kernel local | 0,100285 | 0,495950 | 0,004290 | 0,600525 |
| Aviar local, kernel local | 0,099414 | 0,508901 | 0,004353 | 0,612669 |

El kernel aviar tiene aproximadamente0,50 de sesgo en direcciones que el sistema de sensores sí observa, frente a≈0,10 en direcciones no observadas. El oracle reduce ese sesgo observado a≈0,013–0,015y amplifica más ruido. Así, la pérdida del kernel no se puede explicar sólo por conteos raros o falta absoluta de observaciones.

Pero kernel y oracle aún difieren en alcance y conocimiento de banda/ruido. La descomposición no demuestra que una sola de esas diferencias cause el efecto. Precisamente por eso se necesita el siguiente factor limpio con regla común.

## Resultado4: diferencias diminutas full/local dependen del promedio evaluado

En fine, sigma 0,1, el banco histórico realizado tenía MSEoracle full 0,137279/local 0,136919. La expectativa del ensemble sobre esas mismas queries es full 0,136894/local 0,137050: la pequeña diferencia cambia de signo. No se reclasifican los resultados antiguos; se registra que una media finita de campos comunes no equivale al riesgo esperado del ensemble.

En queries continuas uniformes integradas analíticamente, los valores esperados son full 0,136536/local 0,137784. En ambos casos son diferencias pequeñas sobre un suelo≈0,10. Esto no demuestra superioridad full ni local, con sólo tres geometrías coadaptadas y sin contraste residual espectral identificado.

En smooth, sigma 0,1, full/local tienen riesgo esperado0,001972/0,001989. Shuffle aumenta el riesgo esperado de ambas familias en smooth y lo reduce en fine; esa inversión permanece en las expectativas, por lo que no procede únicamente de ruido realizado o de un mundo particular. Sigue siendo diagnóstico del paquete y del modelo conocido.

## Figura y fuentes

![Descomposición de riesgo esperado y medias finitas históricas](C:/Programación/LARP/artifacts/sampling_information/v1/risk_decomposition.png)

Las escalas verticales difieren entre paneles. Las barras son expectativas, los puntos medias del banco antiguo; no intervalos de confianza ni pruebas causales entre decoders. Los datos completos están en [results.json](artifacts/sampling_information/v1/results.json); identidad y protocolo en [protocol_freeze.json](artifacts/sampling_information/v1/protocol_freeze.json), supervisor en [runner_receipt.json](artifacts/sampling_information/v1/runner_receipt.json).

## Decisión para avanzar

Priorizar una misma regla LMMSE multicanal y factores separados:

- 24 observaciones locales seleccionadas por distancia frente a400 globales; sin fallback oculto ni24 sensores por canal.
- Modelo verdadero conocido frente a rho estimado en un banco offline común y separado del test; ambos conocen diccionario/ruido.
- Correlación cruzada0frente a0,8, con **igual espectro y varianza marginal esperada**. Usar campos gaussianos nuevos sin normalizar por realización.

La mezcla de un campo común suave y contrastes finos será un panel posterior, porque alterar su peso cambia correlación y espectro a la vez. La [ficha del próximo piloto](docs/projects/MULTICHANNEL_INFORMATION_PILOT_NEXT.md) fija observación, selección local, covarianzas, métricas y cierres; declara pendientes constructores, seeds, presupuesto ejecutable y margen práctico antes de cualquier dato confirmatorio. Su estado sigue **NOT_RUN**.

No buscar MHU3D/multicapa ni añadir entrenamiento recurrente en esta fase. El mejor siguiente conocimiento es si la organización puede predecirse y transferirse bajo restricciones, permitiendo que gane una estructura no MHU. Las identidades conocidas y la corrección del estimando merecen **1/3 de innovación**; el potencial2/3 exige pruebas nuevas y una regla que supere antecedentes como diseño información/comunicación y selección distribuida. [Registro de cuatro fuentes nuevas](docs/literature/MULTICHANNEL_INFORMATION_FOLLOWUP_2026_10_09.json).

## Actualización AB

- `belief_revision`: sin actualización numérica H1–H6/C; diagnóstico retrospectivo de un paquete conocido.
- `hypothesis_generation`: concretar separación nulidad/query/decoder y controles B03/B07; no tratar resultados antiguos como confirmación independiente.
- `objective_revision`: ninguna, continuar la cartera multicanal ya delegada.
- `decision`: cerrar este diagnóstico completo, preparar el piloto y conservar3D/composición como ramas sin ejecución.

El informe y código nuevos permanecen separados del Corner. La invitación a recreo no cambia umbrales, ratings, recursos ni clasificación científica.
