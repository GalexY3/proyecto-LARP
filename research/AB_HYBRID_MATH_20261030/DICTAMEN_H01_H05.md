# LARP · AB-R matemática, primera rama híbrida H01–H05

**Fecha:** 30 de octubre de 2026. **Repositorio privado:** `GalexY3/proyecto-LARP`. **Rama:** `research/ab-r-mhu-hybrids-20261030`. **Autorización:** hasta 30 ciclos AB-R libres; **5 contrastes deductivos ejecutados, 25 autorizados pendientes**. Sin fusión a `main` ni CI costosa.

## Identidad de la investigación

El contrato de hipótesis y criterios de refutación se congeló **antes** del cálculo en GitHub, commit `12083759d28527968d75e7879568315793c44fad`. El código **completo** se congeló antes de ejecutar, commit `3738712ff153307fa0683a3e6322fcec69c2065c`, blob Git `4e42be1b22095ea88767e0fb00abfb865b85ceb9`, SHA256 `5e6487a901111d346a7859633afbfac1d7ac5c5d3868d4d3337f744e1f7e2086`. Resultado JSON SHA256 `57a86c7774be32ef3ad732721eb75f3ac7d6f803abd549352dea1142cde35f7a`. Cinco comprobaciones pasaron y una segunda ejecución, en otro directorio del mismo equipo, produjo los **mismos bytes**. No se ha verificado un clon limpio desde otro equipo, un asistente formal de pruebas o la revisión por un matemático independiente. El código finito **no sustituye** a los argumentos generales.

## H01 — Frontera exacta entre cuantización y un pico de aliasing

**A (problema):** Círculo unitario, n puntos (n par), configuraciones `p_j = j/n + (-1)^j ε` para `0 ≤ ε ≤ 1/(4n)`. El error de cuantización por vecino más próximo es `Q(P)=∫_0^1 dist(x,P)^2 dx`. El adversario espectral es la potencia normalizada `S_n(P)=|n^{-1} Σ_j exp(2π i n p_j)|²` en el modo resonante n.

**B (rival):** Cuadrícula regular ε=0, óptima para Q, frente a familia perturbada que puede suprimir una frecuencia resonante. Una hipótesis excesiva diría que eliminar el alias no empeora la cobertura.

**C–E (demostración y verificación):** Los n intervalos entre puntos tienen longitudes alternas `g_±=1/n±2ε`. El error exacto es `Q=Σ g_j³/12 = 1/(12n²)+ε²`. En k=n, las fases de las dos paridades difieren en signo: `n^{-1}Σ exp(2π i n p_j)=cos(2πnε)`, luego `S_n=cos²(2πnε)`. En ε=1/(4n), la resonancia desaparece, pero `Q` aumenta exactamente `1/(16n²)`; en ε=0, la resonancia vale 1 y `Q` es mínimo. Para objetivo híbrido `J=λ(Q-Q0)+w S_n`, la curvatura en ε=0 es `J''(0)=2λ−8π²n²w`: el patrón regular deja de ser mínimo local si `λ<4π²n²w`. Se verificaron configuraciones n=8, ε∈{0,1/128,1/32}.

**F–I (auditoría):** Este es un subespacio constructivo de configuraciones, no el óptimo general de todos los patrones ni un certificado MHU asintótico. El resultado amplía la familia alternante estudiada en S09 y la óptima CVT 1D de S08: **no es un teorema original demostrado**. No aporta resultados visuales, ahorro físico ni superioridad neuronal. N1 nuevo=0; N2=N3=0.

**H (prior):** Reforzar la separación entre cobertura CVT y resonancia alta: una penalización espectral puede mejorar un modo sacrificando cuantización. **J:** CERRAR H01; usar curva exacta como control de futuros híbridos multibanda.

## H02 — Matriz exacta de covarianzas entre cinco especies con cuotas fijas

**A (problema):** Coordenadas fijas X, fases unitarias `z_i=e^{2πikx_i}`, N sensores, m clases con cuotas n_c. Etiquetado uniforme entre todas las asignaciones con cuotas fijas. Definir `Z=Σ z_i`, `ρ_c=Σ_{i:clase c}z_i` y concentración `η_c=ρ_c-(n_c/N)Z`.

**B:** El control ingenuo trata las m clases como independientes; rival competente: permutación de etiquetas **sin reemplazo** y espectro de unión fijo.

**C–E:** Por la covarianza hipergeométrica de la suma de una muestra finita y porque `|z_i|=1`, resulta la matriz hermítica exacta

`E[η_c conjugate(η_d)] = [N/(N−1)] [n_c δ_cd−n_c n_d/N] [1−|Z|²/N²]`.

