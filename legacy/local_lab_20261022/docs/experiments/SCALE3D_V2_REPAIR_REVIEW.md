# Revisión adversarial de la reparación del generador 3D

**Fecha:** 2026-10-10. **Tipo:** diagnóstico exploratorio e inferencia analítica; no ejecución GPU ni prueba de superioridad MHU. Se han leído `AGENTS.md`, la carta AB 2.1, el protocolo v1, el constructor y las auditorías guardadas. El encargo humano «corrijamos» autoriza la reparación; v1 y sus resultados conservan su clasificación e historia.

## Diagnóstico concreto

Las cuatro realizaciones grandes fallaron la puerta de primera capa. En N=16384, la media de primera capa del tipo 0 fue 0,2811 y 0,2450; en N=32768, los tipos 0/1 alcanzaron 0,3596/0,4199 y 0,1934/0,2784. La unión sí pasó en todos esos casos. A la vez, las medias de las muestras de la banda baja quedaron aproximadamente entre 0,0002 y 0,0044. No es evidencia de imposibilidad de MHU en 3D: el promedio de miles de modos ocultó unos pocos modos muy lentos. Tampoco es aún un diagnóstico demostrado de toda la banda, porque v1 muestreó como máximo 128 modos por componente.

## Una intervención razonable

Recomiendo sustituir únicamente el peso espectral constante por peso inverso de la norma entera al cuadrado, sin tocar cutoff, shells completos, inicialización, etiquetas, 600 iteraciones, término local, calendario del optimizador ni entrenamiento:

\[
 w_c(m)=\frac{h(m)\,1_{0<|m|^2\leq K_c^2}/|m|^2}
 {\sum_{m'}h(m')\,1_{0<|m'|^2\leq K_c^2}/|m'|^2}.
\]

`h` es la multiplicidad hermítica de la representación rFFT. Normalizar por separado unión y cinco tipos; conservar después la mezcla original 0,5 para unión y 0,1 para cada tipo. Excluir explícitamente el modo cero antes de dividir. El cambio es isotrópico y no selecciona direcciones, semillas o sólo los tres modos de la puerta.

La justificación es **inferencia propia**, no un resultado publicado ni garantía bajo Adam. Para `S_c(m)=|sum_j exp(2π i m·x_j)|²/n_c`, el Jacobiano de la amplitud contiene un factor `|m|`; una aproximación de relajación modal tiene curvatura proporcional a `w_c(m)|m|²`. Los pesos inversos compensan esa dependencia. En tres dimensiones hay O(K³) modos: el peso constante de la primera capa decrece como N⁻¹. La suma de `1/|m|²` crece como O(K), de modo que el nuevo peso de primera capa decrece como N⁻¹ᐟ³. Se reduce la dilución, pero Adam, interferencias entre componentes y CIC impiden convertir esto en una tasa de convergencia exacta.

## Riesgos que la reparación no resuelve

- **Desplazamiento del error:** la periferia recibe relativamente menos peso. Calcular la banda baja completa mediante sumas continuas FP64, además de conservar las primeras capas, máximos y bandas exteriores. Mantener las medias ≤0,20; no admitir por una media ponderada que favorezca la nueva función objetivo. El máximo queda diagnóstico, como en v1.
- **Impronta de rejilla:** v1 tiene fracciones coherentes `S/N` de aproximadamente 0,075–0,10 en los ejes de la rejilla CIC para MHU; LOCAL tiene aproximadamente 0,18–0,21. Es orden vinculado a la instrumentación y no una reproducción demostrada de retina desordenada. Conservar esta medida por brazo, junto con separación homotípica, p05 y CV de vecinos; informar diferencias. El nuevo peso puede cambiar también esas propiedades.
- **Tratamiento diferente:** v2 modifica el objetivo geométrico, no sólo su ejecución numérica. Las métricas neuronales de MHU-v2 no deben mezclarse silenciosamente con MHU-v1 en una sola curva. Congelar código/configuración nuevos, repetir o identificar claramente toda geometría de cada brazo; un LOCAL reutilizado necesita hashes idénticos y trazabilidad explícita.
- **Control no necesariamente no-MHU:** LOCAL ya pasa la puerta finita en ambos N=1024 y en una semilla N=4096. El contraste MHU/LOCAL mide la penalización adicional; RANDOM aporta el contraste convencional, confuso por cobertura y separación local. Mantener ambos.
- **Escala y competencia:** aumentar N sigue escalando densidad con 4,83 M parámetros, grado 16 y ocho capas. No es escalado paramétrico; el alcance físico se reduce. La tarea 2 próxima a MSE=1 sigue siendo incompetencia dentro de este presupuesto, no refutación de MHU. No cambiar arquitectura/currículo a la vez que el constructor.

## Condición de cierre

Una comprobación técnica nueva puede establecer que el mecanismo de reparación funciona; las mismas semillas fallidas no son confirmación independiente del diagnóstico. Si alguna realización vuelve a fallar la puerta exacta inalterada, conservarla y detener su tríada; no reemplazarla ni reducir el umbral. Sólo después de pasar la puerta procede la comparación neuronal emparejada. Dos semillas y este diseño exploratorio no justifican actualizar numéricamente los priors históricos ni afirmar que MHU mejora al escalar.
