# AB30 drift B04 — preregistro de datos reales: Diabetes
Version AB3.2.1/O1/O2. Congelación ANTERIOR a ejecutar. SHA256 del JSON íntegro que se ejecutará: 984aceb47b6d8ad46378af37ec756f386a3b1f3a6a6a76ab58e04c973d4e9ceb. SHA256 del motor: 867e75309dfa81c8568bb2360d4cb4909560a338d7f16a587d03bba877f1deb6.
Causa del branching: tras 18 contrastes sintéticos, no se logró distinguir ventaja robusta consistente ante comparadores competentes. Abandonar el generador; pasar a dataset público diabetes de scikit-learn (442 filas, 10 covariables, regresión).
Splits: 16 semillas 1500..1515; 70% train, 30% test, con train separado en subtrain/validación para búsqueda greedy. StandardScaler ajustado solo al subtrain; modelo Ridge(alpha=10); k=3 o 6 variables. Endpoints MSE en test, delta método-control; intervalos pareados descriptivos, reutilización adaptativa de un único dataset.
- T19 stable vs filter, k=3: estabilidad en submuestras supera filtro por correlación;
- T20 wrapper vs filter, k=3: greedy por error de validación supera correlación;
- T21 wrapper vs stable, k=3: greedy supera estabilidad;
- T22 filter vs random, k=3: selección informada supera azar;
- T23 wrapper vs full, k=6: greedy supera el Ridge de diez variables;
- T24 stable vs full, k=6: estabilidad supera Ridge de diez variables.
Todos falsables si delta>=0; preferencia no impuesta por regla. Rivales: ajuste excesivo a validación, full ridge competente, selección inestable por colinealidad. No hay réplica externa ni validación causal. Los registros brutos y manifiesto JSON por semilla se archivarán preservando este SHA.
