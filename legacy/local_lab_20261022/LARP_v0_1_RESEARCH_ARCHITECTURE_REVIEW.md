# LARP v0.1 — revisión científica y contrato experimental

Especificación autoritativa: **LARP_ASTRA_ARCHITECTURE_REVIEW_v2.md**, leída íntegramente. Fecha de esta revisión y corte de búsqueda: **8 de octubre de 2026**. Implementador previsto: **SOL 6.1 UltraCode**. Estado: diseño previo a resultados; ninguna cifra de rendimiento de LARP en este documento es un resultado observado. Los umbrales numéricos son decisiones de preregistro, no constantes universales.

## A. Executive verdict

**LARP es técnicamente coherente y merece un experimento pequeño, condicionado a validar primero el tratamiento geométrico.** Su hipótesis defendible es estrecha: una distribución de tipos que reduce fluctuaciones de abundancia a escalas útiles podría beneficiar computación que realmente necesita funciones diferentes distribuidas por el dominio. La retina proporciona un ejemplo geométrico y una motivación; no demuestra esa utilidad neuronal.

La principal debilidad conceptual es equiparar cinco marcas con cinco recursos funcionales. Una red con cinco embeddings puede ignorarlos, utilizarlos como códigos de posición o aprender cinco funciones redundantes. Incluso una ventaja de MHU-T podría deberse a correlaciones locales entre tipos, exposición de entradas, optimización o longitud de caminos. Ninguno de esos resultados identifica automáticamente la supresión de «desiertos funcionales».

El experimento decisivo comienza con **los mismos puntos, las mismas aristas y la misma interfaz**, cambiando únicamente la asignación espacial de tipos y reentrenando. La comparación entre geometrías completas es necesaria para utilidad práctica, pero identifica un paquete de cambios. MHU-G observa únicamente la unión de puntos: no puede detectar multihiperuniformidad de marcas ocultas. Permutar esas marcas debe dejar sus predicciones idénticas.

Recomiendo **400 nodos, estado de 32 dimensiones, seis mensajes entrantes por nodo y 16 pasos recurrentes compartidos**, en un toro 2D de lado 20. Las proporciones empíricas verificadas serán la condición nominal; una condición equiproporcional es obligatoria. La escala propuesta de 4096 nodos queda para después: no es necesaria para identificar el primer efecto y perjudica la información por unidad de cómputo. La geometría se verificará además a 1600 y 6400 puntos sin entrenar redes de ese tamaño.

El núcleo usa geometría congelada, agregación media y un bloque recurrente sencillo. La versión funcional utiliza cinco adaptadores de rango 2; su control homogéneo utiliza un adaptador de rango 10, con exactamente el mismo número de parámetros. Esto iguala presupuesto, aunque deja diferencias de rango activo y coste que deben declararse. Grid, HU-union IBM-inspired, random-regular, small-world y Poisson son controles reales; Poisson no será el adversario principal.

Las primeras tareas serán XOR remoto como comprobación, copia direccionada de ocho bits entre cinco fuentes, y flood fill de ocho iteraciones sobre un mundo lógico independiente del sustrato. El tercer problema no se redefine según el grafo de cada arquitectura. Se separarán dos preguntas: rendimiento a igual cómputo y efecto de distribución de tipos. Lesiones y escalado se aplicarán después a modelos ya entrenados, con hipótesis y endpoints fijados.

**La decisión de continuar exige un efecto práctico replicado o una intervención de mecanismo convincente.** Un buen resultado de XOR, una figura visualmente uniforme, una patente o una mejora contra Poisson no justifican v0.2. Un nulo preciso frente a HU fuerte y etiquetas redistribuidas debilitaría esta implementación de MHU. No refutaría toda combinación futura imaginable, pero sí impediría sostener una ventaja general sin nueva hipótesis.

## B. Corrections

1. **La evidencia biológica es finita y específica.** Jiao et al. caracterizan mosaicos de pollo y presentan un modelo; no hay una prueba asintótica experimental para todas las aves. Kram et al. documentan variación por cuadrante. Adoptaremos la inspiración como estructura estadística, no como reconstrucción de retina. [Jiao et al., PRE 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC5836809/), [Kram et al., PLoS ONE 2010](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0008992).
2. **Las proporciones sí están verificadas:** doble cono 40,7%; verde 21,1%; rojo 17,1%; azul 12,6%; violeta 8,5%. Son proporciones del muestreo citado, no una ley biológica universal. Un doble cono es una unidad formada por dos células; no se duplicará automáticamente su número de nodos. El orden A–E sólo conserva esas frecuencias. No asignaremos color, movimiento u otra función retiniana a operaciones artificiales.
3. **Unión HU no implica componentes HU.** El etiquetado aleatorio de una unión HU introduce fluctuaciones de composición. La comparación más barata y limpia es conservar esa unión y destruir la regularidad de las marcas. A la inversa, si todas las amplitudes de componentes se anulan a baja frecuencia, la de la unión también se anula: los requisitos no son independientes.
4. **MHU-G no identifica el efecto multicomponente.** Cualquier efecto suyo procede de la geometría no marcada y del grafo resultante. Debe describirse como «unión generada mediante restricciones MHU», no como evidencia de utilidad funcional de cinco clases.
5. **T y F no son categorías de expresividad disjuntas.** Un MLP compartido condicionado por identidad puede aproximar funciones diferentes. F impone una factorización y un reparto explícitos. El contraste estudia parametrización y aprendizaje, además de heterogeneidad.
6. **Hiperuniformidad no certifica cobertura local.** Suprimir modos de longitud de onda grande no garantiza vecinos próximos de cada tipo ni tolerancia a lesiones. Mediremos radios relevantes para la propagación efectiva; una tarea que sólo usa vecinos inmediatos puede no experimentar el tratamiento.
7. **Ni blue noise ni Poisson-disk ni Lloyd son certificados MHU.** El generador tendrá una función objetivo explícita y un certificado finito. La apariencia y una distribución estrecha de distancias no sustituyen `S(k)` y varianza de conteos.
8. **kNN no controla todo el grado.** Seis vecinos entrantes controlan aristas e in-degree; out-degree, reciprocidad, conectividad, longitudes y espectro siguen cambiando. Mutual-kNN pierde incluso ese control y puede desconectar el grafo.
9. **Delaunay no es evidencia de conectividad sináptica retiniana.** Es una elección de grafo geométrico reproducible. Su grado medio cercano a seis en el toro permite una comparación ecológica económica, pero no elimina diferencias de grado.
10. **Un presupuesto común no garantiza dificultad común.** Si una fuente queda fuera del campo receptivo de T pasos, fallar es obligatorio. Se registrará accesibilidad antes de interpretar errores como incapacidad de razonamiento.
11. **Lesiones de radio fijo pueden eliminar cantidades distintas.** El análisis primario igualará nodos removidos; el radio fijo será secundario. Perder la entrada correcta y fallar no mide resiliencia de cómputo.
12. **Escalar N sin escalar el dominio prueba otra cosa.** Mantendremos densidad uno: L aumenta como raíz de N. Densificar el mismo dominio se deja como factor posterior separado.
13. **Permutar identidades sólo en evaluación es una intervención fuera de distribución.** Es diagnóstico de dependencia, no estimación limpia de ventaja de cobertura. El contraste causal requiere reentrenar. Renombrar coherentemente clases y parámetros debe ser una simetría exacta.
14. **H1–H6 pueden coexistir.** Sus probabilidades serán marginales subjetivas, no un reparto que sume uno. Routing puede dominar mientras cobertura ayuda bajo daño y MHU inicializa bien.
15. **Prior art cercano reduce la novedad defendible.** HU neuronal ya aparece en IBM; recurrencia local, robustez y extrapolación de pasos aparecen en NCA. La posible contribución de LARP sería un efecto multicomponente identificado, no inventar redes espaciales o computación emergente.
16. **No prometer tiempos sin medir la máquina.** Doy fórmulas y límites operativos. Se calibra el tiempo de 200 actualizaciones antes del piloto; si falla el límite, se reduce conjuntamente el presupuesto y se registra una nueva versión de protocolo.

## C. Prior-art map

Las fuentes de esta tabla son primarias: publicaciones, registros editoriales, manuscritos de autores o solicitud de patente. «Fuerte» significa que respalda la afirmación citada dentro de su ámbito; no significa validación de LARP. La búsqueda dirigida no halló una reproducción neuronal multihiperuniforme recurrente equivalente al diseño propuesto; esto no certifica novedad.

