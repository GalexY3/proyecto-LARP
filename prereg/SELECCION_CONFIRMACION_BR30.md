# Selección confirmatoria BR30 — tras piloto, ANTES de ejecutar confirmación

**Fecha:** 2026-10-21. Selección declarada por comparación exploratoria previa. El piloto ha abierto todas las condiciones A01–F30; **no** son treinta pruebas confirmatorias independientes.

## ÚNICA afirmación confirmatoria
C11, frecuencia espacial f=1, tarea sintética y=f0*f1 + f2*f3 + .4*f0*f2*f4, interpolador gaussiano fijo ancho 0.11, 24 sensores más próximos, comparar MSE emparejado LOCAL vs un estratificado multiclase (cuotas originales, rejilla cúbica por tipo perturbada), además frente a RANDOM y MHU. Orientación preregistrada LOCAL < STRATIFIED; métrica diferencia (MSE_LOCAL − MSE_STRATIFIED) por mundo generado. N=20 mundos de 512 consultas cada uno, seeds 901..920, tests sobre media de diferencias por mundo, IC95 t bilateral, prueba unilateral descriptiva si procede. No decidir otros hiperparámetros en confirmación. Ajuste de multiplicidad: una única afirmación elegida tras piloto independiente; todas las demás confirmaciones A–F tendrán status exploratorio/diagnóstico.

## Datos del piloto que motivan elección (NO evidencia confirmatoria)
MSE LOCAL=0.133975; MHU=0.140211; RANDOM=0.355091; STRATIFIED=0.207771. En frecuencia 6 LOCAL≈2.106 y STRATIFIED≈2.149; dependencia de suavidad importante. Contraste sobre 10 mundos sintéticos y UNA geometría por construcción.

## Falsadores
Diferencia media confirmatoria LOCAL−STRATIFIED ≥0, IC incluyendo cero, o alta heterogeneidad con signo cambiante refutan/limitan la prioridad. Cualquier ventaja permanecerá restringida al mismo generador de funciones y geometría fija; no puede reivindicar superioridad en lenguaje, en arquitectura LARP ni novedad matemática.

## Control técnico
Huella del código congelado antes del piloto: 6ba3d7347c087bdf71c7de800312866c4f10dbf0f9da5ba26b499a33957284c5. La implementación se publicará, con su huella y semilla, en commits posteriores; deben conservarse esa distinción temporal y los datos negativos.
