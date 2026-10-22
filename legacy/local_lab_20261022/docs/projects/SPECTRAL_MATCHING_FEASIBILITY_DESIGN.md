# Factibilidad de controles de concentración sobre X/E fijos

Fecha: 2026-10-08. Estado: **diseño prospectivo de factibilidad**, con un diagnóstico algebraico de las tres geometrías ya existentes. No se han construido controles en esta revisión, generado campos ni calculado rendimiento. La autorización humana de continuar el laboratorio permite preparar esta línea; sus reglas de admisión deben congelarse antes de la búsqueda. El documento padre es `docs/INDEPENDENT_SPECTRAL_MATCHING_NEXT.md`; sus tolerancias se conservan.

## 1. Qué queremos identificar

La intervención cambia asignaciones funcionales A–E sobre los mismos 400 puntos y arcos. Conserva conteos `[163,85,68,50,34]`, coordenadas y orden de nodos, radios físicos originales, distancias, grafo, puertos y espectro de la unión. Busca aumentar la media de los seis modos de **cada componente** hasta al menos 0,50, manteniendo las estadísticas locales fijadas en el protocolo padre. Por tanto, manipula concentraciones condicionadas al sustrato de unión; no manipula la hiperuniformidad de la unión, ni reproduce una retina donde función y tamaño celular sean inseparables.

El primer resultado útil es saber si encontramos controles admitidos con recursos modestos. No necesitamos rendimiento para responder eso. Un control admitido permite abrir después una comparación de adquisición; no demuestra por sí mismo utilidad de MHU. Un control no encontrado deja la atribución causal pendiente.

Las geometrías serán las tres referencias aviares completas g1101/g1102/g1103 ya fijadas. No escoger una después por facilidad de matching, apariencia o futura ventaja de adquisición. Su población de referencia es la del generador aviar con certificado finito; reutilizarlas sirve para factibilidad exploratoria y no aporta tres nuevas realizaciones independientes.

## 2. Existe una tensión matemática real, pero no una prueba de imposibilidad

Escribamos `V=L²=400`, `ρ_c(n)=Σ_{i:t_i=c} exp(2πi n·X_i/L)` y `S_c(n)=|ρ_c(n)|²/n_c`. Para la ventana disco de radio R y centro uniforme en el toro, definamos

\[
\bar w_R(n)=\frac{\pi R^2}{V}\frac{2J_1(2\pi |n|R/L)}{2\pi |n|R/L}.
\]

Parseval da, con todos los modos recíprocos distintos de cero,

\[
\operatorname{Var}_{z\sim U(V)}C_{c,R}(z)
=n_c\sum_{n\ne0}S_c(n)|\bar w_R(n)|^2.
\]

Los seis modos positivos usados en el protocolo tienen sus seis conjugados. Como todas las contribuciones son no negativas, imponer `mean(S_c en seis modos)≥0,50` exige

\[
\operatorname{Var} C_{c,R}\ge
2n_c\sum_{n\in\mathcal K_6}S_c(n)|\bar w_R(n)|^2
\ge 6n_c\min_{n\in\mathcal K_6}|\bar w_R(n)|^2.
\]

En R2,5 esta cota es aproximadamente `0,007530223776*n_c`; en R1,25 es `0,000772883238*n_c`. Esto significa que matching de ventanas locales y manipulación espectral no son necesariamente factores ortogonales. Igualar exactamente toda la distribución de conteos de una ventana, incluido su segundo momento, podría impedir ciertas manipulaciones.

La varianza nativa puede calcularse sin centros aleatorios y sin campos. Para R≤L/4, el área de intersección de dos discos a distancia mínima periódica d es

\[
A_R(d)=\begin{cases}
2R^2\arccos(d/(2R))-\frac d2\sqrt{4R^2-d^2}, & d<2R,\\
0,&d\ge2R.
\end{cases}
\]

Así,

\[
\operatorname{Var} C_{c,R}
=\frac{n_c\pi R^2}{V}
+\frac2V\sum_{i<j:t_i=t_j=c}A_R(D_{ij})
-\left(\frac{n_c\pi R^2}{V}\right)^2.
\]

Una recomputación de sólo lectura de las referencias produjo estos valores en R2,5:

