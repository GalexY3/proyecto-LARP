# HU/MHU: antenas, muestreo, mecánica y límites

Fuentes primarias consultadas el 17 de octubre de 2026. No se modificó LARP ni se ejecutaron experimentos. Fichas de menos de 100 palabras por trabajo, excluyendo la referencia bibliográfica.

## Distinciones

HU de fracción de volumen en materiales polidispersos no equivale a HU de conteos de centros ni a MHU por especie. Blue noise multiclase tampoco certifica automáticamente el límite HU. Un DPP no es HU por definición: depende del kernel y del régimen. Un dispositivo MHU funcional no identifica causalmente cuánto aporta su supresión espectral frente a su separación, topología, componentes o lectura.

## 1. MHU: antena de siete clases fabricada y medida

Christogeorgos, O.; Okon, E.; Hao, Y. (2024). *An Ultrawideband (35:1) Shared-Aperture Antenna Array With Multihyperuniform Disorder*. IEEE Transactions on Antennas and Propagation 72(7), 5794–5809. Revisado por pares, julio de 2024. [DOI](https://doi.org/10.1109/TAP.2024.3406040). [Texto primario de los autores/final](https://www.researchgate.net/publication/381171643_An_Ultrawideband_351_Shared-Aperture_Antenna_Array_With_Multihyperuniform_Disorder).

Simulación, fabricación y medidas: 80 hélices, siete subarrays intercalados, 0,4–14 GHz. El espectro espacial controla lóbulos de rejilla mientras cada especie cubre una banda sin solapamiento físico. Comparan subarrays HU aislados, conjunto MHU y literatura; falta una ablación geométrica causal. El conjunto pierde prestaciones frente a aislados: PSLL máximo −5,8 dB, 2,8 dB peor; ganancia máxima 24 dBi, 1,5 dB menor. No pudieron simular completamente el conjunto con recursos disponibles, aunque sí lo midieron. Es aplicación real de MHU y también evidencia de que no elimina el acoplamiento entre especies.

## 2. HU: array Vivaldi frente a periódico

Christogeorgos, O.; Zhang, H.; Cheng, Q.; Hao, Y. (2021). *Extraordinary Directive Emission and Scanning from an Array of Radiation Sources with Hyperuniform Disorder*. Physical Review Applied 15, 014062. Revisado por pares; 29 de enero de 2021. [DOI/texto editorial](https://journals.aps.org/prapplied/abstract/10.1103/PhysRevApplied.15.014062).

Teoría, simulaciones y prototipo de 16 antenas Vivaldi; comparación con 16 elementos periódicos. Estudia 3/6 GHz y steering. PSLL simulado a 3 GHz: −13,85 dB frente a −2,4 dB periódico. Mecanismo: la disposición aperiódica suprime réplicas de difracción y genera una zona de baja emisión alrededor del haz principal. Es HU monoclase, no MHU. Ganar al periódico no establece superioridad frente a todas las disposiciones aperiódicas optimizadas con el mismo presupuesto.

## 3. MHU: generador físicamente restringido y parches/metasuperficies

Christogeorgos, O.; Okon, E.; Hao, Y. (2024). *A computational model for generating multihyperuniform distributions for realistic antenna array and metasurface designs*. EPJ Applied Metamaterials 11, 5. Revisado por pares; 8 de marzo de 2024, aceptado 4 de enero. [DOI](https://doi.org/10.1051/epjam/2024003), [PDF editorial](https://epjam.edp-open.org/articles/epjam/pdf/2024/01/epjam230018.pdf).

Construcción y simulación electromagnética, no confundir con el prototipo IEEE anterior. Genera especies secuencialmente con objetivos colectivos y restricciones de no solapamiento. Cinco clases de parches resuenan a 4/5/6/7/8 GHz; compara mediante CST conjunto MHU con subarrays aislados. Incluye metasuperficie con varios tipos de metaátomos. Prior art directo para un generador MHU con tamaños reales. La secuencia de colocación y el acoplamiento entre elementos siguen siendo decisiones importantes; no son beneficios gratuitos de la propiedad HU.

## 4. Prior art cercano: blue noise multiclase para gráficos/sensores

Wei, L.-Y. (2010). *Multi-Class Blue Noise Sampling*. ACM Transactions on Graphics 29(4), artículo 79; SIGGRAPH 2010. Revisado por pares. [Materiales del autor](https://www.liyiwei.org/papers/noise-sig10/), DOI 10.1145/1778765.1778816 [verificado institucionalmente](https://hub.hku.hk/handle/10722/141787).

Algoritmo y demostraciones computacionales en colocación de objetos, distribución de sensores y punteado de color. Busca propiedades blue noise por clase y en uniones. Disco duro controla separación; disco blando controla conteos; admite adaptación de densidades. Es comparación obligada para patrones aviares multiclase en gráficos y precede la retina de 2014. No renombrarlo como demostración matemática de MHU: espectro blue noise, restricción local y HU asintótica son afirmaciones distintas.

## 5. Cuadratura con garantías: DPP, literatura adyacente

Bardenet, R.; Hardy, A. (2020). *Monte Carlo with determinantal point processes*. The Annals of Applied Probability 30(1), 368–417. Revisado por pares; febrero de 2020, preprint inicial 2016. [DOI](https://doi.org/10.1214/19-AAP1504), [manuscrito](https://arxiv.org/abs/1605.00361), [código](https://github.com/rbardenet/dppmc).

Teoría y simulación. DPPs específicos de polinomios ortogonales multivariados permiten RMSE de orden N^{−(1+1/d)/2}, bajo regularidades de medida e integrando, frente a N^{−1/2} de MC crudo. La generación cuesta y la ventaja de tasa mengua con dimensión. No es garantía universal, ni todo DPP es HU, ni una validación de MHU por clases. Una propuesta MHU-cuadratura debe contar generación de muestras además de evaluaciones y competir con cuadratura adaptada a la familia de funciones.

## 6. Contraejemplo actual: mejor integración sin evidencia HU

Hawat, D.; Mastrilli, G.; Bardenet, R.; Lachièze-Rey, R. (2026). *Repelled Point Processes With Application to Numerical Integration*. Scandinavian Journal of Statistics 53(3), 1101–1133. Revisado por pares; online 20 de mayo de 2026, número septiembre. [DOI/texto editorial](https://onlinelibrary.wiley.com/doi/10.1111/sjos.70073).

Teoría y experimentos numéricos. Un paso de repulsión coulombiana sobre Poisson reduce varianza conservando insesgadez bajo hipótesis: d≥3, función C² de soporte compacto, paso pequeño. Coste O(N²), paralelizable. Explora además Ginibre y Sobol aleatorizado. Los autores no hallan evidencia numérica de HU del Poisson repelido, pese a mejorar integración. Por tanto, mejorar varianza no prueba HU ni la requiere universalmente. Repulsión local, estratificación y Sobol son controles necesarios antes de atribuir ganancias a MHU.

## 7. Mecánica: mayor resistencia a fractura, menor rigidez

Xu, Y.; Chen, S.; Chen, P.-E.; Xu, W.; Jiao, Y. (2017). *Microstructure and mechanical properties of hyperuniform heterogeneous materials*. Physical Review E 96, 043301. Revisado por pares; 2 de octubre de 2017. [DOI editorial](https://doi.org/10.1103/PhysRevE.96.043301), [manuscrito aceptado](https://link.aps.org/accepted/10.1103/PhysRevE.96.043301).

Reconstrucción estocástica y simulación de elasticidad/fractura. Los comparadores no-HU igualan S₂(r) de corto alcance hasta un corte γ, control especialmente relevante causalmente. En los modelos estudiados, HU produce materiales generalmente más resistentes a fractura, pero más blandos. Mecanismo propuesto: menos concentraciones de tensión. Es HU de fracción de volumen bifásica, no MHU de conteos. El resultado ilustra mejoras y costes simultáneos, no superioridad mecánica universal.

## 8. Transporte: espectro y conectividad de materiales bifásicos

Chen, D.; Torquato, S. (2018). *Designing disordered hyperuniform two-phase materials with novel physical properties*. Acta Materialia 142, 152–161. Revisado por pares; número enero de 2018, online 2017. [DOI](https://doi.org/10.1016/j.actamat.2017.09.053), [manuscrito](https://arxiv.org/abs/1709.09997).

Construcción Fourier, teoría y cálculos de propiedades efectivas. Diseña densidad espectral, fracción y conectividad. Algunas familias tienen conductividad eléctrica/térmica cercana a fórmulas o límites óptimos bajo condiciones específicas. La posibilidad de impresión 3D/litografía es una proyección, no una fabricación demostrada en este artículo. HU de fracción de volumen no certifica MHU de cinco especies. La lección transferible es diseñar espectro junto a topología para una función física definida; no atribuir a la etiqueta HU todas las propiedades.

## Inferencias propias: posibles alternativas abordables con PC

Son hipótesis motivadas, no evidencia ni autorización para ejecutar corridas.

1. **Arrays multibanda simplificados o micrófonos:** la suma de fases relaciona geometría, aliasing y lóbulos. El factor de array es manejable; Maxwell completo de antenas grandes puede requerir recursos superiores. El prior art implica buscar una aportación estrecha.
2. **Máscaras multicanal y punteado:** reutilizar el generador manteniendo calidad por canal/unión. Comparar con Wei y blue noise multiclase es indispensable.
3. **Cuadratura de campos multicanal con sensores escasos:** tiene sentido si cada canal presenta espectro/budget diferente; competir con Sobol, estratificación, DPP y repulsión. Sin prometer conservación total de información.
4. **Biblioteca de atribución espectro/topología:** separar vacíos, conectividad, separación y supresión espectral puede ser una contribución metodológica defendible.
5. **Material bifásico numérico 2D:** factible en principio, cambiando explícitamente de objeto científico a fracción de volumen y topología.

No aparece en este bloque evidencia que justifique inferir ventajas multilingües o conservación general de información.
