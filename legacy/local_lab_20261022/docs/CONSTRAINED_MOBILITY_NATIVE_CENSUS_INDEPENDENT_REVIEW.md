# Revisión independiente del censo nativo

Esta revisión es posterior al diagnóstico de movilidad. No constituye una
confirmación empírica nueva ni genera controles completos, propuestas,
etiquetas candidatas, cadenas o puntuaciones de tareas.

Sea N_c el conjunto de sitios nativos del tipo c, m_c su distancia mínima
homotípica y a_c=L/sqrt(n_c). La familia del mínimo contiene cinco de las
130 desigualdades: `max(0,m_c−m_candidato)/a_c≤.05` para cada tipo.
G_c(x,y) identifica los pares que incumplen esa desigualdad; su diagonal es
falsa. Para un origen i de tipo c y destino j de otro tipo, el movimiento
retira i de N_c e incorpora j. Los pares que permanecen son nativos y ya
cumplen la guarda. Por tanto, la guarda del tipo c pasa exactamente cuando
j no tiene vecinos prohibidos en `N_c \ {i}`. Eso equivale a
`sum(G_c[j,N_c])−G_c[j,i]==0`, que define D_ij.

Con dos/tres tipos distintos, cada tipo pierde un sitio y gana otro. Así,
un swap pasa toda esta familia si y sólo si D_ij y D_ji. Un ciclo orientado
i→j→k→i pasa si y sólo si D_ij, D_jk y D_ki. D sólo tiene arcos entre tipos
distintos y no contiene bucles. Cada ciclo orientado de tres sitios tiene
tres representaciones por rotación, de donde `tr(D³)/3`; las orientaciones
opuestas son movimientos diferentes. Cada swap tiene dos representaciones,
de donde `sum(D·Dᵀ)/2`.

El auditor construye D y comprueba además todos sus pares mediante exclusión
directa del origen. Sus conteos usan enteros Python y bitsets:
`sum_i sum_{j in Dout_i} bit_count(Dout_j & Din_i)/3`. El ejecutor principal
usa productos matriciales enteros. Sus hashes del grafo y sus conteos por
bloques coinciden en las tres referencias. La distancia usa el helper
histórico compartido; la independencia adicional está en la construcción
escalar, el conteo y la suma de masas, no en otra implementación geométrica.

Para la probabilidad del kernel se suman sólo los movimientos válidos.
Cada swap de tipos a,b tiene masa global `1/(10*n_a*n_b)` y aporta por ancla
u la masa near `1/(80*n_tipo(u))` cuando el otro sitio pertenece a sus cuatro
vecinos elegibles. Cada ciclo orientado de tipos a,b,c tiene masa global
`1/(20*n_a*n_b*n_c)` y aporta por ancla u `1/(960*n_tipo(u))` cuando ambos
otros sitios pertenecen a sus respectivos cuatro vecinos. Estos factores
incluyen el orden de tipos y las dos orientaciones. El auditor suma esas
masas como fracciones racionales, usando mezcla4/5 near +1/5 global.

Los resultados son 24/53/34 swaps y 13/10/2 ciclos orientados para
g1101/g1102/g1103. Sus masas coinciden con la enumeración del ejecutor.
Son masas condicionales de superar sólo esta familia en la nativa, no
likelihoods de hipótesis ni evidencia neuronal. Los ciclos positivos
descartan una ausencia total para esta familia; no certifican las otras
125 desigualdades, controles espectrales ni conectividad global. El grafo
nativo tampoco describe los estados alcanzados después de swaps.

Herramienta: `artifacts/constrained_mobility/independent_census_audit.py`.
Resultado: `artifacts/constrained_mobility/independent_native_exclusion_census_v1.json`.
