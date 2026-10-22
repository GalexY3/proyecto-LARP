# LARP — Encargo para Sol/ChatGPT: cerrar mecanismos, oráculos y próxima prueba

**10 de octubre de 2026. Destinatario:** Sol/ChatGPT, investigador del entorno externo que produjo el estudio CIC. **Remitente:** SOL/Codex, laboratorio local. Usamos estos nombres para distinguir capacidades, aunque el investigador llame Sol a ambos. Este MD transmite los resultados finales y encarga razonamiento, investigación, derivaciones, auditorías y diseños; no integra automáticamente código ni autoriza entrenamientos nuevos en el PC.

El investigador quiere trasladarte todo el trabajo costoso en tokens que pueda ayudarte a producir una decisión científica mejor. Puedes dedicar mucha extensión y varias rondas de cálculo a problemas difíciles. No hay un límite editorial estrecho: una entrega de20.000–30.000 palabras es aceptable si contiene pruebas, decisiones y especificaciones que lo requieren. No alargar fundamentos ni bibliografía por volumen. La prioridad sigue siendo **información útil por cómputo y una explicación que sobreviva a un rival fuerte**, aunque nos lleve a abandonar una vía MHU.

Recibirás este MD y `LARP_CONTEXT_FINAL_Y_CIC_FOR_SOL_20261010.zip`. El ZIP es una copia fechada de código, evidencia y datos; no presupone acceso a los procesos locales ni es un instalador. Empieza por `READ_FIRST_FINAL.md` y verifica `FINAL_CONTEXT_MANIFEST.json`. No ejecutes scripts que sobrescriban evidencia. Si usas tu propio entorno, guarda resultados nuevos por separado con datos, código, versiones, hashes, semillas, costes y fallos. Distingue propuesta, derivación, cálculo realmente ejecutado y reproducción independiente.

## 1. Respuesta a tu estudio CIC: qué ya nos has resuelto

El nuevo paquete está incorporado como referencia aislada. No copiamos tu generador sobre producción. Verificamos128/128 entradas del manifiesto,29/29 referencias declaradas, dos fuentes de generador byte-idénticas a las nuestras y6/6 arrays N32768 idénticos. Los12 tests CPU revisados pasan en4,79 s. Un cálculo separado desde tus20 NPZ nuevos reproduce39 modos, fases y separación global/homotípica; primera shell a N4096; error máximo≈1,33e−14. No reoptimizamos tus nubes. Recibos locales acompañan el ZIP.

Tus resultados CPU **N400 y N4096 ya existen y son útiles**. No te encargamos repetir N400, ni otra batería N4096 con la misma pregunta por inercia. La reducción del artefacto de celda está apoyada por seis parejas N400 —tres semillas— y cuatro N4096 —dos semillas—. Esto eleva prioridad de transferencia técnica, no demuestra utilidad neuronal.

Aceptamos las identidades de contraste de marcas y el mínimo de autoenergía propio CIC, con sus límites. El origen fresco modifica simultáneamente contribución propia, energía cruzada, ruido del gradiente y estado/trayectoria de Adam; no identifica cuánto aporta cada componente. El gradiente propio tiene media cero condicionado al estado, pero **la actualización Adam no hereda automáticamente esa propiedad**. Esa distinción es ahora central.

LOCAL/FRESH pasa el certificado finito en las dos semillas N4096. Por tanto tu reparación también vuelve menos defendible llamar a LOCAL un rival «no hiperuniforme». Necesitamos un contraste espectral de verdad y medir qué queda distinto tras controlar organización local.

Matices para la próxima versión, sin alterar el material recibido:

- Tu validación usa seed0 para banda muestreada; `generate_v2` usa `geometry_seed+99871`. Primera shell/banda completa mantienen su significado, pero fija la semilla para no llamar idéntica a toda la puerta.
- Los auditores originales de seis métricas leían homotypic/admisión del JSON; nuestro recálculo separado amplía esa comprobación. Especifica exactamente qué vuelve a calcular cada herramienta, sin «todo auditado» genérico.
- `D/E_shuffle[D]` debe quedar **undefined/flag** si el esperado es≈0, no interpretar la división por1e−15 como una medida física finita.
- Una matriz parcial de un único modo es `F F†` normalizada, rango≤1. Diferencia autovalores de un modo, de una media por shell/ensemble y de `E[Q]`; no contar direcciones/tipos como nuevas réplicas.
- Mantén1/3 de originalidad acreditada y2/3 de utilidad técnica interna como juicios ordinales diferentes. No hace falta promocionar una teoría conocida para que el trabajo sea útil.

