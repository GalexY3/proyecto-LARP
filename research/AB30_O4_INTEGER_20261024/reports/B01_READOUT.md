# B01 E/G — alias de asignaciones enteras (Q01–Q06), 2026-10-24
**Prereg remoto previo:** a2ce3359. Fuente exacta SHA256 f800f562..., tres partes b64 precommitted. Seis poblaciones observadas, 3 estratos (20/30/50), 21 parámetros de mezcla λ y los presupuestos 10/14/18 (E) y 26/34 (G). Mismo dato para ambos, G es extrapolación a presupuestos, no replicación externa.
| Ciclo | Fuente | Fracción E de λ alias | Fracción G |
|---|---|---:|---:|
| Q01 | Diabetes | 0.809524 | 0.642857 |
| Q02 | Breast Cancer | 0.793651 | 0.595238 |
| Q03 | Wine | 0.888889 | 0.809524 |
| Q04 | Digits | 0.857143 | 0.785714 |
| Q05 | Nile | 0.841270 | 0.761905 |
| Q06 | Sunspots | 0.857143 | 0.761905 |
A: distinción entre parámetro nominal continuo y tratamiento entero; B: H1 alias>0.5 y H0<=0.5, todos E confirman condicionalmente; C λ∈21 valores y presupuesto pre-fijo; D suma presupuesto y n_h entre 1,N_h afirmados en código; E resultados exactos, sin p por enumeración; F alias ya conocido matemáticamente por discretización, posible dependencia de λ-grid; G presupuestos mayores bajan la fracción pero no la eliminan, misma fuente; H 1/3 portfolio único por advertencia operativa replicable, no seis descubrimientos; I validez interna alta, originalidad 0, fuerte antecedente Census Bureau 2014; J CONTINUE a controles de asignación entera exacta. 
CT2 de línea: **18→16/100** (prior art fuerte, un hallazgo útil interno, ninguna evidencia de ley novedosa). N1 campaña: **1** (AUDIT-ALIAS-01), N2=0, N3=0.
**Pretest excluido:** B01 sobre presupuestos [9,12,16,24,32] se ejecutó ANTES de congelar GitHub; archivo tmp conservado como PILOT_NOT_COUNTED, no hace parte de Q01–Q06.
