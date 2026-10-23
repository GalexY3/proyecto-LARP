# LARP — laboratorio de investigación

**Estado (23 de octubre de 2026):** programa exploratorio abierto. La hipótesis inicial MHU (multihiperuniformidad) **no tiene una ventaja computacional específica confirmada**. Tras varios contrastes adversariales, el programa permite DRIFT hacia selección de información, decisiones bajo incertidumbre y monitorización del riesgo. No se ha acreditado ningún descubrimiento interno de nivel 2/3.

## Empezar aquí

1. **[Índice de investigaciones y estado de cada campaña](research/INDEX.md)**. Distingue evidencia integrada, trabajos pendientes y ramas históricas.
2. **[Política de integración, trazabilidad y reproducibilidad](docs/INTEGRACION_Y_REPRODUCIBILIDAD.md)**. Fusionar archivos exploratorios no los convierte en conclusiones confirmadas.
3. **[Priors acumulativos originales](docs/02_PRIORS_LARP.md)**. Conservar también apéndices de cada campaña y evidencia contraria; no sustituir este ledger en un merge de rama divergente.
4. **[Metodología AB 3.2.1, anexos O1/O2/O3](https://github.com/GalexY3/Metodologia-AB)**. O3 incorpora bucles DRIFT, branching y pivot; su eficacia metodológica sigue sin validación externa.

## Evidencia destacada

**Observaciones físicas, no simulación:** [Beijing Multi-Site Air Quality](research/AB45_BEIJING_20261022/DICTAMEN.md): doce estaciones, series de 2013–2017, 45 condiciones adaptativas de validación y una única prueba cronológica de 39 semanas. Se comprobó que `COSI_PROXY` no era el mecanismo COSI/MHU original; **no** se atribuyó eficacia al mecanismo. El test está consumido y no es replicación externa multinacional.

**Auditoría geométrica y de aprendizaje:** [AB30 INTENSIVE](research/AB30_INTENSIVE_20261022/reports/DICTAMEN.md) y [AB30 DISCOVERY](research/AB30_DISCOVERY_20261022/reports/DICTAMEN.md). Exploran geometrías, espectro por tipos, reconstrucción, Digits y rivales. No hay certificación de multihiperuniformidad asintótica ni replicación independiente.

**Histórico de 2026-10-21 y 2026-10-22:** [BR30](docs/00_DICTAMEN.md), [ledger A–J](docs/01_LEDGER_30_CICLOS.md), [AB30 CODEX](research/AB30_CODEX_20261022/REPORT.md), [importación de 539 archivos locales](legacy/local_lab_20261022/README_IMPORT.md) y [ChatRelay adversarial](research/RELAY_LARP_20261022/README.md). Las 10 ejecuciones del bloque CODEX no equivalen a los 30 contrastes de campañas posteriores.

## Reglas de interpretación y próximos pasos
- Los datasets reales públicos no equivalen a un despliegue experimental; múltiples seeds del mismo generador no son réplicas externas.
- Mantener código y preregs vinculados a commits, JSON brutos, fallos, reparación, costes y pruebas de clon limpio. Etiquetar ausencias; no inventar `freeze-run` remoto.
- Pendientes de integración: PR [#8](https://github.com/GalexY3/proyecto-LARP/pull/8) y [#9](https://github.com/GalexY3/proyecto-LARP/pull/9), con expedientes brutos en ZIP fuera del repositorio. La cadena antigua de PR #1–#5 requiere trasplantes selectivos, no merge indiscriminado.

Repositorios privados: [LARP](https://github.com/GalexY3/proyecto-LARP) y [Metodología AB](https://github.com/GalexY3/Metodologia-AB). Este README es índice; los informes científicos conservan sus reivindicaciones y límites originales.
