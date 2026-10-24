# LARP AB30 O4 — Anexo acumulativo de priors (24-10-2026)

No sobrescribir ni reinterpretar los priors anteriores. **R1 corregida** y post-expuesta, no confirmatoria externa.

**O4-P01 [1/3, ALIAS-01]:** 21 mezclas nominalmente distintas colapsan en gran parte sobre pocas asignaciones enteras con 10–18 etiquetas, en seis poblaciones. Con presupuestos 26/34 persiste, pero disminuye. Anterioridad: distribución de restos/asignación entera y censos. Falsador: otros presupuestos y restricciones donde los tratamientos difieran.

**O4-P02 [1/3, PROXY-GAP-02]:** la minimización EXACTA de varianza bajo proxy empeora el resultado verdadero frente a una asignación Hamilton redondeada en cinco de seis fuentes; Wine es el contraejemplo. Implicación: minimizar con más precisión una medida auxiliar no mejora automáticamente el estimando principal. Anterioridad fuerte: Goodhart y error de medición. Falsador: proxies externamente calibrados de bajo error.

**O4-P03 [0/3 adicional]:** aleatorizar el redondeo dependiente mantiene la esperanza fraccional pero en seis fuentes E incrementa la varianza verdadera respecto a Hamilton; G cambia signo en varias fuentes. Conocido diseño aleatorizado, no una novedad.

**O4-P04 [candidato subordinado, no doble contar]:** la reserva 50/50 proporcional mejora worst-case en Diabetes/Breast/Nile y pierde en Wine/Digits/Sunspots ante volatilidad construida. Está subsumido conceptualmente en P02. La volatilidad no proviene del mundo observado.

**O4-P05 [0/3 adicional]:** minimizar peor varianza proxy bajo tres escenarios alternativos de aumento no reduce necesariamente la peor varianza real: el método robusto perdió frente a mezcla protegida en las seis fuentes E/G. Problema clásico de especificar conjunto de incertidumbre.

**O4-P06 [instrumentación, no hallazgo]:** el código v1 denominó incorrectamente Hamilton a una regla iterativa de restos. 30 resultados inválidos y un piloto de seis sin freeze se conservaron; source R1 reparada precommit antes de repetición; no demuestra validez confirmatoria externa ni suma 1/3.

**O4-P07 [confianza trayectoria]:** CT2 18→16→13→12→20→15/100. Juicio ordinal, no P(2/3). Baja por estado del arte fuerte y falta de dominio externo; puede subir solo con comparación adversarial independiente y reivindicación novedosa precisa.

**Balance campaña:** N1=2 únicos (ALIAS-01 y PROXY-GAP-02), N2=0, N3=0. N1 histórico de otras campañas NOT_AUDITED. No contar una idea una vez por dataset.
