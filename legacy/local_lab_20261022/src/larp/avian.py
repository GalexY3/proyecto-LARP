"""Versioned avian-inspired geometric candidate, separate from LARP v0.1.

This is a soft-penalty, finite spectral hybrid descended from the preview. It
does not reproduce Jiao et al.'s dynamics or empirically establish a retina.
The frozen v0.1 certificate is reused, never replaced by a visual plausibility
test. A failed seed is retained and cannot be promoted to an admitted pattern.
"""
from __future__ import annotations

from pathlib import Path
import importlib.metadata
import json
import math
import platform
import time

import numpy as np
from scipy.optimize import minimize
from scipy.spatial import cKDTree

from .artifacts import digest, file_hash, write_json, utc_now
from .geometry import Geometry, TYPE_NAMES, array_hash, certify_geometry, common_window_centers, minimum_image

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs" / "avian_v1.json"
VERSION = "avian_spectral_hybrid_v1"
_CONFIG_HASH = "5be454858d9316af73499e4e32ccf807f6c07e165ef073a64c65833a99a0e471"


def load_avian_config() -> dict:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if digest(config) != _CONFIG_HASH:
        raise ValueError("Frozen avian v1 config changed; create a new version instead.")
    return config


def cell_radii(config: dict | None = None) -> np.ndarray:
    config = load_avian_config() if config is None else config
    relative = np.asarray(config["relative_radii_A_to_E"], dtype=np.float64)
    counts = np.asarray(config["counts_A_to_E"], dtype=np.int64)
    return relative * np.sqrt(config["packing_fraction"] * config["L"]**2
                              / (np.pi * np.sum(counts * relative**2)))


def homotypic_distances(config: dict | None = None) -> np.ndarray:
    config = load_avian_config() if config is None else config
    return np.sqrt(2 / (np.sqrt(3) * np.asarray(config["counts_A_to_E"]) / config["L"]**2))


