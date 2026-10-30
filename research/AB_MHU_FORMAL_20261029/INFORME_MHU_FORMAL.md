# LARP–MHU: límites de optimalidad, robustez y composición de especialistas

**Campaña:** AB 3.2.1 / O1–O7. **Fecha:** 29-10-2026. **Rama:** `research/ab-mhu-formal-20261029` (derivada de `research/ab-vision-mhu-20261029`). **Hipótesis y falsadores congelados prospectivamente** antes del análisis de demostraciones en commit `1c27c5d2679f876cbda60987b1152246a72a75c9`. 18 plazas matemáticas asignadas a M01–M18, cada una con prueba argumental y contraejemplo o auditoría formal. No se trata de 18 teoremas originales ni de 18 replicaciones experimentales. No se realizaron experimentos visuales nuevos ni se accedió a cubos CAVE.

## Dictamen de una página

1. **No existe superioridad universal de MHU como sistema de adquisición o de inferencia.** Los resultados M07–M10 y M17 construyen dominios donde la geometría regular alcanza el minimax, donde el diseño óptimo se concentra en extremos, o donde cualquier distribución pierde alguna familia de funciones. La palabra *superior* necesita fijar clase de señales, riesgo, número de mediciones, ruido y costo.
2. **Hay garantías estructurales positivas, pero no garantías neuronales.** Si las cinco subpoblaciones son HU, cualquier unión de ellas también es HU (M01/M04). Las correlaciones interclase pueden cambiar radicalmente el espectro de la unión sin cambiar los cinco espectros individuales (M05/M06). No se deduce precisión visual, ni robustez funcional, ni menor consumo.
3. **Un fallo aleatorio de sensores puede eliminar exactamente la característica que se pretende explotar.** La retención independiente con probabilidad p añade ruido estructural `1-p` a la densidad espectral, aunque el patrón original fuera HU (M03). No contradice la conservación frente a supresión completa de clases (M04).
4. **La ventaja de MHU en un sistema con cinco modalidades es necesariamente *condicional a las estadísticas conjuntas de las señales*.** El error cuadrático espectral es una forma cuadrática `a* C a` (M11/M12); con covarianza desconocida adversarial, la cancelación favorable entre clases desaparece como garantía minimax (M18). Esto produce una pregunta científicamente más útil: estimar o acotar el conjunto admisible de covarianzas multisensor, y diseñar frente a ese conjunto con rivales potentes de muestreo óptimo.
5. **Superponer expertos previamente entrenados es posible, pero la geometría no los alinea ni crea información.** Cinco filtros RGB construidos a partir de tres canales tienen rango ≤3 (M13); el procesado determinista no supera a la observación completa bajo el mismo presupuesto de decisión (M14); dos módulos correctos pueden anularse si se mezclan representaciones ocultas incompatibles (M15). La fusión estadísticamente óptima depende de incertidumbres y covarianzas, no de la etiqueta MHU (M16).

### Qué significa `MHU` aquí

En un proceso de puntos estacionario, *hiperuniformidad* significa `Var[N(W_R)] = o(|W_R|)` al crecer la ventana adecuada (típicamente esferas; la forma y orientación importan en redes cristalinas). *Multihiperuniformidad* significa que **cada subpoblación identificada** es hiperuniforme (y, por lo tanto, su unión finita). No confundir un objetivo espectral pequeño en 160 posiciones con un certificado asintótico de MHU. El estudio original Jiao et al. 2014 ya documenta hiperuniformidad por tipo y de la unión, y describe conservación tras pérdida de clases completas.

## BLOQUE I — Geometría y destrucción/conservación de MHU

### M01 · Teorema de clausura por unión finita
**Enunciado.** Sean `X_1,…,X_m` procesos de puntos conjuntamente definidos en R^d, con m finito y para la misma familia de ventanas W_R, `Var N_i(W_R)=o(|W_R|)` para todo i. Entonces `Var Σ_i N_i(W_R)=o(|W_R|)` incluso si los tipos están correlacionados.

**Demostración.** Escribimos `Z_i=N_i−E N_i`. Por Cauchy–Schwarz `|Cov(Z_i,Z_j)|≤sqrt(Var Z_i Var Z_j)`. En consecuencia,

`Var Σ_i N_i = Σ_i,j Cov(Z_i,Z_j) ≤ (Σ_i sqrt(Var N_i))²`.

Como m es finito, cada raíz es `o(sqrt(|W_R|))`, de modo que el cuadrado total es `o(|W_R|)`. QED.

