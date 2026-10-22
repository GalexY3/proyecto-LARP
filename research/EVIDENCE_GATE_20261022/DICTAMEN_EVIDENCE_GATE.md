# LARP · Dictamen de la nueva campaña de valor (22 de octubre de 2026)

**Veredicto:** el mecanismo COSI no ha demostrado ventaja general sobre algoritmos competentes de diseño de sensores; conserva **una ventaja exploratoria delimitada** con predictor Ridge sobre cuatro imágenes reales diferentes y tres observables *derivados* de cada imagen. El objetivo inicial de corroboración sobre redes físicas multisitio **no se ejecutó** por bloqueo material de los datos. **AB-DECIDE = STOP condicionado, con prerrequisitos para FOCUS**; no consumir ciclos adicionales del mismo generador para justificar originalidad.

## 1. Objetivo y evidencia recuperada

Antes de esta campaña, LARP ya había consumido las imágenes RGB astronaut, coffee, chelsea, immunohistochemistry, rocket, hubble y retina de scikit-image en diferentes condiciones, y contrastes temporales NOAA Niño 1+2. Los resultados favorables a COSI eran sensibles al tipo de readout; el valor incremental de la covarianza cruzada respecto a la potencia espectral por canal seguía débil. El nuevo experimento NO reutiliza ninguna de estas escenas como prueba.

Se buscó el dataset genuinamente físico y multisitio **Beijing Multi-Site Air Quality** de UCI (12 estaciones, marzo 2013-febrero 2017, seis contaminantes). Se verificó la existencia y licencia, pero no se recuperó el ZIP original, ni coordenadas validadas para todas las estaciones. Se detuvo esa rama sin fabricar datos; `SOURCE_ACQUISITION_GATE.md` conserva el protocolo futuro.

## 2. Contraste sustituto: múltiples escenas físicas, canales derivados

**Origen:** imágenes monocromas distribuidas con `scikit-image`: cámara, Luna, hierba, grava, ladrillos, células y microaneurismas. **Train**: camera y moon (160 recortes 24x24 por escena); **desarrollo**: grass (160 recortes); **holdout nuevo**: gravel, brick, cell, microaneurysms (160 recortes por escena). Tres tipos de «lectura» calculados del mismo campo original: intensidad, desenfoque gaussiano σ=1.3 y módulo de Sobel/4. Aunque proceden de señales visuales observadas, **son operadores deterministas, no tres magnitudes físicas medidas por sensores independientes**.

**Estimando:** media ponderada completa por parche de los tres canales, con pesos [0.5, 0.2, 0.3] fijados antes de abrir prueba. Presupuesto: exactamente 16 lecturas, cuotas [4,8,4]. Cinco algoritmos: Sobol, optimizador directo por RMSE piloto de media fija, greedy de covarianza-target GP-like (NO un GP de Krause), POWER_DIAG y COSI-SHRINK. Se evalúa cada diseño con **ambos** readouts: media fija y Ridge con α=.02 entrenado en idénticos parches piloto.

Se ejecutaron seis condiciones planeadas antes de abrir las escenas de prueba: pilotos 16,16,32,32,96,96, semillas 4001–4006. La elección de qué evaluar ya estaba en el script; son **seis condiciones**, no branching adaptativo genuino. Se escribió el fichero de diseños `HOLDOUT_FREEZE.json` y SHA256 `c686157283f0d617cf05b55d02e69ee2e481b945045fbfadc2371d57b8185a22` **antes de cargar** las imágenes de prueba en el programa. Se abrió el holdout **una vez**.

## 3. Resultado externo único, macro entre cuatro escenas

Cada cifra es el promedio no ponderado de cuatro RMSE por escena; dentro de cada escena promedia seis diseños; esas semillas **no** equivalen a nuevos dominios ni a una distribución de cuatro escenas elegidas aleatoriamente.

| Diseño | Media fija, RMSE | Ridge, RMSE |
|---|---:|---:|
| SOBOL | 0.016818 | 0.014061 |
| DIRECT | 0.018167 | 0.015558 |
| GP aproximado | 0.020009 | 0.017522 |
| POWER_DIAG | **0.016716** | 0.013268 |
| COSI-SHRINK | 0.016821 | **0.012409** |

Para Ridge, COSI muestra RMSE medio un **6.47% inferior** a POWER_DIAG, su ablación estructural más cercana. Las medias Ridge por escena fueron:

| Escena | POWER_DIAG | COSI |
|---|---:|---:|
| grava | 0.028113 | 0.026434 |
| ladrillo | 0.015753 | 0.015446 |
| célula | 0.003626 | 0.003315 |
| microaneurismas | 0.005581 | 0.004442 |