| Concepto | Trabajo más próximo | Fuerza y estatus | Relevancia | Brecha que permanece |
|---|---|---|---|---|
| Mosaicos aviares y frecuencias | [Kram et al., 2010](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0008992) | Datos primarios; PLoS ONE, revisado | Cinco mosaicos y proporciones verificadas | Transferencia a recursos computacionales |
| Multihiperuniformidad aviar | [Jiao et al., 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC5836809/) | PRE, revisado; estadísticas y modelo | Antecedente directo del patrón | Utilidad neuronal y causalidad |
| Definición y fluctuaciones | [Torquato y Stillinger, 2003](https://doi.org/10.1103/PhysRevE.68.041113) | PRE, revisado; teoría | Relaciona estructura y conteos | Certificar asintótica desde N pequeño |
| Generación por coordenadas colectivas | [Torquato et al., PRX 2015](https://arxiv.org/abs/1503.06436), [PRR 2023](https://doi.org/10.1103/PhysRevResearch.5.033190) | Publicaciones revisadas | Optimización espectral y degeneración de configuraciones | Muestreo multicomponente controlado |
| Generador MHU multicomponente | [Christogeorgos et al., 2024](https://doi.org/10.1051/epjam/2024003) | EPJ Applied Metamaterials, revisado | Optimización con restricciones de no solapamiento | No demuestra mejora neuronal |
| Puntos HU convertidos en grafos | [Newby et al., JCN 2025](https://doi.org/10.1093/comnet/cnaf040), [PRE 2025](https://doi.org/10.1103/PhysRevE.111.034123) | Revisados | Delaunay/Voronoi no trasladan trivialmente todas las estadísticas | HU de vértices no certifica HU de conectividad |
| MHU con funciones distintas por componente | [Keeney et al., 2026](https://doi.org/10.1002/adom.202503139) | Advanced Optical Materials; publicación revisada, online 27/06/2026 | Materiales ópticos inspirados en retina; antecedente aplicado cercano | Función óptica no equivale a cómputo aprendido |
| HU/NHU neuronal | [IBM US20240202508A1](https://patents.google.com/patent/US20240202508A1/en) | Solicitud publicada 20/06/2024; patente, evidencia independiente débil | HU como diseño neuronal disperso; Delaunay y organización espacial | No valida cinco componentes ni recurrencia LARP |
| Marco message passing | [Gilmer et al., ICML 2017](https://proceedings.mlr.press/v70/gilmer17a.html) | Revisado | Mensaje/agregación/update ya establecidos | Qué geometría favorece la tarea |
| Inferencia iterativa compartida | [Palm et al., NeurIPS 2018](https://papers.nips.cc/paper/7597-recurrent-relational-networks.pdf) | Revisado | Razonamiento relacional recurrente | MHU frente a grafos fuertes |
| NCA y reparación | [Mordvintsev et al., Distill 2020](https://distill.pub/2020/growing-ca/) | Artículo científico con revisión y discusión editorial | Estado local compartido y regeneración | Reparación depende del entrenamiento |
| NCA para razonamiento reciente | [Etcheverry et al., 28/09/2026](https://arxiv.org/abs/2609.36126) | Preprint v1, sin revisión verificada | Maze, Sudoku, ARC y extrapolación; baseline conceptual muy próximo | Reproducibilidad y contribución de geometría |
| Benchmark algorítmico | [CLRS, ICML 2022](https://proceedings.mlr.press/v162/velickovic22a.html), [repositorio oficial](https://github.com/google-deepmind/clrs) | Revisado y software primario | Referencia posterior para generalización | Interfaz espacial diferente |
| Bottlenecks de GNN | [Alon y Yahav, ICLR 2021](https://arxiv.org/abs/2006.05205) | Revisado | Over-squashing como explicación rival | La normalización no elimina el cuello de botella |
| Small-world y topología neuronal | [You et al., ICML 2020](https://proceedings.mlr.press/v119/you20b.html), [Xie et al., ICCV 2019](https://openaccess.thecvf.com/content_ICCV_2019/papers/Xie_Exploring_Randomly_Wired_Neural_Networks_for_Image_Recognition_ICCV_2019_paper.pdf) | Revisados | Conectividad aleatoria estructurada puede ser fuerte | Correlaciones no son ley causal universal |
| Recurrencia espacial | [Achterberg et al., NMI 2023](https://www.nature.com/articles/s42256-023-00748-9) | Revisado | Coste de cableado y comunicación producen estructura | Separar estos mecanismos de HU |
| Geometría, wiring y función | [Shakiba et al., 12/06/2026](https://arxiv.org/abs/2606.14975) | Preprint | Inductive biases corticales combinados | Cambios conjuntos confunden atribución |
| Conectividad dispersa aprendida | [RigL, ICML 2020](https://proceedings.mlr.press/v119/evci20a.html) | Revisado | Baseline necesario al reclamar ventajas de topología fija | Adaptación cuesta cómputo adicional |
| Optimizar posiciones | [Erb et al., Living Machines 2025](https://doi.org/10.1007/978-3-032-07448-5_23) | Capítulo de conferencia; cita editorial 2026 | Parametrización mediante posiciones aprendidas | No prueba MHU ni tareas algorítmicas |
| Especialización funcional | [Béna y Goodman, Nat. Commun. 2025](https://www.nature.com/articles/s41467-024-55188-9) | Revisado | Modularidad no garantiza especialización | Exigir intervención funcional específica |
| Estados de aristas | [Battaglia et al., 2018](https://arxiv.org/abs/1806.01261), [EB-GNN, ICML 2026](https://proceedings.mlr.press/v306/barcelo26a.html) | Primero preprint de marco; segundo revisado | Edge updates y mensajes aristas/triángulos | Ganancia independiente de MHU |
| Hypergraphs y complejos | [HGNN, AAAI 2019](https://arxiv.org/abs/1809.09401), [MPSN, ICML 2021](https://proceedings.mlr.press/v139/bodnar21a.html) | Publicaciones revisadas | Relaciones múltiples y simpliciales | Cambian dominio y expressividad |
| Inferencia comparativa | [Benavoli et al., JMLR 2017](https://www.jmlr.org/papers/v18/16-305.html), [Agarwal et al., NeurIPS 2021](https://arxiv.org/abs/2108.13264) | Revisados | ROPE, incertidumbre y pocas semillas | No suministran likelihood de H1–H6 |

**Consecuencia arquitectónica del prior art:** el grid recurrente será un rival central y recibirá exactamente la misma política de entrenamiento. No se atribuirá a MHU un beneficio que en realidad provenga de replay, entrenamiento con daños, recurrencia o pasos adicionales. Estas técnicas se excluyen inicialmente del núcleo; si se necesitan para aprender, se incorporarán a todas las condiciones bajo un nuevo preregistro.

## D. Competing hypotheses + priors

Defino los priors como probabilidades subjetivas de que el mecanismo produzca un efecto relevante en **alguna condición del dominio preregistrado**, no de que sea cierto en toda tarea posible. Son marginales y pueden sumar más de uno. Las probabilidades de H5 se actualizarán sólo cuando se ejecute plasticidad. Las cifras evitan tanto certeza nula como entusiasmo biológico.

| Hipótesis | Mecanismo y prior | Evidencia esperada | Evidencia que la perjudica |
|---|---|---|---|
| H1: suficiencia de estructura genérica | `P=0,70`. Localidad, cobertura total, grado y entrenamiento explican la mayor parte de diferencias | G-MHU equivalente a HU; T/F nativas equivalentes a redistribuidas; grid fuerte | Ventaja nativa replicada con puntos/aristas constantes y control de mixing local |
| H2: cobertura bajo perturbación | `P=0,35`. Redundancia espacial de clases útiles reduce déficits tras daño o reubicación | Diferencia pequeña en limpio y mejora de AUC de daño; menor cola de déficit funcional | Lesión igualada elimina ventaja; mejora sólo por perder menos puertos; no cambia mediador |
| H3: heterogeneidad distribuida | `P=0,25`. Funciones distintas deben reencontrarse durante integración recurrente | Interacción marcas×T/F; especialización intervenible; ganancia desaparece al alterar cobertura con mixing preservado | G mejora igual; tipos redundantes; ventaja persiste tras colapsar funciones; efecto explicado por pares locales |
| H4: dominancia de transporte global | `P=0,75`. Accesibilidad y menor compresión de señales dominan routing | SW/RR mejores a T fijo; gap se reduce con más T o shortcuts; sensibilidad remota mayor | MHU mejora con distancia/hops igualados sin mayor accesibilidad |
| H5: buena inicialización | `P=0,20`. Estado inicial regular facilita optimización, aunque otra topología convenga al final | MHU aprende antes; plasticidad iguala rendimiento final manteniendo ventaja de muestras | Warm starts cruzados muestran que sólo importa topología final o pesos heredados |
| H6: restricción perjudicial | `P=0,30`. Distribuir clases dificulta módulos, hubs o especialización local útil | Etiquetas agrupadas o wiring modular mejoran tareas; MHU pierde con intervalo preciso | MHU gana cuando la tarea necesita heterogeneidad y cuando admite clustering |

Preregister también dos proposiciones cuantitativas separadas: **A**, diferencia media de score nativa–shuffle superior a 0,02; **C**, una intervención de cobertura altera rendimiento mediante funciones no redundantes. Para A uso un prior de efecto `\mu\sim\mathcal N(0,0,05^2)`; por simetría no da ventaja previa a MHU. Para C uso `P(C)=0,25`. Que A aumente mientras C disminuye será un resultado permitido.

H3 es la apuesta científicamente más interesante, pero no la más probable. Un escenario plausible es que tipos libremente entrenables acaben siendo intercambiables: dispersarlos con cuidado entonces aporta poco. La condición de recursos artificialmente restringidos que se define más adelante comprueba sensibilidad del ensayo, no convierte H3 en cierta para redes libres.

## E. Architecture Decision Record — LARP v0.1

| Campo | Decisión fijada |
|---|---|
| N de entrenamiento | **400**. N=1600 para inferencia de escala; N=6400 sólo para validación geométrica |
| Espacio | 2D, toro cuadrado; L=20 para N400, L=40 para N1600, L=80 para N6400; densidad total 1 |
| Clases A–E | Pesos enteros [407,211,171,126,85]/1000; Hamilton con desempate A→E |
| Conteos N400 | **[163,85,68,50,34]**, equivalentes a [40,75;21,25;17;12,5;8,5]% |
| Conteos N1600 / N6400 | [651,338,274,201,136] / [2605,1351,1094,806,544] |
| Ablación frecuencias | [80,80,80,80,80] en N400; clases sin semántica biológica |
| Generador | Minimización de amplitudes Fourier por componente y unión, más repulsión corta común; detalle abajo |
| Grafo causal | **kNN dirigido de seis vecinos entrantes**, distancia periódica, sin autoaristas ni simetrización; E=2400 |
| Grafo ecológico | Delaunay periódico no dirigido, convertido a dos arcos; aproximadamente E=2400 en configuraciones genéricas |
| Estado y bloque | d=32; mensaje 32→32 con distancia escalar; update 100→64→32 |
| Agregación | Media sobre vecinos vivos; cero si no hay vecinos |
| Recurrencia | 16 pasos síncronos, pesos ligados, geometría y aristas congeladas |
| Entrada | 25 canales; encoder lineal 25→32; estado inicial igual al encoder; entrada persistente reintegrada en update |
| Salida | MLP compartido 32→32→o, o=1 para XOR/fill y o=8 para copy; sólo puertos designados |
| Normalización | Un LayerNorm de 32 canales compartido, afín, epsilon 1e−5; sólo estado antes de mensaje/update |
| Activación | tanh en mensajes/adaptadores; SiLU en update/readout |
| Residual | h siguiente = h + 0,1 × incremento; coeficiente fijo |
| Parámetros | G: 12.261 para o1, 12.492 para o8. T/F: 12.277 para o1, 12.508 para o8 |
| Entrenamiento | AdamW, lr piloto 0,003; betas (0,9;0,999), eps 1e−8; weight decay 1e−4; clipping global 1 |
| Precisión | float64 geometría; float32 red; sin AMP ni dropout en piloto |
| Software | Python, PyTorch, NumPy, SciPy, Matplotlib; NetworkX sólo estadísticas pequeñas. PyG no requerido |
| Memoria esperada | B4/T16/N400: orden 0,1–0,5 GB de tensores de entrenamiento; proceso objetivo <2 GB; medir RSS y pico de dispositivo |
| Cómputo esperado | Orden 4,2 millones de MAC por ejemplo/paso; unos 67 millones por forward T16, más backward |

**La dimensionalidad espacial 2 no guarda relación con d=32.** Elegir 3D cambiaría cobertura, volumen accesible y aristas al mismo tiempo, encareciendo la primera identificación. Una superficie plana es suficiente para probar la hipótesis geométrica inspirada en retina; no es un modelo de circuitería retiniana. No habrá condición 3D en v0.1.

### Generación reproducible

El patrón se llamará **MHU finito con supresión espectral de banda baja**, sin afirmar que reproduce el exponente de la retina. El método de coordenadas colectivas permite controlar directamente amplitudes; el objetivo multicomponente y la repulsión que fijamos son una adaptación propia. No se presentará como reproducción exacta del modelo de Jiao ni del generador de antenas. [Generación por coordenadas colectivas](https://doi.org/10.1103/PhysRevResearch.5.033190), [generación multicomponente](https://doi.org/10.1051/epjam/2024003).

1. Generar N coordenadas uniformes independientes en [0,L)² y asignar exactamente los conteos Hamilton mediante permutación independiente. El seed identifica posiciones y marcas iniciales; no se ordenan tipos espacialmente.
2. Optimizar coordenadas conservando las marcas. Usar todos los vectores enteros no nulos con norma ≤L/10 y conservar un representante de cada pareja ±n: n_x>0, o n_x=0 y n_y>0. El cutoff físico es K=2π/10. Para N400 son seis modos: (1,0), (0,1), (1,1), (1,−1), (2,0), (0,2).
3. Minimizar el objetivo de F: promedio de S por componente, S de la unión y repulsión entre cualquier pareja a distancia <0,30. La normalización por N evita que el término corto crezca como N². No hay repulsor diferente por clase ni tamaño biológico distinto: serían confounds adicionales.
4. Adam para geometría: 6000 pasos, lr coseno desde 0,025 hasta 0,0001, betas (0,9;0,999), sin weight decay; luego L-BFGS con memoria 20, búsqueda strong-Wolfe, máximo 250 iteraciones/1000 evaluaciones, tolerancia de gradiente 1e−8 y cambio 1e−12. Todas las coordenadas se envuelven módulo L al evaluar.
5. Las parejas de repulsión se recalculan **en cada evaluación** con cKDTree periódico; el gradiente deriva de las distancias de las parejas activas. El término y su primera derivada se anulan en el cutoff: no congelar una lista de vecinos que deje entrar colisiones. Guardar también energía, norma de gradiente y número de parejas.
6. Hasta cuatro reinicios por seed geométrico, derivados con SeedSequence. Elegir el **primer patrón que pasa** los criterios siguientes, nunca el de mejor rendimiento de tarea. Registrar todos los intentos y fracasos. Si ninguno pasa, el seed se marca fallido y se detiene la batería científica.
7. Guardar posiciones float64, marcas, vectores k, certificado, parámetros del generador, seed, hash y versión. El entrenamiento carga esos ficheros inmutables. El coste de generar y verificar geometrías se reporta aparte y amortizado.

Con 34 puntos de la clase minoritaria hay 66 grados de libertad posicionales tras quitar traslación y 12 restricciones reales Fourier. Esto permite intentar el tratamiento sin cristalizarlo por construcción, pero deja muy pocos modos para establecer comportamiento asintótico. Para N1600/6400 se conserva K físico, aumentando el número de modos. No reducir el cutoff al ampliar L: produciría una familia de tratamientos distinta.

### Certificado finito y condición de admisión

Todos los umbrales siguientes se aplican antes de conocer rendimiento. Deben cumplirse **para A–E y la unión**.

- **Espectro:** media de S en modos optimizados ≤0,05; máximo ≤0,10. Guardar los seis valores individuales en N400. No sustituirlos por S(0), que es trivialmente fijo.
- **Conteos:** 10.000 centros uniformes compartidos entre condiciones; discos periódicos de radios R={0,5;1;2;3;4;5}. Para cada conjunto a, dividir su varianza por N_a p_R(1−p_R), p_R=πR²/L². El promedio del cociente en R4 y R5 debe ser ≤0,65. No usar R cercano al tamaño del toro, donde fijar N fuerza varianza pequeña artificialmente.
- **Separación:** distancia mínima de la unión ≥0,299; sin duplicados. Este umbral es higiene numérica, no evidencia HU.
- **Desorden:** en modos no optimizados con 2<norma(n)≤10 para N400, máximo S_a/N_a<0,50. Rechaza concentraciones de tipo cristalino muy intensas; no certifica ausencia de orden. La misma regla usa K<|k|≤π a tamaños mayores.
- **Isotropía:** calcular cuadrupolo angular normalizado del espectro no optimizado, ponderado por S, sobre K<|k|≤π. Módulo >0,30 activa una bandera descriptiva. No se excluye automáticamente una clase con sólo 34 puntos por esa cifra ruidosa. Comparar el ensemble con 200 controles aleatorios, publicar orientaciones y órdenes q4/q6; una anisotropía sistemática se convierte en confound y exige control D4.

El rebote de S inmediatamente fuera de la banda se **mide y publica**, no se exige que también sea pequeño. Un patrón stealthy puede tenerlo; exigir bajo S en todo holdout impondría otra geometría. Se muestran espectros direccionales además de promedio radial, varianza completa, g₂ homotípica/heterotípica, CDF de vecinos cercanos, área de Voronoi y seisfold local. Estas métricas describen efectos colaterales del generador.

La cobertura de tipos requiere otra medición: fracción de ventanas sin cada clase, percentiles 50/90/95 de distancia al tipo más cercano y tamaño de ventanas deficitarias. Se miden en R1,2,4,5 y en bolas de 1,2,4,8 hops. **Pasar el certificado geométrico no garantiza mejorar estas métricas en la escala que usa la red.**

Validación entre tamaños: tres seeds nuevos por N en {400,1600,6400}, sin entrenamiento. Reportar cocientes y fallos por seed, y la estabilidad de la supresión a igual k físico/R. Si N400 pasa pero al aumentar N la construcción pierde supresión, no se inferirá una familia HU escalable. Si los criterios de admisión bloquean >25% de seeds, revisar el generador y preregistrar v0.1b; no seleccionar una población silenciosamente distinta.

### Conectividad y coste

El kNN causal es dirigido: j→i cuando j está entre los seis más próximos a i. Desempate por hash de IDs, independiente de clase y de etiqueta objetivo. Es una decisión deliberada para fijar exactamente E=6N. No se afirma controlar out-degree. No se añaden puentes cuando el grafo se desconecta: conectividad es parte del resultado. Se publican SCC, out-degree, reciprocidad y accesibilidad de puertos.

Delaunay ecológico se calcula sobre nueve copias periódicas. Conservar triángulos cuyo circuncentro está en [0,L)², extraer sus tres aristas, deduplicar por IDs originales y comprobar traslación. Arcos bidireccionales, sin autoaristas. Si un circunradio conservado alcanza L/2, repetir con 5×5 copias y verificar invariancia; si persiste ambigüedad, registrar fallo. En el toro genérico una triangulación cumple E_no_dirigido=3N; medirlo y no forzarlo podando. La degeneración del grid se resuelve con su vecindad nativa, no con una diagonal elegida para favorecerlo.

Mutual-kNN, Gabriel, relative-neighborhood y radio con cap quedan excluidos inicialmente: cambian simultáneamente edge count y conectividad sin aportar una intervención más clara que el control de marcas. Un grafo de radio fijo será un diagnóstico secundario sólo si el efecto causal parece depender de radios largos de kNN.

Aplicar W_m una sola vez por nodo y expandir después a aristas. Cachear u durante el rollout. Así el coste recurrente es O(TB[Nd²+Ed]), no O(TBEd²). El adaptador F ejecuta 128 MAC por nodo frente a 640 en T/G: se reportan costes activos aunque su presupuesto de parámetros sea igual. A N400, B4 y T16, 1000 updates suman aproximadamente 0,8×10¹² MAC de entrenamiento usando backward≈2×forward, una estimación de orden, no un cronómetro.

Calibrar 200 updates de copy con B4 y cuatro threads CPU; excluir calentamiento, incluir forward/backward/optimizer, registrar mediana y percentil 90. Objetivo: una ejecución piloto completa ≤30 min. Si tarda más, fijar para **todas** las condiciones B4 y 500 updates en lugar de 1000 y declarar protocolo de presupuesto reducido antes de abrir test. Si aún supera 30 min, ejecutar sólo certificado, smoke y dos contrastes focales; la comparación amplia queda pendiente y no se declara ausencia de ventaja. El coste confirma la viabilidad, no decide qué arquitectura conservar.

## F. Mathematical specification

Para posiciones $x_i$, la distancia y el desplazamiento usan imagen mínima:

$$
\delta_{ij}=x_j-x_i-L\,\mathrm{round}((x_j-x_i)/L),\qquad r_{ij}=\|\delta_{ij}\|_2.
$$

Para el conjunto $a$, componente o unión:

$$
A_a(k)=\sum_{i\in a}e^{\,\mathrm i k\cdot x_i},\quad
S_a(k)=\frac{|A_a(k)|^2}{N_a},\quad
\mathcal E=\overline S_\cup+\frac15\sum_{c=1}^5\overline S_c+
\frac{10}{N}\sum_{i<j}\left[\max(0,1-r_{ij}/0.30)\right]^2.
$$

La barra promedia los modos no redundantes fijados en E. $A_\cup=\sum_c A_c$: comprobar esta identidad y el límite $S_\cup\leq\sum_c S_c$ numéricamente.

El encoder, normalización, mensaje y agregación son:

$$
u_i=W_x x_i^{\mathrm{in}}+b_x,\qquad h_i^0=u_i,\qquad
z_i^t=\operatorname{LN}(h_i^t),
$$
$$
v_{ji}^t=\tanh\left(W_m z_j^t+w_r\log(1+r_{ij})+b_m\right),\qquad
m_i^t=\frac{1}{|N_{\mathrm{alive}}(i)|}\sum_{j\in N_{\mathrm{alive}}(i)}v_{ji}^t.
$$

Si el denominador es cero, $m_i^t=0$. La distancia se mide en unidades de densidad uno, no dividida por L; así conserva significado físico al escalar. No entran dirección, pares de clases ni gates en el mensaje inicial. La posición de los puertos sí entra en el encoder para especificar el mundo lógico.

$$
a_i^t=\operatorname{SiLU}\!\left(W_1[z_i^t;m_i^t;u_i;q_i]+b_1\right),
\qquad
f_i^t=W_2 a_i^t+b_2+\mathcal A_i(z_i^t),
$$
$$
\mathcal A_i(z)=r_i^{-1/2}U_i\tanh(V_i z),\qquad
h_i^{t+1}=h_i^t+0.1 f_i^t,\qquad t=0,\ldots,15,
$$
$$
\ell_p=W_o\,\operatorname{SiLU}(W_hh_{\pi(p)}^{16}+b_h)+b_o,
\qquad \widehat y_p=\operatorname{sigmoid}(\ell_p).
$$

$\pi$ es la asignación puerto→neurona. $W_1$ recibe 100 canales y produce 64; $W_2$ produce 32. $U_i\in\mathbb R^{32\times r_i}$ y $V_i\in\mathbb R^{r_i\times32}$. Los parámetros son compartidos entre tiempos. No se introduce pooling global, token central, readout de todas las fuentes ni mezcla entre ejemplos.

Todos los Linear principales se inicializan Xavier-uniform gain 1, bias cero; LN gamma uno/beta cero. Embeddings T/F normales de desviación 0,02, centrados entre las cinco filas; q de G inicial cero. Factores U/V normales independientes con desviación $1/\sqrt{32}$, sin biases. El factor $r^{-1/2}$ aproxima igual escala inicial entre rangos; reportar norma inicial y no ajustarla según resultados. Derivar streams por nombre de módulo: los pesos compartidos empiezan idénticos entre familias y controles a igual training seed; el orden de construcción no debe desplazar el RNG.

Pérdida XOR/copy: BCEWithLogits media sobre bits del puerto de salida. Fill: promedio de BCE sobre celdas, con peso de clase positivo calculado una vez sobre train y recortado a [1,5]. La máscara de puerto sirve para selección y pérdida; no transmite la etiqueta.

## G. MHU-G / MHU-T / MHU-F

**G:** q_i es un único vector entrenable de cuatro entradas, idéntico para todos. U/V son un único adaptador compartido de rango 10. Las marcas almacenadas sólo se usan en certificados geométricos y en metadatos; nunca en la ejecución neuronal. Posiciones, entradas y grafo son el único vehículo geométrico.

**T:** q_i es la fila c_i de una tabla 5×4. Todos los W y el adaptador de rango 10 siguen compartidos. No hay encoder ni head específico de tipo. La tabla puede inducir funciones diferentes mediante el update, pero no las presupone. Remota selección de fuente A–E no significa clase A–E: esos IDs se generan independientemente.

**F:** q_i usa la misma tabla 5×4 que T; sustituir el adaptador único por cinco adaptadores de rango 2, seleccionados estáticamente por c_i. Todos los W principales continúan compartidos. No hay router aprendido ni capacity factor de MoE. Sólo se ejecuta el adaptador seleccionado y se contabiliza su coste.

El conteo exacto por tarea con o logits es:

$$
P_{\mathrm{base}}=832+1088+8544+64+1056+33o=11584+33o,
$$
$$
P_G=P_{\mathrm{base}}+4+640=12228+33o,\qquad
P_T=P_F=P_{\mathrm{base}}+20+640=12244+33o.
$$

Los 640 parámetros del adaptador se reparten como $2dr$: rango10 compartido o cinco rangos2. **T y F están exactamente parameter-matched**, sin parámetros ficticios congelados. G tiene 16 parámetros menos, diferencia de 0,13%; esto afecta el contraste G–T, pero no ningún contraste geométrico dentro de familia. No cambiar d ni readout para ocultar esa diferencia.

Hay dos confounds residuales de F–T: menor rango activo por clase y menor trabajo por nodo de F. Reportar ambos. Un F ganador sería evidencia a favor del reparto explícito con este presupuesto; un F perdedor podría reflejar rango2 insuficiente. Si el efecto F–T decide continuación, v0.2 incluirá control compartido rango2 y heterogéneo rango10, evaluados como curvas rendimiento–parámetros–MAC, no como reemplazo post hoc del matching.

No interpretar la distancia entre embeddings como especialización. En un lote de diagnóstico fijo se calcularán las funciones contrafactuales de cada tipo en los mismos estados, sus Jacobianos y sus contribuciones al loss. Esos lotes no se usan para entrenamiento ni elección de hiperparámetros. Saturación o una norma grande pueden separar embeddings sin crear funciones útiles.

## H. Baselines

Todos los baselines neuronales del régimen causal utilizan el bloque G/T/F anterior, los mismos 25 canales, puertos y presupuesto. Labels aleatorias mantienen conteos exactos. El nombre del baseline indica geometría/grafo; la familia funcional se declara aparte.

**B1 Grid:** 20×20 puntos $(a+0,5,b+0,5)$ en L20. Causal: seis vecinos entrantes más próximos, con desempate por hash. Ecológico: cuatro vecinos cardinales bidireccionales, E=1600 arcos. Para T/F habrá marcas aleatorias y una condición fuerte de marcas balanceadas por intercambios en puntos fijos. Su energía es la media de los cinco S de componente en los modos de E; 100.000 propuestas de intercambio entre clases distintas, Metropolis, temperatura logarítmica 0,1→0,0001, diez reinicios. Elegir el primero que satisface criterios espectrales/de conteos de componente; si ninguno pasa, guardar el de menor energía como «Grid balanceada aproximada», publicando residuos y sin llamarlo MHU certificado. En proporciones iguales, usar directamente $c=(a+2b)\bmod5$: cinco subretículas regulares. La condición balanceada merece tanto protagonismo como HU: si iguala MHU, la explicación es disponibilidad regular, no desorden.

**B2 HU-union / IBM-inspired:** mismo objetivo y repulsor de E, retirando términos por componente; mismo seed inicial y presupuesto. Exigir el certificado sólo de unión. Marcas posteriores aleatorias con conteos exactos. Causal: kNN6. Ecológico: Delaunay periódico. Se reproduce la idea HU más sparse geometry-derived connectivity, **no la arquitectura completa IBM**. La solicitud US20240202508A1 describe, entre otras opciones, redes feedforward, estructuras materiales, superficies/anillos y conectividad Delaunay; no aporta un protocolo equivalente al nuestro. Su ejemplo no valida multicomponente recurrente. [Solicitud IBM](https://patents.google.com/patent/US20240202508A1/en).

**B3 Random-regular:** grafo simple no dirigido 6-regular, generado por seed, convertido en dos arcos por arista; E=2400. Ubicar vértices en los mismos puntos MHU para conservar interfaz física en el contraste de routing. Marcas shuffle. Aceptar el primer grafo conectado entre un máximo de 20 intentos, sin evaluar tareas. Si no hay uno, registrar fallo. Causal aquí significa efecto del wiring completo, no sólo geometría; sus longitudes largas son precisamente el factor experimental.

**B4 Small-world:** causal sobre posiciones Grid y kNN6: cada slot entrante se redirige con probabilidad 0,10 a un origen uniforme sin autoarista ni duplicado; mantiene E=2400 e in-degree6, pero cambia out-degree. Ecológico: cuatro cardinales de Grid más dos orígenes remotos entrantes por nodo, con distancia física ≥L/4, sin duplicados; E=2400. Ambas versiones conservan parámetros y T. No se dará un encoder más poderoso al baseline global. RR y SW permiten probar H4 con un bloque idéntico, sin introducir atención.

**B5 Poisson:** N uniformes independientes en el toro; no repulsión ni optimización. Causal kNN6, ecológico Delaunay. Se registra separación mínima y desconexión. Sirve para detectar efectos de regularidad genérica y cobertura total; ganar sólo a B5 no constituye evidencia suficiente.

**Control crítico MHU-shuffle:** misma X, mismo grafo, marcas permutadas con conteos exactos. Entrenamiento independiente y seeds emparejados. Es un HU-union condicional de marcas, distinto de B2: comparte exactamente estadísticas no marcadas con MHU.

**Control de mixing local:** conservar X y aristas; intercambiar dos etiquetas distintas mediante annealing. Objetivo: igualar matriz de pares dirigidos de tipos y histogramas homotípicos en bins [0;0,5;1;2;3]. 100.000 propuestas, temperatura logarítmica 0,1→0,0001, hasta diez reinicios; elegir primer control admitido. Se admite si cada celda con ≥20 pares difiere ≤5%, cada celda menor difiere ≤2 pares, degree medio por clase difiere ≤0,10, y la media de S de **cada componente** en banda baja es ≥0,50. Estas tolerancias pueden ser incompatibles: si no se cumple, no habrá afirmación de mecanismo «ondas largas independientemente de mixing». El control shuffle completo sigue siendo válido para organización de marcas como paquete.

Energía de ese annealing: sumar, sobre cada feature de conteo f, $[\max(0,|f-f_0|-\tau_f)/\tau_f]^2$, con las tolerancias anteriores; sumar el mismo término para out-degree medio de clase con $\tau=0,10$; añadir por clase $[\max(0,0,50-\overline S_c)/0,50]^2$. Todos los términos tienen peso uno. Propuesta uniforme de pareja de nodos con marcas distintas; aceptar siempre descenso y, para incremento ΔE, con probabilidad exp(−ΔE/temperatura). La condición de admisión exige energía cero dentro de 1e−10. La versión Grid usa esta misma regla Metropolis con su energía espectral.

**Control agrupado:** ordenar posiciones por coordenada x después de una traslación periódica determinada por seed y repartir bloques consecutivos con los conteos exactos. Crea franjas de clases. Mantiene X, E y presupuesto; cambia mixing local deliberadamente. Si mejora, favorece organización modular para esa tarea; si empeora, no distingue cobertura de mixing.

**Grid de tarea como rival ecológico adicional:** para fill, una NCA de 100 celdas coincide con el mundo 10×10, cuatro vecinos cardinales y el mismo bloque G, d32/T16. Su input/readout se aplican directamente por celda. N y MAC son menores: reportar rendimiento–coste y no meterla en el contraste causal N400. Es una alternativa práctica fuerte porque evita aprender la interfaz. Si domina claramente, LARP necesita una aplicación donde su geometría ofrezca algo útil.

Grafo transformer, expander adicional y topología aprendida se excluyen de v0.1. RR cubre el control disperso de caminos cortos; añadir otro generador ahora aporta poco. Una atención global barata podría ser rival ecológico posterior si SW/RR revelan que falta routing, pero no se usará para atribuir un beneficio a MHU.

## I. Ablation matrix

Sea $P_1=12.277$ y $P_8=12.508$ para T/F; G resta 16. Cada fila incluye dos tareas informativas, copy/fill, salvo indicación. «6 in» no implica 6 out.

| ID/etapa | Geometría | Identidad | Parámetros por tipo | Conectividad | Grado/arcos | P | T | Propósito |
|---|---|---|---|---|---|---|---|---|
| S0 | MHU/ Grid | G | No | kNN | 6 in/2400 | G | 16 | Smoke, fugas y propagación |
| C1 piloto | MHU nativa | T | No; embedding | kNN | 6 in/2400 | P_o | 16 | Condición funcional nominal |
| C2 piloto | Misma X, shuffle | T | No; embedding | mismo kNN | idénticos | P_o | 16 | Efecto causal de marcas |
| C3 focal | Misma X, matched mixing | T | No; embedding | mismo kNN | idénticos | P_o | 16 | Cobertura a ondas largas |
| C4 focal | Misma X, agrupadas | T | No; embedding | mismo kNN | idénticos | P_o | 16 | Distribución frente a módulos |
| C5 | MHU nativa/shuffle | F | Cinco rango2 | mismo kNN | idénticos | P_o | 16 | Interacción con reparto funcional |
| C6 | MHU/HU-union | G | No | kNN | 6 in/2400 | G | 16 | Unión geométrica; no H3 |
| B1–B5 screen | Grid/HU/RR/SW/Poisson | T | No; embedding | definiciones H | 2400 causal | P_o | 16 | Oponentes funcionales de estructura y routing |
| B1/B2 funcional | Grid balanceada / HU-union | T | No; embedding | kNN | 6 in/2400 | P_o | 16 | Rival funcional fuerte |
| P1 | MHU y shuffle, iguales 20% | T | No; embedding | kNN | 6 in/2400 | P_o | 16 | Separar frecuencias |
| E1 ecológico | MHU / HU / Grid / SW | G y T | según familia | nativa | medido | misma familia | 16 | Arquitectura completa |
| E2 ecológico | Grid de tarea N100 | G | No | cardinal | 4/400 | G | 16 | Alternativa de bajo coste |
| T1 evaluación | Modelos congelados | igual | igual | igual | igual | igual | 8,16,32,64 | Curva de transporte/estabilidad |
| N1 evaluación | N1600, L40 | igual | igual | misma regla | 9600 causal | igual | 16,32,64 | Escala de dominio |
| R1 evaluación | Lesiones/dropout | igual | igual | sin reconectar | decreciente | igual | 16 | Robustez |
| A1 condicional | X fija, distancia de arista anulada | T | No; embedding | mismo kNN | igual | igual | 16 | Ventaja por edge feature |
| M1 condicional | Colapso o relocación de funciones | T/F | intervención | mismo grafo | igual | igual | 16 | Dependencia funcional causal |

No ejecutar el producto cartesiano completo. La secuencia de J indica qué filas se abren y con cuántas semillas. C3 sólo se abre si se consiguió el control geométrico; su fracaso no se oculta. Las evaluaciones sin reentrenamiento no cuentan como nuevas réplicas de entrenamiento.

## J. First experiment sequence

### J0. Auditoría del tratamiento y de la interfaz

Antes de entrenar: certificado, Hamilton, invariancia G ante marcas, renombrado coherente T/F, asignación de puertos, conectividad y coste. Probar 100 casos contra un oráculo convencional de tarea. Para pares de puertos computar distancia dirigida mínima origen→salida. Que exceda T significa inaccesibilidad obligatoria, no error de implementación.

Mundo externo común: 100 sitios $(2a+0,5,2b+0,5)$, a,b=0,…,9, en el toro L20. Asignación inyectiva $\pi$ por Hungarian, coste distancia periódica al cuadrado entre los 100 sitios y los N nodos. Resolver una vez por geometría y fase de puertos, conservar para nativa/shuffle/controles. Desempatar con perturbación lexicográfica menor que 1e−10, no con tipo. Registrar RMS, máximo y distribución de desplazamientos. No rechazar geometrías por mala interfaz.

Canales 0–24: puerto presente; ocho bits de payload; cinco indicadores de ID de fuente; cinco de consulta; indicador seed; indicador free; cuatro coordenadas sin/cos. Las coordenadas son sin/cos de posición física en nodos internos y de posición del sitio lógico en puertos, normalizadas por L. Fuentes no usadas tienen bits cero. Las coordenadas nunca incluyen distancia a la respuesta, BFS ni información de etiquetas. Entrenar un modelo separado por tarea.

Todos los puertos posibles existen como direcciones, pero sólo los usados por la tarea llevan mask=1. La entrada permanece en u a cada paso: la tarea copy es **routing de fuentes persistentes**, no memoria temporal. La salida lee únicamente neuronas de puertos designados.

La comparación de geometrías cambia $\pi$ y calidad de muestreo; ese efecto forma parte de utilidad arquitectónica. La interpretación causal fuerte se reserva a los controles que mantienen X y $\pi$. Un análisis de regresión sobre desplazamientos no elimina mágicamente este confound.

### J1. Tarea 1: XOR de dos fuentes remotas

Elegir tres sitios distintos al azar; cada fuente a distancia física ≥L/4 del destino. Inputs de un bit, cuatro combinaciones en cantidades iguales. Fuente IDs 0/1; consulta identifica ambas; salida XOR. El dataset se genera sin mirar conectividad. Fuente e identidad de nodo son independientes de tipo.

Train 2048 ejemplos, validación 512, test 2048; B4, máximo 250 updates. Grid-G y MHU-G, una geometría y dos inicializaciones. Umbral de smoke: ≥0,98 accuracy en el subconjunto accesible y loss finito; publicar también accuracy sobre todos los ejemplos y fracción accesible. Baselines constantes y una implementación que reúne explícitamente los dos bits comprueban etiquetas.

Si ambos fallan incluso en train accesible, parar tareas posteriores y corregir optimización o interfaz. Si sólo falla un grafo y el fallo corresponde a inaccesibilidad, el resultado diagnostica transporte. H1–H6 no se actualizan sustancialmente por acertar XOR. No optimizar arquitectura para maximizarlo.

### J2. Tarea 2: copia direccionada de ocho bits entre cinco fuentes

Cada ejemplo elige seis sitios distintos: cinco fuentes, un destino. Todas las fuentes están a distancia ≥L/4 del destino. Asignar IDs 0–4 mediante permutación independiente de sitios/tipos; generar cinco payloads de ocho bits Bernoulli(0,5). El destino recibe un query one-hot de cinco entradas y debe copiar el payload de esa fuente. Equilibrar queries en train/val/test hasta diferencia ≤1 ejemplo. No inyectar el payload seleccionado en otro sitio.

Train 8192, validación 1024, test ID 4096. Pilot B4/1000 updates, o 500 si activa la regla de tiempo. Permutaciones de orden de minibatch por seed; no reemplazo hasta agotar train, luego nuevo orden. Endpoint principal: accuracy por bit. Secundarios: vector exacto, BCE, calibración, pasos hasta 0,95 bit accuracy, score por distancia física y hops. El nivel azar es 0,5 por bit y 1/256 por vector.

**Piloto focal:** tres geometrías × dos inicializaciones, emparejadas, para C1/C2. Son seis realizaciones por condición, doce entrenamientos. **Screen de alternativas:** B1–B5 en familia T y G-MHU/G-HU, una geometría × dos inicializaciones, 500 updates comunes. Comparar a sus checkpoints de 500 también las condiciones focales; no enfrentar 1000 updates a 500. Es diagnóstico y selección en validación; no estimación confirmatoria con dos seeds.

H4 predice SW/RR superiores a T fijo y aumento de error con hops; H1 predice poco efecto de marcas; H3 requiere nativa>shuffle con funciones diferentes. H2 predice mayor separación en daño/reubicación que en limpio. H6 admite ventaja del control agrupado. H5 no se identifica aquí. Si los tipos no se especializan, un nulo sólo debilita H3 en este entrenamiento.

### J3. Tarea 3: flood fill acotado en un mundo independiente

Mundo lógico 10×10 toroidal, **cuatro** adyacencias cardinales. Elegir p de {0,45;0,55;0,65} con frecuencias iguales, muestrear celdas libres Bernoulli(p), elegir seed uniformemente y forzarlo libre. La etiqueta de cada celda es pertenecer al conjunto alcanzado tras **ocho iteraciones** de flood fill, incluyendo seed. El oráculo BFS se ejecuta en el mundo lógico, nunca en el grafo neuronal. Obstáculos no eliminan aristas del sustrato: la red es un procesador del problema.

Train 8192, validación 1024, test ID 4096, mismo presupuesto que copy. Los 100 puertos contienen free/seed y se leen sus 100 outputs. No supervisar estados intermedios en v0.1. Las matrices se generan sin seleccionar tamaño favorable de componente. Publicar distribución de prevalencia y distancia BFS.

Endpoint principal: balanced accuracy **por mapa** sobre celdas libres, $\mathrm{BA}=\tfrac12(\mathrm{TP}/n_++\mathrm{TN}/n_-)$; si no hay clase negativa usar accuracy del mapa e informar su frecuencia. Promediar mapas dentro de cada p y después los tres promedios con peso 1/3. Binarizar con sigmoid≥0,5, también en XOR/copy. Secundarios: IoU, mapa exacto, BCE, errores por distancia BFS y errores en obstáculos. Un rival que predice todas las libres y otro que predice sólo seed son obligatorios: evitar un benchmark casi saturado por percolación.

Repetir C1/C2 y el screen causal B1–B5-T/G-MHU/G-HU **también en fill**, con los mismos números de seeds y presupuesto que copy. Screen ecológico adicional: Grid400-T balanceada, HU-Delaunay-T, MHU-Delaunay-T, SW-T y NCA100-G, una geometría×dos inicializaciones, presupuesto común 500 updates; incluir compute real y mantener checkpoints a 500 también en causal. H1 favorece grid/HU; H4 favorece transporte si falta campo receptivo; H3 exige que funciones y cobertura importen; H2 se contrasta después mediante daño. Una victoria sólo en fill podría ser interpolación espacial: exigir control de marcas y reportar interfaz.

El propósito no es anunciar «maze solved». Fill8 es un cálculo iterativo finito; extrapolar a conectividad ilimitada requerirá tareas posteriores.

### J4. Confirmación focal y factores secundarios

Congelar selección antes de abrir test confirmatorio: **para cada tarea**, baseline causal más fuerte según score medio de validación de las dos inicializaciones del screen, con G-MHU/G-HU como contraste geométrico separado. No promediar copy y fill para elegir un rival. Empates dentro de 0,005 se resuelven por menor MAC y después por orden Grid, HU, SW, RR, Poisson. No escoger el rival más débil. En Grid funcional, la condición balanceada es el rival nominal y la aleatoria es ablación.

Confirmación inicial: **ocho geometrías nuevas × dos inicializaciones**, 16 realizaciones por condición; seeds separados del piloto y calibración. Dataset nuevo: train 32.768, val 2048, test 4096. B4, 3000 updates. Cada condición causal evalúa lr {0,001;0,003;0,01}, 300 updates por candidato, una geometría de calibración y dos inicializaciones. Elegir **una lr común por tarea** por score de validación: promediar inicializaciones, luego condiciones de una misma geometría/familia, y después dar peso igual a los grupos geométricos admitidos en confirmación. El par nativa/shuffle forma un único grupo MHU; si se incluye G/F, sus promedios forman subgrupos de igual peso dentro de MHU. Desempate por lr menor. Todos los contrastes causales de esa tarea usan esa lr y schedule constante; calibración no cuenta como réplica. En comparación ecológica posterior se permite mejor lr individual con igual búsqueda, reportando que es otro estimando.

Confirmar sólo el contraste nativa–shuffle en **ambas tareas** y contra el baseline fuerte de cada tarea. Añadir F nativa/shuffle si validación sugiere especialización o T pierde por capacidad; añadir G-MHU/G-HU si el screen mostró efecto de unión. La selección sirve para gasto de cómputo, no para renombrar el endpoint tras ver test. Si ningún contraste muestra señal y el piloto aprendió, confirmar el nulo nativa–shuffle, no toda la matriz.

La diferencia de 0,02 es la mínima relevante. Si tras ocho geometrías el posterior no resuelve ventaja, equivalencia o daño, ampliar **una sola vez a 16 geometrías**, conservando las dos inicializaciones por geometría, sin tocar hiperparámetros. Si sigue amplio, resultado inconcluso. No convertir 16 entrenamientos correlacionados en 16 geometrías independientes.

Abrir C3/C4 y frecuencias iguales con tres geometrías×dos inicializaciones sólo si hay efecto de marcas o diagnóstico de falta de tratamiento. Para corroborar H3, C3 debe confirmarse con ocho×dos antes de una afirmación mecanística fuerte. Un presupuesto que no alcanza esa etapa permite afirmar rendimiento, no mecanismo.

Evaluación de escala: N1600/L40 con tres geometrías nuevas, mismos pesos sin fine-tuning, T={16,32,64}. Copy conserva cinco fuentes y distancia mínima L/4. Fill usa mundo20×20, 400 puertos separados dos unidades, etiqueta fill8; esto prueba tamaño, no más pasos lógicos. Fill16/T32 es exploratorio aparte. Comparar T8/16/32/64 también en N400 con la **misma etiqueta**, para detectar degradación o ausencia de halting.

La primera tanda debe ser certificado→smoke→copy focal. Estimar el coste total tras calibración: si excede ocho horas para el piloto previsto, aplicar el presupuesto de 500 updates a todas las condiciones antes de test y ejecutar fill en una segunda tanda. La confirmación puede distribuirse en sesiones; no prometer que una batería completa de decenas de entrenamientos acaba en horas.

### J5. Control positivo de recursos y diagnósticos de mecanismo

Si el tratamiento altera cobertura pero T/F no adquieren funciones distintas, introducir un **ensayo artificial de sensibilidad**, separado de las tareas principales. Para cada canal c, muestrear ocho coeficientes normales independientes de cuatro modos (1,0),(0,1),(1,1),(1,−1). Definir $f_c(x)=\sum_m[a_{cm}\cos(k_mx)+b_{cm}\sin(k_mx)]/\sqrt{\tfrac12\sum_m(a_{cm}^2+b_{cm}^2)}$; media espacial cero y varianza uno. No normalizar usando sólo muestras de un tipo.

Cada uno de los N nodos recibe exclusivamente $f_{c_i}(x_i)$ en el slot de payload c_i; los otros cuatro slots de campo son cero y los últimos tres slots de payload son cero. Los 25 destinos comunes son $(4a+0,5,4b+0,5)$, a,b=0,…,4, registrados por Hungarian. Target en cada destino: promedio de los cinco $f_c$ evaluados en **ese destino**. En este ensayo usar 29 canales: los 25 habituales, conservando coordenadas físicas incluso en puertos, más cuatro sin/cos del query externo sólo en destinos. Source/query IDs y free/seed quedan cero; mask=1 sólo en destinos. El encoder 29→32 añade exactamente 128 parámetros a cada familia; T/F tienen 12.405 parámetros con o1. Mantener el mismo readout 32→32→1, omitiendo sigmoid; pérdida MSE.

Train 4096 campos, val512, test2048; tres geometrías×dos inicializaciones, 1000 updates comunes. Comparar marcas nativas, shuffle, matched y Grid balanceada, familia T. NMSE=MSE/varianza de todos los targets train, estimada una vez y congelada; informar correlación de error con déficit de canales en bolas accesibles. La asignación por clase impone escasez de recursos: **una ventaja demuestra sensibilidad del ensayo a cobertura restringida, no que tipos aprendidos libres necesiten esa cobertura**. No mezclar su score con copy/fill ni usarlo solo para justificar LM.

Además: distancia al tipo, ventanas vacías, conteos por hops, mixing, distribución de Jacobianos input→output por distancia/tipo, funciones contrafactuales y caída al colapsar q/adaptadores. Si los radios donde cambia cobertura exceden los radios de influencia funcional, H3 no fue adecuadamente probado. Esa discrepancia justifica cambiar K o tarea en v0.1b; no contar el cambio como confirmación de v0.1.

**M1 operativo, sin reentrenamiento:** para T/F calcular las cinco funciones completas $f_c(z,m,u)$ del incremento de F, con sus q y adaptadores, sobre el mismo estado. Construir $\bar f=\sum_c(N_c/N)f_c$ y usar $f_{c,\lambda}=(1-\lambda)f_c+\lambda\bar f$, λ={0;0,5;1}. No promediar factores U/V ni sólo embeddings. Evaluar en los mismos 512 ejemplos y medir interacción $D=(s_{\mathrm{native},0}-s_{\mathrm{shuffle},0})-(s_{\mathrm{native},1}-s_{\mathrm{shuffle},1})$ por geometría/init. Usar modelo L; P(D>0,01)≥0,90 es dependencia funcional auxiliar, sólo si ambos modelos permanecen >0,10 sobre azar/trivial bajo intervención; de lo contrario hay efecto suelo y no se interpreta.

Intervención de disponibilidad distinta: con pesos fijos, relocalizar **funciones completas** mediante 20 asignaciones permutadas con counts conservados, derivadas de clave7201; incluir la asignación matched si existe. X, aristas, u, consultas y puertos permanecen idénticos; q y selección de adaptador se trasladan conjuntamente. Contrastar cambio de score y cobertura efectiva, y usar renombrado global coherente como control cero. Esto prueba causalmente dependencia de la colocación en el modelo congelado, pero es OOD: sólo el contraste **reentrenado** matched de J4 identifica utilidad de organización sin ese confound. M1 no demuestra mediación natural exacta.

## K. Robustness protocol

Aplicar sin fine-tuning a los checkpoints congelados; 512 ejemplos de test elegidos por hash antes de resultados. Para cada nivel, diez máscaras aleatorias comunes y veinte centros físicos comunes en lesiones. Agregar primero dentro de cada geometría, después entre geometrías; ejemplos y centros no son réplicas independientes de arquitectura.

1. **Dropout de nodos:** retirar exactamente round(qN) nodos para q={0;0,05;0,10;0,20}; muestreo uniforme entre elegibles. Endpoint primario protege todos los puertos activos del ejemplo. Nodo retirado: estado y encoder cero, sin mensajes entrantes/salientes y sin readout. No reconectar kNN.
2. **Lesión localizada igualada:** mismo q y centro; retirar los round(qN) nodos elegibles más próximos. Registrar radio resultante, clases perdidas y huecos por protección de puertos. Esta es la comparación primaria H2.
3. **Disco de radio fijo:** R={1;2;3;4}, retirar elegibles dentro del disco. Reportar cantidad removida, y score condicionado a esa cantidad como descriptivo. No presentar una comparación desigual de cantidad como prueba principal.
4. **Lesión por tipo:** retirar n={4;8;16} nodos de cada clase, comparando con retiro aleatorio del mismo n. En N1600 multiplicar n por cuatro. Si hay menos elegibles, registrar que el nivel no existe; no completar con otro tipo. Secundario: retirar {25;50;75}% de cada clase elegible y reportar cantidad absoluta. Las clases minoritarias no reciben automáticamente el mismo daño global.
5. **Aristas:** borrar exactamente round(qE) arcos para q={0;0,05;0,10;0,20;0,40}. En grafos bidireccionales hay dos análisis: arcos independientes y parejas no dirigidas; no mezclarlos. Renormalizar la media por vecinos vivos, con cero si no quedan.
6. **Reubicación:** desplazar todo el sistema de puertos en (0,5;0), (0;0,5), (0,5;0,5) unidades físicas, recomputar Hungarian sin mirar tipos. Copy/XOR mantienen los mismos payloads y roles. Fill conserva su mundo/etiquetas y cambia sólo registro físico. Traslaciones de entrada sola o salida sola se prueban en copy, conservando información lógica. Reportar desplazamiento de interfaz.
7. **End-to-end:** repetir dropout/lesión sin proteger puertos como endpoint secundario. Mostrar rendimiento condicionado a conservación de entradas esenciales y output. Un ejemplo sin output no recibe una predicción fabricada; contar fallo en éxito de sistema y excluirlo del score de procesamiento condicionado.

Métrica primaria de daño: AUC normalizada del score entre q=0 y 0,20, interpolación lineal/trapecios; dividir por 0,20. Publicar también score limpio y caída absoluta para impedir que un modelo malo parezca resistente por suelo. Registrar fracción de puertos fuente→destino aún accesible a T pasos, SCC y distribución de pérdida por clase.

Para H2/H3 importa **qué recurso falta y dónde**, no sólo cuántas células quedan. En cada máscara medir déficit por clase en R4/R5 y en bolas de cuatro/ocho hops. Si MHU retiene menos desiertos pero pierde igual score, el mediador cambió sin utilidad. Si score mejora sin cambio de déficit, la explicación por cobertura pierde apoyo.

No entrenar con daño en la primera ronda. Si el objetivo pasa a reparación aprendida, preregistrar entrenamiento con máscaras idénticas para todos y repetir el contraste. Una red robusta gracias a esa política no demuestra robustez intrínseca de geometría.

## L. AB update protocol

El producto científico incluye el historial de decisiones. Antes de entrenar cada etapa escribir un registro inmutable con ID, fecha, commit o hash de código, versión/hashes de tarea y geometría, condiciones, parámetros/aristas, seeds, optimizer, search budget, endpoints, priors, predicciones y reglas de decisión. El campo resultados permanece vacío hasta congelar el análisis.

Seeds base: master 20261008; geometrías piloto 1101–1103; inicializaciones piloto 2101/2102; geometrías confirmatorias 3101–3108, extensión 3109–3116; inicializaciones confirmatorias 4101/4102; splits train/val/test 5001/5002/5003; sentinel 6101–6103 derivados por N; controles de marcas derivados de seed geométrico y 7101; calibración 9001/9002. Derivar substreams mediante SeedSequence con claves numéricas documentadas, no mediante hash de Python variable entre sesiones.

Al completar el entrenamiento registrar accuracy/task score, loss final y curva, updates/muestras hasta umbral, tiempo de entrenamiento e inferencia, memoria, fallos, varianza de init y de geometría. Una divergencia reproducible después de descartar fallo de infraestructura recibe **score de sistema cero** en el endpoint y posterior primarios, loss +infinito; no se elimina. Publicar además rendimiento condicionado a ejecuciones válidas y failure rate. Interrupciones de infraestructura se reanudan con mismo seed/checkpoint; invalidaciones de implementación detienen la etapa y no se imputan como evidencia contra MHU. Graph metrics: in/out-degree y varianzas, reciprocidad, clustering de versión no dirigida, distribución dirigida de caminos finitos e inaccesibles, diámetro finito máximo, componentes y longitudes de aristas. Algebraic connectivity de Laplaciano simetrizado se reporta como descripción, **no certificado de estabilidad** de dinámica no lineal. A N400 usar todos los pares; a N1600, 256 orígenes fijados por hash, declarando estimación.

Para proposición A, efectos emparejados $\Delta_{g,s}$, score nativa−control, usando iguales datos y training seeds. Modelo:

$$
\Delta_{g,s}=\mu+b_g+\epsilon_{g,s},\quad
b_g\sim\mathcal N(0,\sigma_g^2),\quad
\epsilon_{g,s}\sim\mathcal N(0,\sigma_s^2),
$$
$$
\mu\sim\mathcal N(0,0.05^2),\qquad
\sigma_g,\sigma_s\sim\operatorname{HalfNormal}(0.05).
$$

Implementación del análisis sin añadir una infraestructura pesada: integrar $\mu$ analíticamente condicionado a varianzas y usar cuadratura Gauss-Legendre 96×96 para sigmas en [1e−6;0,25], con densidad y normalización de priors. Publicar posterior de $\mu$, intervalo creíble 95%, P(μ>0,02), P(|μ|≤0,02), P(μ<−0,02). Repetir con prior de μ de desviación 0,02 y 0,10 y con 192×192 puntos para comprobar sensibilidad numérica. Si las colas fuera de 0,25 son relevantes, extender integración antes de decidir.

La normalidad modela variación de **diferencias de scores agregados**, no cada bit. Comprobar sensibilidad con bootstrap por geometría y gráficos de efectos; si ambas conclusiones discrepan, declarar sensibilidad. No tratar 4096 ejemplos, diez máscaras o dos inicializaciones correlacionadas como réplicas de geometría. La tabla de priors marginales H1–H6 no reemplaza este modelo cuantitativo.

Plantilla de actualización:

| Campo | Contenido exigido |
|---|---|
| Proposición | A de rendimiento, C de mecanismo, o H concreto; indicar alcance |
| Prior | Probabilidad/modelo previo y razones; referenciar el registro anterior |
| Evidencia anticipada | Diferencia/ROPE, intervención y qué debería mantenerse fijo |
| Resultado | Todas las semillas y fallos, incertidumbre, presupuesto efectivo |
| Likelihood | Distribución explícita para A; para H/C, evaluación cualitativa y confounds |
| Actualización | Posterior cuantitativo donde existe; dirección/fuerza ordinal donde no |
| Mecanismo | Cambió cobertura, especialización, alcance o ninguno; distinguir correlación e intervención |
| Próximo ensayo | Predicción nueva y por qué discrimina más por unidad de cómputo |

Para mecanismos sin likelihood validada usar grados **contradice fuerte / contradice débil / neutro / apoya débil / apoya fuerte**. Si se desea un odds update ilustrativo, asignar LR convencionales {1/5;1/2;1;2;5}, registrar que son **elicitudes subjetivas**, y mostrar sensibilidad usando {1/3;1/1,5;1;1,5;3}. No llamarlos Bayes factors estimados a partir de datos.

No multiplicar como independientes evidencia de accuracy, AUC, Jacobiano y cobertura de los mismos runs. Constituyen un solo paquete de evidencia; preregistrar endpoint primario y usar lo demás para diagnóstico. Una comparación seleccionada durante piloto se confirma con nuevas geometrías y datos; el análisis confirmatorio no reaprovecha sus scores como si no hubiera selección.

**C obtiene apoyo específico sólo si**: tratamiento altera cobertura en escalas usadas; T/F muestran funciones causalmente diferentes; el efecto nativa–shuffle se replica; persiste frente al control de mixing local; y una intervención sobre disponibilidad funcional reduce el beneficio sin cambiar X/aristas/puertos. Los primeros cuatro elementos no permiten afirmar una mediación natural exacta, pero constituyen un paquete mucho más discriminante que una correlación. Si matched mixing no puede construirse, C permanece parcialmente no identificada.

## M. Stop / pivot / continue

**Parar por invalidez, sin actualizar contra MHU:** certificado fallido; G sensible a marcas; fugas de etiquetas; encoder/readout con acceso remoto accidental; parameter count incorrecto; datasets distintos; bug de oracle; o matriz que cambia fuera del factor declarado. Resolver el fallo y versionar preregistro.

**Parar o reformular el ensayo por falta de aprendizaje:** ningún rival fuerte supera azar/triviales después de presupuesto confirmatorio, o XOR accesible no aprende. Esto evalúa el bloque/interfaz, no geometría. Una sola revisión permitida v0.1b: sustituir update por GRU compartido o aumentar T de todos a 32, con nuevo matching y presupuesto común. Elegir GRU si no converge incluso en problemas locales; T32 si el problema es alcance. No hacer ambos cambios sin separar sus efectos.

**Continuar hacia v0.2 por utilidad:** posterior P(μ>0,02)≥0,95 en copy o fill para nativa−shuffle, sin daño relevante confirmado en la otra tarea; además rendimiento frente al rival fuerte no inferior por más de 0,02 con probabilidad ≥0,95. Si el rival gana claramente, un mecanismo identificado puede justificar investigación científica específica, pero no reclamar una arquitectura superior.

**Continuar por robustez:** ventaja de AUC de lesión igualada >0,02 con probabilidad ≥0,95, score limpio no inferior dentro de 0,02, puertos protegidos y misma cantidad retirada. Exigir réplica en una geometría/tarea fuera del piloto. Un único punto q favorable no basta.

**Equivalencia/stop de la propuesta actual:** P(|μ|≤0,02)≥0,90 en ambas tareas, y sin ventaja robusta ni de muestras/coste frente a HU/Grid fuertes. Reducir H3 para estas condiciones; detener escala y lenguaje. Puede conservarse LARP como banco de investigación geométrica, sin perseguir arquitectura general por inercia.

**Daño relevante/pivot:** P(μ<−0,02)≥0,95 en ambas tareas o agrupadas/matched superan consistentemente nativas. Investigar modularidad, grados o routing como explicaciones; no suavizar la conclusión por inspiración biológica. Una pérdida de F con T estable pivota parametrización, no geometría.

**Inconcluso:** intervalos amplios después de 16 geometrías, divergencias de sensibilidad, o efecto de cobertura no intervenido. Detener expansión de suite; mejorar precisión o tratamiento. Ausencia de significación no es equivalencia.

**Apoyo a H3:** paquete definido en L, incluyendo control de mixing y dependencia funcional. **Plausibilidad reducida de MHU:** cobertura efectivamente mejora, funciones son necesarias, los pares locales se igualan, la tarea aprende y aun así la diferencia cae en ROPE en dos tareas y bajo daño. Éste es un nulo informativo mucho más fuerte que «T/F no se especializaron».

**Pivot de routing:** SW/RR aventajan a locales ≥0,05 y el gap sigue accesibilidad/hops, mientras nativa−shuffle está en ROPE. Priorizar routing disperso; no añadir MHU al híbrido sin una razón residual. **Good initialization:** se evalúa únicamente mediante plasticidad y warm starts cruzados; no inferir H5 de que una geometría cambie durante entrenamiento.

## N. v0.2 roadmap

| Resultado v0.1 | Siguiente ensayo autorizado científicamente |
|---|---|
| Cobertura funcional apoyada y SW transporta mejor | Factorial {MHU, HU-shuffle}×{0%,10% shortcuts}×{gate fijo, gate compartido aprendido}; edge count constante por reemplazo, no adición |
| G gana pero marcas no importan | Investigar unión, radios, out-degree y registro de puertos; retirar narrativa multicomponente |
| T gana, F no | Mantener conditioning; curva rank2/5/10 y compute matching; no cinco expertos grandes |
| Daño revela ventaja real | Entrenamiento con y sin daño idéntico para todos; prueba de reparación de estados en tiempos no vistos |
| Agrupadas ganan | Arquitectura modular como competidora; tarea mixta con demandas locales/globales y roles exógenos |
| Nulo preciso | Detener escalado; una única nueva tarea sólo si hay mecanismo distinto preregistrado |
| Tratamiento no altera cobertura útil | v0.1b cambia K o incorpora escala de cobertura; medir primero, reusar resultados anteriores sólo como exploratorios |

**Plasticidad:** comienza en v0.2, después de cerrar comparación congelada. Primera etapa: gates de función compartida sobre las mismas aristas, igual coste/parámetros para todas las geometrías. Segunda: swaps dirigidos de aristas con presupuesto y secuencias in/out fijos. Comparar MHU/HU/random iniciales y analizar topología final, coste de cambios y velocidad de aprendizaje.

Para separar inicialización y destino, usar warm starts cruzados: pesos aprendidos transferidos a grafos comparables y grafos finales evaluados con reinicialización/reentrenamiento. Si sólo la topología final predice éxito, H5 pierde; si MHU reduce muestras a igual destino, gana. Pinning de puertos impide que mejorar interfaz se confunda con mejorar compute.

Coordenadas aprendidas son una tercera etapa: kNN es discontinuo y no basta backprop por vecinos seleccionados. Usar candidatos locales fijos y kernels/gates continuos, medir deriva de S y regularización en una cuadrícula de pesos predefinida, siempre con controles de inicialización. La deriva por sí sola no identifica daño ni ventaja de MHU.

**3D:** después de replicar beneficio en 2D y en al menos dos tamaños. Comparar densidad, degree, distancia de influencia y compute, con coordenadas colectivas 3D y criterios nuevos para ventanas esféricas. Una única comparación 2D/3D con igual N y T no es justa por cambiar radios y caminos. No incluir 3D sólo para acercarse a una ambición LM.

**Shortcuts:** sólo bajo la primera fila o cuando el objetivo declarado pivote a routing. Antes de gates dinámicos probar enlaces fijos: identifica si basta accesibilidad. Dynamic routing añade otro mecanismo y su coste; se incorpora después de mostrar que enlaces estáticos no bastan.

## O. Route toward problem solving and later LM

Antes de hablar de problem solver general deben demostrarse: reachability de horizonte creciente, shortest path con costes, connected components, routing con múltiples demandas y memoria con entradas retiradas. Usar tareas exógenas y luego un subconjunto CLRS; distinguir aprender respuestas de aprender un procedimiento transferible. Exigir dos tamaños nuevos, variación de dificultad y rollout más largo estable, con baselines de igual coste. [CLRS](https://proceedings.mlr.press/v162/velickovic22a.html).

La extrapolación de recurrent steps no aparece por ligar pesos. Hace falta entrenamiento de trayectorias/halting, control de oversmoothing y estabilidad bajo entradas/datos nuevos. El preprint reciente de NCA vincula capacidades OOD con replay y perturbaciones: es una advertencia para no atribuir al sustrato lo aprendido mediante política de entrenamiento. [NCA para razonamiento, preprint 2026](https://arxiv.org/abs/2609.36126).

Para secuencias, primero copy temporal y associative recall con longitudes 16/32 train y 64/128 test, retirando inputs cuando corresponde. Introducir estados persistentes, direccionamiento y presupuesto de latencia. Después comparar con RNN/GRU y un transformer pequeño a parámetros, muestras y MAC razonables; los detalles serán preregistro posterior.

Lenguaje sólo se abre si hay una ventaja que sobreviva esa fase: eficiencia o generalización reproducible, no una victoria aislada en fill. Una LM probablemente necesita una interfaz de tokens, memoria direccionable, comunicación global, batching y entrenamiento estable. MHU podría ocupar un módulo interno; no hay razón actual para imponer geometría espacial al orden de tokens.

La ambición LM queda sustancialmente debilitada si la ventaja depende de entradas espacialmente continuas, tipos forzados artificialmente o reconstrucción local, y desaparece en memoria no espacial; si los shortcuts eliminan la contribución MHU; o si latencia/memoria exceden baselines sin mejor loss. No gastar un entrenamiento SLM para intentar rescatar un nulo geométrico. Tampoco equiparar resolver tres tareas pequeñas con inteligencia emergente.

## P. Edge-as-computation branch

Es una rama coherente, con abundante prior art. Graph Networks ya permiten actualizar estados de aristas; line graphs convierten aristas en vértices; factor graphs y hypergraphs representan restricciones/relaciones múltiples; complejos simpliciales incorporan incidencia y orientación. EB-GNN aporta un antecedente de 2026 particularmente próximo con mensajes sobre aristas y triángulos. Esa expressividad no proviene de MHU ni prueba que una motivación relacional sociológica prediga rendimiento. [Graph Networks](https://arxiv.org/abs/1806.01261), [EB-GNN, ICML 2026](https://proceedings.mlr.press/v306/barcelo26a.html), [simplicial message passing](https://proceedings.mlr.press/v139/bodnar21a.html).

Ensayo mínimo posterior: line graph de un grafo 6-regular de 100 nodos; señal/consulta en aristas; tarea predecir reachability de aristas a cuatro iteraciones bajo bloqueos de aristas. Comparar node-state+edge-message, edge-state recurrente y representación de incidencia bipartita, con mismo grafo objetivo, readout y curvas de presupuesto total de estado, parámetros y MAC. E=300 aristas implica line graph de 300 vértices y degree10 en caso regular; contabilizar crecimiento, no compararlo sólo por dimensión d.

La propuesta de **conectividad MHU** necesita una medida definida. Para clase relacional a, representar aristas como un campo espacial de peso:

$$
w_a(x)=\sum_{e\in E_a}w_e\,\delta(x-m_e),\qquad
S_a^E(k)=\frac{|\sum_{e\in E_a}w_e e^{\,\mathrm ik\cdot m_e}|^2}
{\sum_{e\in E_a}w_e^2}.
$$

Medir banda baja, varianza integrada en ventanas, orientación y longitud por clase, cross-spectra, degree incidente y correlación con densidad de nodos. Los midpoints son una formulación posible para aristas locales, pero dejan de describir bien recursos de enlaces largos. En el toro, midpoint requiere elegir el segmento de imagen mínima; lazos que atraviesan el borde no se promedian ingenuamente.

Alternativa más física: integrar longitud/capacidad de cableado dentro de ventanas y medir sus fluctuaciones, además de densidad de incidencias de cada relación. Una unión de midpoints HU no garantiza comunicación, capacidad de corte ni rutas. También puede heredar regularidad trivialmente de nodos y degree fijo.

«local/same-type/cross-type» mezcla categorías solapadas: usar capas de relación mutuamente etiquetadas o explicitar multiplicidad. Para probar valor añadido de edge-MHU, mantener puntos, degree, longitudes y counts de cada relación, y redistribuir las clases relacionales alterando su espectro. Sólo después comparar rendimiento. Ninguna de estas modificaciones entra en v0.1.

## Q. Implementation contract for SOL 6.1 UltraCode

- Implementar esta revisión y el brief v2 como contrato; registrar cualquier desviación científica antes de resultados. No añadir attention, gating, replay, daños de entrenamiento ni geometría aprendida al núcleo.
- Separar generador/certificador, grafo, mundo lógico, registro de puertos, módulo G/T/F, entrenamiento, evaluación y actualización AB. Los datasets no reciben topología neuronal.
- Producir preregistro, config resuelta y hashes antes de abrir test; código versionado con commit, lock de dependencias, equipo/threads/BLAS, tiempo y límites de memoria.
- Usar cantidades Hamilton exactas con pesos enteros y desempate fijo. Certificar por componente y unión; nunca usar una geometría visualmente plausible sin medidas.
- Comprobar gradiente del objetivo geométrico contra diferencias finitas en 20 coordenadas; verificar periodicidad, identidad de amplitudes y densidad. Esto prueba el generador, no la hipótesis.
- kNN6 tiene exactamente 6N arcos sin loops ni duplicados; guardar grado entrante/saliente y SCC. Delaunay usa copias periódicas y validación de traslación. No reparar grafos silenciosamente.
- Si routing muestra efecto y cambia out-degree, añadir control diagnóstico de swaps dirigidos: 100E propuestas que preserven in/out por vértice, rechazando loops/duplicados. Separa grado de localidad; mismo update, datos y presupuesto.
- Verificar los conteos de parámetros de G/T/F para o1/o8. Todos los parámetros deben participar realmente; no padding ficticio. Log de MAC activo diferencia T/F.
- Probar invariancia de outputs/loss/gradientes G ante cualquier marca y de T/F ante renombrado coherente de marcas y parámetros. Permutar sólo marcas con pesos fijos es otra intervención.
- Probar aislamiento de ejemplos y límite de alcance: alterar un input a más de T hops no cambia salida, salvo dependencia explícita de coordenadas/inputs del propio output. No pooling global.
- Oráculos exactos de XOR, selección y BFS8 con casos manuales; generar splits por seeds y hashes. No filtrar ejemplos por performance ni graph distance específico de arquitectura.
- Cachear u por forward y W_m z por timestep; no guardar tensores de todas las evaluaciones de geometría. Medir coste real, no inferirlo de firing o E únicamente.
- Mantener budgets/optimizer/encoder/readout comunes; HPO sólo según J. Guardar todos los seeds, checkpoints finales y curvas. Checkpoint primario es el final del presupuesto; no escoger el mejor test.
- Fallos NaN o interrupciones se registran. Reintentar únicamente fallo de infraestructura desde checkpoint o con mismo seed; no sustituir semillas desfavorables. Divergencia cuenta en failure rate y en éxito de sistema.
- Lesiones siguen K, sin reconexión, y distinguen puertos protegidos de end-to-end. Las máscaras y centros están fijados antes de scores.
- Generar tablas y figuras de rendimiento, loss, incertidumbre por geometría, coste, espectro, conteos, cobertura, paths y daño. Matplotlib para gráficos científicos, ejes/unidades y fuente de datos verificables.
- Ejecutar el piloto escalonado; detenerse ante invalidez, aprendizaje ausente o reglas M. Implementar no significa perseguir un resultado positivo con nuevos hiperparámetros.
- El análisis posterior distingue A de C y no transforma odds subjetivos en Bayes factors medidos. El informe final conserva resultados negativos, confounds y ensayos no ejecutados.

## R. Machine-readable decision block

El objeto siguiente es `larp_v0_1_decisions`. Los factores declarados son experimentales; no autorizan al implementador a elegirlos mirando test. Las ramas futuras son condiciones de continuidad, no parte del núcleo.

```json
{
  "larp_v0_1_decisions": {
    "review_date": "2026-10-08",
    "authoritative_brief": "LARP_ASTRA_ARCHITECTURE_REVIEW_v2.md",
    "status": "pre_experiment_specification",
    "implementer": "SOL 6.1 UltraCode",
    "production_code_requested": false,
    "primary_estimand": "native_minus_shuffled_marks_retrained_on_identical_points_edges_and_ports",
    "primary_tasks": ["addressed_copy_5x8_persistent", "flood_fill_8"],
    "smoke_task": "remote_xor",
    "spatial_dimension": 2,
    "N_train": 400,
    "N_inference_scale": 1600,
    "N_geometry_validation": [400, 1600, 6400],
    "density": 1.0,
    "domain": {"boundary": "periodic_torus", "L": "sqrt(N)", "L_train": 20.0},
    "types": {
      "names": ["A", "B", "C", "D", "E"],
      "biological_reference": ["double_cone_unit", "green", "red", "blue", "violet"],
      "computational_roles": "not_assigned_by_biology",
      "weights_integer": [407, 211, 171, 126, 85],
      "denominator": 1000,
      "rounding": "Hamilton_largest_remainder_ties_in_A_to_E_order",
      "counts_400": [163, 85, 68, 50, 34],
      "counts_1600": [651, 338, 274, 201, 136],
      "counts_6400": [2605, 1351, 1094, 806, 544],
      "equal_counts_400": [80, 80, 80, 80, 80]
    },
    "geometry": {
      "method": "joint_multicomponent_collective_coordinate_optimization",
      "claim_scope": "finite_low_frequency_suppression_not_asymptotic_proof",
      "initial_positions": "iid_uniform",
      "initial_marks": "independent_permutation_with_exact_counts",
      "marks_during_optimization": "fixed",
      "dtype": "float64",
      "wavevectors": "k=2*pi*n/L; 0<norm(n)<=L/10; nx>0 or nx=0 and ny>0",
      "modes_400": [[1,0],[0,1],[1,1],[1,-1],[2,0],[0,2]],
      "K_physical": "pi/5",
      "objective": "mean_S_union+mean_over_5_components_and_modes_S+10/N*sum_pairs_relu(1-r/0.30)^2",
      "repulsion_radius": 0.30,
      "periodic_pairs": "cKDTree_query_pairs_recomputed_each_objective_evaluation",
      "adam": {
        "steps": 6000, "lr_start": 0.025, "lr_end": 0.0001,
        "schedule": "cosine", "betas": [0.9,0.999], "weight_decay": 0.0
      },
      "lbfgs": {
        "max_iterations": 250, "max_evaluations": 1000, "history": 20,
        "line_search": "strong_wolfe", "gradient_tolerance": 1e-8,
        "change_tolerance": 1e-12
      },
      "max_restarts_per_seed": 4,
      "selection": "first_pattern_passing_certificate",
      "certificate": {
        "apply_to": ["A","B","C","D","E","union"],
        "restricted_mean_S_max": 0.05,
        "restricted_max_S_max": 0.10,
        "minimum_union_distance": 0.299,
        "window_centers": 10000,
        "window_radii": [0.5,1,2,3,4,5],
        "variance_reference": "N_a*p*(1-p); p=pi*R^2/L^2",
        "mean_variance_ratio_R4_R5_max": 0.65,
        "nonoptimized_spectrum_range": "K<norm(k)<=pi",
        "max_S_over_N_in_that_range": 0.50,
        "anisotropy_quadrupole_flag": 0.30,
        "anisotropy_flag_is_exclusion": false,
        "heldout_spectrum_suppression_required": false,
        "descriptive_metrics": [
          "directional_and_radial_S","all_window_variances","g2_same_cross_union",
          "nearest_neighbor_CDF","toroidal_Voronoi_area","q4_q6",
          "empty_windows","nearest_type_p50_p90_p95",
          "type_counts_in_1_2_4_8_hop_balls"
        ]
      },
      "sentinel_seeds_per_size": 3,
      "generator_review_if_failed_seed_fraction_exceeds": 0.25
    },
    "graphs": {
      "causal": {
        "rule": "directed_incoming_knn",
        "k": 6, "edges_400": 2400, "distance": "minimum_image",
        "symmetrize": false, "self_loops": false,
        "tie_break": "class_independent_ID_hash",
        "connectivity_repair": false,
        "residual_confound": "out_degree_reciprocity_lengths_components_and_spectrum"
      },
      "ecological_MHU_HU": {
        "rule": "periodic_Delaunay_via_3x3_tiling",
        "triangle_selection": "circumcenter_in_fundamental_domain_then_extract_edges_deduplicate_original_IDs",
        "large_circumradius_policy": "repeat_5x5_only_if_radius>=L/2;fail_only_if_noninvariant_or_still_ambiguous",
        "direction": "bidirectional",
        "edges": "measure; generic_torus_approximately_6N",
        "prune_to_match_edges": false
      },
      "conditional_degree_preserving_control": {
        "method": "directed_double_edge_swaps",
        "proposals": "100*E", "preserve": ["in_degree_per_node","out_degree_per_node"],
        "reject": ["self_loop","duplicate"]
      }
    },
    "neural_block": {
      "d": 32, "input_channels": 25, "update_hidden_width": 64,
      "input_encoder": "Linear(25,32); cache_u; h0=u",
      "persistent_input": true,
      "normalization": "shared_affine_LayerNorm(32,eps=1e-5)_before_message_and_update",
      "edge_features": ["log1p_minimum_image_distance_in_density_units"],
      "message": "tanh(Wm*LN(hj)+wr*log1p(rij)+bm)",
      "apply_Wm": "once_per_node_per_time_step",
      "aggregation": "mean_over_alive_incoming_neighbors; zero_if_empty",
      "update": "h_next=h+0.1*(W2*SiLU(W1*[z;m;u;q]+b1)+b2+adapter(z))",
      "update_input_dimension": 100,
      "adapter": "U*tanh(V*z)/sqrt(rank); no_bias",
      "recurrence": "synchronous_tied_weights",
      "T_train": 16, "T_test": [8,16,32,64],
      "learned_gates": false, "attention": false,
      "stacked_untied_layers": false, "plasticity_v0_1": false,
      "network_dtype": "float32",
      "readout": "shared_Linear(32,32)_SiLU_Linear(32,o)_on_designated_ports",
      "global_pooling": false,
      "initialization": {
        "main_linears": "Xavier_uniform_gain1_bias0",
        "LN": "gamma1_beta0",
        "G_q": "zero",
        "T_F_embeddings": "Normal(0,0.02),center_rows",
        "adapter_factors": "Normal(0,1/sqrt(32)),independent",
        "shared_weights_across_families": "identical_training_seed_streams_per_named_module"
      }
    },
    "variants": {
      "G": {"q": "one_shared_trainable_4vector", "adapter": "shared_rank10", "marks_visible": false},
      "T": {"q": "embedding_5x4", "adapter": "shared_rank10", "marks_visible": true},
      "F": {"q": "embedding_5x4", "adapter": "five_rank2_selected_by_type", "marks_visible": true},
      "parameter_formulas": {"G": "12228+33*o", "T": "12244+33*o", "F": "12244+33*o"},
      "parameters_o1": {"G": 12261, "T": 12277, "F": 12277},
      "parameters_o8": {"G": 12492, "T": 12508, "F": 12508},
      "adapter_parameters_each_variant": 640,
      "T_F_exact_parameter_match": true,
      "G_T_residual_parameter_difference": 16,
      "active_adapter_MAC_per_node": {"G": 640, "T": 640, "F": 128}
    },
    "baselines": {
      "grid_causal": "20x20_half_integer_positions; directed_knn6",
      "grid_ecological": "four_cardinal_neighbors",
      "grid_types_strong": "minimize_mean_component_S_via100000_Metropolis_swaps_temperature0.1_to0.0001_ten_restarts; equal_case_(a+2b)%5",
      "grid_balance_failure": "minimum_energy_pattern_named_approximate_with_residuals_not_MHU_certified",
      "HU_IBM_inspired": "same_generator_without_component_terms; causal_knn6_ecological_Delaunay",
      "IBM_source": "US20240202508A1; not_exact_reproduction_not_independent_validation",
      "random_regular": "simple_undirected_degree6_on_same_MHU_coordinates; bidirectional; first_connected_of_20",
      "small_world_causal": "grid_knn6_each_incoming_slot_rewired_with_probability0.10",
      "small_world_ecological": "four_grid_cardinal_plus_two_remote_incoming; r>=L/4",
      "Poisson": "iid_positions; knn6_causal_Delaunay_ecological",
      "grid_task_ecological": "N100_10x10_direct_interface_four_cardinal_same_G_block_T16",
      "mark_controls": ["native","shuffle_exact_counts","matched_local_statistics","clustered_stripes"],
      "matched_local_statistics": {
        "swap_proposals": 100000, "restarts": 10,
        "temperature": [0.1,0.0001], "schedule": "logarithmic",
        "match": ["directed_type_edge_matrix","homotypic_pair_bins"],
        "distance_bin_edges": [0,0.5,1,2,3],
        "count_ge20_relative_tolerance": 0.05,
        "small_count_absolute_tolerance": 2,
        "class_mean_degree_tolerance": 0.10,
        "degree_kind": "out_degree",
        "each_component_mean_low_k_S_min": 0.50,
        "energy": "sum_squared_normalized_hinge_tolerance_violations_of_counts_outdegree_and_low_k_S",
        "energy_weights": "all_one",
        "zero_energy_tolerance": 1e-10,
        "acceptance": "descent_or_probability_exp(-energy_increase/temperature)",
        "failure_policy": "declare_long_wave_mechanism_not_identified"
      },
      "clustered": "periodically_shifted_x_order_then_consecutive_exact_count_blocks",
      "excluded_initially": ["global_attention","learned_topology","extra_expander","edge_states"]
    },
    "interface": {
      "world_sites_train": "10x10;(2*a+0.5,2*b+0.5)",
      "port_assignment": "injective_Hungarian_periodic_squared_distance",
      "tie_perturbation_max": 1e-10,
      "type_dependent_assignment": false,
      "report": ["RMS_port_displacement","maximum_port_displacement"],
      "channel_layout": [
        "0:port_mask","1..8:payload","9..13:source_ID",
        "14..18:query","19:seed","20:free","21..24:sin_cos_coordinates"
      ],
      "coordinates": "physical_at_internal_nodes; logical_site_at_ports; normalized_by_L",
      "source_query_IDs_independent_of_type": true
    },
    "tasks": {
      "remote_xor": {
        "sources": 2, "output_bits": 1, "minimum_source_output_distance": "L/4",
        "train": 2048, "validation": 512, "test": 2048,
        "updates": 250, "geometries": 1, "initializations": 2,
        "architectures": ["Grid_G","MHU_G"],
        "smoke_pass_accessible_accuracy": 0.98,
        "superiority_evidence": false
      },
      "addressed_copy_5x8_persistent": {
        "sources": 5, "payload_bits": 8, "query": "uniform_onehot",
        "minimum_each_source_output_distance": "L/4",
        "pilot_train": 8192, "pilot_validation": 1024, "pilot_test": 4096,
        "primary_score": "bit_accuracy", "secondary": ["exact_vector_accuracy","BCE"],
        "threshold_metric": 0.95, "memory_claim": false
      },
      "flood_fill_8": {
        "world": "10x10_periodic_four_cardinal",
        "free_probability_factor": [0.45,0.55,0.65],
        "factor_distribution": "equal",
        "seed": "uniform_site_forced_free",
        "target": "BFS_distance<=8_in_external_world",
        "neuronal_edges_pruned_by_obstacles": false,
        "pilot_train": 8192, "pilot_validation": 1024, "pilot_test": 4096,
        "primary_score": "BA_per_map_on_free_cells_then_mean_within_p_then_uniform_mean_over_three_p",
        "degenerate_map_score": "accuracy; report_frequency",
        "binary_threshold": 0.5,
        "secondary": ["IoU","exact_map","BCE","error_by_BFS_distance","obstacle_error"],
        "trivial_baselines": ["all_free","seed_only"],
        "positive_BCE_weight": "train_negative_positive_ratio_clipped_to_1_5"
      },
      "resource_positive_control_conditional": {
        "purpose": "assay_sensitivity_only_not_free_network_evidence",
        "channels": 5,
        "field_modes": [[1,0],[0,1],[1,1],[1,-1]],
        "field_coefficients": "8_independent_Normal_coefficients_per_channel_divide_by_sqrt(sum_squares/2)",
        "access": "type_c_sees_only_channel_c",
        "injection_sites": "all_N_nodes_at_physical_coordinates",
        "destinations": "5x5;(4*a+0.5,4*b+0.5),a_b_in0_to4;Hungarian_registration",
        "target": "mean_of_five_channels_at_query_coordinate",
        "input_storage": "only_selected_channel_value_in_its_payload_slot; others_zero",
        "input_channels": 29,
        "extra_channels": "four_query_sin_cos_at_destinations; physical_coordinates_preserved_everywhere",
        "zero_channels": "source_query_IDs_free_seed",
        "port_mask": "destinations_only",
        "T_F_parameters": 12405,
        "head": "same_shared_readout_32_to32_to1_without_sigmoid",
        "loss": "MSE", "score": "MSE_divided_by_train_target_variance_frozen",
        "family": "T",
        "train": 4096, "validation": 512, "test": 2048,
        "geometries": 3, "initializations": 2, "updates": 1000
      }
    },
    "training": {
      "batch_size": 4, "optimizer": "AdamW",
      "betas": [0.9,0.999], "epsilon": 1e-8,
      "weight_decay": 1e-4, "global_gradient_clip": 1.0,
      "pilot_lr": 0.003, "pilot_updates": 1000,
      "screen_updates": 500, "screen_geometries": 1, "screen_initializations": 2,
      "pilot_focal_geometries": 3, "pilot_initializations": 2,
      "confirm_geometries_initial": 8, "confirm_geometries_max": 16,
      "confirm_initializations": 2, "confirm_updates": 3000,
      "confirm_train": 32768, "confirm_validation": 2048, "confirm_test": 4096,
      "confirm_lr_candidates": [0.001,0.003,0.01],
      "confirm_HPO_updates_per_candidate": 300,
      "confirm_HPO_geometries": 1, "confirm_HPO_initializations": 2,
      "causal_lr_selection": "one_common_lr_per_task_pooled_calibration_scores_equal_weight_per_geometry_group_native_shuffle_pooled",
      "ecological_lr_selection": "individual_best_lr_equal_HPO_budget_separate_estimand",
      "lr_schedule": "constant",
      "weight_decay_parameter_groups": "all_trainable_parameters",
      "HPO_tie_break": "smaller_lr",
      "checkpoint_primary": "final_budget",
      "data_order": "seeded_no_replacement_per_epoch",
      "dropout": false, "AMP": false, "damage_training": false,
      "replay": false,
      "budget_policy": {
        "calibration_updates": 200, "CPU_threads": 4,
        "pilot_run_max_minutes": 30, "pilot_target_total_hours": 8,
        "if_exceeded_before_test": "all_conditions_pilot_updates500; fill_separate_tandem",
        "if_still_infeasible": "certificate_smoke_two_focal_conditions_only; broad_comparison_pending"
      },
      "baseline_selection": "strongest_per_task_mean_validation_score_of_two_screen_initializations; Grid_balanced_nominal; ties_within0.005_by_MAC_then_Grid_HU_SW_RR_Poisson",
      "confirm_minimum": "native_vs_shuffle_both_tasks_and_strongest_baseline_per_task",
      "F_G_extra_confirmation": "conditional_on_pilot_diagnostics_not_test_selection"
    },
    "mechanism_interventions": {
      "collapse": "evaluate_all_five_complete_increment_functions_at_same_state_then_interpolate_to_count_weighted_mean",
      "lambda": [0,0.5,1],
      "factor_average_allowed": false,
      "interaction": "D=(native0-shuffle0)-(native1-shuffle1)",
      "auxiliary_dependence_probability": "P(D>0.01)>=0.90",
      "floor_control": "both_scores_under_intervention_above_chance_or_trivial_by0.10",
      "relocate_functions": "20_exact_count_assignments_with_weights_fixed; move_q_and_adapter_together",
      "relocation_seed_key": 7201,
      "matched_assignment_included_if_available": true,
      "interpretation": "OOD_auxiliary; re-trained_matched_control_required_for_clean_organization_claim"
    },
    "robustness": {
      "test_examples": 512, "random_masks_per_level": 10, "lesion_centers": 20,
      "primary_protect_active_ports": true,
      "node_removal_fraction": [0,0.05,0.10,0.20],
      "localized_primary": "nearest_eligible_exact_round(q*N)_nodes",
      "localized_radius_secondary": [1,2,3,4],
      "subtype_absolute_n_400": [4,8,16],
      "subtype_n_1600_multiplier": 4,
      "insufficient_eligible_policy": "log_unavailable_not_replace",
      "subtype_fraction_secondary": [0.25,0.50,0.75],
      "edge_removal_fraction": [0,0.05,0.10,0.20,0.40],
      "bidirectional_edge_modes": ["independent_arcs","paired_undirected_edges"],
      "reconnect": false, "renormalize_neighbor_mean": true,
      "relocation": [[0.5,0],[0,0.5],[0.5,0.5]],
      "separate_end_to_end_unprotected": true,
      "primary_AUC": "trapezoidal_score_integral_q0_to0.20_divided_by0.20"
    },
    "scale_evaluation": {
      "N": 1600, "geometries": 3, "fine_tuning": false,
      "T": [16,32,64], "copy": "same5sources8bits_minimum_distanceL/4",
      "fill_primary": "20x20_world400ports_fill8",
      "fill_exploratory": "fill16_at_T32"
    },
    "metrics": [
      "task_score_loss","steps_samples_to_threshold","failure_rate",
      "training_inference_wallclock","parameters_active_edges_MAC",
      "RSS_device_peak_memory","geometry_init_variance",
      "in_out_degree_mean_variance","reciprocity","undirected_clustering",
      "directed_shortest_paths_inaccessible_fraction","finite_diameter",
      "SCC","symmetrized_algebraic_connectivity","edge_lengths",
      "coverage_functional_counterfactuals_Jacobians",
      "robustness_AUC","relocation","scale","extra_steps_stability"
    ],
    "belief_update": {
      "H_marginal_priors": {"H1":0.70,"H2":0.35,"H3":0.25,"H4":0.75,"H5":0.20,"H6":0.30},
      "mutually_exclusive": false,
      "architecture_model": "paired_delta_g_s=mu+b_g+epsilon_g_s",
      "mu_prior": {"distribution":"Normal","mean":0.0,"std":0.05},
      "sigma_priors": {"distribution":"HalfNormal","std":0.05},
      "ROPE": [-0.02,0.02],
      "quadrature": {"sigma_range":[1e-6,0.25],"nodes_per_sigma":96,"validation_nodes":192},
      "mu_prior_sensitivity_std": [0.02,0.10],
      "bootstrap_unit": "geometry",
      "mechanism_prior": 0.25,
      "qualitative_grades": ["strong_against","weak_against","neutral","weak_for","strong_for"],
      "optional_subjective_LR": [0.2,0.5,1,2,5],
      "LR_sensitivity": [0.3333333333,0.6666666667,1,1.5,3],
      "LR_is_estimated_Bayes_factor": false
    },
    "failure_analysis": {
      "reproducible_training_divergence_system_score": 0.0,
      "divergence_loss": "positive_infinity",
      "include_in_primary_posterior": true,
      "conditional_valid_run_scores_also_reported": true,
      "infrastructure_failure": "resume_same_seed_checkpoint",
      "implementation_invalidity": "stop_repair_not_evidence_against_MHU"
    },
    "decision_rules": {
      "invalid": "stop_without_evidence_against_MHU; repair_and_version",
      "continue_architecture": "P(mu>0.02)>=0.95_on_a_primary_task; no_confirmed_harm_other; noninferiority_to_strong_baseline_with_margin0.02_probability>=0.95",
      "continue_robustness": "P(AUC_difference>0.02)>=0.95; clean_noninferior_margin0.02; equal_damage_ports_protected",
      "equivalence_stop": "P(abs(mu)<=0.02)>=0.90_on_both_tasks_and_no_other_confirmed_value",
      "harm_pivot": "P(mu<-0.02)>=0.95_on_both_tasks",
      "routing_pivot": "SW_RR_gap>=0.05_tracks_accessibility_and_marks_effect_in_ROPE",
      "inconclusive": "after_max16_geometries_or_model_sensitivity; do_not_claim_equivalence",
      "mechanism_support": [
        "coverage_changes_at_used_scales","functional_specialization_is_causal",
        "native_shuffle_replicated","persists_against_local_mixing_control",
        "functional_availability_intervention_reduces_gain_with_X_edges_ports_fixed"
      ],
      "failed_learning_revision": "v0.1b_shared_GRU_if_local_optimization_fails_or_T32_if_accessibility_fails; do_not_change_both_together"
    },
    "future_gates": {
      "v0_2_hybrid": "functional_coverage_supported_and_global_routing_better",
      "plasticity": "v0.2_after_frozen_results; gates_then_degree_preserving_rewiring_then_positions",
      "3D": "after_replicated_2D_value_in_two_sizes",
      "sequence": "after_general_algorithmic_and_memory_evidence",
      "LM": "after_sequence_advantage_against_strong_RNN_transformer_cost_controls",
      "edge_computation": "separate_future_branch",
      "edge_MHU": "define_weighted_midpoint_or_incidence_capacity_field_and_control_node_statistics"
    },
    "seeds": {
      "master": 20261008,
      "pilot_geometry": [1101,1102,1103], "pilot_training": [2101,2102],
      "confirm_geometry": [3101,3102,3103,3104,3105,3106,3107,3108],
      "confirm_extension_geometry": [3109,3110,3111,3112,3113,3114,3115,3116],
      "confirm_training": [4101,4102],
      "train_val_test": [5001,5002,5003],
      "sentinel": [6101,6102,6103],
      "mark_control_key": 7101, "calibration": [9001,9002],
      "derivation": "SeedSequence_with_documented_numeric_keys"
    },
    "stack": ["Python","PyTorch","NumPy","SciPy","Matplotlib"],
    "optional_stack": ["NetworkX_for_small_graph_metrics"],
    "PyG_required": false,
    "expected_compute": {
      "MAC_per_example_step_order": 4200000,
      "MAC_per_example_forward_T16_order": 67000000,
      "training_MAC_per_update_B4_order": 800000000,
      "activation_memory_GB_order": [0.1,0.5],
      "process_RSS_target_GB": 2,
      "runtime_verified": false
    },
    "mandatory_artifacts": [
      "resolved_preregistration","code_commit_dependency_lock","geometry_hashes_certificates",
      "task_hashes_splits","graph_metrics","all_run_logs_and_failures",
      "final_checkpoints","scientific_figures_and_underlying_tables","AB_history"
    ]
  }
}
```
