# Candidata geométrica aviar v1

La candidata `avian_spectral_hybrid_v1` combina exclusión local de discos polidispersos, repulsión entre nodos del mismo tipo y supresión explícita de seis modos espectrales. Se implementa separadamente en `src/larp/avian.py`; el generador y los perfiles científicos de LARP v0.1 permanecen intactos. Esta es una exploración geométrica, sin entrenamiento neuronal ni actualización de priors.

## Qué se conserva y qué se cambia

Se conservan `N=400`, `L=20`, el toro periódico de densidad uno y los conteos `[163,85,68,50,34]`, para permitir comparación con las realizaciones de LARP originales. Se conservan los umbrales completos de `finite_certificate_v0.1`, las seis poblaciones certificadas A–E/unión y los mismos 10.000 centros comunes. El criterio adicional de empaquetamiento exige solapamiento relativo máximo ≤0,002. Un certificado positivo describe criterios finitos; no prueba hiperuniformidad asintótica, parecido empírico con una retina ni ventaja computacional.

La nueva energía es:

\[
E=5\left[\overline{S}_{\cup}+\frac15\sum_c\overline{S}_c\right]
+\frac{20000}{400}\sum_{i<j}[1-r_{ij}/(a_i+a_j)]_+^2
+\frac{20}{5}\sum_c\frac{1}{n_c}\sum_{i<j:c_i=c_j=c}[1-r_{ij}/d_c]_+^2.
\]

Aquí `r` usa distancia mínima periódica y los pares activos se reconstruyen en cada evaluación. No se inventa una dirección de gradiente en una coincidencia exacta; esa situación se rechaza. `a_c` se normaliza para que la suma nominal de áreas de disco sea 0,58 veces el área del dominio. `d_c=sqrt(2/(sqrt(3)*n_c/L²))`. El término homotípico permanece fijo mientras los radios de disco crecen durante Adam.

| Tipo | Nombre de referencia | Conteo | Radio del disco | Corte homotípico |
|---|---|---:|---:|---:|
| A | Doble | 163 | 0,503088 | 1,683336 |
| B | Verde | 85 | 0,378993 | 2,331069 |
| C | Rojo | 68 | 0,355516 | 2,606215 |
| D | Azul | 50 | 0,399117 | 3,039343 |
| E | Violeta | 34 | 0,335392 | 3,685744 |

Los radios son regiones de exclusión del modelo, no neuronas con función visual ni estados de distinto tamaño. Todos los nodos conservarían el mismo estado computacional en un experimento neuronal posterior.

El optimizador reproduce el antecedente visual: Adam float64, 6.000 pasos, LR coseno 0,015→0,0001, radios iniciales al 25% y crecimiento completo al paso 3.000; después SciPy L-BFGS-B sin límites de coordenadas, 1.000 iteraciones/2.000 evaluaciones, memoria 20, `gtol=1e-8`, `ftol=1e-12`. El objetivo evalúa coordenadas módulo L. Esta elección de L-BFGS-B corresponde al antecedente visual y constituye una diferencia deliberada respecto al L-BFGS con búsqueda strong Wolfe implementado en el contrato original.

La configuración nueva se congela antes de la validación en `configs/avian_v1.json`, con SHA-256 canónico `5be454858d9316af73499e4e32ccf807f6c07e165ef073a64c65833a99a0e471`. Cambiar números requiere otra versión. Semillas: 1101, 1102, 1103; RNG `[20261008,semilla,intento]`; máximo cuatro intentos; se devuelve la primera realización admitida. No se sustituye una semilla fallida. El límite de optimización por semilla es 120 s, con la certificación completa registrada aparte y conservada incluso ante timeout. Los intentos fallidos se guardan antes de seleccionar el siguiente intento. Los módulos y versiones usados se registran con hashes locales, evitando que cambios paralelos en módulos ajenos alteren la identidad de esta generación.

## Relación con la referencia primaria