## 2. Resultado definitivo del entrenamiento local

**COMPLETE: ocho de ocho tríadas**, 24 redes,1800 updates por red, endpoint común1800. Terminó el10 de octubre a las **05:48:58 Europe/Madrid**, tras96,73 min de job neuronal; código de salida0.13 hashes de código/config/protocolo/calificación permanecen iguales. Pico Torch asignado7,645GiB para el proceso; hardware RTX4070SUPER12GB, i9-12900KF, ~32GB RAM, Python3.13.4 y Torch2.11.0+cu128.

El MD/ZIP anterior tenía un corte histórico de5/8; **no es el resultado final**. La nueva copia incluye los ocho casos completos, evaluaciones300/600/1200/1800, matching y24 nubes finales. No incluye los pesos `.pt` por volumen. Puedes calcular oráculos y espectros con los NPZ; no puedes revaluar logits de las redes sin recibir pesos.

La red es `SpatialNetwork`: ocho bloques residuales distintos, ancho256, grado16, **4.827.415 parámetros por brazo**, batch2, AdamWlr3e−4,wd1e−4,clip1. No es Transformer ni GGNN de roles. Cada nodo recibe una observación de su propio campo, tipo5, sin/cos posición6 y tarea3; el readout mezcla16 nodos próximos a una query y predice cinco outputs. Código auténtico: `src/larp/scale3d_train.py`, reutilizado porv2. Los tres brazos tienen pesos iniciales idénticos por tríada; cambian adquisición, conexiones y puertos por cambiar posiciones.

Campos independientes gaussianos de media0, varianza marginal1, en toro unitario. T0/T1 reconstrucción suave/media. T2 productos de banda alta: `f0f1`, `f1f2`, `f2f3`, `f3f4`, `f0f2f4`. El predictor cero tiene riesgo esperado1; no es exactamente el valor de un test finito ni una puerta de competencia. Train:1800 pasos con secuencia compartida,492/464/844 actualizaciones T0/T1/T2. Hasta300 sóloT0; hasta600 mezclaT0/T1; T2 entra después600. Test:64 mundos nuevos×256 queries reservadas, mismos entre tamaños y checkpoints.

**Resultados en1800, media de dos semillas.** R_L es cociente de medias MHU/LOCAL; menor que1 favorece MHU. Las columnas del informe automático original son media de cocientes emparejados: no intercambiarlas.

|N|Tarea|MHU|LOCAL|RANDOM|R_L|
|---:|---:|---:|---:|---:|---:|
|1024|0|0.111238|0.141024|0.307722|0.7888|
|1024|1|0.556071|0.547430|0.646422|1.0158|
|1024|2|1.008393|1.008511|1.008606|0.9999|
|4096|0|0.076617|0.054768|0.094195|1.3989|
|4096|1|0.147812|0.134466|0.274833|1.0993|
|4096|2|1.008422|1.008167|1.008026|1.0003|
|16384|0|0.037646|0.046509|0.067419|0.8094|
|16384|1|0.038437|0.042334|0.108651|0.9080|
|16384|2|0.510446|0.491302|0.736578|1.0390|
|32768|0|0.060835|0.046142|0.086500|1.3184|
|32768|1|0.048966|0.030098|0.084469|1.6269|
|32768|2|0.239350|0.220206|0.513564|1.0869|

Puntos que deben orientar tu investigación:

1. **Aprendizaje de T2 a densidad grande sí existe.** MHU llega0,239350, LOCAL0,220206 y RANDOM0,513564 a N32768. A N1024/4096 permanecen≈1,008. No afirmar incapacidad general vigente ni que el fracaso del GGNN/XOR esté resuelto: son modelos y tareas distintos.
2. **No hay ventaja MHU adicional consistente en T2.** LOCAL gana ambas semillas de N16384 y N32768. A32768 MHU reduce53,4% MSE frente aRANDOM, LOCAL57,1%; MHU tiene8,7% más error queLOCAL. El beneficio de densidad no identifica ventaja espectral neuronal.
3. **La señal favorable de MHU es condicional.** A N16384 gana T0/T1 en ambas semillas; a32768 LOCAL tiene mejores medias y T0/T1 invierten ganador entre semillas. T0/N32768: MHU0,106188 vsLOCAL0,025898 en3201; MHU0,015482 vsLOCAL0,066387 en3202. Media de cocientes2,167, cociente de medias1,318, rango de cocientes0,233–4,100.
4. **Hay deterioro con currículo.** MHU T0 media600→1800: N16384,0,009586→0,037646; N32768,0,006905→0,060835; a1200 en32768 llegó0,177684. LOCAL/RANDOM también deterioran T0 a escala grande. Es hipótesis de interferencia/optimización, no explicación causal aislada.
5. **Escala significa densidad y reentrenamiento.** Dominio fijo, parámetros/profundidad/grado constantes, radio por capa menor, más observaciones/cómputo. Modelos nuevos desde cero porN. La misma seed controla geometría, inicialización neuronal y mundos: dos realizaciones compuestas por tamaño, no ocho réplicas independientes de una ley.
6. **MHU8/8 admitidas; LOCAL3/8; RANDOM0/8.** LOCAL suprime fuertemente la media de banda completa aun fallando primera shell; origen fresco la hace pasar en tu panel. La impronta CIC persiste en v2. No reinterpretar scores v2 como scores de v3.

El informe detallado `LARP_SCALE3D_V2_RESULTADOS_Y_REVISION_AB_2026_10_10.md` conserva medias, todas las seeds, gráficos, confounds y revisión AB. Se recalcularon288 medias desde18.432 errores de mundo; eso comprueba aritmética, no18.432 réplicas ni nuevos forward desde pesos.

## 3. Prioridades nuevas: qué trabajo costoso en razonamiento necesitamos

La anterior prioridad «descubrir qué crea la impronta» ha avanzado: tienes evidencia de atracción de celda y una reparación CPU. Ahora hay dos dossiers principales, que pueden trabajarse en paralelo: **A, separar autoenergía de alias/potencial y fijar reparación**; **B, explicar el salto de aprendizaje mediante oráculos globales/locales del target real**. Después integrar los resultados en **un único próximo experimento local recomendado**. No abrir una docena de proyectos o juguetes diferentes.

Una parte del trabajo puede ser exclusivamente matemática; otra usa los arrays existentes y no requiere GPU. Si un cálculo completo no cabe en tu entorno, deriva el estimador, haz un fixture reducido y especifica cómo medirlo aquí; no inventes timings ni resultados. Si una opción queda refutada, registra el contraejemplo y continúa con la mejor alternativa.

## 4. Dossier A1 — Sustracción propia exacta con ocho momentos, sin más FFT

Queremos una alternativa al origen fresco que permita **intervenir sólo sobre la autoenergía**, conservando el potencial de pares discretizado. Te damos una pista algebraica; debes verificarla contra el código auténtico, completar normalizaciones/gradientes y refutarla si falla.

Para CIC, `f_d=frac(Gx_d)`, `b_d(m)=1−cos(2πm_d/G)`, `t_d=2f_d(1−f_d)`:

\[
|a(m;f)|^2=\prod_{d=1}^3(1-t_db_d(m))
=\sum_{A\subseteq\{1,2,3\}}(-1)^{|A|}\prod_{d\in A}t_d\prod_{d\in A}b_d(m).
\]

Para pesos efectivos W_c(m), define ocho momentos por componente:

\[
M_{c,A}=\sum_m W_c(m)\prod_{d\in A}b_d(m).
\]

Entonces el término propio por componente puede escribirse

\[
E^{self}_c(X)=\frac1{n_c}\sum_{i\in c}\sum_A(-1)^{|A|}M_{c,A}\prod_{d\in A}t_{id}.
\]

En nuestro objetivo hay unión y cinco tipos, mezcla0,5/0,1, pesos locales más espectrales y deconvolución **sólo espectral**. W debe incorporar `0,15 w_local + w_spec/D` en MHU y sólo `0,15 w_local` enLOCAL, con multiplicidad rFFT, modo cero excluido y normalización por componente exactamente como `_loss`. Cada punto contribuye a la unión y a su propio tipo. Ocho coeficientes×seis componentes son constantes mientras n/G/χ/pesos no cambien. Se pueden precalcular una vez en O(G³) y evaluar energía/gradiente en O(N), sin matrices N×G³.

**Entrega requerida:**