En cambio, la media fija no acredita mejora COSI sobre POWER_DIAG (0.016821 frente a 0.016716), ni siquiera sobre Sobol (0.016818). Esto obliga a diferenciar **beneficio condicionado por el estimador** de la supuesta superioridad geométrica universal. La evidencia es de transferencia descriptiva a cuatro fuentes visuales nuevas, no a cuatro redes físicas multivariantes. No aplicar bootstrap a cientos de recortes tratando cada recorte como escenario independiente. La incertidumbre entre dominios es considerable con n=4.

## 4. Auditoría adversarial después de prueba (NO nueva confirmación)

El código heredado `gp_greedy` aceptaba `candidates=144`, pero usaba `Sobol.random_base2(7)[:candidates]`, limitando el conjunto inicial a 128 puntos por rol, y menos después de quitar duplicados. La etiqueta nominal era engañosa. Para corregir la desigualdad, `repair_gp.py` comparó un selector GP-like con **los 576 píxeles** permitidos para cada rol. Resultado post hoc, promedio de cuatro escenas: RMSE media fija 0.022993, Ridge 0.019287. Sigue siendo peor que COSI en este benchmark, pero se trata de una selección avariciosa con shrinkage prefijado y sin una búsqueda adversarial amplia del modelo de covarianza. **No es demostración de superioridad frente a los procesos gaussianos del estado del arte**.

Se detectó una discrepancia numérica de ~1.08e-6 en un test de integración exacta a grilla completa por acumulación de float32; se corrigió la tolerancia del test a 2e-6 sin modificar el algoritmo ni los resultados congelados. Los seis tests ahora pasan; registrar como reparación instrumental, no experimento nuevo.

## 5. Teoría y antecedentes

Para una variable objetivo escalar Y y lecturas X_S de media y covarianza dadas, el estimador lineal de mínima varianza cuadrática tiene riesgo poblacional

`Var(Y) - Cov(Y,X_S) [Cov(X_S,X_S)+R]^{-1} Cov(X_S,Y)`

para un ruido de medición de covarianza R y supuestos lineales/segundo orden. Este riesgo depende del **estimador**, no solo del patrón. Una variante espectral optimizada para el promedio fijo no tiene por qué minimizar el riesgo del predictor entrenado. Es una formalización conocida por condicionamiento de covarianzas, no un nuevo teorema.

Antecedentes: Krause, Singh & Guestrin (2008), JMLR v9, colocación de sensores GP por información; Wei (2010), SIGGRAPH, multi-class blue noise; Chen, Ji y Saibaba (2026), arXiv 2601.20781, métodos CSSP para diseño GP. Ninguno ha sido reproducido y afinado a igualdad de condiciones contra COSI en este paquete.

## 6. Dictamen multidimensional AB

- **Validez interna del test reproducible:** limitada pero informativa: reparto fijo entre escenas, pruebas invariantes y readouts pareados, código íntegro y SHA. No hay preregistro remoto previo; la secuencia freeze-before-load de la misma ejecución es auditable, pero no equivale a preregistro externo blindado.
- **Información nueva:** cuatro imágenes nunca expuestas al diseño en la campaña, no nuevas observaciones de canales ambientales físicos. Correlación entre recortes dentro de imagen.
- **Atribución causal:** no demostrada, pues la modificación geométrica cambia múltiples propiedades y Ridge interactúa con ellas. Diferencia POWER_DIAG vs COSI en condiciones controladas es indicio, no mediación identificada.
- **Generalización:** a 4 dominios visuales locales sí; a sensores heterogéneos reales, climas, acuíferos o LLM, NO medida.
- **Originalidad:** 1/3; objetivo formal de discrepancia con covarianzas forma parte del prior art de kernels; no 2/3 ni 3/3.
- **Próximo bloqueo verdadero:** acceso a serie multisitio nativa de varios canales, coordenadas y comparadores GP/kernel quadrature expertos con readout pareado, coste y prueba temporal auténtica.

## 7. Valor práctico y decisión

**[Inferencia]** La oportunidad defendible de LARP no es vender una arquitectura neuronal que derrota el estado del arte. Se puede desarrollar un *motor de selección de acciones de medida* para presupuesto reducido y experiencia piloto escasa, con cambio explícito entre geometrías según la tarea. El producto solo tendría valor cuantificable si reduce costo real de adquisición para un error tolerable frente al mejor método convencional.

**STOP** de pruebas reiteradas sobre estas siete escenas. **FOCUS** cuando exista el dataset UCI materializado y un holdout físico no utilizado. Si el baseline gaussiano o un estimador directo selecciona mejor bajo mismas condiciones, adoptar la solución convencional; descartar exclusividad COSI sin intentar rescatarla mediante nuevos nombres.

**No se necesitan más ciclos de la misma clase de evidencia.** La autorización de ciclos adicionales no obliga a gastarlos; el siguiente avance depende de nuevos datos y de implementación comparable, no de lanzar más semillas artificiales.