**Falsador auditado:** ni correlaciones arbitrariamente negativas ni positivas admisibles pueden violar Cauchy–Schwarz. **Límite:** m no puede crecer sin cota con R; ventana y definición del HU deben ser comunes. **Novedad:** conocida/implícita en definición de MHU.

### M02 · El inverso es falso: una unión HU puede tener especies no HU
**Construcción.** Tomemos una retícula 1D desplazada por una fase uniforme, de modo que su conteo en una ventana larga tiene fluctuación acotada. Coloreemos cada nodo, de forma independiente, como A con probabilidad q∈(0,1) y B con 1−q. La unión sigue siendo la retícula HU. Condicional al número original N de nodos, `N_A|N~Binomial(N,q)` y

`Var N_A = q² Var N + q(1−q) E N`.

El segundo término es `Θ(|W|)`, así que A no es HU, ni tampoco B. **Conclusión:** «total HU» NO implica «multihiperuniforme»; no basta con colorear al azar una distribución buena. **Novedad:** construcción estándar por marcas Bernoulli, no propia de LARP.

### M03 · Pérdidas individuales aleatorias destruyen HU estricta
**Enunciado.** Sea X HU estacionario con densidad ρ>0 y retengamos cada punto independientemente con probabilidad p, 0<p<1. Para cualquier ventana W,

`Var N_p(W)=p² Var N(W)+p(1−p) E N(W)`.

**Prueba.** Ley de varianza total: `E[Var(N_p|N)]=p(1−p)E N` y `Var(E[N_p|N])=p² Var N`. Dividiendo por `E N_p=p E N` y tomando límite de grandes ventanas se obtiene un piso normalizado `1−p`. Con la convención habitual del factor de estructura no singular, `S_p(k)=1−p+p S(k)`; por ello `S_p(0)=1−p>0`, bajo las hipótesis usuales de continuidad/ausencia de anomalías. **Límite:** pérdida IID, no caídas espacialmente coordinadas. **Novedad:** analizada previamente, p.ej. en *Effect of imperfections on the hyperuniformity of many-body systems* (2018).

### M04 · Supresión completa de una o varias especies preserva HU
**Enunciado.** En una MHU de m clases estacionarias, retirar cualquier subconjunto **completo de clases** y dejar al menos una conserva HU en el resto, en la misma familia de ventanas.

**Prueba.** El resto es la unión finita de subpoblaciones que eran individualmente HU; aplicar M01. **Importante:** esto no es resistencia funcional. Si quitas todos los receptores sensibles al azul, la cobertura geométrica sigue siendo HU, pero has perdido la medición del azul. **Relación con M01:** corolario deliberado; no se contabiliza como hallazgo independiente nuevo. Este hecho aparece explícitamente en Jiao et al. 2014.

### M05 · Matriz espectral multiclase y una cota que no implica superioridad
**Marco finito.** Para una frecuencia `k≠0` y clases con fracción `f_i=N_i/N`, definamos `Z_i(k)=N_i^(−1/2) Σ_{x∈X_i} e^{−i k·x}` y `H_ij(k)=E[Z_i(k) conjugate(Z_j(k))]`. La matriz H es hermítica semidefinida positiva porque `u*Hu=E|Σ_i conjugate(u_i)Z_i|²≥0`. Poniendo `v_i=sqrt(f_i)`,

`S_total(k)=v* H(k) v = Σ_i f_i H_ii + 2 Σ_{i<j} sqrt(f_i f_j) Re(H_ij)`.

Además `0≤S_total≤(Σ_i sqrt(f_i H_ii))²`, por Cauchy–Schwarz. **Resultado:** los cinco espectros `H_ii` no determinan el espectro agregado; las correlaciones cruzadas importan. **Límite:** la ventaja espectral en k no es una ventaja en error de ninguna tarea sin fijar la señal (véase M11/M12).

### M06 · Las fases relativas pueden invertir la potencia conjunta
**Construcción exacta.** Sean dos conjuntos de puntos del mismo tamaño cuyos factores de amplitud en modo k son `A` y `A exp(iφ)` tras trasladar una clase. Los espectros propios son siempre `|A|²`; la unión tiene amplitud `(A+A exp(iφ))/2` y potencia `|A|² cos²(φ/2)`. Para φ=0 obtenemos `|A|²` y para φ=π obtenemos 0, **sin cambiar un solo espectro intraclase**.

