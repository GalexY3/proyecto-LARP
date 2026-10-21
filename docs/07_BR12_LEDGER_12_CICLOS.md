# LARP — AB 3.2.1 | BR12 dinámico (12 decisiones documentadas)

**Fecha:** 21-10-2026. **Autorización:** 12 ciclos y hasta 12 más condicionados a necesidad. **Estado:** 12 preguntas sustantivas evaluadas, 12 decisiones; las ampliaciones no utilizadas. Un ciclo aquí es pregunta + contraste/auditoría + decisión que orienta el siguiente, NO una semilla/valor de k. Se conservan errores y desviaciones del plan. **Todos los ensayos numéricos nuevos son exploratorios**, aunque algunos usan mundos nuevos después de ajustar en desarrollo; no hay registro confirmatorio previo específico que permita reclamar confirmación externa.

**Ojo:** la cronología corresponde a sucesivas decisiones durante esta sesión; los scripts de C04–C12 se añadieron tras observar pruebas previas. Sólo el código inicial `src/dynamic_research.py` fue subido a GitHub *antes* de la primera comparación nueva. No hay continuidad de optimizador entre LOCAL_derived (N512) y LOCAL_original (N4096). Se conserva explícitamente el código de cada brazo en el paquete.

## Convención A-J
A = pregunta/unidad, B = hipótesis rivales, C = protocolo/predecisión, D = instrumentación, E = medida, F = falsadores, G = confirmación, H = actualización cualitativa, I = dictamen/alcance, J = decisión y siguiente pregunta. No se han abierto 12 holdouts independientes. Parar si no existe ganancia informativa.

## C01 | Prior art
**A — Pregunta:** ¿Es nueva la disponibilidad local de múltiples clases y qué baseline es genuino?
**B — Rivales / D — Instrumentación:** H_nueva: propiedad única de LOCAL; H_W: multi-class blue noise preexistente. Evidencia fuerte a favor de H_W.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** Wei 2010 ya define sampling multiclase en dimensiones arbitrarias, con código original; avian-patterns-lab es 2D y pequeño. No se ejecuta el código original Wei aquí.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **PIVOT**. **Siguiente ciclo decidido a partir de esta evidencia:** Inspeccionar realizaciones independientes y evitar usar nombre Wei para un control propio.

## C02 | Replicación geométrica
**A — Pregunta:** ¿Podemos generar patrones independientes y no depender de una sola geometría?
**B — Rivales / D — Instrumentación:** H: se pueden generar geometrías comparables; H_alt: extrapolación entre implementaciones. Limitación: reconstrucción no es réplica algorítmica.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** 12 semillas independientes × cuatro procedimientos con N=512 y cinco tipos, cuotas [209,109,87,64,43]. LOCAL_derived sólo implementa una repulsión local inspirada, no el optimizador original de Scale3D.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **REPAIR**. **Siguiente ciclo decidido a partir de esta evidencia:** Medir cobertura con CVT por tipo y no adjudicarle resultados al LOCAL original.

## C03 | Cobertura independiente
**A — Pregunta:** ¿LOCAL derivado conserva la ventaja ante un baseline espacial robusto?
**B — Rivales / D — Instrumentación:** H_LOCAL, H_CVT, H_null. Conclusión dependiente de versión LOCAL_derived y N512; no refuta Scale3D original.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** Con 16 vecinos y 12 geometrías nuevas: IID 61.43%, stratified 77.41%, LOCAL_derived 69.17%, CVT per-type 97.31%. CVT domina en esta implementación.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **PIVOT**. **Siguiente ciclo decidido a partir de esta evidencia:** Revisar N4096 con coordenadas auténticas, no extender conclusión al original.

## C04 | Escala original 4096
**A — Pregunta:** ¿CVT puede rivalizar con las coordenadas LOCAL originales al mismo N y cuotas?
**B — Rivales / D — Instrumentación:** H_cobertura_L > CVT; H_CVT≈L; H_seeds. Requiere convergencia del comparador antes de discriminar.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** N4096: ORIGINAL_LOCAL cobertura k16=96.08%, MHU=95.28%; seis CVT con 8 iter. cobertura k16 entre 94.72% y 96.52%. Solo una LOCAL original.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **REPAIR**. **Siguiente ciclo decidido a partir de esta evidencia:** Aumentar iteraciones CVT; no interpretar una línea base suboptimizada como victoria.

