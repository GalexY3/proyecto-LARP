# Estado de implementación LARP v0.1

Fecha: 2026-10-08. **Implementación y verificaciones terminadas; piloto detenido por puerta XOR fallida.** Código ejecutado: commit `a580b3654136fa5cc7e5d5bd7c053ffd49a23006`; identidad de fuentes/protocolo/runtime `69c4739d1221098d3684d8c70acf33b52ed503dfb8e3ee863e6790f11285ed78`. Los commits posteriores de informes no cambian esa identidad computacional.

**Continuación posterior:** [LARP_PHASE_3_RESULTS_AND_NEXT.md](C:/Programación/LARP/LARP_PHASE_3_RESULTS_AND_NEXT.md) registra fase 3 `role_coverage_v1`: cuatro corridas completas de 250 updates, 38,912 segundos de proceso frente al límite de 120; BALANCED train/SS/UU al 100% en ambas semillas, puerta local PASS. AUX antiguo falla en destino 61 para 2102. XOR/piloto siguen cerrados; H1–H6/C no cambian. H-R se actualiza ordinalmente por separado. Suite actual: 232 PASS; los 163 PASS y las puertas originales de abajo son históricos. La identidad original se conserva para esa serie; los módulos nuevos tienen identidad y manifiestos propios.

## Implementación y ejecución

| Área/fase | Estado y alcance real |
|---|---|
| Auditoría, instalación, perfiles | Implementados; Python3.13.4/PyTorch2.14.1+cpu, lock de29 paquetes comprobado, pip check limpio |
| Geometría/grafos | Original MHU/HU, gradientes, certificados por tipo/unión, controles, kNN6, Delaunay, RR/SW/Grid/Poisson implementados y probados; originalN400/g1101 certificado ejecutado |
| Núcleo/datos | G/T/F, matching, simetrías, propagación/batch, XOR/copy/fill8/resources29, puertos/oráculos y trainer reanudable implementados y probados |
| Suite global | **163 PASS**, cero fallos/errores/skips,8.12s de pytest; log y JUnit en `artifacts/tests/` |
| Calibración | Ejecutada:5 updates warmup+200medidos de copyT, N400/g9001/s9002, CPU4threads, T16/B4 |
| Smoke | Cuatro corridas completas de XOR G a250updates; **puerta científica FAIL**, ningún test abierto |
| Copy focal/fill/screens | Implementados/dry-run probado; **NOT_RUN / bloqueados por smoke** |
| HPO/confirmación | Implementados/dry-run probado; **NOT_RUN**, congelación y suite completa obligatorias antes de inferencia |
| Robustez/M1/funciones/escalado | Evaluadores invocables, pesos congelados, masks/coverage/SCC y tests mini; **NOT_RUN científicamente**, escala exige tres archivosN1600 nuevos certificados |
| AB/reportes | Implementados y tests sintéticos; CSV/PNG reales generados; priors **UNUPDATED** |
| Recursos artificiales | Oráculos, encoder29, pérdida/varianzaNMSE y tests implementados; ensayo científico completo con matched pendienteC3 |
| Jacobianos/plasticidad | Diagnóstico input→output XOR ejecutado; suite mecanística general/plasticidad **NOT_RUN**, H5 sin identificar |

La carpeta `runs/series_cli_exitfix/` contiene la serie actual. `runs/calibration/` y `runs/smoke/` conservan la primera serie. Tras reparar únicamente la propagación del código de salida CLI, se repitieron las mismas semillas. Los cinco modelos finales, datasets, pairing y scores/loss son **exactamente iguales**, comprobados en `artifacts/reproducibility_cli_fix.json`. Son repeticiones técnicas, no geometrías independientes nuevas. No se seleccionó el resultado más favorable.

## Certificado original real