**Interpretación:** la coordinación entre capas *puede* ser importante. **Advertencia:** el efecto es sobre una frecuencia concreta, no sobre aprendizaje ni sobre toda la banda de imágenes. Además, desplazar sensores cambia cobertura física y puede violar restricciones locales; no hay garantía de realizabilidad para todos los modos a la vez.

## BLOQUE II — Contraejemplos rigurosos de «MHU siempre mejor»

### M07 · Diseño regular es minimax exacto para cobertura Lipschitz en 1D
**Modelo.** Clase `F_L={f:[0,1]→R: |f(x)−f(y)|≤L|x−y|}`; n lecturas exactas de f en puntos P; pérdida supremo del error sobre x y f, con estimador basado solo en lecturas.

**Cota geométrica.** Si el radio de cobertura es `r(P)=max_{x∈[0,1]} min_{p∈P}|x−p|`, las n bolas de radio r cubren el intervalo de longitud 1: `2nr≥1`. Las posiciones `p_j=(2j−1)/(2n)` alcanzan `r=1/(2n)`.

**Cota estadística.** Funciones `f_±(x)=±L dist(x,P)` pertenecen a F_L, coinciden en todas las observaciones (son 0), pero difieren `2Lr(P)` en un punto lejano. Cualquier estimador falla al menos Lr(P) en una de las dos. El vecino más cercano nunca supera Lr(P), de modo que el minimax óptimo es exactamente `L/(2n)` y lo alcanza la cuadrícula centrada. **No puede existir una mejora estricta universal de MHU frente a ese control** para este problema y costo. **Límite:** 1D, norma uniforme, clase Lipschitz y sensores puntuales.

### M08 · Empate inevitable para señales gaussianas isotrópicas
**Modelo.** `X~N(0,I_d)`, n observaciones lineales exactas `Y=AX` con A de rango n<d; reconstrucción posterior óptima bajo pérdida cuadrática.

**Demostración.** `Cov(X|Y)=I_d−Aᵀ(AAᵀ)⁻¹A`, que es un proyector ortogonal de rango d−n. Su traza, equivalente al riesgo Bayes cuadrático de reconstruir X, es `d−n` sin depender de las posiciones/orientaciones de los n vectores de medida. **Ninguna geometría estrictamente gana bajo este prior isotrópico y medidas lineales igualmente exactas.** **Límite:** prior isotrópico, observación sin ruido, reconstrucción Bayes y mismo rango; con anisotropía o ruido, la posición sí puede importar.

### M09 · Una distribución concentrada puede superar a la regular
**Modelo.** `y_i=α+β x_i+ε_i`, con ε_i IID N(0,σ²), x_i∈[0,1], n par; queremos estimar β sin conocer α.

**Derivación.** La información Fisher efectiva sobre β después de eliminar la ordenada es `I_β=(1/σ²)Σ_i(x_i−x̄)²`. Por la cota clásica de Popoviciu, `Σ_i(x_i−x̄)²≤n/4`, igualdad al medir la mitad de veces en x=0 y la mitad en x=1. Para una cuadrícula de puntos medios `Σ(x_i−x̄)²=(n²−1)/(12n)`. Con n=4: extremos=1, cuadrícula=0,3125, **3,2 veces más información** usando extremos. **Límite:** observaciones repetidas con ruidos independientes permitidas; modelo afín con intercepto y estimando pendiente, no reconstrucción general de imágenes.

### M10 · Imposibilidad de reconstrucción universal de todas las imágenes suaves
**Modelo.** Conjunto finito P={p_1,…,p_n} de puntos en [0,1]. Definamos `φ(x)=∏_j(x−p_j)²`, función polinómica C∞, no idénticamente cero y φ(p_j)=0. Normalizando `h(x)=φ(x)/max_{[0,1]}φ(x)` y fijando 0<ε≤1/2, las señales `f_±(x)=1/2±ε h(x)` son lisas, permanecen en [0,1] y producen exactamente las mismas lecturas `1/2` en P, pero difieren en el dominio.

**Conclusión:** para una clase de funciones suaves no restringida más allá de C∞ y rango acotado, ninguna disposición de un número finito de sensores permite reconstrucción exacta universal. **Límite:** el teorema no impide éxito en un subespacio bandlimitado o bajo un prior estadístico realista.

