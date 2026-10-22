"""Graph-independent task worlds, deterministic port registration and metrics.

Datasets store external worlds and targets, never substrate coordinates, marks,
edges or graph distances. ``batch`` binds a previously generated world to ports.
Layout: mask, payload[8], source ID[5], query[5], seed, free, sin/cos[4].
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType

import numpy as np
import torch
from scipy.optimize import linear_sum_assignment


CHANNEL_LAYOUT = {"port_mask": 0, "payload": slice(1, 9),
                  "source_id": slice(9, 14), "query": slice(14, 19),
                  "seed": 19, "free": 20, "coordinates": slice(21, 25),
                  "resource_query_coordinates": slice(25, 29)}
TASK_KEYS = {"xor": 201, "copy": 202, "fill": 203, "resource": 204}
SPLIT_KEYS = {"train": 301, "validation": 302, "val": 302, "test": 303,
              "diagnostic": 304}
TASK_VERSIONS = {"xor": "remote_xor_v1", "copy": "addressed_copy_5x8_persistent_v1",
                 "fill": "external_toroidal_flood_fill_8_v1", "resource": "resource_fourier_control_v1"}
ALIASES = {"remote_xor": "xor", "addressed_copy_5x8_persistent": "copy",
           "flood_fill_8": "fill", "resource_positive_control": "resource"}
FILL_PROBABILITIES = np.array([0.45, 0.55, 0.65], dtype=np.float64)


def canonical_task(task: str) -> str:
    task = ALIASES.get(task, task)
    if task not in TASK_KEYS:
        raise ValueError(f"unknown task: {task}")
    return task


def _digest(config: dict, arrays: dict[str, np.ndarray]) -> str:
    h = hashlib.sha256(json.dumps(config, sort_keys=True, separators=(",", ":")).encode())
    for name in sorted(arrays):
        array = np.ascontiguousarray(arrays[name])
        h.update(name.encode())
        h.update(array.dtype.str.encode())
        h.update(str(array.shape).encode())
        h.update(array.tobytes())
    return h.hexdigest()


def minimum_image_displacements(x: np.ndarray, y: np.ndarray, L: float) -> np.ndarray:
    delta = np.asarray(y) - np.asarray(x)
    return delta - L * np.round(delta / L)


def world_sites(world_side: int = 10, L: float = 20,
                offset=(0.0, 0.0)) -> np.ndarray:
    """Sites (2a+.5,2b+.5), flattening a first then b, translated on the torus."""
    if world_side < 1 or L <= 0:
        raise ValueError("positive side and L required")
    a, b = np.meshgrid(np.arange(world_side), np.arange(world_side), indexing="ij")
    return (np.stack((2 * a.ravel() + 0.5, 2 * b.ravel() + 0.5), axis=-1)
            + np.asarray(offset)) % L


def coordinate_channels(points: np.ndarray, L: float) -> np.ndarray:
    phase = np.asarray(points) * (2 * np.pi / L)
    return np.stack((np.sin(phase[:, 0]), np.cos(phase[:, 0]),
                     np.sin(phase[:, 1]), np.cos(phase[:, 1])), axis=-1).astype(np.float32)


@dataclass(frozen=True)
class PortAssignment:
    indices: np.ndarray
    sites: np.ndarray
    displacements: np.ndarray
    L: float
    digest: str

    @property
    def rms_displacement(self) -> float:
        return float(np.sqrt(np.mean(self.displacements**2)))

    @property
    def maximum_displacement(self) -> float:
        return float(np.max(self.displacements))

    def report(self) -> dict:
        return {"digest": self.digest, "port_count": len(self.indices),
                "RMS_port_displacement": self.rms_displacement,
                "maximum_port_displacement": self.maximum_displacement,
                "displacements": self.displacements.tolist()}


def assign_ports(points: np.ndarray, sites: np.ndarray, L: float) -> PortAssignment:
    points = np.asarray(points, dtype=np.float64)
    sites = np.asarray(sites, dtype=np.float64) % L
    if points.ndim != 2 or points.shape[1] != 2 or len(points) < len(sites):
        raise ValueError("injective ports require at least as many 2D nodes as sites")
    delta = minimum_image_displacements(sites[:, None, :], points[None, :, :], L)
    cost = np.sum(delta**2, axis=-1)
    # Lexicographic row priority, total perturbation strictly <1e-10. Stable
    # original IDs and SciPy's deterministic solver settle residual machine ties.
    row_priority = np.exp2(-np.arange(len(sites), dtype=np.float64))
    perturb = 5e-11 * row_priority[:, None] * np.arange(len(points))[None, :] / max(1, len(points))
    rows, columns = linear_sum_assignment(cost + perturb)
    if not np.array_equal(rows, np.arange(len(sites))):
        raise RuntimeError("Hungarian registration did not cover every external site")
    columns = columns.astype(np.int64)
    distances = np.sqrt(cost[rows, columns])
    digest = _digest({"L": L, "version": "Hungarian_squared_torus_v1"},
                     {"positions": points, "sites": sites, "indices": columns})
    return PortAssignment(columns, sites, distances, float(L), digest)


def register_ports(points: np.ndarray, L: float = 20, world_side: int = 10,
                   offset=(0.0, 0.0)) -> PortAssignment:
    return assign_ports(points, world_sites(world_side, L, offset), L)


def xor_oracle(bits: np.ndarray) -> np.ndarray:
    bits = np.asarray(bits)
    if bits.shape[-1] != 2:
        raise ValueError("XOR requires exactly two bits")
    return np.logical_xor(bits[..., 0], bits[..., 1]).astype(np.float32)


def copy_oracle(payload: np.ndarray, query: np.ndarray) -> np.ndarray:
    payload, query = np.asarray(payload), np.asarray(query, dtype=np.int64)
    if payload.shape[-2:] != (5, 8):
        raise ValueError("copy requires five sources with eight bits each")
    return np.take_along_axis(payload, query[..., None, None], axis=-2)[..., 0, :]


def flood_fill_oracle(free: np.ndarray, seed: int, iterations: int = 8,
                      return_distances: bool = False):
    """Conventional BFS on the *external* toroidal cardinal world, not a GNN."""
    free = np.asarray(free, dtype=bool)
    if free.ndim != 2 or free.shape[0] != free.shape[1] or iterations < 0:
        raise ValueError("square Boolean world and nonnegative horizon required")
    side = free.shape[0]
    if not 0 <= seed < side * side or not free.ravel()[seed]:
        raise ValueError("seed must be a free world cell")
    distance = np.full(side * side, -1, dtype=np.int16)
    distance[seed] = 0
    queue, cursor = [int(seed)], 0
    while cursor < len(queue):
        site = queue[cursor]
        cursor += 1
        a, b = divmod(site, side)
        for neighbor in (((a - 1) % side) * side + b,
                         ((a + 1) % side) * side + b,
                         a * side + (b - 1) % side,
                         a * side + (b + 1) % side):
            if free.ravel()[neighbor] and distance[neighbor] < 0:
                distance[neighbor] = distance[site] + 1
                queue.append(neighbor)
    target = ((distance >= 0) & (distance <= iterations)).reshape(side, side).astype(np.float32)
    return (target, distance.reshape(side, side)) if return_distances else target


@dataclass(frozen=True)
class TaskDataset:
    task: str
    seed: int
    split: str
    world_side: int
    L: float
    arrays: dict[str, np.ndarray]
    version: str
    positive_weight: float | None = None
    train_target_variance: float | None = None
    _digest_value: str = field(init=False, repr=False)

    def __post_init__(self):
        object.__setattr__(self, "task", canonical_task(self.task))
        # Bytes-backed arrays cannot be made writable again via setflags. The
        # mapping and metadata are frozen too: a digest cannot become stale.
        arrays = {name: np.frombuffer(np.ascontiguousarray(array).tobytes(),
                                     dtype=array.dtype).reshape(array.shape)
                  for name, array in self.arrays.items()}
        object.__setattr__(self, "arrays", MappingProxyType(arrays))
        object.__setattr__(self, "_digest_value", _digest(self.config, self.arrays))

    @property
    def config(self) -> dict:
        return {"task": self.task, "task_version": self.version, "seed": self.seed,
                "split": self.split, "world_side": self.world_side, "L": self.L,
                "positive_weight": self.positive_weight,
                "train_target_variance": self.train_target_variance,
                "size": len(self.arrays["target"])}

    @property
    def digest(self) -> str:
        return self._digest_value

    @property
    def target(self) -> np.ndarray:
        return self.arrays["target"]

    def __len__(self) -> int:
        return len(self.target)

    def __getitem__(self, index):
        return {name: array[index] for name, array in self.arrays.items()}

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(path, metadata=json.dumps(self.config, sort_keys=True),
                            digest=self.digest, **self.arrays)

    @classmethod
    def load(cls, path: str | Path) -> "TaskDataset":
        with np.load(path, allow_pickle=False) as archive:
            config = json.loads(str(archive["metadata"]))
            arrays = {key: archive[key].copy() for key in archive.files if key not in {"metadata", "digest"}}
            dataset = cls(config["task"], config["seed"], config["split"], config["world_side"],
                          config["L"], arrays, config["task_version"], config["positive_weight"],
                          config.get("train_target_variance"))
            if dataset.digest != str(archive["digest"]):
                raise ValueError("dataset archive hash mismatch")
        return dataset

    def batch(self, indices, positions: np.ndarray, ports: PortAssignment,
              device: str | torch.device = "cpu", *, labels=None,
              input_ports: PortAssignment | None = None,
              output_ports: PortAssignment | None = None) -> dict:
        """Bind graph-free samples. Separate input/output ports support K6 copy.

        Ordinary tasks overwrite coordinate channels at all registered sites,
        including inactive addresses. Resource control preserves physical coords.
        Targets/roles contain no biological type identity in the primary tasks.
        """
        indices = np.asarray(indices, dtype=np.int64).reshape(-1)
        positions = np.asarray(positions, dtype=np.float64)
        input_ports, output_ports = input_ports or ports, output_ports or ports
        p, n, b = self.world_side**2, len(positions), len(indices)
        if self.task != "resource" and len(ports.indices) != p:
            raise ValueError("port count differs from external world")
        if self.L != ports.L:
            raise ValueError("world and ports must use the same torus L")
        channels = 29 if self.task == "resource" else 25
        inputs = np.zeros((b, n, channels), dtype=np.float32)
        inputs[:, :, 21:25] = coordinate_channels(positions, self.L)
        if self.task != "resource":
            inputs[:, input_ports.indices, 21:25] = coordinate_channels(input_ports.sites, self.L)
            inputs[:, output_ports.indices, 21:25] = coordinate_channels(output_ports.sites, self.L)
        samples = {key: value[indices] for key, value in self.arrays.items()}
        result = {}
        if self.task in {"xor", "copy"}:
            source_nodes = input_ports.indices[samples["source_sites"]]
            output_nodes = output_ports.indices[samples["destination"][:, None]]
            rows = np.arange(b)
            if input_ports.digest != output_ports.digest:
                # One node has only one coordinate slot. K6 does not prescribe
                # encoding two different active logical sites on the same node.
                for row in rows:
                    collision = source_nodes[row] == output_nodes[row, 0]
                    if collision.any():
                        source_coordinates = input_ports.sites[samples["source_sites"][row, collision]]
                        destination_coordinate = output_ports.sites[samples["destination"][row]]
                        if not np.allclose(source_coordinates, destination_coordinate, rtol=0, atol=1e-12):
                            raise RuntimeError("SCIENTIFIC_BLOCKER_K6_active_input_output_coordinate_collision")
            for source_id in range(source_nodes.shape[1]):
                node = source_nodes[:, source_id]
                inputs[rows, node, 0] = 1
                inputs[rows, node, 9 + source_id] = 1
                inputs[rows, node, 1:9] = samples["payload"][:, source_id]
            inputs[rows, output_nodes[:, 0], 0] = 1
            if self.task == "copy":
                inputs[rows, output_nodes[:, 0], 14 + samples["query"]] = 1
                result["selected_source_nodes"] = source_nodes[rows, samples["query"]]
            else:
                inputs[rows, output_nodes[:, 0], 14:16] = 1
                result["selected_source_nodes"] = source_nodes
            result["source_nodes"] = source_nodes
        elif self.task == "fill":
            output_nodes = np.broadcast_to(output_ports.indices, (b, p)).copy()
            inputs[:, input_ports.indices, 0] = 1
            inputs[:, input_ports.indices, 20] = samples["free"]
            inputs[np.arange(b), input_ports.indices[samples["seed_site"]], 19] = 1
            result.update(free=samples["free"], p=samples["p"],
                          bfs_distance=samples["bfs_distance"],
                          source_nodes=input_ports.indices[samples["seed_site"][:, None]])
        else:
            if labels is None or np.asarray(labels).shape != (n,):
                raise ValueError("resource control requires one resource label per node")
            labels = np.asarray(labels, dtype=np.int64)
            if np.any((labels < 0) | (labels > 4)):
                raise ValueError("resource labels must be 0..4")
            physical_values = evaluate_resource_fields(samples["coefficients"], positions, self.L)
            inputs[:, np.arange(n), 1 + labels] = physical_values[:, labels, np.arange(n)]
            output_nodes = np.broadcast_to(ports.indices, (b, len(ports.indices))).copy()
            inputs[:, ports.indices, 0] = 1
            inputs[:, ports.indices, 25:29] = coordinate_channels(ports.sites, self.L)
        result.update(inputs=inputs, target=samples["target"], output_nodes=output_nodes,
                      active_nodes=inputs[:, :, 0].astype(bool))
        return {name: torch.as_tensor(np.array(value, copy=True), device=device)
                for name, value in result.items()}


def _balanced_categories(size: int, categories: int, rng: np.random.Generator) -> np.ndarray:
    values = np.arange(size, dtype=np.int64) % categories
    rng.shuffle(values)
    return values


def generate_task(task: str, size: int, seed: int, world_side: int = 10,
                  L: float = 20, split: str = "train", fill_iterations: int = 8) -> TaskDataset:
    task = canonical_task(task)
    split = "validation" if split == "val" else split
    if size < 1 or split not in SPLIT_KEYS:
        raise ValueError("positive dataset size and known split required")
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), TASK_KEYS[task], SPLIT_KEYS[split]]))
    sites = world_sites(world_side, L)
    p = len(sites)
    arrays = {}
    weight = None
    if task in {"xor", "copy"}:
        sources = 2 if task == "xor" else 5
        delta = minimum_image_displacements(sites[:, None], sites[None, :], L)
        distances = np.linalg.norm(delta, axis=-1)
        source_sites = np.empty((size, sources), dtype=np.int64)
        destination = rng.integers(p, size=size, dtype=np.int64)
        for row, dest in enumerate(destination):
            candidates = np.flatnonzero((distances[dest] >= L / 4) & (np.arange(p) != dest))
            if len(candidates) < sources:
                raise ValueError("world has too few remote sites for this task")
            # Order is source ID; the random permutation is independent of marks.
            source_sites[row] = rng.choice(candidates, sources, replace=False)
        if task == "xor":
            combinations = _balanced_categories(size, 4, rng)
            bits = np.stack((combinations // 2, combinations % 2), axis=-1)
            payload = np.zeros((size, 2, 8), dtype=np.float32)
            payload[:, :, 0] = bits
            target = xor_oracle(bits)[:, None, None]
        else:
            payload = rng.integers(2, size=(size, 5, 8)).astype(np.float32)
            query = _balanced_categories(size, 5, rng)
            arrays["query"] = query
            target = copy_oracle(payload, query)[:, None, :]
        arrays.update(source_sites=source_sites, destination=destination, payload=payload,
                      target=target.astype(np.float32))
    elif task == "fill":
        factors = _balanced_categories(size, 3, rng)
        probabilities = FILL_PROBABILITIES[factors]
        free = rng.random((size, p)) < probabilities[:, None]
        seed_site = rng.integers(p, size=size, dtype=np.int64)
        free[np.arange(size), seed_site] = True
        target = np.empty((size, p, 1), dtype=np.float32)
        bfs_distance = np.empty((size, p), dtype=np.int16)
        for row in range(size):
            reached, distance = flood_fill_oracle(free[row].reshape(world_side, world_side),
                                                 int(seed_site[row]), fill_iterations, True)
            target[row, :, 0], bfs_distance[row] = reached.ravel(), distance.ravel()
        arrays.update(free=free, seed_site=seed_site, p=probabilities,
                      p_factor=factors, target=target, bfs_distance=bfs_distance)
        if split == "train":
            positive = int(target.sum())
            weight = float(np.clip((target.size - positive) / max(1, positive), 1, 5))
    else:
        coefficients = rng.normal(size=(size, 5, 4, 2))
        coefficients /= np.sqrt(np.sum(coefficients**2, axis=(2, 3), keepdims=True) / 2)
        query_sites = world_sites(5, L) * 2 - 0.5  # exactly (4a+.5,4b+.5)
        query_sites %= L
        target = evaluate_resource_fields(coefficients, query_sites, L).mean(axis=1)[..., None].astype(np.float32)
        arrays.update(coefficients=coefficients, query_sites=query_sites, target=target)
        # query_sites is dataset-global, not an example array; retain coefficients
        # and targets here, and obtain registration via resource_ports below.
        del arrays["query_sites"]
    version = TASK_VERSIONS[task]
    if task == "fill" and fill_iterations != 8:
        version = f"external_toroidal_flood_fill_{fill_iterations}_exploratory_v1"
    variance = float(np.var(arrays["target"], dtype=np.float64)) if task == "resource" and split == "train" else None
    return TaskDataset(task, int(seed), split, world_side, float(L), arrays, version, weight, variance)


def resource_sites(L: float = 20) -> np.ndarray:
    a, b = np.meshgrid(np.arange(5), np.arange(5), indexing="ij")
    return np.stack((4 * a.ravel() + 0.5, 4 * b.ravel() + 0.5), axis=-1) % L


def resource_ports(points: np.ndarray, L: float = 20) -> PortAssignment:
    return assign_ports(points, resource_sites(L), L)


def evaluate_resource_fields(coefficients: np.ndarray, points: np.ndarray, L: float) -> np.ndarray:
    """Return [fields,channels,points], normalized using Fourier coefficients."""
    modes = np.array([[1, 0], [0, 1], [1, 1], [1, -1]], dtype=np.float64)
    phases = np.asarray(points) @ (2 * np.pi / L * modes.T)
    return (np.einsum("bcm,pm->bcp", coefficients[..., 0], np.cos(phases))
            + np.einsum("bcm,pm->bcp", coefficients[..., 1], np.sin(phases)))


def _as_numpy(value) -> np.ndarray:
    return value.detach().cpu().numpy() if isinstance(value, torch.Tensor) else np.asarray(value)


def evaluate_task(task: str, logits_selected, target, free=None, p=None,
                  train_target_variance: float | None = None) -> dict:
    """Evaluate aggregate predictions; concatenate minibatches before fill macro.

    No test-derived class weights or thresholds. Fill score averages BA *within
    each map*, then within each p, then weights the three factors equally.
    """
    task = canonical_task(task)
    logits, truth = _as_numpy(logits_selected), _as_numpy(target)
    if logits.shape != truth.shape:
        raise ValueError("selected logits and targets must have identical shape")
    if not np.all(np.isfinite(logits)):
        return {"score": 0.0, "loss": float("inf"), "divergent": True}
    if task == "resource":
        mse = float(np.mean((logits - truth)**2))
        if train_target_variance is None or train_target_variance <= 0:
            raise ValueError("resource NMSE requires positive frozen train target variance")
        return {"score": -mse / train_target_variance, "NMSE": mse / train_target_variance,
                "MSE": mse, "loss": mse}
    prediction = logits >= 0  # sigmoid(logit)>=0.5, including the equality case.
    truth_bool = truth.astype(bool)
    bce = float(np.mean(np.logaddexp(0.0, logits) - truth * logits))
    accuracy = float(np.mean(prediction == truth_bool))
    if task != "fill":
        result = {"score": accuracy, "accuracy": accuracy, "loss": bce,
                  "BCE": bce, "exact_accuracy": float(np.mean(np.all(prediction == truth_bool, axis=tuple(range(1, logits.ndim)))))}
        if task == "copy":
            result["bit_accuracy"] = accuracy
            result["exact_vector_accuracy"] = result["exact_accuracy"]
        return result
    if free is None or p is None:
        raise ValueError("fill requires free-cell masks and probability factors")
    free_array = _as_numpy(free).astype(bool)
    probabilities = _as_numpy(p).reshape(-1)
    prediction = prediction[..., 0]
    truth_bool = truth_bool[..., 0]
    if free_array.shape != prediction.shape:
        raise ValueError("free must have shape [maps,world_cells]")
    scores, iou, degenerate = [], [], []
    for pred, actual, eligible in zip(prediction, truth_bool, free_array):
        positive, negative = eligible & actual, eligible & ~actual
        if not positive.any() or not negative.any():
            score = float(np.mean(pred[eligible] == actual[eligible])) if eligible.any() else float("nan")
            degenerate.append(True)
        else:
            score = 0.5 * (np.mean(pred[positive]) + np.mean(~pred[negative]))
            degenerate.append(False)
        scores.append(float(score))
        union = np.count_nonzero((pred | actual) & eligible)
        iou.append(np.count_nonzero((pred & actual) & eligible) / union if union else 1.0)
    per_factor = {}
    for factor in FILL_PROBABILITIES:
        selected = np.isclose(probabilities, factor, rtol=0, atol=1e-12)
        if selected.any():
            per_factor[f"{factor:.2f}"] = float(np.mean(np.asarray(scores)[selected]))
    if not per_factor:
        raise ValueError("no known fill probability factor found")
    return {"score": float(np.mean(list(per_factor.values()))),
            "balanced_accuracy": float(np.mean(list(per_factor.values()))),
            "BA_by_p": per_factor, "p_factors_present": len(per_factor),
            "BA_per_map": scores, "degenerate_map_frequency": float(np.mean(degenerate)),
            "IoU": float(np.mean(iou)), "exact_map_accuracy": float(np.mean(np.all(prediction == truth_bool, axis=1))),
            "obstacle_error": float(np.mean(prediction[~free_array])) if (~free_array).any() else 0.0,
            "accuracy": accuracy, "loss": bce, "BCE": bce}


def fill_trivial_predictions(dataset: TaskDataset) -> dict[str, np.ndarray]:
    if dataset.task != "fill":
        raise ValueError("fill-only trivial controls")
    seed = np.zeros_like(dataset.arrays["free"])
    seed[np.arange(len(dataset)), dataset.arrays["seed_site"]] = True
    return {"all_free": dataset.arrays["free"].copy(), "seed_only": seed}
