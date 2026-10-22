# LARP: factibilidad espectral v2 y límites del contraste

9 de octubre de 2026. **Fase cerrada: NOT_IDENTIFIED.** Se ejecutaron los seis inicios fijados, 502 propuestas por inicio, 3.012 propuestas en total. Ningún control superó todas las condiciones. Calibración, preparación y búsqueda consumieron **126,728 s** dentro del máximo global de 360 s. No se calcularon scores de adquisición, tareas o redes; no se reabrió XOR ni se actualizaron H1–H6/C/H-R1–H-R4.

El resultado relevante tiene dos partes: una obstrucción matemática de un contraste demasiado fuerte con varianza local controlada, y una búsqueda limitada cuyo algoritmo apenas se desplazó. La primera permite una exclusión precisa; la segunda no permite declarar vacío el conjunto factible.

## 1. Qué se investigó realmente

Tres geometrías aviares completas históricas g1101/g1102/g1103, N400/L20 y conteos [163,85,68,50,34]. Coordenadas, arcos kNN dirigidos, centros de matching y radios físicos por nodo permanecieron fijos. Las etiquetas representan funciones, sin transportar el radio celular. No se manipuló el espectro de la unión ni se construyeron tres geometrías nuevas.

La propuesta anterior permanece intacta y NOT_RUN. Antes de buscar etiquetas, la revisión algebraica justificó un protocolo nuevo: todos los componentes debían alcanzar media S≥0,25 en los mismos seis modos; conservar las tolerancias de cobertura, ventanas, NN homotípicos, pares físicos y mezcla dirigida; y mantener la varianza continua de conteos dentro de ±5% de la nativa en R1,25/R2,5. El cambio se decidió sin rendimiento ni búsqueda de controles, en [la decisión prospectiva](docs/decisions/ADR_2026_10_09_SPECTRAL_LOCAL_VARIANCE_V2.md). El objetivo de utilidad MHU permaneció abierto.

La varianza se calculó mediante intersecciones de discos sobre todos los pares del tipo, con centro uniforme continuo en el toro; no mediante una estimación sobre los 10.000 centros de matching. Estos últimos se usaron para CDF y cuantiles, con el namespace original. Todas las guardas se exigieron conjuntamente, sin seleccionar un tipo favorable.

## 2. El hallazgo matemático

Sea K el conjunto de seis modos no redundantes, n_c el número de sensores de un tipo, V=L² y q el suelo de su media espectral. Para un disco de radio R,

\[
\bar w_R(n)=\frac{\pi R^2}{V}\frac{2J_1(2\pi|n|R/L)}{2\pi|n|R/L},\qquad
v_{c,R}=n_c\sum_{n\ne0} S_c(n)|\bar w_R(n)|^2.
\]

La no negatividad y los conjugados dan una condición necesaria:

\[
v_{c,R}\ge12n_cq\min_{n\in K}|\bar w_R(n)|^2.
\]

Para A/R2,5, q=0,50 impone varianza≥1,227426. Las nativas son 0,830803/0,875142/0,850924: un incremento mínimo de 40–48%. Por tanto, q=0,50 **con la nueva guarda±5%** es imposible en los tres sustratos. No se gastó búsqueda en esa combinación.

| Referencia | Varianza A/R2,5 nativa | Máximo permitido±5% | Cota q=.25 | Cota q=.50 | Techo q necesario |
|---|---:|---:|---:|---:|---:|
| g1101 | .830803 | .872343 | .613713 | 1.227426 | .355354 |
| g1102 | .875142 | .918899 | .613713 | 1.227426 | .374319 |
| g1103 | .850924 | .893471 | .613713 | 1.227426 | .363961 |

No se probó imposible la propuesta anterior con CDF empírica≤.02: las colas pueden cambiar segundos momentos y los centros muestreados no equivalen a la medida uniforme continua. Tampoco se probó factible q=.25; sólo que esta cota no lo excluye.

![Cota necesaria de varianza frente al contraste espectral; las bandas representan límites de admisión, no intervalos de confianza](artifacts/spectral_matching/variance_spectral_bound.png)

