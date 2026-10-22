# Siguiente fase: especificación de ejecución

Fecha: 2026-10-08. Estado actualizado: **secciones1 y2 ejecutadas; comparación neuronal posterior condicionada**. Las decisiones se fijaron antes de sus nuevas series y se conservan a continuación. No sustituyen v0.1 ni abren sus puertas. La implementación posterior no debe inventar un sweep ni elegir la seed favorable.

**Fase 3 posterior ejecutada:** [LARP_PHASE_3_RESULTS_AND_NEXT.md](C:/Programación/LARP/LARP_PHASE_3_RESULTS_AND_NEXT.md) y [PHASE_3_ROLE_COVERAGE.md](C:/Programación/LARP/docs/PHASE_3_ROLE_COVERAGE.md). El currículo BALANCED pasa la puerta registrada train/SS/UU ≥98% en ambas semillas: cuatro corridas completas en 38,912 segundos frente al límite de 120, sin modificar núcleo, semillas, 250 updates o umbral. Una medición AUX retiene el fallo `[61,62,60]` en 2102. Fase 3 terminada, sin extensión automática a XOR/MHU/remoto. H-R1 recibe apoyo débil; H-R2/H-R3, contraevidencia débil; H1–H6/C intactos. La siguiente intervención neuronal propuesta debe aislar orientación de roles sobre contextos físicos fijos; necesita su propio preregistro y no se ejecutó aquí. La línea espectral independiente queda en [INDEPENDENT_SPECTRAL_MATCHING_NEXT.md](C:/Programación/LARP/docs/INDEPENDENT_SPECTRAL_MATCHING_NEXT.md), NOT_RUN.

## 1. Generalización de roles y coordenadas

**Estado de esta sección:** ejecutada el 2026-10-08, dos corridas COORDS_OFF completas; **puerta conjunta fallida**. El protocolo previo se conserva a continuación. La evidencia nueva figura al final de la sección; XOR/MHU/remoto no se ejecutaron.

**Pregunta:** ¿la entrada de coordenadas absolutas facilita memorizar contextos y perjudica una regla de selección compartida? El candidato GRU ajustó train, falló en los mismos dos destinos retenidos y el control determinista resolvió todos los casos. Esto motiva una intervención sobre el input; no establece su resultado.

Serie `role_generalization_v1`, directorio nuevo, máximo dos corridas nuevas, techo 120 s CPU4. Usar exactamente `GGNNLikeModel` y su configuración publicada: N400 Grid1101, d32/T16, 12.481 parámetros, seeds2101/2102, AdamW .003, betas(.9,.999), eps1e−8, wd1e−4, clip1, B4, 250 updates y estado final exclusivamente. Reutilizar pool, inputs/targets y calendario BALANCED por seed, con verificación de hashes previa.

Única intervención: poner a cero **todos** los canales21:25 en train, validación y medidas, tanto en nodos normales como en puertos. Conservar X/E, distancias de aristas, coordenadas lógicas externas para seleccionar/evaluar casos, roles9/10, queries14/15, payload y readout. Las distancias siguen entrando en mensajes: el contraste elimina coordenadas absolutas del encoder, no toda información espacial. Inputs se copian, nunca se modifica el archivo previo.

El control COORDS_ON se reutiliza de `gru_baseline/v1` (no nueva réplica); COORDS_OFF son las únicas dos corridas nuevas. Verificar mismos pesos iniciales, parámetros, optimizer y calendario. Agrupamiento, orden y exposiciones son idénticos entre las condiciones; la desviación de ±1 exposición del contraste RANDOM/BALANCED anterior no se convierte en diferencia de este factor.

Target inicial b0 conserva la segunda fuente distractora. Registrar accuracy/loss train/val, logits por los cuatro patrones/destino, sensibilidad y fracción de cambios de clase al voltear cada fuente, curva/normas y estado final. Para copy perfecto: cambio1 en fuente0 y cambio0 en fuente1. Las predicciones correctas tras flips no son evidencia independiente de accuracy.

**Puerta:** ambas seeds finitas con train+val≥.98 finales. Con 48/16 casos, esto requiere acertar todos los ejemplos de ambos splits. Si falla, cerrar la serie y registrar que esta intervención no resuelve el problema bajo el presupuesto. No prolongar entrenamiento, eliminar la fuente problemática ni pasar a remoto. Si pasa, congelar otra serie para XOR local y después generalización remota; no ejecutar automáticamente esa extensión ni declarar aprendido el smoke original.

Trade-off: eliminar coordenadas puede impedir rutas dependientes de posición, mejorar simetría o simplemente cambiar condicionamiento del encoder. Un resultado positivo no prueba que memorizar coordenadas fuese la única causa; examinar los destinos retenidos y transferir la regla en otra serie. No adoptar un encoder nuevo como default científico por una única geometría.

### Resultado de role_generalization_v1

