# Ledger acumulativo de priors LARP — actualización BR30 (21-10-2026)

Se conserva la procedencia histórica documentada; **no se inventa un ledger histórico exhaustivo que aquí no se ha importado**. IDs locales nuevos BR30-L01 etc, sujetos a reconciliación con el ledger principal cuando esté disponible. Un prior no es un hecho universal.

| ID | Proposición | Procedencia | Alcance y clase | Evidencia favorable | Evidencia contraria / incertidumbre | Falsador | Decisión |
|---|---|---|---|---|---|---|---|
| BR30-L01 | La cobertura multiclase local reduce distancias al quinto tipo frente a puntos iid bajo cuotas fijas | Geometrías originales + nuevos A/B | SINTÉTICO geométrico; una geometría por algoritmo | Cobertura k16 LOCAL 96.20%, RANDOM 62.32%, estratificado 80.88% | Depende de constructor y distribución fija; los antecedentes multi-class blue noise ya persiguen esto | Control multi-class blue noise optimizado iguala o supera con mismo coste | CONTINUE condicionado |
| BR30-L02 | LOCAL mejora reconstrucción composicional de campos suaves frente a muestreo estratificado simple | Piloto C11 y confirmación nueva en mundos sintéticos | SINTÉTICO, condicionado a DGP Fourier y kernel gaussiano | Delta confirmación −0.0750 IC95 [−0.0912,−0.0589] por mundo | Una geometría fija y una familia Fourier; control estratificado simple no es SOTA | Replicación con nuevas geometrías y baselines multiclase blue noise elimina ventaja | CONTINUE limitado |
| BR30-L03 | La ventaja espacial se reduce conforme crece la frecuencia del campo | Piloto C11–C15 | SINTÉTICO exploratorio | LOCAL 0.134 vs 2.106 al pasar f1→f6; delta frente estratificado cae | En f6 MSE elevado para todos; escalas y amplitudes fijas | Una nueva familia de señales altas frecuencias preserva ventaja | PIVOT a suavidad/cobertura |
| BR30-L04 | El beneficio espacial depende de correspondencia correcta entre etiquetas y sensores | F26, F28, F29 | SINTÉTICO exploratorio | Permutar etiquetas/descorrelacionar señales degrada casi a nulo | Consecuencia parcialmente incorporada al DGP que define cinco campos | Alternativas sin tipos conservan misma ventaja | CONTINUE con ablaciones fuertes |
| BR30-L05 | MHU supera a LOCAL por la penalización espectral en este benchmark | Piloto C11–C15 y confirmación C11 | NO_VALIDADO; contraste H3 | MHU f2 ligeramente menos MSE (0.807 vs .812) | LOCAL mejor f1 (0.134 vs 0.140), confirmación .1258 vs .1323; sin control estadístico de H3 | Series independientes grandes, tareas long-range y medidor asintótico | STOP afirmación fuerte |
| BR30-L06 | La geometría LOCAL por sí sola supera modelos de lenguaje y Transformers | Contexto previo LARP vs GPT | NO_VALIDADO | Ventaja en tareas espaciales bajo prototipo inicial | GPT pequeño gana bytes-per-byte, interpolación clásica supera redes en tarea espacial; ninguna comparación actual con GPT | Comparación GPU con paridad FLOPs y benchmarks externos | STOP reivindicación |
| BR30-L07 | Hay novedad científica al promover cobertura heterotípica local | Estado del arte revisado en BR30 | NO_VALIDADO | Interesante hipótesis funcional | Multi-Class Blue Noise Sampling (Wei, SIGGRAPH 2010) y heterocoordinación retinal (Lomba et al., 2020) anticipan idea | Mecanismo que supera métodos competentes con predicciones nuevas y replicación externa | NO 2/3 |
| BR30-L08 | Una red de especialistas semánticos (lenguaje/código/matemáticas) mejora gracias a geometría LOCAL | Propuesta del usuario; todavía no probada aquí | HIPÓTESIS NO_VALIDADA | Cobertura geométrica de cinco tipos y éxito espacial como motivación | No equivalen sensores Fourier a expertos semánticos; MoE ya existe | Factorial geometría × especialización sobre corpus externo; mejores baselines | REPAIR antes de afirmar |


