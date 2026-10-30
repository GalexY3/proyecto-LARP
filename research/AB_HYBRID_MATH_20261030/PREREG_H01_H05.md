# AB 3.2.1 / O1–O7 — LARP HÍBRIDOS GEOMÉTRICOS · PRERREGISTRO H01–H05
Fecha 2026-10-30. Autorización expresa: **30 ciclos AB-R libres**. Este registro propone únicamente **5** nuevos ciclos matemáticos H01–H05; los otros 25 no están consumidos ni prerregistrados. Rama research/ab-r-mhu-hybrids-20261030, base research/ab-archive-audit-20261030, HEAD histórico 5c1f00dab72a4c744b32a2a64efd298f9b24c8a9. `main` sin tocar, no merge, no CI costosa. 
**Regla A–J común**: A definición exacta, alcance/tarea e inferencia; B nula y rival competente; C prueba algebraica discriminante y contraejemplo; D código/semillas/entradas congelados antes de cualquier ejecución de verificación, sin outcome; E derivación íntegra, incluido fallo; F auditoría adversarial y límites; G comprobación simbólica/combinatoria independiente local, sin confundir con revisión formal ni replicación empírica; H actualizar priors con antecedentes; I grado separado de corrección y originalidad, N1/2/3 no automáticos; J STOP/BRANCH según R5. 
**No contar** la simple elaboración de un preregistro como ciclo ni los checks como descubrimientos. Estudios previos S01–S20 y M01–M18 son antecedentes; no duplicarlos. Todos los teoremas son condicionales a configuraciones finitas, 1D y clases etiquetadas, no prueban hiperuniformidad asintótica, coste computacional ni IA general. El auditor no puede usar datos externos o métricas visuales. Sin holdout externo.
## H01 — Tradeoff exacto entre CVT y aliasing fuera de banda
A: n par >=4, puntos (p_j=j/n+(-1)^j ε) en círculo unitario, ε∈[0,1/(4n)], cuantización 1D (Q=∫d(x,P)^2 dx), S_n = |n^{-1} Σe^{2πin p_j}|².
B: supuesto falso de que quitar el alias k=n puede hacerse sin deteriorar Q; rival cuadrícula regular ε=0.
C/falsador: buscar curva cerrada Q(ε) y S_n(ε); Q=1/(12n²)+ε² y S_n=cos²(2πnε). Para (J=λ(Q-Q_0)+w S_n), ε=0 no es mínimo local si λ<4π²n²w. Verificar igualdad exacta y umbral por expansión; si falla, refutar/registrar.
D: n=8, ε=1/128 y 1/32 como muestras aritméticas; no optimización posterior.
## H02 — Nulo espectral multiclase con cuotas exactas
A: fases (z_i=e^{2πikx_i}) fijas, k≠0, N objetos, color aleatorio con cuotas n_c. (ρ_c=Σ_{i:color=c} z_i), (η_c=ρ_c-(n_c/N) Z).
B: falsa independencia entre clases o cero covarianza cuando la unión tiene S=0.
C/falsador: (Eη_c \barη_d= [N/(N-1)](n_c δ_{cd} - n_c n_d/N)[1-|Z|²/N²]). Verificar por enumeración de todas las asignaciones de cuotas (2,1,1) en N=4 y un modo con Z=0. Construir matriz hermítica PSD de rango m−1 si amplitudes no constantes.
D: N=4, z=(1,i,-1,-i), n=(2,1,1), exact rational/sympy.
## H03 — Diseño robusto minimax exacto para dos sensores y dos frecuencias
A: dos posiciones 0 y Δ en círculo, Δ∈[0,1/2], factor (S_k=|[1+e^{2πikΔ}]/2|²), modos k=1,2, potencia de señal desconocida en simplex q. Riesgo máximo = max(S1,S2).
B: selección de ponderación inversa (w=(4/5,1/5)) de MHU-v2 necesariamente minimax; rival minimax del máximo sin prior.
C/falsador: con (x=cos²(πΔ)), (S1=x,S2=(2x-1)²); global minimax =1/4 en x=1/4 (Δ=1/3), mientras ponderación 4:1 minimiza en x=0 (Δ=1/2) y tiene peor caso 1. Probar rigurosamente sobre intervalo [0,1].
D: evaluación simbólica/intervalos, sin seleccion adaptativa.
## H04 — Cuello de botella para especialistas por vecindario de grado seis
A: N=400, cuotas (163,85,68,50,34), vértice focal de clase c, d=6 vecinos distintos elegidos uniformemente sin reemplazo entre los otros N−1 nodos. Evento: vecinos contienen al menos una unidad de las cinco modalidades.
B: interpretar heterotipia de aristas ~74% como cobertura de cinco modalidades; rivales IID, nulo de etiquetas permutadas, mejor diseño determinista con ≥5 vecinos.
C/falsador: fórmula inclusión-exclusión (P_c =Σ_{J⊆[5]} (-1)^{|J|} C[(N−1)-Σ_{j∈J}(n_j-1_{j=c}), d]/C(N-1,d)), convenciones C(a,d)=0 si a<d. Estimar P por clase y promedio focal Σ n_c P_c/N; nunca inferir comportamiento de grafos reales con vecinos geométricos a partir de nulo. Probar identidad con enumeración combinatoria o DP multinomial hipergeométrica.
D: N=400, d=6, n exactos de proyecto.
## H05 — Obstrucción aritmética más fuerte a subretículas CVT óptimas
A: círculo 1D, N=12 puntos en una retícula unión CVT/minimax óptima, cuotas tres especies n=(6,4,2), cada especie debería ser retícula propia óptima de paso 1/n. S07 histórico prueba que n_c|N es necesario; preguntar si es suficiente.
B: hipótesis alternativa: cuando cada n_c divide N, existe siempre una partición en cosets de retículas óptimas.
C/falsador: cada clase reticular de tamaño n_c es un coset módulo q_c=N/n_c. Dos cosets módulo q_a,q_b se intersectan si y solo si sus residuos coinciden módulo gcd(q_a,q_b) (CRT). Para 6 y4, q=2 y3, gcd=1; sus cosets siempre se solapan, impidiendo partición 6+4+2. Probar generalidad y verificar los 2×3 cosets con conjuntos finitos.
D: N=12; una cota necesaria pareja es gcd(q_a,q_b)>1 para toda pareja de clases con n_a+n_b≤N, no suficiente globalmente.
## Gobernanza y separación
Bloque efectivo 5 preguntas con derivaciones y herramientas reusables; si un objetivo cae por error matemático, registrar invalidez sin maquillar. La investigación previa S07/S08 y S13 y S16/S17 son antecedentes: H01/H02/H03/H04/H05 solo pueden reclamar **extensiones matemáticas condicionadas**, nunca cinco descubrimientos científicos nuevos. No escalar a N2/3 sin originalidad literaria y observación independiente. CT2 ramas heredadas conservadas hasta evidencia pertinente; no subir por número de pruebas.