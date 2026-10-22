"""Read-only arithmetic/provenance audit of completed Scale3D v2; no training."""
from pathlib import Path
import csv
import hashlib
import json
import math
from collections import Counter
from datetime import datetime, timezone
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RUN = ROOT / "runs/scale3d_v2"
SIZES = (1024, 4096, 16384, 32768)
ARMS = ("mhu", "local", "random")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, data):
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")


final = load(RUN / "results.json")
runner = load(RUN / "runner.json")
config = final["config"]
assert final["status"] == "COMPLETE" and final["common_scale_endpoint"] == 1800
assert runner["returncode"] == 0 and runner["status"] == "FINISHED"
records = {(r["N"], r["seed"]): r for r in final["records"]}
assert len(records) == len(final["records"]) == 8
assert set(records) == {(N, s) for N in SIZES for s in (3201, 3202)}
source_hashes = []
for path, expected in load(RUN / "protocol.json")["files"].items():
    actual = digest(ROOT / path)
    assert actual == expected, path
    source_hashes.append({"path": path.replace("\\", "/"), "sha256": actual})
rows, indexed, geometry = [], {}, []
for (N, seed), record in sorted(records.items()):
    pair = RUN / f"N{N}_g{seed}"
    assert record == load(pair / "result.json")
    assert record["status"] == "COMPLETE" and record["training_updates"] == 1800
    assert [e["step"] for e in record["evaluations"]] == [300, 600, 1200, 1800]
    matching = load(pair / "matching.json")
    assert set(matching["parameter_counts"].values()) == {4827415}
    assert matching["common_initialization"]
    for evaluation in record["evaluations"]:
        step = evaluation["step"]
        assert evaluation == load(pair / f"evaluation_u{step}.json")
        assert (pair / f"checkpoint_u{step}.pt").is_file()
        for arm in ARMS:
            assert {s["task"] for s in evaluation["scores"][arm]} == {0, 1, 2}
            for score in evaluation["scores"][arm]:
                values = score["world_MSE"]
                assert len(values) == 64 and all(math.isfinite(v) and v >= 0 for v in values)
                recomputed = math.fsum(values) / len(values)
                assert abs(recomputed - score["MSE"]) < 1e-12
                task = score["task"]
                indexed[N, seed, step, arm, task] = recomputed
                rows.append({"N": N, "seed": seed, "step": step, "arm": arm,
                             "task": task, "MSE": recomputed})
    for arm in ARMS:
        g = load(pair / f"{arm}_geometry.json")
        v = g["validation"]
        with np.load(pair / f"{arm}_geometry.npz", allow_pickle=False) as data:
            points, labels = data["points"], data["labels"]
            assert points.shape == (N, 3) and labels.shape == (N,)
            assert np.isfinite(points).all() and ((points >= 0) & (points < 1)).all()
            assert np.bincount(labels, minlength=5).tolist() == v["counts"]
        gate = all(c["exact_low_k_mean"] <= .20 and c["first_shell_mean"] <= .20
                   and c["exact_full_band_mean"] <= .20 for c in v["components"])
        assert gate == v["finite_low_k_pass"]
        geometry.append({"N": N, "seed": seed, "arm": arm, "gate": gate,
            "counts": v["counts"], "max_component_first_shell": max(c["first_shell_mean"] for c in v["components"]),
            "max_component_full_band_mean": max(c["exact_full_band_mean"] for c in v["components"]),
            "union_full_band_mean": v["components"][0]["exact_full_band_mean"],
            "grid_axis_S_over_N": v["CIC_grid_axis_coherent_power_fraction"],
            "NN_p05_physical": v["nearest_neighbor_p05_physical"],
            "NN_CV": v["nearest_neighbor_cv"],
            "homotypic_NN_p05_physical": v["homotypic_nearest_p05_physical"],
            "graph_train_query_diagnostics": matching["graph"][arm]})

summary = []
for N in SIZES:
    for task in range(3):
        values = {a: [indexed[N, s, 1800, a, task] for s in (3201, 3202)] for a in ARMS}
        entry = {"N": N, "task": task, "MSE_means": {a: sum(v)/2 for a, v in values.items()},
                 "seed_values": values}
        for control in ("local", "random"):
            ratios = [x/y for x, y in zip(values["mhu"], values[control])]
            entry[f"MHU_over_{control}"] = {"mean_paired_ratio": sum(ratios)/2,
                "ratio_of_means": sum(values["mhu"])/sum(values[control]),
                "min_paired_ratio": min(ratios), "max_paired_ratio": max(ratios)}
        summary.append(entry)

csv_rows = list(csv.DictReader((RUN / "comparison.csv").open(encoding="utf-8")))
assert len(csv_rows) == 12
for row in csv_rows:
    expected = next(e for e in summary if e["N"] == int(row["N"]) and e["task"] == int(row["task"]))
    for arm in ARMS:
        assert abs(float(row[f"MSE_{arm}_mean"]) - expected["MSE_means"][arm]) < 1e-12
    for control in ("local", "random"):
        assert abs(float(row[f"ratio_MHU_{control.upper()}_mean"])
                   - expected[f"MHU_over_{control}"]["mean_paired_ratio"]) < 1e-12