---
## Anexo BR12 dinámico — 2026-10-21
**Procedencia:** docs/07_BR12_LEDGER_12_CICLOS.md; commit 4d4d2179c2c9913150d9cb7088fe645fb2603037. **NO es confirmación externa.** Los IDs BR12-L09–L15 son distintos de BR30-L01–L08 y no los sustituyen. Mantener la evidencia anterior para reconstruir la actualización abductiva.

# Priors nuevos LARP · BR12 dinámico (anexar al ledger maestro)

| ID | Proposición y procedencia | Evidencia favorable | Contraevidencia / incertidumbre | Falsador | Estado |
|---|---|---|---|---|---|
| BR12-L09 | CVT por tipo logra cobertura próxima de las cinco clases; 12 geometrías N512 y N4096. | CVT512 97.31% k16; CVT refinados 4096 ~97.6%. | CVT no es Wei; no existe réplica independiente del original LOCAL a N4096. | Original LOCAL nuevas geometrías supera CVT genuino y barato de forma replicada. | SINTÉTICO exploratorio |
| BR12-L10 | La ventaja LOCAL f1 sobre CVT puede explicarse parcialmente por iteraciones de optimización y bandwidth del estimador. | CVT inicial MSE f1 k24 .1542 > LOCAL .1404; refinado+tuning f1 CVT .0893–.0922 < LOCAL .1074. | Efectos de CVT refinamiento y tuning no se aislaron factorialmente con igualdad total de coste. | Diseño independiente y igualado de geometrías/costo invierte el ranking. | SINTÉTICO exploratorio |
| BR12-L11 | Función aprendida multiclase sobre posiciones favorece necesariamente LOCAL. | No confirmada. | MLP cinco canales: CVT .1249–.1319, LOCAL .1478 y MHU .1608; estimador analítico mejora todos. | GNN original Scale3D con múltiples patrones independientes y nuevos datos supera CVT/PointNet++ a igual coste. | NO_VALIDADO |
| BR12-L12 | La supresión espectral MHU de modos bajos es condición necesaria para predecir campos suaves. | MHU S_all finito ~4.35e-6. | CVT tiene S_all muy superior (.05–.09) y menor MSE. Metrica S calculada en 80 modos y geometrías fijas. | Tareas nuevas de largo alcance muestran ventaja replicable espectral neta. | REFUTADO EN ESTE MODELO, universal NO_VALIDADO |
| BR12-L13 | El acceso oracular de un punto por tipo es más eficiente para composición que los 16 vecinos globales. | Garantiza cinco tipos con solo 5 lecturas de sensores. | LOCAL MSE .316 vs .114 con 16 vecinos; ruido de interpolación mayor; búsqueda de 5 árboles tiene coste extra. | Otras funciones/tareas y costes totales muestran superioridad reproducible. | NO_VALIDADO |
| BR12-L14 | CVT mantiene ventaja bajo perturbaciones por sensores perdidos. | A 0% CVT ~.10 vs LOCAL .129. | A 60% MHU .474 < CVT ~.499 y LOCAL .531, todo muy degradado. | Ensayos independientes con fallos correlacionados/ruido real. | SINTÉTICO condicionado |
| BR12-L15 | La diferencia original Scale3D/N4096 puede inferirse a partir de LOCAL_derived/N512. | Ninguna. | El derivado N512 tiene peor cobertura que estratificado; no comparte optimizador/escala. | Reimplementación matemáticamente equivalente con tests de gradiente e inicialización. | RECHAZADO como equivalencia |


