# Decisión: ejecutar el contraste de orientación y evaluar expansión

Fecha: 8 de octubre de 2026. Autorización: el investigador respondió al borrador de fase 4 con «Okay» y «De todas formas, sigamos adelante», solicitando también evaluar escalado, 3D MHU y multicapa estilo transformer. Se conserva la autorización y los límites del trabajo científico ya acordados; no se pide de nuevo aprobación para implementar y ejecutar este contraste concreto.

Se adopta para esta ejecución la recomendación B/D8 de [ROLE_ORIENTATION_PHASE4_DRAFT.md](../projects/ROLE_ORIENTATION_PHASE4_DRAFT.md): misma Grid, doce slots físicos y sus multiplicidades, una orientación cambiada, cuatro parejas SS inéditas con soporte común en ambos roles y cuatro queries comunes con UU. La fuente de datos/contextos es el manifest de fase 3; sus archivos permanecen intactos. El borrador histórico conserva su estado original de propuesta; la configuración y manifest nuevos gobiernan la ejecución.

Modelo: GGNNLikeModel/COORDS_OFF sin cambios, 12.481 parámetros, d32/T16, B4, 250 updates, AdamW .003, CPU4/float32. Inicializaciones nuevas2103/2104; calendarios anteriores2101/2102 respectivamente. Orden D8/2103, B/2103, B/2104, D8/2104. Cuatro corridas como máximo, **120 segundos globales duros incluyendo imports**, sin reintentos, extensiones o elección de checkpoint. Es una etapa exploratoria registrada antes de sus resultados, no confirmación de una arquitectura MHU.

El candidato primario B debe superar train/SS/UU finales≥98% en ambas semillas. La preparación admite duplicados orientados de D8: doce slots y 48 casos, once triples orientados únicos. No deduplicar ni exigir el guard histórico de doce triples únicos. La orientación identifica un tratamiento que incluye soporte por rol y diversidad de contextos marcados; no aislar el escalar de desequilibrio como mediador único.

La disposición para proponer después XOR requiere además AUX_OLD≥98% en ambas semillas B, incluido el desafío conocido61. Es un guard prospectivo nuevo, sin endurecer retrospectivamente fase 3. Ninguna puerta positiva ejecuta XOR automáticamente. Un fallo cierra esta intervención sin prolongarla.

Se registra **H-R4** antes de optimizar en `configs/role_orientation_hypotheses_v1.json`. Su predicción es una ventaja UU material concordante; las reglas ordinales de apoyo/contraevidencia quedan fijadas, incluyendo el caso de igual techo como contraevidencia débil de esa ventaja específica. Este supuesto nuevo no reinterpreta H-R1–H-R3 ni usa fase 3 como confirmación independiente. Datos derivados de accuracy/flips/BCE forman un solo paquete. H1–H6/C permanecen inalterados.

En paralelo se revisan literatura y diseños de 3D/multicapa/escalado. No se cambia objetivo general ni se adopta una nueva arquitectura por esta revisión. La comparación espectral con estadísticas locales emparejadas mantiene su propio estimando, protocolo y presupuesto; no queda bloqueada por el diagnóstico neuronal.

Antes de entrenar: código/config/hipótesis/decisión, datasets, calendario, pesos iniciales y runtime congelados; tests de soporte, duplicados y límites; auditoría antes de la señal de ejecución. Después: conservar todas las corridas y fallos, verificar bytes históricos y estados individuales, registrar costos y actualización H-R4 aparte. No usar el resumen permisivo de fase 3 ni sobrescribirlo.