### M11 · Fórmula exacta del error espectral de cuadratura
**Modelo.** En toro [0,1]^d, `f(x)=μ+Σ_{k∈K} b_k cos(2πk·x+φ_k)`, con frecuencias no nulas, fases φ_k IID uniformes y amplitudes b_k conocidas. `A_P(k)=n⁻¹Σ_{x∈P} exp(2π i k·x)`. Estimador μ_P es promedio de f en P.

**Prueba.** La media real de cada coseno sobre el toro es 0. El error de cuadratura es `Σ b_k Re(exp(iφ_k)A_P(k))`. Cada término tiene esperanza 0 y varianza `b_k² |A_P(k)|²/2`; los términos son incorrelados por independencia de fases. Por tanto,

`E[(μ_P−μ)²]=(1/2)Σ_{k∈K} b_k² |A_P(k)|²`.

**Consecuencia:** si una distribución anula los modos que realmente contienen la energía de la señal, obtiene error nulo en esta tarea; si solo suprime modos irrelevantes, no tiene ventaja. **Novedad:** identidad estándar de muestreo/cuadratura espectral, no un nuevo teorema MHU.

### M12 · Cuando hay varios tipos de señales, importa su covarianza
**Modelo.** Para una frecuencia k, sean `ξ=(ξ_1,…,ξ_m)` coeficientes aleatorios de las señales por modalidad, con `E ξ=0` y `C=E[ξξ*]` PSD. Sean `a_i` respuestas geométricas complejas ponderadas para cada modalidad. El error `e=a*ξ` satisface

`E|e|²=a* C a`.

**Caso explícito:** a=(1,1), varianzas unitarias: si modalidades independientes C=I, riesgo=2; si correlación perfectamente positiva C=ones, riesgo=4; si perfectamente anticorrelacionadas C=[[1,−1],[−1,1]], riesgo=0. **Una geometría que ayuda a señales correlacionadas puede no hacerlo a independientes/anticorrelacionadas**. Supresión espectral conjunta de *una suma preelegida* no garantiza un mínimo de este riesgo para todas las C.

## BLOQUE III — Cinco modalidades, expertos y límites informativos

### M13 · Cinco filtros RGB no representan cinco dimensiones espectrales
**Modelo del anterior C02.** Observamos R, G, B, (R+G)/2, (G+B)/2. La matriz de filtros es

`F = [[1,0,0],[0,1,0],[0,0,1],[1/2,1/2,0],[0,1/2,1/2]]`.

Las tres primeras filas forman I_3 y las dos últimas son combinaciones lineales; por tanto `rank(F)=3`, no 5. **Un sistema con cinco etiquetas no dispone de cinco modalidades ópticas independientes**, aunque recoger diferentes combinaciones en *posiciones espaciales distintas* sí puede aportar más información para reconstruir un campo. **Auditoría:** rango exacto confirmado con SymPy.

### M14 · Una reordenación determinista no crea información disponible
**Modelo.** X es la imagen completa, Y etiqueta o propiedad de interés, T(X) un preprocesado o muestreo determinista, misma pérdida ℓ y sin restricción adicional a la familia de funciones de decisión. Cualquier regla δ(T(X)) puede implementarse como regla sobre X mediante composición δ∘T. Por ello,

`inf_g E ℓ(Y,g(X)) ≤ inf_δ E ℓ(Y,δ(T(X)))`.

Es el principio de procesamiento de datos desde teoría de decisiones; adicionalmente `I(Y;T(X))≤I(Y;X)` cuando están definidas las informaciones mutuas. **La ventaja de MHU, si existe, debe venir de restricciones reales de sensores, costos, regularización, entrenamiento finito o cambio del prior**, no de que al reordenar píxeles sintéticamente surja información física nueva. **Límite:** un sistema hardware que mide T directamente sin registrar X puede costar menos; el teorema no niega eficiencias computacionales.

### M15 · Los expertos independientes no se pueden promediar ingenuamente
**Contraejemplo.** Para una entrada x, dos expertos entrenados por separado almacenan representaciones ocultas h_1(x)=x y h_2(x)=−x, con cabezas o readouts respectivos g_1(h)=h y g_2(h)=−h. Ambos predicen exactamente x. Si fusionamos sus **estados ocultos** por promedio, `(h_1+h_2)/2=0`, destruimos la representación. El fenómeno persiste con permutaciones de unidades ocultas y transformaciones internas compensadas por la salida.

**Conclusión:** superponer capas especializadas exige alinear espacios de representación, aprender adaptadores o combinar salidas, **no únicamente colocar pesos según MHU**. **Límite:** no implica que una combinación con adaptadores entrenados no pueda funcionar; solo invalida la garantía automática.

