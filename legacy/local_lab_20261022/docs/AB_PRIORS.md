# Priors y actualización abductivo-bayesiana de LARP v0.1

Contrato: review principal D:74–85, L:389–422 y M:424–442. Estado inicial: **UNUPDATED**. Los tests técnicos, certificados, calibración, smoke y selección del piloto no modifican las creencias de arquitectura. Se conserva todo resultado negativo y fallo verificado.

## Dos niveles distintos

| Hipótesis marginal | Prior | Alcance |
|---|---:|---|
| H1 | .70 | Estructura genérica explica la mayor parte del rendimiento |
| H2 | .35 | Cobertura funcional aporta robustez bajo perturbación |
| H3 | .25 | Funciones distintas distribuidas espacialmente añaden utilidad |
| H4 | .75 | Transporte global domina los efectos de organización local |
| H5 | .20 | MHU ayuda como inicialización para plasticidad posterior |
| H6 | .30 | Las restricciones MHU dificultan organización útil |

Son probabilidades **marginales**, pueden coexistir y suman2.55. No se normalizan a uno. H5 permanece sin actualizar hasta plasticidad y warm starts cruzados. La proposición mecanística C tiene prior .25 y requiere el paquete de cobertura efectiva, especialización causal, réplica, control de mixing e intervención funcional descrito en L:422.

La proposición cuantitativa A es diferente: efecto práctico medio nativa−shuffle sobre un endpoint de tarea. Su prior de efecto es simétrico y no favorece MHU. Una posterior de A no es automáticamente una posterior de H3 ni C.

## Modelo cuantitativo preregistrado

Para diferencias de **scores agregados** emparejadas por geometría e inicialización:

$$\Delta_{g,s}=\mu+b_g+\epsilon_{g,s},\quad b_g\sim N(0,\sigma_g^2),\quad\epsilon_{g,s}\sim N(0,\sigma_s^2),$$

$$\mu\sim N(0,.05^2),\qquad\sigma_g,\sigma_s\sim\operatorname{HalfNormal}(.05).$$

`sigma_s` es la variación residual de inicialización dentro de geometría en esta ecuación. No se añade un efecto cruzado común de training seed entre geometrías. Bits, ejemplos, mapas, máscaras y centros de lesión no son réplicas de arquitectura. El bootstrap remuestrea **geometrías completas**, incluyendo sus dos inicializaciones.

ROPE: ±.02. Reportar media/mediana, IC95, `P(mu>.02)`, `P(|mu|≤.02)` y `P(mu<−.02)`. El efecto frente al baseline fuerte es un estimando de arquitectura diferente del contraste de marcas; no exige igualdad de geometría/grafo/puertos, pero sí datos, familia, optimizer, presupuesto y semillas emparejadas.

`src/larp/analysis.py` integra μ y el efecto de geometría analíticamente. A sigmas fijas, la covarianza de cada grupo es `sigma_s² I + sigma_g² 11ᵀ`, y su media tiene varianza `sigma_g²+sigma_s²/S`. Las sigmas se integran por Gauss–Legendre96×96 sobre [1e−6,.25], conservando los determinantes y la densidad de los priors.

Sensibilidad obligatoria:192×192, prior de μ con desviaciones .02 y .10, y extensión del límite superior de sigma a .50 con384×384 nodos para mantener resolución. Se informa la normalización del prior sobre el intervalo numérico: no se presenta el log normalizador como Bayes factor de H1–H6. Una cola previa pequeña fuera de .25 no garantiza una cola posterior pequeña.

Las tolerancias de aproximación computacional son independientes de los criterios científicos: diferencias de probabilidades/media/std≤.001, extremos de IC≤.0001, log normalización≤.01 y masa posterior extendida fuera de .25≤.0001. Si fallan o la sensibilidad cambia la clasificación, la decisión de arquitectura queda inhabilitada; los cálculos descriptivos se conservan.

## Puertas de evidencia implementadas