def avian_objective(points: np.ndarray, labels: np.ndarray, *, growth: float = 1.0,
                    treatment: str = "full_spectral", config: dict | None = None,
                    details: bool = False) -> tuple:
    """Analytic gradient on the periodic torus, rebuilding all active pairs.

    E = ws*(S_union_mean + mean_c S_c_mean)
        + wp/N*sum_all_pairs relu(1-r/(a_i+a_j))^2
        + wh/5*sum_c [sum_homotypic_pairs relu(1-r/d_c)^2 / n_c].
    Radii grow during Adam only. Homotypic cutoffs remain fixed, as in preview.
    Exact coincident points are nondifferentiable and explicitly rejected.
    """
    config = load_avian_config() if config is None else config
    if treatment not in config["allowed_treatments"]:
        raise ValueError("treatment must be full_spectral or local_only")
    if not np.isfinite(growth) or not 0 < growth <= 1:
        raise ValueError("radius growth must lie in (0,1]")
    L, N = float(config["L"]), int(config["N"])
    points = np.asarray(points, dtype=np.float64) % L
    labels = np.asarray(labels, dtype=np.int64)
    if points.shape != (N, 2) or labels.shape != (N,):
        raise ValueError("Avian v1 has a fixed 400-node shape")
    counts = np.asarray(config["counts_A_to_E"])
    if not np.array_equal(np.bincount(labels, minlength=5), counts):
        raise ValueError("Avian v1 conserves frozen counts")
    if not np.isfinite(points).all():
        raise ValueError("coordinates must be finite")
    weights = config["weights"]
    gradient = np.zeros_like(points)
    spectral_energy = 0.0
    if treatment == "full_spectral":
        wavevectors = 2*np.pi/L*np.asarray(config["optimized_integer_modes"])
        phase = np.exp(1j*points @ wavevectors.T)
        amplitude = phase.sum(axis=0)
        M = len(wavevectors)
        spectral_energy = float(np.mean(np.abs(amplitude)**2/N))
        coefficient = -2/(N*M)*np.imag(phase*amplitude.conj())
        for c in range(5):
            mask = labels == c
            amplitude = phase[mask].sum(axis=0)
            spectral_energy += float(np.mean(np.abs(amplitude)**2/counts[c])/5)
            coefficient[mask] += -2/(5*counts[c]*M)*np.imag(phase[mask]*amplitude.conj())
        spectral_energy *= weights["spectral"]
        gradient = weights["spectral"]*(coefficient @ wavevectors)

    def repulsion(pairs: np.ndarray, exclusions: np.ndarray, weight: float) -> float:
        if not len(pairs):
            return 0.0
        delta = minimum_image(points[pairs[:, 0]] - points[pairs[:, 1]], L)
        distance = np.linalg.norm(delta, axis=1)
        if np.any(distance == 0):
            raise ValueError("Exact collisions make the repulsion gradient undefined")
        deficit = np.maximum(0.0, 1-distance/exclusions)
        pair_gradient = (-2*weight*deficit/exclusions/distance)[:, None]*delta
        np.add.at(gradient, pairs[:, 0], pair_gradient)
        np.add.at(gradient, pairs[:, 1], -pair_gradient)
        return float(weight*np.dot(deficit, deficit))

    radii = cell_radii(config)[labels]*growth
    pairs = cKDTree(points, boxsize=L).query_pairs(2*radii.max(), output_type="ndarray")
    packing_energy = repulsion(pairs, radii[pairs[:, 0]]+radii[pairs[:, 1]], weights["packing"]/N)
    homotypic_energy, homo_pairs = 0.0, 0
    distances = homotypic_distances(config)
    for c in range(5):
        indexes = np.flatnonzero(labels == c)
        local = cKDTree(points[indexes], boxsize=L).query_pairs(distances[c], output_type="ndarray")
        homo_pairs += len(local)
        homotypic_energy += repulsion(indexes[local], np.full(len(local), distances[c]),
                                     weights["homotypic"]/(5*counts[c]))
    total = spectral_energy+packing_energy+homotypic_energy
    if details:
        return total, gradient, {"spectral_energy": spectral_energy, "packing_energy": packing_energy,
                                 "homotypic_energy": homotypic_energy, "packing_pairs": len(pairs),
                                 "homotypic_pairs": homo_pairs, "growth": growth,
                                 "gradient_norm": float(np.linalg.norm(gradient))}
    return total, gradient


def check_avian_gradient(points: np.ndarray, labels: np.ndarray, *, seed: int = 6101,
                         coordinates: int = 24, epsilon: float = 1e-6,
                         growth: float = 1.0, treatment: str = "full_spectral") -> dict:
    energy, gradient = avian_objective(points, labels, growth=growth, treatment=treatment)
    rng = np.random.default_rng(np.random.SeedSequence([20261008, seed, 8911]))
    chosen = rng.choice(points.size, min(coordinates, points.size), replace=False)
    expected, numeric = [], []
    for index in chosen:
        plus, minus = points.copy(), points.copy()
        plus.flat[index] += epsilon
        minus.flat[index] -= epsilon
        numeric.append((avian_objective(plus, labels, growth=growth, treatment=treatment)[0]
                        - avian_objective(minus, labels, growth=growth, treatment=treatment)[0])/(2*epsilon))
        expected.append(float(gradient.flat[index]))
    errors = np.abs(np.asarray(expected)-numeric)
    return {"energy": energy, "treatment": treatment, "growth": growth, "coordinates": chosen.tolist(),
            "analytic": expected, "finite_difference": numeric,
            "maximum_absolute_error": float(errors.max()),
            "maximum_scaled_error": float(np.max(errors/(1+np.abs(expected)))),
            "passed": bool(np.allclose(expected, numeric, atol=2e-6, rtol=2e-5))}


