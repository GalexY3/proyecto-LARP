"""Descriptive, endpoint-checked reporting of the fixed scale3d_v2 job."""
from __future__ import annotations

import csv
import math
from pathlib import Path
from statistics import mean

SIZES = (1024, 4096, 16384, 32768)
SEEDS = (3201, 3202)
ARMS = ("mhu", "local", "random")
CHECKPOINTS = (300, 600, 1200, 1800)
VALID_STATUSES = {"COMPLETE", "BUDGET_LIMIT_MATCHED_STEPS"}


def _evaluations(record):
    result = {}
    if record.get("status") not in VALID_STATUSES:
        return result
    for evaluation in record.get("evaluations", []):
        step = evaluation.get("step")
        if step not in CHECKPOINTS or step > record.get("training_updates", -1):
            continue
        try:
            values = {arm: {item["task"]: float(item["MSE"])
                            for item in evaluation["scores"][arm]} for arm in ARMS}
            valid = all(len(evaluation["scores"][arm]) == 3 for arm in ARMS) and all(set(items) == {0, 1, 2} and
                        all(math.isfinite(v) and v >= 0 for v in items.values())
                        for items in values.values())
        except (KeyError, TypeError, ValueError):
            valid = False
        if valid and step not in result:
            result[step] = values
    return result


def _stats(values):
    return (mean(values), min(values), max(values)) if len(values) == 2 else (None, None, None)


def _number(value):
    return "—" if value is None else f"{value:.6g}"