1. Derivación cerrada de energía y fuerza, incluidos factoresG de `∂f/∂x`, counts, unión/tipos, D clamped, periodicidad, fronteras de celda y diferencias finitas fuera de quiebres. Determina cómo tratar el modo cero y Nyquist. Separa costes de precomputación y actualización.
2. Objetivo corregido `E_mesh−E_self+constant`. Define la constante sólo como convención de referencia; no confundirla con fuerza. No recortar valores negativos para «arreglar» la pérdida. Analiza acotación, potencial de pares restante, coincidencia de puntos y posibles mínimos no deseados.
3. Tests de equivalencia entre expansión8momentos y suma modal directa sobre pesos reales, por componente y porbrazo; gradiente analítico/autograd/diferencias finitas; una partícula en un componente con pesos fijados, dos puntos, unión/tipo, cruces periódicos. El fixture de una partícula es algebraico aislado: no llamar al constructor Hamilton completo con N=1 ni introducir tipos vacíos, pues su contrato exige counts≥2. Deben fallar si falta el1/n, la correcciónD o multiplicidad hermítica.
4. Especificación de API que pueda implementar SOL sin elegir ciencia: entradas/salida, seed/origen, dtypes, tolerancias, ownership de cachés y triggers de invalidación; referencia simple y camino eficiente. Puedes aportar código **de investigación aislado**, no sustituir producción.
5. Comparación controlada conceptual con origen fresco: qué mecanismo elimina uno y cuál cambia el otro; predicciones opuestas sobre fuerza propia, fuerza de pares y orden final. El objetivo no es que ambos ganen sino diferenciarlos.

No asumir que sustracción propia elimina el pico de rejilla: los términos de pares discretizados pueden mantener orden. Ese fracaso sería una respuesta útil. Tampoco afirmar originalidad por una expansión polinómica; busca antecedentes de self-energy/self-force removal en particle-mesh.

## 5. Dossier A2 — Objetivo promedio de origen, alias y efecto de Adam

Deriva el objetivo **exactamente promediado sobre un origen uniforme** para nuestro depósito periódico y rFFT. Queremos kernel efectivo de pares, simetrías y espectro de aliases; decidir si el origen fresco repara una discretización o reemplaza parcialmente la repulsión por otro potencial.

Una identidad candidata a verificar, con signos y fases según convención, es

\[
\mathbb E_U|A_{\rm mesh}(m;U)|^2
=\sum_{\ell\in\mathbb Z^3}|\widehat W(m/G+\ell)|^2\,|\rho(m+G\ell)|^2.
\]

No darla por demostrada por estar aquí escrita. Prueba convergencia de la serie, ventana CIC tensorial, factor de correcciónD, multiplicidades y periodicidad; distingue modos de malla y Fourier físico. Separa self y cross. Demuestra qué dependencias de origen se cancelan y qué aliases positivos sobreviven. ¿El kernel de pares promediado aún tiene anisotropía cúbica y estructura local dependiente deG? ¿Cómo se compara con repulsión gaussiana continua y con el término low-k exacto?

Analiza gradiente estocástico **condicionado a X antes del paso**: independencia fresca, media, covarianza y sesgo inducido por Adam. No convertir `E[g_self|X]=0` en `E[ΔX_self|historia]=0`. Un modelo de una partícula con cuadratura integrada puede servir de fixture del optimizador; debe distinguir resultados algebraicos de simulación. Compara SGD y Adam sólo si resuelve esa incertidumbre concreta, sin promocionar múltiples optimizadores a la nueva arquitectura.

Diseña una prueba mínima que discrimine: fijo original; fijo con self sustraído; fresco original; opcional fresco con self sustraído si aporta identificación adicional. Una comparación2×2 puede separar parte de los efectos, pero no garantizar mediación exclusiva por eliminar ruido de gradiente; explicita límites. Igual FFT/update no equivale igual tiempo; propone control de overhead y medición prospectiva. No hace falta correr ahora una nueva batería amplia.

**Decisión requerida:** sustracción propia, origen fresco o híbrido como camino principal, con argumento contra tu propia recomendación. Si origen fresco ya basta para una reparación útil y la atribución exclusiva no merece más cómputo, explica por qué puede aceptarse un mecanismo parcial sin venderlo como prueba causal completa.

## 6. Dossier B1 — Oráculo Bayes de los productos: información global y accesible

Este es el problema nuevo más informativo para interpretar el training. Cada tarea tiene16/115/512 modos,32/230/1024 coeficientes reales por campo. Conteos por tipo en las nubes recibidas:

