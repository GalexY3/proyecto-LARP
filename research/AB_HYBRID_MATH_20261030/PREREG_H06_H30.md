# LARP AB3.2.1 · BRANCHING — H06–H30
**Fecha:** 2026-10-30. **Autorización previa:** 30 ciclos; H01–H05 ejecutados y auditados (HEAD `8098f79b55a52b454b03027c709f61d12fe4751e`); **saldo inicial 25**. Este documento solo congela preguntas, NO cuenta ninguna como realizada.
**Objetivo:** matemáticas de las hermanas MHU/LOCAL/CVT, grafos multiespecialistas, espectros, robustez, multicriterio y cotas de comunicación. No asumir novedad; no reusar observaciones de C01–C04 como confirmación.

**Contratos A–J:** A estimando exacto, espacio y supuestos por H; B rival competente y negación; C prueba algebraica/constructiva y falsador; D scripts íntegros y protocolo con commit antes de observar los resultados de verificación; E ejecución real con datos de prueba sintéticos o enumeración y demostración matemática escrita; F auditoría de límites, casos degenerados, modelos originales de LARP y antecedentes; G validación auxiliar independiente (símbolos/ejemplos) sin confundir con prueba formal o replicación externa; H priors cualitativos, positivos y adversos; I corrección, novedad, causalidad, generalidad y reproducibilidad separadas; J stop/branch/pivot condicionado. La prueba escrita prevalece sobre los tests finitos.
**Control R5:** las identidades/corolarios estrechamente relacionadas conservan su dependencia; un test no equivale a descubrimiento 1/3 o 2/3. Fallos: INVALID/ERRATA; nunca reparar a posteriori sin registrar. Código fuente completo debe congelarse antes de los resultados y reproducirse con un clon limpio si es posible. Sin main ni CI costosa.
**Literatura de partida:** Wei SIGGRAPH 2010, Torquato 2018, Morse & Torquato 2024, Krause et al 2008; histórico LARP S01–S20, M01–M18 y H01–H05. Todo teorema básico con precedentes NO ES ORIGINAL.

