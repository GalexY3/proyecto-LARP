#!/usr/bin/env python3
"""Reproduce AB20 full-runtime CT2 plot from versioned O6 scores, with no interpolated checkpoints."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

folder = Path(__file__).resolve().parent
data = json.loads((folder / "CT2_TRAJECTORY.json").read_text(encoding="utf-8"))
tracks = data["tracks"]
labels = {
    "AB55_BUGSINPY": "AB55 · revisión documental",
    "AB30_P04_SYNTHETIC": "AB30 P04 · pruebas sintéticas",
    "AB20_REALPATCH_HUNKS": "AB20 · fragmentos upstream",
    "AB20_REAL_FULL_RUNTIME": "AB20 · repositorios completos",
}
markers = ["o", "s", "^", "D"]
for name, low, high in [("CT2_full.png", 0, 100), ("CT2_zoom.png", 6, 16)]:
    fig, ax = plt.subplots(figsize=(12.6, 5.8))
    for i, track in enumerate(tracks):
        pts = track["points"]
        X = [p["x"] for p in pts]
        Y = [p["score"] for p in pts]
        ax.plot(X, Y, marker=markers[i], markersize=5, linewidth=1.8, label=labels[track["branch"]])
        if i == 3:
            for x, y in zip(X, Y):
                ax.annotate(str(y), (x, y), xytext=(3, 7), textcoords="offset points", fontsize=9)
    for item in data["discontinuities"]:
        ax.axvline(item["x"], linestyle=":", linewidth=1)
    ax.set_xlim(-2, 128)
    ax.set_ylim(low, high)
    ax.set_ylabel("CT2 (escala ordinal, no probabilidad)")
    ax.set_xlabel("Hitos/ciclos acumulados del archivo (no tiempo calendario)")
    ax.set_title("LARP · CT2 por línea con discontinuidades de DRIFT / PIVOT")
    ax.grid(True, axis="y", alpha=.3)
    ax.legend(loc="upper right" if high == 100 else "upper left", ncol=2, fontsize=8)
    fig.text(.5, .012, "Rama de código completo: 8 → 11 tras auditar 14/20 casos reproducidos de forma condicionada; N2=0.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .035, 1, 1))
    fig.savefig(folder / name, dpi=180)
    plt.close(fig)
