# LARP/MHU — Campaña libre AB 3.2.1 de 30 ciclos (22-10-2026)

## Dictamen
**30/30 preguntas y decisiones auditables ejecutadas; 0 confirmaciones independientes; 0 descubrimientos 2/3 o 3/3 acreditados.** Los ciclos C01–C30 son preguntas diferentes sobre las *mismas cuatro realizaciones originales de geometría* (5201–5204), combinadas con 7 métodos y funciones sintéticas. No son 30 estudios independientes. Fuentes originales ya versionadas y reevaluadas; este bloque no genera nuevas muestras Scale3D adicionales.

**Hallazgo 1 (conocimiento explícito recuperado):** MHU reduce el espectro de Fourier en la banda optimizada de 40 modos: potencia media **1.2457e-09** versus LOCAL **9.7222e-07**, CVT **1.4891e-05** y RANDOM **0.00022511**. Pero una retícula trasladada (rango uno) consigue **5.574e-33** para la misma banda porque esos modos son no resonantes. Esto es teoría de cuadratura conocida, no arquitectura original. En la frecuencia resonante k=(-25,1,0), esa misma retícula presenta error de potencia **1** —un aliasing extremo—: no existe dominador universal por estos tests.

**Hallazgo 2 (trade-off multicapa):** Con k=16 vecinos y cuatro seeds, disponibilidad de los cinco tipos: MHU **95.06%**, LOCAL **95.69%**, CVT **97.62%** y retícula **74.50%**. MHU combina acceso local razonable con amortiguación espectral superior a LOCAL/CVT en la banda elegida, aunque no domina simultáneamente las métricas ni supera todas las alternativas conocidas.

**Hallazgo 3 (fuera de banda verdadera):** auditoría C11 encontró que la antigua banda high era **100% interna a k²≤78**, donde ya se optimiza la unión MHU. Recalculamos fuera de la banda, modos k²=101–134: MHU **2.1302e-05**, LOCAL **1.455e-05**, CVT **0.00028345**. Fuera del corte global, LOCAL supera a MHU: la ventaja de la penalización no se generaliza uniformemente.

**Hallazgo 4 (revisión conceptual):** si N_a/N→f_a estables y cada población tiene S_a(k)→0 al límite de baja frecuencia, entonces su unión también es HU: escribiendo A_a=(1/N_a)Σ_(i∈a)e^(ik·x_i), S_total=N|Σ f_a A_a|²≤(Σ√(f_a S_a))². Es la desigualdad triangular, NO un teorema nuevo. **La premisa 'combinar especies HU destruye la HU global y exige nuevo acoplamiento' es falsa sin hipótesis adicionales**. Lo que sí añade un acoplamiento de fases es menor S_total finito: al desplazar independiente y aleatoriamente los cinco tipos MHU, la potencia union creció de **1.246e-09** a **2.668e-08**, unas **21.4 veces**. No se puede decir que las fases desplazadas rompan la HU de cada tipo.

**Hallazgo 5 (condiciones de utilidad):** en funciones periódicas Fourier desconocidas e independientes por especialidad, error de integración del promedio multicanal: MHU **3.2521e-08**, LOCAL **7.2479e-06**, CVT **7.7673e-06**, retícula **9.365e-34** (1000 funciones aleatorias por geometría). Bajo un 50% de submuestreo en cada clase, los errores estimados de las opciones organizadas convergen: MHU **0.00032268**, CVT **0.00033227**. En funciones no periódicas, Sobol supera MHU para f(x)=x, con MSE Sobol **4.954e-08** vs MHU **1.068e-05**. El beneficio depende fuertemente de la clase de integrandos y presupuesto.

## Lo que no hemos demostrado
No se entrenaron nuevos modelos de lenguaje, Transformers, PointNet++ o GNN durante este bloque. No se ejecutó el código Multi-Class Blue Noise de Li-Yi Wei. No medimos hiperuniformidad asintótica ni rendimiento fuera de la muestra de datos espaciales sintéticos. Los comparadores Sobol, CVT y retícula no fueron emparejados por coste total de generación y optimización. En todo el bloque la unidad de independencia para comparar Scale3D original es **cuatro geometrías**. El script contenía una secuencia extensa de preguntas antes de evaluar los resultados; hubo reparación y pivot documentados C06, C11 y C22, pero no debe presentarse como 30 decisiones completamente replanificadas desde cero ni 30 falsaciones independientes.

## Riesgos, reparación realizada y calidad de los datos
- Se detectó y reparó un factor de 1/2 incorrecto en la derivación analítica de error con coeficientes real e imaginario gaussianos N(0,1): E[(Re(cz))²]=|z|² (no |z|²/2, que corresponde a fase uniforme). El código final y todos los resultados C26–C27 están recalculados; la primera ejecución errónea se conserva descriptivamente como errata técnica.
- La banda denominada high inicialmente era **in-band**; no se utiliza como validación OOD. La banda outside se eligió tras este descubrimiento, de manera exploratoria.
- Los modos reticulares resonantes fueron elegidos adversarialmente tras inspeccionar la regla; no medir su frecuencia por un único ejemplo ni comparar únicamente ese modo contra rivales.
- Las afirmaciones métricas se condicionan al modelo de entrada y al conjunto finito de funciones; no atribuimos ventajas a ontología neuronal o generalidad de inteligencia.

## Próxima investigación que podría justificar presupuesto adicional
**Solicitar 8 ciclos focalizados, no 30 automáticos**, condicionados a conseguir una implementación ejecutable del algoritmo original de Wei y a poder entrenar baselines neuronales con datos fuera del generador Fourier. Una línea plausible es aprovechar *interacciones entre funciones compartidas por diferentes tipos* para probar si el acoplamiento de fases que reduce S_union (sin alterar S_a) afecta a la transmisión de señales compartidas. Falsadores principales: control de cinco poblaciones independientemente desplazadas (mismas S_a), reglas QMC/Wei competentes y coste igualado. Sólo si ese mecanismo sobrevive, probarlo en modelo Scale3D entrenado con varias semillas y datos sensoriales externos.

## Referencias y prioridad
- Li-Yi Wei, *Multi-Class Blue Noise Sampling* (SIGGRAPH 2010): https://www.liyiwei.org/papers/noise-sig10/
- Morokoff & Caflisch, *Quasi-Random Sequences and Their Discrepancies* (SIAM, 1994): https://doi.org/10.1137/0915077
- Pilleboue et al., *Variance Analysis for Monte Carlo Integration* (2015): https://perso.liris.cnrs.fr/david.coeurjolly/publication/pilleboue-15-variance/
- Klatt, Lovrić et al., *Universal hidden order in amorphous cellular geometries* (2019): https://www.nature.com/articles/s41467-019-08360-5
- Investigación anterior y código original: https://github.com/GalexY3/proyecto-LARP (privado)