## Claims and falsifiers congelados
### H06 — Coste mínimo del enrutamiento multiespecialista
**H:** En un digrafo sin autoaristas, recibir al menos un mensaje de cada una de m especies exige grado de entrada >=m y >=mN aristas dirigidas; para n_c>=2 existe construcción alcanzable sin límite de salida.
**Falsador:** Una configuración con <mN aristas satisface todos los destinos
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H07 — Límite de fan-out de la especie escasa
**H:** Si todo vértice necesita información de clase c en un paso, cada emisor c tiene fan-out como máximo D, luego D>=ceil(N/n_c); para (163,85,68,50,34) se requiere D>=12.
**Falsador:** Cobertura global de una clase con n_cD<N
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H08 — Profundidad mínima para comunicación global
**H:** En un digrafo con out-degree <=d la cantidad de nodos alcanzable por una fuente en T pasos es <=sum_{j=0}^T d^j; d=6,N=400 exige T>=4.
**Falsador:** Un grafo dirigido con d<=6 y diámetro<=3 y 400 nodos
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H09 — Espectro del grafo completo multipartito
**H:** Laplaciano de K_{n1,...,nm} tiene autovalores 0, N (m-1 veces), N-n_c (n_c-1 veces); conectividad algebraica N-max_c n_c si nmax>=2.
**Falsador:** Cálculo exacto de eigensistema contradice fórmula
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H10 — Sesgo estacionario de mezcla entre tipos
**H:** En paseo aleatorio de grafo completo multipartito, probabilidad estacionaria de cada clase proporcional n_c(N-n_c); flujo de c a d cumple balance detallado.
**Falsador:** Flujo dirigido no satisface reversibilidad
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H11 — Cobertura óptima de subrejilla discreta
**H:** Seleccionar n posiciones entre N equiespaciadas en círculo minimiza la máxima separación circular en ceil(N/n) / N; construcción índices floor(j*N/n).
**Falsador:** Selección con máximo gap inferior a ceil(N/n)
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H12 — Presupuesto de energía espectral de una especie
**H:** Para etiquetas binarias de cuota n sobre retícula de N, sum_{k=1}^{N-1} S_c(k)=N-n; una reducción de potencia en bajas frecuencias desplaza masa espectral a otras.
**Falsador:** DFT/Parseval incumple igualdad para alguna etiqueta
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H13 — Restricción exacta de correlación al primer vecino
**H:** En etiquetado circular binario b_j, sum_{k=1}^{N-1} |rho(k)|² cos(2πk/N)=N*C1-n² donde C1=sum b_j b_{j+1}.
**Falsador:** Autocorrelación y DFT de la misma secuencia difieren
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H14 — Intercalación espectral de m especies iguales
**H:** m retículas n igualmente espaciadas, desplazadas c/(mn), generan unión de mn posiciones; cada especie anula modos k no múltiplos n, unión todos k no múltiplos mn, particularmente n..mn-1.
**Falsador:** La suma de raíces de unidad no se anula
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H15 — Cota del coste CVT multiespecie
**H:** Para posiciones de cada clase sobre círculo con n_c puntos, Q_total=sum w_c Q_c>=sum w_c/(12 n_c²); igualdad simultánea requiere subretículas equiespaciadas compatibles.
**Falsador:** Coste inferior a la cota convexa
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H16 — Fases óptimas con correlación conocida
**H:** Para dos errores de módulo a y covarianza ρ real, riesgo=2a²(1+ρ cosδ), mínimo 2a²(1-|ρ|), alcanzable con δ opuesto al signo de ρ.
**Falsador:** Una fase obtiene riesgo inferior al mínimo declarado
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H17 — Fases minimax con signo de correlación desconocido
**H:** Si |ρ|<=r>0, riesgo peor caso=2a²(1+r|cosδ|), mínimo en δ=π/2 modulo π, frente a fase alineada peor 2a²(1+r).
**Falsador:** Otra fase reduce el peor riesgo bajo simetría del intervalo
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H18 — Justificación RKHS del score espectral
**H:** Para funciones periódicas con norm²=sum |f_k|²/w_k<=1 y Fourier summable, error de cuadratura al cuadrado peor caso=sum w_k |a_P(k)|²; requiere sum w_k finita para evaluación puntual.
**Falsador:** Cauchy-Schwarz da un valor diferente o no se alcanza
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H19 — Obstrucción crítica de los pesos 1/|k|²
**H:** En dimensión d>=2, sum_{k in Z^d\{0}} |k|^-2 diverge; por eso peso v2 no define kernel continuo acotado de evaluación puntual si se extiende a todos los modos sin truncamiento.
**Falsador:** Una prueba de convergencia de la serie en d=2
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H20 — Existencia de óptimos híbridos
**H:** Sobre (toro)^N compacto, score J=αCVT+β sum_{k∈K} w_k |a(k)|² continuo para K finito, por lo que existe un minimizador global; mínimos separados por especie si función objetivo lo permite.
**Falsador:** Secuencia sin subsecuencia convergente o discontinuidad del integrando fijo
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H21 — Los pesos lineales omiten Pareto eficientes
**H:** Con tres candidatos A=(0,4), B=(1,3.5), C=(4,0), B es Pareto eficiente pero nunca es mínimo de λL+S con λ>=0.
**Falsador:** Algún λ hace a B estrictamente preferido
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H22 — La restricción epsilon recupera soluciones no soportadas
**H:** En el mismo conjunto A,B,C, minimizar S sujeto a L<=1 selecciona B, que ninguna ponderación positiva selecciona.
**Falsador:** Con L<=1 otro candidato tiene menor S
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H23 — Penalización por cuotas sin compensar varianzas
**H:** Para cinco canales con varianza igual σ² y estimador de media de canales, varianza es σ²/m² sum 1/n_c, mínima σ²/N si n_c=N/m; calcular ratio para cuotas reales.
**Falsador:** Una reasignación peor que balance tiene menor varianza
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H24 — Diversidad superviviente tras fallos iid
**H:** Con retención independiente p, P(todas las m especies conservan al menos un sensor)=prod_c[1-(1-p)^n_c]; para cuota total fija, se maximiza cuando tamaños difieren como máximo 1.
**Falsador:** Trasladar un sensor desde clase mayor a menor reduce la probabilidad
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H25 — Submodularidad informativa gaussiana
**H:** Con variable latente gaussiana y lecturas lineales con ruido independiente, información mutua I(θ;Y_S)=0.5 logdet(I+sum H_iᵀR_i^-1 H_i) es monótona submodular; comprobar caso escalar.
**Falsador:** Retorno marginal de sensor mayor tras observar otros, manteniendo independencia de ruidos
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H26 — Contraejemplo XOR a selección submodular
**H:** Para bits independientes X1,X2 y etiqueta XOR, I(Y;X1)=I(Y;X2)=0 pero I(Y;X1,X2)=1; la utilidad I(Y;observaciones) no siempre es submodular.
**Falsador:** XOR tiene información marginal >0 en observación aislada
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H27 — Localidad exacta de redes por mensajes
**H:** Con T rondas y aristas fijas, salida de nodo v depende solo de características dentro de T hops de entrada (y parámetros compartidos) si no hay readout global/atajos.
**Falsador:** Se observa dependencia de fuente a distancia>T sin ruta auxiliar
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H28 — Cuello de botella de rango a través de cortes
**H:** En redes lineales por mensajes, con b aristas dirigidas cruzando corte A→B por ronda, estados de ancho h y T rondas, rango de transmisión de entradas A a salidas B <=b h T.
**Falsador:** Una red lineal de rango>bhT sin caminos alternativos ni entrada directa
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H29 — Fusión minimax de estimadores correlacionados
**H:** Para dos estimadores insesgados σ1,σ2 con ρ∈[-r,r], pesos convexos, peso óptimo w1=clip[(σ2²-rσ1σ2)/(σ1²+σ2²-2rσ1σ2),0,1], no siempre precisión inversa.
**Falsador:** Otro peso convexos da menos peor varianza
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

### H30 — Invariancia al patrón sin acceso a posiciones
**H:** Una arquitectura de atención o mensajes permutation-equivariant que recibe mismas features y grafo independientemente de coordenadas no puede distinguir patrón MHU de retícula tras relabeling; requiere canal geométrico.
**Falsador:** Cambio de coordenadas no usadas altera resultado
**Separación:** cálculo finito/teorema condicionado; revisar rivales, costes y fuentes antes de elevar grado.

## Seguimiento
Solo cuenta una Hxx si tiene ficha A–J, demostración completa, check auditado, adversarios y dictamen archivado. Al primer STOP local, ramificar a uno de los otros bloques; no aumentar CT2 por el número. Al agotar los 25, declarar saldo 0 y solicitar una nueva concesión solo si existe cuello de botella científicamente justificado.
