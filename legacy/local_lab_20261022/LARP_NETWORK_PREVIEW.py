"""Vista LARP con mosaico inspirado en retina aviar; no entrena una red.

Adaptación visual, no réplica del algoritmo ni datos experimentales de Jiao 2014.
Esta vista revisada es un generador alternativo, no una edición del preregistro.
Fuente: https://pmc.ncbi.nlm.nih.gov/articles/PMC5836809/
Combina tamaños relativos publicados, separación homotípica y control espectral.

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
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.patches import Rectangle, Circle

N, L, K_NEIGHBORS = 400, 20.0, 6
COUNTS = np.array([163, 85, 68, 50, 34])
MODES = np.array([[1, 0], [0, 1], [1, 1], [1, -1], [2, 0], [0, 2]])
WAVEVECTORS = 2 * np.pi * MODES / L
COLORS = ["#424B62", "#249F78", "#E3685C", "#4D88D8", "#A26ACB"]
TYPE_NAMES = ["Doble", "Verde", "Rojo", "Azul", "Violeta"]
RELATIVE_RADII = np.array([1.50, 1.13, 1.06, 1.19, 1.00])
PACKING_FRACTION = 0.58
CELL_RADII = RELATIVE_RADII * np.sqrt(
    PACKING_FRACTION * L ** 2 / (np.pi * np.sum(COUNTS * RELATIVE_RADII ** 2)))
HOMOTYPIC_DISTANCE = np.sqrt(2 / (np.sqrt(3) * COUNTS / L ** 2))
SPECTRAL_WEIGHT, HOMOTYPIC_WEIGHT, PACKING_WEIGHT = 5.0, 20.0, 20000.0
ROOT = Path(__file__).resolve().parent


def spectra(points, labels):
    phase = np.exp(1j * points @ WAVEVECTORS.T)
    rows = [np.abs(phase[labels == c].sum(axis=0)) ** 2 / COUNTS[c]
            for c in range(5)]
    rows.append(np.abs(phase.sum(axis=0)) ** 2 / N)
    return np.array(rows)


def energy_gradient(flat, labels, growth=1.0):
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
    energy *= SPECTRAL_WEIGHT
    gradient = SPECTRAL_WEIGHT * (coefficient @ WAVEVECTORS)
    radii = CELL_RADII[labels] * growth
    pairs = cKDTree(points, boxsize=L).query_pairs(2 * radii.max(), output_type="ndarray")
    if len(pairs):
        delta = points[pairs[:, 0]] - points[pairs[:, 1]]
        delta -= L * np.round(delta / L)
        radius = np.maximum(np.linalg.norm(delta, axis=1), 1e-12)
        exclusion = radii[pairs[:, 0]] + radii[pairs[:, 1]]
        deficit = np.maximum(0.0, 1 - radius / exclusion)
        energy += PACKING_WEIGHT / N * np.sum(deficit ** 2)
        pair_gradient = (-2 * PACKING_WEIGHT / N * deficit / exclusion / radius)[:, None] * delta
        np.add.at(gradient, pairs[:, 0], pair_gradient)
        np.add.at(gradient, pairs[:, 1], -pair_gradient)
    for c in range(5):
        indexes = np.flatnonzero(labels == c)
        local_pairs = cKDTree(points[indexes], boxsize=L).query_pairs(
            HOMOTYPIC_DISTANCE[c], output_type="ndarray")
        if not len(local_pairs):
            continue
        pairs = indexes[local_pairs]
        delta = points[pairs[:, 0]] - points[pairs[:, 1]]
        delta -= L * np.round(delta / L)
        radius = np.maximum(np.linalg.norm(delta, axis=1), 1e-12)
        deficit = np.maximum(0.0, 1 - radius / HOMOTYPIC_DISTANCE[c])
        energy += HOMOTYPIC_WEIGHT / (5 * COUNTS[c]) * np.sum(deficit ** 2)
        pair_gradient = (-2 * HOMOTYPIC_WEIGHT / (5 * COUNTS[c])
                         * deficit / HOMOTYPIC_DISTANCE[c] / radius)[:, None] * delta
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
            growth = 0.25 + 0.75 * min(step / 3000, 1.0)
            _, gradient = energy_gradient(flat, labels, growth)
            first = 0.9 * first + 0.1 * gradient
            second = 0.999 * second + 0.001 * gradient ** 2
            rate = 0.0001 + (0.015 - 0.0001) * (1 + np.cos(np.pi * step / 6000)) / 2
            flat -= rate * (first / (1 - 0.9 ** step)) / (
                np.sqrt(second / (1 - 0.999 ** step)) + 1e-8)
            flat %= L
        optimized = minimize(energy_gradient, flat, args=(labels,), jac=True,
                             method="L-BFGS-B", options={"maxiter": 1000,
                             "maxfun": 2000, "maxcor": 20, "gtol": 1e-8, "ftol": 1e-12})
        points = optimized.x.reshape(N, 2) % L
        structure = spectra(points, labels)
        ratios = variance_ratios(points, labels)
        minimum = float(cKDTree(points, boxsize=L).query(points, k=2)[0][:, 1].min())
        pairs = cKDTree(points, boxsize=L).query_pairs(2 * CELL_RADII.max(), output_type="ndarray")
        delta = points[pairs[:, 0]] - points[pairs[:, 1]]
        delta -= L * np.round(delta / L)
        exclusion = CELL_RADII[labels[pairs[:, 0]]] + CELL_RADII[labels[pairs[:, 1]]]
        overlap = np.maximum(0, 1 - np.linalg.norm(delta, axis=1) / exclusion)
        maximum_overlap = float(overlap.max(initial=0))
        nearest_type = [cKDTree(points[labels == c], boxsize=L).query(
            points[labels == c], k=2)[0][:, 1] for c in range(5)]
        other_modes = np.array([(a, b) for a in range(-10, 11) for b in range(-10, 11)
                                if (a > 0 or a == 0 and b > 0) and 2 < np.hypot(a, b) <= 10])
        other_phase = np.exp(1j * points @ (2 * np.pi * other_modes / L).T)
        peak_ratios = [float((np.abs(other_phase[labels == c].sum(axis=0)) ** 2
                            / COUNTS[c] ** 2).max()) for c in range(5)]
        peak_ratios.append(float((np.abs(other_phase.sum(axis=0)) ** 2 / N ** 2).max()))
        passed = (np.all(structure.mean(axis=1) <= 0.05)
                  and np.all(structure.max(axis=1) <= 0.10)
                  and np.all((ratios["4"] + ratios["5"]) / 2 <= 0.65)
                  and maximum_overlap <= 0.002 and max(peak_ratios) < 0.50)
        print(json.dumps({"attempt": attempt + 1, "max_S": float(structure.max()),
                          "max_overlap": maximum_overlap,
                          "nearest_type_CV": [float(v.std() / v.mean()) for v in nearest_type]},
                         ensure_ascii=False), flush=True)
        if passed:
            diagnostics = {"N": N, "L": L, "counts": COUNTS.tolist(),
                "attempt": attempt + 1, "training": False,
                "scope": "avian_inspired_hybrid_finite_checks; not_an_empirical_retina_reproduction",
                "differs_from_preregistered_v0_1_generator": True,
                "source": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5836809/",
                "relative_cell_radii_A_to_E": RELATIVE_RADII.tolist(),
                "cell_radii_A_to_E": CELL_RADII.tolist(),
                "target_packing_fraction": PACKING_FRACTION,
                "homotypic_interaction_distances_A_to_E": HOMOTYPIC_DISTANCE.tolist(),
                "energy_weights": {"spectral": SPECTRAL_WEIGHT,
                                   "homotypic": HOMOTYPIC_WEIGHT, "packing": PACKING_WEIGHT},
                "maximum_relative_overlap": maximum_overlap,
                "nearest_type_mean_A_to_E": [float(v.mean()) for v in nearest_type],
                "nearest_type_CV_A_to_E": [float(v.std() / v.mean()) for v in nearest_type],
                "nonoptimized_max_S_over_N_A_to_E_union": peak_ratios,
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
    fig = plt.figure(figsize=(12.8, 9.4), facecolor="#F7F8FC")
    layout = fig.add_gridspec(2, 5, height_ratios=[2.6, 1], left=0.045,
                             right=0.97, bottom=0.17, top=0.835, wspace=0.32, hspace=0.48)
    main, zoom = fig.add_subplot(layout[0, :3]), fig.add_subplot(layout[0, 3:])
    subtype_axes = [fig.add_subplot(layout[1, c]) for c in range(5)]
    focus = int(np.argmin(np.linalg.norm(points - L / 2, axis=1)))
    center = points[focus]
    halfwidth = 2.7

    def cells(ax, only_type=None, alpha=1.0):
        patches, facecolors = [], []
        for i, point in enumerate(points):
            c = int(labels[i])
            if only_type is not None and c != only_type:
                continue
            radius = CELL_RADII[c]
            for sx in [-L, 0, L]:
                for sy in [-L, 0, L]:
                    shifted = point + [sx, sy]
                    if np.all(shifted + radius >= 0) and np.all(shifted - radius <= L):
                        patches.append(Circle(shifted, radius))
                        facecolors.append(COLORS[c])
        ax.add_collection(PatchCollection(patches, facecolors=facecolors, edgecolors="white",
                                          linewidths=0.6, alpha=alpha, zorder=3))
        ax.set(xlim=(0, L), ylim=(0, L), xticks=[], yticks=[])
        ax.set_aspect("equal")
        ax.set_facecolor("white")
        for spine in ax.spines.values():
            spine.set_color("#DDE2EC")

    cells(main)
    main.set_title("Mosaico completo", loc="left", pad=12)
    main.add_patch(Rectangle(center - halfwidth, 2 * halfwidth, 2 * halfwidth,
                            fill=False, edgecolor="#17233C", linewidth=1.2, linestyle="--", zorder=4))
    cells(zoom, alpha=0.20)
    pairs = sorted({tuple(sorted((i, int(j)))) for i in range(N) for j in neighbors[i]})
    segments = []
    for i, j in pairs:
        delta = points[j] - points[i]
        delta -= L * np.round(delta / L)
        segment = np.array([points[i], points[i] + delta])
        segments.append(segment)
    zoom.add_collection(LineCollection(segments, colors="#8E9AAF", linewidths=0.6,
                                       alpha=0.26, zorder=2))
    for c in range(5):
        zoom.scatter(*points[labels == c].T, s=36, color=COLORS[c], edgecolors="white",
                     linewidths=0.5, zorder=4)
    zoom.set(xlim=(center[0] - halfwidth, center[0] + halfwidth),
             ylim=(center[1] - halfwidth, center[1] + halfwidth))
    zoom.set_title("Conexiones locales · zoom", loc="left", pad=12)
    for j in neighbors[focus]:
        zoom.annotate("", xy=center, xytext=points[int(j)],
                      arrowprops={"arrowstyle": "-|>", "color": "#25324A",
                                  "lw": 1.6, "shrinkA": 4, "shrinkB": 6}, zorder=5)
    zoom.scatter(*center, s=180, facecolors="none", edgecolors="#25324A", linewidths=1.8, zorder=6)
    for c, ax in enumerate(subtype_axes):
        cells(ax, only_type=c)
        ax.set_title(f"{chr(65+c)} · {TYPE_NAMES[c]}\n{COUNTS[c]} nodos", fontsize=10,
                     color=COLORS[c], pad=8)
    fig.text(0.045, 0.953, "LARP · mosaico inspirado en retina aviar", fontsize=23,
             weight="bold", color="#17233C")
    fig.text(0.045, 0.908, "400 nodos · cinco poblaciones intercaladas · separación por tipo + empaquetamiento",
             fontsize=11.5, color="#59667D")
    fig.text(0.045, 0.10, "Cada color forma su propio mosaico. Discos: exclusión local. Flechas: seis entradas al nodo resaltado.",
             fontsize=10, color="#34435D")
    fig.text(0.045, 0.065, "Modelo inspirado en Jiao et al. (2014), con control espectral añadido; no son datos reales de una retina.",
             fontsize=9, color="#69758A")
    fig.text(0.045, 0.037, "Geometría sin entrenamiento · estado por nodo: 32 valores · actualización recurrente: 16 pasos",
             fontsize=9, color="#69758A")
    fig.savefig(ROOT / "LARP_NETWORK_PREVIEW.png", dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    points, labels, diagnostics = generate_geometry()
    neighbors = cKDTree(points, boxsize=L).query(points, k=K_NEIGHBORS + 1)[1][:, 1:]
    diagnostics["directed_edges"] = int(neighbors.size)
    diagnostics["incoming_degree"] = K_NEIGHBORS
    draw(points, labels, neighbors)
    np.savez_compressed(ROOT / "LARP_NETWORK_PREVIEW_GEOMETRY.npz",
                        points=points, labels=labels, incoming_neighbors=neighbors,
                        cell_radii=CELL_RADII[labels])
    (ROOT / "LARP_NETWORK_PREVIEW_DIAGNOSTICS.json").write_text(
        json.dumps(diagnostics, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"image": str(ROOT / "LARP_NETWORK_PREVIEW.png"),
                      "finite_checks_passed": True, "edges": neighbors.size,
                      "max_restricted_S": float(spectra(points, labels).max())}, ensure_ascii=False))
