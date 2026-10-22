## AB-M029 — Selección adaptativa de cuotas y contaminación del holdout (PROPUESTA)

**Procedencia:** `GalexY3/proyecto-LARP`, `research/VALUE_REAL_20261022/`, ensayo exploratorio 2D con parches RGB reales del 22-10-2026. **Estado:** propuesta metodológica contextual, no adopción normativa ni nueva versión AB.

**Problema:** la cuota [6,16,2] se seleccionó después de inspeccionar resultados de las dos escenas externas, aunque cada diseño de disposición solo vio los cuatro archivos de entrenamiento. Un algoritmo puede estar libre de *data leakage interno* mientras la decisión del investigador produce *test-set leakage adaptativo* mediante selección retrospectiva del ganador. La confirmación de [6,16,2] exige un tercer entorno verdaderamente nuevo con cuotas/hiperparámetros congelados antes de observarlo.

**Propuesta:** añadir al registro de validación `design_data_seen`, `selection_data_seen`, `metric_reused_as_holdout`, `number_of_external_environments` y `unit_of_replication`. No presentar 800 parches de una misma fotografía como 800 réplicas independientes. Separar mejoras por distribución de cuotas, geometría, lectura entrenada y costes.

**Evidencia a favor:** la discrepancia entre selector directo con 12 parches (muy buen ajuste de entrenamiento, peor transferencia) y con 1.800; cuota seleccionada post hoc; solo dos escenas independientes. **Contraevidencia:** estas precauciones ya están implícitas en R3/O2 y por tanto puede bastar una nota de aplicación, sin regla nueva. **Falsador de utilidad:** evaluar si los metadatos adicionales evitan efectivamente falsos positivos frente a registro estándar; pendiente.
