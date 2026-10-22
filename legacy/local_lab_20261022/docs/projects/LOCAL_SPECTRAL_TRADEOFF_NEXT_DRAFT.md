# Compromisos locales/espectrales — estrategia contingente

2026-10-09. **DRAFT; no ejecutado ni autorizado por este documento.** Se prepara antes de conocer el resultado de Constrained Mobility Diagnostics. Se activaría para decisión si ambos operadores incumplen su puerta de viabilidad. No modifica esa fase, sus 130 guardas, v2, tolerancias, resultados o hashes históricos. Marco: [AB2.1](../charter/LARP_RESEARCH_CHARTER_AB_2_1.md) y [decisión de movilidad](../decisions/ADR_2026_10_09_CONSTRAINED_MOBILITY.md).

## Pregunta y cambio de alcance

Explorar **qué combinaciones de cobertura local y supresión espectral conseguimos construir**, conservando conteos y sustrato. El objetivo deja de ser encontrar un control perfectamente emparejado: un candidato que incumpla las guardas históricas permanece fuera del contraste residual v2. Publicar sus incumplimientos con los mismos denominadores y tolerancias; no recalibrarlas para admitirlo.

Una comparación de estructuras puede estudiar el **efecto total** de sus diferencias. El contraste residual mantiene determinadas estadísticas casi fijas. Son estimandos distintos. Una ventaja total acompañada de ausencia de ventaja residual no demuestra mediación: también cambian soporte, potencia y propiedades no controladas. Harían falta intervenciones adicionales sobre el mecanismo.

## Objetivos simples y baselines

En el piloto, reutilizar g1101/g1102/g1103 sólo para exploración. Dentro de cada comparación conservar X, E, orden, radios físicos por nodo, centros, conteos y semántica funcional de etiquetas. Sin seleccionar geometrías o tipos por facilidad.

Minimizar dos objetivos dimensionless previamente definidos:

- **Local:** `C=max_c(p95(distancia del centro al tipo c)/a_c)`, con `a_c=L/sqrt(n_c)`. Mide el peor canal de cobertura; no suma métricas correlacionadas.
- **Espectral:** `Q=max_c(mean_K S_c)/0.05`, usando los seis modos históricos. El denominador fijo expresa la escala del certificado finito, no una probabilidad ni propiedad asintótica.

Registrar separadamente CDF, vacíos, varianzas continuas por radio, vecinos homotípicos, anisotropía, cada modo, espectros cruzados y todas las guardas históricas. Un objetivo bajo no sustituye esos controles. Usar el peor canal evita mejorar una media sacrificando silenciosamente una población.

Tres baselines sobre el mismo sustrato: etiquetas **nativas**; **shuffle** de conteos exactos como control de calibración; y **construcción local sin término espectral**, con esfuerzo comparable, orientada a cobertura y vacíos. La construcción local es el rival práctico principal; shuffle no basta como rival fuerte. Comparar coste de construir, no sólo valores finales. No introducir otra geometría bajo el nombre de control sobre X fijo.

Usar una sola familia de construcción/ajuste, elegida antes del piloto, con tres prioridades prefijadas `J_λ=(1−λ)C+λQ`, λ∈{0,0.5,1}. La scalarización produce soluciones alcanzadas; puede omitir regiones no convexas. Publicar todos los puntos, dominados o no. Llamar al subconjunto no dominado **frente alcanzado**, nunca frontera Pareto verdadera sin garantías globales. λ0 y la construcción local pueden compartir algoritmo, pero sus definiciones y restricciones deben declararse para no contar duplicados como métodos independientes.

## Adquisición y redes requieren paneles distintos

El panel de **adquisición** usa disponibilidad espacial de canales y decoders que no consumen E. La mezcla dirigida de tipos de arco no será objetivo de ese panel; sus diferencias seguirán registradas y cualquier incumplimiento impedirá llamar al candidato control v2.

El panel de **redes** usa E y deberá conservar o manipular explícitamente mezcla dirigida, grados y rutas. Una estructura útil para adquisición no justifica ventaja neuronal. No abrirlo mientras no exista un núcleo competente y protocolo propio. No agregar resultados de ambos paneles como evidencia de un mismo mecanismo.

## Antes de gastar recursos

Revisar antecedentes primarios sobre diseño multicomponente, muestreo espacial, hiperuniformidad, optimización multiobjetivo y movimientos que conservan restricciones. Registrar DOI/URL, estatus revisado/preprint, contribución, limitaciones y método reutilizable. Contrastar métodos existentes antes de reclamar originalidad o construir otro optimizador. La revisión actual no establece novedad.

Presupuesto **provisional**, pendiente de decisión y congelación: ≤180s científicos globales, con ≤30s preparación, ≤30s calibración de coste y ≤120s construcción. Plan máximo: tres geometrías × dos RNG nuevos × cuatro condiciones de construcción × ≤5s. Las cuatro condiciones son construcción local y tres prioridades; si λ0 es idéntica al rival, fusionarla y ahorrar el coste. Nativa/shuffle se calculan dentro de preparación. Sin transferencia del presupuesto de movilidad, reintentos o ampliación posterior. El cap se resuelve antes de buscar; si no permite comparar condiciones completas, cerrar por recursos.

## Stop y validación posterior

Un único piloto, sin ajustar λ, objetivos, seeds o tolerancias mirando sus puntos. Parar si falla integridad, termina presupuesto o se completa el plan. Si no añade estructuras útiles respecto de los baselines, cerrar la secuencia de iteradores y documentar el límite; no probar otra colección de optimizadores por inercia. Avanzar sólo con una predicción discriminante sobre un compromiso reproducido en ambas semillas de al menos dos sustratos, o una mejora conjunta auditada sobre el rival local.

El piloto no usa MSE, tareas o redes para seleccionar estructuras. Después, un protocolo separado preregistrará **nuevas realizaciones geométricas**, seeds, campos/queries, ruido común y decoders locales más un estimador espectral fuerte. Congelar selección antes de scores; evaluar también construcción y coste. Conservar resultados adversos y limitar inferencias al tamaño, modos y generador comprobados: N400 y seis modos sólo acreditan propiedades finitas, no el límite k→0.

Registro AB: hipótesis nuevas exploratorias; sin actualización automática de utilidad MHU o priors arquitectónicos. Pivote científico, ejecución y evaluación posterior requieren decisiones propias. Este borrador conserva la línea residual como pregunta histórica abierta.
