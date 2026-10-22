# AB30 Codex — branching secuencial, 22 de octubre de 2026

**Cierre solicitado por el investigador: 10/30 ciclos ejecutados; veinte pendientes.** Véanse el [informe](REPORT.md), el [ledger A–J](LEDGER.md) y la [verificación](CLOSEOUT.json). La autorización inicial de treinta ciclos se conserva abajo como historial; no se afirma haberla completado.

Autorización: el investigador encarga revisar AB/LARP actualizados y realizar 30 ciclos dinámicos con commits. La campaña inicia desde `proyecto-LARP` `8ab51f58c688d10209afae6a4cb39d43d82b73e5` y metodología `ed02e7a5f6d2baaf1a45ae41ae7fdd48d4e143e4`, además del núcleo AB3.2.1 recuperado de Drive el 22 de octubre. No modifica retrospectivamente experimentos anteriores ni interpreta el cierre neuronal de octubre como prohibición de este nuevo encargo.

Cada pregunta se elige tras examinar la evidencia anterior. Se conserva protocolo y fuente completos en un commit antes de ejecutar; cada decisión incluye opciones rechazadas y evidencia que abre la siguiente rama. Barridos, inicializaciones y magnitudes de corrupción son condiciones dentro de un ciclo. Todos los análisis adaptativos son exploratorios; no se afirma confirmación externa por cambiar semillas o reutilizar UCI Digits.

Primer cuello de botella: posible fallo de escalado de píxeles constantes en AB06 C06. Primero se examina esa intervención, antes de aceptar la aparente robustez sensorial. No hay lista de treinta experimentos fijada por adelantado.

Ejecución desde raíz, Python con numpy/scipy/torch y scikit-learn; dependencias auxiliares aisladas en `.deps`, ignoradas por Git. El entorno CPU existente de LARP se reutiliza sin instalar paquetes en él; scikit-learn/joblib/threadpoolctl se instalaron únicamente en `.deps` de este checkout.

```powershell
& 'C:\Programación\LARP\.venv\Scripts\python.exe' research/AB30_CODEX_20261022/manage.py freeze C01
& 'C:\Programación\LARP\.venv\Scripts\python.exe' research/AB30_CODEX_20261022/manage.py run C01
```

Las fuentes históricas permanecen intactas. Los wrappers nuevos declaran cualquier diferencia de rutas, tipos numéricos, checkpoint o preprocesamiento. Los resultados de fuentes externas y las identidades matemáticas se distinguen de nuevas mediciones. Las auditorías iniciales de agentes sirven para seleccionar C01, no se presentan como experimentos independientes.
