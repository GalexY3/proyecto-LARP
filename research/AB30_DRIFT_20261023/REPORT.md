# LARP — Drift AB30 (23-10-2026): dictamen final

**Resultado:** 30 contrastes T01–T30 ejecutados en cinco bloques adaptativos; 12/30 diferencias con signo local favorable y 11/30 IC t descriptivos que excluyen cero, SIN corrección por multiplicidad ni replicación externa. **2/3 NO ACREDITADO.** La originalidad del proceso AB tampoco ha sido validada.

**Cambio de línea:** se abandona MHU como hipótesis privilegiada. Se investigó el valor de información condicionada a una decisión cuando cambian covarianzas, selección robusta de sensores y selección supervisada de características.

**B01 T01–T06:** selector nominal que conoce covarianza supera azar (T05 delta -0.20210, IC [-0.32637,-0.07783]), pero minimax/CVaR no ganan establemente. Prereg commit 4aa480c, resultados 3594945. **PIVOT** a riesgo de cola.

**B02 T07–T12:** CVaR tampoco domina a nominal; T09 empate exacto, T12 ignorar la correlación firmada es perjudicial (delta diagonal-nominal +0.07949, IC [0.00957,0.14941]). Prereg 397d60d, resultados d2b8edd. **PIVOT** a stress.

**B03 T13–T18:** bajo correlación alta T13 nominal supera diagonal (delta -0.03676, IC [-0.05898,-0.01454]), pero shrink y CVaR no producen ventaja consistente. Prereg d6e8064, resultados ed026b1. **PIVOT** a datos reales.

**B04 T19–T24:** sklearn Diabetes, 16 particiones sobre un dataset, Ridge regularizado. Filtro por correlación supera azar T22 (delta -1100.31 MSE, IC [-1399.72,-800.91]); wrapper greedy no domina filtro ni Ridge completo. B04 inicial INVALID por schema dataset ausente, sin entrenar; freeze reparado b9fa7d5 previo a rerun. Resultados 083be4d. **PIVOT** a clasificación.

**B05 T25–T30:** Breast Cancer Wisconsin, mismo dataset reutilizado 16 splits, LogisticRegression. Wrapper de 3 características supera filtro de 3 en T26 (delta error de BA -0.01434, IC [-0.02499,-0.00369]) pero pierde con 5 características frente al clasificador completo de 30 características T29 (delta +0.01990, IC [0.00767,0.03213]). Prereg a62ba7f, resultados eeb991c. **CLOSE cuota**.

**Auditoría prospectiva extra AUD01, no contada:** 50 mundos con cambios PSD de covarianza de igual norma Frobenius. Cambio de riesgo máximo en el núcleo del decoder 5.55e-17, incremento promedio en dirección útil 0.09658. Prereg 11b8c53. Esto verifica la identidad matemática conocida R(K,Σ+Δ)−R(K,Σ)=tr(KΔKᵀ), **no una nueva ley 2/3**. La dirección plausible es monitorización de drift condicionada al riesgo, aún sin evidencia externa.

**Inferencia y validez:** el objetivo de predicción, no una noción puramente geométrica de dispersión/diversidad, determina qué ruido perjudica. No concluir superioridad de métodos robustos ni de AB. El optimizador sintético enumera exhaustivamente los 84 subconjuntos 3-de-9; el mejor en test es oráculo retrospectivo no disponible para uso real. Los métodos robustos ven escenarios derivados del mismo generador que el test. Las bases reales son públicas y múltiples splits comparten muestras: no prueba externa ciega. Información y coste de selección de modelo completo y subset no se emparejan. El diseño contiene cinco commits de decisión entre bloques, no treinta replanificaciones completamente independientes.

**Fuente y archivo:** motor SHA256 congelado antes de B01 mediante commit 0be4f7c y contenido recuperable de cinco partes src/engine.py.gz.b64.part1 a part5, concatenar, añadir relleno base64 doble, decodificar y descomprimir gzip, confirmar SHA256 867e75309dfa81c8568bb2360d4cb4909560a338d7f16a587d03bba877f1deb6. Código bytes subido DESPUÉS, no simular anterioridad. [Resumen CSV 30 resultados](results/AB30_SUMMARY.csv); [seis priors](PRIORS_APPEND.md). El ledger individual A–J y los resultados exactos por seed están en ZIP de conversación, NO completos en este GitHub: SHA256 ZIP b24a2adc36588589cc9dd783785907ff2e4f9cc53c51d4638a671282917059ab. CLEAN_CLONE_NOT_VERIFIED. PR en borrador.

**Bibliografía y prior art:** Kim 2024 (correlated noise sensor selection), Uciński 2020 (D-opt correlated sensor selection), Krause et al. 2008 (robust submodular observation selection), Goldfarb/Iyengar 2003 (robust portfolio optimization); ver fuentes en expediente descargable. Ninguna novedad de 2/3 establecida.

**AB-DECIDE:** CLOSE 30; PIVOT hacia detección de drift relevante para decisiones con etiquetas tardías, solo como HIPÓTESIS prospectiva contra detectores OOD competentes y datos externos.
