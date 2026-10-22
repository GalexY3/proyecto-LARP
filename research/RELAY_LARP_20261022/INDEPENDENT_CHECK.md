# Comprobación matemática independiente del relay

Este razonamiento se registró sin recibir todavía las respuestas delegadas. No constituye un experimento ni un ciclo AB adicional.

Con Z = X M, M de dimensión 64×80 y rango fila completo, pesos sensoriales A y pesos equivalentes B = M A, sea K = M Mᵀ y G = gradiente de la pérdida respecto de B. Entonces gradiente_A = Mᵀ G y SGD en A induce B⁺ = B − η K G. La métrica correspondiente en B es K⁻¹. La representación de mínima norma es A* = Mᵀ K⁻¹ B y su norma al cuadrado es tr(Bᵀ K⁻¹ B).

Con L2 sobre A, la actualización inducida es B⁺ = B − η(K G + λB), equivalente a descenso precondicionado sobre L + λ/2 tr(Bᵀ K⁻¹ B). Una inicialización isotrópica de A también induce una inicialización anisótropa de B. Igualar solamente función inicial o parámetros no controla todos estos efectos.

Si las representaciones se centran con medias compatibles y usan escalas globales s_x y s_z, el operador normalizado es N = (s_x/s_z) M. Esto reescala K, pero no cambia su número de condición. Escalas por característica sí pueden cambiar su anisotropía. AdamW depende de momentos por coordenada y no es invariante a estas reparametrizaciones: ni siquiera N Nᵀ = I garantiza igualdad de trayectorias AdamW.

**Cautela adicional sobre C10:** `common.train` emplea clipping ±9; `C10/source.py` compara explícitamente ambos modelos sin clipping en la evaluación del transporte. La identidad acredita el MLP afín/ReLU sin recorte; la identificación con el pipeline recortado exige verificar que el clipping esté inactivo en todos los ejemplos relevantes. El acuerdo de predicciones observado no demuestra esa condición fuera de las entradas probadas. Además, el transporte de 78 unidades usa 7.108 parámetros frente a los 5.834 del frontend histórico de 64 unidades. No acredita equivalencia con el presupuesto de C04.

Un posible control futuro es comparar sensor-SGD con pixel-SGD precondicionado por N Nᵀ, con mismo ancho y función inicial, batches, sesgos y penalización correspondiente. Antes de correr debe congelarse el protocolo y comprobarse la condición del operador. Igualdad de trayectorias identificaría una explicación por reparametrización en ese control; no constituiría evidencia favorable a MHU ni confirmación externa.