`infer_paired_effect` y `analyze_paired_effect` aceptan paneles numéricos para validación estadística. Un array carece de identidad de semillas y preregistro, por lo que **nunca acredita por sí solo elegibilidad de arquitectura**.

`analyze_records` comprueba los siguientes requisitos:

1. Una sola tarea/familia y fase `confirmation` o `robustness`, con `preregistered=True`.
2. Un registro por condición/geometría/training seed; panel emparejado completo. Duplicados, máscaras o mapas no se convierten en seeds nuevas.
3. En el contraste `estimand='marks'`, igualdad de hashes de coordenadas, aristas, puertos, datasets train/validation/test, optimizer, budget y pesos iniciales; las marcas deben tener hashes distintos. En `estimand='architecture'`, se declara la otra comparación y se permiten X/E/puertos distintos.
4. COMPLETE requiere `score_split='test'`; confirmación exige además `test_opened=True`. Validación/HPO permanece fuera de la evidencia confirmatoria.
5. TRAINING_DIVERGENCE sólo recibe score de sistema cero cuando `divergence_verified=True` e `infrastructure_excluded=True`. Un fallo numérico sin verificar, infraestructura, run incompleto o implementación inválida bloquea el análisis científico.
6. Listas `expected_geometry_seeds` y `expected_training_seeds`, procedentes del preregistro congelado. Pueden pasarse como argumentos o incorporarse idénticas en todos los registros. Si el panel difiere, se rechaza; si faltan listas, la inferencia queda descriptiva y `architecture_decision_eligible=False`. Confirmación nominal exige8 o16 geometrías y dos inicializaciones.
7. Cuadratura/colas/prior/bootstrap compatibles y ausencia de la frontera singular siguiente. Elegibilidad de un contraste no resuelve por sí sola las condiciones de ambas tareas, baseline fuerte y robustez en M.

## Caso de residuos exactamente cero

Si todas las inicializaciones producen diferencias exactamente iguales dentro de cada geometría, `sum((Delta_gs−mean_g)^2)=0`. En el límite `sigma_s→0`, la likelihood contiene `sigma_s^(-G*(S−1))`, mientras el HalfNormal tiene densidad positiva en cero. Para el panel usual, la posterior continua sin truncación puede ser impropia. Los scores discretos hacen que este caso sea posible.

El límite numérico inferior1e−6 produce un cálculo truncado finito, pero no elimina la ambigüedad sustantiva. La implementación activa `continuous_model_boundary_sensitive=True` e impide decisiones de arquitectura. Resolverlo exige preregistrar un modelo de observación discreto, un ruido de medición o un mínimo sustantivo de sigma; **no se ajusta el modelo para rescatar la conclusión observada**. Véase `B_AB_ZERO_RESIDUAL` en SPEC_AUDIT.

## Historial y actualizaciones cualitativas

`initial_beliefs()` produce un registro persistible con los seis priors/posteriors iguales, estado UNUPDATED y lista de evidencia vacía. `reporting.summarize` lo conserva en sus informes y no realiza actualizaciones automáticas a partir de curvas técnicas.

Cada actualización posterior debe registrar proposición/alcance, prior anterior, evidencia anticipada, todas las seeds/fallos, likelihood o evaluación cualitativa, confounds, mecanismo y siguiente experimento. Para H/C sin likelihood validada se usa grado ordinal: contradice fuerte/débil, neutro, apoya débil/fuerte.

`subjective_hypothesis_update` permite un odds update ilustrativo explícito con LR{.2,.5,1,2,5} y sensibilidad{1/3,2/3,1,1.5,3}. Sus resultados están etiquetados como **elicitudes subjetivas**, nunca Bayes factors estimados. Exige paquete de evidencia identificado en fase confirmatoria/robustez/plasticidad; H5 sólo permite plasticidad. Accuracy, AUC, Jacobiano y cobertura de los mismos runs forman un paquete correlacionado y no se multiplican como evidencia independiente.

Ninguna prueba sintética escrita para verificar estas funciones actualiza un prior de LARP.