---
## Actualización acumulativa BR30 dinámico (22-10-2026)
Procedencia: `docs/BR30_DYNAMIC_C01_C08_LEDGER.md`, commit `135c4a1575addef794eee69b6b0052e011ea415d`. Las entradas BR30-D16–D21 NO sustituyen ni borran hipótesis históricas; todos los contrastes funcionales son exploratorios.

# Anexo acumulativo de priors LARP (BR30 dinámico)

**Priors nuevos BR30-D16–D21**. Son actualizaciones cualitativas, no probabilidades bayesianas calibradas; la fuente es el estudio exploratorio C01–C08. Integrar al ledger maestro conservando priors anteriores BR12/BR30 sin borrar contradicciones.

| ID | Procedencia / proposición | Favorable | Contraria / incertidumbre | Falsador / siguiente prueba | Estado |
|---|---|---|---|---|---|
| BR30-D16 | C01/C02: el generador original Scale3D v1/v2 es recuperable y ejecutable en CPU. | Exact hash y cuatro seeds x 600 iteraciones. | No se cotejó bitwise con todos los checkpoints históricos. | Comparación contra archivos históricos en mismo hardware/software. | TECNICO_VERIFICADO limitadamente |
| BR30-D17 | C03/C04: MHU mejora sistemáticamente la reconstrucción bajo agujeros espaciales. | Seed 5201 MHU .147 vs LOCAL .166; seed 5204 MHU .184 vs LOCAL .205. | Seeds 5202/5203 invierten; media −.00253, IC descriptivo cruza cero. | Nuevas geometrías y perturbaciones de naturaleza distinta fijadas antes de test. | NO_VALIDADO |
| BR30-D18 | C05: la supresión espectral finita MHU crea una topología kNN mejor para aprendizaje. | Brecha Laplaciana .03416 MHU vs .03385 LOCAL. | CVT .0334–.0336; efecto pequeño; no mide aprendizaje. | Mostrar mejora de aprendizaje con mediación topológica y recursos iguales. | SINTETICO_EXPLORATORIO |
| BR30-D19 | C06/C07: LOCAL ofrece ventaja neuronal reproducible vs MHU/CVT. | LOCAL gana por .0027–.0042 en una seed. | Orden cambia en otra seed y entrenamiento incompleto; CVT reusable. | Convergencia/replicaciones verdaderas/benchmarks no construidos para suavidad. | NO_VALIDADO |
| BR30-D20 | C08: presupuestos breves de aprendizaje pueden invertir rankings prematuramente. | Todos los mejores checkpoints al final y MSE mejora solo 7% vs cero. | No prueba que el ranking convergido difiera realmente. | Seguimiento de pérdidas hasta meseta por varias seeds con mismo compute. | PRIOR_METODOLOGICO_CONTEXTUAL |
| BR30-D21 | Validación: cuatro muestras MHU original reproducen supresión de banda finita para union y tipos. | Auditoría exacta FP64, todas superan criterio finito; S_union .00044–.00046. | No prueba HU asintótica, novedad ni valor para arquitectura. | Repetición en tamaños crecientes y medición función/coste. | SINTETICO_VERIFICADO_FINITO |


---
## Actualización acumulativa 22-10-2026 — Nuevo bloque AB30 libre
Fuente íntegra en commit `4f8c7c37bd633cd4fd9d12e4be8f09b65a53ce83` y `docs/AB30_LIBRE_20261022/LEDGER_30_CICLOS.md`. Preservar BR30-F01..F10, las afirmaciones anteriores y sus contraejemplos. Todos son resultados exploratorios sobre cuatro geometrías originales; no posterior bayesiano calibrado.

# Ledger acumulativo de priors de LARP — apéndice BR30 libre (no borrar entradas anteriores)

