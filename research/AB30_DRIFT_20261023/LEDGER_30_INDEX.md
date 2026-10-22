# Ledger compacto por ensayo AB3.2.1 — LARP AB30 Drift

**Fuente**: bloques pre-registrados antes de cada grupo, SHA de código 867e75309dfa81c8568bb2360d4cb4909560a338d7f16a587d03bba877f1deb6, resultados en AB30_SUMMARY.csv. Ledger A–J completo y resultados por semilla en ZIP de conversación. 30 tests, cinco decisiones verdaderamente adaptativas, fase G sin confirmación externa.

## Contrato A–J común

A: estimando diferencia de error del mismo objetivo/semilla en los métodos A y B; simulador n=24 mundos por test en B01–B03, datos reales n=16 particiones del mismo dataset en B04–B05. B: H1 A reduce pérdida, H0 misma pérdida, H_otros: baseline competente, sobreajuste, escenario impuesto, variables diferentes. C: subconjunto 3/9 enumerado exactamente en simulador; selección nested train/validation, test reservado dentro de dataset público para B04/B05. D: motor precomprometido; seed y datasets definidos, hash de manifiesto congelado antes del bloque. E: diferencias e intervalos en filas. F: auditoría de mismos datos/semillas, control full-feature y nominal; importante coste desigual y leakage adaptativo. G: NO confirmación externa; no considerar varios splits del mismo dataset independientes externamente. H: actualización cualitativa por signo y amplitud, no posterior numérico inventado; la observación que inspira H futura no la confirma. I: validez sólo condicionada, no originalidad 2/3 ni causalidad externa; reproducibilidad local, clon limpio pendiente. J: continuar dentro del bloque y aplicar la decisión de rama solo tras recibir los seis resultados.

**T01 (B01):** Nominal vs diagonal bajo ruido correlacionado estacionario. **E:** Δ=-0.010965, IC95=[-0.022110, 0.00018000], n=24 gaussian_estimator_mse. **H:** a favor sólo local; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T02 (B01):** Minimax vs nominal tras desplazamiento de grupos. **E:** Δ=0.032672, IC95=[-0.013150, 0.078500], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T03 (B01):** Minimax vs shrinkage ante desplazamiento. **E:** Δ=0.0095896, IC95=[-0.042960, 0.062140], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T04 (B01):** CVaR frente a minimax en escenario adverso. **E:** Δ=-0.016500, IC95=[-0.062630, 0.029630], n=24 gaussian_estimator_mse. **H:** a favor sólo local; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T05 (B01):** Nominal frente a elección aleatoria. **E:** Δ=-0.20210, IC95=[-0.32637, -0.077830], n=24 gaussian_estimator_mse. **H:** a favor sólo local; CI excluye cero (descriptivo). **J:** CONTINUE. **G:** no réplica externa.

**T06 (B01):** Shrinkage frente a nominal bajo correlación con signos. **E:** Δ=0.00073820, IC95=[-0.031700, 0.033170], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI incluye cero. **J:** PIVOT a colas de riesgo. **G:** no réplica externa.

**T07 (B02):** CVaR frente a nominal con desplazamiento de grupos. **E:** Δ=0.010638, IC95=[-0.030359, 0.051636], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T08 (B02):** CVaR frente a nominal con factores aleatorios. **E:** Δ=-0.024220, IC95=[-0.056521, 0.0080810], n=24 gaussian_estimator_mse. **H:** a favor sólo local; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T09 (B02):** CVaR frente a nominal con un factor global. **E:** Δ=0.0000, IC95=[0.0000, 0.0000], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T10 (B02):** Minimax frente a nominal con factores aleatorios. **E:** Δ=0.0069143, IC95=[-0.039291, 0.053119], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T11 (B02):** Shrinkage frente a nominal tras desplazamiento fuerte. **E:** Δ=0.0024874, IC95=[-0.0026580, 0.0076330], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T12 (B02):** Diagonal frente a nominal bajo correlaciones firmadas. **E:** Δ=0.079487, IC95=[0.0095690, 0.14941], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI excluye cero (descriptivo). **J:** PIVOT a estrés de covarianzas. **G:** no réplica externa.

**T13 (B03):** Nominal frente a diagonal con correlación extrema. **E:** Δ=-0.036759, IC95=[-0.058975, -0.014543], n=24 gaussian_estimator_mse. **H:** a favor sólo local; CI excluye cero (descriptivo). **J:** CONTINUE. **G:** no réplica externa.

