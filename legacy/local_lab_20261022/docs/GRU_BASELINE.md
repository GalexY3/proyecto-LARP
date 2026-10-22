# Baseline GGNN-like aislado, versión técnica1

Protocolo previo a resultados, **NOT_RUN** alcongelar, fecha2026-10-08. Esta rama construye un **candidato de referencia** con recurrencia explícita inspirada en Gated Graph Sequence Neural Networks ([Li etal., ICLR2016](https://arxiv.org/abs/1511.05493)). Es una arquitectura distinta y no reemplaza ni rescata retrospectivamente LARP v0.1; su competencia no se presupone ni queda validada por el nombre del método.

Se mantienen encoder25→32, LN32, mensaje tanh con distancia/mean y readout32→32→1, copiando sus parámetros iniciales byte por byte del G a idéntica seed. Se eliminan update1/update2/q/adapters y se actualiza `h ← GRUCell([mean_message32,encoded32],raw_h32)`, input64/hidden32, sin residual. El encoding sigue persistente y la recurrencia compartida en espacio/tiempo; las marcas son invisibles. GRUW_ih yW_hh completos se inicializan Xavier gain1 con namespaces( seed,9921,1/2), ambos biases0, sin consumir RNG externo.

**No es matching exacto:** GRU tiene12,481 parámetros frente12,261 (+1.794%); MAC lineales por nodo/paso10,240 frente10,112 (+1.266%). Las cifras excluyen activaciones/bias/reducciones y costes del encoder/readout comunes fuera de cada paso. Esta comparación diagnóstica evalúa viabilidad de un bloque estándar; no atribuye cualquier ventaja únicamente a gates ni a MHU.

Se reutilizan el pool16destinos,12train/4val, todos los inputs/roles/coordenadas/grafos/puertos, inicializaciones de cores y el calendario BALANCED congelado porseed. T16/d32, AdamW.003, betas.9/.999, eps1e-8,wd1e-4,clip1,B4,250updates, seeds2101/2102. Se conservan ambosbits incluso en targetb0. El último estado cuenta; no se escoge un checkpoint temprano favorable.

Orden: Grid-localb0(2corridas); únicamente si ambas seeds finitas train+val≥.98 abrir Grid-localXOR(2); únicamente si ambas XORpasan abrir MHU-localb0/XOR(4); únicamente si todas las condiciones locales comunes pasan abrir remoto Grid/MHU×b0/XOR×seeds(8). Techo240s CPU4, máximo16corridas. Puertas fallidas dejan posterioresNOT_RUN; agotamiento conserva parcialesRESOURCE_LIMIT. No hay retries/HPO ni ampliación de presupuesto si falla.

Se congelan módulo/config/dependientes nombrados/runtime y manifest antesdelprimeroptimizer; calendario e inputs se hashean. Registrar loss/accuracytrainyval, gradientes, logits y flips porpatrón. La fraccióncorrecta de flips es redundante conaccuracy alenumerarlos4patrones; evaluar también cambiosdeclase porrol para b0. El resultado nunca abre el pilotooriginal ni test ni actualiza H1–H6.

Comando: `.venv\Scripts\python.exe -m larp.gru_baseline`. El directorio de evidencia es exclusivo. Pruebas: parámetros/RNG/cores exactos, invariancia a marcas y entrebatches, soporte causal≤T y reutilización delcalendario original. Si elbaseline falla, detener esta tanda de transporte sin HPO adicional.

## Resultado observado

**La puerta Grid-localb0 falla.** Ambas corridas llegaron a250updates sin divergencia en18.504s totales, RSSmáximo429,379,584bytes. La pérdida de validación es alta aunque se aprenden los ejemplos train. Se conservan las14ramas XOR/MHU/remoto como **NOT_RUN**, sin iniciar ninguna ni ampliar presupuesto. Identidad congelada: `acc219867e36ec0352ddb344e299166b78a811eaf5379fd7c7f50cb1c8e5893e`.

| Seed | Accuracy train | Accuracy val | BCE val | Mediana update | Mediana \|∂logit/∂b0\| |
|---:|---:|---:|---:|---:|---:|
|2101|1.0000|.7500|1.558116|31.109ms|.4553|
|2102|.9375|.7500|1.670898|31.131ms|.3511|

El GRU mejora ajuste train respecto al nominal BALANCED (.7083/.8958) y obtiene .75/.75 en validación frente .75/.6875. Son dos inicializaciones de un ensayo técnico pequeño; no hay matching exacto, posterior ni evidencia de mecanismo específico GRU. No se adopta automáticamente el baseline ni se declara solucionado el .98. La BCE elevada señala predicciones erróneas muy confiadas fuera de train.

El patrón por contexto importa: **ambas seeds** aciertan los cuatro patrones en destinos26y61, pero responden de forma constante en destinos20y21 (dos aciertos de cuatro). Estos últimos comparten fuente0lógica11 del pool preregistrado. Seed2101 da logits positivos≈6 en ambas interfaces fallidas; seed2102 da negativos en20 y positivos en21. Este hallazgo es posthoc y puede orientar un nuevo diseño de cobertura espacial; no autoriza sustituir destinos ni entrenar selectivamente source11.

| Destino val |2101 predicciones00/01/10/11|2102 predicciones00/01/10/11|Oracle b0|
|---:|---|---|---|
|20|1,1,1,1|0,0,0,0|0,0,1,1|
|21|1,1,1,1|1,1,1,1|0,0,1,1|
|26|0,0,1,1|0,0,1,1|0,0,1,1|
|61|0,0,1,1|0,0,1,1|0,0,1,1|

Los flips fuente0 cambian clase en50% de casos, y los fuente1 en0%; el valor requerido para seleccionar b0 sería100%/0%. Eso concuerda con éxito en dos contextos y fracaso en dos, no con un circuito universal de selección. Los gradientes no corrigen esa interpretación. La fracción de flips correctos vuelve a ser redundante con accuracy porque se enumeran todos los patrones.

**Parada recomendada:** conservar el diagnóstico de generalización/selectividad y terminar esta serie de transporte; no extender250 ni barrer lr/dimensión/GRUinit. Una versión científica futura necesitará un control/oracle para verificar la interfaz y una distribución train/validation con cobertura preregistrada suficiente para atribuir fallos al mecanismo. Mientras tanto, la utilidad espacial del mosaico aviar puede estudiarse en el ensayo de muestreo separado; estos entrenamientos G no dan evidencia contra MHU funcional. El piloto original sigue cerrado; test no abierto y H1–H6 intactos.

Cuatro tests aprobados en1.56s. Resultados/manifest/checkpoints/flips íntegros: `artifacts/gru_baseline/v1`. Figura de predicciones porcontexto: `context_predictions.png`, con errores marcados y logits mostrados; es postprocesamiento, no selección de checkpoint.
