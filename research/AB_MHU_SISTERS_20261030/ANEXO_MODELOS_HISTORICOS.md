# Anexo — Revisión matemática de variantes históricas no reducidas a MHU/LOCAL/CVT

Este documento es una **auditoría documental complementaria**, no un ciclo AB adicional ni una ejecución del código histórico. Se revisaron archivos originales del repositorio privado `GalexY3/proyecto-LARP`, árbol `main`, `legacy/local_lab_20261022`, vía herramienta de GitHub. Se conservan las afirmaciones y condiciones del archivo sin reinterpretarlas como experimentos nuevos.

## H1. Geometría aviar con restricciones de exclusión / emparejamiento espectral

Referencias internas: `legacy/local_lab_20261022/LARP_SPECTRAL_FEASIBILITY_V2_RESULTS.md`; `docs/projects/SPECTRAL_MATCHING_V2_DECISION_REVIEW.md`; `docs/SPECTRAL_MATCHING_INDEPENDENT_METRIC_AUDIT.md`.

Situación real: tres geometrías g1101/g1102/g1103, **N=400, L=20, cuotas exactas [163,85,68,50,34]**. Las coordenadas, arcos, puertos y tamaños físicos por nodo quedan fijos; se pretendía cambiar etiquetas funcionales conservando 130 restricciones locales y una guarda de varianza de conteos de ventanas ±5% a R=1,25 y 2,5. En seis modos no redundantes K, cada tipo debería alcanzar media S≥0,25. Un umbral mayor q=0,50 se descartó prospectivamente por incompatibilidad matemática con la guarda.

El resultado histórico se basa en Parseval y no negatividad:

\[
 \operatorname{Var}(N_{c,R})=n_c\sum_{k\neq0}S_c(k)|\widehat{w_R}(k)|^2 \ge 12n_c q \min_{k\in K}|\widehat{w_R}(k)|^2.
\]

Para el tipo A y R=2,5: `12·min|w|²=.0150604475514` y `n_A=163`. Por ello, **si q=.50**, `Var≥.0150604475514×163×.5=1.227426...`, que supera incluso los máximos (1+5%) de las varianzas nativas: g1101 .872343; g1102 .918899; g1103 .893471. Los máximos NECESARIOS permisibles para q son aproximadamente .355354/.374319/.363961. Esto **no** prueba la existencia de controles con q=.25, ni demuestra que la CDF histórica igualada implicase igualdad de varianza continua.

Además, mantener casi fija la varianza mientras se eleva la energía de K obliga a reducir potencia ponderada del resto de modos: `ΔU≤.05 Var_native−(LB_K(q)−B_native)`. Para q=.25 se requieren reducciones históricas en el resto equivalentes a ~68,7%/64,7%/67,0% para tipo A a R2,5. No sería correcto llamar a ese contrafactual un cambio «exclusivamente de ondas largas».

**Estado:** el algoritmo histórico ejecutó 3012 propuestas en seis inicios, y ningún candidato superó todas las condiciones. Eso solo informa sobre aquel algoritmo/presupuesto; la imposibilidad q=.5 es matemática y distinta de la no-identificación de q=.25. No extrapolar a MHU asintótica, otros radios o otra parametrización.

## H2. Grafo de movilidad de etiquetas y ciclos de tres posiciones

Referencias: `legacy/local_lab_20261022/LARP_CONSTRAINED_MOBILITY_RESULTS.md`, `LARP_NATIVE_NEIGHBORHOOD_AND_TRADEOFF_RESULTS.md`.

Los grafos de exclusión por especie codifican restricciones necesarias para conservar separaciones mínimas. La revisión exhaustiva histórica de 136 candidatos filtrados por mínimos halló 95 movimientos que satisfacen las 130 guardas completas: 77 swaps y 18 ciclos orientados. Tres ciclos admitidos de g1101 no se podían descomponer en dos swaps admisibles directos desde nativa, pero esto **no prueba** que no existan caminos más largos. Esta es información específica del grafo de reconfiguración, no una demostración de más inteligencia o de una nueva especie matemática.

