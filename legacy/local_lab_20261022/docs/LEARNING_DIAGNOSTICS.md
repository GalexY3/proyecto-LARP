# Diagnóstico de aprendizaje, serie técnica v1

Protocolo congelado antes de resultados, 2026-10-08. El objetivo es localizar el fallo de XOR remoto sin cambiar LARP v0.1, su umbral .98, sus datasets ni sus checkpoints. Estado inicial: NOT_RUN. Esta serie no produce evidencia de superioridad MHU ni actualiza H1–H6.

Orden y puerta previa: MLP 2→32→1 SiLU centralizado, seeds 2101/2102, los cuatro patrones como batch4; después el bloque G original sobre Grid/MHU N400 g1101, mismos seeds y ambos bits inyectados en slots1/2 del receptor lógico0. G mantiene T16 y la interfaz original de coordenadas; source/query IDs son cero y sólo el receptor tiene mask1. Cada corrida dispone de250 updates AdamW lr.003, betas .9/.999, eps1e-8, weight decay1e-4 y clip1. Sólo el estado final cuenta. Los cuatro patrones deben acertarse y todas las cifras/ponderaciones deben ser finitas para aprobar. Un fallo o resultado mixto cierra la siguiente puerta, sin retries, sweep, test ni extensión de presupuesto.

Sólo si todos los controles anteriores pasan se compara local separado frente a remoto: 16 destinos lógicos comunes y dos fuentes distintas, locales a1–2 hops dirigidos en **ambos** sustratos o remotas a≥5 unidades físicas en ambos. Se enumeran candidatos; se seleccionan16 destinos por SeedSequence(20261008,9912), roles por clave9913 y minibatches por(20261008,training_seed,9914). Se usan12 triples train y4 validation, cada uno con los cuatro patrones, con iguales destinos/inicialización/budget. Si el pool no tiene16 destinos admisibles, DIAGNOSTIC_UNAVAILABLE, sin ampliar hops.

Techo completo300 segundos en CPU4 threads, incluyendo preparación y medidas. Una corrida que agota techo conserva estado parcial como RESOURCE_LIMIT y las pendientes quedan NOT_RUN. Se guardan hashes explícitos del módulo diagnóstico, model.py, data.py, graphs.py, geometry.py, artifacts.py, config y runtime; la identidad no depende de src concurrentemente mutable. El manifest y su manuscrito quedan en artifacts/learning_diagnostics/v1 antes de crear el primer optimizer. Se conservan loss/accuracy, curvas de loss y norma de gradiente, logits, gradientes respecto de ambos bits y flips para todos los casos. No hay selección de checkpoint favorable.

Interpretación previa: si falla MLP, diagnosticar loss/interfaz/optimización; si MLP aprende y G local falla, examinar norma/saturación/gradientes del bloque antes de proponer una modificación versionada. Si G local aprende y sólo remoto falla, priorizar transporte efectivo. Un éxito pequeño no abre el smoke científico. GRU, T32 y generador aviar permanecen intervenciones futuras separadas.

Comando reproducible: `.venv\Scripts\python.exe -m larp.learning_diagnostics`. El directorio de evidencia se crea exclusivamente; una ejecución repetida contra la misma ruta se rechaza.

Pruebas de software previas: cuatro tests verifican la separación real de bits, masks/IDs, preservación de labels XOR y que un pool imposible o una corrida parcial no pueda abrir la puerta. Resultado: 4 passed en3.14s. Las pruebas no demuestran capacidad de aprendizaje.

## Resultado observado

Tanda única completada sin retries en **112.576 s**, con14 corridas y3500 updates totales. RSS máximo muestreado460,914,688 bytes (439.56MiB). Se mantuvo la identidad congelada `78de730c0f319f96a25f09290fd90d9c3ba8dba66196ddc011400c4ed262c851`. El pool exacto tiene84 destinos admisibles; no se amplió el rango1–2hops. Los grafos/puertos coinciden byte por byte con los anteriores entrenamientos smoke. Los resultados completos y cada patrón/flip constan en `artifacts/learning_diagnostics/v1/results.json`; los estados finales y curvas se conservan en subdirectorios. Todos los valores/ponderaciones finales son finitos.

| Control | Seed | Accuracy final | BCE final | Mediana \|∂logit/∂bit\| | Fracción flips que cambian clase |
|---|---:|---:|---:|---:|---:|
| MLP centralizado |2101|1.00|.038097|5.649|1.00|
| MLP centralizado |2102|1.00|.033948|6.055|1.00|
| Bits en receptor, Grid |2101|1.00|1.02e−6|9.801|1.00|
| Bits en receptor, Grid |2102|1.00|2.49e−6|3.723|1.00|
| Bits en receptor, MHU |2101|1.00|1.24e−6|11.231|1.00|
| Bits en receptor, MHU |2102|1.00|2.56e−6|2.910|1.00|
| Interfaces separadas locales, Grid |2101|.50|.693355|4.43e−5|0|
| Interfaces separadas locales, Grid |2102|.50|.693206|2.77e−4|0|
| Interfaces separadas locales, MHU |2101|.50|.693480|5.92e−5|0|
| Interfaces separadas locales, MHU |2102|.50|.693169|2.05e−4|0|
| Interfaces separadas remotas, Grid |2101|.50|.693298|1.41e−12|0|
| Interfaces separadas remotas, Grid |2102|.50|.693185|1.53e−12|0|
| Interfaces separadas remotas, MHU |2101|.50|.693427|8.05e−16|0|
| Interfaces separadas remotas, MHU |2102|.50|.693179|9.10e−15|0|

En los controles centralizados y receptor directo se enumeran los mismos cuatro patrones; estas accuracies miden capacidad local, **no generalización a datos retenidos**. En las interfaces separadas la accuracy train también es .50 en todas las corridas: no es únicamente un problema de destinos de validación. Las fuentes locales de validación están a2hops en Grid y1–2hops en MHU; las remotas a6–11 y8–12 respectivamente, todas≤T16. Los flips locales llegan a modificar el logit hasta9.67e−4 en Grid y6.82e−3 en MHU, pero nunca cruzan el umbral; los cambios remotos máximos son≤6.71e−8, cercanos al redondeo float32. Un gradiente pequeño no demuestra por sí solo causalidad.

**Conclusión técnica:** etiquetas/loss/optimizer y el bloque pueden aprender XOR cuando reciben conjuntamente sus bits. El bloqueo aparece al separar las interfaces incluso a corto rango. La evidencia es compatible con atenuación de mensajes y con dificultad de integrar XOR cuando cada bit tiene marginalmente información nula sobre su etiqueta. Esas alternativas siguen confundidas; no procede concluir que el alcance T16 o la MHU sean la causa. No se abre el piloto, no se baja .98 y H1–H6 siguen intactos.

**Siguiente prueba recomendada:** mantener exactamente ambos bits, roles, coordenadas, puertos y triples; cambiar sólo el target a `b0`. Esa comparación distingue selectividad/transporte de la interacción XOR sin eliminar la segunda fuente. Cruzarla en una nueva serie técnica explícita con multiplicador de incremento1 frente10 (residual efectivo .1 frente1), conservando parámetros e inicialización, probaría una intervención concreta sobre intensidad de actualización. No es un rescate retrospectivo de v0.1 ni HPO; debe congelarse y tener reglas de parada antes de resultados. GRU, cambio de geometría y más pasos siguen fuera de esta tanda.
