# Ledger AB 3.2.1 — 30 ciclos de preguntas distintas (investigación libre)

**Fecha:** 22 de octubre de 2026. **Registro en JSON:** `data/AB_LEDGER_C01_C30.json`. Exploración adaptativa y controles agrupados sobre 4 geometrías originales (n=4), sin confirmar independencia por 30 ciclos. No se comparó con GPT ni Wei original. Algunas preguntas estaban previstas en un mismo script: el branching fue parcialmente adaptativo, no 30 decisiones preregistradas separadamente antes de sus datos.

### C01 · Procedencia y cuotas de las cuatro geometrías originales
**Hipótesis:** No leakage por reetiquetado o fallo de distribución. **Rival:** Etiquetas erróneas, fuga de observaciones, fuentes duplicadas. **Falsador:** Identidad de archivos repetidos o cuotas inválidas. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C01 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿La penalización MHU reduce amplitudes bajas por tipo?.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C02 · Varianza espectral baja de población total
**Hipótesis:** MHU suprime amplitud de modos bajos. **Rival:** CVT, Sobol, retícula, azar. **Falsador:** MHU no inferior a LOCAL. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C02 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿La supresión afecta a cada especie?.

*Alcance:* Exact Fourier sum, not claim asymptotic hyperuniformity.

### C03 · Especies individuales y la peor clase
**Hipótesis:** MHU suprime amplitud en las cinco especies. **Rival:** Supresión sólo en población global; tipo raro deteriorado. **Falsador:** MHU no mejora peor especie frente a LOCAL. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C03 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿La varianza de integración se deduce de estas amplitudes?.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C04 · Identidad exacta: error de un seno aleatorizado
**Hipótesis:** E_phi error cuadrático=S(k)/(2n). **Rival:** Efecto distinto a la optimización espectral. **Falsador:** Relación falla por fórmula o normalización. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C04 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿Cómo compite MHU con muestreadores QMC especializados?.

*Alcance:* La identidad es álgebra conocida, no novedad.

### C05 · Comparador Sobol por especie menos abundante
**Hipótesis:** MHU aventaja a Sobol aleatorizado en error medio Fourier. **Rival:** Sobol QMC gana sin hiperuniformidad construida. **Falsador:** Sobol iguala/supera la supresión MHU. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C05 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿Una retícula de rango uno domina ambas?.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C06 · Regla reticular trasladada como comparador fuerte
**Hipótesis:** MHU sigue competitiva en integrales periódicas suaves. **Rival:** Regla de retícula anula modos no resonantes exactamente. **Falsador:** Retícula mejora drásticamente modo de integración elegido. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C06 (observación completa). **Decisión:** PIVOT. **Siguiente pregunta:** ¿Hay trade-off de cobertura de tipos entre retícula y MHU?.

*Alcance:* Rank-1 lattice no equivale a Wei; baseline construido y declarado. Puede tener resonancias a frecuencias altas.

### C07 · Compromiso entre cobertura local y supresión espectral
**Hipótesis:** Retícula óptima Fourier también cubre tipos localmente. **Rival:** Cobertura y S(k) no cooptimizan. **Falsador:** Método domina en ambas sin coste. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C07 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿CVT ofrece un compromiso mejor que las dos?.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C08 · Frontera de Pareto para cobertura y cuadratura
**Hipótesis:** MHU exhibe intercambio defendible frente a CVT/Lattice. **Rival:** Dominancia completa por un método clásico. **Falsador:** MHU dominada en las dos métricas. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C08 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿Se mantiene fuera de modos optimizados?.

*Alcance:* Pareto de dos métricas y métodos finitos, no teorema de optimalidad.

### C09 · Generalización fuera de la banda Fourier baja
**Hipótesis:** Ventaja espectral MHU persiste a frecuencias medias. **Rival:** Sobreajuste al espectro de la pérdida. **Falsador:** La supresión se pierde o invierte. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C09 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿Cuál es el riesgo en frecuencias altas?.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C10 · Riesgo de amplitudes altas y aliasing
**Hipótesis:** Suprimir modos bajos no aumenta modos altos. **Rival:** Desplazamiento de energía espectral al exterior. **Falsador:** Potencia MHU supera claramente LOCAL/Sobol en banda alta. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C10 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿Existe orientación direccional privilegiada?.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C11 · Auditoría de fuga: frecuencia alta realmente fuera del objetivo
**Hipótesis:** La banda high verifica generalización espectral fuera de train. **Rival:** Corte union k²=78 y tipos menores, banda high parcialmente dentro. **Falsador:** Toda o parte de high estaba entrenada. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C11 (observación completa). **Decisión:** REPAIR. **Siguiente pregunta:** Redefinir una banda estrictamente exterior y repetir diagnóstico.

