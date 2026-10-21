# Anexo acumulativo de priors LARP (BR30 dinámico)

**Priors nuevos BR30-D16–D21**. Son actualizaciones cualitativas, no probabilidades bayesianas calibradas; la fuente es el estudio exploratorio C01–C08. Integrar al ledger maestro conservando priors anteriores BR12/BR30 sin borrar contradicciones.

| ID | Procedencia / proposición | Favorable | Contraria / incertidumbre | Falsador / siguiente prueba | Estado |
|---|---|---|---|---|---|
| BR30-D16 | C01/C02: el generador original Scale3D v1/v2 es recuperable y ejecutable en CPU. | Exact hash y cuatro seeds x 600 iteraciones. | No se cotejó bitwise con todos los checkpoints históricos. | Comparación contra archivos históricos en mismo hardware/software. | TECNICO_VERIFICADO limitadamente |
| BR30-D17 | C03/C04: MHU mejora sistemáticamente la reconstrucción bajo agujeros espaciales. | Seed 5201 MHU .147 vs LOCAL .166; seed 5204 MHU .184 vs LOCAL .205. | Seeds 5202/5203 invierten; media −.00253, IC descriptivo cruza cero. | Nuevas geometrías y perturbaciones de naturaleza distinta fijadas antes de test. | NO_VALIDADO |
| BR30-D18 | C05: la supresión espectral finita MHU crea una topología kNN mejor para aprendizaje. | Brecha Laplaciana .03416 MHU vs .03385 LOCAL. | CVT .0334–.0336; efecto pequeño; no mide aprendizaje. | Mostrar mejora de aprendizaje con mediación topológica y recursos iguales. | SINTETICO_EXPLORATORIO |
| BR30-D19 | C06/C07: LOCAL ofrece ventaja neuronal reproducible vs MHU/CVT. | LOCAL gana por .0027–.0042 en una seed. | Orden cambia en otra seed y entrenamiento incompleto; CVT reusable. | Convergencia/replicaciones verdaderas/benchmarks no construidos para suavidad. | NO_VALIDADO |
| BR30-D20 | C08: presupuestos breves de aprendizaje pueden invertir rankings prematuramente. | Todos los mejores checkpoints al final y MSE mejora solo 7% vs cero. | No prueba que el ranking convergido difiera realmente. | Seguimiento de pérdidas hasta meseta por varias seeds con mismo compute. | PRIOR_METODOLOGICO_CONTEXTUAL |
| BR30-D21 | Validación: cuatro muestras MHU original reproducen supresión de banda finita para union y tipos. | Auditoría exacta FP64, todas superan criterio finito; S_union .00044–.00046. | No prueba HU asintótica, novedad ni valor para arquitectura. | Repetición en tamaños crecientes y medición función/coste. | SINTETICO_VERIFICADO_FINITO |
