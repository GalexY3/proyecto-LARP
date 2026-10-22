"""Vista reproducible de geometría y conexiones LARP; no entrena una red.

Dependencias: numpy, scipy, matplotlib. Ejecutar: python LARP_NETWORK_PREVIEW.py
Genera PNG, diagnóstico JSON y geometría NPZ junto a este archivo.
"""
from pathlib import Path
import json
import importlib.util
import sys

# En este equipo SciPy está aislado en caché; en otros basta instalar dependencias.
cached_scipy = Path.home() / ".cache" / "larp-preview-python"
if importlib.util.find_spec("scipy") is None and sys.version_info[:2] == (3, 14) and cached_scipy.exists():
    sys.path.insert(0, str(cached_scipy))

import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

N, L, K_NEIGHBORS = 400, 20.0, 6
COUNTS = np.array([163, 85, 68, 50, 34])
MODES = np.array([[1, 0], [0, 1], [1, 1], [1, -1], [2, 0], [0, 2]])
WAVEVECTORS = 2 * np.pi * MODES / L
COLORS = ["#526AE5", "#17A78E", "#ED875B", "#BF5EAC", "#CBA322"]
ROOT = Path(__file__).resolve().parent


def spectra(points, labels):
    phase = np.exp(1j * points @ WAVEVECTORS.T)
    rows = [np.abs(phase[labels == c].sum(axis=0)) ** 2 / COUNTS[c]
            for c in range(5)]
    rows.append(np.abs(phase.sum(axis=0)) ** 2 / N)
    return np.array(rows)


def energy_gradient(flat, labels):
    points = flat.reshape(N, 2) % L
    phase = np.exp(1j * points @ WAVEVECTORS.T)
    union = phase.sum(axis=0)
    energy = np.mean(np.abs(union) ** 2 / N)
    coefficient = -2 / (N * len(MODES)) * np.imag(phase * union.conj())
    for c in range(5):
        mask = labels == c
        amplitude = phase[mask].sum(axis=0)
        energy += np.mean(np.abs(amplitude) ** 2 / COUNTS[c]) / 5
        coefficient[mask] += -2 / (5 * COUNTS[c] * len(MODES)) * np.imag(
            phase[mask] * amplitude.conj())
    gradient = coefficient @ WAVEVECTORS
    pairs = cKDTree(points, boxsize=L).query_pairs(0.30, output_type="ndarray")
    if len(pairs):
        delta = points[pairs[:, 0]] - points[pairs[:, 1]]
        delta -= L * np.round(delta / L)
        radius = np.maximum(np.linalg.norm(delta, axis=1), 1e-12)
        deficit = np.maximum(0.0, 1 - radius / 0.30)
        energy += 10 / N * np.sum(deficit ** 2)
        pair_gradient = (-20 / (N * 0.30) * deficit / radius)[:, None] * delta
        np.add.at(gradient, pairs[:, 0], pair_gradient)
        np.add.at(gradient, pairs[:, 1], -pair_gradient)
    return float(energy), gradient.ravel()


def variance_ratios(points, labels):
    centers = np.random.default_rng(6101).uniform(0, L, (10000, 2))
    membership = np.column_stack([labels == c for c in range(5)] + [np.ones(N, bool)])
    result = {}
    for radius in [4.0, 5.0]:
        counts = []
        for chunk in np.array_split(centers, 20):
            delta = chunk[:, None, :] - points[None, :, :]
            delta -= L * np.round(delta / L)
            inside = np.sum(delta ** 2, axis=2) <= radius ** 2
            counts.append(inside.astype(np.int16) @ membership.astype(np.int16))
        probability = np.pi * radius ** 2 / L ** 2
        null_variance = np.append(COUNTS, N) * probability * (1 - probability)
        result[str(int(radius))] = np.vstack(counts).var(axis=0) / null_variance
    return result


def generate_geometry():
    for attempt in range(4):
        rng = np.random.default_rng(np.random.SeedSequence([20261008, 1101, attempt]))
        labels = rng.permutation(np.repeat(np.arange(5), COUNTS))
        flat = rng.uniform(0, L, (N, 2)).ravel()
        first, second = np.zeros_like(flat), np.zeros_like(flat)
        for step in range(1, 6001):
            _, gradient = energy_gradient(flat, labels)
            first = 0.9 * first + 0.1 * gradient
            second = 0.999 * second + 0.001 * gradient ** 2
            rate = 0.0001 + (0.025 - 0.0001) * (1 + np.cos(np.pi * step / 6000)) / 2
            flat -= rate * (first / (1 - 0.9 ** step)) / (
                np.sqrt(second / (1 - 0.999 ** step)) + 1e-8)
            flat %= L
        optimized = minimize(energy_gradient, flat, args=(labels,), jac=True,
                             method="L-BFGS-B", options={"maxiter": 250,
                             "maxfun": 1000, "maxcor": 20, "gtol": 1e-8, "ftol": 1e-12})
        points = optimized.x.reshape(N, 2) % L
        structure = spectra(points, labels)
        ratios = variance_ratios(points, labels)
        minimum = float(cKDTree(points, boxsize=L).query(points, k=2)[0][:, 1].min())
        passed = (np.all(structure.mean(axis=1) <= 0.05)
                  and np.all(structure.max(axis=1) <= 0.10)
                  and np.all((ratios["4"] + ratios["5"]) / 2 <= 0.65)
                  and minimum >= 0.299)
        if passed:
            diagnostics = {"N": N, "L": L, "counts": COUNTS.tolist(),
                "attempt": attempt + 1, "training": False,
                "scope": "finite_low_k_and_number_variance_checked; not_asymptotic_proof",
                "preview_optimizer": "analytic_gradient_Adam_then_SciPy_LBFGSB",
                "restricted_structure_factor_mean_A_to_E_union": structure.mean(axis=1).tolist(),
                "restricted_structure_factor_max_A_to_E_union": structure.max(axis=1).tolist(),
                "variance_ratio_A_to_E_union": {k: v.tolist() for k, v in ratios.items()},
                "minimum_distance": minimum, "finite_preview_checks_passed": True}
            return points, labels, diagnostics
    raise RuntimeError("No se obtuvo geometría válida; no se dibuja un patrón falso MHU.")


