# LARP AB45 · Exploración adaptativa en cuatro datasets observados

- `DICTAMEN.md`: resultados, incertidumbre y dictamen 1/3.
- `campaign.py`: política explícita de decisión después de cada resultado de validación. 45 ciclos únicos.
- `decision_events.jsonl`: decisión y justificación escribiéndose **antes** de ejecutar cada ciclo.
- `cycles.jsonl`: error por brazo y subset de variables elegido.
- `SUMMARY.json`: 45 victorias de validación y 4 pruebas test finales, usadas una vez.
- `audit.py`/`AUDIT_TEST.json`: bootstrap post-hoc pareado, no confirmatorio.
- `verify.py`: invariantes de partición, cadena de decisiones, cuotas de features, normalización.
- `INVALID_DOUBLE_SCALE_*`: primera campaña exploratoria invalidada por doble transformación del evaluador.
- `PRIORS.md`, `NOTA_AB_M034.md`: registros acumulativos sin alterar protocolos anteriores.

Reproducir:
```
pip install numpy scipy scikit-learn matplotlib
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python campaign.py 45
OPENBLAS_NUM_THREADS=1 python verify.py
OPENBLAS_NUM_THREADS=1 python audit.py
python build_report.py
```
**Atención:** volver a ejecutar `campaign.py` reescribe el ledger validado y vuelve a abrir el test; mantener hashes originales antes de hacerlo. No afirmar confirmación nueva. Los datos proceden de `sklearn.datasets` instalado localmente; licencia/procedencia según paquete original.

Esto NO es Scale3D MHU ni COSI histórico, ni arquitectura neuronal, ni datos espaciales multisensor reales. Es una prueba de portabilidad conceptual que principalmente identifica límites a la originalidad.
