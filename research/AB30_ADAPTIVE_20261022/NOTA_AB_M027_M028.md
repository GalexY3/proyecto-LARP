# Nota al observatorio AB — AB-M027/AB-M028 (22-10-2026)

**Fuente:** campaña sintética LARP BR30-A, `GalexY3/proyecto-LARP` (rama de investigación), `DICTAMEN.md`, `run_ab30.py`, `ledger.jsonl`, `repair_optim.json`. Estas observaciones **no modifican el núcleo AB 3.2.1 ni O1/O2** ni prueban superioridad metodológica.

### AB-M027 — GATE de comparador informacional y optimizador estable
**Problema confirmado dentro del código experimental:** en C27, el optimizador «oráculo» que conocía la covarianza verdadera obtuvo RMSE fuente peor que MHU por comportamiento de pasos y repulsión intercalada. Una reparación post hoc con descenso monótono recuperó el orden esperado en C27. **Propuesta:** antes de atribuir mejora a geometría, exigir control de descenso, sensibilidad al optimizador y comparador igualmente informado si el modelo candidato usa pilotos auxiliares. Preservar el resultado inicial y el repair sin renumerar sus ciclos. Falsador: problemas genuinamente no convexos donde oráculo local no domina sin multi-start; no exigir garantía universal de óptimo global. **Estado:** PROPUESTA — eficacia AB no validada.

### AB-M028 — BRANCHING adaptativo acotado, no exploración irrestricta
**Observación:** el scheduler eligió familias según regret y cobertura de seis alternativas predefinidas; 30 filas con parent, freeze hash y estado previo sí existen, pero las 30 pruebas reutilizan el mismo DGP sintético. **Propuesta:** además de contar ciclos, registrar espacio de decisiones disponible, contrafactuales no seleccionados, eventos de REPAIR fuera del cupo, y criterio explícito de detener la familia cuando falte evidencia nueva. Un scheduler adaptativo no crea nuevas fuentes empíricas por el mero orden secuencial. **Estado:** PROPUESTA — no implica AB 3.3 ni actualiza A01–A21.