def packing_diagnostics(geometry: Geometry, config: dict | None = None) -> dict:
    config = load_avian_config() if config is None else config
    p, labels, L = geometry.points, geometry.labels, geometry.L
    radii = cell_radii(config)[labels]
    pairs = cKDTree(p, boxsize=L).query_pairs(2*radii.max(), output_type="ndarray")
    distance = np.linalg.norm(minimum_image(p[pairs[:, 0]]-p[pairs[:, 1]], L), axis=1)
    overlap = np.maximum(0.0, 1-distance/(radii[pairs[:, 0]]+radii[pairs[:, 1]]))
    nearest = {}
    for c, name in enumerate(TYPE_NAMES):
        points = p[labels == c]
        d = cKDTree(points, boxsize=L).query(points, k=2)[0][:, 1]
        nearest[name] = {"mean": float(d.mean()), "CV": float(d.std()/d.mean()),
                         "minimum": float(d.min()), "p05_p50_p95": np.quantile(d, [.05, .5, .95]).tolist()}
    maximum = float(overlap.max(initial=0))
    return {"cell_radii_A_to_E": cell_radii(config).tolist(),
            "nominal_disk_area_fraction": float(np.pi*np.sum(radii**2)/L**2),
            "hard_core_enforcement": "soft_penalty_with_finite_relative_overlap_tolerance",
            "maximum_relative_overlap": maximum,
            "overlap_pairs_positive": int(np.sum(overlap > 0)),
            "overlap_pairs_above_tolerance": int(np.sum(overlap > config["maximum_relative_overlap"])),
            "packing_admitted": maximum <= config["maximum_relative_overlap"],
            "homotypic_target_distances_A_to_E": homotypic_distances(config).tolist(),
            "nearest_homotypic": nearest}


def avian_local_identity() -> dict:
    """Hash only modules used by this generator, unaffected by parallel work."""
    modules = [Path(__file__), ROOT/"src/larp/geometry.py", ROOT/"src/larp/graphs.py",
               ROOT/"src/larp/data.py", ROOT/"src/larp/artifacts.py", CONFIG_PATH,
               ROOT/"LARP_NETWORK_PREVIEW.py"]
    modules += [p for p in (ROOT/"artifacts/avian_v1/reference_Jiao2014.pdf",)
                if p.exists()]
    files = {str(p.relative_to(ROOT)).replace("\\", "/"): file_hash(p) for p in modules}
    runtime = {name: importlib.metadata.version(name) for name in ("numpy", "scipy", "psutil")}
    runtime["python"] = platform.python_version()
    return {"files": files, "runtime": runtime, "hash": digest({"files": files, "runtime": runtime})}


class _BudgetLimit(RuntimeError):
    pass


