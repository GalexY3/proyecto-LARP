# Revisión adversarial de decisión — matching espectral v2

Fecha: 2026-10-09. Rol: arquitecto/revisor; derivación y recomendación prospectivas, sin búsqueda, controles nuevos, campos, scores ni entrenamiento. Gobernanza: [AB 2.1](../charter/LARP_RESEARCH_CHARTER_AB_2_1.md). Documentos históricos conservados: [protocolo original](../INDEPENDENT_SPECTRAL_MATCHING_NEXT.md) y [factibilidad v1](SPECTRAL_MATCHING_FEASIBILITY_DESIGN.md). Esta revisión no modifica sus condiciones ni reclasifica resultados antiguos.

## 1. Decisión y pregunta que queda abierta

**Recomiendo retirar v1 como próxima intervención y abrir un único ensayo prospectivo de factibilidad v2: media de los seis modos ≥0,25 en A–E, todas las restricciones locales originales y guardia de varianza toroidal continua de ±5% en R1,25/R2,5 para cada tipo.** La raíz del trabajo adoptó esta recomendación dentro de la autorización humana de continuar. El protocolo ejecutable debe congelar versión, hashes, semillas, presupuesto y métricas antes de la búsqueda. Esta revisión por sí sola no ejecuta esa fase.

El presupuesto acordado es **360 segundos globales**, incluyendo ≤60 segundos de calibración y seis inicios de ≤50 segundos, dos por referencia g1101/g1102/g1103. No ampliar a600 segundos. Si la calibración no permite al menos500 propuestas completas por intento bajo el cap conservador, cerrar por recursos antes de buscar. El límite global domina los individuales; no reasignar presupuesto para favorecer referencias difíciles o fáciles.

Cerrar únicamente v1 sería defendible si el objetivo fuese el efecto total de la supresión de fluctuaciones, para el cual esta guardia puede controlar una parte del mecanismo. Sin embargo, dejaría sin resolver una pregunta más estrecha y útil: **¿existe una reasignación funcional que altere apreciablemente la distribución espectral mientras preserva, aproximadamente, la cobertura y el segundo momento de los conteos a las escalas del decoder?** El ensayo v2 ofrece información sobre esa separabilidad con un coste máximo pequeño. No es una promesa de encontrar controles.

La denominación del estimando será **redistribución espectral de componentes a segundo momento local casi fijo, condicionada al mismo sustrato de unión**. Evitar «efecto puro de ondas largas», «destrucción de MHU» o «efecto total de MHU». La intervención no cambia X, E, radios físicos, conteos, puertos o el espectro de la unión.

## 2. Qué está probado y qué no

Para cada componente, con V=L²=400, seis modos no redundantes K y q como umbral de su media:

\[
\rho_c(n)=\sum_{i:t_i=c} e^{2\pi i n\cdot X_i/L},\quad
S_c(n)=|\rho_c(n)|^2/n_c,
\]

\[
\bar w_R(n)=\frac{\pi R^2}{V}\frac{2J_1(2\pi|n|R/L)}{2\pi|n|R/L},\qquad
v_{c,R}=n_c\sum_{n\ne0}S_c(n)|\bar w_R(n)|^2.
\]

Por no negatividad, incluidos los conjugados:

\[
v_{c,R}\ge 2n_c\sum_{n\in K}S_c(n)|\bar w_R(n)|^2
\ge \underbrace{12n_cq\min_{n\in K}|\bar w_R(n)|^2}_{L_{c,R}(q)}.
\]