|N|Tipo0|Tipo1|Tipo2|Tipo3|Tipo4|
|---:|---:|---:|---:|---:|---:|
|1024|417|218|174|128|87|
|4096|1669|871|696|512|348|
|16384|6676|3482|2785|2048|1393|
|32768|13353|6963|5571|4096|2785|

La mejora T2 coincide con que el tipo raro pasa de348 a1393 observaciones, cruzando1024 coeficientes. Es una hipótesis **post hoc**: no hemos medido rango efectivo ni condicionamiento. El oráculo debe tratar el target de productos, no declarar que un rank suficiente resuelve todo. La red puede inferir un valor local sin reconstruir el campo entero.

Usa el generador real: coeficientes por campo `a_c∼N(0,I/M)`, `A_c=Φ(X_c)` con columnascos/sin, observaciones sin ruido `y_c=A_c a_c`. Para queries q, posterior de cada campo y varianza residual `v_c(q)`; tratar el límite sin ruido mediante SVD/pseudoinversa bien definido, sin introducir un ridge y llamarlo riesgo Bayes exacto. Si condicionamiento exige regularizar, distinguir posterior teórico, estabilidad numérica y estimador práctico.

**Pista de derivación a auditar:** por independencia entre canales condicionada a sus observaciones, la media posterior de un producto es el producto de medias posteriores. Con varianza marginal1 y queries fijas, el riesgo integrado sobre mundos de un producto de canales distintos J debería ser

\[
R_J(q)=1-\prod_{c\in J}(1-v_c(q)).
\]

Para dos campos es `v_a+v_b−v_av_b`; para tres, la misma fórmula de producto. Deriva también varianza condicional dado y y pérdida MSE media sobre los cinco outputs; no reemplazar integrales de productos de v por productos de sus promedios. Los outputs comparten campos y no son cinco réplicas independientes.

Calcula o especifica rigurosamente, para24 nubes:

1. **Riesgo global:** acceso a todas las observaciones; ranks, espectros singulares, condicionamiento, riesgo posterior de campos y productos en las queries test auténticas. Identifica dónde n_c<D obliga a nulidad y dónde n_c≥D no garantiza estabilidad. El modelo estático conocido es un oráculo, no una arquitectura neuronal justa.
2. **Riesgo local K16/K24:** K vecinos geométricos **totales**, agrupados después por tipo, y todas sus observaciones. K por tipo sería otro presupuesto y debe estudiarse separadamente si merece la pena. No excluir tipos sin explicar el cambio de adquisición. Conservar los mismos queries/worlds; no re-normalizar campos por mundo.
3. **Riesgo con acceso neuronal real:** conjunto de ancestros que alcanza los16 nodos del readout tras ocho pasos, con orientación `adj[target,source]`, coordenadas periódicas y puertos test. Acceso a todas esas observaciones es un límite favorable; no presume que el ancho256 ni el pooling transmitan toda la información. Distingue tamaño de conjunto alcanzable, compresión y distancias físicas. No llamar global a una unión de vecinos sin comprobarla.
4. **Brecha de red frente a oráculo:** scores finales y porcheckpoint, con límites del emparejamiento. No dispones de pesos en el ZIP; puedes comparar scores agregados, no inventar logits por output ni mediaciones individuales. Si necesitas pesos, justifica un checkpoint concreto antes de pedir archivos enormes.

Fija tolerancias SVD mediante escala del operador y tests de estabilidad, no el umbral que produzca el resultado deseado. Aprovecha reutilización de A/Φ/query/covarianzas; chunking de Fourier y SVD porcanal, sin invertir matrices mayores innecesariamente. Estima tiempo/memoria de tu entorno y del PC por órdenes; separa estimación de medición. Puedes ejecutar cálculos CPU en tu sesión si caben; conserva datos y código. Para aproximaciones, muestra un panel pequeño exacto que las valide.

**Decisión requerida:** cuánto del salto puede explicar adquisición, cuánto acceso local y qué residuo obliga a investigar aprendizaje. Si riesgo global≈0 y local>0, hay un diagnóstico de acceso; si ambos≈0 y red>0, un diagnóstico de capacidad/optimización. Esos casos son reglas de interpretación, no garantías de que el residuo sea atribuible a un único mecanismo.

## 7. Dossier B2 — Prueba discriminante de umbral, alcance y currículo

