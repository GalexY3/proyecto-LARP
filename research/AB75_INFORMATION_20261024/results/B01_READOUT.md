# INVALIDADO PARA REIVINDICACIÓN CIENTÍFICA — VERSIÓN v1/V2 CON FILTRACIÓN DE RESPUESTA

Los números en este readout pertenecen a los 75 primeros contratos ejecutados con preprocesado de y global. **No** son resultados válidos para una política que solo compra etiquetas del piloto. Se preservan EXCLUSIVAMENTE para auditoría del error. El [dictamen R1 corregido](../DICTAMEN_R1.md) resume las 75 reparaciones; contrato [R1](../prereg/REPAIR_R1_NO_FULL_Y_PREPROCESSING.md). La segunda ejecución está etiquetada POST-EXPOSURE/EXPLORATORY, no confirmación ciega.

---

# B01 C01–C06 — AB post-execution, exploratory

Six transformed observed finite populations; 650 independent *sampling trajectories* E at total B=30 labels, 750 G at B=48 on the SAME sources (not outside confirmation). A=p1/p2 pooled stratum sample mean; B=stage-conditional HT estimator. Stage2 is chosen adaptively from pilot **stratum means**. Source engine frozen SHA256 e20d7220.

| Cycle/source | Δ MSE A−B E | Δ MSE G | absolute bias A−B E |
|--|--:|--:|--:|
| C01 Engel | −0.005061 | −0.001302 | +0.00610 |
| C02 Fair | −0.009486 | −0.004341 | +0.01113 |
| C03 ANES96 | −0.015658 | −0.006734 | +0.00392 |
| C04 RANDHIE | −0.013977 | −0.006933 | +0.00320 |
| C05 Grunfeld | −0.006454 | −0.001765 | +0.00371 |
| C06 Macrodata | −0.014309 | −0.005952 | −0.00474 |

**A–J aggregate**: A estimand finite source transformed y mean. B H1 pooled has larger absolute bias than stage-conditional correction (5/6 positive E, one negative), rivals regularization and finite-sample variance. C identical pilot/second-stage queries, prereg B01 before run. D outcomes hidden until selected; finite budget+stratum support. E all six outcomes above, full per-draw JSON local. F **naive pooled MSE lower in all six**, so lower bias can worsen MSE and sampling/conditional inference are distinct estimands. G only fresh Monte Carlo randomness and B transfer, NOT source-independent replication. H known bias-variance tradeoff, no fresh novelty; CT2 branch 12→11. I grade 0/3 new, N1 unchanged 3; prior art Salehi 2010 and adaptive design theory. J DRIFT to a NEW adaptive variance-based allocation for B02 to avoid a duplicate swapped comparison; 30+45 authorization remains valid.