curriculum = Counter()
for step in range(1, 1801):
    rng = np.random.default_rng(config["master_seed"] + step)
    task = 0 if step <= 300 else int(rng.choice(2, p=[.2, .8])) if step <= 600 else int(rng.choice(3, p=[.1, .2, .7]))
    curriculum[task] += 1
counts = {N: next(g["counts"] for g in geometry if g["N"] == N) for N in SIZES}
mode_counts = []
for lower, upper in config["bands"]:
    total = sum(lower**2 <= i*i+j*j+k*k <= upper**2 and
        (i > 0 or i == 0 and j > 0 or i == j == 0 and k > 0)
        for i in range(-upper, upper+1) for j in range(-upper, upper+1) for k in range(-upper, upper+1))
    mode_counts.append(min(total, config["modes_per_task"]))
payload = {"generated_utc": datetime.now(timezone.utc).isoformat(),
    "scope": "Arithmetic and source audit; predictions not recomputed from weights",
    "runner": runner, "job_seconds": final["seconds"], "complete_triplets": len(records),
    "trained_networks": 24, "paired_updates": 14400, "network_updates": 43200,
    "scalar_evaluation_means_checked": len(rows), "world_errors_checked": len(rows)*64,
    "source_hashes_verified": source_hashes, "results_sha256": digest(RUN / "results.json"),
    "curriculum_updates": dict(curriculum), "modes_by_task": mode_counts,
    "real_coefficients_per_field_by_task": [2*M for M in mode_counts],
    "counts_by_N": counts, "endpoint_summary": summary, "geometry": geometry,
    "max_VRAM_GiB": max(r["peak_VRAM_GiB"] for r in records.values()),
    "training_timer_seconds_sum": sum(sum(r["training_seconds"].values()) for r in records.values()),
    "classification": "Descriptive exploratory comparison; not mechanistic confirmation"}
write(OUT / "analysis.json", payload)
with (OUT / "learning_curve.csv").open("x", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader(); writer.writerows(rows)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
colors = {"mhu": "#7656b8", "local": "#1b8275", "random": "#b76435"}
fig, axes = plt.subplots(1, 3, figsize=(13, 4.1))
for task, axis in enumerate(axes):
    for arm in ARMS:
        data = np.array([[indexed[N, s, 1800, arm, task] for s in (3201, 3202)] for N in SIZES])
        avg = data.mean(1)
        axis.plot(SIZES, avg, marker="o", color=colors[arm], label=arm.upper())
        axis.fill_between(SIZES, data.min(1), data.max(1), color=colors[arm], alpha=.13)
    axis.axhline(1, color="#888888", linestyle=":", linewidth=1)
    axis.set_xscale("log", base=2); axis.set_xticks(SIZES, labels=["1024", "4096", "16384", "32768"])
    axis.set_xlabel("N: sensores en dominio fijo")
    axis.set_title(["T0: reconstrucción suave", "T1: reconstrucción media", "T2: productos de banda alta"][task])
    axis.set_ylim(0, 1.12); axis.grid(alpha=.18)
axes[0].set_ylabel("MSE de test en update 1800")
axes[-1].legend(fontsize=8)
fig.suptitle("Scale3D v2: media y rango de dos semillas; banda ≠ intervalo de confianza", fontsize=11)
fig.tight_layout()
with (OUT / "endpoint_MSE.png").open("xb") as stream:
    fig.savefig(stream, format="png", dpi=160)
plt.close(fig)
fig, axes = plt.subplots(1, 4, figsize=(14, 3.8), sharey=True)
steps = [300, 600, 1200, 1800]
for N, axis in zip(SIZES, axes):
    for arm in ARMS:
        data = np.array([[indexed[N, s, step, arm, 0] for s in (3201, 3202)] for step in steps])
        axis.plot(steps, data.mean(1), marker="o", color=colors[arm], label=arm.upper())
        axis.fill_between(steps, data.min(1), data.max(1), color=colors[arm], alpha=.13)
    axis.axvline(600, linestyle=":", color="grey")
    axis.set_title(f"N={N}"); axis.set_xlabel("Updates"); axis.set_xticks(steps)
    axis.set_yscale("log"); axis.grid(alpha=.18)
axes[0].set_ylabel("T0: MSE de test (escala log)")
axes[-1].legend(fontsize=8)
fig.suptitle("Tarea suave: después de 600 entra T2; rango de dos semillas, sin selección de checkpoint", fontsize=11)
fig.tight_layout()
with (OUT / "task0_curriculum.png").open("xb") as stream:
    fig.savefig(stream, format="png", dpi=160)
plt.close(fig)
print(json.dumps({"complete_triplets": len(records), "means_checked": len(rows),
    "source_hashes_verified": len(source_hashes), "modes": mode_counts,
    "curriculum": dict(curriculum), "analysis": str(OUT / "analysis.json")}, ensure_ascii=False))
