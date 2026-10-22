# LARP — Resultado descriptivo de escala 3D

Estado del job: `INCOMPLETE_OR_INVALID`.

**ESCALA INCONCLUYENTE:** falta cobertura válida de las ocho tríadas o un endpoint global común registrado. No se presenta una curva global.

Las filas disponibles son comparaciones independientes por N con dos semillas y un checkpoint propio común; no permiten extrapolar una tendencia de escala.

| N | Tarea | Paso | MSE MHU | MSE LOCAL | MSE RANDOM | MHU/LOCAL | MHU/RANDOM |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1024 | 0 | 1800 | 0.0968661 | 0.0926878 | 0.20117 | 1.04499 | 0.481523 |
| 1024 | 1 | 1800 | 0.566454 | 0.553225 | 0.660886 | 1.02388 | 0.857624 |
| 1024 | 2 | 1800 | 1.00962 | 1.00975 | 1.00974 | 0.999871 | 0.999879 |
| 4096 | 0 | 1800 | 0.0259549 | 0.0238959 | 0.080411 | 1.08641 | 0.325181 |
| 4096 | 1 | 1800 | 0.155047 | 0.133424 | 0.287951 | 1.16851 | 0.540029 |
| 4096 | 2 | 1800 | 1.01001 | 1.00972 | 1.00893 | 1.00028 | 1.00107 |

MSE: media de dos semillas geométricas. Cocientes: media de dos cocientes emparejados; un denominador cero deja el cociente sin definir. CSV contiene mínimos y máximos entre semillas, sin intervalos inferenciales.

En el paso 300 sólo se ha entrenado la tarea 0; hasta el paso 600 la tarea 2 aún no entra en el currículo. Sus evaluaciones tempranas no miden competencia después de entrenarla.

Se escala densidad en un toro fijo con parámetros, grado y profundidad constantes; el alcance físico cambia. Geometría y conexiones cambian juntas. El certificado MHU es finito, LOCAL puede también suprimir potencia espectral, y dos semillas no constituyen confirmación concluyente. No se declara superioridad general ni se actualizan los priors históricos H1–H6/C.
