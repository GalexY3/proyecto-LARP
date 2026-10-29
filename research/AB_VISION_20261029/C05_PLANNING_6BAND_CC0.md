# C05 / PLANIFICACIÓN AB A–J — evidencia nueva: capturas ópticas de 6 bandas independientes
Fecha: 2026-10-29. `PLANNING_AB_ONLY`. NO consume ciclo experimental del cupo (18 disponibles tras C04). No se han descargado las imágenes multiespectrales ni ejecutado el comparador Wei.

## A — Pregunta y estimando
¿Puede la coordinación espacial de cinco subtipos MHU (vs optimización por tipo y Wei original) permitir recuperar cinco bandas medidas ópticamente, bajo mismo número de lecturas por modalidad, con menor error fuera de muestra, ruido y fallos de sensor? Unidad independiente primaria = captura completa / bloque de terreno y sesión, NO parches repetidos o semillas; controlar correlación por mismo vuelo y misma zona. Outcome: MSE/PSNR de bandas originales, con orientación geométrica y calibración correctas; coste real de muestreo computacional como medida secundaria.

## B — Hipótesis rivales
H1 ventaja de coordinación entre tipos por interacción espacial de espectros. H0 la cobertura individual basta, no contribución cruzada. H2 patrones tipo Wei2010 y farthest-first/Poisson disk igualan o superan MHU. H3 más ventaja viene de un decoder aprendido y/o de la selección adaptativa de bandas que de topología fija. Evitar diseño que use el test al elegir sensor.

## C — FUENTE NUEVA, LEGAL Y CIENTÍFICAMENTE DIFERENTE
- `idt-fhac/odm_data_buergewald` en GitHub, README y **LICENSE CC0 verificados directamente** con conector GitHub el 2026-10-29. 735 capturas completas de cámara MicaSense RedEdge-P, 4410 archivos geotiff, **6 bandas medidas** (azul, verde, rojo, infrarrojo cercano, borde rojo, pancromática), resolución 1456×1088; volumen ~17.8 GB. Distinto de CAVE y distinto de filtros RGB sintéticos de C02. GitHub: https://github.com/idt-fhac/odm_data_buergewald, licencia https://github.com/idt-fhac/odm_data_buergewald/blob/main/LICENSE.
- Se propone elegir 12 capturas enteras con identificadores SHA de hash de ruta (fijar lista antes de outcomes) y usar pares de adquisición para asegurar bandas completas. No seleccionar escenas por efecto favorable. **Peligro importante**: distintas bandas pueden estar desalineadas geométricamente / con radiometría no calibrada; estas diferencias NO son efecto MHU. La pancromática tiene respuesta distinta, por tanto cinco de seis bandas deberían priorizarse (Blue,Green,Red,NIR,RedEdge), y Panchro queda en análisis secundario.
- CAVE (32 escenas × 31 bandas) sigue candidato para un segundo dataset verdaderamente distinto: https://cave.cs.columbia.edu/repository/Multispectral . NO asumir permiso para redistribuir archivos CAVE sin licencia verificada. Comparaciones de CAVE con dataset de dron no deben equipararse por iluminación/superficie/objetivo.
- Para reproducibilidad, datos fuente permanecen externos. Guardar SHA256 de cada banda, metadata exposición/banda, software de registro/calibración, recortes de región compartida, escena y hash; solo derivados permitidos.

## D — Gate instrumental verificable
1. Descarga con un ejecutor con acceso de red: **NO realizada en esta sesión**, contenedor sin resolución DNS; GitHub conector de Chat no descarga blobs PNG/TIFF (probado, UnicodeDecodeError). No aceptar términos nuevos ni suscripciones.
2. Registro y alineación por imagen/metadata controlando paralaje; obtener comprobación visual y residual pixel; no hacer interpolación test dependiente del método.
3. Obtener ejecutable original `RainbowNoise/src/Main/DartThrowing.cpp` de `1iyiwei/noise` y correr/depurar scripts con commit exacto, verificando tasa de clases y densidad, sin renombrar PoissonDisk como Wei auténtico.
4. Solo después de superar gates, congelar en GitHub protocolo+fuente FULL+pre-resultado; preferir escenas test sin exposición previa.

## E — Ejecución eventual
Presupuesto inicial 12 capturas × 3 seeds geométricas × 5 métodos × 3 perturbaciones × 5 bandas, pero ajustar por correlación entre capturas solo antes de registrar contrato. No ejecutar aquí: NO datos original, NO Wei compilado. No consumir plaza ficticia.

## F — Auditoría adversarial
- Fotos del mismo vuelo no equivalen a 12 dominios externos independientes.
- Bandas no registradas generan artefactos de error muy altos, confusión geométrica.
- Mosaico fijo no implica sensor hardware real ni reducciones energéticas medidas.
- Reproducir Wei vs MHU con cuota, costes, parametrización, inspección de código y control de densidad.
- Benchmark para reconstrucción no demuestra mejora de reconocimiento; para IA debe añadirse después un task downstream real con labels independientes.
- C04 LFW saturó 97% y no discriminó (NO reciclar).

## G — Replicación
Un único entorno (Bürgewald) = consistencia intradataset, **no** replicación externa. CAVE como replicación posterior condicional y dominio distinto; siempre split por captura/sesión, nunca parches del mismo mosaico en train y test.

## H — Priors
P-VIS14: la ausencia de mediciones espectrales físicas era limitación causal de C01/C02/C04; fuente CC0 verificada abre nueva clase de evidencia, **no** confirma ventajas MHU. P-VIS15: registro, calibración y variación entre sensores pueden dominar pequeñas ventajas geométricas; prior de que la medición controla experimentos. Mantener CT2 visión 11/100 hasta un experimento legal, válido y adversarial.

## I — Dictamen
Existencia de una fuente de 6 bandas reales y licencia CC0: **documental verificado**. Datos originales descargados: NO. Prueba de MHU/Wei: NO. N1 nuevo: NO. Grado 2/3: NO. Valor metodológico: concreta vía de confirmación, no descubrimiento.

## J — Decisión / next executor task
`PIVOT_GATE`: priorizar instrumento de acceso y decoder para multibanda con CAVE como external follow-up, sin consumir más ciclos hasta despejar gate. En equipo con red, clonar GitHub CC0, obtener 12 capturas completas según seed hash predefinido, verificar banda/EXIF/calibración/registro, guardar hashes y crear script de lectura y dataset split por captura y bloque; ejecutar Wei2010 original y generar primeras geometrías. Entregar logs y commit SHAs. Una vez proceda, abrir C05 experimental A-J nuevo (ID experimental separado, sin reclamar este planning como ejecución).

**Nota científica:** C05 documental no valida originalidad, no aumenta CT2, no cambia contadores de N1/N2/N3. Por R5 no gastar el cupo artificialmente.