**T14 (B03):** Shrinkage frente a nominal con correlación extrema. **E:** Δ=-0.079870, IC95=[-0.18518, 0.025439], n=24 gaussian_estimator_mse. **H:** a favor sólo local; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T15 (B03):** CVaR frente a nominal con desplazamiento mayor. **E:** Δ=-0.079319, IC95=[-0.18722, 0.028579], n=24 gaussian_estimator_mse. **H:** a favor sólo local; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T16 (B03):** Minimax frente a CVaR con signos alternos. **E:** Δ=0.015227, IC95=[-0.030188, 0.060642], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T17 (B03):** Diagonal frente a nominal con factor global. **E:** Δ=0.011283, IC95=[-0.0052610, 0.027828], n=24 gaussian_estimator_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T18 (B03):** Nominal frente a aleatorio con correlación firmada. **E:** Δ=-0.24132, IC95=[-0.44142, -0.041216], n=24 gaussian_estimator_mse. **H:** a favor sólo local; CI excluye cero (descriptivo). **J:** PIVOT a datos reales. **G:** no réplica externa.

**T19 (B04):** Selección estable frente a filtro Diabetes k3. **E:** Δ=8.1313, IC95=[-24.681, 40.944], n=16 diabetes_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T20 (B04):** Wrapper frente a filtro Diabetes k3. **E:** Δ=66.554, IC95=[-42.979, 176.09], n=16 diabetes_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T21 (B04):** Wrapper frente a estable Diabetes k3. **E:** Δ=58.423, IC95=[-52.264, 169.11], n=16 diabetes_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T22 (B04):** Filtro frente a aleatorio Diabetes k3. **E:** Δ=-1100.3, IC95=[-1399.7, -800.91], n=16 diabetes_mse. **H:** a favor sólo local; CI excluye cero (descriptivo). **J:** CONTINUE. **G:** no réplica externa.

**T23 (B04):** Wrapper frente a Ridge completo Diabetes k6. **E:** Δ=79.993, IC95=[-10.557, 170.54], n=16 diabetes_mse. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T24 (B04):** Estable frente a Ridge completo Diabetes k6. **E:** Δ=65.893, IC95=[33.872, 97.915], n=16 diabetes_mse. **H:** en contra o nulo; CI excluye cero (descriptivo). **J:** PIVOT a clasificación. **G:** no réplica externa.

**T25 (B05):** Selección estable frente a filtro Breast k3. **E:** Δ=0.0030210, IC95=[-0.0038100, 0.0098600], n=16 breast_1_minus_balanced_accuracy. **H:** en contra o nulo; CI incluye cero. **J:** CONTINUE. **G:** no réplica externa.

**T26 (B05):** Wrapper frente a filtro Breast k3. **E:** Δ=-0.014338, IC95=[-0.024990, -0.0036900], n=16 breast_1_minus_balanced_accuracy. **H:** a favor sólo local; CI excluye cero (descriptivo). **J:** CONTINUE. **G:** no réplica externa.

**T27 (B05):** Wrapper frente a estable Breast k3. **E:** Δ=-0.017359, IC95=[-0.030520, -0.0042000], n=16 breast_1_minus_balanced_accuracy. **H:** a favor sólo local; CI excluye cero (descriptivo). **J:** CONTINUE. **G:** no réplica externa.

**T28 (B05):** Filtro frente a aleatorio Breast k3. **E:** Δ=-0.088438, IC95=[-0.14321, -0.033660], n=16 breast_1_minus_balanced_accuracy. **H:** a favor sólo local; CI excluye cero (descriptivo). **J:** CONTINUE. **G:** no réplica externa.

**T29 (B05):** Wrapper frente a logística completa Breast k5. **E:** Δ=0.019896, IC95=[0.0076700, 0.032130], n=16 breast_1_minus_balanced_accuracy. **H:** en contra o nulo; CI excluye cero (descriptivo). **J:** CONTINUE. **G:** no réplica externa.

**T30 (B05):** Estable frente a logística completa Breast k5. **E:** Δ=0.036867, IC95=[0.030720, 0.043020], n=16 breast_1_minus_balanced_accuracy. **H:** en contra o nulo; CI excluye cero (descriptivo). **J:** CLOSE cuota. **G:** no réplica externa.

