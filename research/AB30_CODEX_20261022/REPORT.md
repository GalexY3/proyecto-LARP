# LARP: cierre de diez ciclos dinámicos, 22 de octubre de 2026

Se ejecutaron **10 de los 30 ciclos solicitados**. El usuario pidió finalizar por créditos; los veinte restantes quedan pendientes. Cada ciclo abrió su pregunta después del resultado anterior, con protocolo y fuente comprometidos en Git y publicados antes de ejecutar. Las condiciones, semillas y modelos dentro de un ciclo no cuentan como ciclos adicionales. Este bloque es exploratorio y no contiene confirmación externa.

**Dictamen:** estas pruebas no muestran una ventaja específica de MHU sobre controles convencionales. Identifican un confound fuerte de preprocesamiento y acotan una explicación arquitectónica: los frontends completos estudiados son transformaciones lineales que permiten representar el mismo clasificador de píxeles. Sigue siendo posible una diferencia de optimización o regularización; no se ha demostrado que favorezca a MHU.

## Qué cambió científicamente

1. La normalización por característica amplifica severamente variaciones de píxeles con varianza nula o pequeña. Corregir únicamente la condición de varianza cero **no recupera** la robustez: en C01, ruido pasa de 38,89% a 35,78%; la alternativa sin estandarización por característica obtiene 86,44%. C02 localiza la mayor energía residual en características con desviación positiva inferior a 0,05. Esa energía es un diagnóstico, no una prueba suficiente de causalidad sobre exactitud.
2. C03 encuentra un baseline convencional con centrado por característica y escala global que alcanza 92,44% bajo ruido. C06 separa ambos componentes: centrado y escala influyen, con interacciones. Por tanto, no atribuimos toda la recuperación a una corrección puntual de código ni solo a la escala.
3. Al igualar la política de normalización, C04 no muestra superioridad descriptiva clara de MHU. La mayor tolerancia a rotación de algunos frontends espaciales viene acompañada de pérdidas en otras condiciones. CVT y LOCAL ofrecen resultados comparables.
4. Una explicación sencilla por desenfoque queda debilitada: C07 no reproduce la tolerancia rotacional mediante blur gaussiano. C08 reproduce parte del efecto con RBF convencional, pero con costes en otras métricas. No se convierte una historia plausible en mecanismo establecido.
5. C09 conserva gran parte de la tolerancia rotacional al promediar los cinco bloques de tipos. En este pipeline, mantenerlos separados no es indispensable para ese efecto. El promedio pierde información y empeora otras métricas; no es una mejora general.
6. C05 establece la identidad lineal del encoder y C10 transporta exactamente el mismo clasificador a los frontends MHU/CVT completos. Esto descarta una ventaja de expresividad de esos frontends frente a ese clasificador en las condiciones algebraicas estudiadas. No descarta diferencias de entrenamiento, sensibilidad numérica o coste.

## Comparación principal del pipeline, C04

Exactitud porcentual. Frontends: media de cuatro geometrías y dos inicializaciones; píxeles: dos inicializaciones. Todos comparten datos, corrupciones y política de normalización. No son intervalos de confianza ni ocho muestras independientes de datos.

| Entrada | Limpio | Ruido | Oclusión | Rotación |
|---|---:|---:|---:|---:|
| Píxeles | 98,22 | 92,67 | 86,56 | 60,67 |
| LOCAL | 96,92 | 91,39 | 80,56 | 72,11 |
| MHU | 96,78 | 90,81 | 81,22 | 72,81 |
| CVT | 97,08 | 90,47 | 80,89 | 74,14 |
| Sobol | 96,25 | 90,86 | 80,64 | 69,47 |
| Aleatorio | 96,36 | 90,50 | 81,33 | 67,53 |

El baseline de píxeles ya supera descriptivamente el 98% limpio en este protocolo. Eso no repara ni valida retrospectivamente la tarea XOR, los experimentos tridimensionales u otros umbrales históricos. Tampoco convierte esta tabla en un ranking general de arquitecturas.

## Control de información y transporte

Para imágenes vectorizadas de dimensión 64 y representaciones de dimensión 80, el encoder es **F = X M**. C05 reproduce las representaciones con residuo máximo de 8,88e-16. Diecisiete de veinte operadores tienen rango completo 64; los cuatro MHU y cuatro CVT lo tienen. En rango completo, si la primera capa de píxeles es `x W + b`, una capa sobre `x M` puede usar `M⁺ W` y el mismo sesgo, incorporando también el cambio de centrado y escala. No aparece información independiente nueva.

C10 entrena un único clasificador de píxeles y transporta su primera capa, sin volver a entrenar ocho clasificadores sensoriales. Conserva 78 unidades ocultas: el modelo transportado tiene **7.108 parámetros**, frente a **5.860** del original de píxeles y **5.834** del frontend de 64 unidades de C04. Por tanto, es un control funcional de ancho fijo, no una prueba de equivalencia bajo el presupuesto aproximadamente igualado de C04. Entre las ocho geometrías y las cuatro condiciones de evaluación:

- Acuerdo mínimo de predicciones: **100%**, tanto en float64 como en float32.
- Error máximo de logits: **8,1464e-12** en float64 y **3,4235e-4** en float32.
- Algunas normas de pesos transportados superan 6.000. La equivalencia funcional puede tener un coste de condicionamiento; no garantiza igual estabilidad ni igual aprendizaje.

