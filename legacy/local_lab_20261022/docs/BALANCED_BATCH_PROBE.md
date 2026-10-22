# Cuartetos balanceados frente a batches aleatorios

Protocolo previo, estado al congelar **NOT_RUN**, fecha2026-10-08. La tanda anterior mostró que aumentar el incremento×10 no resolvía b0 ni XOR local. Esta comprobación mínima interviene sobre **la política de minibatches**, agrupando los cuatro patrones de un contexto. Cambian acoplamiento y orden de contextos; además, el último ciclo incompleto introduce pequeñas diferencias de exposición individual, cuantificadas abajo. El contraste orienta el diagnóstico de entrenamiento, pero no aísla exclusivamente el balanceo de etiquetas.

Se conserva Grid N400 g1101, G original/gain1, target b0, T16, inputs completos con ambas fuentes/IDs/query/coordenadas,12triples train/4validation,48/16casos y las seeds2101/2102. AdamW .003, B4, clip1 y250updates. RANDOM se reutiliza explícitamente de `transmission_probe_v1`: no son nuevas corridas ni réplicas independientes. BALANCED toma los cuatro patrones00/01/10/11 de un mismo triple porupdate, con ciclos de12triples aleatorios sin reemplazo segúnSeedSequence(20261008,seed,9914). Cada caso recibe20–21exposiciones y, en BALANCED, cada triple todos sus patrones por igual. El total1000casos vistos es común; el vector de exposiciones por caso no es idéntico entre políticas.

Antes del primer optimizer se congelan módulo/config, dependientes/runtime nombrados, calendario de minibatches, casos/hashes y referencia exacta a controles RANDOM. Se verifica identidad byte a byte de inputs, targets e inicialización. Registrar todos los patrones y gradientes de fuentes en updates0,1,25…250, además de norma de gradiente de parámetros/loss porupdate. Las medidas son lecturas y no escogen checkpoints. Un éxito técnico exige ambosseeds con train+validation≥.98, finitos, enupdate250. No abre el piloto v0.1 ni demuestra ventaja MHU.

Techo120sCPU4 para doscorridas nuevas; conservar parciales si seagota y no extender/reintentar. Fullbatch48 se registra **NOT_RUN**, sin ejecutarlo. Si BALANCED falla, detener el rescate del núcleo nominal y considerar un baseline competente con recurrencia explícita bajo una nueva versión/preregistro; GRU no se añade aquí. No se elimina ninguna coordenada/fuente ni se modifica geometría. No se abre test ni se actualizan H1–H6.

Comando: `.venv\Scripts\python.exe -m larp.balanced_batch_probe`. La ruta de evidencia es exclusiva; una repetición que intente sobrescribirla se rechaza. La corrida sólo empieza tras liberar la reserva CPU del sampler aviar.

## Resultado observado

Ambas corridas completaron250updates, sin reintentos, en **44.246 s** incluyendo todas las trazas. RSS máximo muestreado460,632,064bytes. Identidad congelada `e8abca25c617b7d53c98ca7096ff67e9b1c1a332bc24a2c0ac9ca335b613af7f`. Todos los checks de compatibilidad con RANDOM aprobaron: misma inicialización, inputs, targets, interfaz y presupuesto. RANDOM se conserva como control reutilizado; las dos corridas BALANCED son las únicas nuevas.

| Seed | RANDOM train/val reutilizado | BALANCED train final | BALANCED val final | BCE val final |
|---:|---:|---:|---:|---:|
|2101|.50/.50|.708333|.750000|.565222|
|2102|.50/.50|.895833|.687500|.946849|

**La puerta≥.98 falla.** El balanceo sí permite aprendizaje parcial que los batches aleatorios no mostraron, pero no resuelve selectividad/generalización. Seed2102 aprende más en train y pierde calibración en validación; su BCE final incluso supera RANDOM (.693912). Se conserva toda la trayectoria: no se elige el update175 de seed2102, cuya val era .75/BCE.4387. Fullbatch48 permanece **NOT_RUN**, y esta rama de rescate del núcleo nominal se detiene aquí.

**Limitación de atribución detectada en auditoría:**250updates×B4=1000 no es múltiplo de48. Ambos métodos completan20exposiciones de cada caso y40observaciones adicionales, pero estas40 se reparten de forma diferente. Reconstruyendo exactamente el RNG de RANDOM: seed2101 tiene16casos cuya exposición difiere en±1 de BALANCED; seed2102 tiene12. Totales de targets positivos: RANDOM499/BALANCED500 en2101;500/500 en2102. Los totales por patrón de RANDOM2101 son `[251,250,249,250]`, frente a `[250,250,250,250]` de BALANCED; en2102 ambos totales globales son250porpatrón, aunque difiere el reparto por contexto. La intervención también modifica la secuencia de contextos. Por ello, el aprendizaje parcial no se atribuye exclusivamente a equilibrio de labels dentro de B4. Los protocolos/configs/checkpoints congelados y resultados permanecen intactos; no se ha ejecutado un rescate nuevo. Una comparación futura con ciclos completos podría eliminar el resto de exposición, pero requeriría otra serie y no corregir retrospectivamente ésta.

Accuracy por patrón en los cuatro destinos de validación (target=b0):

| Seed |00|01|10|11|
|---:|---:|---:|---:|---:|
|2101|4/4|1/4|3/4|4/4|
|2102|3/4|3/4|2/4|3/4|

La mediana de sensibilidad al bit0/bit1 es .283/.760 para2101 y .542/.575 para2102. La fracción de flips que cambia clase es .50/.50 y .375/.125, respectivamente: para una selección perfecta de b0, debería ser1 para fuente0 y0 para fuente1. La fuente distractora todavía modifica respuestas y la fuente relevante no las controla consistentemente. En una enumeración completa de los cuatro patrones, la fracción de predicciones correctas tras flips es matemáticamente redundante con accuracy porque los flips permutan los casos; no se presenta como validación independiente del mecanismo. Los patrones, logits y gradientes individuales permiten examinar las asociaciones sin inflar réplicas.

La intervención acotada orienta hacia **ruido/coherencia de gradientes y representación selectiva**, además de atenuación con distancia. No acredita utilidad MHU, no elimina alternativas de implementación del bloque y no sugiere que bastaría extender updates hasta ganar. Debe continuar un baseline competente en versión nueva, con prerregistro y presupuesto común, conservando estos resultados negativos y parciales. No se añade GRU aquí. El piloto original sigue cerrado, test no abierto y H1–H6 sin actualizar.

Software: dos tests pasan en1.55s, verificando ciclos sin reemplazo, cuartetos/patrones completos, exposiciones20–21 exactas y rechazo de controles con distinto input o inicialización. Figura: `artifacts/balanced_batch_probe/v1/batch_summary.png`; JSON íntegro y checkpoints/trazas se encuentran en el mismo directorio.
