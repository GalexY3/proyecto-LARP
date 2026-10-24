# AB30 O4 — 30 ciclos AB con CT2 1–100, niveles 0–3 y reparación visible

**Estado:** 30 ciclos **REPARADOS-EXPLORATORIOS** Q01–Q30 completados (seis poblaciones observadas × cinco familias de hipótesis). CT2 de esta línea 18→15/100. Hallazgos únicos **1/3: 2**, 2/3: 0, 3/3: 0. No inferir confianza=probabilidad.

## Entrar aquí
- [Dictamen R1 válido](reports/DICTAMEN_R1.md)
- [Resultados numéricos de los 30 ciclos R1](results/RESULTS_R1_30_ROUNDED.json), con fase E (presupuestos 10,14,18) y G (26,34).
- [Priors acumulativos nuevos](reports/PRIORS_APPEND_R1.md).
- [Prerregistros originales B01–B05](prereg/), [reparación R1](prereg/REPAIR_R1_SOURCE.md) y [código fuente reconstruible con SHA](src/reconstruct.py).
- [Fuente académica de referencia](https://www.census.gov/library/working-papers/2014/adrm/rrs2014-07.html): ya existían métodos de asignación entera exacta.

## Incidencia no negociable
Un pretest local B01 de seis fuentes salió antes de congelar contratos y NO cuenta. Además, 30 pruebas ejecutadas con el motor inicial v1 estaban **mal etiquetadas** como Hamilton: resultados INVALID, preservados en el ZIP. Los [informes antiguos B01–B04](reports/) están expresamente marcados inválidos. El código corregido R1 SHA256 `ad330115b84f9e47b8d0372c8d3b6222ae5c34b916b0d364d9a34b82c7449b14` y el cambio exacto fueron versionados ANTES del replay de 30. Como se vieron las salidas originales, R1 es **exploratorio post-exposición**, no confirmación preregistrada ciega.

## Reproducción y faltantes
El archivo local `LARP_AB30_O4_20261024.zip` contiene **27 entradas** con código editable, todas las entradas de datos por presupuesto, resultados v1 inválidos, A–J íntegro (92.710 bytes), auditoría, priors, figura, archivo de hashes y dependencias. SHA256 ZIP `25f1918c9d5991f2684bce4ac9601d2b489b0382c15d84ebc8cc44a8a844259f`. Desde una extracción nueva, los cinco resultados B01–B05 de R1 se reprodujeron **byte a byte** bajo el mismo entorno. No hubo clon GitHub limpio ni replicación científica externa.

**Deuda O3:** los JSON brutos y A–J extensos siguen en el ZIP de la conversación y **no están todavía subidos íntegros a GitHub**. Un merge a main podría conservar el expediente pero no debe declararse cumplimiento documental total ni 2/3. Mantener PR draft hasta recuperar esos brutos con identidad SHA.

**Regla de usuario:** se completaron obligatoriamente 30 con cuatro cambios de rama, sin STOP. No se aumentó N1 por repetir una idea en seis fuentes.
