# Próxima prueba: organización multicanal, información y alcance

2026-10-09. Estado: **SPECIFICATION_DRAFT / NOT_RUN**. Procede de B03+B04+B07 y del diagnóstico B02/B06; no sustituye protocolos históricos. El usuario autorizó empezar la línea; en este turno se ejecuta únicamente el diagnóstico pequeño registrado en ADR_INFORMATION_DIAGNOSTIC. Esta ficha fija decisiones científicas del piloto y declara las puertas todavía pendientes. No es un contrato confirmatorio ni autoriza por su existencia nuevas corridas.

## Pregunta y contribución posible

¿El beneficio de una organización de tipos cambia al limitar las observaciones disponibles, manteniendo la regla de estimación y el conocimiento del modelo iguales? ¿Una correlación cruzada definida cambia ese efecto sin alterar el espectro marginal?

La ventaja local/oracle histórica cambió simultáneamente algoritmo, alcance e información. La nueva comparación debe separar esos factores. Predecir un ranking a partir del riesgo verdadero del mismo modelo verifica álgebra conocida. Un potencial2/3 requiere una regla de organización barata y transferible, frente a rivales competentes y en casos nuevos retenidos. No atribuir3/3 a una interacción estadística ni a aumentar dimensiones/capas.

## Decisiones fijas del estimador

- Dominio periódico2D, L20, N400 y conteos163/85/68/50/34. Cada sensor i observa exclusivamente el canal de su marca: `y_i=f_c_i(x_i)+0.1*epsilon_i`. Ruido IID por mundo/node ID, común entre condiciones comparables; no valores ocultos de otros canales.
- Alcance **LOCAL_K24**:24 nodos más próximos a cada query por distancia periódica, desempate por node ID. Selección independiente de marcas, valores y resultados; el mismo conjunto produce los cinco outputs. No son24 sensores por canal. Registrar cobertura por tipo, radio al nodo24 y observaciones utilizadas. Si falta un tipo, no hacer fallback global.
- Alcance **GLOBAL**:400 observaciones. Es un factor de acceso a datos, no una medición de message passing en un grafo. La selección espacial tiene coste y no representa disponibilidad gratuita en hardware distribuido.
- Regla común: LMMSE multicanal `W=K_qo (K_oo+0.01 I)^(-1)`. Usar solves Cholesky, sin inversa explícita; el ruido positivo hace SPD la covarianza observable. La implementación primal/dual puede reducir coste pero debe producir el mismo mapa. No introducir NN, embeddings de ID, HPO por geometría o regularización elegida mirando test.
- Factor de conocimiento **KNOWN_MODEL** frente a **TRAIN_ESTIMATED_MODEL**. Ambos conocen diccionario Fourier, sigma y familia de covarianzas. Sólo difiere conocimiento de rho. La condición estimada utiliza una estimación global única por banco de entrenamiento, compartida por todas las geometrías; no estima un modelo por estructura ni consulta test.

## Factor puro de correlación y campos

Primera prueba: mismas dos bandas marginales que el diagnóstico —smooth radios1–2 y fine3–5—, y `C_rho=(1-rho)I5+rho11^T`, rho 0/.8. Para cada componente real cos/sin y modo, theta tiene covarianza `C_rho/M`; componentes, modos y mundos independientes. La varianza marginal esperada de cada campo es1, idéntica al variar rho.

**Cambiar a campos gaussianos nuevos**, declarando la diferencia respecto al banco histórico esférico. No renormalizar cada mundo/canal. Eso cambiaría covarianzas, correlaciones y ruido relativo. Guardar la varianza analítica realizada como diagnóstico sin modificar scores o sigma.

Entrenamiento recomendado:64 mundos nuevos, mapas completos de los cinco canales sobre una rejilla16×16 común, ruido IID sigma 0.1 y banda conocida. Esta información offline es privilegiada pero explícita, común para todos los diseños; no equivale a inferir el prior con sólo los sensores desplegados. Recuperar coeficientes con LS en esa rejilla, que admite ambos diccionarios sin el aliasing Nyquist antiguo. Estimar rho a partir del promedio de covarianzas cruzadas de componentes, con escala M conocida, restando la contribución de ruido cuando corresponda; ruido entre canales independiente implica contribución cruzada esperada cero. Fijar estimador sin centrar usando medias test y clipping a[0,.95]. No ajustar por score. La construcción deberá registrar covarianza real del ruido de LS y comprobar el estimador en simulación técnica antes de usarlo.

