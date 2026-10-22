# Control positivo determinista de transporte por rol

Tanda única congelada2026-10-08, completada en **.111231s** de cálculo/preparación medidos enmain; comando completo2.038s conimports. Se evaluaron256inputs únicos (Grid/MHU×local/remoto×12train/4validation×4patrones),512decisiones al aplicar b0yXOR. **100% de accuracy final en los16estratos target/familia/distancia/split**, todos los roles accesibles aT16. No se entrenó ningún parámetro. Identidad congelada: `202f291ff3f038475b2124dbd6b3e2c6b48316cdc458ecabcb8a5d9949dbd488`.

El script nuevo `artifacts/diagnostics/role_transport_oracle.py` recibe en su función de cálculo **únicamente inputs, arcos, horizonte y persistencia**. No recibe source_nodes, coordenadas de fuentes, casos ni targets. El destino se obtiene de los canales query14:19 de los inputs; las fuentes se distinguen por canales9y10. Los targets se leen únicamente después de calcular predicciones, para evaluar. Config/script/dependientes/runtime y referencia alpool fueron hasheados en `artifacts/diagnostics/role_transport_oracle_v1/preregistration.json` antes de producir outputs. La ruta exclusiva impide sobrescribir resultados.

Se codifican cuatro campos porneurona desde inputs: `[role0*bit,role0,role1*bit,role1]`. Cada paso es difusión no aprendida `h_next=.5h+.5mean_incoming(h)` con los arcos originales y vacío→0. EnT16, el decoder calcula cada bit como numerator/denominator local en el query. Si denominator=0, marca ese rol inaccesible y devuelveNone en la decisión que lo requiere; nunca completa con el target. Los campos se calculan float64. Dos selfchecks verifican recuperación de los cuatro patrones enunhop y Nonecuando no hay transporte.

La razón de este éxito es conocida. Para el rolr hay una fuente única con bitb_r. Si la máscara inicial esv_r, el numerator inicial esb_r·v_r. La difusión linealW aplica el mismo operador a ambos, así que despuésTpasos `numerator=W^T(b_r·v_r)=b_r·W^T(v_r)=b_r·denominator`. El ratio recupera exactamenteb_r cuando existe un camino de≤T, independientemente de cuánto se haya atenuado. Esta prueba explica el resultado; no representa una red que haya aprendido selección ni normalización.

| Familia | Distancia | Split | Denominador mínimo porrol | Accuracy b0/XOR |
|---|---|---|---:|---:|
|Grid|local|train|.012452|1/1|
|Grid|local|validation|.007901|1/1|
|Grid|remoto|train|7.75e−9|1/1|
|Grid|remoto|validation|1.46e−8|1/1|
|MHU|local|train|.002564|1/1|
|MHU|local|validation|.006993|1/1|
|MHU|remoto|train|4.12e−12|1/1|
|MHU|remoto|validation|3.66e−10|1/1|

**Interpretación permitida:** la interfaz suministra la información de rol y payload necesaria, el grafo transmite influencia a tiempo y existe una solución algorítmica especializada con estos inputs. Los fallos de G/GRU no se explican por ausencia de accesibilidad en estepool. Sigue abierta la dificultad de aprender selectividad/generalización bajo el bloque y presupuesto previstos. La solución usa inducción específica de la tarea, ratio explícito y aislamiento porrol; no tiene matching de parámetros, FLOPs ni entrenamiento con las redes.

**Límite crucial:** denominadores remotos de hasta4.12e−12 implican señales muy atenuadas. La exactitud delratio se beneficia de difusión ideal y numerator/mask perfectamente acoplados; ruido interno independiente o un decoder aprendido podrían fracasar. No se probó robustez. La existencia delalgoritmo no garantiza que SGD descubra algo equivalente, ni que MHU mejore su coste/calidad. No se resuelve el98% neural, no se abre elpiloto original, no se abre testcientífico ni se actualizan H1–H6.

Resultados íntegros y valores recuperados: `artifacts/diagnostics/role_transport_oracle_v1/results.json`. Se conserva el mismo pool congelado, incluidos los contextos que fallaron en GRU. Con este control se **cierran las ramas diagnósticas de transporte de esta fase**, sin nuevas corridas/HPO ni rescates.
