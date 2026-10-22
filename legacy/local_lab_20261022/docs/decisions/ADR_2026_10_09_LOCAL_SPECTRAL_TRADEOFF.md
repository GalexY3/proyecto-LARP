# Piloto local/espectral v1: construcción de efecto total

2026-10-09. Prospectivo, autorizado por «Y luego siguiente fase de exploración» en la sesión vigente. Adopta y concreta LOCAL_SPECTRAL_TRADEOFF_NEXT_DRAFT; conserva intactas las guardas y el cierre de spectral v2. No es un control residual v2 ni abre la comparación neuronal.

## Pregunta y algoritmo elegido

Sobre X/E/radios físicos/centros/conteos fijos de g1101/g1102/g1103, ¿qué puntos de cobertura y espectro consigue un único constructor con esfuerzo igual? Sólo EXPLORACIÓN de estos sustratos usados anteriormente; RNG nuevos no hacen nuevas realizaciones geométricas.

C=max_c p95(cobertura_c)/a_c, W=max_c mean_6(S_c), Q=W/.05. Optimizar Jλ=(1−λ)C+λW, λ=0,.5,1. La normalización Q del borrador situaba un shuffle en escala espectral ~20 versus C~1: se cambia explícitamente antes de ejecutar. W y C tienen escalas más comparables en shuffle; .5 tampoco implica equivalencia física, utilidad ni una frontera completa. λ0 es exactamente el rival local con esfuerzo igual: no duplicarlo ni denominarlo baseline local óptimo/fuerte garantizado.

Referencia fuerte existente: marcas nativas. Baseline de calibración: shuffle exacto común por geometría×semilla, compartido entre tres prioridades. Ni CDF, vacíos, distancias homotípicas, varianzas ni mezcla de arcos son guardas de admisión de ESTE piloto; todas se recomputan y publican con las 130 tolerancias históricas al final. Su incumplimiento impide clasificar cualquier salida como control v2.

Una única familia: simulated annealing de swaps globales. Elegir par uniforme entre diez pares de tipos y nodo uniforme de cada tipo. Counts fijos hacen el kernel de propuesta simétrico; no se afirma equilibrio/mixing durante annealing o selección de mínimo. Temperatura geométrica .02→.0002 según índice/P. Mejor J visitado incluye inicio; empate exacto retiene primera aparición. Propuesta actualiza amplitudes por delta exacta y cobertura de los dos tipos afectados; métricas completas finales desde etiquetas.

RNG: shuffle [20261009,9929,g,seed], propuestas [20261009,9931,g,seed], aceptación [20261009,9932,g,seed]. Semillas índices0,1. Compartir streams entre λ; consumir una uniforme de aceptación en CADA propuesta, incluso mejoras. Las trayectorias siguen divergentes: common random numbers no son replicaciones independientes ni aseguran idénticos nodos después de divergencia. Orden λ rotado por (índice_geometría+seed)%3. Sin seeds selectivas, reinicios, ajuste de temperatura o tareas.

## Bandas y diagnóstico

Optimizar los seis modos históricos. Registrar además ocho modos externos congelados: (1,2),(1,-2),(2,1),(2,-1),(2,2),(2,-2),(3,0),(0,3). No se usan en selección J. Registrar cada modo, máximo/medio por tipo, espectros cruzados de la banda optimizada, anisotropía descriptiva, cobertura, NN, vacíos, varianza exacta, arcos y todas las 130 desigualdades finales. Estos diagnósticos no son oportunidades independientes de evidencia y ninguna banda finita acredita k→0.

## Presupuesto y resolución previa del cap

Una sola ejecución global ≤180s: preparar ≤30s, calibrar ≤30s, 18 cadenas ≤5s cada una (≤90s) y reserva nominal de30s para métricas finales/escritura, que consumen el remanente del límite GLOBAL (no un cap separado). Supervisor aplica deadline global y de fases/cadenas. Cómputo CPU float64, cuatro threads; no alterar runtime histórico para activar GPU. N400 no justifica CUDA ni mayor batería.

