# Tarea concreta para ejecutor Windows/Codex independiente — recuperar N400 y Wei auténtico

**Estado:** SPEC_ONLY_NOT_EXECUTED. Esta tarea no consume ningún ciclo funcional nuevo ni valida LARP. No ejecutar CI costosa, no fusionar a main, no aceptar licencias nuevas ni redistribuir datos originales ajenos.

## Puerta 1 — Exportar seis geometrías N400, CON hashes

En Windows con acceso legítimo al repositorio privado GalexY3/proyecto-LARP:

```powershell
git clone https://github.com/GalexY3/proyecto-LARP.git
cd proyecto-LARP
git fetch origin research/ab-r-native-certificates-20261030
git switch research/ab-r-native-certificates-20261030
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy
.\.venv\Scripts\python.exe research/AB_NATIVE_AUDIT_20261030/export_native_n400.py --root .
# Solo si el dry-run confirma SIX/6 originales y los SHA:
.\.venv\Scripts\python.exe research/AB_NATIVE_AUDIT_20261030/export_native_n400.py --root . --write
```

El script debe leer los seis originales NPZ de legacy/local_lab_20261022/artifacts/avian_v1, contrastar 400 posiciones y etiquetas por archivo, SHA256 de points/labels/geometry con los certificados fuente, metadatos y conteos [163,85,68,50,34]. Conservar el SHA Git de cada NPZ. Exporta únicamente a una nueva carpeta PRIVADA seis JSON de puntos IEEE-754 exactos mediante float.hex, etiquetas enteras y L.hex; la recarga debe restaurar idénticos bits. No editar/sustituir los NPZ. Registrar Python/NumPy y errores.

Si la exportación termina y la política de acceso al repositorio lo permite, abrir rama distinta research/ab-r-native-binary-export-20261030 desde esta rama, incorporar únicamente estos seis JSON y un manifiesto SHA; no hacer merge, ni publicar en un repo externo. Revisión por un segundo proceso de los hashes antes de consumir nuevos outcomes. GitHub connector de Chat lee JSON texto, no NPZ.

**Aceptación A:** seis exports, 6/6 hashes points/labels/geometry exactos, 6/6 source git blobs exactos, trazabilidad commit, cero cambios en los NPZ y permisos privados. **Falsador:** un SHA no coincide ⇒ STOP_NATIVE_HASH_FAILURE, conservar ambos hashes/log, no reparar datos para cuadrarlos.

## Puerta 2 — Comparador multiclase verdadero de Li-Yi Wei

Fuente canónica: https://github.com/1iyiwei/noise.git, commit fijado **0d1be2030518517199dff5c7e7514ee072037d59**. README licencia MIT. Ruta RainbowNoise/src/Main/DartThrowing.cpp; proyecto CMake original declara mínimo 2.6 y dependencias Windows, por tanto compatibilidad con CMake moderno no garantizada.

```powershell
git clone https://github.com/1iyiwei/noise.git
cd noise
git checkout 0d1be2030518517199dff5c7e7514ee072037d59
cmake -S RainbowNoise -B build -DCMAKE_POLICY_VERSION_MINIMUM=3.5
cmake --build build --config Release --target DartThrowing
```

Si CMake falla por cambios de versión o archivos obsoletos, guardar stderr, parches mínimos y hashes; STOP_WEI_BUILD antes de predicciones, no bautizar un sustituto Poisson como Wei. Leer la CLI real de DartThrowing.cpp, ejecutar prueba de humo multiclase 5 tipos con 400 posiciones y cuotas exactas o registrar qué restricciones impiden obtenerlas; medir tiempos, distancias por clase y bandas espectrales, sin manipular quotas a posteriori.

**Aceptación B:** binario ejecutable auténtico, commit exacto, build log, parámetros reales extraídos de su código, salidas multiclase reproducibles y cuotas/espacio comparables. El proyecto de 2010 tiene prior art en muestreo multiclase; no reclamar originalidad sin contraste real.

## Puerta 3 — Siguiente contrato AB-R funcional (solo después de A y B)

Congelar nuevo preregistro A–J, código completo SHA y dataset antes de mirar outcomes. Confrontar originales N400 MHU y LOCAL de tres semillas (mismo inicio/etiquetas) vs Wei real y CVT regular, con mismo número de lecturas, cuotas y nivel de información. Para red neuronal, mismo modelo/optimizador/entrenamiento y coste de aristas/longitud/FLOPs medido. El conjunto externo debe contener modalidades ópticas independientes reales y procedencia/permiso documentados; no sustituirlas por cinco etiquetas sobre RGB ni reutilizar C01/C02/C04. Prerregistro de splits por escena completa y medida de covarianzas interbanda. Análisis emparejado por escena, no por nodos/repeticiones.

**Criterios R5:** si Wei/CVT domina o no hay originales y datos accesibles, publicar negativos o bloqueo y parar; no repetir semillas artificiales para agotar una cuota. No atribuir efectos a MHU sin ablación del término espectral y control fuerte. En todos los casos conservar logs y hashes.

## Evidencia NO disponible en esta sesión

Los NPZ originales se ven en GitHub con sus objetos Git, pero el conector rechaza la codificación binaria y el contenedor Chat no resuelve internet. No he compilado Wei ni ejecutado una sola red neuronal sobre las seis geometrías originales. Los 20 análisis N01–N20 son una revisión documental de certificados finitos, no la finalización de estas tres puertas.
