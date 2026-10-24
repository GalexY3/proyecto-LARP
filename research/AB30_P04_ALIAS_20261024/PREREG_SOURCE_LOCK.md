# AB30 — prerregistro prospectivo: equivalencia observacional de pruebas metamórficas

Fecha: 24-10-2026. Rama: research/ab30-p04-alias-drift-20261024. Derivado de AB55 BugsInPy P04 D3,7. Autoriza 30 ciclos A–J experimentales exploratorios (cinco bloques de seis programas); NO reproduce BugsInPy ni ejecuta bugs históricos. La investigación utiliza funciones de referencia propias y fallos inyectados artificialmente, sin afirmar descubrimiento ni replicación externa.

SOURCE_LOCK antes de ejecutar: `experiment.py` local SHA256 **3324c4978699454fec6f5d69fb5e5ba952e897bf7895f5819f5ef38549d0bf7b**, 12.602 bytes, py_compile comprobado. IMPORTANTE: los bytes del script están inicialmente solo en el sandbox, no remotos; el hash en este commit congela el compromiso pero NO satisface el requisito O3 de código completo remoto pre-run. Se preservará como desviación; nunca se reclamará freeze remoto íntegro.

## Estimando y puerta de información

Unidad de ciclo: uno de seis programas matemáticos implementados con Python (sum, min, max, mean, range, unique). Seis repeticiones por ciclo con seeds deterministas 74000+cycle*100+rep. Candidatos: 14 transformaciones de entradas, con relaciones analíticas verificables sobre la versión correcta y 16 entradas base por candidato. Tres familias disjuntas de ocho defectos inyectados: input, output, conditional; train y holdout disjuntos por familia; test de cambio de distribución de inputs nonnegative o mixed. Cada relación se evalúa con el mismo número de llamadas y bajo igualdad de cuota: seleccionar cuatro relaciones para un conjunto. Métricas: fracción de pares de relaciones indistinguibles en TRAIN que se separan en HOLDOUT; recall en HOLDOUT (por conjunto de 8 fallos) de greedy SET-COVER, deduplicación observacional+greedy, greedy con tie-break de diversidad y RANDOM. Todos los métodos disponen del mismo TRAIN; ninguno accede al HOLDOUT durante selección.

No equivale a evaluación de tiempo humano de concepción de tests ni al estándar profesional property-based testing. Optimizar ocho mutantes no demuestra detección de defectos naturales. No reportar intervalos como si 30 ciclos fueran 30 muestras independientes: los seis programas/familias se reutilizan.

## Branching / selección secuencial

B01 C01-C06 prueba train=input, test=conditional, domain=mixed. B02–B05 usan elección adaptativa al cerrar cada bloque, nunca datos de bloques futuros. Si mean alias-break>0.15: lista priorizada [1,4,2,3,5,6,7]; si no, [2,3,5,1,4,6,7]. Si Δ(DEDUP−GREEDY)<−0.10, se sustituye prioridad por [3,5,2,1,4,6,7]. Elegir primer brazo no usado.
REGIMES:
0=input→conditional,mixed;
1=output→input,mixed;
2=conditional→output,nonnegative;
3=input→output,nonnegative;
4=conditional→input,mixed;
5=output→conditional,nonnegative;
6=input→output,mixed;
7=conditional→input,nonnegative.
Orden dentro de bloque: sum,min,max,mean,range,unique. Hay 30 contrastes A–J, PERO solo cinco decisiones sustantivas de branching, y no 30 teorías nuevas.

## Evaluación y controles

A-J por ciclo registra estimando, H1/H0/Hother, comparadores, instrumento, resultados brutos 6 seeds, auditoría, carencia de réplica externa, priors, grado y decisión. Invariantes: versión correcta pasa cada MR, selección cuatro por método, seeds pareadas, y no intersección entre conjuntos de ocho fallos. Si falsos positivos de clean >0, resultados INVALID hasta reparación archivada. Guardar JSON raw, diccionario de los treinta ciclos, hashes, figura CT2 doble escala y resumen. Re-run local verifica identidad.

CT2 inicial propia de rama P04 = 12/100 (plan previo) tras pivot D3,7 desde línea BugsInPy principal CT2=8. Si se confirma el antecedente de TSR / mutant subsumption / MR composition, CT2 ajustable a 10 en checkpoint B01; no cambiar por volumen de semillas, resultados elegidos o deseo de una gráfica bonita. CT2 es ordinal y por línea, no probabilidad. N1 nuevos presumidos=0 hasta auditoría de novedad independiente; N2=N3=0. Priors originales históricos intactos.

## Antecedentes adversariales pre-experimento

Koitz-Hristov (2024) DOI 10.1002/smr.2656; greedy mutation-based test-suite minimization (2023) DOI 10.1109/ACCESS.2023.3289073; test reduction on real failed builds (2018) DOI 10.1145/3213846.3213875; MR composition IEEE TSE (2020/22) DOI 10.1109/TSE.2020.3009698; mutation scores vs real faults ICSE (2018) DOI 10.1145/3180155.3180183. Esta literatura ya trabaja la sustitución/reducción y los riesgos de transferencia, por lo que un resultado positivo en nuestra matriz no se atribuirá originalidad.

**AB-R5**: es legítimo cerrar antes si no hay información discriminante; el cupo de 30 no obliga a probar 30 teorías. Esta campaña se ejecuta por bloque con costes modestos y detiene si falla instrumentación.