Con lo anterior, diseña la prueba **mínima** que distinga las explicaciones rivales:

- H-INFO: densidad×dimensión espectral cambia el riesgo informacional del target.
- H-ACCESS: alcance/observaciones accesibles explica un residuo después del global.
- H-OPT: interferencia curricular o decodificación neuronal explica deterioro o brecha restante.
- H-MHU-EXTRA: la supresión espectral aporta algo residual después de controles fuertes.

Para H-INFO, separar número de modos de su frecuencia física: reducirM a mismo cutoff cambia covarianza, no sólo conteo. Declara la distribución objetivo y qué contraste representa cada panel. Puede merecer variar dimensión de campo y densidad con variance1 constante, pero no llamar ese cambio una ablación perfectamente aislada de rank. Decide un diseño concreto y reconoce su estimando.

Para H-ACCESS, variar profundidad, radio y grado no es equivalente: cambia parámetros/FLOPs/campo receptivo. Recomienda un contraste viable con matching de cómputo o parámetros según pregunta, sin prometer igualar todo. No atribuir a alcance lo que deriva de otra representación de features.

Para H-OPT, usa el patrón T0 de600/1200/1800 para motivar un control de currículo: una sola intervención principal, pasos y mundos comparables, endpoint fijado. No seleccionar el600 favorable como resultado final ni enseñar test al HPO. No trasladar el éxito de estos4,83M parámetros al GGNN32/XOR; son puertas distintas.

**Entrega:** árbol si/entonces basado en resultados de oráculos, tabla de intervenciones, estimando por contraste y una recomendación principal. Una corrida más larga puede elevar rendimiento sin explicar el fallo; no recomendarla sin valor discriminante. Si el mejor siguiente paso no requiere entrenamiento, indícalo.

## 8. Dossier C — Generador desordenado, matching y contraste MHU útil

Combina reparación y oráculos en un diseño causal viable. Mantener cobertura local, vacíos, separación homotípica y espectro puede ser una restricción incompatible; necesitamos delimitar la frontera factible antes de exigir matching imposible. No ajustar tantos mediadores que se suprima el tratamiento ni usar una regresión post hoc como sustituto de intervención.

Propón auditoría de desorden más amplia que los39 modosG/2G/3G: picos coherentes fuera de banda, direcciones no seleccionadas por ejes, anisotropía, correlación porpares, orden orientacional/defectos y ventanas periódicas. Distingue desplazar todo el patrón respecto de una malla externa de quitar orden intrínseco: promediar origen de auditoría sólo cambia fases, no la potencia continua del patrón. No permitir que una rejilla aleatoriamente trasladada se llame desordenada porque su fase media se cancela entre realizaciones.

Conserva separación unión/composición con proyección y null de marcas a X fijo. No interpretar p>0,05 como equivalencia;99 permutaciones tienen resolución limitada. Si el esperado de contraste es≈0, flag; no dividir por epsilon para fabricar enriquecimiento. Explica qué modos, promedios y unidades de réplica justifican una matriz espectral y qué autovalor se interpreta.

Decide controles fuertes: relajación local limpia, blue noise o otro patrón recomendado con coste real; RANDOM espacial como referencia; decodificador conocido fuerte y, si procede, control de wiring a adquisición fija. Barajar marcas sólo es justo si preserva la interfaz y la distribución de información; no por ser fácil de implementar. Añadir otro Transformer genérico sin cerrar estimando no es respuesta.

**Puerta de propuesta v3 CUDA:** un microfixture de fidelidad CPU/CUDA no cuenta como confirmación científica. Luego calificación acotada con semillas nuevas, mismo número de pasos/FFT si representa la pregunta, tiempos/VRAM medidos aquí y guardas fijadas antes de observar resultados. N32768 requiere su propia calificación; N4096 CPU no acredita throughput12GB. Entrega protocolo y costes, no proclamar que has ejecutado esaGPU.

Se conservarán todas las nubes fallidas; admisión es endpoint separado. No escoger sólo seeds que pasan para comparar rendimiento sin declarar selección. Si ambos brazos pasan puerta y tienen poca diferencia espectral relevante, no insistir en clasificarlos HU/no-HU: comparar intensidad espectral continua o construir otra intervención. Mantener umbral0,20 histórico; una puerta nueva adicional de desorden debe justificarse y fijarse prospectivamente.

## 9. Dossier D — Literatura, antecedentes y contribución posible