*Alcance:* Corrección obligatoria: las anteriores medidas medium/high NO eran un holdout seguro del objetivo espectral de unión.

### C12 · Extrapolación a modos fuera del corte spectral del conjunto
**Hipótesis:** MHU reduce amplitudes también fuera de modos optimizados. **Rival:** S(k) se desplaza a modos vecinos; CVT/QMC mejora. **Falsador:** MHU pierde la supresión fuera de banda. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C12 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Aislar si la especie escasa, cuya banda es menor, mantiene la ganancia.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C13 · Cambio de banda por especie escasa
**Hipótesis:** Especie rara retiene regularidad espectral aun superando su k²=13. **Rival:** Cae la protección fuera de su propia penalización. **Falsador:** Fuera del corte raro MHU se comporta como CVT. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C13 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Comprobar anisotropía direccional y coste de regularidad.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C14 · Isotropía del error espectral: ejes frente a diagonales
**Hipótesis:** MHU mantiene baja potencia en múltiples orientaciones. **Rival:** FFT/CIC introduce artefactos de ejes. **Falsador:** MHU favorece sustancialmente ejes. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C14 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Buscar fallo adversarial de la retícula, comparador dominante low.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C15 · Modo resonante adversarial para retículas exactas
**Hipótesis:** Retícula es óptima universalmente porque anula 40 modos bajos. **Rival:** Resonancias producen S(k) grande cuando k·g=0 mod n. **Falsador:** La retícula tiene error extremo en un modo permitido. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C15 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Comparar riesgo máximo, no solo media espectral.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C16 · Riesgo máximo de error por modo
**Hipótesis:** MHU controla tanto la media como el peor modo. **Rival:** Un modo mal protegido domina bajo estímulo adversarial. **Falsador:** MHU peor que CVT en peor modo de interés. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C16 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Auditar invariancia geométrica para descartar artefactos.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C17 · Invariancia de traslación del toro
**Hipótesis:** Potencia S(k) es invariante bajo traslación periódica común. **Rival:** Error de implementación FFT, redondeo o máscara. **Falsador:** El desplazamiento cambia S(k) fuera de tolerancia. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C17 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Examinar perturbación de coordenadas a pequeña escala.

*Alcance:* Control exacto, no hallazgo científico de originalidad.

### C18 · Estabilidad ante desplazamientos independientes de sensores
**Hipótesis:** MHU conserva supresión bajo ruido de coordenadas. **Rival:** Penalización hipersensible a posiciones exactas. **Falsador:** Jitter anula ganancia MHU. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C18 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Ensayar fallos de disponibilidad en vez de movimiento.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C19 · Pérdida aleatoria del 20 % de sensores raros
**Hipótesis:** MHU conserva ventaja espectral relativa tras dropout. **Rival:** El muestreo Bernoulli destruye el cero espectral con piso ≈p/((1-p)n). **Falsador:** El dropout borra la relación de orden original. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C19 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Probar agujero espacial, menos benigno que dropout.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C20 · Fallos espaciales correlacionados de tipo raro
**Hipótesis:** MHU conserva utilidad espectral cuando se vacía una región. **Rival:** Todos los diseños quedan dominados por el hueco y sesgo de cobertura. **Falsador:** Sin ventaja MHU frente a controles después del agujero. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C20 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Usar inversión causal de etiquetas para aislar origen del espectro.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C21 · Ablación causal: permutar marcas de tipo manteniendo todas las posiciones
**Hipótesis:** MHU precisa asignación geométrica coordinada de clases. **Rival:** Supresión por sola unión de puntos o etiqueta sin efecto. **Falsador:** Barajar tipos no altera espectro por clase. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C21 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Demostrar relación exacta entre espectro de subtipos y el de la unión.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C22 · Teorema elemental: la unión de clases HU también es HU bajo fracciones estables
**Hipótesis:** Es posible mantener S_i(k)→0 en todas las especies y S_total(k) distinto de cero. **Rival:** La desigualdad triangular obliga S_total(k)≤(Σ sqrt(f_i S_i(k)))². **Falsador:** La desigualdad algebraica falla o límites sin fracciones estables. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C22 (observación completa). **Decisión:** REPAIR. **Siguiente pregunta:** Estudiar papel real de correlaciones intertipo sin repetir la premisa falsa.

*Alcance:* No es una demostración novedosa. Bajo hipótesis regulares cada especie asintóticamente HU implica unión HU; la afirmación de que mezclarlas destruye necesariamente HU es falsa.

