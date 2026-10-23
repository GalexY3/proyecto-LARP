# AB65 FRONTIER — Dictamen de cierre documental (2026-10-24)

## Alcance y recuento

El usuario autorizó 30 ciclos AB experimentales y, si no se acreditaba 2/3/3/3, cinco ciclos AB exclusivamente de planificación y otros 30 experimentales, con branching y pivot libre. La conversación registra la ejecución completa de esa secuencia. La **evidencia remota en este repositorio todavía es parcial**: diez resúmenes de bloque B01–B10, cinco ciclos P01–P05, código comprimido y contratos previos; los resultados numéricos originales por semilla y el ledger íntegro A–J no están versionados aquí.

**Primera ola:** C01–C30, seis fuentes Statsmodels (FAIR, ANES96, RANDHIE, MODECHOICE, GRUNFELD, STAR98), 5 bloques × 6.  
**Planificación:** P01–P05, revisión de novedad, inferencia muestral, potencia/dependencia, no-identificabilidad y selección de fuentes nuevas.  
**Segunda ola:** C31–C60, seis fuentes históricas distintas (Engel, Cancer, Macrodata, Fertility, Sunspots, Scotland), cinco bloques × seis posiciones; cuatro comparaciones sin intervención efectiva fueron invalidadas (C42, C55, C57 y C58). Se prerregistraron reemplazos C61–C64. Solo **C61 tiene un readout individual remoto**; C62–C64 fueron descritos como ejecutados en la conversación, pero sus JSON, estadísticas exactas y auditoría de resultados no están presentes en GitHub. Por eso no declarar aquí «60 ciclos completamente archivados y reproducibles».

## Resultados generales

1. C01–C06: muestreo aleatorio supera muestras deterministas de máxima incertidumbre al estimar error **poblacional**. Es un control deliberadamente débil y un principio de teoría del muestreo ya conocido, **no novedad**.
2. C07–C12: la estratificación proporcional mejora poco e inconsistentemente frente a muestreo aleatorio; varios recontrastes G cambian de signo.
3. C13–C18: asignación idéntica por estrato 20/30/50 frente a asignación proporcional pierde en las seis fuentes; recontrastes G también adversos.
4. C19–C24: Neyman basado en proxy de incertidumbre frente a proporcional ofrece resultados mixtos e inestables. No refuta el óptimo de Neyman con la varianza **verdadera**, que es inaccesible sin conocer las etiquetas.
5. C25–C30: regresión aumentada (AIPW) frente a estimador Neyman con el **mismo conjunto de etiquetas**, sin mejora concluyente en seis fuentes.
6. P01–P05: literatura ya cubre la combinación de muestreo activo, ponderación y monitorización de riesgo; simulaciones de adquisición reusan las mismas poblaciones y no equivalen a muestras independientes. La falta de positividad impide identificar el riesgo global desde etiquetas observadas solo en una región.
7. C31–C36: errores artificialmente localizados en casos confiados producen ventajas y fallos distintos para el proxy Neyman (Cancer adverso; Fertility/Sunspots favorables). **No son eventos naturales observados**.
8. C37–C42: mezcla protegida 50/50 proporcional+Neyman no domina al Neyman puro, con alguna mejora en Cancer; C42 inválido por asignación exactamente idéntica. C61 lo sustituyó por un contraste proporcional vs SRS y mostró mejora local/interna en Scotland (ver readout individual).
9. C43–C48: asignación igualitaria pierde en las seis fuentes bajo errores artificialmente concentrados en casos inciertos; el tamaño de los estratos explica gran parte de la derrota.
10. C49–C54: AIPW con idénticas etiquetas reduce MSE en Engel y Macrodata, pero no uniformemente en las demás fuentes.
11. C55–C60: mezcla 75/25 vs 50/50 no produce ganancia general; C55, C57, C58 **INVALID_NONDISCRIMINATING** por misma asignación entera. C56 revierte el signo entre exploración y G, C59 inconcluso y C60 no discrimina en G. C62–C64 fueron autorizados/prerregistrados y la conversación registra sus resultados cualitativos, pero **faltan sus estadísticas remotas**.

## Evaluación epistemológica

**2/3 = NO ACREDITADO; 3/3 = NO ACREDITADO.** No se encontró una ley nueva ni un método que mejore consistentemente a los controles profesionales en datos independientes. Las ventajas dependen del presupuesto, tamaños de estrato, exactitud del proxy y de **cambios de etiquetas impuestos por el experimento**. Los antecedentes incluyen diseño estratificado/Neyman, estimadores aumentados, métodos de muestreo activo y monitorización predictiva del riesgo. No convertir una demostración sintética sobre observaciones históricas en causalidad de campo.

Cuatro semillas para modelos en cada fase, adquisiciones repetidas anidadas y datos históricos reutilizados: los intervalos por semilla son descriptivos; G solo recontrasta nuevas particiones **de las mismas fuentes**. No hay replicación externa independiente, ni corrección suficiente de multiplicidad para reivindicar efectos confirmatorios.

## Archivo y pendientes para el gate de merge

- La rama `research/ab65-frontier-20261023` contiene tres partes `src/engine.py.gz.b64.part1..3`. Hash SHA256 declarado del fuente descomprimido: `dbaf936199752781606303a07df61de600e0bd12af5b8a27d064d28aebe15421`. Los tres blobs GitHub fueron reconsultados y sus hashes de contenido Git coinciden con los originales.
- `prereg/B01.md` … `B10.md` y reemplazos `C61_REPLACEMENT.md`, `C62_C64_REPLACEMENTS.md` están presentes; también `reports/PLAN5_READOUT.md`.
- Falta introducir resultados E/G numéricos C62–C64, todos los JSON brutos por semilla/adquisición, ledger A–J completo P01–P05 y C01–C64, comprobación de SHA de fuente reconstruida desde clon y replay limpio. **CLEAN_CLONE_NOT_VERIFIED**.
- Reconciliar la contabilidad de ciclos usando los identificadores válidos (C01–C41, C43–C54, C56, C59, C60, C61–C64), sin convertir los cuatro inválidos en efectos nulos válidos.
- Conservar versiones y cronología de fallos, incluir documentación sobre derechos/licencia de los datos, ejecutar revisión de controles SIS/PPRM con paridad presupuestaria y diseñar replicación prospectiva independiente si vuelve a intentarse 2/3.

**AB-DECIDE:** CERRAR LA BÚSQUEDA LOCAL / NO 2/3. No recomendar más semillas de los mismos generadores como sustituto de una nueva clase de evidencia. **Estado GitHub:** archivo de investigación parcialmente versionado; no fusionar a `main` antes de completar las puertas documentales.