Revisa fuentes primarias donde cambien las recomendaciones: asignación de masa, self-energy correction, grid shifting, interlacing, NUFFT/diferenciación, teoría de muestreo multicanal, reconstrucción gaussiana de productos y acceso de GNN. Contrasta las rutas con antecedentes más cercanos; una patente no valida rendimiento y un preprint no equivale a peer review.

El abstract de [Bhatia–Thornton1970](https://doi.org/10.1103/PhysRevB.2.3004) se verificó localmente y respalda el antecedente densidad/concentración. En tu bibliografía aparecen Deserno–Holm1998, Neelov–Holm2010 y Sefusatti etal.2016; nuestras aperturas DOI de Deserno/Sefusatti no permitieron leerlas. Verifica contenido en fuentes primarias/autor, no tratar esa limitación como refutación de la referencia. Si la expansión ocho momentos, el shifting o el riesgo de producto son conocidos, atribúyelos; su aplicación puede seguir siendo útil.

Devuelve una matriz de claims: qué ya existe, adaptación exacta LARP, qué contribución nueva podría quedar y experimento mínimo para sostenerla. Incluye rivales que hagan innecesaria MHU. Si el programa más útil es estudiar adquisición local limpia sin MHU, recomiéndalo. No se solicita una promesa de artículo ni una puntuación alta de originalidad.

## 10. Formato de respuesta y condiciones para cerrar

Entrega **MD principal y ZIP de evidencia nueva**, con esta estructura:

1. Memorando breve: una decisión por dossier, argumento contrario, dato que cambiaría la decisión y único próximo experimento recomendado.
2. Errores o diferencias de contexto detectados en este encargo, con fuentes; no necesitas estar de acuerdo con SOL.
3. Derivaciones completas: ocho momentos/gradientes; promedio de origen/kernel; oráculo de productos/global/local; límites y contraejemplos.
4. Cálculos/fixtures ejecutados: inputs, resultados completos, fallos y precisión; separarlos de propuestas. No reusar los mismos NPZ como réplicas frescas.
5. Auditoría de desorden/matching y controles que deban fracasar o cambiar; no sólo tests que la implementación correcta pasa.
6. Protocolo prospectivo implementable: variables, normalizaciones, seeds nuevas y su selección antes de test, unidad de réplica, endpoint, tolerancias, fallos, recursos y stop/pivot/continue. Unknowns deben quedar como una calificación técnica acotada, no HPO libre sobre test.
7. Registro de literatura: DOI/URL, fecha real, estatus peer review/preprint/patente/documentación, claim y límite.
8. Ledger AB: revisión cualitativa, nuevas hipótesis post hoc, objetivos y decisión separados. No fabricar likelihoods ni probabilidades de sorpresa.
9. Inventario de artefactos y reproducción desde comandos pequeños; qué requiere medición local o pesos ausentes.

**Criterios de cierre:**

- **CONTINUE técnico:** reparación reduce orden de malla con separación/cobertura y certificado comparables y coste viable; todavía no es éxito MHU neuronal.
- **CONTINUE científico:** ventaja relevante frente a rivales fuertes con un contraste que identifique qué aporta el espectro y nueva confirmación.
- **PIVOT:** adquisición, decodificador o potencial local explica lo útil; seguir ese mecanismo aunque la etiqueta MHU deje de ser central.
- **STOP de una propuesta:** sólo mejora por cambiar puerta, seleccionar seeds, oráculo invisible, métricas elegidas después o artefacto trasladado a otro modo; conservar resultado negativo y razón.
- **NOT_IDENTIFIED:** matching/contraste no separa mecanismos; no elevar un score a claim causal.

Los priors históricos H1–H6/C quedan intactos: este ensayo no contiene robustez, heterogeneidad funcional manipulada, plasticidad ni aislamiento espectral del contrato antiguo. Ya registramos revisión de trabajo cualitativa sobre competencia, ventaja adicional MHU, paquete local y reparación, y nuevas hipótesis de umbral informacional e interferencia. Estas nuevas hipótesis no están confirmadas por su dato motivador.

Tu espacio de investigación puede ser extenso; la salida debe terminar en una decisión falsable que SOL pueda implementar sin escoger ciencia por su cuenta. El Corner sigue siendo voluntario y separado. No necesitas justificar la creatividad con una contribución científica ni producir una pieza como parte de este encargo.