Las dos corridas finalizaron 250 updates en 20.200 s totales (CPU4; RSS máximo 426,299,392 bytes), sin divergencia ni reintentos. Los controles COORDS_ON se reutilizaron con comprobación exacta de inputs, targets, pesos iniciales, modelo/optimizer/presupuesto y calendario. COORDS_OFF dio train 1.0 en ambas seeds y validation .875/1.0 frente a .75/.75 de COORDS_ON. BCE de validación: .377215/.000588 frente a 1.558116/1.670898. **No pasa la puerta conjunta ≥.98** porque seed2101 conserva dos errores en destino20; no se escoge seed2102 ni se prolonga entrenamiento.

En seed2101, destino20 responde siempre 0 y destinos21/26/61 seleccionan b0 en los cuatro patrones. Seed2102 selecciona b0 correctamente en los cuatro destinos. Los flips de fuente0 cambian clase en .75/1.0 y los de fuente1 en 0/0. Se eliminó exclusivamente información absoluta del encoder: distancias y conectividad permanecen. El resultado es compatible con mejor condicionamiento/simetría y menor dependencia del contexto, pero no identifica memorización como causa única ni una ventaja MHU. El factor queda cerrado bajo este presupuesto; las extensiones **XOR/MHU/remoto siguen NOT_RUN**, sin test ni actualización de H1–H6.

Identidad congelada `00bba94bd0208fb164f89b8fed14b71bbb34635d114edbbc70acc344aaf23376`; manifest/resultados/checkpoints en `artifacts/role_generalization/v1`. Informe con limitaciones y figuras: [ROLE_GENERALIZATION.md](C:/Programación/LARP/docs/ROLE_GENERALIZATION.md). Dos tests de copia/ablación y preflight aprobaron en1.65s. Se conserva el protocolo anterior y su regla de parada.

## 2. Baselines de adquisición

Resultado actualizado: **576/576 condiciones completas**, Grid3/3 admitida con100.000 propuestas completas por seed en primer intento. Calibración previa sin MSE y verificación exacta de216 celdas reutilizadas. El ranking depende del decoder: aviar gana interpolación local y Grid gana oracle fine con ruido. Véase [SAMPLING_GRID_RESULTS.md](C:/Programación/LARP/docs/SAMPLING_GRID_RESULTS.md). Las decisiones previas se conservan debajo.

Seguir [SAMPLING_GRID_SUPPLEMENT_PROTOCOL.md](C:/Programación/LARP/docs/SAMPLING_GRID_SUPPLEMENT_PROTOCOL.md) para construcción Grid balanceada y dos estratos de queries. Calibración de tiempo sin MSE; no reducir el baseline a una coloración rápida presentada como equivalente. Conservar candidatos fallidos y su estado aproximado. Una rejilla constante con distintas coloraciones no proporciona coordenadas independientes.

Incluir los dos estimadores locales y el oracle-band ya fijados. El oracle requiere información global de banda/ruido y comunicación de todas las observaciones del canal; declarar ese acceso y coste. NN/kernel son decoders locales baratos con información distinta. No presentar la precisión de un decoder global como comparación neuronal con presupuesto de comunicaciones igualado.

Para extender el protocolo previo: añadir el oracle a cada celda compartida da 576 celdas únicas en total (4familias×3realizaciones×2marcas×3estimadores×2bandas×2ruidos×2queries), contando los estratos previos como datos reutilizados. Congelar esa ampliación antes de evaluar Grid/queries nuevas; conservar la evaluación local original como registro. Construcción y evaluación tienen presupuestos separados. Si la calibración no garantiza el techo de construcción, dejar la tanda pendiente en vez de omitir un rival lento.

Criterio descriptivo: informar todas las bandas/ruidos/queries/estimadores y diferencias por realización. Si Grid/HU-unión igualan o superan la candidata, restringir la utilidad aviar a las condiciones donde efectivamente aparece. Una ganancia local que desaparece con oracle apoya conveniencia de decoder, no superioridad universal de información adquirida.

## 3. Condiciones para una comparación neuronal nueva

No abrir T/F, robustez ni escalado antes de contar con un núcleo que seleccione roles y aprenda el smoke bajo una versión congelada. Evaluar el nuevo núcleo en **ambos** sustratos con presupuesto/HPO común; conservar todos los fallos y el cambio de encoder/update como factor declarado.

Para atribuir multicomponente, native/shuffle debe compartir X/E/puertos/datos/optimizer/init. Para distinguir adquisición y procesamiento, targets permanecen en el mundo externo y se cruzan sensores distribuidos con observaciones igualadas. Medir si T/F realmente aprenden funciones diferentes; nombres de conos no acreditan especialistas.

El contraste full/local es una intervención sobre el objetivo del generador y cambia microestructura. Antes de una afirmación específica de ondas largas se necesita un control que iguale estadísticas locales y un protocolo de matching congelado. Antes de afirmar desorden/asintótica, revisar picos por población y su estabilidad con N; el pico E=.474 actual obliga a cautela.

H1–H6 y C siguen sin actualizar. Confirmación requiere resolver los bloqueos pertinentes de [SPEC_AUDIT.md](C:/Programación/LARP/docs/SPEC_AUDIT.md), panel independiente, rival fuerte y likelihood apropiada. Los nuevos diagnósticos no autorizan Bayes factors arquitectónicos ni selección retrospectiva de resultados.
