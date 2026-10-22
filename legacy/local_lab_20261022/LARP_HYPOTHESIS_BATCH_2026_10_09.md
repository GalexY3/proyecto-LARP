# LARP — Nueva cartera y lote de32 hipótesis fundamentadas

**Fecha:**2026-10-09. **Estado:** síntesis adversarial, hipótesis propuestas, cero nuevas corridas. **Padre:**`75580c6`. **Decisión:**[ADR del pivote](docs/decisions/ADR_2026_10_09_MHU_PORTFOLIO_PIVOT.md). Revisión de tres agentes especializados más integración de la raíz; no equivale a cuatro réplicas empíricas. La decisión se toma bajo la delegación humana explícita de este turno y AB 2.1.

## 1. Mi decisión sobre MHU

**MHU deja de ser la apuesta principal.** Conservaría su generador y una comparación secundaria acotada, pero no dedicaría ahora el siguiente presupuesto a una red MHU más grande,3D o multicapa. La pregunta principal pasa a ser qué organización multicanal adquiere o transporta mejor información bajo señales, decoders y recursos declarados. La distribución ganadora puede resultar MHU, local, cristalina, adaptada al kernel o aprendida.

Es perfectamente posible que MHU no sea mejor en el problema que importa. En varios regímenes locales ya hay estructuras que conservan casi toda la mejora sin aprobar su certificado; con reconstrucción competente hay inversiones de ranking. Esto debilita la necesidad práctica de perseguir MHU como objetivo. No demuestra que jamás aporte valor, ni una ausencia causal universal: las propiedades geométricas y la información del decoder todavía no se aislaron completamente.

El cambio elimina una apuesta implícita: antes buscábamos un control que permitiera preguntar si «MHU añade algo» sobre un sustrato elegido por su organización nativa. Ahora comenzamos por un riesgo o una operación concreta y exigimos que cualquier estructura justifique su coste. MHU tiene que ganarse su lugar frente a rivales pertinentes. No basta mejorar a shuffle, superar XOR, parecerse a una retina, producir un certificado o admitir más movimientos.

La línea MIN-conditioned conserva utilidad instrumental eventual, pero **deja de ser el siguiente paso automático**. Resuelve si podemos mover marcas sin salir de unas guardas; no si esos movimientos cambian información útil. La mantendría archivada hasta formular un contraste funcional que realmente necesite ese control. Este cambio prospectivo no altera su plan anterior ni los resultados cerrados.

## 2. Lo que la evidencia permite revisar

| Paquete de evidencia local | Conclusión defendible | Afirmación que no queda identificada |
|---|---|---|
| Aviar full/local contra nominal/shuffle con NN y kernel | La organización aviar facilita reconstrucción LOCAL de determinados campos. | Que la supresión de ondas largas sea su causa exclusiva. |
| Local-only:0/3 certificados MHU, adquisición próxima a full | Exclusión y cobertura son un rival explicativo fuerte; el término espectral no parece necesario para la mayor mejora observada. | Equivalencia exacta full/local o mediación local completa. |
| Oracle smooth sin ruido: máximoMSE 5.79e−30 | Con banda conocida y rango completo, las otras estructuras no pierden esa información recuperable. | Igual coste de información/comunicación que un decoder local. |
| Oracle fine con ruido: shuffle mejora aviar full/local en3/3 seeds | La organización nativa no es universalmente superior en ese benchmark. | Inutilidad neuronal de MHU o causa única de cada inversión. |
| Grid fuerte y queries continuas | La ganancia aviar LOCAL no era sólo coincidencia de queries; Grid puede ganar con oracle. | Coloración Grid óptima o superioridad universal de una familia. |
| v2y130 guardas | q=.5 es incompatible con varianza exacta±5% en los casos demostrados; q=.25 sigue sin identificar. | Imposibilidad general de separar organización local y espectral. |
| Vecindario:77 swaps y18 ciclos completos | La nativa no está aislada para esos movimientos; el kernel anterior proponía ciclos válidos muy raramente. | Componente factible grande, plasticidad útil o beneficio computacional. |
| Piloto de18cadenas,130 swaps cada una | Ese constructor desde shuffle falla su puerta; corresponde cerrarlo. | Frontera intrínseca cobertura/espectro o comparación justa de generadores. |
| BALANCED b0 pasa dos seeds, AUX conserva un fallo | Un paquete curricular facilita selección de roles en un panel limitado. | XOR universal, transporte remoto o ventaja MHU. |

Fuentes locales: [muestreo](docs/SAMPLING_PROBE.md), [oracle](docs/SAMPLING_ORACLE.md), [Grid](docs/SAMPLING_GRID_RESULTS.md), [generador](docs/AVIAN_GENERATOR_REPORT.md), [roles](docs/PHASE_3_ROLE_COVERAGE.md), [v2](LARP_SPECTRAL_FEASIBILITY_V2_RESULTS.md), [últimas fases](LARP_NATIVE_NEIGHBORHOOD_AND_TRADEOFF_RESULTS.md). El [snapshot histórico](artifacts/hypothesis_batch_2026_10_09/historical_before.json) conserva hashes; no se vuelven a ejecutar auditores que escriben archivos antiguos.

Un dato adverso merece énfasis: para queries continuas, fine yσ=.1, el oracle obtiene MSE macro .138230 con full,.136474 con local y .128437 con Grid. En el suplemento previo, full−local smoothoracle fue aproximadamente−3.09e−6. Son tres realizaciones descriptivas y bancos reutilizados: los cientos de celdas o miles de queries no crean cientos de réplicas geométricas. Tampoco ocultamos las pequeñas mejoras full en determinados decoders locales smooth.

Full/local **sí es una ablación trazable del regularizador del generador**: mismos términos locales, inicialización, pasos y opciones, intento0. El efecto total de añadir ese término puede describirse dentro del procedimiento. Su resultado no identifica exclusivamente HU porque cambia X, microestructura, E y puertos. Un mediador geométrico correlacionado no se convierte en mecanismo por añadirlo a una regresión sobre tres semillas.

No cambiaré los números históricos H1–H6/C. No hay likelihood defendible que conecte estas observaciones con sus proposiciones arquitectónicas completas. La nueva revisión de trabajo es cualitativa: alta prioridad a información/decoder; menor prioridad a MHU neuronal genérica; mantenimiento de MHU como factor candidato. Plausibilidad de una hipótesis y prioridad de probarla son cosas distintas.

## 3. Dos mecanismos concretos que cambian el programa

### 3.1. La matriz de observación ve diferencias de frecuencias

Para un canal c, sensores X_c y base compleja de modos K:

\[
A_{ik}=e^{2\pi i k\cdot x_i/L},\qquad
(A^*A)_{k\ell}=\sum_{i\in X_c}e^{2\pi i(\ell-k)\cdot x_i/L}
=\rho_c(\ell-k).
\]

En una base real cos/sin también aparecen sumas de frecuencias. **Deducción algebraica propia:** recuperar una banda no depende sólo de S_c en sus propios modos; depende de amplitudes en K−K y, con la representación real, sus sumas. Incluso una señal smooth con radios enteros≤2 produce términos hasta radio4. Nuestro certificado optimiza seis modos, de modo que no controla toda la Gram, sus autovalores ni el error de ruido. En fine, parte del problema es además subdeterminado.

Para un modelo gaussiano explícito, coeficientes con covarianza Cθ, ruidoΣε y matriz de evaluación Q:

\[
C_{\rm post}=C_\theta-C_\theta A^*(A C_\theta A^*+\Sigma_\epsilon)^{-1}A C_\theta,
\quad R=\mathrm{tr}(Q C_{\rm post}Q^*)/m.
\]

La primera expresión exige que `A Cθ A*+Σε` sea invertible; con ruido cero suele ser singular incluso si A tiene rango completo de columnas. En ese caso se utiliza pseudoinversa de Moore–Penrose y condicionamiento sobre observaciones consistentes. La forma inversa `(Cθ⁻¹+A*Σε⁻¹A)⁻¹` requiere covarianzas invertibles. R puede calcularse sin miles de campos y predice riesgo bajo sus supuestos. Para el banco esférico histórico, la misma expresión con covarianza correcta da riesgo del estimador LINEAL correspondiente; no es posterior gaussiano exacto de ese banco. Un valor bajo de seis S no garantiza R bajo; minimizar R puede tolerar mayor S si sacrifica frecuencias irrelevantes.

