# Priors acumulativos nuevos — LARP AB30-TS (real, histórico, pronóstico)

Estos priors son incrementales y NO sustituyen los anteriores. No se asignan posteriors numéricas ficticias. Cada proposición especifica evidencia contraria, alcance y falsador.

**TS-P01 (diferenciación por proceso):** la historia reciente tiene valor desigual en procesos observados. B01 y B02 apoyan persistencia/ventana corta para CO2, log PIB e intereses, pero no establecen dominancia sobre ciclos. Contra: Nilo inconcluso, manchas solares y El Niño muestran heterogeneidad. Alcance: seis series históricas de statsmodels. Falsador: mismas predicciones en fuentes temporales externas y periodos posteriores.

**TS-P02 (periodicidad):** EWMA alpha=.3 mejora sobre media4 en Sunspots y El Niño, pero empeora CO2 y log PIB. Explicación por periodicidad NO identificada; faltan modelos estacionales ARIMA competentes y comparaciones con armónicos. Alcance: descriptivo. Falsador: controlar estacionalidad/ciclo y repetir con modelos competentes y cambios de periodo.

**TS-P03 (riesgo de extrapolación):** tendencia lineal sobre ocho instantes frecuentemente agrava error en procesos cíclicos (Sunspots, El Niño). Contra: log PIB y Nilo tienen puntos negativos/inconclusos; horizontes y escalas varían. Conocido en forecasting clásico. Falsador: diseño rolling multi-horizonte con tendencia calibrada antes de evaluar.

**TS-P04 (agregación de expertos):** ponderar por los últimos doce errores NO supera al experto fijo elegido solamente en desarrollo para estas fuentes y configuraciones. Contra: un ensemble adaptativo optimizado ex ante o con regularización adecuada puede mejorar; no generalizar. El baseline fijo es particularmente fuerte donde persiste buena predicción. Falsador: drift prospectivo de distribución frente a métodos Hedge/online aggregation bien calibrados.

**TS-P05 (validación y holdout):** comparar validación 50–75% con test cronológico 75–100% ofrece una comprobación interna más exigente que remuestrear semillas de un generador, pero los procesos siguen siendo los mismos y la inferencia HAC/moving-block es aproximada. Contra: series muy autocorreladas reducen N efectivo; no nuevo estudio independiente. Falsador: réplica temporal verdaderamente posterior al cierre o nuevos instrumentos.

**TS-P06 (metodología AB):** un flujo freeze–validate–branch–unseal-test obliga a preservar negativos y previene parte del peeking, pero NO demuestra que AB sea científicamente superior al diseño experimental convencional. Falsador: estudio de eficiencia AB vs expertos con misma información/recursos y resultados externos.