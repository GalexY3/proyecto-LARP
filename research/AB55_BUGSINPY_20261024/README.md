# LARP AB55 — BugsInPy, planificación intensiva y DRIFT

**Fecha:** 24-10-2026. **Estado:** archivo de 50 auditorías documentales A–J y cinco planes AB A–J. Las pruebas de detección dinámica originalmente deseadas **NO SE EJECUTARON**, porque no se creó un entorno histórico verificado para Python 3.6–3.8. No confundir "55 expedientes" con "55 experimentos reales".

## Entrada rápida
- [Dictamen científico honesto](reports/DICTAMEN.md)
- [Prerregistro original (20+5+30)](prereg/CAMPAIGN_55.json)
- [Contrato de extracción/estimando](prereg/MEASUREMENT_CONTRACT.md)
- [20 auditorías Q01–Q20](results/Q01_Q05.json), [Q06–Q10](results/Q06_Q10.json), [Q11–Q15](results/Q11_Q15.json), [Q16–Q20](results/Q16_Q20.json)
- [Cinco planes A–J](planning/P01_P05_INTENSIVE_AB.json)
- [30 auditorías X01–X30, por proyecto](results/AGGREGATED_50.json) (cada fila referencia su archivo completo)
- [Errata FastAPI](prereg/REPAIR_R1_FASTAPI_REDIRECT.md), original X07–X12 **inválido**, [resultado corregido](results/X07_X12_FASTAPI_R1.json)
- [Resumen cuantitativo verificable](results/AGGREGATED_50.json)
- [CT2 versionada](reports/CT2_TRAJECTORY.json) y [script Python para ambas gráficas](reports/plot_ct2.py)
- [Priors nuevos y refutaciones](reports/PRIORS_APPEND.md)

## Resultados descriptivos
Cohorte Q: veinte fixes expuestos antes del preregistro formal. Cohorte X: treinta IDs seleccionados antes de consultar bug.info y fixed patches, aunque NO independientes del mismo benchmark.
En la selección total, **50/50** upstream fix commits modifican test files, en **8** proyectos. Mediana de cambios en archivos de implementación Python = **6 líneas** (rango 1–159). No implica 50/50 detección de bugs ni generalidad externa: BugsInPy está curado para disponer de pruebas.
Sin ejecución buggy/fixed, no es posible comparar la eficacia de testing metamórfico frente a controles profesionales.

## Hallazgos y CT2
Nuevo 1/3 = 0. Registro previo auditado = 6 únicos. N2=N3=0. CT2 de línea principal 11→8/100; oportunidad conceptual separada DRIFT D3,7 CT2 12/100, planificación únicamente.
Se necesitan contenedores históricos reproducibles, pruebas cegadas al fix y paridad de coste, por lo que **2/3 NO ACREDITADO**.

## GitHub/AB O6 y próxima decisión
La presentación, CT2, D0–D5, contabilidad 1/3 y solicitud final de 20–45 ciclos se regulan en [AB 3.2.1-O6](https://github.com/GalexY3/Metodologia-AB/blob/main/docs/AB_3_2_1_O6_CAMPANAS_INFORMES_CT2_Y_CICLOS.md) y [AGENTS.md](https://github.com/GalexY3/Metodologia-AB/blob/main/AGENTS.md). Esta campaña sigue íntegramente autorizada sin necesidad de rehacer grants.

Decisión científica: no invertir más ciclos solo en inspeccionar metadatos. Prioridad para próxima autorización: **20 ciclos AB de PIVOT instrumental** a reproducir defectos y medir métodos de testing realmente ejecutados, si se habilita el entorno histórico. No confundir trabajo ejecutado sobre GitHub con pruebas de software ejecutadas en Python.