| ID | Hallazgo/Hipótesis | A favor | En contra o límite | Estado |
|---|---|---|---|---|
| BR30-F01 | MHU penaliza eficazmente fluctuación espectral finita de conjunto y cinco tipos | C02-C03, C21, fuente original | Estaba definido como objetivo; no novedad asintótica | VERIFICADO FINITO |
| BR30-F02 | MHU ofrece cuadratura superior a alternativas competentes | C24 frente LOCAL/CVT/Sobol | Retícula exacta en banda baja; Sobol mejor en varias funciones no periódicas | REFUTADA UNIVERSALIDAD |
| BR30-F03 | Una retícula sin aliasing domina MHU | C06 integrales no resonantes exactas | C15 encuentra resonancia con S=1 | REFUTADA UNIVERSALIDAD |
| BR30-F04 | Supresión MHU persiste fuera de banda | C09/C10 parecían favorables | C11 revela fuga, C12 encuentra LOCAL mejor fuera del corte | REPARADA: NO VALIDADO |
| BR30-F05 | Cada especie HU podría producir unión no HU bajo fracciones estables | Premisa histórica | C22 demuestra desigualdad triangular: imposible bajo sus hipótesis | RECHAZADA COMO PRINCIPIO |
| BR30-F06 | Coordinación de fases entre especies añade supresión finita de unión | C23: shifts independientes elevan S_total ~21x conservando S_i | Objetivo explícito del optimizador, no nueva teoría ni ventaja neural | OBSERVACIÓN SINTÉTICA |
| BR30-F07 | Multiespectral y disponibilidad local generan intercambio útil | C07-C08 y C29 frontera observada | CVT/QMC/lattice otras ventajas, se ignoran costes de construcción | HIPÓTESIS ABIERTA |
| BR30-F08 | Métrica de S(k) baja predice mejora en GPT | Ninguna | Experimentos Scale3D previos no concluyentes, ningún test de GPT aquí | NO VALIDADO |
| BR30-F09 | Reducción de sensores preserva gran ventaja MHU | C27 ligera ventaja a mitad densidad | Pérdida de casi toda supresión: MSE entre organizados converge | DEBILITADA |
| BR30-F10 | Beneficio de fases cruzadas podría mediar tareas de señal compartida | C23 y álgebra de amplitudes | No se ha entrenado ni ensayado tarea shared-channel | PRIORIZAR SI HAY 8 CICLOS MÁS |

**Procedencia:** `docs/AB_LEDGER_C01_C30.json`, fuente `src/ab30_live.py`. Estados exploratorios no son *Bayes factors* ni posteriores calibrados. Históricos BR12/BR30 anteriores permanecen en ledger maestro.


---
## Anexo acumulativo: AB08 coordinación intertipo, 22-10-2026
**Procedencia:** `docs/AB08_CROSSPHASE_20261022/LEDGER_AB08.md`, `data/AB08_CROSSPHASE_20261022/AB08_ALL_CYCLES.json`, ocho pruebas exploratorias sobre cuatro geometrías antiguas. No nuevos BF ni posteriores calibrados; conservar las entradas históricas con sus contraejemplos.

# Actualización acumulativa de priors LARP · AB08 2026-10-22
Todas las probabilidades son **cualitativas**, no Bayes factors calibrados. Fuente por ciclo `results/Cxx.json`. Las entradas anteriores BR30-F01..F10 se preservan.