| Tipo | n | Varianza nativa g1101 | g1102 | g1103 | Cota mínima de cualquier control espectral |
|---|---:|---:|---:|---:|---:|
| A | 163 | 0,830803 | 0,875142 | 0,850924 | 1,227426 |
| B | 85 | 0,595269 | 0,547461 | 0,584576 | 0,640069 |
| C | 68 | 0,424985 | 0,450122 | 0,450088 | 0,512055 |
| D | 50 | 0,476422 | 0,474751 | 0,483258 | 0,376511 |
| E | 34 | 0,397244 | 0,401857 | 0,385930 | 0,256028 |

En A, cualquier control admitido espectralmente debe aumentar la varianza toroidal de R2,5 al menos 0,352–0,397, aproximadamente 40–48% de la nativa. B y C también tienen una brecha positiva. En R1,25 las cotas están por debajo de todas las referencias. Estas cifras sugieren inspeccionar especialmente R2,5/A cuando falle la búsqueda.

**No certifican incompatibilidad con el protocolo.** La admisión empareja CDF empíricas con tolerancia 0,02 sobre 10.000 centros, no varianzas toroidales exactamente. Una pequeña cantidad de masa en las colas puede modificar segundos momentos. Además, optimizar sobre esos centros puede producir diferencias en centros no usados. Una cota calculada para la medida uniforme continua no se puede comparar como si la CDF empírica fuese esa misma medida. El histograma de pares se empareja sólo hasta 2,5, mientras que la varianza del disco R2,5 incluye pares hasta 5. No añadir ahora una puerta de varianza ni extender los bins: ambas cosas cambiarían la intervención.

Las cinco poblaciones están acopladas: `Σ_c ρ_c=ρ_union` y `Σ_c η_c=0`. No imponer objetivos de fase compleja independientes que violen esa identidad. Tampoco hay una incompatibilidad espectral pura evidente. Una asignación uniforme de un subconjunto de n_c puntos, sin matching local, cumple

\[
\mathbb E[S_c(n)]
=\frac{N-n_c}{N-1}
+\frac{n_c-1}{N-1}S_{union}(n).
\]

Con unión de bajo espectro, las bases esperadas son aproximadamente 0,594/0,789/0,832/0,877/0,917. El umbral 0,50 no es intrínsecamente imposible; conseguirlo **junto con** todos los matches es la cuestión. Esta identidad no garantiza que una realización concreta de shuffle supere los cinco umbrales, ni justifica usar shuffle como control admitido.

## 3. Búsqueda mínima recomendada

Congelar seis intentos: dos RNG distintos por referencia, siempre empezando de sus etiquetas nativas. No buscar primero en muchas geometrías y conservar sólo las fáciles. Un shuffle tiene una gran distancia inicial en separación homotípica y cobertura; gastaría gran parte del presupuesto reparando confounds. Puede usarse como diagnóstico descartado de calibración, nunca reemplazar los inicios fijados según lo observado.

Cada propuesta es un intercambio de dos etiquetas distintas; los conteos permanecen exactos. Elegir uniformemente uno de los diez pares de tipos, después un nodo i uniforme del primer tipo. Con probabilidad 0,8 elegir j uniformemente entre hasta cuatro nodos del segundo tipo más próximos a i; con probabilidad 0,2 elegirlo uniformemente entre todos los nodos de ese tipo. Resolver empates por índice. Actualizar las listas de pertenencia tras cada intercambio. Esta mezcla ofrece movimientos que perturban poco la geometría local y una minoría de movimientos amplios, dando oportunidades comparables a E y A. No permite permutar radios físicos con las funciones.

Para priorizar propuestas usar un objetivo geométrico fijo, sin campos, targets, MSE, logits o gradientes de tarea:

\[
J(t)=100\sum_j[(r_j(t)/\tau_j-1)_+]^2
+\sum_c[((0,50-\operatorname{mean}S_c(t))_+)/0,50]^2.
\]

Aquí r_j es **cada residual de admisión** y τ_j su tolerancia congelada. Los residuales de CDF y cuantiles son diferencias absolutas; el mínimo homotípico utiliza sólo el déficit unilateral `max(0,min_native−min_candidate)`, normalizado por `0,05*a_c`. Aplanar y registrar una sola vez la lista de features: cobertura CDF y tres cuantiles; dos ventanas con CDF/vacío; NN homotípico CDF/tres cuantiles/mínimo; todos los cinco bins de pares por tipo; todas las 25 celdas dirigidas; cinco outdegrees medios. No sumar puntos de CDF como miles de términos ni usar factores dependientes del tipo escogidos después.