def generate_avian(seed: int = 1101, *, treatment: str = "full_spectral",
                   output_dir: str | Path | None = None, test_only: bool = False,
                   adam_steps: int | None = None, lbfgs_iterations: int | None = None,
                   max_attempts: int | None = None, maximum_seconds: float | None = None,
                   centers: np.ndarray | None = None) -> Geometry:
    """Return first admitted candidate, or final explicit failure without tuning.

    The 120-second seed cap governs optimization across all attempts. A full
    certificate is always computed for a returned candidate, also on timeout;
    certificate CPU cost is recorded and may add several seconds to this cap.
    Saved attempts include every failed candidate; no replacement seed is used.
    """
    config = load_avian_config()
    if treatment not in config["allowed_treatments"]:
        raise ValueError("unknown avian treatment")
    opt = config["optimizer"]
    defaults = (opt["Adam_steps"], opt["LBFGSB_maxiter"], config["max_attempts"],
                config["maximum_generation_seconds_per_seed"])
    budget = tuple(default if value is None else value for value, default in zip(
        (adam_steps, lbfgs_iterations, max_attempts, maximum_seconds), defaults))
    if not test_only and budget != defaults:
        raise ValueError("Budget overrides require test_only=True or a new avian version")
    if not test_only and seed not in config["geometry_seeds"]:
        raise ValueError("v1 validation seeds are frozen to 1101,1102,1103")
    if budget[0] < 0 or budget[1] < 0 or budget[2] < 1 or budget[3] <= 0:
        raise ValueError("invalid generation budget")
    if not test_only and centers is not None:
        expected = common_window_centers(config["L"])
        if not np.array_equal(centers, expected):
            raise ValueError("Scientific validation uses frozen 10000 common centers")
    centers = common_window_centers(config["L"]) if centers is None else centers
    output_dir = Path(output_dir) if output_dir is not None else None
    prefix = f"avian_{treatment}_N400_g{seed}"
    if output_dir is not None and (output_dir/f"{prefix}.npz").exists():
        existing = Geometry.load(output_dir/f"{prefix}.npz")
        if existing.metadata.get("local_identity_hash") != avian_local_identity()["hash"]:
            raise FileExistsError("Existing avian artifact belongs to different generator provenance")
        return existing
    identity = avian_local_identity()
    start = time.perf_counter()
    deadline = start+float(budget[3])
    attempts, certificate_seconds = [], 0.0
    counts = np.asarray(config["counts_A_to_E"], dtype=np.int64)
    import psutil
    process = psutil.Process()
    peak_RSS = process.memory_info().rss
    for attempt in range(int(budget[2])):
        rng = np.random.default_rng(np.random.SeedSequence([config["master_seed"], seed, attempt]))
        labels = rng.permutation(np.repeat(np.arange(5), counts))
        points = rng.uniform(0, config["L"], (config["N"], 2))
        initial_hash = array_hash(points)
        first, second = np.zeros_like(points), np.zeros_like(points)
        trace, steps, lbfgs_steps, evaluations = [], 0, 0, 0
        stop, message = "COMPLETE", None
        before = time.perf_counter()
        try:
            for step in range(1, int(budget[0])+1):
                if time.perf_counter() >= deadline:
                    raise _BudgetLimit()
                growth = opt["growth_start"]+(1-opt["growth_start"])*min(step/opt["growth_end_step"], 1.0)
                energy, gradient, parts = avian_objective(points, labels, growth=growth,
                                                        treatment=treatment, config=config, details=True)
                first = opt["beta1"]*first+(1-opt["beta1"])*gradient
                second = opt["beta2"]*second+(1-opt["beta2"])*gradient**2
                rate = opt["lr_end"]+(opt["lr_start"]-opt["lr_end"])*(1+math.cos(math.pi*step/opt["Adam_steps"]))/2
                points = (points-rate*(first/(1-opt["beta1"]**step))/
                          (np.sqrt(second/(1-opt["beta2"]**step))+opt["epsilon"])) % config["L"]
                steps = step
                if step % 500 == 0 or step == int(budget[0]):
                    peak_RSS = max(peak_RSS, process.memory_info().rss)
                    trace.append({"optimizer": "Adam", "step": step, "energy": energy, "lr": rate, **parts})
            accepted = points.copy()

            def objective(flat):
                nonlocal evaluations
                if time.perf_counter() >= deadline:
                    raise _BudgetLimit()
                evaluations += 1
                value, gradient = avian_objective(flat.reshape(-1, 2), labels, treatment=treatment, config=config)
                return value, gradient.ravel()

            def callback(flat):
                nonlocal accepted, lbfgs_steps
                accepted = flat.reshape(-1, 2).copy() % config["L"]
                lbfgs_steps += 1

            if budget[1]:
                try:
                    optimized = minimize(objective, points.ravel(), jac=True, method="L-BFGS-B",
                                         callback=callback, options={"maxiter": int(budget[1]),
                                         "maxfun": opt["LBFGSB_maxfun"], "maxcor": opt["LBFGSB_maxcor"],
                                         "gtol": opt["LBFGSB_gtol"], "ftol": opt["LBFGSB_ftol"]})
                    accepted = optimized.x.reshape(-1, 2) % config["L"]
                    message = str(optimized.message)
                finally:
                    points = accepted
        except _BudgetLimit:
            stop, message = "RESOURCE_LIMIT", "Optimization seed cap reached; final accepted iterate retained"
        except (FloatingPointError, ValueError) as exc:
            stop, message = "NUMERICAL_FAILURE_UNVERIFIED", f"{type(exc).__name__}: {exc}"
        base = {"generator_version": VERSION, "kind": "avian_hybrid", "treatment": treatment,
                "geometry_seed": seed, "attempt": attempt, "test_only": bool(test_only),
                "config_hash": digest(config), "local_identity_hash": identity["hash"],
                "differs_from_preregistered_v0_1": True, "empirical_retina_replication": False,
                "architecture_preregistered": False, "neural_training": False,
                "seed_keys": [config["master_seed"], seed, attempt]}
        candidate = Geometry(points, labels, config["L"], base)
        cert_start = time.perf_counter()
        cert = certify_geometry(candidate, scope="mhu", centers=centers, detailed=True)
        cert_duration = time.perf_counter()-cert_start
        certificate_seconds += cert_duration
        packing = packing_diagnostics(candidate, config)
        energy, _, parts = avian_objective(points, labels, treatment=treatment, config=config, details=True)
        admitted = stop == "COMPLETE" and cert["scientific_admissible"] and packing["packing_admitted"] and not test_only
        record = {"attempt": attempt, "status": stop, "message": message, "initial_points_hash": initial_hash,
                  "hashes": candidate.hashes, "adam_steps": steps, "lbfgsb_iterations": lbfgs_steps,
                  "lbfgsb_evaluations": evaluations, "optimization_seconds": cert_start-before,
                  "certificate_seconds": cert_duration, "final_energy": energy, **parts,
                  "packing": packing, "certificate": cert, "admitted": bool(admitted), "trace": trace}
        attempts.append(record)
        metadata = {**base, "status": "ADMITTED" if admitted else "NOT_ADMITTED",
                    "admitted": bool(admitted), "certificate": cert, "packing": packing,
                    "optimizer": {"name": "float64_Adam_then_SciPy_LBFGSB", "status": stop,
                                  "adam_steps": steps, "lbfgsb_iterations": lbfgs_steps},
                    "attempts": attempts, "runtime_seconds": time.perf_counter()-start,
                    "peak_RSS_bytes": peak_RSS, "local_identity": identity,
                    "certificate_total_seconds": certificate_seconds,
                    "config": config, "finite_certificate_is_not_asymptotic_proof": True}
        candidate = Geometry(points, labels, config["L"], metadata)
        if output_dir is not None:
            candidate.save(output_dir/f"{prefix}_attempt{attempt}.npz")
            write_json(output_dir/f"{prefix}_attempt{attempt}_record.json", record)
        if admitted or stop != "COMPLETE" or time.perf_counter() >= deadline:
            break
    if output_dir is not None:
        candidate.save(output_dir/f"{prefix}.npz")
        write_json(output_dir/f"{prefix}_manifest.json", {"created": utc_now(), **candidate.to_dict()})
        write_json(output_dir/f"{prefix}_certificate.json", cert)
    return candidate


