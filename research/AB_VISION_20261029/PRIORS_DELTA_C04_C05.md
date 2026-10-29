# C04–C05 | PRIORS_DELTA — LARP Visión, 2026-10-29
Apéndice acumulativo; no sobrescribir ni mejorar artificialmente priors previos. C04 fuente original congelada commit 4e4f4e1; test raw sha256 ec917d39129004f56066836a1637c7d263099bc28c6f8880082303ee03474456. C05 DOCUMENTAL/PLANNING solamente.

**P-VIS10 — Sensibilidad del endpoint LFW** [COMPUTACIONAL_EXPLORATORIO]: MHU_joint, grid, Poisson, Sobol, random y full_pixels caen cerca del techo de 96–97% en rostro/no rostro con 160 lecturas vs 625 píxeles. Falsador: escenas/etiquetas independientes y difíciles que permitan separar geometrías. Actualización: no nueva evidencia diferencial del mecanismo, CT2 baja.

**P-VIS11 — Proxy espectral frente a tarea aprendida** [COMPUTACIONAL_EXPLORATORIO, DUPLICATE_OVERLAP P-VIS02]: joint reduce potencia low-k, sin superar a grid/Poisson/subtipo en clean classification, joint y subtype exactitud 97.17%. Falsador: cinco modalidades ópticas reales y decoder competitivo en imágenes nuevas. No duplicar como N1.

**P-VIS12 — Paridad de información** [RIESGO_METODOLÓGICO]: 160 lecturas bilineales pueden combinar hasta 4 píxeles y no equivalen a 160 fotodiodos físicos; no inferir reducción energética 74.4% sin instrumentación.

**P-VIS13 — Rival de selección aprendida** [LÍMITE]: selección univariante ANOVA entrenada en folds obtuvo 93.5% y no es rival moderno fuerte (TokenLearner, selección aprendida de patches). No concluir que MHU supera aprendizaje adaptativo. Falsador: adversarios entrenados completos con igualdad de FLOPs/información.

**P-VIS14 — Nueva fuente real multisensor** [FUENTE_DOCUMENTAL]: dataset Bürgewald, 735×6 capturas geotiff MicaSense RedEdge-P, 17.8GB, licencia CC0 confirmada por repositorio GitHub. Datos NO descargados en este entorno; implicación: permite un gate de 5 canales físicos independientes, no demuestra eficacia de MHU. Fuente https://github.com/idt-fhac/odm_data_buergewald. Falsador: interband alignment/calibration incompleto o acceso técnico defectuoso.

**P-VIS15 — Registro y calibración como variable confusora** [DISEÑO_PRERREG]: banda por banda tiene óptica y posible paralaje; corregir registro y radiometría sin usar test outcomes antes de comparar patrones. Efecto sobre resultados NO evaluado todavía.

CT2 rama VISIÓN: 13→11 (solo por C04; C05 planificación no modifica). N1 nuevos 0, N2=N3=0, grado 2/3 NO ACREDITADO. 20 ciclos concedidos: C02+C04 ejecutados = 2, C03+C05 planning = 0, saldo 18. R5: stop repetición LFW y C01–C02; continuar solo con fuente de observación realmente nueva.