[Figura vectorial](artifacts/spectral_matching/variance_spectral_bound.svg). El gráfico muestra la cota para A/R2,5; no representa una simulación de controles construidos.

Hay otra consecuencia causal: si el aumento de la contribución de K supera el margen permitido de varianza total, **debe decrecer la contribución fuera de K**. En concreto, esto se exige cuando ΔB_K>0,05·v_nativa. En A/R2,5, q=.25 y guarda±5% obligan a reducir al menos alrededor de 65–69% de la contribución nativa restante. El estimando v2 es redistribución espectral a segundo momento local casi fijo. No sería correcto atribuir una futura mejora exclusivamente a los seis modos, ni llamarla efecto total de MHU. La media de seis modos tampoco exige que todos suban ni clasifica el límite k→0.

La relación entre espectro y varianza de ventanas es anterior a LARP: [Torquato y Stillinger, PRE 2003](https://doi.org/10.1103/PhysRevE.68.041113), revisado por pares. La necesidad de considerar distribuciones y momentos superiores está desarrollada en [Torquato, Kim y Klatt, PRX 2021](https://doi.org/10.1103/PhysRevX.11.021028), revisado por pares. Las cotas finitas, cifras y evaluación del diseño son derivaciones propias verificadas localmente; no se reclama novedad del principio de Parseval. [Verificación independiente](artifacts/spectral_matching/window_spectral_bound_independent.json) y [presupuesto espectral](artifacts/spectral_matching/independent_window_budget.json).

## 3. Ejecución registrada y resultado

Veinte mediciones geométricas descartadas fijaron el cap antes de buscar. Máximo coste observado por propuesta: 0,0488032 s; reserva de certificado/escritura: 1 s. La fórmula congelada resolvió 502 propuestas/start, apenas por encima del mínimo operativo 500. No se repitió calibración para elevarlo. El mínimo es una regla de eficiencia, no una potencia estadística.

Los seis starts comenzaron de etiquetas nativas con RNG distintos. Los swaps conservaron conteos. La admisión exigía 130 restricciones locales, certificado nativo y media espectral≥.25 de cada tipo; el objetivo de búsqueda nunca sustituyó a esas guardas. Se conservaron estados y movimientos diagnósticos sin convertirlos en controles de menor intensidad.

| Referencia/start | Propuestas | Swaps aceptados | Menor media S en el mejor diagnóstico | Matching local completo | Tiempo del inicio |
|---|---:|---:|---:|---|---:|
| g1101/0 | 502 | 3 | .001617 | PASS | 16,736 s |
| g1101/1 | 502 | 2 | .001011 | PASS | 18,256 s |
| g1102/0 | 502 | 2 | .001742 | PASS | 18,688 s |
| g1102/1 | 502 | 1 | .001742 | PASS | 18,698 s |
| g1103/0 | 502 | 2 | .000997 | PASS | 20,051 s |
| g1103/1 | 502 | 5 | .001229 | PASS | 18,391 s |

Los mejores diagnósticos conservaron las guardas locales, pero quedaron muy lejos del objetivo espectral. La mayor media de cualquier componente en ellos fue aproximadamente .00508, también muy por debajo de .25. Ninguno es un control admitido. Los casos individuales, no sólo este resumen, están en [la cápsula de búsqueda](artifacts/spectral_matching/v2/search/results.json).

Calibración: 6,009 s; preparación: 7,828 s; búsqueda: 112,892 s. Los seis inicios terminaron por cap de propuestas, con todos los checkpoints finales y sin corte del supervisor, reintentos o transferencia de presupuesto. Desarrollar/auditar software y verificar estados se contabilizó aparte. Las interrupciones por créditos ocurrieron antes de la ejecución y no fabricaron réplicas científicas.

## 4. Por qué repetir el recocido tiene poco valor

Sólo se aceptaron 15 swaps de 3.012 propuestas, aproximadamente 0,50%. Eso describe movilidad pobre del buscador; no mide utilidad de MHU ni demuestra imposibilidad geométrica.

El objetivo preregistrado fue

\[
J=100\sum_j[(r_j/\tau_j-1)_+]^2+
\sum_c[(1-\bar S_c/.25)_+]^2,
\]

con temperatura máxima 0,10. El término espectral está entre0 y 5. Desde un estado que pasa las guardas locales, una sola discrepancia de 3 en un conteo cuya tolerancia es 2 produce coste local ≥25. El incremento de energía es entonces ≥20 y la probabilidad Metropolis de cruzarlo es ≤exp(−200), aproximadamente1,4×10⁻⁸⁷. Esta es una propiedad matemática del **algoritmo**, no un likelihood de la teoría ni una probabilidad de éxito experimental.

Varias restricciones de bins/arcos tienen tolerancia2. Para esas barreras, este recocido opera prácticamente como búsqueda dentro de la región local admisible. No conocemos si esa región conecta con controles útiles mediante swaps de dos nodos. El resultado no identifica qué guarda bloqueó cada propuesta; el historial no contiene el diagnóstico completo de cada rechazo. El bajo movimiento y la barrera justifican cambiar la pregunta de búsqueda, no aumentar el tiempo del mismo método esperando un resultado favorable.

## 5. Auditoría y actualización AB

La suite completa pasó 274 tests. La implementación coincidió con 59 comprobaciones independientes por sustrato; los 20 estados de calibración fueron auditados; y los seis mejores estados finales se reconstruyeron con fórmulas independientes, sin repetir búsqueda. [Auditoría final](artifacts/spectral_matching/final_independent_metric_audit.json): PASS de integridad, resultado NOT_IDENTIFIED. Conserva 435 archivos científicos/de gobernanza anteriores y los 391 hashes históricos originales. No se abrieron scores de utilidad ni modelos neuronales. Otro agente escribió las fórmulas y el comparador independientes; el agente principal ejecutó el cierre final. Esa independencia corresponde a la implementación de métricas, no a un laboratorio o réplica experimental independiente.

- **belief_revision:** el contraste .50+guarda queda excluido en estas referencias. La estrategia registrada no produjo controles; esta conclusión acota el algoritmo y presupuesto. H1–H6/C/H-R1–H-R4 permanecen intactos.
- **hypothesis_generation:** H-MOVE1 propone que movimientos compensados entre varios sitios puedan mejorar la conectividad/movilidad de la región admisible frente a un swap. Nace mirando estos resultados; necesita una comparación nueva para validarse. H-SF2 no obtuvo construcción positiva bajo el método registrado.
- **objective_revision:** no cambia la misión de LARP; se mantiene explícito el estimando residual y la diferencia respecto del efecto total MHU.
- **decision:** cerrar v2 sin relajar tolerancias ni añadir propuestas. No abrir comparación de adquisición sin controles. No escalar N ni arquitectura para resolver este bloqueo de identificación.

## 6. Siguiente prueba recomendada

Antes de otro generador o red, comparar **movilidad bajo restricciones**: swaps de dos sitios frente a ciclos compensados de tres, con conteos y radios conservados, nuevas semillas, coste igualado y referencias declaradas. Medir admisibilidad local y qué familias de restricciones rechazan cada propuesta; todavía sin tareas, decoders o objetivo de rendimiento. El propósito sería distinguir un cuello de botella del movimiento de una falta de solapamiento entre tratamientos.

Si ambos movimientos apenas tienen movilidad, priorizar cotas/relajaciones del espacio factible y revisar cuáles restricciones corresponden al estimando. La mezcla de tipos de arco es pertinente para una red que usa E; un decoder de adquisición que no usa E plantea otro contraste. Cualquier separación entre esas líneas requiere otro protocolo explícito, conservando éste. No retirar guardas por observar un fallo ni presentar un control nuevo como equivalente al anterior.

La exploración 3D y la atención dispersa conservan sus propuestas previas; no se ejecutaron en esta fase. Este bloqueo de identificación ofrece mayor prioridad informativa que apilar capas o aumentar N6400. El laboratorio obtuvo un límite concreto y una explicación del bajo movimiento, sin producir evidencia favorable o desfavorable sobre utilidad neuronal MHU.