Calibración: 20 evaluaciones por sustrato sobre shuffle separado [20261009,9930,g], recorrer los diez pares dos veces, propuestas desechadas, incluir generación, evaluación y serialización escalar. Resolver P=min(4096,floor(4/(2 t_max))), un cap común, con peor coste medido en los 60 casos. Reservar1s por cadena; no cambiar P tras resultados. Si P<100, cerrar RESOURCE_LIMIT sin iniciar búsqueda. Calibración y cap se publican antes del primer paso. Guardar trace por propuesta, etiquetas del mejor estado e inicio, hashes y tiempos; todas las condiciones completas o clasificación parcial/invalidada. No continuar una cadena interrumpida ni transferir presupuesto de otras fases.

## Puerta y límites

Para justificar una prueba futura de ESTE constructor, mismo λ>.0 en ambas semillas de≥2 sustratos: W≤.5W_λ0, C≤1.10C_λ0, W_externa≤1.10W_externa_λ0 y punto no dominado por nativa en (C,W). Es puerta operativa exploratoria, no test estadístico ni estimación bayesiana. Una mejora de seis modos con empeoramiento externo no satisface la puerta. Publicar todos los puntos, dominados o no; llamar a los no dominados «frente alcanzado», nunca Pareto verdadero. Si falla, cerrar este constructor y no añadir optimizadores por inercia; valorar un protocolo distinto con antecedentes y pregunta discriminante. No concluir incompatibilidad intrínseca de C y W.

Sin scores de adquisición/redes ni modificación H1–H6/C/roles. Una evaluación posterior requiere geometrías y campos/queries nuevos, ruido compartido, decoder local y espectral fuerte, selección congelada antes de scores y costes de construcción incluidos. No se ejecuta ese panel en esta fase.

## Literatura que cambia decisiones

- Wei, ACM TOG/SIGGRAPH2010, DOI10.1145/1778765.1778816, revisado: [fuente del autor](https://www.liyiwei.org/papers/noise-sig10/). Muestreo blue noise multiclase, control de conteos y espacios discretos/continuos. Rival relevante; no demuestra HU asintótica ni utilidad neuronal. Nuestro λ0 acotado no reproduce ese algoritmo.
- Jiao etal, PRE2014, DOI10.1103/PhysRevE.89.022721, revisado: [editor](https://link.aps.org/doi/10.1103/PhysRevE.89.022721). Restricciones físicas multiescala y retina aviar; no implica que marcas reetiquetadas sobre X fijo reproduzcan desarrollo biológico ni superioridad computacional.
- Shih/Casiulis/Martiniani, PRE2024, DOI10.1103/PhysRevE.110.034122, revisado: [editor](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.110.034122). FReSCo/NUFFT reduce coste de diseño espectral a O(N log N), incluye restricciones de espacio real y 2D/3D. Antecedente directo para ESCALAR; no reinventar generación espectral, no transportar garantías a nuestro problema discreto multicomponente. El arXiv2305.15693 es versión del mismo trabajo, no réplica.
- Morse etal, PRResearch2023, DOI10.1103/PhysRevResearch.5.033190, revisado: [editor](https://link.aps.org/doi/10.1103/PhysRevResearch.5.033190). GPU y precisión ampliada para configuraciones stealthy; aconseja validar precisión antes de mover certificados a GPU. No exige double-double en este piloto finito float64.

Revisión consultada2026-10-09, fuentes primarias (abstracts/editor/autor), no evaluación exhaustiva de todo prior art ni patente invocada. Kernel/temperatura/puerta son decisiones propias. Beneficio esperado: separar limitación del constructor de afirmaciones MHU, reutilizar auditoría y descubrir predicciones; novedad no reclamada. Registro AB se completará tras resultados: creencias, nuevas hipótesis, objetivo y decisión en campos separados.

Revisión prelaunch de otro agente: kernel/RNG/deltas aprobados; corrigió supervisión de cierres porfase antes del sello. Supervisor v2 separado conserva el supervisor v1 usado en auditoría nativa; valida timestamps de todos los phase_end y distingue RESOURCE_LIMIT por calibración/deadline de fallo de software.
