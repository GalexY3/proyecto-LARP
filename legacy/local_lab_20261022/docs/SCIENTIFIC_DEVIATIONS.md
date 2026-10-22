# Registro de desviaciones científicas y límites

Fecha: 2026-10-08. Referencia: contrato principal E–M/Q/R y prompt de implementación. Este archivo registra diferencias o restricciones; el estado de ejecución y los números observados pertenecen a `IMPLEMENTATION_STATUS.md` y a los manifests. No declara tests `PASS` sin logs.

## Desviaciones del tratamiento nominal

**Ninguna modificación científica aprobada del núcleo nominal.** Se conservan generador, umbrales, Hamilton, grafos, modelo, tareas, optimizer, presupuestos y seeds. Las resoluciones operativas están en `ADR.md` y categoría (b) de `SPEC_AUDIT.md`. Esta afirmación describe el diseño implementado, no una garantía de ausencia de bugs; los tests y revisión verifican fidelidad.

| ID | Estado / alcance | Diferencia y manejo |
|---|---|---|
| `VIS_AVIAN_ALTERNATIVE` | Figura alternativa; fuera del preregistro | La visualización solicitada después de Astra usa tamaños/espaciado por tipo. El contrato exige repulsión común0,30. Se conservan imagen/script/arrays y antecedentes LOW_K_ONLY como material visual; no se importan como geometrías de corridas nominales. Incorporarlos científicamente requeriría nuevo factor/versionado y certificación antes de resultados. |
| `TEST_ONLY_REDUCTIONS` | Sólo tests técnicos | Configuraciones pequeñas, menos updates/pasos/centros o optimización reducida aceleran pruebas de interfaces. Se etiquetan técnicas y no pueden certificar MHU ni alimentar análisis científico. Un resultado sintético verifica software, no arquitectura. |
| `CPU_INITIAL_ENVIRONMENT` | Resolución operativa | El entorno instalado es CPU Python3.13 con cuatro threads. GPU es opcional y no forma parte del costo medido de CPU; cualquier ejecución futura con otro runtime informa lock/hardware nuevos. No cambia hiperparámetros según velocidad de una condición. |
| `BOUNDED_GEOMETRY_EXECUTION` | Límite de ejecución inicial | Un certificado completo N400 válido no acredita la validación3seeds×3tamaños. N1600/N6400 o centinelas no ejecutados conservan `NOT_RUN`; no se afirma una familia escalable por extrapolación. |
| `GATED_NOT_RUN` | Etapas posteriores | Implementar un comando o dry-run no equivale a ejecutarlo. Smoke fallido/invalidez/budget pueden impedir piloto o suite. Se conservan todas las condiciones ejecutadas, incluidas negativas, y no se sustituye la seed ni se elimina el fallo. |
| `BUDGET_REDUCTION` | Condicional; sólo antes de test | El paso1000→500 está previsto por contrato y debe fijarse para todas las condiciones en un registro resuelto con medición/estimación identificadas. No es permiso para reducir sólo rivales, cambiar batches o restaurar1000 tras ver scores. El manifest de presupuesto registra si se activa; este documento no presume que se haya activado. |

## Bloqueos pendientes de decisión científica

| ID | Rama bloqueada | Propuesta registrada, todavía no autorizada | Consecuencia experimental |
|---|---|---|---|
| `B_MATCHED_PAIR_DOMAIN` | C3 y atribución de ondas largas independientemente de mixing | Contar histogramas homotípicos sobre todas las parejas espaciales `i<j`, además de matriz de arcos. La implementación candidata debe etiquetar ese dominio explícitamente. | Contar sólo parejas conectadas produce otro control; no se usa una interpretación elegida por ingeniería como prueba de mecanismo. Nativa/shuffle permanece definido. |
| `B_SEPARATE_PORT_RELOCATION` | Copy con entradas solas/salidas solas desplazadas | Preregistrar asignación conjunta inyectiva para roles móviles/fijos o un régimen explícito de colisiones/coordenadas. | Dos Hungarian independientes pueden asignar roles incompatibles a una neurona con25canales. La reubicación conjunta es independiente y permanece ejecutable. Una colisión no se resuelve silenciosamente. |
| `B_D4_INTERVENTION` | Control de anisotropía, si el ensemble lo activa | Definir si D4 transforma puntos, puntos/puertos o también mundo/datos. | Transformaciones parciales cambian interfaz; globales pueden conservarla. La bandera individual se informa y no excluye automáticamente una geometría minoritaria. |
| `B_AB_ZERO_RESIDUAL` | Decisión AB cuando todas las diferencias por init coinciden exactamente dentro de cada geometría | Decidir modelo de observación discreto/ruido sustantivo o prior/límite inferior sustantivo antes de interpretar. | La posterior continua HalfNormal puede ser singular enσs→0. La cuadratura truncada se conserva como diagnóstico y se inhabilita decisión; no se finge precisión mediante el límite numérico1e−6. |