### M16 · Fusión óptima de estimadores depende de incertidumbre
**Modelo.** Expertos estiman el mismo escalar θ, `T_i=θ+ε_i`, errores insesgados e independientes con varianzas `σ_i²>0`. Combinación lineal T=Σ_i w_i T_i, restricción Σ_i w_i=1. Por Lagrange, minimizar `Var T=Σ_i w_i²σ_i²` da

`w_i=(1/σ_i²)/Σ_j(1/σ_j²)` y `Var(T)=1/Σ_j(1/σ_j²)`.

Con dos varianzas 1 y 4, w=(0,8;0,2), riesgo=0,8 frente a 1,25 del promedio igualitario. Para matriz de covarianza Σ positiva definida, `w=Σ⁻¹1/(1ᵀΣ⁻¹1)`. **La geometría MHU no determina esos pesos; habría que demostrar que modifica favorablemente Σ con costo igualado.** **Límite:** especialistas lenguaje/código no suelen estimar el mismo escalar insesgado; el ejemplo es un mecanismo de fusión específico.

### M17 · Inversión explícita de preferencias al cambiar de frecuencia
**Dos conjuntos de n=2 muestras en el toro 1D:** P={0,1/2} y Q={0,1/4}. Para modo entero k, definamos `A_P(k)=1/2Σ_{x∈P} exp(2πikx)` y análogamente Q. Por sustitución:

| modo | |A_P(k)|² | |A_Q(k)|² | mejor para ese modo |
|--:|--:|--:|--|
| k=1 | 0 | 1/2 | P |
| k=2 | 1 | 0 | Q |

Ambos tienen dos lecturas. Por M11, si la señal se concentra en frecuencia 1 gana P, mientras que si se concentra en frecuencia 2 gana Q. **Ninguna ordenación de eficiencia geométrica es absoluta sin definir el espectro de la tarea**. Nota: Q no se presenta como MHU; es un contraejemplo general a inferir superioridad desde el mero orden espacial.

### M18 · Teorema robusto contra covarianzas desconocidas
**Modelo.** Dados coeficientes complejos `a_i` y desviaciones típicas de canal `σ_i>0`, la matriz de covarianza C solo se sabe PSD con diagonal `C_ii=σ_i²`. Preguntamos cuánto puede llegar a ser `a*Ca` frente a correlaciones adversariales.

Por la condición PSD, `|C_ij|≤σ_iσ_j`, por lo que

`a*Ca ≤ Σ_i,j |a_i|σ_iσ_j|a_j| = (Σ_i σ_i |a_i|)²`.

La igualdad se alcanza con la covarianza de rango uno `C=vv*`, `v_i=σ_i exp(i arg a_i)`, porque `a*v=Σ_iσ_i|a_i|`. Por tanto

`sup_{C ⪰ 0,diag C=σ²} a*Ca = (Σ_iσ_i|a_i|)²`.

**Interpretación:** una geometría que consigue una cancelación de fases favorable para señales perfectamente correlacionadas **no tiene garantía de esa cancelación si se desconoce cómo correlacionan las modalidades**. El objetivo robusto depende de las amplitudes por clase y de cotas empíricas de covarianza. **Límite:** adversario que puede elegir todas las correlaciones físicas compatibles con PSD; puede ser demasiado pesimista para sensores reales, y no prueba superioridad de un algoritmo minimax nuevo. Es una identidad clásica de análisis matricial.

## Auditoría transversal