[Jiao et al., *Physical Review E* 89, 022721 (2014)](https://doi.org/10.1103/PhysRevE.89.022721) es un artículo revisado por pares. El [PDF del laboratorio de Corbo](https://corbolab.wustl.edu/publications/Jiao2014.pdf) se consultó directamente y se conserva en `artifacts/avian_v1/reference_Jiao2014.pdf`, SHA-256 `12e4a868a52709e7b16d3b1cdeeecca355b15f10be0aec91a61d4838ed0ce3af`; la extracción de texto está junto a él.

Los radios relativos `[1,1.19,1.13,1.06,1.50]` en orden violeta/azul/verde/rojo/doble, el corte `2Rs=sqrt(2/(sqrt(3)*rho))` y una fracción de empaquetamiento aproximadamente 0,58 se verificaron en sección IV, páginas impresas 022721-7 a 022721-9. El artículo combina exclusión dura exacta, inicialización RSA y etapas de crecimiento/relajación. Nuestro híbrido usa penalización blanda, inicialización binomial y optimización Adam/L-BFGS-B. Su control espectral explícito es añadido propio, no una fuerza biológica demostrada. El artículo tampoco estudia redes neuronales artificiales.

El artículo simula 2.600 células: violeta 210, azul 355, verde 530, rojo 405, doble 1.100. Nuestros conteos preservan el contrato LARP, por lo que no coinciden exactamente con aquella simulación. Tampoco se ajustan estadísticas contra sus datos empíricos. La asignación de nombres A–E describe procedencia geométrica; no establece correspondencia neuronal funcional.

## Atribución causal y siguiente contraste

El aspecto visual intercalado puede provenir de repulsión homotípica y empaquetamiento aun cuando la supresión a largas escalas sea insuficiente. Por eso el objetivo incluye `treatment="local_only"`, que pone exactamente a cero el término espectral y conserva los demás factores, la inicialización y el presupuesto. Su finalidad es una ablación del control espectral; no se llamará MHU a una realización local que no apruebe el certificado. Se autorizó y ejecutó adicionalmente la comparación de las tres semillas locales en una ventana de CPU separada.

La ejecución apropiada de ese control usa `src/larp/avian_local.py`: se selecciona el primer candidato completo y empaquetado **sin filtrar por resultado de la certificación MHU**. Sus campos `control_admitted` y `mhu_admitted` separan idoneidad como control y cumplimiento de los criterios MHU. Un certificado MHU fallido no provoca reintento para obtener otro control ni sustitución de semilla. Esta ruta conserva el sourcehash exacto de los tres candidatos full ya ejecutados. La ruta genérica `generate_avian(treatment="local_only")` conserva la política de admisión MHU del generador original y, por tanto, no debe usarse para seleccionar controles en la comparación causal full/local. La nueva ruta evita ese sesgo de selección.

Para atribuir un eventual resultado neuronal a multihiperuniformidad habrá que comparar híbrido completo, local-only y original espectral, usando el mismo bloque capaz de aprender, presupuesto, conteos y datos. La permutación de marcas en coordenadas fijas sigue siendo necesaria para distinguir distribución funcional de cambios del grafo inducidos por geometría. Las distancias locales, matriz de tipos, cobertura, distribución de longitudes de arista y desplazamientos de puertos son confounds medidos, no mediadores probados. Aislar el efecto de los modos largos exige además un control local emparejado admisible: al eliminar el término espectral pueden cambiar también pequeñas distancias. No basta atribuir toda diferencia full-vs-local a hiperuniformidad.

La batería devuelve espectros por componente y unión, ventanas R=0,5/1/2/3/4/5, anti-Bragg en modos no optimizados, anisotropía descriptiva, `g2` por pares de tipos, distancia al tipo, Voronoi y orden orientacional. Añade el grafo causal kNN entrante de grado 6, sus SCC/caminos/longitudes/cobertura y los puertos Hungarian inyectivos. No se impone conectividad a posteriori ni se reconecta una realización fallida. Un indicador de anisotropía no se convierte automáticamente en exclusión; una valoración sistemática necesitaría la batería de 200 controles y más realizaciones.

## Verificación y ejecución

Las 17 pruebas de `tests/test_avian.py` y `tests/test_avian_local.py` pasan; registro JUnit `artifacts/avian_v1/test_avian.xml`. Incluyen diferencias finitas del gradiente en coordenadas aleatorias con pares activos para ambos tratamientos y dos escalas de crecimiento, invariancia de traslación periódica, equivariancia a permutación, suma de gradientes cero, eliminación exacta del término espectral, conteos/radios, timeout conservado y prohibición de promover un presupuesto reducido a candidato científico. Las pruebas adicionales comprueban que un control empaquetado se conserva aunque falle la certificación MHU y que mantiene la misma inicialización con semillas fijas; los mocks solo se utilizan en pruebas unitarias, nunca en artifacts científicos.

Comando independiente, sin entrenamiento:

```powershell
.\.venv\Scripts\python.exe -m larp.avian --dry-run
.\.venv\Scripts\python.exe -m larp.avian --output-dir artifacts/avian_v1
.\.venv\Scripts\python.exe -m larp.avian_local --dry-run
.\.venv\Scripts\python.exe -m larp.avian_local --output-dir artifacts/avian_v1
.\.venv\Scripts\python.exe -m pytest tests/test_avian.py tests/test_avian_local.py -q
```

API principal: `generate_avian(seed, treatment="full_spectral", output_dir=...) -> Geometry`. La admisión se consulta en `geometry.metadata["admitted"]`; un objeto geométrico devuelto puede representar un fallo retenido. `validate_avian_suite(...)` ejecuta exactamente las tres semillas y escribe resumen, artefactos y figura, con éxitos y fallos visibles.

## Resultado observado

Se ejecutaron las tres semillas completas, todas admitidas en el intento cero y sin relajación de criterios. Se almacenaron los tres intentos, certificados y manifests. Cada ejecución completó 6.000 pasos Adam y 1.000 iteraciones L-BFGS-B. El optimizador alcanzó su límite de iteraciones: **no se reclama convergencia numérica al mínimo**. La admisión describe exclusivamente los criterios geométricos observados tras el presupuesto fijado.

| Semilla | Tiempo generación + certificado | Máx. media S restringida | Máx. S restringido | Máx. razón de varianzas R4/R5 | Máx. pico S/N no optimizado | Máx. solapamiento relativo |
|---|---:|---:|---:|---:|---:|---:|
| 1101 | 8,267 s | 0,002392 | 0,007581 | 0,126329 | 0,474116 | 0,000619 |
| 1102 | 7,806 s | 0,003871 | 0,011364 | 0,127994 | 0,351665 | 0,000708 |
| 1103 | 7,912 s | 0,003982 | 0,017198 | 0,136798 | 0,248807 | 0,000301 |

Los máximos agregan tipos y unión. Los límites correspondientes permanecen 0,05/0,10/0,65/<0,50 y, para solapamiento, 0,002. Las distancias mínimas de unión son 0,690788/0,690768/0,690868, superiores al mínimo 0,299. La certificación completa tardó 0,279/0,252/0,252 s y utilizó exactamente los 10.000 centros comunes; los gradientes verificados en los candidatos tienen error absoluto máximo 8,97e-11/9,38e-11/6,53e-11. El RSS máximo **muestreado** durante generación fue 243.245.056/260.460.544/262.414.336 bytes; representa todo el proceso Python, con dependencias cargadas, y no un pico garantizado a resolución continua ni memoria exclusiva del kernel geométrico.

Los tres grafos mantienen 2.400 arcos, una SCC y fracción inaccesible cero, sin reparación. Las medias de longitud de arista son 1,104165/1,104667/1,105435; las medias de camino dirigido, 7,341410/7,297049/7,293979. Los puertos presentan RMS de desplazamiento 0,442135/0,450593/0,450709 y máximos 0,772766/0,802780/0,882368. Las cuadrupolas de anisotropía máximas por realización son 0,076438/0,084462/0,162638, por debajo del indicador descriptivo 0,30; no se ejecutó la batería de 200 controles aleatorios.

**Reserva científica concreta:** en 1101 el pico no optimizado 0,474116 pertenece a E, la población de solo 34 nodos, y queda próximo al umbral 0,50. Es admisible bajo el contrato finito, pero insuficiente para llamar a cada componente un mosaico desordenado semejante al empírico. La estabilidad de los picos por componente con N y el orden orientacional homotípico necesitan revisión antes de extrapolar al límite asintótico. La unión tiene picos mucho menores, 0,004250/0,006063/0,003637, y eso tampoco sustituye el análisis de cada población.

Una medición adicional explícitamente descriptiva, seis vecinos homotípicos más próximos en el toro, da orden hexático global de E 0,462225/0,351962/0,252991. Se conserva script y hash en `diagnose_homotypic_order.py` y resultados `*_homotypic_order.json`. Es consistente con precaución ante orden parcial en la población rara. No se convierte este resultado en nuevo criterio de exclusión retrospectivo ni se afirma comparación cuantitativa con la retina sin equiparar definiciones y tamaños.

La figura `artifacts/avian_v1/avian_full_spectral_validation.png` muestra las tres candidatas reales. Se inspeccionó y se amplió el margen de su pie con el script de presentación `render_validation.py`; `plot_manifest.json` registra hashes de script/entrada/PNG. Este ajuste no recomputó geometrías ni cambió el código científico o sus manifests.

El resumen de ejecución es `artifacts/avian_v1/summary_full_spectral.json`. Los artifacts incluyen certificados detallados, NPZ verificables, métricas del grafo, registros de puertos, verificaciones del gradiente y orden orientacional homotípico descriptivo. Los éxitos de esta tanda prueban que la candidata se puede generar y admite la batería finita; **no prueban aprendizaje, robustez ni superioridad neuronal**. Ningún prior se actualizó.

## Resultado del control local sin término espectral

Los tres controles locales se generaron y conservaron como controles empaquetados válidos en intento cero. **Ninguno aprueba el certificado MHU completo.** Fallan criterios espectrales de componentes A/B/C/D en distintas combinaciones, pese a que sus razones de varianza de ventanas son bajas. No se reemplazaron por intentos más favorables. Las etiquetas y las coordenadas iniciales tienen hashes idénticos a la contraparte full de cada semilla, verificados directamente en sus manifests. Se completaron 6.000 pasos Adam y 1.000 iteraciones L-BFGS-B en todos; tampoco se reclama convergencia.

| Semilla local | Tiempo generación + certificado | Máx. media S restringida | Máx. S restringido | Máx. razón de varianzas R4/R5 | Máx. pico S/N no optimizado | Máx. solapamiento relativo |
|---|---:|---:|---:|---:|---:|---:|
| 1101 | 6,705 s | 0,227986 | 0,567900 | 0,315586 | 0,328060 | 0,000547 |
| 1102 | 6,587 s | 0,135435 | 0,339640 | 0,222186 | 0,321196 | 0,000254 |
| 1103 | 6,315 s | 0,100453 | 0,286579 | 0,204063 | 0,390353 | 0,001113 |

Todos conservan distancia mínima >0,6908, 2.400 arcos, SCC única y acceso completo. Las medias de arista son 1,104791/1,106980/1,107551, frente a 1,104165/1,104667/1,105435 en full. Los RMS de puertos son 0,421923/0,442930/0,413563 y los máximos 0,881915/0,808801/0,752096. Parecido aspecto visual y conectividad no implican el mismo espectro: precisamente esta comparación mide ese fallo de interpretación. El término espectral modifica la geometría final y por ello también grafo/puertos/distancias; esas diferencias no se presentan como controles exactamente emparejados de mecanismos locales.

Se conserva una incidencia numérica y su resolución: la verificación original de gradiente de local 1103 con epsilon=1e-6 no pasa la tolerancia, error máximo 2,544e-5. En la coordenada 375 el par de nodos 187/17 queda a 5,55e-9 de su corte de empaquetamiento. El hinge cuadrático es C¹, con segunda derivada discontinua en ese punto: la diferencia finita central atraviesa el corte para epsilons grandes. Se midió convergencia del error con epsilon 1e-5/1e-6/1e-7/1e-8: 2,578e-4/2,544e-5/2,212e-6/1,610e-8; el último pasa. El fallo original permanece en `*_gradient.json`, no se reescribió. `avian_local_only_N400_g1103_gradient_convergence.json` retiene todas las comprobaciones; no se cambió el gradiente ni la geometría para obtener el pase. Los otros dos gradientes locales pasan la verificación inicial. Una futura modificación de la energía debe repetir ambas verificaciones aleatorias y cerca de contactos.

`summary_local_only.json` separa `packed_control_count=3` de `finite_MHU_admitted_count=0`. Su figura indica explícitamente control empaquetado con certificado MHU fallido; la generación local se llama con `python -m larp.avian_local`, no con el filtro de admisión MHU de la ruta genérica. El código full conserva su hash exacto `08dc1a3a45195963cab81a910cbed589e73d8460a4d46a5fa7736cc563e6edfd` y sus manifests intactos. No hay entrenamiento, comparación de capacidad ni actualización posterior de arquitectura.

## Auditoría posterior de procedencia

`artifacts/avian_v1/provenance_audit.json` verifica los seis manifests individuales contra los NPZ y contra los archivos de código actuales. Todos coinciden. Full y local comparten ocho archivos con SHA-256 idénticos, incluido `avian.py` con el objetivo científico, la configuración, certificación, grafos, puertos y referencia primaria. Comparten igualmente Python/NumPy/SciPy/psutil. La identidad agregada difiere porque local añade `avian_local.py` al conjunto de archivos, no porque `avian.py` haya cambiado de versión.

La lectura directa de los dos wrappers confirma igual inicialización `[20261008,semilla,intento]`, radio de crecimiento, LR, correcciones de momentos, 6.000 pasos Adam y opciones/callback de L-BFGS-B. Local usa el mismo `avian_objective`, con el término espectral omitido; los términos locales permanecen idénticos. Su política de selección evita exigir una certificación MHU positiva, diferencia deliberada para no condicionar la ablación al fenómeno que se intenta retirar. Las seis realizaciones terminaron en intento cero, por lo que aquí no se introdujo un reintento diferencial. Las diferencias de coordenadas y microestructura final sí permanecen como limitación real de atribución al mecanismo de ondas largas.
