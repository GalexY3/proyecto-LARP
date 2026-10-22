# Encargo a Sol/ChatGPT — replay T2, máximo 30 minutos

**Este es el encargo vigente para la próxima sesión. Sustituye el plan de exploración de 60 minutos; los documentos anteriores del kit son referencias históricas.** No abras seis vías nuevas. Ejecuta un piloto que compruebe si la mejora de lectura factorizada se reproduce y entrega archivos reales antes de agotar el tiempo. Si falta capacidad, entrega un diagnóstico y código no ejecutado claramente etiquetado.

## Objetivo y materiales

Los resultados neuronales anteriores se perdieron: las mejoras comunicadas MHU/LOCAL no están verificadas. La inversión algebraica T2 sí está auditada. Queremos reproducir el signo y magnitud de la mejora con los pesos congelados, sin afirmar causalidad MHU ni originalidad académica.

El paquete incluye este encargo, `session_clock.py`, el kit previo intacto en `inputs/` y el dictamen de rescate en `references/`. **Lee primero solo este encargo.** Descomprime el kit previo únicamente para obtener código, configuración, geometrías y recibos; no ejecutes su encargo antiguo de una hora ni sus runners de entrenamiento.

Los pesos van en otro adjunto: `LARP_FROZEN_MODELS_N32768_G3201_20261011.zip`, SHA256 `36852d49684fd95e8a195cc8249ededce3e936e70043d3b447be52146669c214`. El `.pt` contiene tres estados, N32768, g3201, u1800; SHA256 `ddc944a49198be0202e387158ce73f989bd5bdd134c9aaa696dcecc7fb05c598`. No contiene optimizadores. Si ya está accesible en la conversación, úsalo. Si no está o falta PyTorch, registra `NOT_RUN_CAPABILITY`; no pases la sesión buscando o instalando dependencias.

## Tiempo y persistencia

Inicia en tu primer acceso a herramientas:

```text
python session_clock.py start --run-dir output/session --minutes 30
```

Usa reloj real y eventos. No simules duración ni esperes para rellenarla. El límite incluye preparación y entrega. **A los 25 minutos cesa el cálculo científico y empaqueta.** Comprueba tiempo entre mundos y etapas; no arranques una operación que pueda consumir el margen de cierre. Si no existe reloj, declara duración no verificable.

Ejecuta extracción y ajuste en bloques que vuelvan a la conversación en aproximadamente 60 segundos o menos, con guardado entre bloques. Estima el tamaño de bloque tras el benchmark. Esto permite comprobar tiempo, emitir los enlaces parciales y cortar antes del cierre.

| Minutos | Trabajo |
|---|---|
| 0–4 | Verificar materiales, cargar fuente/pesos y medir un forward por brazo |
| 4–18 | Extraer features/targets y guardar; ajustar ridges |
| 18–23 | Controles secundarios si el coste medido permite completarlos en los tres brazos |
| 23–25 | Una única evaluación de test y tabla |
| 25–30 | Cerrar reloj, verificar archivos y entregar ZIP final |

Guarda config, script y logs desde el principio; arrays después de cada brazo/split. **Publica un ZIP parcial alrededor del minuto 8**, con lo que exista, aunque todavía no haya resultados. Al minuto 20 actualiza/publica otro parcial. Excluye los pesos para evitar duplicar 54 MB. Los ZIP pueden compartir archivos: no son experimentos distintos. Una entrega parcial honesta tiene prioridad sobre terminar todas las pruebas. La persistencia de archivos fuera de la sesión no está garantizada.

## Dataset y acceso fijo

Trabaja solo con N32768/g3201/u1800 y **MHU, LOCAL y RANDOM**. `SpatialNetwork(256,8)`, grado16, tarea2, `eval` e `inference_mode`. Fuente: `src/larp/scale3d_train.py`; config: `configs/scale3d_v2.json`. Carga estados con `weights_only=True` y carga estricta.

Usa 32/8/32 mundos train/validation/test, 16 queries por mundo, coeficientes y queries idénticos entre brazos. Semillas de mundos: `2026111000+i`, `2026111100+i`, `2026111200+i`; queries NumPy: `2026111300+i`, `2026111400+i`, `2026111500+i`; i es índice dentro del split. Mantén mode-seed, bandas, normalizaciones y observación del canal propio originales. Son semillas locales nuevas; desconocemos las de la corrida perdida.

Captura mediante hook **antes de `model.head[0]`** las 265 features originales: pool256 + sin/cos query6 + tarea3. Obtén simultáneamente la predicción original O en el **mismo forward**. No guardes todos los estados N×256 ni selecciones capas, vecinos o patrones nuevos.