Existe antecedente del marco espacial-espectral en [Kailkhura etal., JMLR 2018](https://jmlr.csail.mit.edu/papers/v19/17-735.html), y de diseños ligados al kernel en [Krause etal., JMLR 2008](https://www.jmlr.org/papers/v9/krause08a.html) y [Belhadji etal., ICML 2020](https://proceedings.mlr.press/v119/belhadji20a.html). Las identidades anteriores y su aplicación a LARP son nuestra inferencia, no un descubrimiento de una nueva teoría ni garantías heredadas de esos algoritmos.

### 3.2. Robustez y supresión espectral no son sinónimos

Reteniendo exactamente m de n sensores de un canal mediante subconjunto uniforme, para cualquier modo del conjunto fijo original:

\[
\mathbb E\left[S_m(k)\mid X\right]
=1+\frac{m-1}{n-1}\left[S_n(k)-1\right],\qquad 1\le m\le n,\ n>1.
\]

Se obtiene expandiendo el cuadrado de la suma: cada término diagonal tiene inclusión m/n y cada par ordenado m(m−1)/(n(n−1)). Es una deducción finita exacta; si S_n≈0, aparece un suelo `(n−m)/(n−1)`. El thinning Bernoulli estacionario habitual produce `1−p+pS(k)`. [Kim/Torquato, PRB 2018](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.97.054105) estudia imperfecciones y pérdida de HU.

Esto invalida deducir inmunidad a fallos independientes a partir de HU. **No invalida** que una distribución mantenga mejor cobertura o menor error después de pérdidas: ese beneficio necesita medir función, ley de daño y rival robusto. Una lesión correlacionada y una pérdida uniforme son intervenciones distintas.

## 4. Cómo leer y usar el lote

Las32 fichas son alternativas de trabajo, no32 baterías que haya que ejecutar. IDs `B01–B32` pertenecen al lote2026-10-09; no reemplazan H1–H6 ni H-R. Toda predicción empírica se formula ahora, después de inspeccionar evidencia vieja: su confirmación requiere datos nuevos. Las identidades algebraicas se verifican como propiedades, sin convertir una prueba de código en apoyo a utilidad MHU.

Prioridades: **P0**, chequeo barato obligatorio; **P1**, candidato a siguiente ensayo; **P2**, condicionada a un resultado de P1; **P3**, aparcada. Son decisiones de cartera, no posteriors. Costes son TECHOS PROPUESTOS para fases futuras, no promesas de rendimiento; incluyen preparación, construcción y escritura en el contrato que se congele. Ninguna ficha abre una corrida por sí sola.

### B01 — La cobertura por canal explica la mayor ganancia local

**Prioridad:P1. Origen:**evidencia de muestreo, inferencia causal todavía no identificada;R02, R03.

**Mecanismo y predicción:** reducir distancia/vacíos del sensor del canal correcto facilita estimación local; un constructor local competente debería conservar la mayor mejora aviar aunque falle el certificado. Full tendrá poco efecto incremental bajo igual presupuesto de vecindario.

**Fallo/confound:** una cola de vacíos no medida o correlación de orden superior puede importar; igualar sólo p95 no aísla todo. Full/local cambia posiciones; emparejar estadísticas posteriores de su efecto puede sobrecontrolar un mecanismo.

**Prueba nueva:** primeras realizaciones full/local desde inicializaciones comunes, conservando conteos y presupuesto; decoder local competente común, queries y campos nuevos. Endpoints por geometría: NMSE y cobertura declarada. Un contraste residual separado sólo se admite si tiene solapamiento real.

**Cierre:** si el local reproduce utilidad dentro del margen práctico con precisión suficiente, retirar necesidad del término MHU para ese régimen. Si full gana, investigar el mediador antes de atribuirlo a ondas largas.

### B02 — El riesgo matricial predice mejor que el certificado MHU

**Prioridad:P1, primera. Origen:**deducción§3.1;R03–R05.

**Mecanismo y predicción:** amplitudes en diferencias/sumas de modos determinan la Gram. Rango, dirección de autovalores y covarianza de señal predecirán las inversiones mejor que seis medias S.

**Fallo/confound:** un riesgo calculado con la banda del test es oracle; singularidad y prior desconocido cambian la conclusión. Correlación sobre los tres X viejos sirve para diagnosticar, no confirmar.

**Prueba:** verificar primero identidades por canal y descomponer nulidad/ruido; después predecir R en geometrías nuevas antes de simular campos. Comparar dos predictores fijados —certificado/cobertura frente a riesgo matricial— en un banco de evaluación que ninguno haya usado para seleccionar estructuras.

**Cierre:** si R explica resultados y el certificado no añade predicción en contrastes identificables, priorizar diseño informativo. Bajo modelo y decoder correctos, reproducir R como riesgo esperado verifica una identidad; el descubrimiento posible está en transferencia y diseño, no en ese cotejo. Si los dos covarían sin separación, cerrar como NOT_IDENTIFIED; no inferir mediación por regresión.

### B03 — MHU puede servir a decoders baratos, sin mejorar información recuperable

**Prioridad:P1. Origen:**interacción local/oracle observada;R04, R05.

**Mecanismo y predicción:** una estructura facilita un filtro local cuando éste no puede acceder al resto de observaciones. Su ventaja decrece al ampliar alcance y usar un estimador competente con información comparable.

**Fallo/confound:** el oracle previo posee banda y ruido verdaderos, además de alcance global. Cambiar ambos simultáneamente confunde conocimientos con comunicaciones.

**Prueba:** factor2×2 de información del modelo —estimada en entrenamiento/común conocida— y alcance —Kvecinos/global—, con la misma regla lineal cuando sea posible. Endpoint: interacción de diseño con alcance, dentro de cada información; contar sensores consultados, MAC y tiempo.

**Cierre:** una ventaja limitada al presupuesto local puede justificar adquisición barata. Si sólo aparece frente a NN mal ajustado y desaparece frente al rival local competente, cerrar esa justificación de MHU.

### B04 — Un prior de señal diferente invierte el diseño conveniente

**Prioridad:P1. Origen:**inversión fine ya observada;R03, R05.

**Mecanismo y predicción:** disminuir potencia de muestreo donde el campo aporta poca información no ayuda al riesgo. Diseñar para smooth puede perjudicar otros modos o distribuciones de amplitudes.

**Fallo/confound:** escoger después del espectro escenas que atacan un diseño es selección adversarial post hoc. El decoder debe recibir idéntico entrenamiento y política de ajuste para todas las estructuras.

**Prueba:** congelar un banco de diseño y dos evaluaciones —prior compatible y desplazado— antes de scores; fases/orientaciones comunes, mismas varianzas analíticas. Comparar riesgo medio y peor región preregistrada, sin buscar nuevas bandas tras resultados.

**Cierre:** si el beneficio tiene una región específica, describirla y medir su utilidad. Si cambia de signo frecuentemente frente a rivales simples, MHU pierde prioridad como sesgo agnóstico; no reclamar superioridad global.

### B05 — La forma completa del espectro importa más que una depresión de seis modos

**Prioridad:P2. Origen:**diagnóstico externo del piloto;R03, R06.

**Mecanismo y predicción:** picos/anillos fuera del objetivo pueden crear error estructurado aunque bajen los seis modos. Una penalización de forma espectral relevante para señal rendirá mejor que el umbral binario de certificado.

**Fallo/confound:** S de densidad no es una función de transferencia completa; amplitudes, fases y decoder intervienen. Añadir muchas métricas y elegir la favorable infla hallazgos.

**Prueba:** panel externo congelado más una métrica de aliasing/direccionalidad, separada de MSE, con señales nuevas. Comparar dentro de un constructor común dos objetivos; ninguna banda externa selecciona el mejor checkpoint de geometría.

**Cierre:** si sólo se mueve energía a bandas dañinas, retirar ese objetivo. Si mejora una banda útil sin coste relevante, documentar diseño espectral finito; no exigir que la contribución lleve la etiquetaHU.

### B06 — El presupuesto de sensores raros domina parte de fine

**Prioridad:P0 para álgebra;P2 para cambiar conteos. Origen:**56 coeficientes,50/34 sensores D/E.

**Mecanismo y predicción:** con 56 coeficientes y 50/34 sensores, las nulidades mínimas son 6/22; los diseños históricos alcanzaban esos mínimos. Nuevas geometrías pueden tener nulidad mayor. Bajo independencia de canales, la geometría puede mejorar direcciones observadas, pero no recuperar todas las faltantes.

**Fallo/confound:** un prior anisótropo o correlación entre canales reduce riesgo aunque el rango siga bajo. Contar nullity no decide cuánto error aporta; el peso macro equiponderado es una elección.

**Prueba:** descomponer el riesgo en posterior/LMMSE por canal antes de construir. Un factor posterior de asignación compara conteos originales contra80×5 a Nfijo; no cambiar simultáneamente correlación ni decoder.

**Cierre:** si asignación domina mejora práctica, investigar reparto de recursos. Preservar proporciones aviares sólo cuando una tarea justifique sus demandas; cambiarlas nunca cuenta como control causal de MHU bajo conteos originales.

### B07 — Correlación entre canales cambia la utilidad de intercalar tipos

**Prioridad:P2. Origen:**cinco campos independientes son una decisión sintética;R04, R07.

**Mecanismo y predicción:** cuando hay componente compartida, muestras de tipos diferentes próximas pueden informar contrastes locales; cuando los campos son independientes, esas muestras no sustituyen al sensor correcto. El espectro cruzado puede importar más que cinco diagonales bajas.

**Fallo/confound:** un decoder multicanal puede resolver todo sin cambiar diseño. HU de cada población no implica independencia entre poblaciones.

**Prueba:** factor de covarianza congelada —independencia frente a componente compartida— con decoder conjunto LMMSE/GP común y mismas observaciones. Evaluar además contrastes entre canales y peor canal, evitando elegir mezcla favorable tras resultados.

**Cierre:** si el ranking sigue covarianza, priorizar diseño multicanal condicionado al problema. No transportar directamente resultados de scattering óptico a procesamiento neuronal; los operadores son distintos.

### B08 — Diseñar para riesgo esperado supera un proxy geométrico

**Prioridad:P1, rival principal. Origen:**§3.1;R04, R05.

**Mecanismo y predicción:** minimizar R integra ruido, frecuencias, queries y observaciones. Puede ganar con peor certificado MHU, porque no gasta recursos suprimiendo fluctuaciones irrelevantes.

**Fallo/confound:** sobreajuste al prior, cómputo de diseño caro y acceso a test. Una comparación entre variables/optimizadores distintos estima sistemas completos, no el efecto aislado del objetivo.

**Prueba:** una sola adaptación de objetivo de riesgo, con variables e inicialización comunes cuando se contraste el regularizador; prior de diseño fijo, evaluación compatible y una perturbación. Reportar construcción y decoder, incluyendo intentos y fallos.

**Cierre:** si gana en ambos regímenes y coste pertinente, pasa a diseño principal. Si sólo gana con información privilegiada, conservar diseños agnósticos como rivales. No ejecutar un catálogo de GP, MI, DPP, VS para escoger el vencedor retrospectivamente.

### B09 — En tareas no estacionarias, clustering puede ser útil

**Prioridad:P2. Origen:**rival aH6, inferencia propia;R04.

**Mecanismo y predicción:** si queries o variabilidad del campo se concentran en una región conocida desde entrenamiento, una densidad desigual bien asignada puede mejorar el riesgo frente a uniformidad global.

**Fallo/confound:** centrar el hotspot después de ver geometrías fabrica una victoria. Una lesión localizada no es la misma tarea que demanda localizada.

**Prueba:** dos mapas de demanda prefijados y un desplazamiento de hotspot fuera de entrenamiento; N/conteos comunes y mismo decoder. El diseño adaptativo conoce sólo la demanda de diseño, nunca el test.

**Cierre:** ventaja bajo demanda estable justificaría organización adaptativa. Si falla al desplazarse, identificar coste de especialización. No interpretar esa victoria como refutación de HU en campos estacionarios ni conservar uniformidad por motivos biológicos.

### B10 — Ventanas y bordes rompen parte de la ventaja del toro

**Prioridad:P2. Origen:**condiciones periódicas actuales;R09.

**Mecanismo y predicción:** máscaras/bordes alteran disponibilidad, observable espectral y error por query. Una organización certificada en el toro puede perder utilidad en un dominio recortado o con una frontera real.

**Fallo/confound:** truncar un patrón y compararlo con otro diseñado ya para el borde cambia recursos y optimización. La fuga espectral de una ventana no prueba que el patrón subyacente deje de serHU.

**Prueba:** declarar observable y máscara común, fijar número de sensores disponibles o informar su diferencia explícitamente; medir interior/borde como estratos congelados. Comparar primero rendimiento, no exponente inferido de un espectro enmascarado.

**Cierre:** si toda ventaja requiere periodicidad o queries interiores, acotar su aplicación. Sólo construir para fronteras cuando el caso de uso lo requiera; no añadir máscaras como otra colección de sorpresas.

### B11 — Pérdidas independientes introducen un suelo espectral

**Prioridad:P0 identidad;P2 utilidad. Origen:**§3.2, R08.

**Mecanismo y predicción:** el thinning destruye cancelaciones largas. Bajo retención de conteo fijo, la identidad finita del§3.2 predice S medio tras daño sin entrenar.

**Fallo/confound:** no confundir retención Bernoulli, conteo fijo y daño espacial. El mejor S residual no garantiza menor riesgo ni reconstrucción de un canal casi eliminado.

**Prueba:** verificar la identidad en datos sintéticos como control de software; si luego se estudia utilidad, ley común de pérdidas por canal y node ID, sin recoloración, con riesgo y cobertura residual frente a un rival robusto.

**Cierre:** si la identidad no se reproduce, diagnosticar código/supuestos. La identidad misma no necesita una confirmación empírica de arquitectura. Cerrar el argumento general «HU garantiza robustez» y mantener abierta una ventaja funcional específica demostrable.

### B12 — Daño correlacionado favorece redundancia local específica

**Prioridad:P2. Origen:**rival a robustez global;R04, R08.

**Mecanismo y predicción:** tolerar una lesión requiere disponibilidad fuera de ella y caminos/observaciones redundantes. Separar homogéneamente tipos puede ayudar, pero una colocación optimizada para la ley de daño puede hacerlo mejor sinHU.

**Fallo/confound:** elegir radio y centro de lesión para atacar MHU tras inspección. Igual porcentaje perdido puede ocultar diferencias de canal raro o de demanda espacial.

**Prueba:** una distribución de lesiones congelada en diseño y otra desplazada; mismos sensores/coste/decoder y pruebas de daño comunes. Separar riesgo condicional de sobrevivientes y número de pérdidas por tipo; ningún promedio debe esconder desaparición de E.

**Cierre:** si un rival robusto iguala o supera MHU, continuar redundancia y ley de daño. Una mejor curva de degradación sin matching residual es efecto total del diseño, no evidencia aislada de ondas largas.

### B13 — Con ruido heterogéneo importa la información ponderada

**Prioridad:P2. Origen:**Σruido en§3.1;R04, R07.

**Mecanismo y predicción:** sensores con ruido o coste desigual aportan distinta información. La matriz A*Σε⁻¹A puede favorecer una distribución que no suprima fluctuaciones de número sin ponderar.

**Fallo/confound:** asignar sensores buenos a posiciones favorables sólo en un brazo mezcla geometría y calidad. Pesos negativos/decoraciones de scattering no equivalen a precisión estadística positiva.

**Prueba:** dos niveles de ruido fijados por identidad física y permutaciones cruzadas comunes, con decoder ponderado para todas las estructuras. Construcción puede usar el mapa de ruido de diseño; la evaluación incluye un mapa nuevo.

**Cierre:** si domina información ponderada, orientar el constructor a ella. No exigir una HU de conteos que trate todos los sensores como iguales ni reutilizar conclusiones de composites ópticos sin derivar el operador correspondiente.

### B14 — Integrar una señal y reconstruirla requieren diseños distintos

**Prioridad:P3, prueba analítica específica. Origen:**R06, R10.

**Mecanismo y predicción:** la varianza de una integral con traslación aleatoria pondera espectro del integrando y del muestreo; reconstrucción usa matriz de información y queries. Una distribución puede ser buena para un objetivo y mala para el otro.

**Fallo/confound:** nuestros campos sin modo DC tienen integral conocida cero; estimarla no sería una tarea informativa. La independencia de puntos o reglas de pesos también cambia garantías.

**Prueba:** sólo si surge necesidad de integración, usar funciones con integrales desconocidas para el estimador y referencias analíticas, comparando estratificado/RQMC, local yMHU. No introducir este benchmark para conseguir que MHU gane una tarea nueva.

**Cierre:** un beneficio se registra como cuadratura bajo ese dominio. Los teoremas de repulsión en d≥3 no acreditan LARP 2D, conteos fijos o reconstrucción neuronal.

## 5. Hipótesis de computación y heterogeneidad

### B15 — Una marca invisible al programa no puede cambiar su función

**Prioridad:P0, identidad de dependencia. Origen:**contrato del forward, inferencia propia.

**Mecanismo y predicción:** con X, E, entradas, puertos, pesos, RNG y scheduling iguales, relabelar sin que ninguna operación consuma etiquetas debe dejar logits, loss y gradientes idénticos. La certificación geométrica puede cambiar sin una vía causal al cálculo.

**Fallo/confound:** máscaras, selección de sensores o puertos construidos por tipo son vías ocultas. Eliminar un embedding no basta si Edepende de marcas.

**Prueba:** inventario explícito de dependencias y contrafactuales sobre el mismo estado; activar después exactamente una vía tipada. Exigir identidad acorde al determinismo declarado, no una accuracy parecida ni una media estadística.

**Cierre:** diferencias en el brazo ciego invalidan el contraste y abren BUG/interfaz. Identidad demuestra que entrenar más ese brazo tiene información cero sobre organización de marcas; no refuta una red que sí las consume.

### B16 — El currículo enseña soporte contextual antes que estructura MHU

**Prioridad:P2, sólo si vuelve la línea neuronal. Origen:**BALANCED;sin confirmación nueva.

**Mecanismo y predicción:** exposiciones de roles, motivos, orientaciones y calendario pueden reducir atajos; el éxito seguirá soporte de contextos sobre Grid/local, independientemente deS(k).

**Fallo/confound:** la primera métrica de cobertura empata24/24 en el ensayo; BALANCED cambia otras propiedades y UNIFORM falla en train. No aislar balance por renombrar el paquete.

**Prueba:** construir factorial admisible de balance y orientación manteniendo soporte/coste cuando sea posible; si no es posible, declarar estimando de paquete. Panel nuevo de contextos/fuentes reservadas y contrafactuales b0/b1. AUX61 permanece conocido, nunca test ciego.

**Cierre:** una única intervención presupuestada; si el núcleo no aprende regla transferible, cerrar ese intento sin retocar hasta pasar. Su fracaso sigue siendo instrumental respecto a MHU.

### B17 — Los tipos útiles deben estar en el cono causal, no sólo cerca

**Prioridad:P1 como preflight, sin entrenamiento. Origen:**grafo dirigido y marcas funcionales;inferencia propia.

**Mecanismo y predicción:** importa la disponibilidad de operaciones y caminos ordenados dentro de T pasos hacia cada query. Un tipo cercano en Euclídeo puede quedar detrás de un cuello de botella.

**Fallo/confound:** diseñar tareas a medida del constructor de conos hace trivial su ventaja. Con T grande todos los conos pueden incluir todo, eliminando el factor.

**Prueba:** reachability y caminos tipados para T=2,4,8,16 con tareas abstractas prefijadas; comparar marcas nativas, locales y colocación para déficit causal a X/E/conteos fijos. Un oracle verifica factibilidad antes de aprendizaje.

**Cierre:** si no hay diferencia de déficit, no hay manipulación. Si predice mejor queS espacial, investigar colocación funcional sobre grafos; su utilidad no se llama MHU específica sin separar las dos variables.

### B18 — El espectro del operador de comunicación puede ser el sesgo relevante

**Prioridad:P1 analítica;R11.

**Mecanismo y predicción:** para un operador simétrico de difusión, proyectar `b_c=1[z=c]−n_c/N` en autovectores del grafo mide fluctuaciones que su filtro temporal amplifica. S Fourier euclídeo sólo se relaciona bajo condiciones adicionales.

**Fallo/confound:** mezclar espectro espacial, Laplaciano, matriz recurrente entrenada y PSDde señal por compartir palabra «espectral». Para Edirigido/nonnormal, el teorema simétrico no se hereda.

**Prueba:** operador lineal declarado y respuesta exacta antes de red; contraste de espectro espacial parecido con proyecciones distintas y el contraste inverso, si existe soporte. Una red dirigida necesitaría otro operador y estimando.

**Cierre:** falta de separación implica NOT_IDENTIFIED. Un efecto que siga ganancias del operador favorece diseño de transporte. Los resultados sobre oversquashing motivan medir topología, no certifican nuestra propuesta de marcas.

### B19 — Routing útil domina en tareas remotas

**Prioridad:P2 tras competencia;R11, R12.

**Mecanismo y predicción:** reemplazar un número fijado de aristas por rutas útiles aliviará cortes/compresión más que bajar S de marcas. Igual grado no iguala alcance ni redundancia.

**Fallo/confound:** añadir enlaces aumenta recursos; cableado largo puede costar más. Hops de llegada no garantizan transmisión ni entrenamiento reproducible.

**Prueba:** factor marcas×routing, con N, d, T, P y pares procesados declarados, aristas reemplazadas y mismos puertos/mundos. Rival expansor/oracle de rutas acotado; adaptación no hereda garantías de Exphormer.

**Cierre:** si no llega información dentro de T, prueba de aprendizaje sin capacidad. Si routing resuelve el problema y las marcas no aportan un efecto práctico identificado, cerrar MHU en esa línea remota.

### B20 — El puerto/readout puede dominar un efecto atribuido al sustrato

**Prioridad:P0 para auditoría;P2 para interacción. Origen:**contratos de puertos y queries.

**Mecanismo y predicción:** elegir sensores, queries y destino mediante una asignación dependiente de geometría cambia error de adquisición y dificultad de caminos antes de la computación.

**Fallo/confound:** fijar node IDentre geometrías no fija posición física; fijar posición y buscar nodo cambia ID/alcance. No se pueden declarar ambas cosas iguales sin especificar la intervención.

**Prueba:** dos interfaces congeladas —queries físicas comunes/interfaz abstracta independiente— y oracles de adquisición/transportes separados. Contabilizar distancias, roles, hops y disponibilidad; análisis por estratos escogidos antes de resultados.

**Cierre:** si el efecto desaparece al controlar interfaz, estudiar diseño de puertos. No atribuirlo a núcleo emergente ni compensarlo cambiando readout hasta superar98%.

### B21 — La diversidad funcional puede ayudar sin requerir colocación MHU

**Prioridad:P2. Origen:**rival aH3;R13, R14.

**Mecanismo y predicción:** múltiples transformaciones aportan especialización. Dentro del MISMO modelo tipado, una colocación local o por cono causal puede igualar a MHU aunque F supere G.

**Fallo/confound:** F/T añaden matrices, adaptadores, MAC y capacidad; igualar parámetros reduciendo ancho cambia memoria. Ganar F vs G no prueba utilidad de una distribución espacial.

**Prueba:** separar comparación arquitectónica G/T/F de colocación dentro de un F fijo. Compartir matrices por tipo, conteos y presupuesto; medir parámetros entrenables REALES, estado y coste activo, además de diversidad aprendida/condicionamiento contextual como rival.

**Cierre:** si sólo gana diversidad, continuar ese principio y retirar restricción espacial sin valor incremental. No usar nombres biológicos de tipos como garantía de funciones distintas aprendidas.

### B22 — Modulación por contexto puede sustituir heterogeneidad espacial estática

**Prioridad:P2. Origen:**R14, aplicación propia.

**Mecanismo y predicción:** un contexto de baja dimensión selecciona transformaciones útiles en tiempo, evitando depender de que un tipo fijo esté cerca de cada query. Puede favorecer recombinación de tareas con mapas espaciales simples.

**Fallo/confound:** un contexto alimentado con labeldel test filtra la respuesta; adaptar pesos efectivos puede añadir capacidad invisible al recuento de P. También puede sobreajustar.

**Prueba:** contexto inferido únicamente de la entrada permitida, frente a heterogeneidad fija a recursos declarados; nuevas combinaciones de programas y controles de permutación contextual. Sin ampliación de núcleo hasta contar con competencia instrumental.

**Cierre:** si gana la modulación en mapas no MHU, la contribución es selección contextual. El antecedente HU+RNN no permite imputar su generalización aHU; tampoco valida nuestra adaptación.

### B23 — Más recurrencia puede borrar la selección que intenta resolver

**Prioridad:P2. Origen:**R11, R15.

**Mecanismo y predicción:** puede existir una ventana de Ttras la llegada de señales y antes de mezcla/atenuación. Más pasos no garantizan preservar rol o contexto.

**Fallo/confound:** sustituirT en inferencia prueba extrapolación del algoritmo aprendido; entrenar aotro T cambia optimización y cómputo. Un Jacobiano bajo no sustituye precisión de tarea.

**Prueba:** pocasTcongeladas con distancia dirigida estratificada; controles lineal, persistente y selector determinista de roles. Separar llegada, memoria y aprendizaje; medir contrafactuales y mensajes útiles.

**Cierre:** si un oracle de interfaz falla, corregir contrato antes de red. Si una intervención no cumple su presupuesto/puerta, cerrar; no añadirTu otra puerta para rescatar accuracy.

### B24 — Un beneficio inicial puede desaparecer al aprender conexiones

**Prioridad:P3. Origen:**H5 sin probar;R16.

**Mecanismo y predicción:** una inicialización estructurada puede estabilizar entrenamiento temprano, mientras conexiones efectivas finales adaptadas a tarea pierden su organización inicial.

**Fallo/confound:** permitir plasticidad a MHU pero no a rivales, o comparar sólo mejores checkpoints, mezcla inicialización y búsqueda. El S de coordenadas puede permanecer igual aunque cambien aristas/pesos.

**Prueba:** factorial de inicialización×plasticidad con misma regla, densidad y presupuesto, usando tareas nuevas; congelar curva temprana y endpointfinal. Medir por separado geometría, topología y operador aprendido.

**Cierre:** beneficio sólo temprano justifica inicialización si amortiza costes, no una topología final MHU. No actualizar H5 con los actuales fallos de matching: allí no se aprendió conectividad.

## 6. Hipótesis de identificación, escalado y diseño de laboratorio

### B25 — El certificado finito puede ser un objetivo demasiado estrecho

**Prioridad:P0 descripción;P2 validación nueva. Origen:**R01, R09.

**Mecanismo y predicción:** un constructor puede bajar el conjunto optimizado sin controlar modos vecinos, anisotropía u orden homotípico. Superar el contrato finito no acredita el límitek→0 ni desorden aviar empírico.

**Fallo/confound:** cambiar criterios después de éxitos borra historia; seleccionar cortes espectrales o componentes favorecidos crea apariencia de validación.

**Prueba:** panel diagnóstico NUEVO, modos/ventanas/orientaciones declarados antes de medición, sin reclasificar certificados antiguos. Si aparece utilidad sin pasarHU, conservar utilidad y describir la propiedad real.

**Cierre:** ausencia de transferencia espectral limita el nombre empleado; no supone ausencia de función útil. No escalar tamaños sólo para que una figura permita pronunciar «asintótico».

### B26 — La población rara no ofrece suficiente separación de escalas

**Prioridad:P3 salvo predicción de escala;R01, R09.

**Mecanismo y predicción:** E34 tiene pocas distancias entre espaciado típico y caja. Certificar unas frecuencias puede esconder orden parcial y errores finitos; densidad física fija cambia kmin al variarN.

**Fallo/confound:** aumentarN, dimensión, cutoff entero y radios simultáneamente modifica bandas y restricciones. Más puntos certificados no equivale a más información sobre cómputo.

**Prueba:** sólo tras un efecto funcional, dos tamaños prefijados a densidad y proporciones constantes; separar banda física de cutoff entero, registrar todas las realizaciones y reservar paneles. No extrapolar exponente con pocos modos de una caja.

**Cierre:** escalar si la hipótesis predice cómo debería cambiar riesgo/coste, no porque haya RAM. Sin predicción discriminante, conservar la limitación N400 y posponer.

### B27 — Matching puede bloquear una ruta causal y volver el contraste sin soporte

**Prioridad:P0 de estimando;sin nuevo buscador. Origen:**v2, Parseval.

**Mecanismo y predicción:** fijar varianza exacta de conteo mientras se modifica potencia espectral puede obligar compensaciones imposibles o muy raras. Cobertura/varianza pueden ser mediadores de la intervención.

**Fallo/confound:** retirar guardas después del fracaso cambia pregunta; un generador que no encuentra contraste tampoco prueba espacio vacío. Las130 desigualdades no son130piezas independientes ni todos los confounds.

**Prueba:** definir DAG/estimando antes del control: efecto total de regularizador, contraste residual limitado o mecanismo de observación. Cotas de factibilidad y rango de manipulación preceden entrenamiento. Si no hay soporte, publicar NOT_IDENTIFIED.

**Cierre:** preservarv2y su cotaq=.5. Una pregunta funcional de efecto total puede ser mejor que insistir en ese residual; ninguna relajación se presenta como cumplimiento del contrato antiguo.

### B28 — La movilidad condicionada podría revelar sólo una pequeña componente

**Prioridad:P3, contingente. Origen:**95 vecinos y rareza del kernel.

**Mecanismo y predicción:** filtrarMIN eleva aceptación por construcción; lo interesante es si amplía desplazamiento/estados por segundo con las130 guardas referidas siempre anativa.

**Fallo/confound:** escoger vecinos uniformes cambia el kernel; usar mínimos del estado nuevo relaja restricciones. Tres ciclos sin ruta de dos swaps no excluyen rutas más largas ni prueban utilidad.

**Prueba:** conservar masas relativas al condicionar y compararlo contraoriginal con nuevos RNG y techo propio, como en el plan guardado. Sólo activarlo si el control alcanzable responde una prueba funcional definida.

**Cierre:** oscilación local cierra esa búsqueda. Aceptación alta nunca es endpoint científico suficiente. No consumir la próxima fase principal en enumerar más movimientos por curiosidad de infraestructura.

### B29 — El coste amortizado cambia qué diseño merece usarse

**Prioridad:P1 para la decisión. Origen:**costes locales medidos;R17.

**Mecanismo y predicción:** una mejora pequeña puede valer en adquisición física reutilizada, mientras construcción/certificación y decoder caro la vuelven poco atractiva para consultas escasas.

**Fallo/confound:** sumar segundos, GPU memoria, longitud de cable y parámetros con pesos arbitrarios crea una métrica conveniente. OcultarHPO, preentrenamiento o intentos no iguala cómputo.

**Prueba:** escenario de uso y número de reutilizaciones declarados; comparar riesgo a presupuestos compartidos y publicar costes separados. LaGPU se evalúa con precisión y carga justificadas, sin mover certificados float64 a float32 por velocidad.

**Cierre:** mantener MHU sólo si existe región de beneficio/coste identificable. Una estructura útil y más barata que falle certificado es un éxito de LARP, no un fracaso que requierarescatarMHU.

### B30 — 3D sólo merece trabajo si cambia una restricción relevante

**Prioridad:P3. Origen:**R16, R17;noNOT_RUN→resultado.

**Mecanismo y predicción:** un dominio volumétrico real o coste de cableado/delay podría favorecer organización3D. En un cálculo abstracto con enlaces libres, la dimensión por sí sola no añade un mecanismo.

**Fallo/confound:** copiar seis vecinos o cutoff entero cambia alcance/banda física; no pueden igualarse densidad, longitud, hops, EyNsimultáneamente sin cambiar estimando.

**Prueba:** comparar primero dentro de3D MHU/local bajo banda y recursos volumétricos definidos. Un contraste2D/3Dnecesita un contrato de coste propio; un certificado por planos no certifica volumen.

**Cierre:** sin tarea/restricción volumétrica concreta, no ejecutar. RNN espacial 3D y generación HU 3D ya tienen antecedentes; mera factibilidad carece de la novedad quejustifiqueprioridad.

### B31 — Multicapa puede aportar complementariedad o capacidad, no MHU

**Prioridad:P3. Origen:**R12, R17, R18.

**Mecanismo y predicción:** planos con vacíos y rutas complementarios pueden ayudar aunque sus espectros individuales sean idénticos. Una máscara aprendida puede atender dependencias mejor que una disposición estática.

**Fallo/confound:** apilar suele aumentar nodos, parámetros, MAC y actualizaciones; T8+T8 no equivale automáticamente a T16. Sin uso de posiciones, tipos o máscaras, colocar tokens MHU no cambia atención densa.

**Prueba:** después de competencia, N total/P/pares activos comunes, copia frente a traslación prefijada, enlaces interplano congelados y rival local/expansor. Comparar máscara aprendida contabilizando preentrenamiento y congelándola antes de test.

**Cierre:** ventaja de complementariedad se atribuye aese mecanismo. No desarrollarMHUmulticapa sin valor incremental frente a rivales fuertes ni por atractivo del diagrama transformer.

### B32 — El mejor resultado puede ser un diseño híbrido que no conserve HU

**Prioridad:P2 trasP1. Origen:**cartera abierta, inferencia propia.

**Mecanismo y predicción:** repulsión local para disponibilidad, pocos objetivos de información y routing específico podrían capturar beneficios relevantes sin garantizar una propiedad geométrica global.

**Fallo/confound:** añadir varios mecanismos juntos vuelve imposible atribución y consume más recursos. Elegir componentes que ya ganaron en muchos ensayos induce selección.

**Prueba:** sólo después de identificar un mecanismo con efecto independiente, añadir UN segundo con factorial mínimo y presupuesto común. Predicción de interacción y contraejemplo se congelan antes de evaluación.

**Cierre:** si el híbrido domina utilidad/coste, conservarlo bajo su descripción exacta y abandonar requisito MHU. Si sólo gana por recursos, volver al modelo simple. No convertir esta ficha en licencia para construir un núcleo cada vez más complejo.

## 7. Selección: qué haría primero y qué dejaría quieto

| Orden | Trabajo elegido | Información que aporta | Techo propuesto | Estado |
|---|---|---|---|---|
| 0 | B15 y dependencia del tratamiento | Descarta contrastes con tratamiento invisible o interfaces ocultas. | 30s de chequeos sintéticos; cero entrenamiento | Propuesto, sólo si se vuelve al núcleo |
| 1 | B02+B06, Gram/riesgo/nulidad | Puede explicar inversiones y evitar buscar una ventaja geométrica donde no hay información observada. | 30s numéricos sobre archivos existentes, validación aparte | Siguiente trabajo recomendado, NOT_RUN |
| 2 | B01+B03+B04+B08 | Compara exclusión local, término MHU y objetivo de información con señales y decoders competentes. | Una fase nueva≤900s CPU, máximo tres familias y ocho inicializaciones comunes | Diseño para preregistrar, NOT_RUN |
| 3 | B07 o B13, uno solo | Comprueba transferencia de la explicación a covarianza multicanal o ruido heterogéneo. | ≤180s de evaluación; reutilización geométrica exploratoria explícita | Condicional a fase2 |
| 4 | B17+B18 | Define disponibilidad funcional y operador antes de volver a aprendizaje distribuido. | ≤60s analíticos, sin nuevas redes | Pista secundaria |

Los techos no son autorización de ejecución ni protocolo ya sellado. No se gastan32 presupuestos de fichas; se escogen predicciones incompatibles y se conserva toda salida. Las puertas anteriores de98%,120s/cuatrocorridas, las series cerradas y sus priors no se cambian. Un nuevo ensayo neuronal tendría un contrato propio, sin reabrir por accidente el piloto original.

### Fase1: diagnóstico de información, antes de otro constructor

Reusar las nueve geometrías de muestreo y sus asignaciones sólo como diagnóstico posterior. Reconstruir matrices con frecuencias, queries y ruido históricos; conservar originales. Para cada canal: rango, nulidad, matriz de información, riesgo esperado con covarianza correcta y descomposición de incertidumbre observada/no observada. Verificar equivalencia de dos fórmulas de riesgo, el caso sin ruido por pseudoinversa y un caso ortonormal sintético. No llamar a la expresión del banco esférico posterior gaussiano exacto.

Preguntas concretas: ¿los modos responsables de los autovalores malos quedan fuera del conjunto optimizado?, ¿qué parte del riesgo fine procede de D/E?, ¿coinciden las inversiones previstas por riesgo con los scores guardados? Las respuestas sobre estos datos sirven para formular predicciones nuevas. No seleccionar después una versión del predictor que ajuste mejor sus seis diferencias y llamarla confirmación.

**Stop:** incoherencia algebraica o de hashes detiene interpretación. Si no queda un contraste discriminante entre cobertura, riesgo y MHU, no generar otra tanda geométrica por inercia. Si aparece, congelar una predicción y pasar a fase2. La disponibilidad de GPU no altera este orden.

### Fase2: una comparación útil que puede cerrar MHU en este régimen

Recomiendo tres familias, ocho inicializaciones geométricas nuevas comunes, N400 y conteos originales: **local aviar competente**, **mismo constructor con término espectral**, **mismo espacio de variables con objetivo de riesgo**. El tercero es UN rival de información, no una búsqueda de veinte algoritmos. Grid balanceado y multiclase blue noise siguen como comparadores pertinentes de un panel posterior; la comparación principal no necesita construirlos todos antes de responder si el regularizador añade valor sobre local.

La comparación del objetivo exige conservar grados de libertad, términos físicos comunes, inicialización y procedimiento de construcción; si una implementación no permite eso, declarar comparación de sistemas completos y limitar causalidad. No repetir el experimento desfavorable de130 swaps sobre X ya coadaptado por nativa como supuesto rival fuerte. El objetivo local no consume campos del test. El objetivo de información usa una covarianza y queries de DISEÑO declaradas antes de cualquier score de evaluación.

Propuesta de datos: independencia de canales inicialmente; prior de diseño suave, evaluación compatible y una banda nueva desplazada prefijada; ruido σ=0/.1 y fases/orientaciones comunes. Separar entrenamiento del modelo de señal de geometría y test. Decoder local ridge/GP de Kvecinos con K fijado o elegido sólo por validación de entrenamiento común; decoder global con modelo estimado en ese mismo entrenamiento. Mantener oracle de banda únicamente como referencia de información privilegiada, no como brazo que decide mérito bajo información aprendida.

Antes de implementación deben congelarse el kernel concreto de señal, covarianza, frecuencia/banda física, K, regularización y regla de escala del objetivo de riesgo. Este documento recomienda la pregunta y la familia; **no se presenta como un preregistro listo para ejecutar con decisiones científicas sin resolver**. Esa especificación debe resultar del diagnóstico de fase1 y escribirse antes de generar realizaciones o scores nuevos. SOL no debe improvisarla mirando rendimiento.

Para recursos, propone≤30s por construcción,24 construcciones máximo=720s, preparación/evaluación/escritura≤180s restantes: techo global900s, una tentativa por celda, sin sustitución de semillas ni filtrado de controles por certificado MHU. Los fallos se conservan en el denominador. Los tiempos históricos sugieren factibilidad N400, pero un preflight de coste separado puede cerrar por recursos; no garantiza convergencia ni permite ajustar por utilidad. Registrar costes de diseño y consulta, en lugar de convertir más cómputo en una ventaja silenciosa.

**Endpoints:** riesgo/NMSE por geometría y canal; contraste primario full−local dentro del decoder local competente y prior compatible. El contraste con diseño informativo y global delimita el caso de uso. El banco desplazado comprueba transferencia; la población rara tiene endpoint adicional, sin convertirlo en segundo éxito independiente. No seleccionar el mejor decoder, banda o semilla como endpoint retrospectivo.

Como umbral de ingeniería propongo **5% de reducción relativa de NMSE** frente al rival local competente en el régimen primario; es una decisión práctica nueva, no el ROPE arquitectónico antiguo. Un cero numérico o un error baseline extremadamente pequeño hace inadecuada esa escala: la escala absoluta debe fijarse con el riesgo del modelo/diagnóstico antes de correr, no tras resultados. Ocho geometrías son suficientes para un primer contraste descriptivo, pero no garantizan un intervalo estrecho ni una conclusión de equivalencia.

**Continue:** efecto≥margen práctico, signo reproducido y explicación que prediga la interacción o transferencia, con costes publicados y sin daño relevante escondido en un canal. Entonces una confirmación con geometrías/campos nuevos y análisis de incertidumbre dimensionado constituye la única ampliación principal de MHU.

**Stop:** si un nulo es suficientemente preciso para excluir el margen útil, cerrar la utilidad del término MHU en ese régimen y continuar con el rival. Si el diseño de riesgo/local consigue utilidad comparable y menor coste, retiraría MHU como objetivo de ingeniería aunque una propiedad residual siga sin identificar. **Inconclusive:** fallo de manipulación, soporte, precisión o recursos se conserva como tal; no se cambia la puerta ni se concede otra batería automáticamente.

### Qué no haría

No abriría3D/multicapa por ahora, no añadiría cientos de semillas a una métrica sin mecanismo, no relajaríamos guardas antiguas para fabricar un control, y no usaría XOR como árbitro de HU. Tampoco intentaría demostrar originalidad a base de llamar «emergente» a estados o «biológico» a cinco operadores. La prioridad viene de una predicción nueva que podría fallar.

## 8. Literatura y prior art que cambian decisiones

La revisión es dirigida, no una certificación exhaustiva de novedad. Se consultan fuentes primarias; cuando sólo se verificó abstract/editor se declara. Las aplicaciones a LARP son inferencias propias. Los artículos revisados, preprints y patentes no se cuentan como evidencia equivalente. Un preprint y su artículo posterior son UNA línea de trabajo, no réplicas independientes.

### R01 — Definición física y observable

Torquato/Stillinger, *Local Density Fluctuations, Hyperuniform Systems, and Order Metrics*, PRE 2003, DOI 10.1103/PhysRevE.68.041113, revisado. [Editor](https://link.aps.org/doi/10.1103/PhysRevE.68.041113). Fundamenta el observable y límite de escalas; no es prueba de capacidad neuronal. Nuestros certificados pequeños requieren descripción finita.

### R02 — Rival computacional multiclase anterior a la retina MHU

Wei, *Multi-Class Blue Noise Sampling*, ACM TOG/SIGGRAPH2010, DOI 10.1145/1778765.1778816, revisado. [Autor](https://www.liyiwei.org/papers/noise-sig10/), [registro institucional](https://hub.hku.hk/handle/10722/141787). Diseña clases/uniones, controla conteos y contempla sensor layouts. Es antecedente directo de organización multicanal; no se equipara blue noise con HU asintótica. Una adaptación nuestra requiere validar su fuerza y coste.

### R03 — Diseño espacial-espectral ya aplicado a reconstrucción

Kailkhura, Thiagarajan, Rastogi, Varshney, Bremer, *A Spectral Approach for the Design of Experiments*, JMLR 19(34),2018, revisado. [Publicación](https://jmlr.csail.mit.edu/papers/v19/17-735.html). Relaciona llenado espacial y calidad espectral y evalúa reconstrucción/surrogates. El marco «cobertura frente a espectro» no es una novedad general de LARP; una contribución requerirá mecanismo/condiciones propios.

### R04 — Colocación basada en información

Krause, Singh, Guestrin, *Near-Optimal Sensor Placements in Gaussian Processes*, JMLR 9,2008, revisado. [Publicación](https://www.jmlr.org/papers/v9/krause08a.html). Motiva objetivos de información y robustez bajo supuestos GP. Sus resultados de submodularidad no se heredan por cualquier reparto marcado y conteos fijos; aquí fundamentan un rival, no su garantía automática.

### R05 — Kernel y espectro del operador de interpolación

Belhadji, Bardenet, Chainais, *Kernel interpolation with continuous volume sampling*, ICML 2020, revisado. [Actas](https://proceedings.mlr.press/v119/belhadji20a.html). Sus cotas de interpolación/cuadratura dependen del kernel. No estamos reproduciendo volume sampling ni atribuyendo sus garantías a un annealing multiclase; muestra que existe teoría más directa que la analogía aviar.

### R06 — Integración y espectro

Pilleboue etal., *Variance Analysis for Monte Carlo Integration*, ACM TOG/SIGGRAPH2015, revisado. [Fuente del autor](https://perso.liris.cnrs.fr/david.coeurjolly/publication/pilleboue-15-variance/). Analiza varianza de integración; no constituye por sí sola teoría del decoder neuronal. La distinción integración/reconstrucción y la derivación Gram del§3 evitan trasladar conclusiones entre problemas.

### R07 — MHU multicomponente con mecanismo óptico,2026

Keeney, Shi, Thomas, Yang, Jiao, *Multihyperuniform Particle Composites Inspired by Avian Photoreceptor Patterns for Multifunctional Optical Applications*, Advanced Optical Materials, publicación27jun2026, DOI 10.1002/adom.202503139, revisado. [Editor/abstract verificado](https://advanced.onlinelibrary.wiley.com/doi/abs/10.1002/adom.202503139). Formula condiciones sobre espectros cruzados para respuesta óptica. Refuerza exigir un operador físico/estadístico que conecte estructura y función. No valida adquisición neuronal. arXiv 2510.06402 pertenece al mismo trabajo.

### R08 — Imperfecciones y límites de robustez

Kim/Torquato, *Effect of imperfections on the hyperuniformity of many-body systems*, PRB 97,054105,2018, revisado. [Editor](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.97.054105). Estudia vacantes/desplazamientos y degradación de HU. La identidad de subconjunto fijo del§3.2 es nuestra deducción para el panel finito; ningún resultado de daño geométrico sustituye medir función después de lesión.

### R09 — Estimar S y probar HU exige supuestos

Hawat, Gautier, Bardenet, Lachièze-Rey, *On estimating the structure factor of a point process, with applications to hyperuniformity*, Statistics and Computing 2023, DOI 10.1007/s11222-023-10219-1, revisado. [Editor](https://link.springer.com/article/10.1007/s11222-023-10219-1). Relevante para estimación y ventanas; no convierte tres N400 toros optimizados en evidencia asintótica ni invalida retrospectivamente el certificado vigente.

### R10 — Repulsión útil sin necesidad de una tesis MHU

Hawat, Mastrilli, Bardenet, Lachièze-Rey, *Repelled Point Processes With Application to Numerical Integration*, Scandinavian Journal of Statistics 2026, DOI 10.1111/sjos.70073, revisado. [Editor](https://onlinelibrary.wiley.com/doi/abs/10.1111/sjos.70073). Teoremas bajo PPP, d≥3, repulsión pequeña y funciones suaves de soporte compacto. No garantizan utilidad para LARP 2D, conteos fijos, reconstrucción ni redes; evitan atribuir cualquier ganancia de repulsión aHU.

### R11 — Transporte y cuellos de botella del grafo

DiGiovanni etal., *On Over-Squashing in Message Passing Neural Networks: The Impact of Width, Depth, and Topology*, ICML 2023, revisado. [Actas](https://proceedings.mlr.press/v202/di-giovanni23a.html). Motiva analizar topología y capacidad de transporte. Los resultados bajo su clase de redes no se trasladan a cualquier GRU/atención; tampoco vinculan oversquashing conS Fourier espacial de nuestras marcas.

### R12 — Rival fuerte de atención dispersa

Shirzad etal., *Exphormer: Sparse Transformers for Graphs*, ICML 2023, revisado. [Actas](https://proceedings.mlr.press/v202/shirzad23a.html). Utiliza expansores/nodos globales y atención dispersa. Rival pertinente de routing y escalado; una versión con otro presupuesto de aristas no se presenta como reproducción fiel ni hereda garantías.

### R13 — Comunicación funcional dependiente del estado

Finkelshtein, Huang, Bronstein, Ceylan, *Cooperative Graph Neural Networks*, ICML 2024, revisado. [Actas](https://proceedings.mlr.press/v235/finkelshtein24a.html). Motiva separar estrategias funcionales de su colocación espacial. Adaptar escucha/emisión a LARP sería trabajo nuevo; el artículo no prueba utilidad de marcas MHU.

### R14 — Antecedente revisado más cercano a HU+RNN

Bull, Kuo, Smith, Buice, *Volume Transmission Implements Context Factorization to Target Online Credit Assignment and Enable Compositional Generalization*, NeurIPS 2025, revisado, DOI 10.52202/085713-4965. [Artículo primario](https://proceedings.neurips.cc/paper_files/paper/2025/file/da4dffbe0ea5181d0ad8c59e1641cecd-Paper-Conference.pdf). §2.1, p4 describe una colocación que los autores denominan hiperuniforme en 2D, tipos excitatorio/inhibitorio aleatorios y conectividad por distancia, junto con recurrencia/modulación. Es antecedente HU+RNN más cercano que la patente; no certifica cinco componentes MHU ni aísla una ablaciónHU. Sus resultados pertenecen a un paquete contextual/espacial, no se imputan al patrónHU.

### R15 — Profundidad y filtrado como mecanismos explícitos

Errica etal., *Adaptive Message Passing: A General Framework to Mitigate Oversmoothing, Oversquashing, and Underreaching*, ICML 2025, revisado. [Actas](https://proceedings.mlr.press/v267/errica25a.html). Justifica considerar mecanismos de profundidad/filtrado; no es razón para una parrilla de Tsin presupuesto ni prueba de una arquitectura MHU.

### R16 — Redes recurrentes espaciales en 3D ya existen

Achterberg etal., *Spatially embedded recurrent neural networks reveal widespread links between structural and functional neuroscience findings*, Nature Machine Intelligence 2023, DOI 10.1038/s42256-023-00748-9, revisado. [Editor](https://www.nature.com/articles/s42256-023-00748-9). Antecedente de regularización espacial y comunicación en 3D. Esta sesión verificó la fuente mediante revisión delegada; acceso directo de la raíz devolvió error del editor. No supone ventaja MHU ni vuelve novedoso apilar coordenadas.

### R17 — Escalar el diseño espectral tiene un antecedente eficiente

Shih, Casiulis, Martiniani, *Fast generation of spectrally shaped disorder*, PRE 110,034122,2024, revisado. [Editor](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.110.034122). FReSCo/NUFFT, O(NlogN), con diseños 2D/3Dy restricciones reales. Antes de inventar otro generador grande, estudiar este antecedente. Su coste publicado no garantiza el de nuestra adaptación discreta marcada, ni relevancia neuronal.

### R18 — Máscaras aprendidas cuentan también su preentrenamiento

Shirzad etal., *Even Sparser Graph Transformers* —Spexphormer—, NeurIPS 2024, revisado. [Actas](https://proceedings.neurips.cc/paper_files/paper/2024/hash/834fe9eecf8d1839f406a79c6982be05-Abstract-Conference.html). Rival de máscaras fijas: usa un modelo estrecho para seleccionar conexiones de otro mayor. Su construcción y entrenamiento previo deben contarse; no es validación de HU.

### R19 — Imagen MHU ya fue implementada físicamente

Zhao, Li, Cao, Sun, *Bionic Birdlike Imaging Using a Multi-Hyperuniform LED Array*, Sensors 21(12),4084,2021, DOI 10.3390/s21124084, revisado. [Texto primario](https://pmc.ncbi.nlm.nih.gov/articles/PMC8231846/). Estudia un arrayRGB y demosaicking simple; incluye rival blue-noise. Bayer cambia proporciones y los controles no aíslan microestructura. La velocidad del sistema LED/FPGA/Hadamard no se atribuye a MHU. Inferir independencia de tipos desde HU no es válido. Es antecedente de adquisición más directo que la observación retiniana, con alcance específico dehardware/decoder; no valida nuestro núcleo. El texto lo consultó el agente de adquisición; la raíz encontró recaptcha al abrirPMC.

### R20 — La retina ofrece inspiración y restricciones, no la conclusión neuronal

Jiao etal., *Avian photoreceptor patterns represent a disordered hyperuniform solution to a multiscale packing problem*, PRE 89,022721,2014, revisado. [Editor](https://link.aps.org/doi/10.1103/PhysRevE.89.022721). Observación de conos y modelo de empaquetamiento; no demuestra que kNN recurrente con cinco funciones sintéticas aprenda mejor. Nuestro término espectral explícito, optimizador y cantidades de células tampoco son una reproducción fisiológica.

### R21 — Aplicación MHU a antenas, sin transportar garantías

Christogeorgos, Okon, Hao, *A computational model for generating multihyperuniform distributions for realistic antenna array and metasurface designs*, EPJ Applied Metamaterials 11,5,2024, DOI 10.1051/epjam/2024003, revisado. [Editor](https://doi.org/10.1051/epjam/2024003). Diseño multiespecie con restricciones físicas y respuesta electromagnética; confirma que existen usos específicos para MHU, no una ventaja computacional genérica.

### R22 — Patente: antecedente técnico, no validación científica

IBM, *Hyperuniform and nearly hyperuniform neural networks*, solicitud publicada US20240202508A1,2024. [Texto de patente](https://patents.google.com/patent/US20240202508A1/en). Describe topologíasHU/NHUy contempla atención dispersa. **No es artículo revisado ni evidencia empírica independiente.** No se emite opinión de patentabilidad ni novedad legal. Bull2025es un antecedente científico más cercano paraHU+RNN.

### R23 — Preprint espacial reciente

Shakiba etal., *Harnessing cortical geometry, wiring, and function as inductive biases for recurrent neural networks*, arXiv 2606.14975, jun2026. [Manuscrito](https://arxiv.org/abs/2606.14975). **Preprint**, sin revisión acreditada aquí. Sugiere separar geometría, conectividad e inicialización funcional; no adopto sus resultados como confirmación ni como evidencia contra MHU. Es pista bibliográfica, no criterio de la cartera.

### R24 — Preprint blue-noise reciente

*Blue Noise as a Lattice Gibbs Ensemble*, arXiv 2608.13446, ago2026. [Manuscrito](https://arxiv.org/abs/2608.13446). **Preprint**, abstract revisado por el agente; métodos/código no auditados. Anuncia extensiones adaptativas/multiclase. No se necesita adoptarlo: Wei2010 sigue siendo antecedente revisado suficiente para exigir un rival fuerte. No aporta validación neuronal niHUpor su nombre.

## 9. Registro AB, límites y compromiso de salida

**belief_revision:** el regularizador MHUpierde prioridad como necesidad práctica general; organización local y decoder/modelo de señal son explicaciones preferentes de trabajo. No sabemos todavía si existe un beneficio residual útil bajo comunicaciones limitadas. Certificados, movilidad y fracasarXORno se usan como likelihoods de utilidad.

**hypothesis_generation:** B01–B32amplían alternativas. Las nuevas predicciones principales son riesgo/Gram, interacción con información/alcance y asignación de recursos por canal. La evidencia usada para formularlas no es su confirmación nueva.

**objective_revision:** la misión científica permanece; la cartera favorece adquirir/transportar información con mecanismos declarados. MHUya no selecciona por defecto objetivos, baselines ni presupuesto. El usuario delegó la decisión de prioridad, que se registra en elADR.

**decision:** diagnóstico Gram/nulidad primero; un contraste nuevo limitado después si tiene poder de discriminar; MHU neuronal,3D, multicapa y búsqueda prolongada de controles quedan aparcados. Si el rival local o informativo ofrece utilidad/coste comparable, seguiría ese rival y archivaría MHUen ese régimen. Se conservarán resultados adversos y toda evidencia antigua.

**Nivel de novedad:** el lote es trabajo de síntesis, diseño y autocorrección. Los marcos generales tienen priorart sólido. Una aportación original requerirá una predicción/mecanismo multicanal que sobreviva baselines, régimen desplazado y confirmación nueva. No presento un conjunto largo deideas como descubrimientos ni prometo una arquitectura mejor.

**Entrega de este turno:**32 fichas, decisión, estrategia ybibliografía/registro legible por máquina. Cero experimentos, generaciones, corridas científicas o entrenamientos nuevos. Las pruebas propuestas permanecen NOT_RUN y no se inician procesos persistentes.
