# LARP — 30 ciclos exploratorios de ramificación adaptativa (22-10-2026)

## Alcance
Disposición espacial real de **54 sensores Intel Berkeley**, recuperada del archivo `mote_locs.txt` del laboratorio. Sus **mediciones de temperatura, humedad, iluminación y voltaje NO se han obtenido**. Los campos, ruido, objetivos, tres roles y fallos son sintéticos; tampoco se midió conectividad inalámbrica ni coste energético. La campaña no reproduce el generador Scale3D ni el COSI histórico: compara explícitamente **proxies**.

## Protocolo
30 problemas distintos, previstos antes de empezar, con **orden de ejecución elegido secuencialmente** según el ganador y margen del ciclo previo. Familias: escenario espacial, pocos pilotos, cambio de distribución, correlación entre tipos, objetivos locales/no lineales, ruido, dropout, presupuesto y distancia como coste teórico. Cada ciclo utiliza 54 posiciones físicas reales, 162 lecturas posibles (3 roles), seis diseños y el mismo estimador Ridge. El conjunto de evaluación se consultó adaptativamente para decidir ciclos posteriores, por lo que todo es **exploratorio, no confirmatorio**.

## Auditoría
Un primer runner regeneraba por error los centros espaciales RBF en cada split, introduciendo un cambio de generador no declarado. Ese registro inicial se conserva como INVALID para el estimando estacionario. Se separaron las semillas estructurales y las de muestreo y se reejecutaron las mismas 30 condiciones como **REPAIR**, no como 60 ciclos. Tests de unicidad, tamaño, cardinalidad de selección, finitud y distancia correlacional pasan.

## Resultados del registro reparado
| Método | Victorias entre 30 condiciones |
|---|---:|
| Greedy orientado al estimando | 18 |
| COSI_PROXY | 6 |
| ROLE_DIAG | 2 |
| LOCAL_PROXY | 2 |
| RANDOM | 2 |
| FPS | 0 |

Una política de selección por validación entre seis algoritmos alcanza RMSE medio descriptivo 0.149708 en las 30 tareas heterogéneas, frente a 0.163876 de greedy orientado al objetivo y 0.176519 de COSI_PROXY; el mínimo ex post por condición es 0.147097. En 56 ejecuciones auxiliares escogidas **tras ver las primeras 30**, la política promedia 0.105493 y greedy 0.117319. Ni 30 ni 56 son dominios físicos independientes, y las escalas de los objetivos difieren.

## Interpretación
No hay ventaja universal MHU/COSI. La elección de estrategia condicionada por la tarea y sus datos de validación es una posibilidad de ingeniería, **no un algoritmo científicamente inédito**. La selección por validación y los diseños submodulares/GP son antecedentes consolidados. **AB-DECIDE: STOP** de repetir el mismo generador; **FOCUS** en contraste físico con mediciones multisitio, comunicación observada y competidores expertos.

## Evidencia preservada
El paquete completo `LARP_BRANCH30_NEW_20261022.zip` se generó en la conversación asociada a esta campaña; contiene fuente Python, decisiones por ciclo, ledger válido e inválido, auditorías, comparaciones post hoc, figuras e índices SHA-256. SHA-256 del ZIP: `c1286aeed8b91d6b5813080de61c95de1fc14133e5f0b592fe4b13321f743bd3`. **Los ficheros íntegros del ZIP aún no se han incorporado todos a este repositorio**; este índice documenta el resultado pero no sustituye el archivo de evidencia.

Fuentes: [Intel Lab original](https://db.lcs.mit.edu/labdata/labdata.html); [mirror de posiciones](https://github.com/linsea423/Intel_Lab_Data/blob/master/mote_locs.txt); [Krause et al. 2008](https://www.jmlr.org/papers/v9/krause08b.html); [Wei 2010](https://www.liyiwei.org/papers/noise-sig10/).
