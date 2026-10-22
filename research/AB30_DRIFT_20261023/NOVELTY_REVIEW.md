# Revisión adversarial de novedad posterior a AB30 Drift (23 octubre 2026)

**Conclusión:** NO reclamar originalidad 2/3 para «monitorizar drift relevante para la decisión» ni para «usar pérdida estimada con etiquetas escasas». Esas líneas tienen antecedentes sustantivos.

1. Koebler et al., *Incremental Uncertainty-aware Performance Monitoring with Active Labeling Intervention*, AISTATS 2025, https://proceedings.mlr.press/v258/koebler25a.html . Monitorizan cambios de rendimiento sin etiquetas mediante transporte óptimo y usan etiquetado activo bajo presupuesto.
2. Zhang, Cai, Yu y Simeone, *Prediction-Powered Risk Monitoring of Deployed Models for Detecting Harmful Distribution Shifts*, ICML 2026, https://proceedings.mlr.press/v306/zhang26g.html . Alertas de drift perjudicial con combinación de etiquetas sintéticas/reales, límites de riesgo en línea y garantías de error tipo I.
3. *Explanatory Model Monitoring to Understand the Effects of Feature Shifts on Performance*, KDD 2024, https://doi.org/10.1145/3637528.3671959 . Explican pérdidas de rendimiento por desplazamientos de características usando transporte óptimo y Shapley.
4. Kim (2024) sobre sensores con ruido correlacionado, https://link.springer.com/article/10.1186/s13634-024-01127-1 ; Krause et al. (2008) observaciones robustas https://www.jmlr.org/papers/v9/krause08b.html .

**Consecuencia AB-H:** DRIFT-P06 sigue siendo una HIPÓTESIS NO VALIDADA, no aportación nueva. La identidad de riesgo `tr(K DeltaSigma K^T)` es álgebra lineal estándar y podría ser una parametrización útil, pero solo puede proponerse un avance concreto si mejora ante estos rivales con mismo acceso a información/etiquetas, errores de falsa alarma y costo computacional, en flujo externo prospectivo. Se deben revisar también su identificación y el efecto de reentrenar K.

**Estado:** revisión de literatura inicial, no revisión sistemática exhaustiva. Evidencia de antecedentes, no inferencia de que toda posible especialización futura sea imposible. Mantener la condición 2/3 como NO ACREDITADO, no asignar créditos por repetir resultados.
