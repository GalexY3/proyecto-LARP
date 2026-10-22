# Ledger A–J: diez ciclos dinámicos

Cierre solicitado por el investigador: 10/30 ejecutados; veinte pendientes. Todos exploratorios. Las preguntas A–D y decisiones E–J se reproducen de sus registros originales; los recibos C01–C05 conservan su estado histórico RUN.

## C01: normalization_intervention

Freeze previo a ejecución: [63871e4](https://github.com/GalexY3/proyecto-LARP/commit/63871e49775a6e07fd272632f81c2faf001e2576). [Protocolo](cycles/C01/protocol.json), [fuente](cycles/C01/source.py), [resultado](cycles/C01/result.json), [decisión](cycles/C01/decision.json).

**A.** En el split histórico UCI Digits, ¿la guarda de desviación nula explica el colapso de robustez del MLP de píxeles? Estimando: diferencia pareada de accuracy al cambiar solo normalización; población condicionada al benchmark.

**B.** ["H_bug: escalar píxeles constantes por 1e-5 crea el colapso", "H_filter: la diferencia sensorial persiste tras reparar", "H_otras: convergencia, regularización y clipping"]

**C.** MLP de píxeles con normalización legacy, guarda correcta y escala fija; misma semilla, entrenamiento, splits y corrupciones. Barrido de escalas es una condición de este único contraste.

**D.** 1797 imágenes 8x8 sklearn Digits, splits 811/812 y corruptions 99128. La auditoría fuente previa ya detectó la condición imposible; este ensayo mide su efecto, no descubre el bug a ciegas.

**E.** Legacy ruido .3889/rotación .3444; guard .3578/.3222; fijo .8644/.5600. Clean ~.97.

**F.** La hipótesis de que solo los cuatro píxeles de varianza cero causan la catástrofe no sobrevive: guard no mejora. El escalado completo sí es un rival material.

**G.** Replay exploratorio sobre test histórico, no réplica externa; versión de entorno difiere.

**H.** Baja credibilidad del bug específico como explicación suficiente; sube preprocesamiento de dimensiones de varianza pequeña.

**I.** Intervención controlada de normalización, coste ~5s; ventaja MHU no probada.

**J.** PIVOT al mecanismo de amplificación por varianzas pequeñas


## C02: rare_variance_noise_amplification

Freeze previo a ejecución: [fb98862](https://github.com/GalexY3/proyecto-LARP/commit/fb988621a3f569a29667a5999600d08899c56cfa). [Protocolo](cycles/C02/protocol.json), [fuente](cycles/C02/source.py), [resultado](cycles/C02/result.json), [decisión](cycles/C02/decision.json).

**A.** ¿La energía de la perturbación estandarizada se concentra en píxeles de pequeña varianza positiva, incluso tras arreglar ceros?

**B.** ["H_rare: pequeñas desviaciones positivas dominan el shift", "H_zero: solo cuatro ceros", "H_other: arquitectura o cambio semántico de corrupción"]

**C.** Descomponer energía normalizada y clipping por dimensiones y cuantificar contribución de std<.05 frente a std>=.05 con legacy/guard/fijo.

**D.** Mismos datos históricos UCI Digits; instrumentos versionados. Elección después de inspeccionar decisión anterior.

**E.** Con guard, 99.52% de energía de ruido normalizado viene de std positiva<.05; ruidoenergía total5982 frente1.17enescala fija. Rotación:92.35% en esasdimensiones.

**F.** Energía medida antes de clipping no equivale al impacto causal del clasificador; hace falta intervención de escala acotada.

**G.** Diagnóstico determinista condicionado a imágenes/corrupciones ya abiertas.

**H.** Amplificación de casi-constantes es mecanismo plausible; ceros solos no bastan.

**I.** Medición exacta de transformación, sin nueva evidencia MHU.

**J.** CONTINUE con controles convencionales de escalado acotado


## C03: conventional_scaling_controls

Freeze previo a ejecución: [a007893](https://github.com/GalexY3/proyecto-LARP/commit/a00789311a564d4dd47b277e29084496cb35965c). [Protocolo](cycles/C03/protocol.json), [fuente](cycles/C03/source.py), [resultado](cycles/C03/result.json), [decisión](cycles/C03/decision.json).

**A.** ¿Un escalado convencional con piso de varianza o escala global elimina la aparente necesidad del frontend sensorial robusto?

**B.** ["H_scale: piso train-only mejora ruido/rotación sin cambiar arquitectura", "H_sensor: hace falta organización sensorial", "H_otras: underfitting y regularización"]

**C.** MLP píxeles, misma semilla/split, modos guard/fixed/global y pisos .05/.1/.2. Son condiciones de una sola pregunta; no selección confirmatoria del mejor.

**D.** Mismos datos históricos UCI Digits; instrumentos versionados. Elección después de inspeccionar decisión anterior.

**E.** Escala global train-only: clean98.22%, ruido92.44%, rotación59.56%; guard97.11/35.78/32.22. Piso .2: ruido89.78. Misma red y datos.

**F.** Escalados elegidos adaptativamente; no afirmar confirmación ni compararlos sin replay con sensores.

**G.** Sin evidencia externa; mismo dataset y corrupción.

**H.** Se debilita fuerte la ventaja de ruido atribuida al pipeline; queda explicar rotación.

**I.** Coste seis entrenamientos; efectos grandes de preprocesamiento, convergencia no establecida.

**J.** PIVOT a comparación completa con escala global común


## C04: pipeline_parity_after_scaling

Freeze previo a ejecución: [d0a45b5](https://github.com/GalexY3/proyecto-LARP/commit/d0a45b5c1c1cee797f4f4d54bc2da839a13335fc). [Protocolo](cycles/C04/protocol.json), [fuente](cycles/C04/source.py), [resultado](cycles/C04/result.json), [decisión](cycles/C04/decision.json).

**A.** ¿Subsiste una ventaja del frontend MHU frente a otros frontends y píxeles bajo la misma política de escalado global y semillas de modelo cruzadas?

**B.** ["H_geom: MHU aporta robustez específica", "H_front: filtrado explica efecto para cualquier geometría", "H_scale: baseline convencional cierra brecha de ruido", "H_otras: convergencia"]

**C.** Cinco métodos×4geometrías×2inicializaciones y píxeles×2inicializaciones; 240steps, mismas corrupciones y global train-only. Agregar primero inicializaciones dentro de geometría.

**D.** Mismos datos históricos UCI Digits; instrumentos versionados. Elección después de inspeccionar decisión anterior.

**E.** Con escala global, pixels ruido92.67%/oclusión86.56%; MHU90.81/81.22. Rotación pixels60.67%, MHU72.81%, CVT74.14%, LOCAL72.11. 13/42bestcheckpointalcap.

**F.** Sensores no tienen ventaja general; rotación puede ser filtrado espacial común y n4noestablece diferenciaespecífica.

**G.** Mismo testhistórico; semillasmodelocruzadasnoconfirmaciónexterna.

**H.** MHUespecialnoapoyado; filtrado/invariancia sigueplausible.

**I.** Pipelinecomparison noigualacosteencoding; controlnormalizaciónsíconsistente.

**J.** CONTINUE con matrizexacta para distinguir información de filtrado


## C05: exact_linear_encoder_information

Freeze previo a ejecución: [f3bc2a5](https://github.com/GalexY3/proyecto-LARP/commit/f3bc2a529d627c09182837d05a8f8ddb2372fa6e). [Protocolo](cycles/C05/protocol.json), [fuente](cycles/C05/source.py), [resultado](cycles/C05/result.json), [decisión](cycles/C05/decision.json).

**A.** ¿Las 80featureshomogéneas constituyen nueva información o una transformación lineal delos64píxeles, yquécondicionamientoimponen?

**B.** ["H_linear: F=XMexactamente", "H_newinfo: frontend añade observaciones independientes", "H_other: nonlinear clipping o bordes"]

**C.** Construir M aplicando encoder a64bases; verificar residual enDigits, SVD/rango, traza y normadefilas para20patrones.

**D.** Mismos datos históricos UCI Digits; instrumentos versionados. Elección después de inspeccionar decisión anterior.

**E.** Residualmáximolineal8.88e-16;17/20operadoresrango64. TodosMHU64;condiciónMHU423–25789,Sobol435–1166. Traza9.92–12.16.

**F.** Másfeatures noañaden información. Invertibilidadformal no implica estabilidad ni invariancia. Auditorindependiente adviertefixed vs global cambiacentrado yescala.

**G.** Identidad instrumentalaudita20patronesexistentes; no originalidad nireplicaciónexterna.

**H.** Bajaexplicación nueva información; sube filtrado/condición. Separarcentradoyescalaantesatribución.

**I.** Exactitudlinealverificada; n4geom, costebajo.

**J.** REPAIR deatribuciónaislando centrado yescala enunfactorial


## C06: centering_scaling_factorial

Freeze previo a ejecución: [d8e0fda](https://github.com/GalexY3/proyecto-LARP/commit/d8e0fda923e5818ca3a249c44e932a8c2cb96737). [Protocolo](cycles/C06/protocol.json), [fuente](cycles/C06/source.py), [resultado](cycles/C06/result.json), [decisión](cycles/C06/decision.json).

**A.** ¿Qué parte del cambio de robustez proviene de centrar por píxel y qué parte de la escala, manteniendo red y clipping?

**B.** ["H_scale: desviacionespequeñas dominan", "H_center: centrado espurio domina", "H_interaction: ambos interaccionan", "H_otras: optimizador/regularización"]

**C.** Factorial centrado{ninguno,porfeature}×escala{unidad,global,guard,piso.2},2inicializaciones, 240steps. Todos son condiciones de este ciclo.

**D.** Mismos datos históricos UCI Digits; instrumentos versionados. Elección después de inspeccionar decisión anterior.

**E.** Escala guard empeora ruido con ysincentrado; globalcentrado92.67 vsglobalnocentrado87.44. Unidadcentrada91.33 vsnocentrada87.0. Ambosfactoresimportan.

**F.** Separaefectodeescala delcentrado; fixedvsglobalera intervencióncompuesta. Todavíano identificafiltrado.

**G.** 16entrenamientosson condicionespareadas, no16ciclos niconfirmaciones.

**H.** Escaladoperverso explica granpartecatástrofe; centrado contribuyeadicionalmente.

**I.** Validezcondicionada aMLP/AdamW; presupuesto yrecibos ahoraenforcedporworker.

**J.** PIVOT acontroleslowpassconvencionalespararotación


## C07: standard_lowpass_baselines

Freeze previo a ejecución: [6255488](https://github.com/GalexY3/proyecto-LARP/commit/62554885e497649a89ecaaf1595e4635f2eaae46). [Protocolo](cycles/C07/protocol.json), [fuente](cycles/C07/source.py), [resultado](cycles/C07/result.json), [decisión](cycles/C07/decision.json).

**A.** ¿El beneficio de rotación del frontend espacial puede explicarse con suavizado o pooling convencional sin MHU?

**B.** ["H_lowpass: blur/poolingretiene beneficio", "H_irregular: hacefaltadistribuciónirregular", "H_otras: capacidad/parametrización"]

**C.** Píxeles, blurgaussiano sigma.5/.85 ypool2x2→4x4; MLP ~5.8kparams,2inits, globaltrain. Benchmark yaexpuestoexploratorio.

**D.** Mismos datos históricos UCI Digits; instrumentos versionados. Elección después de inspeccionar decisión anterior.

**E.** Blur.5rot53.78%, blur.8545.22%, pool4 44.33 frentepíxeles60.67; RBFfrontsC04~68–74. Blurconvencional NOreproducebeneficio.

**F.** Refutada versiónsimplelowpass; nohacefaltainterpretarresultadofavorableMHU, controlesRBFalineadosfaltan.

**G.** Mismotest; exploraciónadaptativa.

**H.** Bajaexplicaciónsolofiltrogaussianotranslacional; sube kernelRBFnormalizado/soporteyfronteras.

**I.** Paramcountparecido, operadoresdistintosnocausalidadMHU.

**J.** CONTINUE con poolingRBFdenso sin puntosirregulares


## C08: dense_rbf_pooling_control

Freeze previo a ejecución: [e39dfe7](https://github.com/GalexY3/proyecto-LARP/commit/e39dfe7424f0034079d789a7abd8dcfb65a33e48). [Protocolo](cycles/C08/protocol.json), [fuente](cycles/C08/source.py), [resultado](cycles/C08/result.json), [decisión](cycles/C08/decision.json).

**A.** ¿Un operador RBF normalizado sobre la rejilla completa reproduce tolerancia a rotación sin geometría irregular ni tipos?

**B.** ["H_RBF: normalización/centrosdelkernel explican", "H_irregular: selecciónirregularesnecesaria", "H_otras: redundancia/capacidad"]

**C.** Píxelesuniformes→RBF16centros, RBF64centros, 5copiasRBF16→80features; misma sigma.16,globaltrain,2inits, ~5.8kparams.

**D.** Mismos datos históricos UCI Digits; instrumentos versionados. Elección después de inspeccionar decisión anterior.

**E.** RBFdenso16centrosrot66.0%,64centros52.89%,16x5 62.22; frontsorganizadosC04~72–74. Todos paganendensidad/clean.

**F.** RBFdensoexplicapartedebrechapero no toda; copiaredfeaturesnobastaypuedecambiaroptimizador.

**G.** Continúaexploraciónsobremismo test; no atribuirmargenaMHUporqueCVTgana.

**H.** Quedaposible diversidaddefiltros/condicionamientocomomecanismocompartido.

**I.** Información/rangodiferenteentrecontrolesexplicitado; comparaciónnocertificacausalidadasintótica.

**J.** CONTINUE ablación de diversidad de cinco lecturas


## C09: multiview_versus_average_pooling

Freeze previo a ejecución: [ccb9a6a](https://github.com/GalexY3/proyecto-LARP/commit/ccb9a6a9a023974906e581440c512095603ed2e3). [Protocolo](cycles/C09/protocol.json), [fuente](cycles/C09/source.py), [resultado](cycles/C09/result.json), [decisión](cycles/C09/decision.json).

**A.** ¿La diversidad entre cinco bloques RBF de intensidad es necesaria, o su promedio espacial explica la tolerancia a rotación?

**B.** ["H_diverse: diferenciasentrebloquesaportaninformaciónútil", "H_pool: promedio16basta", "H_otras: dimensión/regularización"]

**C.** MHU yCVT,4geom,original80vsmean16vsmean16repetido5. Global,init991,~5.8kparams. Medir rangoytodosshifts.

**D.** Mismos datos históricos UCI Digits; instrumentos versionados. Elección después de inspeccionar decisión anterior.

**E.** Promedio16 MHUmantienerot74.11 vsorig75.06, CVTmean76.72 vsorig73.83. Clean yruido empeoran; copias80no recuperanmejora.

**F.** Invarianciacontradeoffdeinformación/regularización, noMHUespecial; promedioperderango16 ypodríamodificarrepresentación.

**G.** Condicionesexploratorias4geomx2métodos.

**H.** Tiposdistintosnoindispensablespara rotación; varíanatribuciónycostes.

**I.** n4, initúnicoporciclo peroC04cruzó2. No significaciónselectiva.

**J.** CONTINUE controlcontrafactual: transportar mismoclasificadorporoperadorinvertible


## C10: neural_function_transport

Freeze previo a ejecución: [42f2777](https://github.com/GalexY3/proyecto-LARP/commit/42f277770336575eabcdbdcc7cbd403163f4bd06). [Protocolo](cycles/C10/protocol.json), [fuente](cycles/C10/source.py), [resultado](cycles/C10/result.json), [decisión](cycles/C10/decision.json).

**A.** ¿Se puede expresar exactamente el mismo clasificador de píxeles a través de frontends MHU/CVT completos, conservando sus predicciones incluso bajo corrupción?

**B.** ["H_reparam: fullrankpermitemismofuncion/robustez", "H_arch: frontendimponeventajaexpresiva", "H_otras: precisiónfinita"]

**C.** EntrenarunpixelMLPglobal, construirprimeracapaequivalentemediantepinversaM para4MHUy4CVT; comprobarlogits/prediccionesfloat64yfloat32 sin volveraentrenar.

**D.** Mismos datos históricos UCI Digits; instrumentos versionados. Elección después de inspeccionar decisión anterior.

**E.** Los ocho transportes (cuatro MHU y cuatro CVT) conservan todas las predicciones evaluadas, tanto en float64 como en float32. Máximo error de logits: 8.146372465489549e-12 en float64 y 0.00034234673114674763 en float32.

**F.** El transporte utiliza el rango completo del operador lineal y una pseudoinversa. Mantiene 78 unidades ocultas: 7108 parámetros sensoriales frente a 5860 del pixel y 5834 del frontend histórico de 64 unidades. No demuestra equivalencia a igual presupuesto, aprendizaje, regularización, estabilidad numérica ni coste. Las normas de pesos pueden crecer mucho.

**G.** Control algebraico y numérico sobre datos históricos expuestos; no hay confirmación externa.

**H.** Se debilita la explicación por mayor expresividad del frontend MHU completo en este pipeline. Siguen abiertas las explicaciones por condicionamiento, optimización y regularización, que también pueden favorecer controles convencionales. No se actualizan numéricamente los priors históricos H1-H6.

**I.** Validez interna del transporte apoyada por acuerdo de predicciones y residuos pequeños. Identificación limitada al operador y clasificador estudiados. Robustez fuera de estos datos y coste total sin establecer.

**J.** STOP de esta sesión por indicación expresa del usuario de finalizar con los créditos restantes. Diez de treinta ciclos solicitados ejecutados; veinte pendientes, sin fabricar ciclos adicionales. No equivale a refutación universal de MHU ni a confirmación de su utilidad.

