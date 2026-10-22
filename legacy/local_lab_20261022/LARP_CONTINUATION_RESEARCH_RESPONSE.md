# LARP: continuación experimental y revisión adversarial

Fecha: 8 de octubre de 2026. Esta continuación conserva la especificación y los resultados de v0.1, incorpora la conversación compartida como contexto y abre series técnicas independientes. Las decisiones que siguen se apoyan en corridas efectivamente ejecutadas y conservadas; los protocolos pendientes se identifican como tales.

**Actualización posterior:** [LARP_PHASE_3_RESULTS_AND_NEXT.md](C:/Programación/LARP/LARP_PHASE_3_RESULTS_AND_NEXT.md) registra otras cuatro corridas, aprobadas con límite de 120 segundos y umbral del 98% sin cambios. BALANCED pasa train/SS/UU al 100% en ambas semillas en 38,912 segundos incluyendo imports; queda un fallo auxiliar en destino 61 y XOR sigue pendiente. H-R1 recibe apoyo débil y H-R2/H-R3 contraevidencia débil; H1–H6/C intactos. Verificación actual: 232 PASS, 16 manifests, 139 hashes y 27 archivos originales intactos. Los resultados y costes de las secciones siguientes se conservan como registro de la continuación anterior.

## 1. Decisión científica principal

Hay dos preguntas que requieren experimentos distintos: si el núcleo puede seleccionar y combinar información distribuida, y si una distribución de sensores por tipos permite adquirir mejor una señal espacial. Una organización útil para adquirir señales no tiene por qué mejorar la computación una vez igualadas esas observaciones. La continuación trata ambas preguntas por separado.

La recomendación es conservar el patrón aviar como candidato, mantener un control con los mismos términos locales y sin penalización espectral, y exigir un núcleo recurrente competente antes de comparar arquitectura neuronal. La prioridad de cómputo pasa de aumentar tamaño a establecer controles fuertes. El generador original, los siete presets, `model.py`, los checkpoints previos y el umbral .98 permanecen como registro de v0.1.

Las ideas recuperadas de la conversación y su evaluación concreta están en [SHARED_CONVERSATION_AUDIT.md](C:/Programación/LARP/docs/SHARED_CONVERSATION_AUDIT.md). Adoptamos recurrencia compartida, comparación de tipos y trazabilidad. Plasticidad, tres dimensiones, estados en conexiones y lenguaje quedan como ramas posteriores con criterios explícitos de entrada. Ninguna metáfora biológica o de emergencia constituye evidencia de capacidad.

## 2. Qué hemos aprendido sobre el 98%

El ensayo original de XOR remoto obtuvo aproximadamente .48–.52 y cerró el piloto. Se ejecutaron tres series nuevas para localizar el fallo sin abrir el test científico ni escoger checkpoints favorables.

| Serie | Cambio controlado y coste medido | Resultado final | Implicación |
|---|---|---|---|
| Diagnóstico de capacidad | MLP, bits juntos en receptor, interfaces separadas locales/remotas; 14 corridas, 112.576 s | MLP 2/2 y G directo 4/4: 100%; local/remoto separado: 50% en train y validación | El bloque calcula XOR con acceso conjunto. El fallo aparece al distribuir la interfaz, incluso a 1–2 hops. |
| Target × intensidad | Mismos inputs/roles; b0 frente a XOR, incremento ×1/×10; ocho corridas Grid-local, 74.367 s | Todas: 50%. Las 24 ramas posteriores quedan NOT_RUN por la puerta previa | Aumentar sensibilidad no basta para seleccionar información ni aprender la función. |
| Política del minibatch | Un triple con sus cuatro patrones por batch, mismo B4 y 250 updates; dos corridas nuevas, 44.246 s | b0: train .708/.896, validación .750/.688 | El paquete de agrupamiento/orden mejora aprendizaje parcial; quedan selección y generalización deficientes. |

La primera serie no demuestra generalización en el control directo: enumera los cuatro patrones posibles. En las interfaces separadas se retienen cuatro destinos y se entrenan doce; las fuentes son distintas del receptor y accesibles dentro de T16. En la segunda serie, gain1/XOR reproduce exactamente los pesos finales de la primera en ambas inicializaciones. La tercera reutiliza RANDOM como control y lo declara como reutilización, sin contar nuevas réplicas. Cambian agrupamiento y orden/curriculum; el remanente de 250 updates deja exposiciones ±1 distintas para 16/12 casos en ambas seeds. El contraste no aísla exclusivamente el balanceo de etiquetas; los protocolos y resultados se conservan con esa desviación declarada.

