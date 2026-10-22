# Inicio de la pista de información multicanal

2026-10-09. Padre científico: `e2d882b`. AB2.1. Autorización en la conversación: «Okay. Deberíamos empezar a trabajar con esto?» después de recomendar adquisición multicanal y una exploración secundaria de composición. Se interpreta como empezar por el paso pequeño recomendado, sin solicitar otra confirmación para diagnóstico, ingeniería reversible o preparación de un protocolo.

## Alcance autorizado y decisión

Ejecutar B02+B06 sobre las nueve geometrías y dos asignaciones históricas. Máximo30 s numéricos CPU, cuatro hilos; lectura de entradas verificadas, ninguna geometría/campo nuevo, ningún entrenamiento, optimización o instalación. Tests y presentación tienen tiempos separados. La ejecución escribe exclusivamente `artifacts/sampling_information/v1/`; ningún archivo histórico se reescribe. El snapshot `historical_before.json` conserva972 archivos científicos/gobernanza previamente rastreados, excluyendo README, atributos y Corner.

La configuración se congela antes de los nuevos cálculos, SHA canónico `2cadcaccb58c764458bf6970ec5188d44da1bcf76cbe4fc8c30f3a3c462e18e2`. El código y todas las entradas quedan en `protocol_freeze.json`. La palabra freeze no convierte este diagnóstico de datos ya vistos en preregistro confirmatorio.

El supervisor `artifacts/sampling_information/run_supervised.py` impone además30 s al proceso frío completo —imports, verificaciones, cálculos y escritura—, una cota más conservadora que el presupuesto numérico. Un timeout interrumpe ese proceso sin repetir la serie; el tiempo de terminación puede añadir latencia de limpieza y se declara por separado. El hijo no crea procesos de trabajo persistentes.

## Preguntas y estimandos

1. Verificar la identidad entre Gram real Fourier y amplitudes de densidad en sumas y diferencias de modos. Los seis modos del descriptor geométrico no determinan esa matriz completa.
2. Calcular riesgo esperado verdadero de los tres estimadores históricos bajo la covarianza del ensemble `I/M`, separando sesgo en subespacio observado, sesgo en nulidad numérica y amplificación de ruido.
3. Separar nulidad del sistema de sensores de riesgo ponderado por las queries históricas. Registrar espectro/rango de `Q.T@Q/m`; evaluar analíticamente el riesgo oracle sobre queries uniformes continuas con segundo momento `I/2`, sin generar queries nuevas.
4. Cotejar expectativas con las medias finitas ya registradas; una discrepancia finita no es automáticamente bug ni evidencia nueva.

Denominadores:180 diseños de canal,72 celdas oracle y216 celdas totales con NN/kernel. Comparten9geometrías,128 mundos por banda y queries antiguas; no son216réplicas independientes. Fine tiene56 coeficientes; la pérdida mínima6/22 de los tipos D/E sólo da un riesgo sencillo bajo ponderación uniforme continua. No imponerlo a la rejilla antigua.

## Puertas y próximos pasos

Software: identidad Gram y descomposición de riesgo dentro de tolerancias declaradas; código nuevo probado contra covarianza independiente, caso de queries ciegas a la nulidad y caso Nyquist. Entradas ausentes/cambiadas o exceso de presupuesto producen fallo/omisión sin inferencia científica. No repetir para obtener resultados más favorables.

Preparar una ficha nueva para B03/B07 que iguale regla e información del decoder y varíe alcance. La mezcla «componente común suave+contrastes finos» se separa del factor puro de correlación: cambiar su mezcla cambia también el espectro marginal. La siguiente batería, sus constructores y campos nuevos no se ejecutan por esta decisión; deben quedar definidos antes de datos nuevos. Se conserva el límite conceptual de≤900s para la comparación de constructores del lote anterior y no se añade automáticamente a esta fase.

## Registro AB

- `belief_revision`: diagnóstico de un paquete ya conocido; sin cambio numérico de H1–H6/C ni nueva confirmación MHU.
- `hypothesis_generation`: concretar B02/B06 y distinguir conocimiento/alcance para B03/B07; ninguna hipótesis post hoc se confirma con estos datos.
- `objective_revision`: ninguna; continuar el pivote multicanal ya delegado.
- `decision`: diagnóstico pequeño ahora, especificación de piloto después; 3D, multicapa y composición neuronal permanecen sin ejecución.

La puntuación de innovación describe contribución demostrada, no la calidad de las herramientas ni la promesa. Esta fase algebraica puede ser útil manteniéndose en1/3. Corner es voluntario y separado, sin recompensa por modificar esa calificación.
