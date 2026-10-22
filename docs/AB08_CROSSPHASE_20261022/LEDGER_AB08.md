# Ledger secuencial · LARP AB 3.2.1 · ocho ciclos adicionales

**Fecha:** 22-10-2026. Ocho ciclos efectivamente ejecutados, con fuente Python y JSON por ciclo. C01–C07 fueron planeados inicialmente como módulos y ejecutados secuencialmente; el protocolo C08 se programó tras observar resultados C01–C07. Por tanto branching **parcialmente adaptativo**, no ocho protocolos independientes congelados antes de cada experimento. Cuatro geometrías Scale3D originales, compartidas por todos los ensayos. Las 96 traslaciones, 2000 mundos de test y los modos Fourier NO son nuevas geometrías.

### 01. ¿Qué parte de la supresión de unión proviene de los términos cruzados entre tipos?
**Resultado:** CONTINUE. **Siguiente pregunta decidida:** Desplazar clases sin alterar sus autospectros y medir efecto. **Fuente numérica:** `results/C01.json`. **Alcance:** Atribución algebraica de Fourier; misma banda optimizada y cuatro semillas, no ventaja neural.

### 02. ¿La coordinación intertipo aporta algo más allá de los autospectros S_a?
**Resultado:** CONTINUE. **Siguiente pregunta decidida:** Examinar señales compartidas frente a independientes. **Fuente numérica:** `results/C02.json`. **Alcance:** Traslaciones mantienen cada S_a exactamente, modifican S_union y cobertura; correlación espectral cruzada es mecanismo clásico.

### 03. ¿Cambia la utilidad de las fases cruzadas al variar correlación funcional y pesos por tipo?
**Resultado:** CONTINUE. **Siguiente pregunta decidida:** Repetir fuera de banda para descartar función fabricada a favor. **Fuente numérica:** `results/C03.json`. **Alcance:** Estimación de DC con campos gaussianos toroidales conocidos; fórmula matemática valida MC, no generalización neuronal.

### 04. ¿Persiste la ventaja por fase cruzada en frecuencias realmente no optimizadas?
**Resultado:** CONTINUE. **Siguiente pregunta decidida:** Intentar construir el mismo efecto con un comparador de bajo coste mediante traslaciones optimizadas. **Fuente numérica:** `results/C04.json`. **Alcance:** La banda fuera de corte es pos-seleccionada y el conjunto de modos finite; no holdout confirmatorio.

### 05. ¿Puede recuperarse acoplamiento mediante traslaciones convencionales manteniendo los S_a?
**Resultado:** CONTINUE. **Siguiente pregunta decidida:** Probar la sensibilidad al ruido y presupuestos de sensores. **Fuente numérica:** `results/C05.json`. **Alcance:** Optimizamos 12 grados de traslación en bandas in-sample; prueba hold-out low no es independiente de entrenamiento original MHU. Tiempo de generación no equiparado.

### 06. ¿La ventaja de fases cruzadas resiste el coste de pérdidas de sensores?
**Resultado:** CONTINUE. **Siguiente pregunta decidida:** Entrenar una lectura aprendida con target variable y comprobar si diferencia es útil. **Fuente numérica:** `results/C06.json`. **Alcance:** Se renormaliza media por tipo tras dropout; no simula costes de red; mismos mundos matemáticos, distinto ratio de sensores.

### 07. ¿Persiste el efecto en una lectura aprendida con objetivo no trivial, sin fórmula fija?
**Resultado:** CONTINUE. **Siguiente pregunta decidida:** Auditar si el mejor rendimiento es también nuevo y suficiente para redes reales. **Fuente numérica:** `results/C07.json`. **Alcance:** Ridge no es Transformer/GNN; las distribuciones de entrenamiento y prueba comparten generador y banda baja optimizada; geometrías n=4.

### 08. ¿Generaliza una lectura entrenada con señales compartidas bajas a frecuencias nuevas?
**Resultado:** CLOSE_BLOCK_REQUEST_DECISION. **Siguiente pregunta decidida:** Evaluación del bloque, novedades, solicitud de ciclos posteriores por valor de información. **Fuente numérica:** `results/C08.json`. **Alcance:** OOD relativo al objetivo espectral de Scale3D; reusar familia espacial Fourier y no disponer de Wei auténtico limitan novedad 2/3. El readout no prueba arquitectura de lenguaje.

**Fuente del protocolo:** `src/ab08_shared.py`; códigos anteriores y archivos de geometría tomados de `LARP_AB30_LIBRE_20261022_VERIFICADO.zip`, SHA incluidos en `manifest.json`. Sin nuevos modelos LLM, sin benchmark del algoritmo Wei ejecutado.
