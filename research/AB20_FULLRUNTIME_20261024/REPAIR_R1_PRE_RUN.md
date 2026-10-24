# Reparación instrumental R1 — PRE-RUN, 24-10-2026

## V0 resultado observado antes de R1
GitHub Actions RUN **40109096869** en el commit `6c8c463` (archivo original intacto, no borrar). De cinco lanes: Python 3.6 de `tqdm` (5 bugs) y `cookiecutter` (4 bugs) ni siquiera inició por no estar 3.6 en setup-python Ubuntu22.04. Los otros lanes ejecutaron 11 casos con commits completos, pero **la inferencia de detección es INVALID**: se probó un fichero completo y no el target `run_test.sh`, se omitió copiar los testigos del fixed a buggy, y aparecieron errores por dependencias ajenas. Particularmente C07 PySnooper parecía fail/pass; buggy tenía ModuleNotFoundError: python_toolbox en recolección y fixed pasaba 31 pruebas. Es un **falso positivo** de la regla antigua, NO bug reproducido. En youtube-dl C16 ambos revisiones pasaron su suite (11 vs 12 tests), por omitir el test reparador en buggy. Las pruebas de black mostraron AioHTTPTestCase no definido o incompatibilidad de Click.

## Puerta R1, antes de nuevos datos
1. Mantener mismos 20 SHAs e IDs del manifesto commit `806095e`. No reemplazar casos incómodos.
2. Para Python 3.6.9 original usar contenedor `python:3.6.15-buster`; **versión micro no idéntica**. Para 3.7/3.8 runner usa la última micro de setup-python. Registrar siempre `sys.version`.
3. Clonar repositorio upstream completo, verificar SHA de cada revisión, y además clonar BugsInPy oficial. Extraer `run_test.sh` y `test_file` oficiales. Como hace `bugsinpy-checkout`, copiar exclusivamente `test_file` de fixed a buggy (incluidos fixtures declarados) y correr el **test dirigido oficial**, nunca sustituirlo silenciosamente por la suite completa. Registrar hash de los bytes overlay.
4. Instalar las dependencias razonables mínimas y registro del pip freeze. No pretender identidad con `requirements.txt` histórico si no se instaló entero. Si faltan dependencias, clasificar `ENV_BLOCKED`, no fallo del bug.
5. Criterio `CANDIDATE_BUG_REPRODUCED`: después de instalar, el test **realmente recopiló y ejecutó** un caso que falla en buggy por AssertionError o similar, y pasa en fixed. Fallo de import, collection, no tests, timeout o pip son `INVALID_INSTRUMENT` o `BLOCKED`. Un candidato posterior necesita auditoría manual de la traza, a veces fallo ambiental que casualmente desaparece.
6. Guardar todos los JSON por caso, comandos y stderr, incluyendo negativos, fallo Docker, varias revisiones. Repetición dentro del mismo GH runner no es confirmación externa, ni blindaje porque se han leído commits; no se promueven N1 ni 2/3.

## Protocolos AB
- A pregunta: ¿se puede reproducir buggy-fail/fixed-pass del test de BugsInPy en paquete histórico completo?
- B H1 paridad con el test oficial; H0 no; Hother incompatibilidad del entorno y test contaminado.
- C 20 IDs ya congelados, igual test y entorno para pareja, sin escoger a posteriori.
- D Git SHA + test overlay hash + intérprete + deps + test exacto, R1 en commit pre-run.
- E invocar y almacenar. F comprobar traceback, host/cmd, colección y paridad real. G no hay validación externa. H priors entre metadatos, hunks y ejecución auténtica. I 0–3 y CT2. J repair/stop condicionado evidencia.
- No confundir 20 bugs reales seleccionados con 20 éxito ni un test dirigido con descubrimiento de bug nuevo.

No activar workflow hasta código R1 remoto íntegro; la señal final será `R1_START.md`. La CT2 de esta línea comenzó en 8/100 y puede decrecer por fallo instrumental; nunca aumenta por poner Docker. **RESULTADOS R1 AÚN NO OBSERVADOS.**
