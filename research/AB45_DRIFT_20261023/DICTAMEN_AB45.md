# AB45 DRIFT — dictamen adversarial (2026-10-23)

**45 contrastes E01–E45 ejecutados**, 9 bucles DR01–DR09; ocho particiones por contraste sobre cuatro datasets públicos de scikit-learn con shifts artificiales. 34 signos favorables y 27 intervalos t descriptivos que excluyen cero, sin ajuste por multiplicidad: **NO** equivalen a descubrimientos. Novedad interna 2/3: NO ACREDITADA.

**DR01 (E01–05):** proyección del shift sobre coeficientes y cambios de output superan indicadores globales en algunas tareas; MMD e incertidumbre ganan otras. No existe detector ganador.

**DR02 (E06–10):** alterar solo las etiquetas aumenta el error real aproximadamente 0.136–0.287 sin alterar ninguna puntuación de los detectores cuando se mantiene el mismo muestreo. Es un límite de identificabilidad conocido. La diferencia numérica riesgo menos score NO compara unidades equivalentes.

**DR03–DR06 (E11–30):** adquirir prioritariamente los casos más inciertos puede estimar peor el error poblacional que random/estratificado, incluso con 32 etiquetas. Ejemplo E28 Digits: delta MSE random−uncertain = −0.20180. No es universal: E30 Iris favorece incertidumbre levemente.

**DR07–DR09 (E31–45):** repetir en otras particiones y shifts devuelve mezclas de triunfos y derrotas. Ejemplos E35 global−output = −0.32745 en correlación; E38 random−uncertain = −0.25530 MSE; E45 global−output = −0.10461 AUC. El modelo fija procedimientos simples, sin tuning competitivo exhaustivo ni algoritmos WATCH/CTM reales.

**Auditoría:** 45 JSON por semilla, 9 specs locales, motor fuente SHA256 f00acd99470bc7d17554bcc778f7cbc1fbacc8626e4eac1c4c8caa7b6b809df8, cuatro fragmentos GitHub verificados. Corrección auditoría MMD: score absoluto bajo nulo puede ser positivo por submuestreo (ej. 0.1146) aunque su DIFERENCIA entre condición nula y label-only sea cero. El fallo y la reparación están en ERRATA_AUDITORIA.md del ZIP.

**Gobernanza:** B01 precommitted GitHub 06aaa28. B02–B09 solo local freeze antes de sus ejecuciones; intentos GitHub bloqueados, NO conformidad plena con O3. JSON y ledger A–J íntegros están en ZIP de conversación, SHA256 0a5b0f8581bc64e5f29734bddf742e554bae85372dc19260b184d7c9c6fc7cd6. Archivo GitHub retrospectivo, no pretender prorregistro remoto posterior. CLEAN_CLONE_NOT_VERIFIED.

**AB-DECIDE:** cerrar cupo y pivotar a evaluación prospectiva de monitorización de riesgo con etiquetas escasas, distinguiendo objetivos de detección, estimación y aprendizaje. WATCH (Prinster et al. ICML 2025) y Conditional CTM (Shaer et al. ICML 2026) son antecedentes, no descubrimos esos principios. Confirmación externa G: AUSENTE.