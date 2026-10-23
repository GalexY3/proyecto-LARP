# LARP — AB30N: campaña experimental dirigida a originalidad 2/3 (22-10-2026)

**Estado:** 30 contrastes D01–D30 ejecutados, cinco etapas adaptativas de seis preregistradas en GitHub ANTES de correr cada bloque, y seis auditorías V01–V06 con nuevas seeds, fuera de cuota. **2/3 NO ACREDITADO.** Ninguna prueba valida hiperuniformidad asintótica ni una nueva ley. Distinguir contrastes con A–J registrados de confirmaciones científicas independientes.

## Pregunta contrastada

¿Aporta la optimización espectral CONJUNTA de cinco clases una ganancia computacional específica y robusta frente a optimizar las CINCO CLASES INDIVIDUALMENTE, y frente a controles convencionales competentes?

Se construyeron 60 sensores (12 por tipo) en un toro cuadrado 2D. «joint» penaliza el espectro intratipo y de unión, «sub» solo intratipo, «union» solo agregado, «repel» repulsión local; controles Sobol, retícula trasladada por tipo e IID. Se usó L-BFGS-B con máximo 65 iteraciones y misma inicialización para optimizadores comparados. No se certificó HU asintótica; son diseños de banda finita, no MHU biológico. «repel» NO es la implementación auténtica de Wei 2010 y las comparaciones no igualan completamente el coste de diseño.

## Ciclos por rama y decisiones

- **B01 D01–D06, mecanismo estructural:** joint=2,69e-10 vs sub=6,98e-10 en potencia de unión low (D01; IC del delta cruza cero), pero joint es levemente peor que sub para potencia intratipo (D02; IC cruza cero). La optimización de subtipos ya casi anula el espectro agregado. La retícula alcanza potencia ~2,31e-32 en los modos de diseño (D05). **PIVOT hacia covarianzas**, no llamar novedosa la potencia finita.
- **B02 D07–D12, cuadratura por correlaciones:** frente sub para shared, joint 1,25e-10 vs 3,93e-10 (D07) a escalas casi nulas; para canales independientes y anticorrelados D08/D09 las diferencias no son concluyentes. El control union-only es claramente peor en canales independientes D10. La retícula vuelve a anular errores sobre armónicos in-band D12. **PIVOT a OOD**.
- **B03 D13–D18, banda exterior y no periodicidad:** fuera de banda joint 0,08471 y sub 0,08376 en energía intratipo (D13). Joint no domina funciones no periódicas frente a Sobol (lineal y escalón); la radial D17 constituye una excepción exploratoria. Un triunfo aparente frente a retícula fuera de banda en D14/D15 no tiene IC excluyente de cero. **PIVOT a perturbaciones**.
- **B04 D19–D24, dropout y jitter:** fallos 20–50% o desplazamientos de posiciones 0,01–0,04 no producen mejora sostenida de joint frente a sub. Todos los IC descriptivos de esta rama abarcan cero. **PIVOT a downstream**.
- **B05 D25–D30, reconstrucción local y Digits:** D27 joint 0,750 vs retícula 1,084 MSE de reconstrucción de frecuencia 3 (aliasing de retícula, un fenómeno clásico); D28 joint 0,1075 vs Sobol 0,1313 MSE con ruido (selección exploratoria). D29 en Digits original 91,75% joint vs 91,89% sub; D30 rotación 69,24% vs 69,61%. Ninguna nueva ventaja de aprendizaje robusta específicamente atribuible al acoplamiento.

**Contabilidad:** 14/30 diferencias con signo favorable a su hipótesis local (sin valor confirmatorio); 11/30 IC t descriptivos excluyen cero, sin corregir multiplicidad. El signo no equivale a descubrimiento. Todas las métricas y todos los resultados, negativos incluidos, están en results/RESULTS_30_ROUNDED.csv y el registro individual A–J está en reports/LEDGER_D01_D30.md.

## Auditoría adversarial adicional V01–V06, después de D28, NO contada

Cada contraste usa 30 semillas geométricas nuevas del MISMO generador. V01 joint − Sobol ΔMSE=-0,02495, IC descriptivo [-0,03246,-0,01745]. V02 joint − sub Δ=-0,000154, IC [-0,000392,+0,000083]. V03 joint − retícula Δ=+0,002486, IC [-0,005332,+0,010304]. V04 joint − repel Δ=-0,006701, IC [-0,013583,+0,000180]. V05 y V06 contra sub a frecuencia alta o pérdida tampoco separan las variantes. Conclusión: **el rendimiento en reconstrucción no aísla el término de unión ni una singularidad MHU**.

## Auditoría y linaje AB

**Anclaje de código ANTES de ejecutar:** commit `e782483`, SHA256 del script fuente `df7e95fa9bb96c8d65b9634b5188dc9ea587d364f6257dcaa8ba8d7d6a42e443`. Los bytes comprimidos del código quedaron incorporados en GitHub más tarde por commit `0c72aaf`, con mismo SHA. Este procedimiento constituye un compromiso criptográfico previo, **no** un archivo de fuente legible ya alojado al momento de ejecutar.

Congelaciones de bloques antes de ejecución: B01 `79be1a2`, B02 `0247871`, B03 `2f042e1`, B04 `0335b86`, B05 `f50e603`, AUDIT01 `5ffe0db`. Se comprobó identidad de SHA-1 de blob entre los cinco JSON locales y los cinco JSON prerregistrados en GitHub. Las 30 verificaciones de spec hash, cuotas por tipo, cota espectral, diferencias finitas del gradiente (error máximo 3,25e-12), y forma cuadrática de covarianzas contra 15.000 realizaciones Monte Carlo (error relativo ~0,51%) pasan en la auditoría local.

**Limitaciones centrales:** Dataset Digits reutilizado de campañas adaptativas, diseño sintético periódico, n=4 semillas para clasificadores, varianzas próximas al piso numérico, múltiples outcomes exploratorios, no se ejecutó Wei auténtico, sin costos de optimización efectivamente equiparados, sin patrones MHU asintóticos certificados, SIN réplica externa, CLEAN_CLONE_NOT_VERIFIED. El raw por semilla está en el ZIP de conversación, no copiado íntegramente todavía en este branch. GitHub sí conserva CSV de agregados y seeds, prerregistros y código congelado por SHA.

## Priors y originalidad

Los ocho nuevos priors del apéndice reports/PRIORS_DELTA.md no borran los previos. La ecuación de error de cuadratura condicionado a covarianza (forma cuadrática) es matemática convencional; *multi-class blue noise sampling* ya trata la unión y clases para sensores. Ninguna identidad trivial, efecto inducido por función de pérdida ni alias de retícula puede promoverse a originalidad 2/3. La próxima hipótesis más prometedora es un criterio minimax espectral bajo **covarianza de canales desconocida** con baselines de diseño óptimo, pero es solo una propuesta que exige búsqueda de antecedentes e implementación externa.

**AB-DECIDE:** CLOSE_QUOTA; PIVOT a nueva fuente de evidencia, no adjudicar 2/3.

Referencias: Jiao et al., Phys Rev E 89 022721 (2014), https://doi.org/10.1103/PhysRevE.89.022721; Li-Yi Wei, SIGGRAPH 2010, https://www.liyiwei.org/papers/noise-sig10/ ; código Wei https://github.com/1iyiwei/noise/tree/master/RainbowNoise .
