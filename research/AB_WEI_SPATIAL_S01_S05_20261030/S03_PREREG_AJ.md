# S03 — AB-R A–J, control adversarial de interpolación por longitud de onda real

Trigger: S02 resultados ya observados (ridge site-MSE 0.0000700363; baseline por índice 0.000234205). Esta prueba es EXPLORATORIA POST-S02, no confirmación nueva; responde a un baseline potencialmente incompetente. Concesión nueva 5, S01 reparado y S02 como tareas 1/2; 3 restantes antes de S03. No mezclar 9 históricos.

A: estimando MSE de B4 y B6 sobre mismos **34 folds por sitio** de S02, usando cinco bandas B1/B2/B3/B5/B7, pero interpolando con longitudes de onda físicas nativas en lugar de índices ordinales. Unidad sitio, misma fuente/splits (no observación nueva). Resultado auditable: si el baseline físico cierra el gap con ridge, la comparación inicial era parcialmente artefacto de implementación del rival.
B: rival H0 la interpolación física explica la ventaja de ridge; H1 ridge sigue superando control físico; H_otra diferenciales de SRF, aerosol, heterogeneidad no-lineal. No afirmar novedad MHU.
C: EXACTAMENTE centros oficiales reportados en repo fuente de investigación: S2A [443,490,560,665,705,740,783], S2B [442,492,559,665,704,739,780] nm; fuente src/data/gloria_loader.py blob 284f9cc05bce08a0cb214d9e7e6d6490a2c5a7a5, tools/satellite/run_acolite_batch.py blob e45a249114324eeda0bb71d1fbada44619cd4ab0, manifest SRF d94443ec147b6c67c27ad9b32782a24415514387. S2B official response SRF noted placeholder; centers treated approximations, not full SRF convolution. Predict B4= B3+(B5-B3)*(λ4−λ3)/(λ5−λ3); B6= B5+(B7−B5)*(λ6−λ5)/(λ7−λ5). Comparator: exactly the ridge outcomes published S02, independent from S03 code. Secondary: baseline ordinal from S02 to check improvement from physical spacing. No parameter fit, no new search.
D: freeze this text and S03_WAVELENGTH.js before outcomes, validate source blob and S02 frozen code result. A priori reject if folds site lists mismatch or any sensor unrecognized. No CI.
E: execute once and record all site MSEs + means, wins ridge vs physical and percentile heterogeneity. Re-run exact code for software replay only.
F: band centers are not spectral response curves, and sources include GEE surface reflectance vs water remote-sensing reflectance ambiguity; physical linear remains simplified. No actual scene image, no Wei run, no MHU architecture.
G: no independent outside-source replication. Same 329 rows as S02, 34 sites.
H: update prior on magnitude of baseline-choice effects; keep CT2 24/18.
I: grade 0/3. A positive ridge does NOT establish novelty, generalization to other missions or MHU benefits.
J: STOP this dataset after S03 unless a genuinely independent data type or benchmark is acquired. New-grant remaining = 2 if S03 succeeds; old 9 untouched.
