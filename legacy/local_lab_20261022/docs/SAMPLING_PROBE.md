# Ensayo independiente de observabilidad espacial

Versión `spatial_sampling_probe_v1`, congelada el 2026-10-08. Estado: **144/144 celdas completadas**, matriz íntegra y semillas conservadas. Configuración: `configs/sampling_probe_v1.json`, SHA256 canónico `8456858c73122c19db3cf846ab7913820e064388d4b04644d5fd58124df98de2`. Coste real: **6.516s** incluyendo generación de dos geometrías nominales faltantes y figura; pico RSS muestreado **92.635MB**, dentro del límite60s.

Este ensayo pregunta si la distribución de cinco poblaciones **adquiere mejor cinco señales espaciales**. No entrena una red, no depende de superar XOR al .98 y no mide ventaja de procesamiento interno. Su inspiración es el muestreo de conos de [Jiao et al., PRE 2014](https://arxiv.org/abs/1402.6058) y la separación entre heterocoordinación y MHU de [Lomba et al., PRE 2020](https://arxiv.org/abs/2005.01558). El benchmark concreto es una propuesta propia; esos artículos no validan sus resultados anticipadamente.

## Resultado observado y decisión

La distribución aviar nativa mejora sustancialmente adquisición/interpolación frente a marcas permutadas y MHU nominal en este ensayo. **El control aviar sin penalización espectral conserva casi toda esa ventaja**, pese a no superar el certificado MHU en ninguna de sus tres semillas. Por tanto, estos resultados favorecen investigar exclusión/heterocoordinación y vacíos locales; no permiten atribuir la mejora principal a multihiperuniformidad.

La siguiente tabla muestra el kernel gaussiano fijado y ruidoσ.1; el CSV conserva también vecino más próximo y ruido0, sin selección posterior de estimador ni semillas. Son medias descriptivas de tres geometrías; menor MSE es mejor.

| Familia | Smooth native | Smooth shuffle | Fine native | Fine shuffle |
|---|---:|---:|---:|---:|
| MHU nominal | .158958 | .179138 | .961615 | .998836 |
| Aviar full_spectral | .047128 | .157525 | .602421 | .929984 |
| Aviar local_only | .050053 | .147542 | .613358 | .919429 |

Full−local nativa en smooth: diferencias por semilla `[-.004676,-.003493,-.000606]`, media−.002925. En fine: media−.010937. Estas diferencias pequeñas son compatibles con una contribución adicional del término espectral, pero también con cambios de microestructura local; tres realizaciones no identifican ese mecanismo. La MHU nominal incluso empeora frente a shuffle en la primera semilla fine para ambos estimadores: se conserva este contraejemplo en los registros completos.

La distancia macro al sensor más próximo confirma una explicación concreta de cobertura: nominalnative1.1895; aviarnative.9624; local_onlynative.9677. Fracción macro de queries sin sensor del canal a radio2.5: nominal4%; aviar/local_only.133%. No es una garantía de robustez neuronal ni un resultado del modelo recurrente.

Las nueve geometrías tienen conteos y domain iguales. MHU nominal3/3 y aviarfull3/3 superan su admisión; local_only0/3 conserva todos los candidatos como ablación deliberada. **La auditoría de procedencia confirma el mismo código del objetivo y la misma configuración numérica full/local.** Los ocho archivos comunes y las versiones de runtime tienen hashes idénticos; la identidad agregada de local difiere únicamente porque incorpora el módulo adicional `avian_local.py`. Ese wrapper reutiliza `avian_objective` con el término espectral omitido, mantiene inicialización, crecimiento, pasos Adam y opciones L-BFGS-B, y selecciona el primer candidato empaquetado sin exigir un certificado MHU positivo. Las tres parejas tienen idénticos hashes de coordenadas iniciales/etiquetas y usan intento cero. No hay evidencia de cambio de versión del optimizador ni de helpers científicos entre tratamientos. La diferencia deliberada de política de admisión queda explícita y no seleccionó otros intentos en esta tanda. Los hashes actuales coinciden con los seis manifests y sus NPZ; evidencia en `artifacts/avian_v1/provenance_audit.json`. No se actualizaron priors ni se abrió test neuronal.

**Siguiente contraste recomendado:** controlar estadísticas locales y vacíos antes de ampliar cualquier afirmación específica sobre MHU. Un rival equilibrado con buena exclusión local puede ser más discriminante que comparar sólo contra shuffle. La tarea aprendida posterior deberá separar señales adquiridas de procesamiento interno.

También es necesario incorporar reconstrucción fuerte: en la banda smooth hay doce coeficientes reales por canal y al menos 34 sensores de cada tipo. Una reconstrucción Fourier por mínimos cuadrados con la banda verdadera conocida, o su equivalente GP con covarianza del banco Fourier, puede recuperar exactamente campos sin ruido cuando la matriz de diseño tiene rango completo. Es una referencia oracle útil para determinar si la ventaja observada consiste en facilitar estimadores locales simples. No se afirma que el híbrido domine interpolación global óptima; esta tanda solo compara los dos estimadores fijados. Las queries en una rejilla fija también limitan la generalización a otras fases/orientaciones espaciales; deberán variarse de forma común y preregistrada en una versión posterior, sin reinterpretar retrospectivamente esta matriz.

![Resultados completos con ruido .1, dos bandas y dos estimadores](C:/Programación/LARP/artifacts/sampling_probe/v1/sampling_MSE.png)

## Matriz congelada

Tres familias, tres semillas comunes `1101,1102,1103` y dos asignaciones de marcas por familia/semilla:

| Familia | Native | Shuffle de conteos exactos | Interpretación |
|---|---|---|---|
| MHU nominal v0.1 | Espectral por población/unión | Mismas X y observaciones ahora según marcas permutadas | Efecto de organización de canales sobre el mismo sustrato |
| Aviar híbrida full_spectral v1 | Empaquetamiento/repulsión homotípica y espectro | Mismas X/conteos | Candidata de interés aviar; no retina empírica |
| Aviar híbrida local_only v1 | Idénticos términos locales, sin penalización espectral | Mismas X/conteos | Ablación del generador; se conserva aunque falle certificado MHU |

El número de réplicas descriptivas es **tres geometrías**, no 128 mundos ni cinco canales. Native/shuffle está emparejado en X, targets, queries y ruido por node ID. Full/local tienen optimizaciones y coordenadas distintas; su contraste no identifica por sí solo fluctuaciones de ondas largas, pues la microestructura local también puede cambiar.

No añadimos Grid balanceado automáticamente: su optimización de marcas costosa introduciría otra política de construcción. HU-unión, Grid balanceado y un control que preserve estadísticas locales deben añadirse en otra versión si el resultado inicial justifica gasto. La matriz actual identifica observabilidad bajo estas condiciones, sin establecer superioridad universal de MHU.

## Campos y observaciones

Para cada banda se generan 128 realizaciones comunes de cinco campos independientes sobre el toro L20. Usar modos enteros reales no redundantes y sin modo cero:

`f_c(x) = sum_m [a_cm cos(2π n_m·x/L) + b_cm sin(2π n_m·x/L)]`.

Coeficientes normales independientes, normalizados mediante `0.5 sum_m(a_cm²+b_cm²)=1`. Media espacial analítica cero y varianza espacial analítica uno para cada mundo/canal. **Nunca** centrar o normalizar usando muestras de cada población: ello introduciría un target dependiente de geometría/marcas.

- Smooth: `1≤|n|≤2`, seis modos; corresponde deliberadamente a escalas grandes cubiertas por el objetivo espectral nominal.
- Fine: `3≤|n|≤5`, escalas fuera del conjunto optimizado.
- Cien queries fijas `(2a+.5,2b+.5)`, `a,b=0..9`; no se asignan a neuronas mediante Hungarian ni cambian con X.
- Sensor i observa sólo `f_label_i(x_i)+σ ε_i`, con σ0/.1. No tiene acceso oculto a otros canales. ε_i normal común por mundo/node ID/semilla, incluso al permutar marcas. Entre geometrías diferentes ese pairing no representa una misma posición física.

Namespaces nuevos y fijados: campos7811, shuffle7812, ruido7813, master20261008. Los campos/targets son idénticos para todas las familias y semillas. El banco de coeficientes, queries y hashes queda en `common_field_bank.npz` y `field_manifest.json`.

## Estimadores y métricas

Dos estimadores fijados, sin parámetros aprendidos ni HPO: vecino más próximo del canal correspondiente en distancia periódica; media gaussiana local con ℓ1.25, soporte≤2ℓ. Un soporte vacío usa exactamente el mismo vecino más próximo; registrar fracción de fallback. Los empates exactos seleccionan menor node ID.

MSE por canal sobre 128×100 predicciones; media macro de los cinco canales con igual peso. La normalización es por varianza analítica uno, de modo que este MSE es un NMSE declarado frente al campo continuo. No es accuracy neuronal. Informar también distancias al sensor del canal más próximo (media, mediana,p90,p95,máximo) y fracción de queries sin sensor de ese canal a radio2.5, independientemente del estimador y de las etiquetas de error.

144 celdas fijadas. Reportar medias/SD entre geometrías y diferencias native−shuffle para cada banda/estimador/ruido, incluidas diferencias positivas que indiquen peor MSE native. Sin p-values, intervalos de arquitectura ni actualización H1–H6. Una ventaja a banda smooth y no fine sería compatible con cobertura de escalas grandes; no prueba su causa sin matching local. Una ventaja sólo del kernel podría depender de su escala fija. Ambos son resultados que requieren especificar alcance, no eliminar condiciones.

## Ejecución, preservación y límites

Ejecutar en proceso independiente, con límites BLAS/OMP4 configurados antes de importar NumPy. El API dentro de un proceso que ya inicializó BLAS no garantiza reconfiguración retrospectiva; el manifest registra el entorno. Presupuesto60s incluyendo gráficos, con checks entre geometrías y registro real de tiempo/memoria. Una generación nominal iniciada no se interrumpe en mitad de un optimizador: si sobrepasa el límite se informa y no se oculta. Aviar debe haberse generado externamente; el probe nunca la regenera ni ajusta.

```powershell
Set-Location -LiteralPath 'C:\Programación\LARP'
& '.\.venv\Scripts\python.exe' -m larp.sampling_probe --dry-run
& '.\.venv\Scripts\python.exe' -m larp.sampling_probe
& '.\.venv\Scripts\python.exe' -m pytest tests/test_sampling_probe.py -q
```

`preregistration.json` se escribe antes de generar campos y calcular scores. Incluye configuración, hashes de módulos/generadores y versiones de runtime. Las MHU nominales faltantes se generan con presupuesto original y se guardan dentro de `artifacts/sampling_probe/v1/geometries/`. Geometrías faltantes o fallidas quedan declaradas; no se reemplazan semillas ni se eliminan del denominador. Los controles local_only pueden analizarse como **no MHU admitida**, sin promover su certificado. Una matriz parcial no admite interpretación positiva.

Una corrida completa con idéntica procedencia se reutiliza sin volver a abrir scores. Si cambia la procedencia, se requiere otra carpeta de serie; no sobrescribir resultados. Artefactos: `results.json`, `partial_results.json`, `summary.csv`, `sampling_MSE.png` y mundos/hash comunes. Cero entrenamiento neuronal y priors conservados.

Verificación actual: **14 tests PASS, .54s**, JUnit en `artifacts/sampling_probe/v1/test_sampling_probe.xml`, incluidos normalización analítica, periodicidad, observación exclusiva de cada canal, reproducción de campos/ruido, fallback exacto, media macro, freeze antes de scores, idempotencia y conservación de geometrías faltantes/no admitidas. Este éxito verifica el estimador y protocolo, no una ventaja empírica de MHU.