El incremento ×10 mejora algunos gradientes y empeora pérdidas/normas. No se interpreta como cura de oversquashing. Los minibatches balanceados consiguen aprendizaje parcial, pero el bit distractor aún cambia clases: para b0, una selección correcta exige que voltear fuente0 cambie la respuesta y fuente1 la conserve. La accuracy tras flips es redundante con accuracy cuando se enumeran los cuatro patrones; los cambios de clase por rol aportan una comprobación distinta de selectividad.

Estos resultados descartan que baste afirmar «existen caminos de longitud ≤16» o «XOR es demasiado difícil». Son compatibles con interacción entre acondicionamiento, agregación, representación de roles y ruido de optimización. No identifican una causa única ni un efecto MHU. Se detiene el ajuste del núcleo nominal bajo esta rama: no se extienden updates, no se elige un punto intermedio favorable y no se rebaja .98.

### Control recurrente de referencia

Se abre una serie independiente con GRU32 compartida sobre el mismo grafo. Conserva encoder, LayerNorm de mensajes, mensajes tanh con distancia, media de vecinos, entrada persistente y readout; sustituye el incremento residual por `h[t+1]=GRUCell([m[t],u],h[t])`. G sigue sin observar tipos.

El control tiene 12.481 parámetros frente a 12.261 del G original: +1,79%. Los MAC lineales por nodo/paso pasan de 10.112 a 10.240: +1,27%, sin contar activaciones y operaciones elementales de gating. Es un rival práctico próximo en tamaño; no es matching exacto ni una intervención que aísle una sola propiedad matemática de la recurrencia. Un éxito mostraría una alternativa de ingeniería, sin atribuirlo a MHU.

Se reutilizan los mismos cuartetos balanceados, datos, dos inicializaciones, AdamW .003, T16, B4 y 250 updates. Primero b0 Grid-local; ambas seeds deben superar .98 en train y validación para abrir XOR local, luego MHU-local y finalmente remoto. Techo 240 s, máximo 16 corridas, todas conservadas y sólo estado final.

**Resultado: no supera la puerta.** Dos corridas completas en 18.504 s; train 1.00/.9375 y validación .75/.75, con BCE de validación 1.558/1.671. Las catorce ramas XOR/MHU/remoto permanecen NOT_RUN. Ambas seeds aciertan todos los patrones de dos destinos y responden de forma constante en los otros dos; éstos comparten fuente0 lógica11. Ese hallazgo posthoc orienta a generalización espacial/roles, sin constituir prueba de su causa. No se adopta GRU como núcleo validado ni se ejecuta otro HPO. Informe y corridas: [GRU_BASELINE.md](C:/Programación/LARP/docs/GRU_BASELINE.md).

### Ablación de coordenadas absolutas

Tras la petición de continuar se ejecutó la siguiente intervención especificada: mismo modelo GRU, pesos iniciales, pool, calendario, targets, mensajes/distancias y presupuesto; únicamente se ponen a cero todos los canales21:25 del input. COORDS_ON reutiliza las corridas anteriores. Dos corridas COORDS_OFF completaron en **20.200 s**:

| Seed | Train OFF | Validación ON reutilizada | Validación OFF | BCE validación OFF |
|---|---:|---:|---:|---:|
|2101|1.00|.75|.875|.377215|
|2102|1.00|.75|1.00|.000588|

La mejora aparece en ambas seeds, pero **la puerta conjunta .98 sigue fallando**. Seed2101 responde constantemente 0 en destino20 y comete dos errores; no se escoge la seed favorable ni se abre XOR/remoto. La intervención elimina información absoluta del encoder, mientras conserva distancias de mensajes. Sus 128 pesos asociados permanecen en el optimizer y conteo nominal, aunque no reciben gradiente de datos. Puede cambiar simetría, condicionamiento y oportunidades de memorización; no prueba una causa única. Es una pista concreta para mejorar el diseño compartido, sin validar todavía un núcleo ni una ventaja MHU. [ROLE_GENERALIZATION.md](C:/Programación/LARP/docs/ROLE_GENERALIZATION.md).