N400, L20, counts `[163,85,68,50,34]`, primer intento admitido;6000Adam, LBFGS terminó por tolerancia de gradiente sin iteraciones adicionales. Generación/certificación original2.600s, pico del proceso96.584MB. Separación mínima0.3000000037. Ratios medios de varianzaR4/R5: A.2832,B.2740,C.3049,D.3544,E.2553,unión.3125. Cada componente/unión satisface espectro y desorden finitos. Esto no es una demostración asintótica ni un resultado de computación neuronal.

kNN6:2400arcos, in-degree6, una SCC, sin reparación. Delaunay:2400arcos y prueba de traslación ejecutada. Gradiente analítico contra diferencias finitas ejecutado. Archivos: `artifacts/geometry/mhu_N400_g1101_{certificate,graph_metrics,technical_checks,timing}.json`, y NPZ local.

## Coste medido y presupuesto

Calibración actual: mediana32.597ms/paso, p9034.818ms;16.289s de entrenamiento incluyendo validaciones periódicas,3.139s de evaluación final separada;RSS muestreado430.686MB. Los pasos individuales excluyen binding de datos; el wall completo lo incluye. CPU4threads, float32, sin AMP/CUDA.

Las cuatro optimizaciones XOR suman50.949s incluyendo validaciones periódicas; cada una procesa1000ejemplos. Calibración procesa820ejemplos incluyendowarmup. Suma de entrenamiento registrada de la serie actual67.238s; no incluye generación, arranque Python ni diagnóstico posterior de todos los ejemplos. RSS máximo muestreado de las cinco corridas430.973MB. Todos estos números proceden de results.json; no son estimaciones.

La extrapolación conservadora a doce corridascopy1000 es1104.17s≈18.4min, **estimación**, no tiempo observado. La regla de coste conserva1000updates, pero la puerta de aprendizaje impide gastarlos. Restan los12000updates previstos del piloto: cero ejecutados. El límite8h no autoriza saltarse esa puerta.

## Resultado negativo completo de XOR

| Geometría/familia | g | init | Train accesible | Validación accesible | Acceso train/val | BCE val |
|---|---:|---:|---:|---:|---:|---:|
| Grid-G |1101|2101|.51025390625|.48046875|100%|.6931000948|
| Grid-G |1101|2102|.5|.5|100%|.7030170560|
| MHU-G |1101|2101|.51416015625|.517578125|100%|.6924373507|
| MHU-G |1101|2102|.5|.5|100%|.6971684694|

El umbral preregistrado es.98. Ninguna corrida lo alcanza, tampoco aprende sustancialmente en train. Mediana de hops requeridos8Grid/9MHU; todos≤16. **STOP** de copy/fill e interpretación arquitectónica. G no recibe marcas, por lo que su diferencia tampoco estimaría utilidad multicomponente si aprendiera. No hay divergencias numéricas ni fallos de infraestructura; es fracaso del ensayo de capacidad bajo este presupuesto.

Respaldos: `runs/series_cli_exitfix/smoke/{results,diagnostics}.json`, cada manifest/curve/checkpoint local, `artifacts/gates/smoke.json`. El CLI impide el piloto con código2: `artifacts/pilot_gate_check.log`.

## Diagnóstico y próximos pasos

En veinte ejemplos de validación por modelo congelado, selección fija9911, mediana de gradiente respecto al bit de fuente≈2.9e−14–2.34e−13 frente a≈.013–.030 para un bit hipotético en el receptor. Invertir el primer bit de fuente cambia el logit en medianas≈1.1e−8–2.2e−8 y no cambia ninguna clase. Pesos conservados, sin optimización/test. `artifacts/diagnostics/xor_influence.json` conserva todos los casos y hash del script.

Esto apoya como **diagnóstico posthoc** una influencia remota muy atenuada, compatible con mala transmisión/condicionamiento. No demuestra su causa única ni constituye evidencia contra MHU. El siguiente paso permitido es el diagnóstico técnico centralizado/directo/local frente a remoto de `NEXT_EXPERIMENT.md`; todavía **NOT_RUN**. No aumentarT ni introducirGRU automáticamente, ni alterarv0.1 tras mirar resultados.