## C05 | Convergencia de baseline
**A — Pregunta:** ¿Optimizar CVT altera la comparación?
**B — Rivales / D — Instrumentación:** H_LOCAL persistentemente mejor; H_competidor subentrenado. Se debilita H_LOCAL. Sin Wei todavía.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** Con 15 iteraciones adicionales en tres CVT independientes: cobertura k16=97.64%, 97.68%, 97.56% > LOCAL original 96.08% (consulta común; no inferencia entre generadores LOCAL).
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **PIVOT**. **Siguiente ciclo decidido a partir de esta evidencia:** Examinar efecto en MSE real, no solo cobertura kNN.

## C06 | Reconstrucción con kernel fijo
**A — Pregunta:** ¿La ventaja inicial LOCAL sobre CVT persiste en una tarea multicanal?
**B — Rivales / D — Instrumentación:** H_LOCAL funcional; H_parametrización kernel; H_CVT por optimizar. El estimador conoce los tipos y la fórmula objetivo.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** f1,k24,bandwidth=.11: LOCAL original MSE=.14040; CVT seis geometrías no refinadas media=.15424; RANDOM .39909; MHU=.15709. Ventaja descriptiva LOCAL sobre CVT suboptimizado (~9%).
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **CONTINUE**. **Siguiente ciclo decidido a partir de esta evidencia:** Variar la suavidad antes de atribuir un mecanismo universal.

## C07 | Escala de señal
**A — Pregunta:** ¿La ventaja se extiende a señales espaciales de frecuencia media o alta?
**B — Rivales / D — Instrumentación:** H_suavidad condiciona ventaja vs H_geometría universal. La diferencia cambia con frecuencia. Diseño exploratorio.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** Con kernel fijo y f5,k16: CVT seis geoms media 2.4708 < LOCAL 2.5151; f2,k24 CVT media .9692 vs LOCAL .9658 prácticamente empate. Los MSE altos indican error considerable en frecuencia 5.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **PIVOT**. **Siguiente ciclo decidido a partir de esta evidencia:** Optimizar bandwidth con desarrollo y aplicar a mundos retenidos por método.

## C08 | Control de estimador
**A — Pregunta:** ¿La pequeña ventaja LOCAL sobre CVT era artefacto de bandwidth?
**B — Rivales / D — Instrumentación:** H_LOCAL mejor a estimador comparable; H_CVT mejor con tuning justo; H_nula. La ventaja LOCAL NO sobrevive este control.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** Bandwidth elegido individualmente por mínima MSE en ocho mundos dev; doce mundos heldout: f1 LOCAL=.1074, CVT refinados .0893–.0922, MHU=.1181; f2 LOCAL=.7274, CVT refinados .6945–.7167. Un MSE condicionado al generador, no generalización externa.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **STOP (superioridad geométrica)**. **Siguiente ciclo decidido a partir de esta evidencia:** Comprobar si acceso semánticamente tipado proporciona una vía independiente de la geometría.

## C09 | Acceso por tipo
**A — Pregunta:** ¿Elegir vecinos expresamente por tipo mejora la tarea con presupuesto de señales reducido?
**B — Rivales / D — Instrumentación:** H_estratificar siempre es mejor; H_varianza por 1 muestra/tipo; resultados niegan H_estratificar en esta configuración.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** Con f1: acceso global k16 LOCAL MSE=.1142; oráculo 1 por tipo (5 lecturas) LOCAL=.3160; CVT refinados global ~.095–.100, oráculo ~.306–.318. Buscar 5 árboles no equivale a coste global; ventaja de asegurar tipos no compensa pérdida de redundancia al interpolar.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **STOP (oráculo de 1 por tipo)**. **Siguiente ciclo decidido a partir de esta evidencia:** Si cobertura no basta, probar composición aprendida en vez de fórmula incorporada.

## C10 | Composición aprendida
**A — Pregunta:** ¿Cinco especialistas aprendidos cambian ranking de geometrías?
**B — Rivales / D — Instrumentación:** H_LOCAL neural; H_CVT + representación 5 canales; H_sesgo. Modelo no es Scale3D GNN ni Transformer; datos Fourier sintéticos.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** MLP 5→48→48→1 (3 inicializaciones) entrenado en mundos distintos: MSE test LOCAL=.1478; CVT refinados .1249–.1319; MHU=.1608; RANDOM=.5298. Interpolación con composición analítica sobre mismos campos supera al MLP.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **STOP (claim LARP > CVT)**. **Siguiente ciclo decidido a partir de esta evidencia:** Comprobar perturbaciones por pérdida de sensores; beneficio puede depender de densidad.

