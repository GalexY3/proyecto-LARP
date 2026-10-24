# AB20 REALPATCH — dictamen final / 24-10-2026

## Estado de evidencia
Autorizados 20 PIVOT AB. **20/20 comparaciones de fragmentos upstream ejecutadas**, 10 defectos reales documentados × 2 estímulos. **0/20 reproducciones dinámicas integrales históricas** (instalación, checkout, dependencias y pytest originales NO realizados). El ejecutor Python 3.13.5 no dispone de acceso de red, Docker, Conda o intérpretes históricos. Ningún control profesional completo comparado; las entradas se escogieron tras ver los fixes, POST_EXPOSURE. No hay 20 bugs independientes ni 20 descubrimientos.

Diez linajes y resultado por pares:
- C01–C02 TQ01 `tqdm/tqdm@c0dcf39b`, `tenumerate(start)`.
- C03–C04 TQ03 `tqdm/tqdm@73962a47`, bool de generadores sin len.
- C05–C06 TQ04 `tqdm/tqdm@964dee63`, escala con total desconocido.
- C07–C08 TQ05 `tqdm/tqdm@4f340697`, total ausente con disable=True.
- C09–C10 PS01 `cool-RR/PySnooper@56f22f8f`, decodificación UTF8 fuente.
- C11–C12 PS02 `cool-RR/PySnooper@814abc34`, custom_repr como único par.
- C13–C14 PS03 `cool-RR/PySnooper@15555ed7`, cierre de ruta output_path sin definir.
- C15–C16 YT01 `ytdl-org/youtube-dl@1cc47c66`, unary matcher booleano.
- C17–C18 YT03 `ytdl-org/youtube-dl@95f3f7c2`, entidades HTML malformadas.
- C19–C20 CC02 `cookiecutter/cookiecutter@90434ff4`, selección de hooks múltiples.

## Resultados cuantitativos
- 20/20 pares old/fixed difieren ante las entradas predirigidas; 20/20 fixed devuelve sin excepción.
- Null controls benignos **12/20 ejecutados**, sin divergencias; 8/20 solo invariantes documentales y NO son ejecuciones.
- 2 entradas por reparación compartiendo el mismo defecto, fuentes y wrapper: no asumir independencia.
- Segundo replay en idéntico intérprete **byte a byte igual**: fuente SHA256 `846e2f2652c7f6825986d3afdd90a373050cfb2bdb4d348df0d89e5f1ddb0f2c`, resultados completos SHA256 `8ee2c2eb69ce737308898c21372cdbfa3951afdf761ce1481e767d85343dbbcf`.

## Auditoría de alcance y validez
La ejecución utilizó un **hunk del diff upstream adaptado a wrapper mínimo**, no el paquete entero en su entorno real. Son `EXPERIMENTAL_PATCH_HUNK_POST_EXPOSURE`, no `DYNAMIC_HISTORICAL_REPRODUCTION`. Comparación contra pruebas propietarias/pytest upstream/Hypothesis/greedy reducción no realizada. El resultado del 100% está condicionado al conocimiento del fix: no estima probabilidad ni sensibilidad de detección de bugs nuevos. La reproducción local no constituye confirmación externa. No se ejecutó un test ciego al parche.

Alcance del prereg: `PREREG.md` commit `b1ae3a5` ANTERIOR a la ejecución y con los 20 estímulos especificados. **La fuente íntegra no estaba remotamente congelada antes de ejecutar**, brecha O3 que NO se puede reparar retroactivamente. El motor y brutos por ciclo están en el ZIP de conversación `LARP_AB20_REALPATCH_20261024.zip` SHA256 `1eadcdab38360062e4c18bba18eae9b71f0a6ee2d91a3c4f2eadefaf31794252`. Pendiente de incorporar fuente exacta, 20 `raw/Cxx.json`, figuras y efectuar un replay de clon limpio; no fusionar todavía.

## CT2, DRIFT, ledger
Rama principal AB55 `11→8`; rama P04 separada `12→10`; nueva línea de fragmentos upstream `8→8/100`. Del P04 a esta línea, DRIFT `D2,4`: población pasan de bugs inyectados a cambios reales de upstream, manteniendo problemas de testing, y estimando se restringe a fragmentos; NO hay continuidad probabilística entre CT2=10 y CT2=8. CT2 es escala subjetiva ordinal, nunca P(descubrimiento). Nuevos 1/3=0; portfolio histórico previamente auditado 6; 2/3=0, 3/3=0. No se modifica ledger acumulativo por no existir hallazgo nuevo.

Priors AB20: (1) evidencias de metadatos vs ejecución de hunk vs reproducción histórica completa son tres niveles diferentes; (2) después de conocer el fix, un test regresivo dirigido no mide capacidad de descubrimiento ciega; (3) veinte estímulos agrupados en diez bugs no deben contarse como veinte fenómenos; (4) cambiar hacia code hunks reales no elimina incompatibilidad de dependencias de la versión histórica. Los antecedentes metodológicos directos (BugsInPy, QuixBugs, metamorphic testing, mutant subsumption) descartan originalidad a priori.

## Decisión
`CLOSE_QUOTA_20`, `STOP_LOCAL` respecto a ventajas de testing, `BLOCKED_FULL_RUNTIME` respecto a reproducción histórica total. Próxima puerta crítica: reproducir versión buggy en checkout completo, hacer fallar test original y pasar en fixed sin modificar tests; diseñar un test propio ciego y comparar con control profesional, en al menos dos revisiones con dependencias congeladas. **NO se acredita nivel 2/3.**

Siguiente propuesta, no concedida todavía: 20 ciclos experimentales en entornos históricos reales (si están disponibles, detener si faltan), sin nuevas pseudorreplicaciones de hunks. SOLICITO PIVOT 20 CICLOS.
