# LARP N400 original — tarea funcional matemática T01–T10, cierre AB-R

**Fecha 2026-10-30.** Por primera vez después del bloqueo se han utilizado directamente las **coordenadas nativas de seis NPZ originales exportados con bits IEEE-754 idénticos**. Rama fuente privada `research/ab-r-native-export-20261030-053103` commit `60ec5f489d18fc97be1d40d135c4142d194d0a1b`; los 6 hashes Git de NPZ coinciden con las identidades históricas. Tres semillas emparejadas 1101–1103, 400 sensores, cuotas por clase 163/85/68/50/34. **No se ha entrenado una red neuronal ni ejecutado Wei original, ni utilizado imágenes multibanda reales**.

## Corrección metodológica E01: resultados originales GP inválidos para escala física

El primer código congelado describía longitud de correlación física `ell` pero aplicaba `exp(-2L²/ell² * sum sin²(pi*d/L))`, equivalente a longitud local `ell/(2*pi)` en el límite de pequeños desplazamientos. Fue corregido después de la primera exposición a resultados: `exp(-L²/(2*pi²*ell²) * sum sin²(pi*d/L))`, con comportamiento local `exp(-d²/(2ell²))`. La primera corrida `RESULTS_T01_T10.json` se preserva pero **T01–T05 son inválidas para aquella interpretación física**. Resultados corregidos `RESULTS_T01_T10_REPAIRED.json` son **exploratorios tras reparación** y no un nuevo test ciego; T06–T10 permanecen idénticos (96 registros no GP). El fuente v2 quedó congelado ANTES de la segunda ejecución. Ver `ERRATA_E01_GP_LENGTHSCALE.md`.

## Comparación de riesgos

Todos los valores siguientes son **medias por especie con igual peso y luego entre tres semillas**. Menor es mejor. Los resultados no identifican causalidad neuronal.

| Ciclo | Estimando | MHU original | LOCAL original | CVT proxy | Semillas MHU mejor que LOCAL |
|---|---|---:|---:|---:|---:|
| T01 | analytic_GP | 0.84808 | 0.84104 | 0.81929 | 0/3 |
| T02 | analytic_GP | 0.62857 | 0.62375 | 0.59460 | 1/3 |
| T03 | analytic_GP | 0.31588 | 0.31613 | 0.30372 | 2/3 |
| T04 | analytic_GP | 0.07672 | 0.07915 | 0.07713 | 3/3 |
| T05 | analytic_GP | 0.01011 | 0.01049 | 0.01028 | 3/3 |
| T06 | graph_communication | 0.10929 | 0.11265 | 0.10417 | 3/3 |
| T07 | graph_communication | 0.00510 | 0.00682 | 0.00677 | 3/3 |
| T08 | graph_communication | 0.00510 | 0.00521 | 0.00478 | 3/3 |
| T09 | heldout_Fourier | 0.03555 | 0.04138 | 0.04870 | 3/3 |
| T10 | heldout_Fourier | 0.73483 | 0.72583 | 0.77542 | 1/3 |

### Hallazgo funcional condicional: transición de escala

En el riesgo posterior de un proceso gaussiano periódico conocido, **CVT gana para ell=0.5 y 0.8**, y también a ell=1.25. A partir de ell=1.25 MHU obtiene **ligerísima ventaja sobre LOCAL** en el promedio, y en ell=2 y 3.5 supera al CVT proxy de media. Esto concuerda con que MHU priorice organización espacial extensa y LOCAL/CVT exploten cobertura local, pero n=3 y dependencia del kernel impiden extrapolar. A ell=2, MHU supera LOCAL en 3/3 semillas, pero CVT en solo 1/3; el ganador por media no equivale a ganancia por mayoría de semillas.

### Beneficio y coste de comunicación

Con seis enlaces a los vecinos próximos, la pérdida de accesibilidad multiclase a **dos saltos** es MHU **0.00509984**, LOCAL **0.00682169**, CVT proxy **0.00676756**: MHU presenta menor pérdida en las tres parejas. A un salto, CVT knn gana y la falta de ciertas modalidades domina. El enrutamiento explícito por tipos proporciona cobertura completa a un salto y riesgo mínimo geométrico por clase, pero requiere enlaces más largos y conocer previamente posiciones/tipos. En MHU, la longitud media de enlaces sube de **1.1048** (kNN) a **1.2426** (por tipo), aproximadamente un **12.5 %** más. CVT sigue siendo mejor bajo routing directo por tipos.

### Fourier fuera de banda

En la banda baja **no incluida en los seis modos optimizados**, MHU ofrece menor potencia espectral media que LOCAL y CVT proxy (T09, 3/3 semillas contra ambos). En las frecuencias más altas T10, LOCAL es mejor de media (MHU/LOCAL=1.0124); por tanto, no existe dominancia total de Fourier. T09–T10 son identidades calculadas sobre puntos fijos para energía igual por modo, no pruebas de hiperuniformidad asintótica.

## Auditoría

- Prerregistro T01–T10 previo al primer cálculo: commit `17824ebbec971764896462e5cba2dee75e84973f`; fuente original congelado `8781b77d2068e45a5e792a63e67f453838e64210`.
- Errata y segundo fuente físicamente corregido: commit `e6791e0c2178b37dbf3679bbb912ef58cbf96483`. Datos antiguos intactos.
- Primera fuente produjo 156 resultados; segunda también 156; **96 registros de T06–T10 idénticos** y 60 registros GP cambian de forma esperada.
- 25/25 chequeos de consistencia y repetición exacta de 156/156 registros y 52/52 medias en un segundo entorno JS. No es reproducción externa en otro ordenador.
- No existen 156 muestras científicas independientes; hay **3 geometrías emparejadas** y los distintos funcionales son altamente dependientes.
- La implementación CVT es un control de Lloyd periódico 24×24, 25 iteraciones; no equivale al optimizador más competitivo posible ni a Wei 2010. Los resultados dependen del prior GP elegido, del radio de comunicación, del número de sensores por especie y del coste no modelado del routing.

## R5 / decisión y continuidad

**10 cuestiones ejecutadas y auditadas**: 5 válidas bajo código original, 5 válidas como análisis exploratorios posteriores a reparación (con 5 primeros intentos inválidos). Cero nuevas validaciones independientes; cero originalidad N1/N2/N3. CT2 condicionado matemático 24/100, rama proxy entrenada 18/100, sin incrementos. **STOP_LOCAL** en este mismo conjunto de geometrías y supuestos. No repetir semillas o cambiar ell retrospectivamente para obtener victoria. El gran salto pendiente es compilación real de Wei + cinco modalidades ópticas independientes y arquitecturas aprendidas equivalentes en datos, coste y entrenamiento.

**Estado GitHub:** rama `research/ab-r-native-functional-20261030`, `main` sin fusionar; artefactos reproducibles con código, fuentes y los 10 contratos A–J en `LEDGER_T01_T10_AJ.json`.