La suma de todos los η_c es cero, por lo que la matriz tiene el vector constante como vector nulo. Con cuotas positivas y fases no constantes, su rango es m−1. Los términos fuera de la diagonal son **negativos**: no hay independencia estadística entre clases. Se enumeraron las 12 permutaciones distintas para N=4, cuotas (2,1,1), fases (1,i,−1,−i), y se obtuvo diferencia exactamente cero dentro de la aritmética utilizada. La matriz resultante tiene diagonal `(4/3,1,1)` y covarianzas fuera de diagonal `(−2/3,−2/3,−1/3)`.

**F–I:** Esta fórmula es un **nulo condicional para reetiquetar el mismo sustrato**; no se aplica cuando las posiciones de los sensores también cambian o se condiciona el empaquetamiento a las etiquetas físicas. Los factores de estructura parciales y las variables de concentración tienen antecedentes en Bhatia–Thornton y literatura multicomponente; es una extensión del control diagonal S17, **no una primicia científica demostrada**. N1=N2=N3 nuevos=0.

**H:** Actualizar P-HYBRID-02: cualquier métrica de coordinación entre clases debe comparar contra la **matriz completa** bajo cuotas fijas, no contra cinco espectros marginales independientes. **J:** CERRAR H02; candidato para instrumentación de falsación con etiquetas verdaderamente alternativas.

## H03 — La prioridad MHU-v2 de bajas frecuencias puede ser peor en minimax

**A:** Dos sensores en posiciones (0,Δ), Δ∈[0,1/2], señales cuyo poder desconocido está concentrado entre k=1 y k=2 con pesos q en el simplex. Para el error de la media de Fourier, el riesgo adversarial es `sup_{q≥0, Σq=1} Σ q_k S_k = max(S1,S2)`.

**B:** Rival de ponderación espectral inversa al cuadrado como MHU-v2: normalizar `(1,1/4)` da `(4/5,1/5)`; contraste frente a un diseño explícitamente robusto.

**C–E:** Con `x=cos²(πΔ)`, `S1=x`, `S2=(2x−1)²`. Para x≤1/4 se cumple `(2x−1)²≥1/4`; para x≥1/4 se cumple `x≥1/4`. En x=1/4 ambas son 1/4, de modo que **el minimax global exacto es 1/4**, alcanzado por Δ=1/3. En cambio, `4S1/5+S2/5 = 4x²/5+1/5` se minimiza en x=0, Δ=1/2, donde `(S1,S2)=(0,1)` y el peor riesgo es 1. Las operaciones simbólicas coincidieron.

**F–I:** El resultado no afirma que el generador v2 real alcance uno u otro diseño, ni que el modo k=2 tenga probabilidades altas en fotografías reales; solo identifica el costo de asumir un prior espectral incorrecto. Diseño minimax para **dos modos, dos sensores, media de señal**; no visión general. El teorema se apoya en optimización clásica de Fourier y es una extensión del S13 histórico. N1=N2=N3 nuevos=0.

**H:** P-HYBRID-03: cuando el espectro de señal es incierto, considerar `min_P max_{k∈K} S_P(k)` o `min_P sup_{q∈Q} Σq_k S_P(k)` como rival adversarial, en lugar de conceder superioridad a `1/|k|²`. **J:** CERRAR H03; ramificar hacia bandas y presupuestos físicamente justificables.

## H04 — Acceso local simultáneo a cinco especialistas con grado entrante seis

**A:** `N=400`, clases `(163,85,68,50,34)`, nodo focal de clase c, seis vecinos distintos elegidos uniformemente sin reemplazo entre los otros 399. Evento: en el vecindario están representadas **las cinco clases**.

**B:** Rival nulo que mide solo fracción de aristas heterotípicas; esto no garantiza cinco clases distintas y no es un control suficiente para una red modular.

**C–E:** Tras quitar el nodo focal, quedan poblaciones `n'_j=n_j−1{j=c}`. El principio de inclusión-exclusión da la probabilidad exacta

`P_c = [Σ_{J⊆{1,...,5}} (−1)^|J| C(399−Σ_{j∈J} n'_j,6)] / C(399,6)`.

Como hay seis vecinos y cinco clases presentes, necesariamente el patrón de conteos es una clase con dos vecinos y las otras con uno. Esto da la expresión independiente

`P_c = [Σ_j C(n'_j,2) Π_{h≠j}n'_h] / C(399,6) = 197 Π_j n'_j / C(399,6)`.

Ambas fórmulas dan exactamente el mismo número racional. Promediando por clase focal con peso n_c/400, la probabilidad es **0,0577384622594 = 5,773846 %**. Los valores por clase focal están entre **5,675 % y 5,811 %**.

**F–I:** Es un resultado sobre vecindarios **uniformemente aleatorios** con grados exactamente seis, no una medida de los grafos kNN reales de LARP. Un diseño consciente de las etiquetas podría cubrir las cinco clases con seis aristas; una estrategia indiscriminada no lo garantiza. Tampoco demuestra que todas las modalidades sean necesarias para cada tarea. No es hallazgo independiente de combinatoria hipergeométrica. N1=N2=N3 nuevos=0.

