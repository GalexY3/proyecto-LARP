# Actualización acumulativa de priors LARP · AB08 2026-10-22
Todas las probabilidades son **cualitativas**, no Bayes factors calibrados. Fuente por ciclo `results/Cxx.json`. Las entradas anteriores BR30-F01..F10 se preservan.

| ID | Proposición | Apoyo nuevo | Contraevidencia y ámbito | Estado |
|---|---|---|---|---|
| BR08-X01 | Coordinar fases cruzadas reduce potencia espectral conjunta | C01/C02: MHU 21.54x aumento tras shifts independientes, S_a constante | Igualdad algebraica conocida; banda in-sample; retícula mejor | FINITO_SINTETICO_VERIFICADO |
| BR08-X02 | La correlación funcional rho determina el valor añadido de fases cruzadas | C03 identidad rho P_total+(1-rho) P_diag, Monte Carlo | La per-type S_a explica parte importante y la identidad es matemática conocida | VERIFICADO_EN_DGP |
| BR08-X03 | Mejora MHU se generaliza a frecuencias diferentes | Ninguno | C04/C08 fuera de banda MHU peor que LOCAL; C08 MSE 3.16e-5 vs 1.71e-5 | REFUTADO_EN_ENSAYO |
| BR08-X04 | Coordinación MHU ofrece ventaja en readout aprendido | C07 Ridge MSE 1.28e-9 vs LOCAL 9.7e-7 | Retícula MSE 8.94e-12; 250 train, 2000 test, campos sintéticos low; no arquitectura neuronal compleja | BENEFICIO_CONDICIONAL_NO_NOVEDAD |
| BR08-X05 | Penalización multiclase añade robustez si desaparecen sensores | Ventaja bajo 10% dropout todavía leve | C06 50% dropout MHU~2.413e-4, LOCAL~2.421e-4 y retícula~2.417e-4 | DEBILITADA |
| BR08-X06 | Un optimizador de traslaciones recupera MHU sobre controles | C05 CVT reduce algunos modos entrenados | No recupera la supresión de MHU, empeora heldout en algunos; faltan Wei y coste comparable | NO_VALIDADO |

**Decisión AB:** observar arquitectura aprendida con señales compartidas *no-Fourier* y comparator Wei real antes de estimar probabilidad de 2/3.