Aplicar Metropolis de recocido con T descendiendo geométricamente de 0,10 a 0,001 durante el número de propuestas congelado del intento. Visitar un estado que viola matching forma parte de la búsqueda; **admitirlo está prohibido**. El objetivo no es un likelihood, Bayes factor ni resultado científico. Sus pesos afectan la eficacia del algoritmo de búsqueda y deben figurar como limitación si no se encuentra un control. No afirmar mezcla uniforme o muestreo de una distribución de controles: es optimización dirigida.

El criterio final no es `J≈0`: es el verificador exacto de todas las condiciones locales y espectrales. Elegir el primer control que pase. Guardar el mejor estado de cada intento fallido sólo como diagnóstico con sus violaciones completas; no llamarlo control, no evaluarlo en campos y no convertirlo retrospectivamente en un tratamiento de menor intensidad. Parar intentos posteriores de una referencia tras su primera admisión, conservando que no fueron ejecutados y sin transferir su presupuesto para favorecer otra.

## 4. Cachés y comprobaciones que abaratan sin cambiar el experimento

Por referencia, precalcular distancias periódicas N×N, matriz fase Φ de N×6, distancias 10.000×N de los centros comunes fijados, incidencia de las ventanas R1,25/R2,5, arcos y vecindarios incidentes. Mantener una referencia inmutable separada del estado candidato. Procesar referencias secuencialmente; no duplicar todos los grandes cachés en seis procesos.

Un swap entre tipos c/d sólo cambia ρ_c/ρ_d por `±(Φ_j−Φ_i)`. Sólo esas dos poblaciones necesitan recomputar métricas propias. Las distancias de cobertura se pueden actualizar al quitar/añadir un punto: si el quitado era el vecino mínimo, buscar su sustituto en un orden de sensores cacheado; después comparar con el añadido. Los conteos de ventanas cambian sumando/restando las dos columnas de incidencia. Los histogramas físicos de pares cambian con pares que contienen i/j, evitando duplicar el par entre ambos. La matriz dirigida necesita todos los arcos incidentes, cada arco una sola vez; las filas corresponden al tipo fuente y las columnas al tipo destino. No sustituirla por contactos simétricos ni por el histograma de pares.

Se puede implementar primero la recomputación completa de dos tipos: menor complejidad y auditoría más simple. Sólo introducir deltas más sofisticados si el coste medido impide una búsqueda informativa. Un proxy barato puede descartar propuestas, pero nunca admitirlas. La CDF de cobertura debe usar sus valores completos: una rejilla gruesa de distancias puede ocultar el máximo de diferencia.

Congelar convenciones numéricas antes de calibrar: distancias float64; CDF `P(d≤x)` evaluada en la unión de soportes; cuantiles con método `linear`; bins `[0,.5)`, `[.5,1)`, `[1,1.5)`, `[1.5,2)`, `[2,2.5]`; ventanas `d≤R`; NN sin diagonal. Los denominadores de tolerancias enteras son los conteos **nativos**, incluyendo sus celdas nulas. La referencia contra sí misma debe pasar con todos los residuales cero. Recomputar desde cero Φ/sumas de fase, counts, matches y hashes en toda posible admisión; no decidir por sumas incrementales con deriva numérica. Verificar después cada control con una implementación independiente antes de calcular utilidad.

## 5. Calibración y presupuesto antes de buscar

Recomendación inicial: **360 segundos globales**, incluyendo una calibración de hasta 60 segundos, cargas, cachés, intentos, certificados y escritura. Seis intentos con techo individual 50 segundos. El límite global domina los individuales; un intento que no empieza consta NOT_RUN. Usar supervisor externo que termine todo el árbol de procesos y preserve registros parciales.

La calibración utiliza entradas fijadas y propuestas descartadas, reseteadas desde la nativa; verifica costes de las métricas completas tanto en cambios próximos como amplios. Registrar versiones, threads, segundos de import/caché, tiempo máximo por propuesta completa y por certificado, RSS y hashes. No elegir después geometrías, tolerancias, objetivos o propuestas según su facilidad. Se permite usar medición de coste para fijar el número de propuestas antes de la búsqueda, no para seleccionar tratamientos por futuros resultados.