**H:** P-HYBRID-04: distinguir heterotipia media, cobertura completa de modalidades, calidad/rango de mensajes y presupuesto de aristas. **J:** CERRAR H04; posible pivote a routing multiclase con controles GraphGPS, expander y cobertura de roles.

## H05 — Divisibilidad individual no basta para optimizar todas las especies

**A:** N=12 posiciones en retícula circular regular y tres clases de tamaños (6,4,2), con sumas 12. En el informe previo S07 se identificó la condición necesaria `n_c | N` para que una especie óptima sea una subretícula del patrón global óptimo. ¿Es suficiente para todas las especies a la vez?

**B:** Nula fuerte: si las tres cuotas dividen 12, existe una partición óptima simultánea.

**C–E:** Una subretícula de tamaño `n_c` corresponde a un coset de residuos módulo `q_c=N/n_c`. Dos clases de pasos q_a,q_b se intersectan si y solo si sus residuos coinciden módulo `gcd(q_a,q_b)` (teorema chino del resto); cuando `gcd(q_a,q_b)=1`, **todos los cosets de las dos clases se intersectan**. Para las clases 6 y4, q son 2 y3, coprimos; cualquier coset de seis puntos y cualquier coset de cuatro comparten exactamente dos posiciones. Se enumeraron las seis parejas posibles y **todas se intersectan en dos puntos**. No existe la partición óptima simultánea (6,4,2) aunque 6, 4 y 2 sí dividan 12.

**F–I:** Resultado unidimensional con subretículas **exactamente regulares** y cuotas rígidas, no prueba que patrones 2D/3D irregulares no alcancen buena cobertura ni que el genoma aviar tenga imposibilidad general. El argumento usa teoría elemental de grupos cíclicos y CRT: **no reivindicar originalidad matemática**. N1=N2=N3 nuevos=0.

**H:** P-HYBRID-05: la compatibilidad de cuotas de especialistas depende de divisibilidad **y de intersección de cosets**, no solo del criterio individual de S07. **J:** CERRAR H05; considerar objetivo híbrido con tolerancias óptimas en vez de igualdad exacta imposible.

## Auditoría transversal AB / O3–O7

- **Validez interna:** los cinco ejemplos condicionados tienen demostraciones explícitas y controles computacionales de coherencia; ningún check verifica automáticamente teoremas generales fuera de sus premisas.
- **Rivales:** CVT/retícula, reetiquetado hipergeométrico, minimax con prior desconocido, routing funcional y aritmética de subgrupos. **No se ha ejecutado Wei 2010 ni un modelo neuronal.**
- **Novela vs antecedente:** resultados derivados de aritmética, Fourier, muestreo, covarianza de muestras finitas y CRT; los antecedentes más específicos son los resultados ya archivados S07–S17, Li-Yi Wei (SIGGRAPH 2010) y Krause et al. (JMLR 2008). Bhatia–Thornton es literatura antigua sobre factores parciales de estructura. No hay un hallazgo de nivel 2/3 ni una nueva validación empírica.
- **Unidad de confirmación:** 5 pruebas simbólicas/numéricas auxiliares y una reproducción exacta local, sin observaciones empíricas nuevas. La inspección matemática interna no equivale a certificación por pares.
- **Priorización futura:** H04 permite una prueba experimental de cobertura local y de routing; H03 sugiere un diseño robusto que use un conjunto de espectros adversarios; H02 proporciona un nulo de etiquetas condicionado al sustrato; H01/H05 imponen fronteras de factibilidad para objetivos híbridos.
- **CT2:** sin cambio automático de ninguna rama. **P-HYBRID-01 a 05** se registran como mejoras metodológicas/condicionales, no como evidencias que suban madurez. Propuesta inicial de línea híbrida condicionada: referencia histórica 24/100, pendiente de una estimación nueva con datos y contraprueba Wei real.
- **Contabilidad:** grant 30; `EXPERIMENTAL_AB=0`, `FORMAL_AB_RUN=5` (H01–H05), `INVALID=0`, `PLANNING=0`, **saldo 25**. Nada se ha fusionado a main.

## Fuentes de contexto y novedad

- Código original: `src/BR30_dynamic/original/scale3d_geometry.py` y `scale3d_geometry_v2.py`; historia: `research/AB_MHU_SISTERS_20261030/INFORME_S01_S20.md`.
- Wei (2010), *Multi-Class Blue Noise Sampling*: https://www.liyiwei.org/papers/noise-sig10/
- Krause, Singh y Guestrin (2008), *Near-Optimal Sensor Placements in Gaussian Processes*: https://jmlr.org/papers/v9/krause08a.html
- Bhatia–Thornton / factores de concentración: https://journals.iucr.org/j/issues/2021/01/00/gj5253/index.html
- Análisis previo del proyecto: `legacy/local_lab_20261022/docs/INDEPENDENT_SPECTRAL_MATCHING_NEXT.md` y `docs/AB08_CROSSPHASE_20261022/DICTAMEN_AB08.md`.
