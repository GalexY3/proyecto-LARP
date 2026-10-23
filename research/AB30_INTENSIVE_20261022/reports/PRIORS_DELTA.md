# LARP — Apéndice acumulativo de priors AB30I, 22-10-2026

Este registro no reemplaza ni elimina los priors históricos. Actualizaciones cualitativas; sin probabilidades inventadas. Todas las observaciones son exploratorias y sin replicación externa.

## P01. Cobertura por tipo
Proposición: optimizar cinco poblaciones mediante CVT aumenta la cobertura espacial. Procedencia: N01–N03; prereg B01 0a3b10d. Favorable: N01 delta -0.10734 vs iid en p95, N02 -0.02322 vs Sobol por tipo en distancia media. Contraria: retícula por tipo supera CVT en N03; la función objetivo ya favorece cobertura. Alcance: 100 puntos 2D, cinco tipos. Falsador: Multi-Class Blue Noise y optimización de cobertura con coste equivalente. Estado: APOYO_INTRAMODELO, novedad no establecida.

## P02. Espectro y dependencia de la tarea
Proposición: mejor potencia espectral media baja no implica mejor integración de cualquier función. Procedencia N04,N05 y N07–N11. Favorable: CVT domina ciertas métricas geométricas, pierde en integración frente a Sobol y retícula. Contraria: las métricas espectrales y frecuencias de las señales no tienen la misma ponderación, fenómeno conocido de cuadratura. Estado: evidencia computacional local, no 2/3. Falsador: generalización predicha antes de probar sobre funciones nuevas.

## P03. Reconstrucción local
Proposición: cobertura por clase reduce MSE en interpolación local con kernel gaussiano de bandwidth 0.095. Procedencia N13–N18 y auditorías AUD01–03. Favorable: seis resultados frente a Sobol, incluso pérdida de 30% de sensores y ruido; supera retícula en tres auditorías adicionales. Contraria: kernel elegido, periodicidad y distribución por tipo pueden producir el efecto; ninguna MHU certificada. Estado: apoyo local moderado, transporte externo desconocido. Falsador: procesos espaciales diferentes, tuning pareado y Wei/GP/Kriging bajo mismo presupuesto.

## P04. Clasificación
Proposición: red de sensores CVT por tipo supera alternativas en datos reales. Procedencia N19–N24. Favorable: N24 +0.03489 de BA frente a píxeles bajo desplazamiento. Contraria: N20 -0.00964 bajo condiciones originales; otros tests ambiguos; cinco vistas son derivadas de 64 píxeles. Estado: hipótesis general debilitada. Falsador: nuevo dataset ciego, misma representación y coste.

## P05. Grafos
Proposición: cobertura CVT mejora conectividad en kNN. Procedencia N25–N30. Favorable: gap superior frente iid N25. Contraria: Sobol mejor en N26, N27, N30; aristas no igualadas exactamente. Estado: no se confirma ventaja general. Falsador: presupuesto de aristas idéntico y GNN entrenada externamente.

## P06. Coordinación de fases entre tipos
Proposición: fases relativas modifican capacidad funcional adicional a regularidad de subtipos. Procedencia AB08 anterior, N06 y N12 nuevos. Favorable: efectos anteriores en banda seleccionada. Contraria: traslación independiente no perjudicó sistemáticamente en N06/N12; invariancia de espectros por tipo verificada. Estado: alcance estrechado, no refutación universal. Falsador: señales externas con control de espectros intraclase y baseline Wei.

## P07. Ventaja específica neuronal MHU
Proposición: MHU mejora aprendizaje computacional frente a controles competentes. Ningún resultado nuevo a favor de manera específicamente MHU; los generadores son CVT/Sobol/retículas y no se entrenó una GNN ni se certificó MHU. Estado: NO_VALIDADO, originalidad 2/3 NO_ACREDITADA. Validación discriminante: nuevos generadores MHU, Multi-Class Blue Noise de Wei, dato externo, costes igualados y holdout verdaderamente independiente.

Árbol de decisión: B01 cobertura -> B02 integración (fracasa) -> B03 reconstrucción (éxito condicionado) -> B04 Digits (mixto) -> B05 grafo (mixto) -> auditoría posterior de retícula. Los prior nuevos deben conservarse como apéndice, sin dar de baja silenciosamente los históricos.