def draw(points, labels, neighbors):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "axes.titleweight": "bold", "axes.spines.top": False,
                         "axes.spines.right": False})
    fig = plt.figure(figsize=(11.8, 7.0), facecolor="#F7F8FC")
    grid = fig.add_gridspec(1, 2, width_ratios=[1.45, 1], left=0.055,
                           right=0.96, bottom=0.19, top=0.80, wspace=0.22)
    main, zoom = fig.add_subplot(grid[0]), fig.add_subplot(grid[1])
    focus = int(np.argmin(np.linalg.norm(points - L / 2, axis=1)))
    center = points[focus]
    halfwidth = max(2.3, 1.25 * np.max(np.linalg.norm(points[neighbors[focus]] - center, axis=1)))
    pairs = sorted({tuple(sorted((i, int(j)))) for i in range(N) for j in neighbors[i]})
    segments = []
    for i, j in pairs:
        delta = points[j] - points[i]
        delta -= L * np.round(delta / L)
        segment = np.array([points[i], points[i] + delta])
        for sx in [-L, 0, L]:
            for sy in [-L, 0, L]:
                shifted = segment + np.array([sx, sy])
                if np.all(shifted.max(axis=0) >= 0) and np.all(shifted.min(axis=0) <= L):
                    segments.append(shifted)
    for ax in [main, zoom]:
        ax.set_facecolor("white")
        ax.add_collection(LineCollection(segments, colors="#8E9AAF", linewidths=0.55, alpha=0.24))
        for c in range(5):
            ax.scatter(*points[labels == c].T, s=24 if ax is main else 90,
                       color=COLORS[c], edgecolors="white", linewidths=0.45, zorder=3)
        ax.set_aspect("equal")
        ax.tick_params(colors="#6A7486", length=0)
        for spine in ax.spines.values():
            spine.set_color("#DDE2EC")
    main.set(xlim=(0, L), ylim=(0, L), xticks=[0, 5, 10, 15, 20], yticks=[0, 5, 10, 15, 20])
    main.set_title("Sustrato completo", loc="left", pad=13)
    main.add_patch(Rectangle(center - halfwidth, 2 * halfwidth, 2 * halfwidth,
                            fill=False, edgecolor="#25324A", linewidth=1.1, linestyle="--", zorder=4))
    zoom.set(xlim=(center[0] - halfwidth, center[0] + halfwidth),
             ylim=(center[1] - halfwidth, center[1] + halfwidth), xticks=[], yticks=[])
    zoom.set_title("Zoom · seis entradas a un nodo", loc="left", pad=13)
    for j in neighbors[focus]:
        start = points[int(j)]
        zoom.annotate("", xy=center, xytext=start,
                      arrowprops={"arrowstyle": "-|>", "color": "#25324A",
                                  "lw": 1.5, "shrinkA": 6, "shrinkB": 8}, zorder=5)
    zoom.scatter(*center, s=240, facecolors="none", edgecolors="#25324A", linewidths=1.8, zorder=6)
    fig.text(0.055, 0.94, "Así se vería LARP v0.1", fontsize=23, weight="bold", color="#17233C")
    fig.text(0.055, 0.887, "400 nodos · 5 tipos · conexiones locales · espacio periódico 2D",
             fontsize=11.5, color="#59667D")
    legend = [Line2D([0], [0], marker="o", linestyle="", markersize=8,
                     color=COLORS[c], label=f"{chr(65+c)} · {COUNTS[c]} nodos") for c in range(5)]
    fig.legend(handles=legend, loc="lower center", bbox_to_anchor=(0.5, 0.103),
               ncol=5, frameon=False, columnspacing=2)
    fig.text(0.055, 0.076, "Cada nodo: estado de 32 valores. El mismo bloque de actualización se repite 16 pasos.",
             fontsize=10, color="#34435D")
    fig.text(0.055, 0.035, "Vista geométrica, sin entrenamiento. Las líneas grises omiten flechas; el zoom muestra su dirección.",
             fontsize=9, color="#69758A")
    fig.savefig(ROOT / "LARP_NETWORK_PREVIEW_LOW_K_ONLY.png", dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    points, labels, diagnostics = generate_geometry()
    neighbors = cKDTree(points, boxsize=L).query(points, k=K_NEIGHBORS + 1)[1][:, 1:]
    diagnostics["directed_edges"] = int(neighbors.size)
    diagnostics["incoming_degree"] = K_NEIGHBORS
    draw(points, labels, neighbors)
    np.savez_compressed(ROOT / "LARP_NETWORK_PREVIEW_LOW_K_ONLY_GEOMETRY.npz",
                        points=points, labels=labels, incoming_neighbors=neighbors)
    (ROOT / "LARP_NETWORK_PREVIEW_LOW_K_ONLY_DIAGNOSTICS.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"image": str(ROOT / "LARP_NETWORK_PREVIEW_LOW_K_ONLY.png"),
                      "finite_checks_passed": True, "edges": neighbors.size,
                      "max_restricted_S": float(spectra(points, labels).max())}, ensure_ascii=False))