**Consecuencia de diseño:** el espacio admisible puede tener cuellos de botella combinatorios, y un optimizador local con propuestas uniformes puede no alcanzar un rival factible aunque este exista; la tasa de aceptación no es un estadístico suficiente de conectividad ni de optimalidad.

## H3. Constructores LOCAL–espectral y supuesta frontera Pareto

La optimización histórica desde etiquetas aleatorias, con 130 swaps y distintas prioridades entre cobertura C y energía W, no generó alternativas que no fueran dominadas por la nativa sobre los tres sustratos, pero **no fue una comparación de esfuerzo computacional emparejado**. El patrón nativo tuvo miles de pasos de optimización coadaptando X y marcas; el rival conservó X y cambió etiquetas con pocas propuestas. La “frontera” observada es un subconjunto de puntos alcanzados, no una frontera Pareto global. El teorema nuevo S18 de este lote solo vale para mínimos GLOBALES bajo el mismo dominio factible, no demuestra optimalidad del resultado nativo.

## H4. Familias neuronales recurrentes y currículos de roles

Referencias: `docs/GRU_BASELINE.md`, `docs/ROLE_GENERALIZATION.md`, `docs/PHASE_3_ROLE_COVERAGE.md`.

- **GGNN-like con GRU:** es otro modelo neuronal, con 1,794% más parámetros que el control nominal; el experimento Grid-local-b0 finalizó con validación .75/.75 y detuvo las ramas MHU/XOR/remoto como NO EJECUTADAS. No es una evaluación de MHU.
- **COORDS_OFF:** elimina coordenadas absolutas, pero conserva distancias de aristas; dos semillas mejoraron validación pero falló la puerta conjunta definida por anticipado. No demuestra invariancia a TODA geometría.
- **BALANCED frente a UNIFORM:** el currículo balanceado resolvió la tarea b0 con ambas semillas en el panel primario mientras el uniforme no. La matriz no identificó el balance de roles aisladamente, porque también variaron otros aspectos del conjunto de entrenamiento; no es un efecto comparado de MHU.

No utilizar esos resultados para afirmar que una distribución MHU supera a una arquitectura recurrente. Se necesita diseño factorial geometría × currículo × mensajes × presupuesto.

## H5. Multicapa, atención y superposición de expertos

Fuente: `docs/projects/MHU_MULTILAYER_REVIEW.md`. Las variantes propuestas **NO se ejecutaron**: (a) planos MHU apilados con interconexiones; (b) máscaras geométricas por cabeza de atención; (c) transformer denso con coordenadas MHU. Las garantías de un plano no certifican hiperuniformidad 3D; duplicar planos duplica nodos salvo control explícito. Si la red ignora por completo posiciones, distancias, máscaras y marcas, las coordenadas MHU NO afectan a la función computada. Si sí las usa, la ganancia puede proceder del routing y debe compararse con GraphGPS, Exphormer y BigBird con la misma información/recursos. Sin resultado ejecutado, queda como propuesta AB-P/AB-R futura, no hallazgo.

## H6. Qué falta para estudiar «las hermanas» exhaustivamente

Se ha dado un fundamento matemático específico a LOCAL/MHUv1/v2, CVT, retícula, IID, subconjuntos marcados, desplazamientos, grafos y gradientes de objetivos. Pero el archivo muestra otras decisiones arquitectónicas (**conectividad, currículo, filtros, dimensiones, semántica de etiquetas**) que no son especies geométricas alternativas certificadas. No existe todavía una comparación integral y científicamente válida de todas las combinaciones. El siguiente trabajo razonable no es inventar un ranking universal, sino seleccionar un estimando concreto y un control adversarial con todos los factores relevantes.

**Clasificación:** AUDITORÍA DOCUMENTAL POSTERIOR a S01–S20, fuera del cupo y sin otorgar nuevos grados N1/2/3.