Bloqueos localizados adicionales: C3 población de parejas, puertos parciales, D4 ante anisotropía sistemática, posterior continuo singular con residuoexactamente cero, retiro pareado de cantidad impar y endpoint resource sin query. SPEC_AUDIT/MODEL_DATA_AUDIT describen alternativas; ninguna fue corregida silenciosamente.

AB inicial: `artifacts/AB_initial.json`; historial conservado `artifacts/report_current/AB_history.json`. H1–H6 permanecen.70,.35,.25,.75,.20,.30, marginales; C=.25. No se calculó posterior de arquitectura a partir de certificados, calibración, smoke o gradientes. Tablas/figuras actuales: `artifacts/report_current/`.

## Continuación del 8 de octubre de 2026

Se completaron series nuevas e independientes, documentadas en [LARP_CONTINUATION_RESEARCH_RESPONSE.md](C:/Programación/LARP/LARP_CONTINUATION_RESEARCH_RESPONSE.md). La mención anterior a NEXT_EXPERIMENT como NOT_RUN describe el estado histórico previo; ahora sus diagnósticos están ejecutados con resultados conservados.

- Capacidad: MLP y G con bits juntos aprenden XOR al100%; G con interfaces separadas queda al50% incluso a1–2hops. Target b0 e incremento×10 tampoco resuelven selección bajo el presupuesto.
- Minibatches por cuarteto mejoran aprendizaje parcial, sin superar.98. Cambian agrupamiento/orden y algunas exposiciones±1; la atribución exclusiva a balanceo está descartada.
- GRU compartida de referencia, +1.79% parámetros, alcanza train1.0/.9375 y validación.75/.75. Dos corridas completas;14 posteriores NOT_RUN. No se adopta como núcleo validado.
- Ablación exacta de coordenadas absolutas: mismo modelo y calendario, train100%/100%, validación87,5%/100%. Mejora ambas seeds pero no supera la puerta común. Se conserva el fallo y no se abre XOR/MHU/remoto.
- Control determinista especializado transporta los bits y resuelve512/512decisiones delpool. No es aprendizaje neuronal ni matching; denominadores remotos diminutos impiden inferir robustez interna.
- Generador aviar híbrido:3/3 certificados MHU finitos. Control con sólo términos locales:3/3 packing válido,0/3 MHU. Ninguna geometría aviar se usó en entrenamiento neuronal de esta continuación.
- Muestreo multicanal:144celdas completas. Avian ayuda a los interpoladores locales, pero su control sin espectro conserva casi toda la ventaja. Oracle-band:72celdas nuevas, reconstrucción smooth sin ruido exacta para todas; fine con ruido invierte el ranking y shuffle mejora ambas aviares.
- Grid balanceada original:3/3 admitidas,100.000 propuestas completas por seed;576celdas con consultas aligned/continuas y tres estimadores.216 previas reproducidas exactamente y360 adicionales. Avian gana decoders locales; Grid gana oracle fine con ruido. No se identifica mecanismo específicamente MHU.

Suite global final: **227PASS,9.07s**, logs en `artifacts/next_phase/tests_v2/`; se conserva la tanda anterior218PASS. Auditoría final:15manifests/122hashes congelados y27archivos científicos originales intactos. Se ejecutaron28 corridas técnicas nuevas/7.000updates. La identidad global ha cambiado por los módulos añadidos; las puertas originales permanecen como registros históricos y el piloto sigue cerrado. Test científico no abierto; H1–H6 y C sin actualizar. NoN1600/6400 ni CUDA.

Las decisiones y los estados de coordenadas/Grid están en [NEXT_PHASE_EXECUTION_SPEC.md](C:/Programación/LARP/docs/NEXT_PHASE_EXECUTION_SPEC.md). Sus secciones1/2 ya están ejecutadas; la comparación neuronal posterior sigue condicionada. Los certificados y los ensayos de sensores no autorizan confirmación de arquitectura.