Son 216 forwards B=1. Antes de generar el dataset estima carga, generación, inferencia y guardado completos. Si extracción no cabe en el tramo presupuestado, entrega `NOT_RUN_BUDGET` y evidencia parcial. No reduzcas N, cambies la tarea ni omitas RANDOM para obtener un resultado. Si una interrupción deja splits incompletos, conserva los datos y marca el contraste primario incompleto; no presentes un subconjunto seleccionado como el piloto terminado.

## Lecturas mínimas

- **O:** cabeza histórica congelada, predice productos T2.
- **R-Y:** ridge directo a las cinco etiquetas T2.
- **R-F:** invertir únicamente etiquetas T2 de train, ajustar ridge a los cinco factores recuperados y componer los cinco productos al predecir.

Si `y=(p01,p12,p23,p34,t)`, usa float64:

```text
f0 = cbrt(t*p23*p01**2/(p34*p12**2))
f1 = p01/f0; f2 = p12/f1; f3 = p23/f2; f4 = p34/f3
```

Composición: `z0*z1, z1*z2, z2*z3, z3*z4, z0*z2*z4`. Las etiquetas limpias exactas identifican factores no nulos: esto no añade información supervisora, pero sí cambia objetivo y sesgo estructural. Verifica finitud y recomposición; no uses campos verdaderos del generador para entrenar R-F. Un fallo numérico se registra, no se resuelve excluyendo silenciosamente filas. No inviertas etiquetas test para predecir ni elimines consultas difíciles.

Normaliza las 265 features usando mean/std de train. Si std≤10⁻¹², divisor1; conservar columna centrada y registrar constante. Intercepto no penalizado. Ridge: minimizar `||XW+b-Y||²/n + lambda*||W||²`; grid `{1e-6,1e-4,1e-2,1}`. Selección por **MSE de productos T2 en validation**, también en R-F; empate: mayor lambda. Mismo grid por brazo. Guarda medias/std, coeficientes y candidato seleccionado.

## Dos controles secundarios, si caben

Decide por coste **antes de abrir test**, para los tres brazos o ninguno:

1. **L-P:** factores lineales + productos, entrenados directamente con pérdida T2, sin inversión ni objetivo de campos. Features estandarizadas, intercepto0, pesos gaussianos std=`1/sqrt(d)` con d=columnas no constantes train. Inicialización común, semilla2026111601. No inicialices todos los factores a cero.
2. **M-R:** copia de la cabeza original reajustada a T2, misma arquitectura y features sin estandarización externa. Backbone congelado.

Ambos: Adam lr0,001, weight_decay0, batch128, 500 pasos; candidatos100/300/500, selección por validation, empate menos pasos. Orden de minibatches común entre brazos/lecturas, semilla2026111602. Registra presupuesto, parámetros y tiempo; no cambies receta para rescatar un brazo. El factor lineal tiene1330 coeficientes; el MLP69911: no hay igualdad de parámetros entre familias.

Si no caben, marca `NOT_RUN_BUDGET`. O/R-Y/R-F todavía permiten una prueba de disponibilidad del decoder; **la atribución a composición, objetivo o optimización queda inconclusa sin los controles**. Fallo de M-R en500 pasos no prueba incapacidad universal. No metas ruido, g3202, nuevas tareas, barridos ni literatura extensa en esta sesión.

## Endpoint y entrega

Test se abre una vez tras fijar modelos. Reporta MSE por mundo, componente, lectura y brazo; pares y triple separados; incluye predictor cero. Principal: mejora absoluta `mean_MSE_O - mean_MSE_R-F`, promediando mundos y después por igual MHU/LOCAL. Mejora relativa: `1 - mean_MSE_R-F/mean_MSE_O`, **no media de ratios por brazo**. RANDOM y resultados individuales son secundarios.

Bootstrap descriptivo10.000 veces por mundo, semilla2026111700; conserva emparejados todos los brazos/lecturas de un mundo. Con32 mundos y una geometría, esto es **piloto**, no confirmación del protocolo mayor. Mejora≥3%, signo favorable en ambos brazos estructurados e intervalo de mejora absoluta por encima de0 justifican proponer réplica. Resultado incierto no autoriza añadir paneles hasta ganar. No actualizar H1–H6 numéricas.

Entrega `LARP_REPLAY_T2_30MIN.zip`: informe≤1000 palabras, scripts ejecutados, config/seeds/versiones, arrays de features/etiquetas/predicciones por mundo, ridges/heads ajustados, logs y manifiesto SHA256 (excluyéndose a sí mismo). Etiqueta lo no ejecutado y conserva resultados adversos. Comprueba CRC y archivos citados. Cierra con `python session_clock.py finish --run-dir output/session`, incluye recibo/trace y duración real. El reloj certifica tiempo transcurrido, no intensidad de razonamiento.

Una réplica pequeña completa o un límite de factibilidad verificable es suficiente. No necesitas alcanzar una puntuación de novedad, defender MHU ni completar artificialmente media hora.
