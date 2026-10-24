# LARP AB20 FULL RUNTIME — dictamen de 20 ciclos PIVOT

**Fecha:** 24 de octubre de 2026. **Método:** AB 3.2.1 + O1–O6. **Autorización:** 20 ciclos de PIVOT desde AB20 REALPATCH (PR #22), sin obligación de éxito. **Estado:** 20 unidades distintas de BugsInPy intentadas; tres versiones de instrumentación R0/R1/R2, **no 60 ciclos**.

## Marcadores científicos

| Aspecto | Resultado final |
|---|---|
| Identificadores de defectos congelados antes de ejecución | 20 |
| Repositorios upstream completos | tqdm, PySnooper, cookiecutter, youtube-dl, black |
| Defectos con contraste dirigido buggy-fail/fixed-pass atribuido al cambio de código | **14/20** (reproducción condicionada) |
| Bloqueados por dependencias, instalación o recopilación | 4/20 |
| Falso positivo descubierto en auditoría manual | 1/20 (C09) |
| Mismo test pasa en ambas versiones | 1/20 (C06) |
| Ejecución externa respecto a sandbox ChatGPT | GitHub Actions, pero NO replicación científica independiente |
| CT2 de esta rama | **8→11/100** (ordinal, no probabilidad) |
| N1 nuevos / portfolio previamente auditado / N2 / N3 | **0 / 6 / 0 / 0** |

## Estimando y datos

Se utilizó [BugsInPy](https://github.com/soarsmu/BugsInPy) como benchmark **retrospectivo curado** y se congelaron los 20 pares de SHA, versiones documentadas y objetivos test en [PREREG_COHORT_20.json](PREREG_COHORT_20.json), commit [806095ea](https://github.com/GalexY3/proyecto-LARP/commit/806095ea98ad8749096f0b0891b2bba35a41bb4b). La unidad de investigación es el bug ID real; las reparaciones instrumentales no aumentan el denominador.

Para cada caso se descargó mediante Git el **repositorio upstream completo**, no un hunk simulado; se verificaron las identidades exactas de los dos commits y se usó el test dirigido en `projects/<project>/bugs/<id>/run_test.sh`. La versión buggy recibió los archivos listados por `test_file` procedentes del commit fixed, según la lógica del `bugsinpy-checkout` original; se registraron los hashes de dichos archivos y la salida de la instalación/ejecución. Esto es **test de regresión retrospectivo post-exposición**, no diseño de detector ciego.

**Desviaciones:** entorno Python3.6.15 Docker frente a 3.6.9 originales; Python3.7.17/3.8.18 hosted frente a micropatches originales; paquetes de testing preparados mínimamente, **no todos los requirements históricos instalados a sus pins exactos**; `tox test_selector` de Cookiecutter traducido a `python -m pytest test_selector`; entornos reutilizados dentro de cada proyecto. Por tanto, el resultado es reproducción funcional condicionada de pruebas dirigidas en fuentes íntegras, **no reproducción bit-a-bit del entorno original del benchmark**. No hay controles profesionales de misma inversión ni fuente externa independiente.

## Reparaciones R0–R2 y por qué no se ocultan

**R0 / INVALIDA**: [run 40109096869](https://github.com/GalexY3/proyecto-LARP/actions/runs/40109096869). Falló el suministro Python3.6 en ubuntu22.04; once casos 3.7/3.8 se intentaron con un test-file completo, sin trasladar los tests añadidos al fixed. C07 PySnooper produjo un espejismo de buggy-fail/fixed-pass causado por `ModuleNotFoundError: python_toolbox` durante la recopilación. NO fue un bug detectado. Los resultados se archivaron sin eliminarlos.

**R1 / REPARACION PRERREGISTRADA, POST-EXPOSICIÓN**: [run 40109855339](https://github.com/GalexY3/proyecto-LARP/actions/runs/40109855339). [Protocolo de reparación previo](REPAIR_R1_PRE_RUN.md), commit d4df9923, [motor](run_full_runtime_r1.py) congelado en 0e6eb231. Docker Python3.6, tests `run_test.sh` y transferencia de fixed-test. Seis candidatos (C01–C05 y C12); once fallos de paquete `bdist_wheel` y tres de opciones pytest-cov.

**R2 / REPARACION PRERREGISTRADA, POST-EXPOSICIÓN**: [run 40110153479](https://github.com/GalexY3/proyecto-LARP/actions/runs/40110153479). [Errata congelada](REPAIR_R2_PRE_RUN.md) commit 487c0020, [motor R2](run_full_runtime_r2.py) commit 72a016cf, trigger posterior 7d9b2b8d. Únicas correcciones instrumentales: `wheel==0.37.1` y `pytest-cov==2.12.1`. Se obtuvo buena parte de la paridad buggy/fixed, pero el detector automático de aserciones era incompleto y el false positive debía identificarse manualmente.

**AUDITORÍA ADVERSARIAL FINAL**: [AUDIT_FINAL_20.json](AUDIT_FINAL_20.json). Se descarta C09: en buggy faltaba el *fixture* `tests/test-generate-context/non_ascii.json`; el `FileNotFoundError` NO prueba el error de encoding. Se añade C16: el unittest de youtube-dl sí ejecutó el código original y falló por `ExtractorError: Unsupported JS expression 'x()'`, arreglado en fixed; el clasificador original ignoraba `unittest errors=1`. No se realizó R3 para perseguir una cuota de éxitos: AB-R5 prioriza conocimiento discriminante frente a buen número.

## Dictamen caso por caso

Los **14 reproducidos** son **C01–C05 tqdm**, **C08 PySnooper**, **C10–C12 Cookiecutter**, **C13–C16 youtube-dl**, **C20 Black**. Entre los mecanismos observados: bool sobre generador sin longitud; formato `total=None`; `output_path` no definido; múltiples hooks; excepción de hook inexistente; match booleano; entidad HTML malformada; representación DASH repetida; llamada JS sin argumentos; y conservación de líneas iniciales en formateo. Cada traceback y comando están conservados en `results_uploaded/R2/` (código + fixture del fixed versionados por SHA).

**C06 PySnooper**: ambas versiones pasan el test. **C07 PySnooper**: error de import `tests.mini_toolbox` antes de ejecutar el test; bloqueado. **C09 Cookiecutter**: falta fixture auxiliar; falso positivo descartado. **C17–C19 Black**: ambos commits bloqueados por una incompatibilidad actual de `setuptools_scm 10.3.4` con los antiguos metadatos del paquete; no se ejecutó el test pertinente. Las categorías no deben colapsarse en «6 fallos».

## Contabilidad del descubrimiento, priors y CT2

**Prior reforzado P1:** un commit verdadero y el hunk ejecutado no garantizan reconstruir el fallo en un paquete completo, y un fallo en la instalación no es bug reproducido. **Prior actualizado P2:** sí es viable montar un instrumento compatible que reproduzca en código fuente íntegro 14/20 pruebas de una cohorte real seleccionada, aunque con dependencias aproximadas y exposición al oracle. **Refutación P3:** la aparente equivalencia «buggy falla/fixed pasa» es insuficiente sin inspeccionar la causa (C09), y las heurísticas de excepción pueden infracontar reproducciones (C16). **Prior negativo P4:** todavía no existe ninguna evidencia de ventaja MHU, un método novedoso de test selection, ni mejora computacional frente a Hypothesis, suites profesionales o subsunción.

Ningún hallazgo es nuevo como principio científico. N1 de campaña **0**; cartera auditada anterior 6 **sin modificar**; N2=N3=0. CT2 de la línea REAL_FULL_RUNTIME cambia **8→11/100** porque ahora hay acceso concreto a fallos reales que permitirían futuros contrastes, pero antecedentes y sesgo retrospectivo siguen siendo fuertes. No es probabilidad, y el salto entre ramas anteriores es discontinuo. Ver [trayectoria reproducible](CT2_TRAJECTORY.json) y el ZIP completo de la conversación para ambas vistas Matplotlib. No se atribuyen CT2 individuales ficticios a R0/R1.

El método AB tampoco queda validado por haber producido esta campaña. La próxima hipótesis científicamente discriminante tendría que diseñar **antes de ver el arreglo** nuevos tests sobre fallos prospectivos, contra controles profesionales con igual coste de diseño/ejecución y validación fuera del benchmark original. Duplicar los mismos veinte bugs o agregar seeds no alcanza 2/3.

## Integridad de datos en GitHub

Los originales completos R0, R1, R2 están preservados bajo [`results_uploaded/`](results_uploaded/) (no solo ZIP de ChatGPT), copiados desde los artefactos GitHub Actions por el [flujo de archivado](https://github.com/GalexY3/proyecto-LARP/actions/runs/40110584855). SHA256 de archivos en [results_uploaded/SHA256SUMS.txt](results_uploaded/SHA256SUMS.txt). El motor de cada versión y los testigos se congelaron por commit **antes de su correspondiente replay**; ninguna reparación retroactiva se presentó como confirmación independiente. El PR debe permanecer draft hasta revisión independiente del flujo y los controles; conservar sin fusionar archivos exploratorios ajenos ni prometer reconstrucción exacta del entorno original.

**AB-DECIDE:** `CLOSE_QUOTA_20`, `STOP_LOCAL` de más ajustes al mismo benchmark y `BRANCH_POSSIBLE` hacia nuevos diseños cegados de testing. Siguiente autorización opcional: 20 ciclos de branching con prereg de propiedades antes de ver el fix, revisión de novedad y presupuesto comparable. **SOLICITO BRANCHING 20 CICLOS**.