- Se congelaron los 18 contratos M01–M18 antes de registrar resultados finales: GitHub prereg `1c27c5d...`. Se comprobó escritura y lectura de ese prereg; código de auditoría SymPy/Numpy se creó después de la congelación. **No afirmar freeze de código de auditoría previo al desarrollo de las pruebas.**
- El script `auditoria_formal.py` efectuó 18 checks etiquetados, ninguno de los cuales constituye por sí solo la demostración universal. Las pruebas reales son los argumentos simbólicos escritos arriba. Algunos resultados son corolarios o instancias de otros (M04 deriva M01; M02/M03 comparten ley de varianza total; M11/M17 comparten Fourier). **18 cuestiones A–J atendidas no equivalen a 18 descubrimientos distintos.**
- R1: estimando y clase de funciones explícitos; R2: cuadrícula, diseño extremo, señal isotrópica y diseño óptimo bajo pérdida; R3: no usar p-valores ni claims de frecuencia; R4: cambiar la clase de señal o correlación destruye ventajas condicionadas; R5: stop en afirmación universal, pivot a modelar covarianzas y costos.
- **Juicio sobre originalidad:** No se ha demostrado ningún teorema nuevo ni hallazgo 2/3. Son demostraciones o contraejemplos derivados de teoría establecida. Los mayores antecedentes relevantes son Jiao et al. 2014 (MHU y subtipos), Torquato 2018 (hiperuniformidad), Kim & Torquato 2018 (vacantes), Wei 2010 (muestreo multiclase), Krause/Singh/Guestrin JMLR 2008 (emplazamiento informativo de sensores y garantías matemáticas).
- **Riesgos abiertos:** rigor de definición de HU bajo ventanas anisotrópicas; costo desigual de generación y adquisición; procesos espaciales finitos no certificados; estimaciones gaussianas como modelos no reales; elección de pérdida funcional; ausencia de vínculos cuantitativos a capacidad, entrenamiento y consumo de transformadores.

## Estado, priors y decisión AB

**Ciclos analíticos M01–M18:** 18 cuestiones matemáticas con A–J documentados, 18 argumentos verificados internamente, 0 invalidados por contradicción encontrada, 0 planificación contada como matemática ejecutada. Por parentesco lógico, M01/M04, M02/M03 y M11/M17 **no se elevan a hallazgos distintos**. **N1 nuevos=0, N2=0, N3=0, confirmación externa=NINGUNA**. Se da por agotado el techo de plazas formales del bloque autorizado, sin inferir validez empírica.

**CT2:** rama vision experimental conserva 11/100; la nueva rama *ventaja universal MHU* recibe CT2=1/100 (contradicha por contraejemplos); rama *diseño MHU condicionado a covarianza multimodal* recibe juicio inicial 24/100 (pregunta y marco matemático identificados, pero antecedentes fuertes y ninguna evidencia funcional). No es incremento del 11 anterior porque son líneas distintas (DRIFT≈D2,0). Estos son juicios metodológicos, no probabilidades ni una serie de mejoras experimentales.

**AB-DECIDE:** **STOP** en tesis «MHU es mejor para toda visión o toda inteligencia». **PIVOT condicionado** a un problema robusto y defendible: minimizar una pérdida de reconstrucción multibanda `Σ_k a(k)* C(k) a(k)` bajo información/costos físicos comparables y un conjunto admisible de covarianzas calibradas con datos multiespectrales reales, frente a Wei 2010, diseño óptimo de sensores y selección aprendida. La identidad robusta M18 puede proporcionar una **cota** o un control adversarial, pero no es novedosa por sí misma. Antes de una nueva campaña, exigir fuentes y controles listos, definición de estimando, presupuesto, falsadores y prerregistro de código.

## Bibliografía y procedencia

- Jiao, Y., Lau, T., Hatzikirou, H., Meyer-Hermann, M., Corbo, J.C., & Torquato, S. (2014). *Avian photoreceptor patterns represent a disordered hyperuniform solution to a multiscale packing problem*. Physical Review E, 89, 022721. https://doi.org/10.1103/PhysRevE.89.022721
- Kim, J. & Torquato, S. (2018). *Effect of imperfections on the hyperuniformity of many-body systems*. Physical Review B 97, 054105. https://doi.org/10.1103/PhysRevB.97.054105
- Torquato, S. (2018). *Hyperuniform states of matter*. Physics Reports, 745, 1–95. https://doi.org/10.1016/j.physrep.2018.03.001
- Wei, L.-Y. (2010). *Multi-Class Blue Noise Sampling*. SIGGRAPH. https://www.liyiwei.org/papers/noise-sig10/
- Krause, A., Singh, A., & Guestrin, C. (2008). *Near-Optimal Sensor Placements in Gaussian Processes: Theory, Efficient Algorithms and Empirical Studies*. JMLR 9:235–284. https://jmlr.org/papers/v9/krause08a.html
- Kershner (1939), circle coverings (antecedente clásico para 2D). No se adjudica optimalidad hexagonal para regiones finitas por simple analogía.

**Última línea de gobernanza:** campaña completada dentro del presupuesto de 18 cuestiones formales; no quedan ciclos de las 20 plazas originales. Cualquier trabajo experimental posterior exige nuevos instrumentos, fuentes y autorización solo si no existe ya un cupo concedido distinto en el proyecto.