Un control positivo determinista usa sólo los inputs disponibles y E: cuatro campos `[mask0·bit,mask0,mask1·bit,mask1]`, difusión `h←.5h+.5mean(h)` durante T16, y cocientes locales numerador/denominador por rol. Query se localiza mediante sus canales de entrada; targets no participan en el cálculo. Resuelve **512/512 decisiones b0/XOR sobre 256 inputs** Grid/MHU, local/remoto, train/val, en .111 s; un denominador cero se registra como inaccesible. Esto confirma un algoritmo de transporte posible para el pool concreto. La separación de roles y el decoder XOR están dados explícitamente: tiene cero parámetros aprendidos, no es un rival con matching neuronal y no resuelve el 98% de aprendizaje. El denominador remoto mínimo es 4.12e−12: la cancelación exacta entre campos proporcionales no demuestra resistencia a ruido interno. Preregistro, script y límites: [ROLE_TRANSPORT_CONTROL.md](C:/Programación/LARP/docs/ROLE_TRANSPORT_CONTROL.md).

## 3. Qué distribución aviar se usa ahora

El generador aviar nuevo combina exclusión polidispersa, repulsión homotípica y penalización espectral por tipo/unión. Conserva N400, L20 y conteos 163/85/68/50/34. Sus radios y una fracción de packing .58 proceden de la referencia retiniana; la inicialización, penalización blanda, optimizador y término espectral explícito son decisiones propias. No reproduce un mosaico empírico ni las proporciones exactas de la simulación publicada. [Jiao et al., PRE 2014](https://doi.org/10.1103/PhysRevE.89.022721).

Se generaron tres semillas completas y tres controles locales desde las mismas etiquetas/coordenadas iniciales, con iguales términos locales y presupuesto. La única intervención del objetivo es poner a cero el peso espectral. La auditoría confirma ocho archivos científicos comunes con hashes idénticos; el hash agregado local difiere por incluir su wrapper adicional. Ese wrapper conserva el primer candidato empaquetado sin seleccionar según certificado MHU. En esta tanda todos los candidatos proceden del intento cero.

| Candidata | Certificado MHU finito | Packing válido | Tiempo de generación y certificado por semilla |
|---|---:|---:|---|
| Aviar completa | 3/3 | 3/3 | 8.267 / 7.806 / 7.912 s |
| Sólo términos locales | 0/3 | 3/3 | 6.705 / 6.587 / 6.315 s |

Las seis tienen 2.400 arcos kNN y una SCC. Todos los optimizadores alcanzaron el límite de 1.000 iteraciones L-BFGS-B; admitir el certificado no implica convergencia al mínimo. El componente raro E de full1101 presenta un pico no optimizado S/N=.4741, próximo al límite .5, y orden hexático descriptivo apreciable. Por ello no se extrapola desorden ni hiperuniformidad al límite asintótico. La estabilidad por población y tamaño debe revisarse antes de escalar.

El control local1103 conservó un fallo inicial de diferencias finitas: un contacto a 5.55e−9 del corte C¹ produce error de discretización. Una auditoría de epsilon muestra convergencia del error hasta 1.61e−8; no se modificaron energía ni geometría para ocultarlo. Certificados, fallos, gradientes y procedencia están en [AVIAN_GENERATOR_REPORT.md](C:/Programación/LARP/docs/AVIAN_GENERATOR_REPORT.md).

## 4. Experimento de adquisición multicanal

Se ejecutaron 144 condiciones de interpolación en 6.516 s: tres familias × tres semillas × native/shuffle × dos estimadores × dos bandas × dos ruidos. Cinco campos independientes, 128 mundos comunes, cien queries externas y conteos iguales. Cada sensor observa sólo su canal; el target y su normalización analítica son independientes de las marcas. El MSE macro pesa los cinco canales por igual.

Resultados con kernel gaussiano local fijado y ruido .1:

| Familia | MSE smooth native | MSE smooth shuffle | MSE fine native | MSE fine shuffle |
|---|---:|---:|---:|---:|
| MHU nominal espectral | .158958 | .179138 | .961615 | .998836 |
| Aviar completa | .047128 | .157525 | .602421 | .929984 |
| Aviar sólo local | .050053 | .147542 | .613358 | .919429 |

El control sin certificado MHU conserva casi toda la ventaja aviar. La diferencia full−local smooth es −.002925, frente a una diferencia full−nominal de −.111830. La distancia media macro al sensor del canal cae de 1.1895 a .9624/.9677; los vacíos a radio2.5 pasan de 4% a .133%. Esto da una explicación concreta de cobertura local, aunque no identifica por separado exclusión, packing y heterocoordinación.

Son tres realizaciones descriptivas, no 128 réplicas arquitectónicas. Full/local cambia coordenadas y microestructura después de optimizar; la cercanía de resultados no prueba efecto espectral exactamente cero. Native/shuffle conserva X y cambia adquisición: estima organización de sensores, no distribución de funciones neuronales. Se conservan los contraejemplos donde MHU nominal empeora frente a shuffle.

### Prueba adversarial con estimador más fuerte

El proceso generador tiene bandas finitas conocidas. Smooth sólo necesita doce coeficientes por canal, mientras el canal menos poblado tiene 34 sensores. Por tanto, buen interpolador local no equivale a información inaccesible para los otros patrones. Se ejecutó un suplemento congelado con pseudoinversa sin ruido y ridge fijado por la covarianza de coeficientes y ruido, sin HPO. Conoce banda y nivel de ruido por igual en todas las condiciones; es un oracle del benchmark, no un estimador universal.

Con M pares de modos, la normalización del banco implica covarianza de coeficientes I/M. El ridge λ=Mσ² minimiza error esperado dentro de estimadores lineales; no es el posterior no lineal exacto de los coeficientes normalizados sobre una esfera. Se fijó rcond=1e−10 para la pseudoinversa. Las 72 condiciones nuevas y los 144 cotejos con los estimadores anteriores completaron en **.644 s**:

| Familia | Oracle smooth, σ=.1, native | Oracle fine, σ=.1, native | Oracle fine, σ=.1, shuffle |
|---|---:|---:|---:|
| MHU nominal | .002397 | .131384 | .140018 |
| Aviar completa | .001994 | .137279 | .129860 |
| Aviar sólo local | .001997 | .136919 | .126345 |

**Sin ruido, todas las condiciones smooth reconstruyen a precisión numérica**: máximo MSE 5.79e−30, rango12 completo y condición máxima4.329. Con ruido smooth, la diferencia full−local es sólo −3.09e−6. En fine, las aviarias nativas empeoran frente al nominal y frente a su shuffle en las tres semillas. Hay 56 coeficientes; D y E tienen sólo 50/34 observaciones y nullidades 6/22, que limitan reconstrucción sin ruido. El oracle supera los interpoladores locales en los 144 cotejos.

Este resultado cambia la recomendación: el hallazgo aviar inicial describe una organización conveniente para decoders locales baratos. No demuestra una ganancia universal de observabilidad ni una ventaja específicamente MHU. El patrón, banda, ruido y estimador interactúan; deben fijarse conjuntamente. El suplemento es posthoc y reutiliza los mismos mundos, por lo que no es nueva confirmación independiente. Datos, condicionamiento y límites están en [SAMPLING_ORACLE.md](C:/Programación/LARP/docs/SAMPLING_ORACLE.md).

### Grid balanceada y consultas continuas

También se ejecutó el baseline Grid con su presupuesto original y conteos desiguales: hasta 100.000 swaps y diez reinicios por seed, sin reducirlos por conveniencia. Una calibración sin MSE predijo 119.21 s en el peor caso conservador, inferior al techo de 180 s. Las tres semillas se admitieron en el primer intento después de 100.000 propuestas completas cada una; construcción 5.518 s, evaluación 3.362 s, total 9.770 s.

Se conservaron las queries originales aligned, que coinciden con nodos Grid, y se añadieron cien consultas continuas comunes por RNG congelado antes de scores. Las **576 condiciones** incluyen cuatro familias, tres estimadores y ambos estratos: 216 aligned previas reproducidas exactamente y 360 adicionales. Reutilizan campos y geometrías; Grid aporta tres coloraciones de una misma rejilla, no tres coordenadas independientes.

MSE macro native, queries continuas y ruido .1:

| Familia | Kernel smooth | Oracle smooth | Kernel fine | Oracle fine |
|---|---:|---:|---:|---:|
| MHU nominal | .154805 | .002405 | .953827 | .131039 |
| Aviar completa | .046185 | .001987 | .608785 | .138230 |
| Aviar sólo local | .047933 | .001987 | .607375 | .136474 |
| Grid balanceada | .130278 | .002230 | .886270 | .128437 |

La ganancia aviar local persiste también fuera de las consultas alineadas. **Con oracle fine gana Grid**; full/local siguen próximos y pueden invertir su orden. No aparece una ventaja específicamente espectral MHU. La Grid fue fuerte bajo el objetivo preregistrado de balance de componentes; no se afirma que sea la mejor coloración posible para exclusión homotípica. Un objetivo que iguale vecinos/vacíos requiere otro contraste. HU-unión generado independientemente sigue pendiente; el shuffle nominal conserva su unión como control condicionado a X. Protocolo y resultados: [SAMPLING_GRID_RESULTS.md](C:/Programación/LARP/docs/SAMPLING_GRID_RESULTS.md).

## 5. Literatura que cambia decisiones

Se encontró un antecedente de generación más cercano: mezcla ternaria de discos no aditivos con repulsión logarítmica homotípica de largo alcance. Distingue desorden, heterocoordinación local y multihiperuniformidad; cinco poblaciones desiguales exigirían una adaptación declarada. Está publicado y revisado por pares. [Lomba et al., PRE 2020](https://arxiv.org/abs/2005.01558).

La recurrencia GRU sobre grafos tiene antecedente revisado en GGNN; justifica un control establecido y no una garantía de resolver nuestro ensayo. [Li et al., ICLR 2016](https://arxiv.org/abs/1511.05493). Los resultados sobre profundidad, topología y sensibilidad motivan medir la dinámica real; sus hipótesis no se transfieren literalmente a este kNN dirigido no reversible. [Di Giovanni et al., ICML 2023](https://proceedings.mlr.press/v202/di-giovanni23a.html).

La investigación reciente distingue sensibilidad remota y capacidad de almacenamiento. XOR de dos bits es una mala prueba inicial de saturación de memoria; no se recomienda saltar a una memoria matricial para resolver este fallo. La publicación de gLSTM se verificó también en las actas oficiales ICLR2026; OpenReview devolvió una comprobación de navegador al acceder directamente al PDF. [Actas oficiales de gLSTM](https://proceedings.iclr.cc/paper_files/paper/2026/hash/c70bc769d6171ef8bb76e36e8d458205-Abstract-Conference.html), [manuscrito de autores](https://arxiv.org/html/2510.08450v2).

El registro completo distingue publicaciones revisadas, preprints y la solicitud IBM publicada; no trata una patente como validación independiente. GHR2026v2 y Park/Kim2024 se registran como preprints con aceptación no verificada. La búsqueda dirigida no encontró una implementación neuronal MHU equivalente, pero no certifica novedad. Los once registros y sus límites de transferencia están en [LITERATURE_NEXT_PHASE.md](C:/Programación/LARP/docs/LITERATURE_NEXT_PHASE.md).

## 6. Próxima fase y reglas de decisión

1. **Cerrar ingeniería de transporte.** Adoptar un candidato práctico sólo después de reproducir capacidad local y generalización de roles; congelar una versión nueva antes de repetir el smoke original. Un control local aprobado no abre el piloto v0.1. Si el control GRU falla bajo el presupuesto, detener la cadena de rescates y auditar selectividad/interfaz con un protocolo nuevo, sin atribuir fracaso a geometría.
2. **Fortalecer muestreo.** Oracle y Grid con queries continuas ya están ejecutados; limitan el hallazgo a conveniencia para ciertos decoders locales. El siguiente rival debe igualar estadísticas locales y añadir HU-unión independiente; conservar tanto decoder local como espectral fuerte. Separar ruido, banda, presupuesto de construcción y coste de estimación. No seleccionar retrospectivamente sólo la combinación donde aviar gana.
3. **Identificar la parte espectral.** Construir un rival que iguale distribución de vecinos homotípicos, vacíos y packing mientras difiere en ondas largas; no aceptar como control suficiente sólo igualar distancia mínima. Congelar tolerancias antes de resultados. Réplicas geométricas nuevas y análisis por población preceden al escalado.
4. **Volver a funciones neuronales.** Con núcleo competente, comparar G/T/F y native/shuffle sobre X/E/puertos fijos. Para una tarea de sensores, cruzar adquisición distribuida con observaciones comunes igualadas. Si la ganancia aparece sólo al adquirir, pivotar hacia muestreo; si persiste al igualar observaciones y depende causalmente de funciones distintas, investigar computación multicomponente.
5. **Confirmar antes de expandir.** Elegir el rival por la política de validación común, conservar presupuesto/HPO simétricos y todas las semillas. Parar la afirmación MHU si un nulo preciso frente a controles fuertes alcanza la ROPE prevista. Ni 3D, plasticidad ni LM son respuestas automáticas a resultados nulos.

La intervención sobre coordenadas y la ampliación Grid de [NEXT_PHASE_EXECUTION_SPEC.md](C:/Programación/LARP/docs/NEXT_PHASE_EXECUTION_SPEC.md) ya están ejecutadas con todos sus resultados conservados. El documento fija las condiciones para volver a funciones neuronales. XOR/MHU/remoto no se abren automáticamente por una seed favorable; no se elige un nuevo núcleo por intuición.

## 7. Actualización abductiva y límites

H1–H6 y C conservan sus priors originales. Las series son diagnósticos técnicos o adquisición con estimadores fijados; no satisfacen el paquete confirmatorio de computación, robustez y especialización del contrato. No se fabrican Bayes factors a partir de una diferencia descriptiva, no se multiplican gradiente/accuracy/flips como evidencia independiente y no se renormalizan hipótesis marginales como una partición exclusiva.

La actualización de trabajo es ordinal y local: se debilita la explicación de un fallo puramente de capacidad XOR; se fortalece investigar política de minibatches/selectividad/generalización. Los datos aviares motivan cobertura local bajo decoders baratos; el oracle debilita una lectura de observabilidad universal y muestra una inversión de ranking en fine. Ninguna de estas observaciones establece robustez, plasticidad o superioridad general. Las nuevas comparaciones posthoc, aunque se congelen antes de su propia ejecución, no se convierten en confirmación de las intuiciones que las motivaron.

Antes de confirmación siguen pendientes los bloqueos localizados del contrato: C3 de parejas, puertos parciales, D4 condicional y frontera singular del posterior continuo, entre otros registrados. La nueva exploración no los resuelve silenciosamente.

## 8. Procedencia y verificación

Cada serie guarda configuración y hashes de dependencias nombradas antes de optimizar/evaluar, inputs, semillas, estados y resultados desfavorables. El material recuperado de la conversación, los arrays y checkpoints grandes permanecen localmente; el repositorio conserva extractores, manifiestos, informes y datos resumidos verificables. No se abrió el test de las tareas neuronales primarias, no se ejecutó el piloto y no se actualizaron priors.

**Suite global final: 227 pruebas aprobadas en 9.07 s**, JUnit y log en `artifacts/next_phase/tests_v2/`; se conserva también la tanda anterior de 218PASS en `tests/`. Son 64 pruebas nuevas además de las 163 anteriores; incluyen gradientes geométricos, selección de controles no MHU, causalidad del soporte, separación de fuentes, preservación de presupuestos, matching declarado, álgebra/rangos del oracle, ablación exacta de coordenadas y guardas de coste/reutilización Grid. Sus resultados verifican software y protocolo, sin sustituir evidencia arquitectónica.

Las 28 corridas neuronales nuevas consumieron 7.000 updates y 269.893 s incluyendo sus medidas. Las seis generaciones aviares sumaron 43.592 s; muestreo local 6.516 s, oracle espectral .644 s, difusión .111 s y suplemento Grid 9.770 s. Estos tiempos miden etapas distintas, con preparación/imports parcialmente fuera según cada serie; no se usan como un benchmark comparativo de velocidad entre algoritmos. Picos RSS muestreados por proceso de estas series permanecen por debajo de 461 MB. No se ejecutó N1600/6400 ni CUDA.

Añadir módulos cambia la identidad global de código usada por las puertas antiguas: esos artefactos se conservan como resultados históricos, no como autorización para abrir una fase actual. La auditoría final verifica **15 manifests, 122 hashes de archivos congelados y 27 archivos científicos originales intactos**. Ambas auditorías e historial quedan en `artifacts/next_phase/`; comandos y archivos de navegación se incorporan al README.
