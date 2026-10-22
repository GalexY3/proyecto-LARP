# Gate de adquisición — multisitio Beijing UCI

Fecha 2026-10-22. Fuente identificada: [Beijing Multi-Site Air Quality (UCI, DOI:10.24432/C5RK5G)](https://archive.ics.uci.edu/dataset/501/beijing%2Bmulti%2Bsite%2Bair%2Bquality%2Bdata).

- 12 estaciones de Pekín, 6 contaminantes y meteorología asociada. 420,768 registros horarios (marzo 2013 – febrero 2017). CC BY 4.0 según UCI.
- Intentos de materialización: enlace ZIP de UCI rechazado por la interfaz de descarga; acceso HTTP directo al contenedor sin resolución de nombres; GitHub público con los CSV de gran tamaño no devuelve su contenido mediante el conector de texto. **No se obtuvo el conjunto original**: no calculamos ninguna métrica sobre él.
- No se obtuvieron coordenadas validadas de todas las estaciones. La selección discreta de estaciones puede plantearse sin geocoordenadas, pero las comparaciones MHU/Local SI geométricas requieren posiciones verificadas y una definición de distancia válida.
- No usar las dos tablas pequeñas `data.csv` y `test.csv` publicadas en UCI como si fueran las 12 series horarias canónicas.

## Próxima ejecución admisible (preprotocolo, NO realizada)

1. Descargar el ZIP **oficial**, registrar SHA-256, versiones y fechas, y conservar CSV crudos sin editar. Confirmar índices de fechas y estaciones en las doce fuentes.
2. Construir panel diario de seis contaminantes, con indicador de faltantes por estación y día. Calcular verdad de referencia solo para días que tengan observadas las 12 estaciones relevantes sin imputar el outcome del test.
3. Estimando primario: media de PM2.5 entre estaciones observadas, o un índice multivariante con normalizaciones físicas fijadas por entrenamiento. No confundir media sobre estaciones con media espacial ponderada de población ciudadana.
4. Separar temporalmente train (2013-2014), desarrollo (2015), holdout (2016 – febrero 2017); no ajustar transformaciones con test. Preferible una segunda ciudad/fuente con sensores comparables para validez externa.
5. Comparar, con idéntico coste de acción y lectura: azar, estratificado, greedy gaussiano para el **mismo estimador**, target-aware empírico, POWER_DIAG, COSI y, si se dispone de geocoordenadas y ejecutable validado, Local SI/MHU/Wei original.
6. Para objetivo global de media, evaluar ambos estimadores: media fija con pesos de importancia acordados y predictor lineal con entrenamiento idéntico (idealmente GP posterior regularizado). Registrar coste de construcción, de calibración, costo lectura, fallos y sensibilidad a cambios temporales.
7. Si la ganancia COSI desaparece tras igualar predicción y información, STOP a exclusividad COSI. No retocar los mismos años/ciudades de test hasta obtener significación.

**Gate:** `BARRERA_DATOS_FISICOS_MULTISITIO`: falta ejecutar la fase de adquisición. No se autoriza reinterpretar pruebas 2D como si cubrieran esa barrera.
