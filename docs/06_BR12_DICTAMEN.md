# Dictamen final LARP · BR12 dinámico

**12 ciclos sustantivos / 12 autorizados, +12 no utilizados.** Rama geométrica detenida por falta de ventaja única; no existe 2/3 o 3/3.

1. Nuevas 12 geometrías por brazo a N=512: CVT por tipo 97,31% cobertura k16; LOCAL_derived 69,17%; iid 61,43%. **LOCAL_derived no es el original**.
2. Coordenadas originales N=4096: LOCAL 96,08% cobertura k16; CVT a 8 iteraciones 94,72%–96,52%; con 15 más, tres CVT llegan a 97,56%–97,68%.
3. Primera comparación de reconstrucción fija: MSE f1,k24, bandwidth .11 LOCAL=.1404, CVT no refinado media=.1542. **Parecía** favorecer LOCAL. El siguiente ciclo impuso calibración individual del estimador y refinó CVT: dev 8 mundos → test 12 mundos. MSE LOCAL=.1074, CVT refinado=.0893–.0922. **El ranking se invirtió**. Esta calibración no fue un confirmatorio pre-registrado, sino nueva exploración con datos apartados del ajuste.
4. MLP neuronal de cinco canales, tres inicializaciones: CVT refinado .1249–.1319; LOCAL .1478; MHU .1608. No es GNN original ni Transformer, así que no generalizar.
5. Al eliminar 60% de sensores, MHU logra MSE .474 frente a CVT ~.499 y LOCAL .531; es un efecto exploratorio no una superioridad universal. En f5 las mejoras se reducen.
6. Factor espectral finito promedio sobre 80 modos: MHU S_all=4.35e-6; LOCAL=.00294, CVT .051–.090, IID=1.16. Una reducción S(k) notable no implica mejor predicción en esta tarea. Ninguna de estas mediciones prueba hiperuniformidad asintótica.

## Gobernanza
La unidad independiente de generación geométrica es la geometría, no los mundos o consultas. Una única geometría LOCAL/MHU original implica ausencia de inferencia causal/general entre algoritmos originales. *CVT per-type* es una implementación de Lloyd del presente bloque, no el algoritmo auténtico de Wei (2010). Comparar ambas bajo el mismo nombre invalidaría la auditoría.

## AB-DECIDE
**STOP a investigar «LOCAL superior» con nuevos mundos Fourier y parámetros similares**. La hipótesis de cobertura funcional no está refutada como mecanismo útil, pero es terreno conocido: Wei 2010 y CVT por tipo. **REPAIR** sólo con código del generador original repetible en N4096, implementación Wei usable a 3D/4096, o datos sensoriales externos / entrenamiento GNN completo con baseline PointNet++. No activar +12 sin esas novedades. Se conserva facultad del usuario de continuar desde nueva evidencia, no una promesa de ejecución posterior.