Localizaciones, argumentos y alternativas exactas: `docs/SPEC_AUDIT.md`. Estos bloqueos no son evidencia contra MHU; no justifican cambiar el tratamiento independiente.

## Límites conservados y confounds declarados

- El certificado es finito y dependiente de banda; no prueba hiperuniformidad asintótica, isotropía universal, cobertura funcional ni fidelidad retiniana.
- Igualar in-degree/E no iguala out-degree, reciprocidad, longitudes, SCC ni accesibilidad. La comparación de marcas conserva el grafo; comparar arquitecturas completas estima un paquete distinto.
- T/F tienen iguales parámetros y distinta factorización, rango activo y MAC. G tiene16parámetros menos. G no ve marcas y su desempeño no identifica el efecto multicomponente.
- Puertos cambian entre geometrías completas; su desplazamiento forma parte de utilidad arquitectónica. Nativa/shuffle conserva asignación y coord/data hashes. No se elimina el confound de interfaz mediante regresión descriptiva.
- Copy tiene entradas persistentes y mide routing, no memoria temporal. Fill8 es un cálculo lógico exógeno finito; obstáculos no podan el grafo neuronal.
- El control de recursos artificial obliga especialización por canal y sólo mide sensibilidad del ensayo. No demuestra valor de tipos libremente aprendidos.
- M1 con pesos fijos/relocalización de funciones es OOD y auxiliar; un efecto no demuestra mediación natural ni reemplaza el contraste matched reentrenado.
- Ejemplos, bits, mapas, máscaras, centros e inicializaciones no son nuevas geometrías. Confirmación requiere panel emparejado, splits nuevos, todos los fallos y selección previa.
- Éxito técnico, certificación y smoke no actualizan los priors H1–H6; un resultado negativo de aprendizaje detiene interpretación sin convertirse en posterior de inutilidad geométrica.

## Protocolo de cambios futuros

Para cada cambio científico: registrar ID y fecha, líneas del contrato, justificación mecanística, efecto sobre estimando/confounds, configuración y seeds, regla de gate y aprobación/resolución explícita; congelar nuevos hashes antes de abrir resultados. Conservar archivos y corridas anteriores. Un cambio de código que invalida pairing crea serie nueva; reanudar infraestructura conserva la serie y el estado RNG/checkpoint.

v0.1b puede cambiar GRU **o** T32 según diagnóstico, conforme M; no ambos simultáneamente ni como reparación silenciosa. K, generador aviar, plasticidad, 3D, lenguaje y edge-as-computation requieren sus nuevas hipótesis/gates. Una suite `NOT_RUN` por tiempo o bloqueo conserva ese estado, nunca equivale a evidencia de ausencia de ventaja.

## Corrección operativa ejecutada del wrapper CLI

El entrypoint `python -m larp` invocaba `main()` sin propagar su retorno: bloqueaba correctamente el entrenamiento, pero el proceso devolvía cero. Se corrigió a `raise SystemExit(main())` y se añadió una prueba real de subprocess. No cambiaron generador, modelo, datos, optimizer ni presupuestos. Se congeló otro commit y se repitieron tests, certificado, calibración y las mismas cuatro corridas XOR en `runs/series_cli_exitfix`; la primera serie permanece en `runs/calibration`/`runs/smoke`. Estas repeticiones verifican reproducibilidad y no añaden réplicas independientes. Los modelos/fallos previos se conservan; no se eligieron nuevas semillas ni se reintentó hasta obtener una victoria.
