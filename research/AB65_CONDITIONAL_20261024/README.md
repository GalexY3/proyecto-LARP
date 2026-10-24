# LARP — AB65: 20 BRANCHING + 45 DRIFT D4–D5

**Documentación para nuevas instancias (24/10/2026). No usar solo memoria de ChatGPT.**

## Leer en este orden
1. [Metodología AB/README](https://github.com/GalexY3/Metodologia-AB/blob/main/README.md), AB 3.2.1, O3 (DRIFT), O4 (CT2 y grados), O5 (D0–D5), O6 (estructura obligatoria).
2. [LARP investigación/index](../INDEX.md) y [última campaña íntegra PR #23](https://github.com/GalexY3/proyecto-LARP/pull/23).
3. [Autorización actual](GRANT_PROTOCOL.md), [prerregistro](MEASUREMENT_PREREG.md), [SHA de fuente antes de fase D45](SOURCE_HASH_LOCK_PRE_D45.md).
4. [DICTAMEN_FINAL.md](DICTAMEN_FINAL.md): qué se ejecutó, no qué se deseaba demostrar.
5. [Ledger permanente completo de N1](N1_REGISTRO_COMPLETO_AUDITADO.json) + [explicación y posibles N1 históricos sin auditar](N1_REGISTRO_Y_HISTORIAL.md).
6. [CT2 puntos JSON](CT2_TRAJECTORY.json), [CSV](CT2_TRAJECTORY.csv), [gráficas regenerables mediante Python/Matplotlib](plot_ct2.py).
7. [Manifiesto de cobertura de GitHub](AUDITORIA_COBERTURA_GITHUB.json): leer `review_status` antes de afirmar que se ha inspeccionado un archivo.

## Autorización y resultado
20 análisis A–J de logs históricos, completos pero post-exposición; 2/3 no alcanzado. Se activaron 45 condiciones D4–D5 (15 de pronóstico físico; 15 de economía observacional; 15 de simulación de genética). **Tres pivotes D4–D5; no 45 saltos temáticos diferentes**. Ningún N1 nuevo; seis N1 previamente auditados; N2=0 y N3=0.

La serie CT2 representa juicios **subjetivos ordinales, no P(descubrimiento)**. Pivotes reabren escalas distintas. Puntos anclados desde AB55 y hasta D4 PopGen son [11→8], [12→10], [8→8], [8→11], [11→9], [9→7], [12→8], [8→4]; **no** unir saltos entre áreas científicas como ganancia de certeza.

## Estado de archivos
- En GitHub: manifest de la autorización, diseño, hashes pre-run, resultados resumidos, documentación de N1, dictamen, CT2 reproducible y manifiesto de cobertura.
- **En el ZIP de conversación, aún no en GitHub:** `phase1.py`, `phase2.py`, 20+45 A-J completos con salida por caso y los PNG exactos. **No afirmar un clean-clone reproductible ni mergear sin backfill y replay**.
- En `main`: seis hallazgos 1/3 en el ledger, pero el inventario histórico anterior sigue **NOT_AUDITED**. Se corrigió aquí el README antiguo que indicaba cuatro. No reetiquetar históricos de manera automática.

## Sobre la «otra conversación»
Recuperados por resúmenes y dictámenes de GitHub **tres AB45 distintas**: Beijing, Dynamic y DRIFT. El archivo MD aportado `información-del-bot-2vs1_20261014_1847.md` termina el 14/10/2026; NO contiene el transcript literal de las AB45 posteriores del 22–23/10. Las políticas recuperadas por contexto personal (guardar cada 1/3, CT2 e informes, pedir autorización explícita y separar la legitimidad de un 2/3 de una cifra numérica) se contrastaron con AB 3.2.1/O6. **Texto literal completo de la conversación de 45 no recuperado**.

## Decisión
`STOP_LOCAL` en repetir estos mismos datasets/modelos; no N2. Fase nueva, si alguna vez se autoriza, debe arrancar con hipótesis original falsable, rival fuerte, test y código preregistrados remotamente, y fuente externa independiente.
