# Propuesta metodológica AB-M030 — objetivo del estimador y comparador competente

**22-10-2026 · Estado:** PROPUESTA; no modificación normativa de AB 3.2.1/O1/O2. Procedencia: LARP VALUE30, `audit.json` y `DICTAMEN_AB30_VALUE.md`.

**Problema confirmado en el instrumento de comparación:** el selector inicial etiquetado GP escogía posiciones para maximizar reducción de varianza CONDICIONAL del estimando bajo un predictor aprendido, mientras la clasificación primaria le asignaba la media aritmética de lecturas con pesos fijos. En consecuencia, una cifra GP desfavorable NO identifica un fracaso de la colocación gaussiana en su tarea. También se le restringía a 72 candidatos por canal frente al espacio 576 de los rivales directos.

**Mejora candidata:** GATE `READOUT_OBJECTIVE_ALIGNMENT`: para comparar algoritmos de diseño de sensores, declarar de antemano qué predicción puede hacer cada uno (media fija, mínimo MSE lineal, posterior GP, estimador calibrado), y qué método de selección optimiza su pérdida. Igualar presupuesto de lecturas, acceso a datos, candidatos, preparación y recursos; evaluar con un readout común si el estimando es causalmente solo la geometría, y con el mejor readout propio si la pregunta es utilidad del pipeline. Si el control no comparte el mismo estimador, clasificar la comparación como **pipeline heterogénea**, nunca como superioridad geométrica específica.

**Coste y limitación:** entrenar y verificar estimadores adicionales tiene un coste real. Esta propuesta ya está parcialmente contenida en AB-M021/M024 y O2: registrar como operacionalización y reparación concreta, NO una nueva teoría metodológica ni eficacia general validada.

**Falsador:** si en varios problemas los distintos readouts son equivalentes bajo pruebas formales y empíricas, las comparaciones heterogéneas pueden ser pertinentes, pero esa equivalencia ha de mostrarse, no asumirse.
