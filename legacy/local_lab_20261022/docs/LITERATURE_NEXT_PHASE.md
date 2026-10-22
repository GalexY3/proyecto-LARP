# Literatura y decisiones para la siguiente fase

Fecha de consulta: 2026-10-08. Alcance: diagnóstico y nueva exploración, sin modificar retrospectivamente v0.1. Este documento propone experimentos; **no contiene resultados nuevos de entrenamiento**. Las cifras previas proceden de `IMPLEMENTATION_STATUS.md` y `NEXT_EXPERIMENT.md`. No autoriza actualizar los priors de arquitectura con diagnósticos técnicos.

## Decisión principal

La primera prioridad es separar **capacidad local, transmisión efectiva y generalización de roles**. Después, evaluar una candidata aviar reproducible. Cambiar simultáneamente recurrencia, geometría y entrenamiento permitiría conseguir una red que aprenda, pero impediría saber qué resolvió el fallo y qué aporta MHU.

La búsqueda aporta dos cambios importantes: un modelo retiniano de 2020 más próximo a la geometría deseada que la mera penalización espectral, y una distinción reciente entre pérdida de sensibilidad remota y saturación de memoria. Ninguno demuestra que una distribución aviar mejore computación neuronal.

## Qué significa el fallo actual

Los cuatro ensayos XOR originales rondan el azar, aunque todas las fuentes tienen caminos de ≤16 hops. Su gradiente fuente→logit es aproximadamente 1e−13, frente a 1e−2 para un bit hipotético en el receptor. Esto demuestra influencia diferencial muy débil en esos ejemplos y checkpoints; no demuestra que el problema sea exclusivamente topológico, ni que el bloque aprenda XOR cuando recibe los bits localmente.