## C11 | Tolerancia a fallos
**A — Pregunta:** ¿CVT/LOCAL muestran ventajas robustas con dropout de sensores?
**B — Rivales / D — Instrumentación:** H_CVT uniforme; H_beneficio condicionado por disponibilidad. Comparación condicionada a una LOCAL y tres CVT; dropout igualado por índices no exactamente espacial.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** f1,k16,band=.05,12 mundos: al 0% LOCAL=.1294, CVT refinados .0993–.1059; al 60% LOCAL=.5311, MHU=.4742 y CVT refinados ~.498; todas empeoran. Ningún vencedor uniforme al borrar 60%.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **PIVOT**. **Siguiente ciclo decidido a partir de esta evidencia:** Verificar si el rasgo espectral definitorio MHU conserva valor diferenciado, sin confundirlo con reducción de MSE.

## C12 | Auditoría espectral y cierre
**A — Pregunta:** ¿La supresión espectral MHU es el factor necesario para la ventaja funcional?
**B — Rivales / D — Instrumentación:** H_espectro global necesario para predicción suave; H_cobertura y precisión local son suficientes en esta tarea. Se debilita necesidad de la penalización espectral.
**C — Estado de protocolo:** pivote adaptativo de AB; todos los resultados de C02–C12 exploratorios; scripts adicionales y decisiones surgen tras resultados de ciclos anteriores (no son confirmatorios prerregistrados).
**E — Observación:** Sobre 80 vectores Fourier discretos de norma <=2.5: S_all medio MHU=4.35e-6, LOCAL=.00294, CVT refinado .051–.090, RANDOM=1.16. MHU suprime mucho más; CVT refinado predice mejor las señales suaves. No hay demostración asintótica de HU.
**F — Auditor adversarial:** un resultado específico del generador y comparador no demuestra novedad; comprobar las equivalencias y falta de independencia geométrica.
**G — Confirmación:** NO confirmación externa ni acceso a generadores originales repetidos; pruebas de generalización son mundos sintéticos del mismo generador.
**H — Actualización de creencias:** se debilitan o condicionan las hipótesis destacadas; sin posterior numérico justificado.
**I — Alcance:** hallazgo exploratorio de geometría/estimación sintética, no una medición de arquitectura GPT ni una muestra biológica.
**J — AB-DECIDE:** **STOP (línea concreta); sin extensión automática**. **Siguiente ciclo decidido a partir de esta evidencia:** Cerrar 12/12; +12 autorizados NO activados por falta de nuevo comparador genuino Wei, nuevas LOCAL originales y validación externa.

## Dictamen acumulativo
LOCAL y MHU muestran cobertura funcional alta frente a iid y estratificado simple. Un CVT per-type convencional, cuando se refina y optimiza el interpolador con datos de desarrollo separados, iguala o supera en tareas suaves al LOCAL original fijo en los casos medidos. Esto **NO prueba** que el optimizador LOCAL original sea inferior a CVT: solo hay una realización original; el estimando entre generadores está sin identificar. La supresión espectral de MHU sobre modos finitos está observada, pero no es necesaria para la ventaja predictiva en este simulador.
Originalidad 2/3 y 3/3: **NO**; no existe validez externa y no se ha ejecutado genuinamente Wei 2010. No hay comparación neuronal Scale3D completa ni con Transformer en este bloque.
Desglose presupuesto: 12/12 iniciales consumidos como decisiones sustantivas; los 12 adicionales quedan disponibles en la autorización del usuario, pero no se activan por ausencia de nueva clase de evidencia o comparador sin implementar. Escalar sólo con el código original repetible LOCAL y baseline Wei correcto, un nuevo dataset externo o GPU para entrenamiento controlado.
## Fuentes y código
- Wei 2010 https://www.liyiwei.org/papers/noise-sig10/ ; código https://github.com/1iyiwei/noise/tree/master/RainbowNoise
- Precedente LARP BR30: https://github.com/GalexY3/proyecto-LARP/blob/main/docs/00_DICTAMEN.md
- Prerregistro dinámico: https://github.com/GalexY3/proyecto-LARP/blob/main/prereg/BR12_DYNAMIC_20261021.md
- El paquete `src/` incluye el código completo, las semillas y el generador derivado; `data/` los cálculos tabulados y las coordenadas de nuevos patrones. Las tres geometrías originales están en el repo previo y se copian al paquete de reproducción.
