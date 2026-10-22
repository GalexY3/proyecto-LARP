# Intensidad de actualización frente a selectividad: serie técnica v1

Protocolo previo a resultados, estado **NOT_RUN**, fecha2026-10-08. El diagnóstico anterior consiguió XOR cuando sus bits entraban juntos en el receptor (4/4G, accuracy1.0), pero no con interfaces separadas a1–2hops (4/4G, train=val.50). Ese resultado no aísla si el obstáculo es transportar un bit, seleccionar su fuente o integrar la interacción XOR. El fallo remoto tampoco demuestra una desventaja MHU.

Esta tanda factorial mantiene exactamente todos los inputs, dos bits, roles, query, coordenadas, triples, grafos, puertos e inicializaciones de `learning_diagnostics_v1`, y cruza dos factores: **target b0 frente XOR** y **multiplicador1 frente10 del incremento completo**. `b0` conserva incluso la segunda fuente distractora. El multiplicador está dentro del residual original `h ← h + .1·gain·f`; afecta tanto base como adapter, no añade parámetros y equivale aquí a residual efectivo .1 frente1. Gain1 devuelve directamente el tensor del bloque original para reproducir sus operaciones byte por byte. No se cambia model.py, T16, dimensión32, AdamW(.003,.9/.999,eps1e-8,wd1e-4), clip1, batch4 ni250updates.

Antes de optimizer se congelan module/config, todos sus dependientes nombrados, runtime y los hashes reales de los inputs. Se reutiliza el pool previamente congelado de16destinos,12train/4val porcondición. Se registra el estado final, sin escoger checkpoints ni barrer learning rates. La comparación target distingue una relación marginalmente aprendible de XOR; la comparación gain interviene sobre intensidad de dinámica, incluyendo efectos de estabilidad/saturación. Una ganancia eventual no se atribuye automáticamente a velocidad de transmisión ni a MHU.

Orden y puertas preregistradas:

1. Ejecutar8corridas Grid-local: targets b0/XOR, gains1/10, seeds2101/2102. Se abre MHU-local únicamente si **un mismo gain** aprende b0 en ambas seeds con train y validation finales≥.98, finitos.
2. Ejecutar8corridas MHU-local si la puerta previa abre. Se abre remoto únicamente si **un mismo gain común** supera ese criterio b0 en Grid y MHU, ambas seeds.
3. Si abre la puerta remota, ejecutar las16combinaciones completas, ambos gains/targets/geometrías/seeds. La puerta regula coste; no selecciona un gain ganador ni un bloque científico adoptado.

Techo total360s CPU4, máximo32corridas×250updates. Si la puerta falla, las ramas siguientes quedan NOT_RUN; si se agota presupuesto, conservar parciales como RESOURCE_LIMIT y pendientes NOT_RUN. No hay reintentos, extensión adaptativa, test, nueva comparación científica de arquitectura ni actualización H1–H6. Gain1/XOR se comprueba contra el hash final de la tanda anterior; una diferencia impediría usar esa reproducción como control exacto.

Registrar train y validation separadamente, pérdida, norma de gradiente, logits, ambos flips y gradientes para todos los patrones. Para b0, voltear fuente0 debe cambiar el target y voltear fuente1 debe conservarlo; para XOR ambos deben cambiarlo. Si sólo train aprende, reportar fallo de generalización de destinos. Una accuracy local ≥.98 o una mejora bajo gain10 no abre el piloto remoto v0.1.

Reglas de interpretación previstas: si b0 falla bajo ambos gains, estudiar interfaz/agregación/selección antes de recurrencia más compleja; si b0 aprende y XOR falla, estudiar integración y crédito de la interacción; si ambos aprenden localmente y remoto falla, priorizar transporte/condicionamiento; si gain10 mejora y empeora estabilidad en otras condiciones, conservar el trade-off explícito sin declararlo arquitectura nueva. GRU y generador aviar quedan como factores posteriores separados.

