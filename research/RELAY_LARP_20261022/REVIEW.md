# Revisión de la asesoría delegada

## Primera respuesta: transporte y optimización

El relay completó el envío y la recogida real del primer encargo. La respuesta original declaró 16.390 caracteres y el retorno se truncó a 8.500. **No se acepta como informe íntegro ni se atribuye una recomendación final a la parte ausente.** Se conservan el recibo, el UUID y el enlace de la conversación; no se reenvía la consulta.

En la porción recibida se comprueban contra la derivación independiente:

- Igualdad funcional de los frontends de rango completo con píxeles a igual ancho, y limitación de C10 frente al presupuesto histórico de C04.
- SGD sobre sensores induce el precondicionador M Mᵀ en coordenadas de píxel.
- L2 clásica sobre sensores induce, al minimizar sobre parametrizaciones redundantes, una penalización anisótropa tr(Bᵀ(M Mᵀ)⁻¹B).
- Weight decay desacoplado de AdamW se transporta como contracción de B, pero no equivale automáticamente a esa penalización L2. Los momentos adaptativos dependen de la base y de su historia. La matriz diagonal del segundo momento debe entenderse **por unidad oculta**, no como un único precondicionador 64×64 compartido por todas las columnas.
- El entrenamiento finito no rompe la equivalencia entre SGD sensorial y SGD de píxeles correctamente precondicionado; sí impide asumir igualdad con SGD ordinario.

Son consecuencias algebraicas condicionales y asesoría sobre diseño, no nuevas mediciones, anterioridad verificada, confirmación de MHU ni actualización numérica de H1–H6. Sigue siendo necesaria la cautela de clipping y de normalización descrita en INDEPENDENT_CHECK.md.

## Segundo encargo

Pendiente de recogida y revisión. Se eligió como revisión independiente de decisiones, no como repetición para obtener una respuesta favorable.

## Recuperación parcial del tramo omitido, sin reenviar

Se leyó mediante la UI de la conversación existente el tramo de las secciones 4–5, ya terminado. La respuesta propone trasladar K a una MLP de píxeles con SGD sin decay; normalizar por el autovalor máximo; comparar dos geometrías MHU y dos CVT con dos inicializaciones y control identidad (diez entrenamientos); medir pérdida de entrenamiento acumulada, excluyendo el test reutilizado. Plantea un umbral operativo del 5%, explícitamente no inferencial. No se reconstruye ni se altera el texto truncado recibido por MCP.

Revisión propia: este experimento identifica efectos de esas matrices bajo ese SGD, no supresión espectral MHU ni el mecanismo completo de C04 con AdamW. El umbral del 5% es una propuesta sin justificación de utilidad/potencia y no se adopta automáticamente. Identidad es un control mínimo, no un precondicionador convencional fuerte; antes de correr debería incluirse una alternativa basada en covarianza de entrenamiento, con regularización fijada sin test. La selección de geometrías debe fijarse sin mirar rendimiento. Esta propuesta aún no es un protocolo aprobado ni un ciclo ejecutado.

## Lección operativa provisional

Una respuesta larga puede exceder el límite explícito pedido por el prompt y quedar cortada correctamente por el relay. Los próximos encargos deberán situar el dictamen y protocolo al principio y dejar margen de caracteres para fórmulas y formato. Esta observación no acredita ahorro de créditos ni fiabilidad general de la integración.