def validate_avian_suite(output_dir: str | Path = ROOT/"artifacts/avian_v1", *,
                        treatment: str = "full_spectral") -> dict:
    """Run exactly the three frozen seeds; no neural model or AB update."""
    from .graphs import knn_graph, graph_metrics, hop_type_coverage
    from .data import register_ports
    config = load_avian_config()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for seed in config["geometry_seeds"]:
        geometry = generate_avian(seed, treatment=treatment, output_dir=output_dir)
        prefix = f"avian_{treatment}_N400_g{seed}"
        edges = knn_graph(geometry.points, geometry.L, 6)
        graphs = graph_metrics(edges, geometry.N, geometry.points, geometry.L)
        graphs["type_coverage"] = hop_type_coverage(edges, geometry.labels, geometry.N)
        ports = register_ports(geometry.points, geometry.L)
        ports_report = {**ports.report(), "indices": ports.indices.tolist(), "sites": ports.sites.tolist()}
        gradient = check_avian_gradient(geometry.points, geometry.labels, seed=seed, treatment=treatment)
        write_json(output_dir/f"{prefix}_graph_metrics.json", graphs)
        write_json(output_dir/f"{prefix}_ports.json", ports_report)
        write_json(output_dir/f"{prefix}_gradient.json", gradient)
        records.append({"seed": seed, "admitted": geometry.metadata["admitted"],
                        "status": geometry.metadata["status"], "hashes": geometry.hashes,
                        "runtime_seconds": geometry.metadata["runtime_seconds"],
                        "peak_RSS_bytes": geometry.metadata["peak_RSS_bytes"],
                        "attempt": geometry.metadata["attempt"],
                        "certificate_passed": geometry.metadata["certificate"]["passed"],
                        "packing_maximum_overlap": geometry.metadata["packing"]["maximum_relative_overlap"],
                        "gradient_passed": gradient["passed"], "SCC_count": graphs["SCC_count"],
                        "port_digest": ports.digest})
    summary = {"version": VERSION, "config_hash": digest(config), "local_identity": avian_local_identity(),
               "treatment": treatment, "records": records, "admitted_count": sum(r["admitted"] for r in records),
               "failed_seeds_retained": True, "selection": "first_admitted_within_frozen_budget",
               "architecture_evidence": False, "neural_training": False, "beliefs_updated": False}
    write_json(output_dir/f"summary_{treatment}.json", summary)
    plot_avian_validation(summary, output_dir)
    return summary