Test recomendado:128 mundos independientes del entrenamiento y del diseño de geometrías; queries continuas nuevas comunes, fuera de la rejilla histórica. Bancos RNG separados por design/train/test/query/noise y mundos comunes entre estructuras. Los seeds/namespace concretos y el número de queries deben congelarse con los constructores antes de generar datos. Este último requisito pendiente impide llamar a esta ficha preregistro listo.

La mezcla `sqrt(rho)*g_smooth+sqrt(1-rho)*h_c_fine` queda para otro panel: variar rho cambia también el espectro marginal. No presentarla como intervención pura sobre correlación. La hipótesis de cancelación local de componente suave se prueba sólo después de separar esa interacción.

## Riesgo y métricas

Para el mapa W formado con un modelo estimado, evaluar riesgo con las covarianzas GENERADORAS:

`R_error=K_qq-W K_oq-K_qo W^T+W(K_oo+0.01 I)W^T`.

La varianza posterior calculada con el modelo estimado no es su riesgo verdadero. Endpoints: MSE macro de cinco canales equiponderados, MSE por canal, riesgo analítico esperado y contraste `(f_D-f_E)/sqrt(2)`. Su varianza esperada es1-rho; informar MSE absoluto y MSE dividido por ese denominador. No usar varianza realizada del banco test como normalización adaptativa.

El contraste principal es interacción de diseño con alcance, calculada dentro de cada condición de información y rho; no agrupar todos los mundos como réplicas geométricas. No afirmar que menor riesgo es causado por supresión espectral a partir de una regresión de descriptores correlacionados.

Costes separados: construir estructura, ajustar prior, formar factores/mapas, inferencia por mundo, número de observaciones, MAC aproximados, memoria y tiempo frío/amortizado. Comparar fronteras de utilidad/coste; GLOBAL posee más observaciones y no es una comparación de cómputo igualado.

## Puertas pendientes para ejecución

1. Cerrar diagnóstico B02/B06 y auditar fuentes/hashes. Si faltan inputs o falla álgebra, reparar una nueva versión sin reinterpretar el fallo como resultado MHU.
2. Implementar y probar un decoder común, incluyendo rho 0que impide dependencia entre canales, ausencia local de un tipo sin fallback, entrenamiento/test separados y riesgo verdadero de modelo incorrecto.
3. Fijar alcance del piloto. Una evaluación con geometrías históricas puede calibrar factibilidad y detectar contrastes, pero sigue siendo exploratoria; no crear por renombrado24réplicas.
4. Para comparación nueva: definir exactamente tres constructores con inicializaciones comunes, presupuesto y tratamiento de fallos; familia local fuerte, misma familia con término MHU y una variante con objetivo de riesgo. Conservar la propuesta≤900s, tres familias×ocho inicializaciones, sin más intentos tras observar resultados. Variables, objetivo de riesgo, pesos/escalas, parada y seeds están **pendientes**; el implementador no debe improvisarlos durante evaluación.
5. Congelar predicciones de ranking/transferencia, unidad de réplica y margen práctico antes de datos nuevos. Ocho geometrías no garantizan precisión. Resultado nulo impreciso termina como INCONCLUSIVE, sin ampliación automática para conseguir2/3.

Continuar si aparece un contraste práctico reproducible y una explicación que sobreviva a rivales locales fuertes y a test nuevos. Pivotar si el rival sencillo reproduce la utilidad o si el cambio sigue sólo disponibilidad de tipos. Cerrar la pretensión de novedad si la regla sólo explica casos usados para formularla, exige rediseñar cada test o reproduce sin aportación el diseño óptimo conocido.

## Literatura y delimitación

Los antecedentes ya incluyen diseño espectral, multiclase blue noise y selección de sensores condicionada a información/comunicación. Se añaden fuentes prospectivas en `docs/literature/MULTICHANNEL_INFORMATION_FOLLOWUP_2026_10_09.json`; no se modifica el lote anterior congelado. Ningún resultado de esta ficha se ha obtenido. Los priors históricos H1–H6/C permanecen intactos.