El protocolo y fuentes exactos de C10 están congelados en [42f2777](https://github.com/GalexY3/proyecto-LARP/commit/42f277770336575eabcdbdcc7cbd403163f4bd06). La afirmación numérica se limita a los ejemplos evaluados; la identidad algebraica requiere rango completo y aritmética exacta. Ninguna de las dos constituye evidencia de un LLM multilingüe sin pérdida.

**Precisión de alcance añadida al revisar el relay:** C10 compara explícitamente la inferencia de ambos modelos sin clipping; el helper histórico de entrenamiento sí aplica recorte ±9. La equivalencia con ese pipeline recortado requiere que el recorte esté inactivo en las entradas relevantes. No se deduce identidad global entre pipelines recortados a partir de esta prueba. La igualdad de clases funcionales del argumento algebraico se refiere a las redes afín/ReLU de igual ancho sin ese recorte.

## Contrato experimental y límites

- Datos: `load_digits`, 1.797 imágenes de 8×8, escaladas por 16; particiones estratificadas de 1.091/256/450, con semillas 811/812. El conjunto histórico y sus resultados están expuestos por uso adaptativo. El test no ofrece una confirmación nueva en cada ciclo.
- Corrupciones emparejadas: ruido gaussiano de sigma 0,17 con recorte, oclusión 2×2 y rotación aleatoria de ±12 grados; semilla 99128. Todos los métodos ven los mismos ejemplos dentro de cada condición.
- Geometrías: cuatro realizaciones de 128 puntos 3D, proyectadas a XY; cinco tipos con tamaños 52/27/22/16/11. Proyección y tarea 2D impiden inferir aquí utilidad computacional de una red 3D nativa. Se reutiliza la etiqueta MHU del artefacto de entrada; este bloque no certifica de nuevo multihiperuniformidad asintótica ni preservación espectral bajo proyección.
- Lectura: interpolación bilineal y RBF gaussianas normalizadas sobre una rejilla 4×4, sigma 0,16; concatenación de cinco bloques. Este encoder no es una red multicapa de message passing ni un transformer.
- Clasificadores MLP ReLU con aproximadamente 5.800 parámetros: 5.834 con 80 entradas, 5.860 con 64 y 5.842 con 16. Esto aproxima parámetros entrenables, no iguala ancho, FLOPs, acondicionamiento ni coste de generar geometrías.
- AdamW, learning rate 0,012, weight decay 0,001, máximo 240 pasos, selección por validación y paciencia 45. En C04, 13 de 42 selecciones caen en el límite de pasos: no se ha establecido convergencia equivalente.
- La medición de tiempo del worker no incluye todo el coste de investigación, instalación, generación histórica o publicación. No presentamos una ventaja de eficiencia total.
- C01–C05 conservan el estado histórico `RUN` del gestor inicial junto a resultados y tiempos; C06–C10 disponen de recibos `COMPLETED`, hashes y ejecución separada con límite de tiempo. No se reescriben los recibos antiguos. Dos intentos iniciales fallaron por dependencias antes de producir resultados científicos; constan en C01.
- No hay tamaño muestral suficiente, partición nueva ni diseño confirmatorio para asignar significación a diferencias pequeñas. Los priors históricos H1–H6 no se actualizan numéricamente con este bloque. La actualización es cualitativa y local a las explicaciones del pipeline.

## Decisión y continuación, si se retoma

**Cerrar esta sesión. No iniciar más barridos ni escalar MHU para intentar obtener una victoria.** Se conserva una rama de investigación sobre geometría, condicionamiento y robustez; MHU queda como una opción entre controles, sin preferencia demostrada.

La continuación útil sería congelar primero tres decisiones: una evaluación en datos no inspeccionados, un presupuesto que permita distinguir convergencia de condicionamiento y una tarea espacial nativa con controles locales/espectrales emparejados. La partición original UCI de 3.823 ejemplos es una oportunidad que no se ha descargado ni evaluado en este bloque: `load_digits` contiene únicamente los 1.797 ejemplos de test originales. Los grupos originales proceden de conjuntos diferentes de escritores. No se ha verificado disponibilidad de identificadores individuales ni independencia estadística dentro de cada grupo. Antes de usarla deben registrarse procedencia y exposición histórica del laboratorio. Fuentes primarias: [documentación de sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html) y [UCI Optical Recognition of Handwritten Digits](https://archive.ics.uci.edu/ml/datasets/Optical).

No calificamos este trabajo como innovación científica 2/3 o 3/3: su valor actual es metodológico y diagnóstico, no una arquitectura novedosa ni una ventaja establecida de MHU.

## Material conservado y metodología

- [Ledger de diez ciclos](LEDGER.md): preguntas, freeze SHA y decisiones A–J; resultados completos en cada directorio de ciclo.
- [Importación del laboratorio local](../../legacy/local_lab_20261022/README_IMPORT.md): 539 archivos originales, 25.845.075 bytes; hashes verificados, sin alterar el laboratorio original. No se suben entornos, checkpoints voluminosos ni materiales de terceros indiscriminadamente. El código importado se inspeccionó, pero no se ejecutó su batería histórica de tests en esta importación.
- [AB O2](https://github.com/GalexY3/Metodologia-AB/blob/57c306715a0003fd2605ebbb537a3b505a049e6c/docs/AB_3_2_1_O2_OPERACIONES_REPRODUCIBLES.md): salvaguardas operativas prospectivas, adoptadas con la autorización del investigador. Su eficacia sigue **NO_VALIDADA**; no se presenta como AB 3.3. El núcleo AB 3.2.1 y los priors históricos permanecen preservados.

La cuota de treinta ciclos no se rellena con condiciones o repeticiones: quedan veinte ciclos sin ejecutar. Cualquier nueva pregunta debe seleccionarse desde esta evidencia y recibir su propio protocolo antes de correr.