| ID | Proposición | Apoyo nuevo | Contraevidencia y ámbito | Estado |
|---|---|---|---|---|
| BR08-X01 | Coordinar fases cruzadas reduce potencia espectral conjunta | C01/C02: MHU 21.54x aumento tras shifts independientes, S_a constante | Igualdad algebraica conocida; banda in-sample; retícula mejor | FINITO_SINTETICO_VERIFICADO |
| BR08-X02 | La correlación funcional rho determina el valor añadido de fases cruzadas | C03 identidad rho P_total+(1-rho) P_diag, Monte Carlo | La per-type S_a explica parte importante y la identidad es matemática conocida | VERIFICADO_EN_DGP |
| BR08-X03 | Mejora MHU se generaliza a frecuencias diferentes | Ninguno | C04/C08 fuera de banda MHU peor que LOCAL; C08 MSE 3.16e-5 vs 1.71e-5 | REFUTADO_EN_ENSAYO |
| BR08-X04 | Coordinación MHU ofrece ventaja en readout aprendido | C07 Ridge MSE 1.28e-9 vs LOCAL 9.7e-7 | Retícula MSE 8.94e-12; 250 train, 2000 test, campos sintéticos low; no arquitectura neuronal compleja | BENEFICIO_CONDICIONAL_NO_NOVEDAD |
| BR08-X05 | Penalización multiclase añade robustez si desaparecen sensores | Ventaja bajo 10% dropout todavía leve | C06 50% dropout MHU~2.413e-4, LOCAL~2.421e-4 y retícula~2.417e-4 | DEBILITADA |
| BR08-X06 | Un optimizador de traslaciones recupera MHU sobre controles | C05 CVT reduce algunos modos entrenados | No recupera la supresión de MHU, empeora heldout en algunos; faltan Wei y coste comparable | NO_VALIDADO |

**Decisión AB:** observar arquitectura aprendida con señales compartidas *no-Fourier* y comparator Wei real antes de estimar probabilidad de 2/3.


---
## Anexo acumulativo BR06-R01..R07 (22-10-2026)
Procedencia: `docs/AB06_REALDATA_20261022/LEDGER_AB06.md`, `data/AB06_REALDATA_20261022/AB06_ALL_CYCLES.json`; modelos sobre UCI Digits 8×8 con 4 geometrías independientes N128; sin Wei auténtico y sin igualdad de FLOPs. Estados son exploratorios, no posteriors bayesianos calibrados. Preservar las entradas previas y sus contraejemplos.

# Priors acumulativos BR06-R (no sustituyen al ledger maestro)

| ID | Proposición | Evidencia a favor | Evidencia adversa | Grado/alcance |
|---|---|---|---|---|
| BR06-R01 | Generador auténtico Scale3D produce MHU finita también en N128 | C02: cuatro nuevas semillas y Fourier 3D mucho menor que LOCAL | Objetivo explícito; validate=False y tarea 2D; no demuestra HU asintótica | Observación finita verificada |
| BR06-R02 | La geometría MHU otorga mejor clasificación real | Ninguna victoria general | C04 MHU 94,94%, Sobol 96,11%, MLP píxel 96,78%; n=4 | Debilitada, no general |
| BR06-R03 | Cinco funciones sensoriales heterogéneas mejoran el aprendizaje | Hipótesis de complementariedad | C05 roles distintos empeoran MHU ≈1,56 pp respecto a mismas cinco funciones de intensidad | Refutada para este operador/dataset |
| BR06-R04 | La representación sensorial espacial puede incrementar robustez a rotación y ruido | C06 supera al MLP directo pixel en varios shifts | Baselines suavizados reducen la brecha; no está aislado efecto MHU | Abierta para otro dominio, confusión reconocida |
| BR06-R05 | MHU tiene robustez específica frente a LOCAL | C06 en alguna semilla | Medias LOCAL superiores MHU en rotación y ruido; semillas heterogéneas | No validada |
| BR06-R06 | Wei original disponible y ejecutado como baseline | Repositorio público confirmado | README VS2003, no binario ejecutado ni comparabilidad con N128 | BARRERA_DE_EJECUCIÓN, fuente localizada |
| BR06-R07 | MHU en 3D transferida por proyección 2D preserva todas sus ventajas | Fourier 3D finito fuerte | Reconstrucción y clasificación en 2D sin dominio MHU | Hipótesis debilitada para proyección |

Procedencia: `docs/01_LEDGER_AB06.md`, scripts `src/cycle*`, datos `data/C0*.json`; todos resultados exploratorios, NO Bayes factors. Conservar las entradas BR08-X01..X06 y BR30-F01..F10 previas.