**Sensibilidad y capacidad son problemas distintos.** gLSTM separa recuperación de múltiples elementos almacenados de insensibilidad a perturbaciones remotas. XOR de dos bits a distancia, en un estado de 32 dimensiones, es inicialmente un ensayo de transporte/integración, no una buena prueba de saturación de memoria. No recomiendo aumentar anchura, adoptar memoria matricial ni llamar al fracaso «capacidad insuficiente» antes del control local. [gLSTM, ICLR 2026](https://openreview.net/pdf?id=c4mXEOXlAL).

**Accesibilidad no es transmisión.** La teoría de Di Giovanni y colaboradores relaciona insensibilidad con dinámica, anchura y topología; añadir capas no garantiza recuperar información. Sus resultados sobre tiempos de commute no se transfieren literalmente al kNN dirigido, no reversible, con LayerNorm, activaciones y entrada persistente de LARP. Usar esos resultados como motivación y medir el operador real. [ICML 2023](https://proceedings.mlr.press/v202/di-giovanni23a.html).

**Oversmoothing requiere una medición diferente.** Si los estados se homogeneizan, deberían disminuir diferencias entre nodos, energía de Dirichlet y rango efectivo. Un Jacobiano remoto diminuto puede aparecer sin homogeneización: no permite diagnosticarla. El preprint de Park y Kim estudia problemas de gradientes en GNN residuales, incluido crecimiento en determinadas direcciones; su propuesta de normalización no está validada para este núcleo. [Preprint, 2024](https://arxiv.org/abs/2410.04824).

**Inferencia propia sobre la recurrencia lenta.** En la caricatura lineal `h[t+1]=(I+αP)h[t]`, con P una media de vecinos, un camino que requiere d transmisiones participa con potencias α^d, multiplicidades de caminos y combinaciones temporales. Para α=.1 y d≈9, el skip puede conservar muy bien información local y aun trasladar poca información remota en T16. El bloque real añade transformaciones, normalización y u persistente: esta explicación es una hipótesis, no una cota demostrada ni la causa establecida. Medir gradiente por distancia, respuesta a flips de ambos bits, normas de estado y saturación permite refutarla.

Finalmente, GLoRa encontró fallos de dependencias largas que sus experimentos no atribuían a las tres explicaciones habituales. Su noción de dependencia incluye información distribuida a lo largo de un camino, diferente de consultar dos endpoints. Adoptar su advertencia metodológica: un diagnóstico de gradiente no sustituye la prueba de aprendizaje de la función. [GLoRa, ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/e779d5a98058b5c9f3df9059a3137647-Paper-Conference.pdf).

## Intervenciones recomendadas, en orden

Cada fila es una serie técnica nueva, con semillas/datos/manifests congelados, sin test primario ni evidencia AB. Mantener todas las corridas, incluidas las fallidas. El diagnóstico existente de cinco minutos tiene prioridad; la autorización para continuar permite ejecutarlo, no declarar superado el gate original con otra tarea.

| Observación previa | Intervención mínima | Qué aisla | Confound / criterio de parada |
|---|---|---|---|
| Aún no sabemos si aprende XOR directo | MLP centralizado y bloque G con ambos bits en receptor, tal como `NEXT_EXPERIMENT.md` | Pipeline y capacidad local sin transporte | Éxito con cuatro patrones no acredita generalización de puertos. Si falla localmente, detener cambios de grafo. |
| Aprende localmente, falla remoto | Comparar α=.1 contra α=1, mismo T16, mean, grafo y parámetros; reentrenar ambas condiciones desde estados comunes | Intensidad de actualización/condicionamiento del núcleo | Cambia la dinámica completa, incluida rama local; vigilar normas, gradientes y divergencia. Mejor gradiente sin ≥.98 no abre piloto. |
| α=1 mejora gradiente pero sigue sin aprender | Diagnóstico de **copy de un solo bit**, luego XOR, con exactamente las mismas fuentes y destinos | Transporte de una señal frente a interacción no lineal de dos señales | Copy se puede resolver por una fuente; XOR exige dependencia causal de ambas mediante flips contrafactuales. |
| Copy remoto falla; local aprende | En una serie posterior, α fijo y factor único ganancia de mensajes β=1 frente a β=√6 antes del bloque de actualización | Dilución por media sin añadir parámetros | No cambiar simultáneamente α/β. El aumento puede saturar o desestabilizar; sum no es neutral y cambia escala. |
| Sensibilidad mejora, pero roles/puertos siguen sin generalizar | Baseline recurrente GRU compartido sobre el mismo E, entrada y readout; mismo rango de datos | Si el update original es el cuello de botella práctico | Es baseline/versión nueva, no reparación cosmética; declarar P/MAC/RSS y presupuesto. No atribuir mejora a MHU. |
| Falla transporte con núcleos competentes | Intercambiar un 10% de arcos por atajos aleatorios manteniendo exactamente E=6N e in-degree6, sin usar labels/targets | Necesidad de rutas frente a dinámica local | Cambia distancias físicas y longitudes de cable; registrar ambos costes. Es contraste de arquitectura completa. |

Para el factor α, registrar gradientes antes y después de entrenar, con consultas fijadas previamente, en float64 como diagnóstico cuando float32 redondee flips. Una propagación lineal congelada sobre el mismo E es un control barato de difusión; no se presenta como red neuronal exitosa. No barrer 20 hiperparámetros hasta hallar una seed favorable. Si dos modificaciones mínimas consecutivas no resuelven transporte, pasar a un baseline competente y dejar de optimizar el bloque nominal.

GRU compartido tiene antecedente claro en Gated Graph Sequence Neural Networks. Es un control de ingeniería razonable después de conocer el fallo local/remoto, no una consecuencia de la biología. [ICLR 2016](https://arxiv.org/abs/1511.05493).

## La candidata aviar: qué copiar y qué no

Jiao et al. observaron patrones de cinco poblaciones de conos de gallina y propusieron un modelo de empaquetamiento multiescala con repulsiones. El resultado concierne organización y muestreo espacial; no prueba inteligencia, transporte de mensajes, memoria ni robustez de una GNN. Una ilustración parecida tampoco reproduce un mosaico empírico. [PRE, 2014](https://arxiv.org/abs/1402.6058).

**Prior art más próximo para el generador:** Lomba et al. modelan una mezcla ternaria equimolar de discos no aditivos con repulsión logarítmica entre partículas del mismo tipo. Su objetivo separa desorden, supresión de fluctuaciones y heterocoordinación local. Por tanto, repulsión homotípica de corto alcance no basta para reclamar el mecanismo multihiperuniforme de ese modelo. Extenderlo a cinco tipos desiguales sería una adaptación propia, no una reproducción publicada. [PRE, 2020](https://arxiv.org/abs/2005.01558).

Recomendación concreta: conservar el generador aviar inspirado de cinco tipos como candidato operativo y compararlo con el nominal; usar el modelo de Lomba como referencia mecanística y eventual control reducido ternario. Certificar por tipo y unión; además informar `g_ab(r)`, vecino homotípico más próximo, varianza de áreas Voronoi, vacíos por componente, anisotropía y espectros de concentración. Separar **cumple certificado finito**, **tiene exclusión/heterocoordinación aviar** y **se ajusta a una retina empírica**; sólo las dos primeras son defendibles sin datos retinianos originales.

No ajustar radios/repulsiones mirando accuracy. Una relajación de empaquetamiento que impida el certificado debe quedar como candidata fallida o una clase distinta, conservando el registro. La MHU nominal espectral puede ser más extrema en los pocos modos anulados que el mosaico natural: «más parecido» y «más hiperuniforme» son objetivos diferentes.

## Cómo explorar utilidad MHU sin confundir muestreo y transporte

**Tres estimandos separados:** efecto del sustrato completo (X+E+puertos), efecto de distribuir funciones sobre el mismo X/E, y efecto de adquirir señales mediante sensores de diferentes tipos. El contraste aviar contra nominal estima el primero; native contra shuffle con T/F estima el segundo. G no recibe marcas, de modo que no puede establecer ventaja funcional multicomponente.

La exploración inicial más informativa de la intuición aviar es un **ensayo de cobertura multicanal sin entrenamiento**: cinco campos suaves independientes con fases/amplitudes aleatorias, mismos conteos, cada tipo observa sólo su canal, queries uniformes y métricas de error de interpolación y vacíos. Usar un estimador idéntico fijado antes, bandas de frecuencia declaradas y controles HU-unión con marcas shuffle, grid con reparto equilibrado y patrón con exclusión local similar. Esta es una propuesta propia para identificar observabilidad; no es el dataset copy actual ni demuestra superioridad de computación interna.

Después, una tarea aprendida debe conservar esos mundos y un target externo independiente de las marcas, y separar adquisición de procesamiento: entrenar tanto con sensores distribuidos como con una observación común igualada. Una ventaja presente sólo cuando cambian las señales adquiridas indica muestreo/cobertura. Una ventaja que persiste con observaciones iguales podría justificar investigar organización de funciones o transporte. Esta rama requiere nuevo encoder/protocolo y no debe abrirse automáticamente por aprobar XOR.

Medir identidad funcional efectiva: similitud de adapters, uso por tipo y sensibilidad a suprimir un tipo. Si todos los adapters se vuelven casi iguales, una cobertura multihiperuniforme de «funciones» puede no existir. Un resultado nulo en una tarea que nunca demanda funciones distintas no refuta una hipótesis fuerte sobre distribución de especialistas; tampoco la respalda.

## Baselines y extensiones que merecen presupuesto

Mantener grid y HU-unión como rivales centrales, con el mismo núcleo competente. Añadir un GRU compartido sobre el mismo grafo como control del update. Un modelo que reúne explícitamente los inputs es un techo técnico y cambia comunicación, por lo que su coste y estimando son distintos.

SWAN ofrece un control publicado de dinámica no disipativa; no garantiza resolver XOR ni mantiene automáticamente el matching de LARP. Reservarlo para cuando falle transporte con los cambios simples. [AAAI 2025](https://ojs.aaai.org/index.php/AAAI/article/view/33858). La sparsificación que preserva espectro motiva controles de rewiring con costes declarados; el espectro de Laplaciano del grafo es diferente del factor de estructura del patrón de puntos. No confundir ambos «espectros». [ICML 2025](https://proceedings.mlr.press/v267/liang25a.html).

GHR combina recurrencia con un grafo agrupado y entradas persistentes: es una ruta potencial si el objetivo futuro requiere distancias crecientes. La versión v2 del 1 de octubre de 2026 modifica el texto y sigue sin publicación revisada verificada en esta consulta. Introduce rutas, normalización y supervisión intermedia; copiar el paquete entero destruiría la ablación actual. En fases posteriores, exigir controles recurrentes planos, mismo presupuesto y extrapolación por hops. [Preprint v2, 2026](https://arxiv.org/html/2605.18387v2).

La solicitud IBM ya contempla redes HU dispersas y conectividad derivada de geometría. Es prior art cercano, pero sus ejemplos no son una replicación independiente ni validan MHU recurrente. La contribución defendible de LARP seguirá siendo una ventaja multicomponente atribuida causalmente, si aparece. [Solicitud publicada US20240202508A1, 2024](https://patents.google.com/patent/US20240202508A1/en).

**Regla final recomendada:** continuar cuando haya un núcleo que aprenda y una comparación que realmente demande el mecanismo; pivotar hacia muestreo si la ganancia procede sólo de observabilidad; parar la afirmación arquitectónica si native/shuffle y HU/grid fuertes producen un nulo preciso. El umbral .98 puede ser alcanzable mediante otra dinámica, pero la literatura no lo garantiza y no autoriza rebajarlo.

## Registro de evidencia

Once fuentes primarias, con enlaces próximos a las afirmaciones. Revisadas por pares: Jiao2014, Lomba2020, Li2016, DiGiovanni2023, GLoRa2025, SWAN2025, Liang2025 y gLSTM2026; gLSTM se verificó mediante texto de conferencia indexado y posteriormente mediante sus [actas oficiales ICLR2026](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c70bc769d6171ef8bb76e36e8d458205-Abstract-Conference.html). OpenReview devolvió una comprobación de navegador al abrir una ruta PDF; eso limita ese acceso, no la verificación de publicación. Preprints con aceptación no verificada: Park2024 y GHR2026v2. Patente: IBM2024. El inventario JSON conserva fuente, versión, estado, alcance y límite de transferencia. No se encontró una implementación neuronal multihiperuniforme equivalente en esta búsqueda dirigida; esa ausencia no certifica novedad.