### C23 · Correlación cruzada: trasladar cada clase independientemente
**Hipótesis:** Correlación entre tipos reduce S_total más que composición por tipo. **Rival:** La fase relativa puede aumentar o disminuir union S sin alterar S_i. **Falsador:** Unión no cambia nunca tras traslaciones independientes. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C23 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Comprobar integración conjunta ponderada de funciones distintas por tipo.

*Alcance:* Contraste de correlaciones de fase a N finito; no implica que suma de HU deje de ser HU.

### C24 · Cuadratura multi-canal: una función Fourier desconocida distinta por tipo
**Hipótesis:** MHU reduce error de agregación de cinco especializaciones. **Rival:** Rank-one lattice puede integrar mejor señales periódicas compatibles. **Falsador:** MHU no mejora a retícula o Sobol. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C24 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿La ventaja está limitada por ruido de medida independiente?.

*Alcance:* Estímulos sintéticos periódicos y regla de promedio conocida; no modelo neuronal ni test externo.

### C25 · Límite por ruido independiente de sensor
**Hipótesis:** Geometría espectral también suprime ruido blanco de lectura. **Rival:** La varianza iid del promedio queda fijada por n y pesos. **Falsador:** Una geometría mejora el término blanco iid en igualdad de número de lecturas. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C25 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿Las clases raras dominan la pérdida aunque el conjunto esté muy regular?.

*Alcance:* Var[Σ w_t mean(noise_t)] = σ²Σ w_t²/n_t si lecturas iid sin correlación; es un piso independiente de posición.

### C26 · Funciones asimétricas y el cuello de botella de la especie rara
**Hipótesis:** El orden de algoritmos depende del peso de la clase minoritaria. **Rival:** El resultado es idéntico si todas las especies se comportan igual. **Falsador:** Todas las ponderaciones producen la misma jerarquía. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C26 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** ¿La ventaja spectral resiste reducción global a mitad de sensores?.

*Alcance:* Exploratory, n=4 original geometries; tasks synthetic and adaptively selected.

### C27 · Presupuesto de 50 % de sensores por especialidad
**Hipótesis:** MHU mantiene ventaja relevante al reducir coste de muestreo. **Rival:** El submuestreo destruye orden y favorece diseños ya baratos. **Falsador:** La ventaja desaparece a media densidad. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C27 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Buscar funciones no periódicas donde un diseño QMC tenga ventaja.

*Alcance:* Pérdida real por reconstrucción del patrón tras reducir n, no escalamiento optimizador a n/2 ni coste total de generación.

### C28 · Transferencia a integración no periódica y función localizada
**Hipótesis:** MHU mantiene ventaja en funciones suaves sin estructura Fourier toroidal. **Rival:** Sobol/retículas o CVT más apropiados para frontera real. **Falsador:** MHU deja de ser competitivo cuando cambia espacio funcional. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C28 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Valorar si existe una ventaja de Pareto real y si es original.

*Alcance:* x,xy y bump gaussiana tienen integrales analíticas en [0,1]^3; los resultados describen estos tres integrandos, no una población universal.

### C29 · Frontera multivariable y prueba de originalidad frente a muestreo conocido
**Hipótesis:** MHU aporta beneficio no reproducible por multi-class blue noise, QMC, retículas. **Rival:** Pareto en estos indicadores no acredita novedad ni utilidad neuronal. **Falsador:** Alguna comparación fuerte elimina o explica la ventaja específica. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C29 (observación completa). **Decisión:** CONTINUE. **Siguiente pregunta:** Auditoría final de resultados e independencia: AB-DECIDE.

*Alcance:* La frontera depende de pesos y métricas elegidos tras exploración; comparación con Wei original NO ejecutada.

### C30 · Auditoría de cierre y decisión sobre extensión
**Hipótesis:** Existe novedad arquitectónica 2/3 o 3/3 después de 30 ciclos. **Rival:** Propiedad geométrica conocida, sin generalización externa ni ventaja sobre baselines mejores. **Falsador:** Hallazgos positivos exclusivos se sostienen bajo todos los controles fuertes. **Evidencia:** `data/AB_LEDGER_C01_C30.json`, entrada C30 (observación completa). **Decisión:** STOP_NOVELTY_CLAIM. **Siguiente pregunta:** Solicitar 8 ciclos focalizados, condicionados a experimento comparador Wei original y datos/sistemas neuronales fuera de Fourier.

*Alcance:* Treinta decisiones científicas correlacionadas, NO treinta ensayos independientes; ningún 2/3 o 3/3 acreditado. Recomendar máximo 8 nuevos ciclos solo si se obtienen controles externos y recursos suficientes.