Fijar el cap como el mínimo de 5.000 propuestas y lo que cabe en 50 segundos usando **dos veces el máximo coste por propuesta medido**, reservando tiempo para un certificado completo y escritura. Publicar la fórmula y el cap resuelto. Si esa calibración no permite aproximadamente 500 propuestas por intento, decidir **antes de congelar la búsqueda** si merece ampliar el global a un máximo de 600 segundos y ajustar los techos. No ampliar tras observar fallos. El mínimo de 500 es una regla de eficiencia, no potencia estadística ni garantía de factibilidad; si no cabe una búsqueda informativa, detenerla por recursos.

No se necesita agotar el presupuesto: las admisiones tempranas ahorran tiempo. La calibración no produce controles utilizables y no se recicla como evidencia de éxito de búsqueda. Tampoco debe ejecutar el decodificador, cargar el banco de campos anterior ni producir una MSE siquiera «para comprobar».

## 6. Interpretación, stop y alternativas

Registrar separadamente: software/verificador válido, referencia elegible, búsqueda completa o limitada, manipulación espectral, matching local y admisión por referencia. Una condición espectral lograda con mismatch, o matches logrados con espectro todavía bajo, es `NO_ADMITTED_CONTROL`; no es un resultado de adquisición. Un error de métricas es BUG/INVALID, un corte del supervisor RESOURCE_LIMIT, y agotamiento válido de las propuestas es SEARCH_EXHAUSTED/NOT_IDENTIFIED. Ninguno refuta utilidad de MHU.

Si hay tres controles admitidos y auditados, congelar **un nuevo** protocolo de campos/queries antes de evaluar: señales dentro/fuera de la banda manipulada, ruido común, decodificadores locales y oracle-band fuerte. Esas decisiones no se implementan implícitamente en la fase de factibilidad. El número de réplicas son tres sustratos, no cinco tipos, diez mil centros, seis modos ni mundos. No actualizar H1–H6/C automáticamente.

Si no hay admisiones, cerrar esta búsqueda limitada y conservar sus residuales. La siguiente acción informativa es caracterizar por qué: por ejemplo, frente local/spectral, tensión de ventanas o conectividad del espacio de swaps. Una prueba de imposibilidad necesitaría una cota válida para **todos** los etiquetados permitidos o una solución global certificada, no ausencia de éxitos en seis recocidos. Alternativas futuras: ciclos de tres tipos; restricciones locales exactas preservadas por movimientos de bloque; optimización combinatoria/MILP de una relajación para producir cotas; o un protocolo diferente que declare otra intensidad espectral u otro conjunto de características. Cada alternativa requiere una versión nueva y no rescata el contraste actual.

Incluso con controles admitidos, matching no equivale a identidad de todos los vecindarios. Anisotropía, correlaciones por encima de 2,5, espectros fuera de banda y residuales dentro de tolerancias pueden cambiar. Registrar esos cambios descriptivamente sin seleccionar por MSE. Una ventaja diminuta comparable a residuales locales no autoriza atribución exclusiva a ondas largas. Los centros de matching son datos de construcción; queries nuevas permiten evaluar cuánto generaliza la equivalencia local, sin descartar a posteriori controles que resulten incómodos.

## 7. Procedencia del cálculo de varianza

Entradas de sólo lectura: `artifacts/avian_v1/avian_full_spectral_N400_g1101.npz` SHA256 `427e9e7ddfb7cbfeea6d53a5ffd25465f90c788f5ce2cfaa41a421a95bb29680`; g1102 `009acff5a4b0fd5baecf2817b9bd4cdf9b9bcda900b9d603c79f2413c6b7485f`; g1103 `de129159097d2e1307c1167e4b2c9d0111fcdac57f6217dd8c57331ab1a203b5`. Cálculo con NumPy/SciPy ya instalados: distancia mínima periódica, selección de pares i<j dentro de cada tipo, suma de áreas de intersección anterior; seis vectores `[1,0],[0,1],[1,1],[1,-1],[2,0],[0,2]` y función J1 para la cota. No se escribieron las entradas, generaron etiquetas ni utilizaron campos. Las identidades y recomendaciones de esta ficha son derivación y juicio propios, no evidencia publicada de una ventaja MHU. La revisión de literatura principal queda separada.