def write_report(final, output):
    """Write SUMMARY.md, comparison.csv, and an optional eligible scale plot.

    Per-N summaries require both specified geometry seeds at one common step.
    A global curve additionally requires all eight triples and the declared
    non-null endpoint, independently checked against every complete evaluation.
    Seed ranges are descriptive; worlds are not geometry replications.
    """
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    records = list(final.get("records", []))
    indexed = {}
    for record in records:
        key = (record.get("N"), record.get("seed"))
        indexed.setdefault(key, []).append(record)
    expected = {(N, seed) for N in SIZES for seed in SEEDS}
    checked = {key: _evaluations(items[0]) for key, items in indexed.items() if len(items) == 1}
    endpoint = final.get("common_scale_endpoint")
    eligible = (set(indexed) == expected and all(len(v) == 1 for v in indexed.values())
                and endpoint in CHECKPOINTS
                and all(endpoint in checked.get(key, {}) for key in expected))
    rows = []
    for N in SIZES:
        keys = [(N, seed) for seed in SEEDS]
        common = set(CHECKPOINTS)
        for key in keys:
            common &= set(checked.get(key, {}))
        if not common:
            continue
        step = endpoint if eligible else max(common)
        for task in range(3):
            row = {"N": N, "task": task, "checkpoint": step, "geometry_seeds": 2,
                   "scope": "GLOBAL_COMMON_ENDPOINT" if eligible else "PER_N_ONLY"}
            for arm in ARMS:
                values = [checked[key][step][arm][task] for key in keys]
                for suffix, value in zip(("mean", "min", "max"), _stats(values)):
                    row[f"MSE_{arm}_{suffix}"] = value
            for control in ("local", "random"):
                ratios = [checked[key][step]["mhu"][task] / checked[key][step][control][task]
                          for key in keys if checked[key][step][control][task] > 0]
                for suffix, value in zip(("mean", "min", "max"), _stats(ratios)):
                    row[f"ratio_MHU_{control.upper()}_{suffix}"] = value
            rows.append(row)
    fields = ["N", "task", "checkpoint", "geometry_seeds", "scope"]
    fields += [f"MSE_{arm}_{stat}" for arm in ARMS for stat in ("mean", "min", "max")]
    fields += [f"ratio_MHU_{control}_{stat}" for control in ("LOCAL", "RANDOM")
               for stat in ("mean", "min", "max")]
    with (output / "comparison.csv").open("x", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    lines = ["# LARP — Resultado descriptivo de escala 3D v2", "",
             f"Estado del job: `{final.get('status', 'NO_REGISTRADO')}`.", ""]
    if eligible:
        lines += [f"Las ocho tríadas comparten el checkpoint **{endpoint}**. "
                  "La tabla permite comparar tamaños en ese endpoint común.", ""]
    else:
        lines += ["**ESCALA INCONCLUYENTE:** falta cobertura válida de las ocho tríadas "
                  "o un endpoint global común registrado. No se presenta una curva global.", "",
                  "Las filas disponibles son comparaciones independientes por N con dos "
                  "semillas y un checkpoint propio común; no permiten extrapolar una tendencia de escala.", ""]
    if rows:
        lines += ["| N | Tarea | Paso | MSE MHU | MSE LOCAL | MSE RANDOM | MHU/LOCAL | MHU/RANDOM |",
                  "|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for row in rows:
            values = [row["N"], row["task"], row["checkpoint"]]
            values += [_number(row[f"MSE_{arm}_mean"]) for arm in ARMS]
            values += [_number(row[f"ratio_MHU_{control}_mean"]) for control in ("LOCAL", "RANDOM")]
            lines.append("| " + " | ".join(map(str, values)) + " |")
        lines += ["", "MSE: media de dos semillas geométricas. Cocientes: media de dos "
                  "cocientes emparejados; un denominador cero deja el cociente sin definir. "
                  "CSV contiene mínimos y máximos entre semillas, sin intervalos inferenciales.", ""]
    else:
        lines += ["No hay comparaciones con dos semillas y checkpoint válido común. "
                  "El CSV conserva sólo la cabecera; no se imputan resultados.", ""]
    lines += ["En el paso 300 sólo se ha entrenado la tarea 0; hasta el paso 600 "
              "la tarea 2 aún no entra en el currículo. Sus evaluaciones tempranas "
              "no miden competencia después de entrenarla.", ""]
    if eligible:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            fig, axes = plt.subplots(1, 3, figsize=(12, 3.6), sharey=True)
            for task, axis in enumerate(axes):
                subset = [row for row in rows if row["task"] == task]
                for control in ("LOCAL", "RANDOM"):
                    valid = [r for r in subset if r[f"ratio_MHU_{control}_mean"] is not None]
                    y = [r[f"ratio_MHU_{control}_mean"] for r in valid]
                    low = [v-r[f"ratio_MHU_{control}_min"] for r, v in zip(valid, y)]
                    high = [r[f"ratio_MHU_{control}_max"]-v for r, v in zip(valid, y)]
                    axis.errorbar([r["N"] for r in valid], y, yerr=[low, high], marker="o", label=f"MHU/{control}")
                axis.axhline(1, color="grey", linestyle="--", linewidth=1)
                axis.set_xscale("log", base=2)
                axis.set_title(f"Tarea {task}; paso {endpoint}")
                axis.set_xlabel("N (densidad)")
            axes[0].set_ylabel("Cociente MSE; rango de dos semillas")
            axes[-1].legend()
            fig.tight_layout()
            with (output / "comparison.png").open("xb") as stream:
                fig.savefig(stream, format="png", dpi=150)
            plt.close(fig)
            lines += ["![Comparación descriptiva](comparison.png)", ""]
        except ImportError:
            lines += ["Figura opcional omitida: matplotlib no disponible.", ""]
    lines += ["Se escala densidad en un toro fijo con parámetros, grado y profundidad "
              "constantes; el alcance físico cambia. Geometría y conexiones cambian juntas. "
              "El certificado MHU es finito, LOCAL puede también suprimir potencia espectral, "
              "y dos semillas no constituyen confirmación concluyente. No se declara "
              "superioridad general ni equivalencia con retina desordenada. CIC puede inducir orden de rejilla; su medida debe inspeccionarse por brazo. Tampoco se actualizan los priors históricos H1–H6/C.", ""]
    with (output / "SUMMARY.md").open("x", encoding="utf-8") as stream:
        stream.write("\n".join(lines))
    return {"global_scale_eligible": eligible, "global_checkpoint": endpoint if eligible else None,
            "comparison_rows": len(rows)}
