# Auditoría del tratamiento geométrico y de grafos

Fecha: 2026-10-08. Contrato leído íntegramente: revisión principal, brief v2 y prompt de implementación. Ámbito: `geometry.py`, `graphs.py`, controles de marcas y tests correspondientes. Esta auditoría describe implementación y pruebas técnicas; no es evidencia a favor de MHU.

## Hallazgos estáticos

| ID | Clasificación | Localización | Impacto y actuación |
|---|---|---|---|
| G-HAMILTON | Verificado, sin contradicción | E, tabla de conteos; R.types | Hamilton entero con desempate A→E reproduce [163,85,68,50,34], [651,338,274,201,136], [2605,1351,1094,806,544]. No se modifican pesos. |
| G-BOUND | Verificado matemáticamente | F, amplitudes y cota de unión | La cota `S_union <= sum_c S_c` es correcta mediante Cauchy-Schwarz ponderado por N_c. Suprimir cada componente implica supresión de unión; se certifican ambos porque umbrales finitos no son redundantes. |
| G-PREVIEW | Elección científica deliberada | E generación §3 y R.geometry.objective; preview posterior | El preview aviar añade exclusión por tipo y tamaños distintos. No satisface el contrato congelado de repulsión común a 0,30. Se conserva separado como ilustración; nunca se carga como tratamiento certificado. |
| G-STREAMS | Omisión operativa inocua resuelta | E generación §1/§6; L seeds | SeedSequence `[20261008, geometry_seed,101]`, child de intento, y streams hijos 0 posiciones/1 marcas. Claves 103 ventanas,105 anisotropía; controles `[master,seed,7101]` y claves4/3 matched/grid. No cambia el estimando. |
| G-LBFGS | Omisión operativa inocua resuelta | E generación §4; R.geometry.lbfgs | L-BFGS explícito con historial20 y búsqueda scipy strong-Wolfe. Caps250 iteraciones y1000 evaluaciones, norma-infinito gradiente1e-8 y cambio1e-12. Fallo de búsqueda se registra; no se cambia a otro optimizer. Sólo se retorna la última iteración aceptada. |
| G-WINDOW-SEED | Omisión operativa inocua resuelta | E certificado, centros comunes | Los centros usan stream fijo6101/clave103 para todas las geometrías del mismo L. Hash y número de centros constan en certificado. El ensayo usa10000; un presupuesto menor no produce artefacto científicamente admisible. |
| G-MIN-COLLISION | Propiedad numérica explícita | F repulsión | El gradiente a r=0 es indefinido. Coincidencias exactas generan error; nunca se inventa dirección de separación. Las inicializaciones continuas y el certificado impiden admitir duplicados. |
| G-ANISOT | Elección científica deliberada y ejecución pendiente | E certificado isotropía | Cuadrupolo>0,30 es bandera descriptiva, no exclusión. Función para200 controles aleatorios disponible; evaluación de ensemble MHU y diagnóstico D4 pendientes hasta que existan múltiples geometrías. Reportes indican NOT_RUN si omitidos. |
| G-KNN | Verificado, sin reparación | E conectividad; R.graphs.causal | Se construyen 6N arcos j→i con6 vecinos entrantes. Hash SHA256 estable de ID rompe sólo empates exactos. No se simetriza, reconecta ni controla out-degree. |
| G-DELAUNAY | Omisión operativa inocua resuelta | E conectividad y R.graphs.ecological | Circuncentros en dominio fundamental, tiling3×3 y comparación traslación fija(.137L,.271L). Si radio≥L/2, comprobar5×5; ambigüedad persistente o no invariancia produce fallo. La triangulación grid degenerada utiliza su grafo cardinal nativo. |
| B_MATCHED-PAIR-POPULATION | SCIENTIFIC_BLOCKER condicional a C3 | H control de mixing; R.baselines.matched_local_statistics | No queda explícito si histogramas homotípicos cuentan todas las parejas físicas no dirigidas o sólo las aristas. Las dos poblaciones alteran las restricciones y estimando de mecanismo. Código implementa la primera interpretación y la registra, pero `long_wave_mechanism_identifiable=false` hasta decisión explícita; no ejecutar C3 ni atribuir ondas largas independientemente de mixing. El contraste nativa/shuffle sigue independiente y válido. |

## APIs e invariantes

`Geometry(points,labels,L,metadata)` congela arrays sobre buffers de bytes inmutables y metadata recursiva; hashes separados de coordenadas, marcas y geometría. `save_geometry`/`load_geometry` usan NPZ sin pickle, JSON y verificación de hashes; se rechaza sobrescribir coordenadas/marcas distintas. `Geometry.to_dict()` convierte la metadata a JSON serializable.

`generate_geometry(N,seed,kind='mhu',equal=False)` usa budgets originales6000 Adam+250 L-BFGS, hasta4 reinicios y el primer certificado admitido. Retorna y registra la geometría fallida cuando ningún intento pasa; el runner debe cerrar gates científicos. Budgets cambiados requieren `test_only=True`; estos artefactos nunca son admisibles aunque pasen números finitos. HU omite solamente términos por componente, mantiene repulsor y exige unión. Grid/Poisson se identifican como baselines sin certificado MHU.

