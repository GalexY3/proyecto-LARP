# Propuesta PIVOT + BRANCHING controlado — LARP (12 ciclos sustantivos)

**Fecha:** 21 de octubre de 2026. **Estado:** PROPUESTA, no ejecución ni prerregistro confirmatorio final. El investigador ha autorizado el PIVOT y ha preguntado cuántos ciclos conceder. **Solicitud: hasta 12 ciclos** con branching condicionado; **no contabilizarlos como consumidos sin autorización explícita de número**. Posible ampliación posterior, máximo tentativo de 6, requiere justificación y nueva aprobación.

## Cambio de estimando
El BR30 mostró que una sola geometría 3D de LOCAL cubre más tipos funcionales en k vecinos que RANDOM y una rejilla estratificada simple, y reduce MSE en el generador Fourier suave con un kernel por tipo. No es evidencia de superioridad general ni del optimizador generador. El primer nuevo estimando debe ser **rendimiento entre geometrías independientes generadas por cada procedimiento** a mismo número de nodos, cuotas y coste comparable. Una vez identificado el efecto geométrico, medir interacción con especialización **aprendida**. El objetivo no es volver a comparar con RANDOM ni buscar confirmación mediante más semillas sobre geometrías fijas.

## Fuentes necesarias/estado de acceso
- `GalexY3/proyecto-LARP`: BR30, 4096 puntos 3D por método, código de prueba y resultados.
- `GalexY3/avian-patterns-lab`: generador abierto con repulsión local vs penalización espectral, **2D, N=120 por defecto**, objetivo O(N²); no es aún generador escalable 3D N=4096.
- Wei (SIGGRAPH 2010): https://www.liyiwei.org/papers/noise-sig10/ ; código original MIT https://github.com/1iyiwei/noise (RainbowNoise); **auditar soporte 3D, cuotas, entornos actuales y licencia antes de llamarlo baseline ejecutable equivalente**.
- Antecedente adicional sensor coverage: https://arxiv.org/abs/2405.09096 ; distinguir multi-cobertura geométrica de reconstrucción de campos.
- Priors LARP sustantivos permanecen separados del observatorio de metodología AB.

## Diseño de 12 ciclos, con decisión individual y *gates*
| Ciclo | Pregunta/nueva evidencia | Falsador/bloqueo |
|---|---|---|
| 01 | Auditoría funcional del código de Wei, avian-patterns-lab y generador LOCAL/MHU; paridad de dimensión/recursos | No es posible ejecutar baseline o regenerar geometrías independientes |
| 02 | Construir 2D/3D generadores con n y cuotas pareadas, al menos 10 geometrías por método si factible | La réplica no conserva configuración o solo funciona en toy distinto |
| 03 | Cobertura multiclase de nuevos patrones (k, radio al quinto tipo, distribuciones), incertidumbre por geometría | LOCAL iguala/pierde contra Wei en presupuesto equivalente |
| 04 | Interpolación/kernel óptimo validado por método (sin retune en test), coste total y riesgo por escala | Ventaja desaparece ante baseline/estimador competente |
| 05 | Descomponer efectos homotípico/intertipo/espectral a cobertura y densidad pareadas | Todo efecto se explica por espaciado convencional |
| 06 | Prueba de límite de comunicación y coste de conexiones, mismo acceso informativo | Ventaja solo surge de permitir canales que otros no reciben |
| 07 | Factorial función×posición×tipo, tareas de suavidad variable, OOD | Las etiquetas funcionales impuestas son toda la ganancia |
| 08 | Falsación con selección adversarial de mundos no geométricos y costes de adquisición | No hay transferibilidad fuera de campos suaves |
| 09 | Reconstruir o adaptar Scale3D original con tests de causalidad e invariancia | No iguala parámetros/FLOPs o fugas de datos |
| 10 | Entrenar ablación LOCAL-homogénea vs LOCAL-especializada y RANDOM-especializada | Diferencia de geometría desaparece en comparación pareada |
| 11 | Incorporar GNN/Set Transformer/PointNet++/MoE cuando existan implementaciones competentes y budget | Sin recursos o baseline válido, **STOP/BARRERA_DE_ACCESO**, no inventar entrenamiento |
| 12 | Validación sobre tareas/dataset fuera del generador y auditoría de originalidad | Solo hay simulación del mismo DGP o se reproduce arte previo |

El bloque de cuatro primeros ciclos es **focalizado**. Los ciclos 5–8 admiten branching SOLO ante mecanismos que superen C04. Los ciclos 9–12 se activan únicamente si existe evidencia de valor incremental y cómputo suficiente. **Se autoriza cambiar la secuencia propuesta en un branching futuro solo anotando decisión, motivo, preguntas originales sustituidas y cambios de multiplicidad**.

## Compromiso de cómputo y rigor
- Una `CONDICION` de una familia (p.ej., otro k) no consume un ciclo AB; un ciclo implica pregunta diferenciada, hipótesis rivales, prueba discriminante, auditoría y AB-DECIDE.
- Como no hay GPU ni acceso garantizado a datos externos, toda barrera se registra como `BARRERA_DE_ACCESO` y puede exigir REPAIR/STOP.
- Separar replicación de **geometrías** y replicación de **mundos de Fourier**. Modelos con n=120 2D no acreditan escala a n=4096 3D.
- Presupuesto por ciclo congelado antes del run, con marco estadístico según número real de afirmaciones, código completo/commit congelado antes del test de confirmación.
- Comparador fuerte Wei 2010; no hacer pasar una implementación simplificada por el algoritmo del autor.
- Cualquier hallazgo nuevo debe actualizar ledger LARP con procedencia y evidencia a favor y contra.
- Si al terminar C04 LOCAL no añade valor sobre la literatura, **STOP**. Si pasa el primer filtro, continuar hasta C08 y re-evaluar. Si C09–C12 requieren GPU ausente, explicar dependencia y solicitar recursos, no afirmar simulación realizada.

## Relación con mejoras de AB
Registro transversal metodológico: https://github.com/GalexY3/Metodologia-AB/blob/main/docs/OBSERVATORIO_AB_MEJORAS_Y_FORTALEZAS.md . No implica actualizar el protocolo AB 3.2.1 ni consolidar nuevas entradas A automáticamente. En este estudio AB-M001/M003/M004/M006 serán los principales puntos de inspección.