La guardia nueva impone \(v'_{c,R}\le(1+\epsilon)v_{c,R}\), con \(\epsilon=.05\). Por tanto, cualquier q admisible debe satisfacer

\[
q\le q^{\rm necessary}_{\max,c,R}
=\frac{(1+\epsilon)v_{c,R}}{12n_c\min_{n\in K}|\bar w_R(n)|^2};\qquad
q\le \min_{c,R}q^{\rm necessary}_{\max,c,R}.
\]

Es un **techo necesario**, no el máximo realmente realizable bajo todas las restricciones. El límite puede ser menor por los modos restantes, acoplamiento entre clases, X fijo, vecindarios, histogramas, ventanas y limitaciones de los movimientos de búsqueda.

En R2,5, \(12\min|\bar w|^2=.015060447551436282\). La población A basta para excluir q=.50 con guardia±5%:

| Referencia | Varianza nativa A | Techo guardia1,05× | LB q=.25 | LB/nativa q=.25 | LB q=.50 | LB/nativa q=.50 | Techo necesario q |
|---|---:|---:|---:|---:|---:|---:|---:|
| g1101 | .830803 | .872343 | .613713 | .738699 | 1.227426 | 1.477398 | .355354 |
| g1102 | .875142 | .918899 | .613713 | .701273 | 1.227426 | 1.402546 | .374319 |
| g1103 | .850924 | .893471 | .613713 | .721231 | 1.227426 | 1.442462 | .363961 |

**q=.50+guardia queda matemáticamente excluido en estas tres referencias; no buscarlo.** B y C en R2,5 también exceden sus guardias. En R1,25 los techos necesarios quedan por encima de.25 y.50. **q=.25 no está excluido por esta cota; no se ha probado que exista un etiquetado admitido.** La cota excluye una condición sobre todo el conjunto de etiquetados, mientras el fracaso de seis recocidos excluiría únicamente éxito de esa búsqueda limitada.

El protocolo v1 sólo empareja CDF empíricas con tolerancia.02 en10.000 centros. Ese criterio no controla exactamente un segundo momento continuo: diferencias pequeñas en colas y entre centros usados/no usados pueden cambiarlo. Por ello, la prueba anterior **no demuestra imposibilidad de v1**. No introducir retroactivamente esta guardia en v1 ni reclasificarlo como un experimento que incluía varianza exacta.

Valores y verificación independiente: [cota de ventanas](../../artifacts/spectral_matching/window_spectral_bound_independent.json) y [presupuesto espectral independiente](../../artifacts/spectral_matching/independent_window_budget.json). La especialización al toro, la cota y su interpretación experimental son derivaciones propias del laboratorio.

## 3. La compensación fuera de banda es parte indispensable del estimando

Definir, sin truncar una suma Fourier infinita:

\[
B_{c,R}=2n_c\sum_{n\in K}S_c(n)|\bar w_R(n)|^2,\qquad
U_{c,R}=v_{c,R}-B_{c,R}\ge0.
\]

U es toda la contribución ponderada **fuera de los doce modos ±K**, calculada como diferencia entre varianza continua exacta y contribución exacta de esos modos. No equivale sólo a ondas cortas: contiene otros modos no incluidos en K. Si el control aumenta B mientras mantiene v casi fijo, necesariamente compensa reduciendo U:

\[
U'_{c,R}-U_{c,R}
\le .05v_{c,R}-[L_{c,R}(.25)-B_{c,R}].
\]

La auditoría independiente arroja, para A/R2,5:

| Referencia | B nativo | Reducción mínima obligada de U con q=.25 | Fracción del U nativo |
|---|---:|---:|---:|
| g1101 | .004427 | .567746 | 68,70% |
| g1102 | .010093 | .559863 | 64,72% |
| g1103 | .002061 | .569106 | 67,04% |

Esto es una exigencia considerable, aunque la cota más simple permita q=.25. La nueva guardia no convierte la manipulación en «banda6 cambió y todo lo demás quedó igual»: **fuerza una reorganización importante fuera de banda**. Una ventaja posterior podría depender del aumento en K, de la reducción fuera de K o de su interacción con el espectro de señal y el decoder. La fase de factibilidad debe registrar B/U nativos y candidatos por tipo y radio; no necesitan campos ni MSE.

Además, una media sobre seis modos permite concentrar potencia en algunos. Puede aumentar en (2,0)/(0,2) manteniendo baja la potencia en (1,0)/(0,1). Publicar los seis S, máximos y distribución por módulos de onda. No añadir ahora una exigencia por modo o elegir posteriormente qué shell se considera el tratamiento: sería otra versión. El contraste v2 deja de cumplir el certificado finito nativo, pero no clasifica el comportamiento asintótico del proceso.

## 4. Sobrecontrol: una restricción útil para una pregunta más estrecha

La varianza de conteos a R2,5 puede participar en el beneficio propuesto: disponibilidad local del canal, redundancia/vacíos y comportamiento de un interpolador con soporte2,5. Mantenerla casi fija elimina esa vía del contraste. Es sobrecontrol **si se pretende estimar el efecto total** de la organización MHU sobre adquisición. Es un control deliberado y defendible **si se pregunta por información adicional de la distribución espectral a estadísticas locales casi fijas**.

No denominarlo automáticamente un controlled direct effect de mediación. Las estadísticas son funciones deterministas del mismo etiquetado y no se ha definido una intervención independiente sobre el mediador; además, son matches dentro de tolerancias, no identidades completas. El estimando realizable es una comparación entre dos arreglos seleccionados por un protocolo geométrico congelado.

Un resultado nulo posterior, aun válido, sólo podría debilitar la utilidad **residual** bajo esas condiciones. No descartaría ventajas que actúan aumentando/reduciendo varianzas, alterando cobertura o combinando escalas. Un resultado positivo tampoco demostraría exclusividad causal de K, porque U debe cambiar y quedan fases, anisotropía, correlaciones y residuales locales no idénticos. La guardia reduce un confound claro; no produce una intervención espectral ortogonal.

El valor de v2 está en comprobar separabilidad y, si hay admisión, habilitar una comparación acotada con decoders fuertes. No hay ventaja informativa en prolongar indefinidamente un optimizador cuya región factible puede ser muy estrecha. Por eso se recomienda un ensayo único y corto, no una nueva campaña de generación.

## 5. Contrato prospectivo de v2

1. Referencias: las mismas tres aviares g1101/g1102/g1103, N400, L20, conteos `[163,85,68,50,34]`. X, orden, E, radios físicos y puertos inmutables. Las etiquetas viajan como funciones; los radios no viajan con ellas.
2. Conservación íntegra de admisión local v1: CDF/cuántiles de cobertura; CDF/vacío de ventanas R1,25/R2,5; NN homotípico con CDF/cuántiles/mínimo; todos los bins de parejas físicas≤2,5; 25 celdas de arcos dirigidos; outdegree por tipo. No cambiar tolerancias, denominadores, centros, bins o convenciones.
3. Guardia nueva, para **los diez pares tipo×radio**: `abs(v_candidate-v_native)/v_native <= .05`, usando varianza sobre centros uniformes continuos calculada por intersecciones de discos periódicos, float64. No estimarla mediante los10.000 centros ni mediante Fourier truncado. Todas las varianzas nativas son positivas.
4. Espectro: referencia conserva media≤.05 y máximo≤.10; candidato media≥.25 en cada uno de A–E para los mismos seis modos. Mantener concentración eta/T, espectros cruzados, unión invariante y checks numéricos. No seleccionar clases por facilidad.
5. Search prospectivo: seis inicios nativos, dos RNG congelados por referencia; misma familia de swaps y recocido v1. Sustituir únicamente el floor.50 por.25 y añadir los diez residuales normalizados de guardia al objetivo. El verificador completo, no el objective surrogate, decide admisión.
6. Cap antes de buscar: `min(5000, floor((50-reserva_certificado_y_escritura)/(2*max_coste_propuesta_calibrado)))`, contando la métrica completa con guardia. Si <500, no buscar y registrar límite de recursos. Techo global360s, calibración≤60s, sin ampliación. Un supervisor externo controla el árbol real.
7. Primer candidato admitido por referencia; parar los inicios posteriores de esa referencia. Conservar rechazos y mejores estados diagnósticos con todas sus violaciones. No convertir estados fallidos en controles de intensidad menor. Sin transferencia de presupuesto y sin nuevos seeds tras los fallos.
8. Registrar directamente v/B/U, cada S y residual, hashes, tiempos, cap e intentos no ejecutados. Recomputar certificado desde cero y auditarlo con implementación independiente. Este documento no autoriza escribir o evaluar campos, ejecutar decoders o entrenar.

Las tres referencias son materiales históricos reutilizados para explorar factibilidad. La elección de v2 nació mirando sus estadísticas; no presentarla como predicción confirmada por esos mismos datos. Guardar protocolos y artefactos v2 en rutas nuevas, sin sobrescribir v1 ni sus recibos.

## 6. Puertas y clasificación

| Resultado de fase v2 | Clasificación y acción |
|---|---|
| Falla identidad, métricas, hashes o supervisor | BUG/INVALID; corregir infraestructura dentro del alcance, no inferir nada sobre MHU. |
| Cap<500 o corte antes de búsqueda informativa | RESOURCE_LIMIT; cerrar este ensayo limitado sin ajustar tolerancias ni ampliar tiempo. |
| Agotamiento válido sin controles | SEARCH_EXHAUSTED/NOT_IDENTIFIED; conservar frente residual y cerrar la búsqueda v2. No es prueba de conjunto factible vacío. |
| Uno/dos controles | Factibilidad parcial; conservar todos, no sustituir referencias y no abrir evaluación de utilidad como si hubiera tres réplicas. |
| Tres controles, completos y auditados | Feasibility established for these references; congelar un protocolo posterior de campos/queries nuevos y decoders, antes de cualquier score. No equivale a superioridad MHU. |

El paso posterior, si se abre, deberá separar señales en K y fuera de K, ruido común, decoders locales y oracle-band fuerte. La compensación obligada exige observar interacciones de banda/decoder; una sola MSE agregada ocultaría el mecanismo. Estas decisiones no se implementan en esta fase. Para una futura afirmación confirmatoria usar nuevas realizaciones o declarar explícitamente la inferencia condicionada a estos tres sustratos seleccionados históricamente.

## 7. Registro AB y procedencia

- `belief_revision`: cambió la valoración de separabilidad/identificabilidad del diseño. q=.50 con la nueva guardia es imposible; v1 sin guardia no queda probado imposible. No hay actualización de utilidad MHU ni de priors arquitectónicos.
- `hypothesis_generation`: v2 y su estimando residual surgieron al inspeccionar referencias existentes. Son prospectivos para nuevas etiquetas, no confirmación independiente aportada por las mismas referencias.
- `objective_revision`: se acota temporalmente la pregunta a factibilidad de redistribución espectral con varianza local casi constante. La misión general de LARP no cambia.
- `decision`: retirar v1 como próxima intervención; una única factibilidad v2, q=.25/guardia±5%/360s, condicionada a calibración informativa. No scores ni entrenamientos en la autorización de esta ficha.

Literatura primaria reconsultada el2026-10-09 únicamente para apoyar la decisión metodológica: [Torquato y Stillinger, PRE2003, relación entre varianza local y representaciones real/Fourier](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.68.041113), **revisado por pares**; [PRX2021, momentos superiores y distribuciones de fluctuaciones](https://journals.aps.org/prx/abstract/10.1103/PhysRevX.11.021028), **revisado por pares**. El primero respalda que espectro y varianza no son factores independientes; el segundo respalda que el segundo momento no agota la información estructural. Ninguno demuestra existencia del control v2 ni utilidad neuronal de MHU. No se han usado patentes, preprints o resultados de rendimiento para justificar esta decisión. Las cotas, cifras finitas y recomendaciones anteriores son inferencias/derivaciones propias, con auditoría local separada.