Comandos: `.venv\Scripts\python.exe -m larp.transmission_probe --freeze-only` inspecciona identidad sin entrenar; `.venv\Scripts\python.exe -m larp.transmission_probe` ejecuta una vez en directorio nuevo. La ejecución requiere liberar la reserva CPU del generador aviar; preparar código/pruebas no consume esa reserva de entrenamiento.

## Resultado observado

Tanda completada en **74.367 s**, ocho corridas Grid-local de250updates; RSS máximo muestreado460,828,672bytes (439.48MiB). Las24ramas MHU-local/remotas quedaron **NOT_RUN** porque ningún gain aprendió b0 en ambas seeds. Todos los parámetros/outputs/gradientes finales son finitos; la puerta cerrada es de aprendizaje, no de infraestructura. Identidad congelada: `8769335e8b47404edfcb4c928912056e9b27308bec89842d3ab9ad10add0d9be`. Los hashes iniciales por seed son exactamente comunes a los cuatro factores; hay12,261 parámetros en todas las corridas. Gain1/XOR reprodujo el hash de estado final de v1 **byte por byte en ambas seeds**. Resultados y todos los patrones/flips: `artifacts/transmission_probe/v1/results.json`; también se conservan checkpoints finales con optimizer, orden, cursor y RNG. No se reintentó ninguna corrida.

| Target | Gain | Seed | Accuracy train/val | BCE val | Mediana \|∂logit/∂b0\| | Norma gradiente final antes de clip |
|---|---:|---:|---:|---:|---:|---:|
| b0 |1|2101|.50/.50|.693111|1.44e−4|.104|
| b0 |1|2102|.50/.50|.693912|1.10e−4|.116|
| b0 |10|2101|.50/.50|.780632|1.02e−3|5.307|
| b0 |10|2102|.50/.50|.954553|.1183|5.994|
| XOR |1|2101|.50/.50|.693355|4.43e−5|.926|
| XOR |1|2102|.50/.50|.693206|2.77e−4|.496|
| XOR |10|2101|.50/.50|.827463|1.02e−3|17.029|
| XOR |10|2102|.50/.50|.749464|5.21e−3|7.091|

Ningún flip de ninguna fuente cambió la predicción de clase. En b0, los flips de la fuente relevante sólo se acertaron en50% y los de la distractora también en50%: conservar una decisión constante no demuestra invariancia selectiva cuando su accuracy base es .50. Gain10 aumentó gradientes locales pero empeoró BCE y provocó mayor clipping; **más sensibilidad numérica no equivale a transmisión útil o decisión correcta**. No hubo NaNs que permitan culpar a divergencia numérica. No se ejecutó la parte MHU de este factorial, así que carece de comparación geométrica incluso técnica.

La selectividad sencilla también falla con las interfaces locales bajo este presupuesto. Por tanto XOR no es la única dificultad. La recomendación inmediata es investigar selección/transmisión y optimización bajo variación de interfaces antes de añadir GRU o sustituir geometría. El multiplicador10 se rechaza como arreglo automático: no logró el objetivo ni justifica ampliar intensidad/updates hasta encontrar un éxito.

**Prueba discriminante siguiente, propuesta y no ejecutada:** conservar los12triples, datos, estados iniciales, B4 y250updates; contrastar el orden aleatorio actual con batches de los cuatro patrones completos de un triple. Así el target está exactamente balanceado en cada update, en lugar de introducir ruido de bias por minibatches. Deben mantenerse fijo el target b0 y el gain original1 para cambiar un factor único. Si el balanceo aprende, el problema de entrenamiento no queda resuelto científicamente: habrá que regresar al dataset y presupuesto originales con una nueva preregistración común. Si falla, un segundo diagnóstico sobre un único triple fijo permite separar dificultad básica de transporte y variación espacial, sin cambios del bloque. Ninguna de estas propuestas ha actualizado H1–H6 ni abierto el piloto.

Pruebas previas: cinco tests aprobados en1.60s verifican gain1 exacto, matching de parámetros/inicialización, preservación de inputs al cambiar target, gate común sin mezclar gains/seeds favorables y scoring correcto de flips para b0. Los tests son comprobaciones de implementación, no evidencia de aprendizaje.