def plot_avian_validation(summary: dict, output_dir: str | Path) -> Path:
    """Scientific disk plot of the saved candidates, including failed seeds."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.collections import PatchCollection
    from matplotlib.patches import Circle
    output_dir = Path(output_dir)
    colors = ["#424B62", "#249F78", "#E3685C", "#4D88D8", "#A26ACB"]
    config = load_avian_config()
    fig, axes = plt.subplots(1, len(summary["records"]), figsize=(12, 4.9))
    for ax, record in zip(np.atleast_1d(axes), summary["records"]):
        seed = record["seed"]
        geometry = Geometry.load(output_dir/f"avian_{summary['treatment']}_N400_g{seed}.npz")
        patches, facecolors = [], []
        for point, label in zip(geometry.points, geometry.labels):
            radius = cell_radii(config)[label]
            for sx in (-geometry.L, 0, geometry.L):
                for sy in (-geometry.L, 0, geometry.L):
                    shifted = point+[sx, sy]
                    if np.all(shifted+radius >= 0) and np.all(shifted-radius <= geometry.L):
                        patches.append(Circle(shifted, radius))
                        facecolors.append(colors[label])
        ax.add_collection(PatchCollection(patches, facecolors=facecolors,
                                          edgecolors="white", linewidths=.35))
        ax.set(xlim=(0, geometry.L), ylim=(0, geometry.L), xticks=[], yticks=[])
        ax.set_aspect("equal")
        status = "ADMITIDA" if record["admitted"] else "NO ADMITIDA"
        ax.set_title(f"Semilla {seed} · {status}\n400 nodos · cinco tipos", fontsize=11)
        ax.set_xlabel(f"Solapamiento relativo máx. {record['packing_maximum_overlap']:.4g}\n"
                      f"SCC {record['SCC_count']} · certificado finito {record['certificate_passed']}", fontsize=9)
    fig.suptitle("LARP · candidata aviar con repulsión por tipo y control espectral", fontsize=15)
    fig.text(.5, .02, "Geometría sintética inspirada en Jiao et al. (2014); no es una retina empírica ni evidencia de mejora neuronal.",
             ha="center", fontsize=9)
    fig.tight_layout(rect=(0, .06, 1, .91))
    path = output_dir/f"avian_{summary['treatment']}_validation.png"
    fig.savefig(path, dpi=170)
    plt.close(fig)
    return path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT/"artifacts/avian_v1")
    parser.add_argument("--treatment", choices=("full_spectral", "local_only"), default="full_spectral")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dry_run:
        print(json.dumps({"config": load_avian_config(), "local_identity": avian_local_identity(),
                          "will_train_neural_network": False}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(validate_avian_suite(args.output_dir, treatment=args.treatment), ensure_ascii=False, indent=2))