`certify_geometry` informa espectros por A–E/unión, S medio≤0,05/max≤0,10, ventanas R4/R5≤0,65, separación≥0,299 y anti-Bragg S/N<0,50 fuera de banda y hastaπ. Scope union sólo exige unión, aunque publica componentes. Mide anisotropía sin transformarla en gate. Diagnósticos incluyen g2 homotípico/heterotípico, CDF vecinos, Voronoi toroidal, q4/q6 y déficit por tipo. `hop_type_coverage` usa campos receptivos entrantes de1/2/4/8 pasos.

`knn_graph(points,L,k=6)` y `build_graph(geometry,...)` retornan `edge_index[0]=source`, `edge_index[1]=target`, enteros (2,E). Las métricas de caminos siguen dirección source→target y declaran inaccesibles. RR6 usa mismos puntos del sustrato, acepta primer grafo conectado entre20, con arcos bidireccionales. SW causal conserva6 slots entrantes y rewiring0,10; ecológico usa4 cardinales+2 remotos≥L/4. Control de swaps preserva cada in/out-degree con100E propuestas y rechaza loops/duplicados.

Los controles conservan coordenadas y counts exactos. Annealing usa amplitudes y estadísticas de pares cacheadas, actualizaciones incrementales exactas, y recomputación antes de admisión. Propuesta uniforme de pareja de nodos con marcas distintas; temperatura logarítmica0,1→0,0001,100000 propuestas,10 reinicios. Grid igual usa `(a+2b)%5`; su orden regular es deliberadamente un baseline fuerte, no un certificado de desorden MHU. Metadatos de controles nunca heredan el certificado MHU nativo como si correspondiera a las marcas nuevas. `matched` con budget científico produce excepción `SCIENTIFIC_BLOCKER B_MATCHED-PAIR-POPULATION`; sólo se habilitan pruebas `test_only` de la interpretación explícita hasta resolver preregistro.

## Pruebas ejecutadas

Primer pase: `.venv\Scripts\python.exe -m pytest tests/test_geometry.py tests/test_graphs.py -q` produjo25 tests pasados en1,47 s. Segundo pase tras añadir inmutabilidad real y validación incremental del annealing:26 tests pasados en1,55 s. Se incluyen espectros radiales en bins físicos comunes y rebote descriptivo fuera del cutoff sin convertirlo en gate.

## Validación real acotada del seed piloto1101

Ejecutada por autorización del agente principal tras cerrar fase0, conN400/L20 y presupuesto original completo. Primer intento0 admitido;6000 Adam, luego1 evaluación L-BFGS y salida por tolerancia de gradiente sin iteraciones adicionales. Tiempo real generación+certificado2,5998565 s, total con graph metrics/guardado2,6830236 s. RSS antes78.487.552 bytes, después91.455.488 bytes; pico medido Windows working set96.583.680 bytes. No se infiere tiempo de otros tamaños a partir de esto.

| Componente | Media S banda baja | Ratio varianza promedio R4/R5 | Máximo S/N banda no optimizada |
|---|---:|---:|---:|
| A |4,669e-31|0,283185|0,055080|
| B |1,503e-31|0,273996|0,054751|
| C |3,417e-31|0,304946|0,100250|
| D |7,288e-31|0,354441|0,110370|
| E |8,413e-31|0,255274|0,144852|
| Unión |3,187e-32|0,312470|0,016850|

Separación mínima0,30000000365714663; certificado científicoPASS para clases y unión. kNN:2400 arcos,1 SCC, fracción de caminos inaccesibles0. Check independiente de gradiente sobre20 coordenadas:PASS, máximo error absoluto1,889e-18 en el punto optimizado; tests unitarios también verifican gradientes no triviales con repulsión activa. Delaunay periódico:800 triángulos/1200 aristas/2400 arcos, circunradio máximo1,464840<L/2; comprobación de traslaciónPASS. Estas pruebas verifican implementación y tratamiento finito, no utilidad neuronal ni hiperuniformidad asintótica.

Respaldo en `artifacts/geometry/mhu_N400_g1101.npz`, `mhu_N400_g1101_certificate.json`, `mhu_N400_g1101_graph_metrics.json`, `mhu_N400_g1101_timing.json` y `mhu_N400_g1101_technical_checks.json`. Hash deX:`cd6ca97d23aee99324621a6eddb8793f630b5758f73cd5c9415f264a66817b84`; hash geométrico:`c0ff8152ca3f7ce08258e7a532f54a52f83e5ab019303471176261b91d55ac2c`.

No se ha ejecutado aquí entrenamiento, piloto ni actualización AB. Validación de sentinelN1600/6400 y ensemble200 controles permanecenNOT_RUN si no figuran en logs reales.
