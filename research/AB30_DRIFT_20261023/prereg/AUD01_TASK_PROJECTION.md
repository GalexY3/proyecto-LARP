# Auditoría adicional A01 — deriva hacia covarianza relevante para la tarea (NO ciclo 31)

**PRE-EXECUTION** 2026-10-23. AB3.2.1+O1/O2. A partir de 30 contrastes que no muestran beneficio robusto universal, analizar el mecanismo del daño por deriva de covarianzas para un decodificador Bayes lineal fijo.

Contrato: y=Hθ+ε, θ~N(0,I2), ε con covarianza Σ, K=(I+HᵀΣ0⁻¹H)⁻¹HᵀΣ0⁻¹. Riesgo R(K,Σ)=||I−KH||_F²+tr(KΣKᵀ). Se seleccionan 3 de 9 sensores con nominal exacto, semillas 2000..2049, y se calculan dos perturbaciones PSD de igual norma Frobenius:
- Δ_null=λ vvᵀ con ||v||=1, Kv=0;
- Δ_aligned=λ uuᵀ con ||u||=1, u orientado al máximo valor singular derecho de K.

Predicciones preregistradas: |R(Σ+Δ_null)−R(Σ)| < 1e-10 cada mundo; R(Σ+Δ_aligned)−R(Σ)>0 cada mundo con K≠0. Las perturbaciones tienen EXACTAMENTE igual norma y siguen siendo covarianzas PSD.

Rival: un índice de severidad basado solo en ||ΔΣ||_F no discrimina daño, mientras el término tr(KΔΣKᵀ) sí. Esto es una identidad algebraica estándar, NO una nueva ley 2/3. El código de auditoría se añadirá después, con prueba y resultados brutos, y queda separado de la cuota de 30.

Falsadores: no invariancia bajo dirección null o igualdad del cambio de riesgo alineado; revisar valores singulares, bug de normalización y redondeo. Resultados sintéticos, sin agentes externos ni datos de campo.