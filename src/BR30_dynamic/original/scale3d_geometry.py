"""Bounded 3D marked low-wave-number candidates; no asymptotic HU claim.

Coordinates live on the unit torus; physical box length is N**(1/3).
Common local relaxation and initialization are shared by both treatments.
The spectral treatment adds a finite-wave-number penalty. CIC/FFT is an
optimization proxy, independently checked with exact point Fourier sums.
"""
from __future__ import annotations

import itertools
import math
import time

import numpy as np
import torch
from scipy.spatial import cKDTree

AVIAN_PROPORTIONS = np.array([163, 85, 68, 50, 34], dtype=np.float64) / 400
VERSION = "scale3d_cic_multicomponent_v1"


def hamilton_counts(N: int) -> np.ndarray:
    if isinstance(N, bool) or int(N) != N or N < 10:
        raise ValueError("N must be an integer >= 10")
    expected = int(N) * AVIAN_PROPORTIONS
    result = np.floor(expected).astype(np.int64)
    # Stable ties prefer the original type order.
    result[np.argsort(-(expected - result), kind="stable")[:int(N)-result.sum()]] += 1
    if np.any(result < 2):
        raise ValueError("At least two points per component are required")
    return result


def cic_density(coordinates: torch.Tensor, labels: torch.Tensor,
                grid_size: int, num_types: int = 5) -> torch.Tensor:
    """Differentiable periodic cloud-in-cell deposition, O(N + grid volume)."""
    if coordinates.ndim != 2 or coordinates.shape[1] != 3:
        raise ValueError("Expected coordinates[N,3]")
    if labels.shape != coordinates.shape[:1] or grid_size < 4:
        raise ValueError("Invalid labels/grid shape")
    scaled = torch.remainder(coordinates, 1) * grid_size
    base = torch.floor(scaled).long()
    frac = scaled - base
    density = coordinates.new_zeros(num_types * grid_size**3)
    for corner in itertools.product((0, 1), repeat=3):
        offset = torch.tensor(corner, device=coordinates.device)
        cell = torch.remainder(base + offset, grid_size)
        factors = torch.where(offset.bool(), frac, 1-frac)
        weight = factors.prod(dim=1)
        indices = labels*grid_size**3 + cell[:, 0]*grid_size**2 + cell[:, 1]*grid_size + cell[:, 2]
        density = density.scatter_add(0, indices, weight)
    return density.reshape(num_types, grid_size, grid_size, grid_size)


def reciprocal_modes(N: int, chi: float = .12) -> tuple[np.ndarray, int]:
    """Complete isotropic shells in one representative of each +/- pair.

    Finite chi is M/(3*(N-1)), M the number of complex constraints. We never
    select only part of a shell to hit a target count: that creates anisotropy.
    """
    if N < 2 or not 0 < chi < .5:
        raise ValueError("N>=2 and 0<chi<.5 required")
    target = max(3, int(3 * (N-1) * chi))
    radius = max(2, int(math.ceil((target*3/(2*math.pi))**(1/3)))+2)
    vectors = np.array(list(itertools.product(range(-radius, radius+1), repeat=3)), dtype=np.int64)
    norm2 = np.sum(vectors*vectors, axis=1)
    half = ((vectors[:, 0] > 0) |
            ((vectors[:, 0] == 0) & (vectors[:, 1] > 0)) |
            ((vectors[:, 0] == 0) & (vectors[:, 1] == 0) & (vectors[:, 2] > 0)))
    vectors, norm2 = vectors[half], norm2[half]
    shells, shell_counts = np.unique(norm2, return_counts=True)
    admitted = shells[np.cumsum(shell_counts) <= target]
    cutoff2 = int(admitted[-1]) if len(admitted) else 1
    selected = vectors[norm2 <= cutoff2]
    # Canonical order facilitates independent reproducibility and testing.
    order = np.lexsort((selected[:, 2], selected[:, 1], selected[:, 0], np.sum(selected*selected, axis=1)))
    return selected[order], cutoff2


def exact_structure_factor(coordinates: torch.Tensor, modes: torch.Tensor,
                           chunk_size: int = 64) -> torch.Tensor:
    """Exact S(k), not CIC; differentiable and bounded in temporary memory."""
    if len(coordinates) == 0 or modes.ndim != 2 or modes.shape[1] != 3:
        raise ValueError("Nonempty coordinates and modes[K,3] required")
    values = []
    for chunk in modes.split(chunk_size):
        phase = 2*math.pi*(coordinates @ chunk.to(coordinates).T)
        real, imag = torch.cos(phase).sum(0), torch.sin(phase).sum(0)
        values.append((real.square()+imag.square()) / len(coordinates))
    return torch.cat(values) if values else coordinates.new_empty(0)


def _objective_data(counts: np.ndarray, grid_size: int, chi: float,
                    device: torch.device, dtype: torch.dtype) -> dict:
    N = int(counts.sum())
    lengths = np.r_[N, counts]
    cutoffs = [reciprocal_modes(int(n), chi)[1] for n in lengths]
    if max(cutoffs) >= (grid_size/3)**2:
        raise ValueError("Grid too coarse: spectral cutoff must remain below one third of Nyquist sampling frequency")
    x = torch.fft.fftfreq(grid_size, device=device, dtype=dtype)*grid_size
    z = torch.fft.rfftfreq(grid_size, device=device, dtype=dtype)*grid_size
    kx, ky, kz = torch.meshgrid(x, x, z, indexing="ij")
    norm2 = kx.square()+ky.square()+kz.square()
    hermitian = torch.where((kz == 0) | (kz == grid_size/2), 1., 2.)
    correction = (torch.sinc(kx/grid_size)*torch.sinc(ky/grid_size)*torch.sinc(kz/grid_size)).pow(4).clamp_min(.03)
    masks = torch.stack([(norm2 > 0) & (norm2 <= c) for c in cutoffs])
    spectral_weights = masks*hermitian
    spectral_weights /= spectral_weights.sum(dim=(-3, -2, -1), keepdim=True)
    # Same short-distance density repulsion in both arms. Self-energy is
    # coordinate-independent in the exact smoothed-density limit; CIC leaves
    # a small grid imprint, measured rather than treated as biological truth.
    physical_L = N**(1/3)
    sigmas = .35 * (N / lengths)**(1/3)
    sigma = torch.as_tensor(sigmas, device=device, dtype=dtype)[:, None, None, None]
    local_weights = torch.exp(-(2*math.pi*sigma/physical_L).square()*norm2[None]) * hermitian
    local_weights[:, 0, 0, 0] = 0
    local_weights /= local_weights.sum(dim=(-3, -2, -1), keepdim=True)
    return {"counts": torch.as_tensor(lengths, device=device, dtype=dtype)[:, None, None, None],
            "spectral_weights": spectral_weights, "local_weights": local_weights,
            "correction": correction, "cutoffs": cutoffs}


def _loss(coordinates: torch.Tensor, labels: torch.Tensor, grid_size: int,
          data: dict, spectral: bool, local_weight: float) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    grids = cic_density(coordinates, labels, grid_size)
    union_and_types = torch.cat((grids.sum(0, keepdim=True), grids), 0)
    amplitudes = torch.fft.rfftn(union_and_types, dim=(-3, -2, -1))
    power = amplitudes.abs().square() / data["counts"]
    local_components = (power*data["local_weights"]).sum(dim=(-3, -2, -1))
    local = .5*(local_components[0]+local_components[1:].mean())
    spectral_components = (power/data["correction"]*data["spectral_weights"]).sum(dim=(-3, -2, -1))
    low = .5*(spectral_components[0]+spectral_components[1:].mean())
    return local_weight*local + (low if spectral else 0), low, local


def validate_geometry(coordinates: torch.Tensor, labels: torch.Tensor, *,
                      chi: float = .12, sample_modes: int = 128,
                      seed: int = 0, threshold: float = .20,
                      grid_size: int | None = None) -> dict:
    """Exact held-out computation on optimization bands, plus outside modes.

    It is a finite audit of a proxy, not held-out evidence of asymptotic HU.
    Randomly subsampling a band is explicitly disclosed. Complete first shell
    is separately audited because mode-count averages can hide low-k peaks.
    """
    points = coordinates.detach().to(dtype=torch.float64)
    labels = labels.detach().to(device=points.device)
    N = len(points)
    if (points.shape != (N, 3) or labels.shape != (N,) or not torch.isfinite(points).all()
            or len(labels) == 0 or labels.min() < 0 or labels.max() > 4
            or sample_modes < 3 or not math.isfinite(threshold) or threshold <= 0):
        raise ValueError("Invalid coordinates, five-component labels, or audit settings")
    counts = torch.bincount(labels, minlength=5).cpu().numpy()
    if counts.shape != (5,) or counts.sum() != N or np.any(counts < 2):
        raise ValueError("Invalid geometry")
    rng = np.random.default_rng(seed)
    records = []
    for c in range(-1, 5):
        component = points if c == -1 else points[labels == c]
        modes, cutoff2 = reciprocal_modes(len(component), chi)
        selected = modes if len(modes) <= sample_modes else modes[rng.choice(len(modes), sample_modes, replace=False)]
        selected_t = torch.as_tensor(selected, device=points.device)
        S = exact_structure_factor(component, selected_t).cpu().numpy()
        first = modes[np.sum(modes*modes, axis=1) == 1]
        firstS = exact_structure_factor(component, torch.as_tensor(first, device=points.device)).cpu().numpy()
        outside_all, _ = reciprocal_modes(max(64, int(len(component)*4)), chi)
        outside = outside_all[(np.sum(outside_all**2, axis=1) > cutoff2) &
                              (np.sum(outside_all**2, axis=1) <= 4*cutoff2)]
        if len(outside) > sample_modes:
            outside = outside[rng.choice(len(outside), sample_modes, replace=False)]
        outsideS = exact_structure_factor(component, torch.as_tensor(outside, device=points.device)).cpu().numpy()
        rows = []
        for axis in range(3):
            axis_selection = np.abs(selected[:, axis]) == np.abs(selected).max(1)
            rows.append(float(S[axis_selection].mean()) if axis_selection.any() else None)
        records.append({"component": "union" if c == -1 else f"type_{c}", "n": len(component),
                        "cutoff_integer_norm_squared": cutoff2,
                        "physical_cutoff": 2*math.pi*math.sqrt(cutoff2)/N**(1/3),
                        "full_band_halfspace_modes": len(modes), "tested_modes": len(selected),
                        "chi_realized": len(modes)/(3*(len(component)-1)),
                        "exact_low_k_mean": float(S.mean()), "exact_low_k_max": float(S.max()),
                        "first_shell_mean": float(firstS.mean()), "first_shell_max": float(firstS.max()),
                        "outside_band_mean": float(outsideS.mean()) if len(outsideS) else None,
                        "outside_band_tested": len(outside),
                        "dominant_axis_means": rows})
    cpu_points = points.cpu().numpy() % 1
    nearest, _ = cKDTree(cpu_points, boxsize=1).query(cpu_points, k=2)
    nn = nearest[:, 1]*N**(1/3)
    homotypic = []
    for c in range(5):
        d, _ = cKDTree(cpu_points[labels.cpu().numpy() == c], boxsize=1).query(cpu_points[labels.cpu().numpy() == c], k=2)
        homotypic.append(float(np.quantile(d[:, 1]*N**(1/3), .05)))
    finite_pass = all(r["exact_low_k_mean"] <= threshold and r["first_shell_mean"] <= threshold for r in records)
    grid_imprint = None
    if grid_size is not None:
        grid_modes = torch.eye(3, device=points.device, dtype=torch.float64)*grid_size
        grid_imprint = (exact_structure_factor(points, grid_modes)/N).cpu().tolist()
    return {"version": VERSION, "N": N, "counts": counts.tolist(), "physical_box_length": N**(1/3),
            "periodic_3d": True, "asymptotic_HU_established": False,
            "finite_low_k_pass": finite_pass, "finite_mean_threshold": threshold,
            "exact_audit_float64": True, "subsampled_bands": any(r["tested_modes"] < r["full_band_halfspace_modes"] for r in records),
            "components": records, "nearest_neighbor_p05_physical": float(np.quantile(nn, .05)),
            "nearest_neighbor_cv": float(nn.std()/nn.mean()), "homotypic_nearest_p05_physical": homotypic,
            "CIC_grid_axis_coherent_power_fraction": grid_imprint,
            "interpretation": "Finite low-k proxy audit; no thermodynamic-limit, isotropy, or avian-retina equivalence certificate."}


def generate(seed: int, N: int, device: str | torch.device = "cpu", *,
             iterations: int = 240, spectral: bool = True, chi: float = .12,
             local_weight: float = .15, grid_size: int | None = None,
             validate: bool = True) -> dict:
    """Create one fixed candidate; never select/retry a failed seed.

    Deterministic CPU initialization is common across treatments/devices.
    CUDA scatter-add may have floating-point nondeterminism, disclosed below.
    Failure to pass the finite audit is retained; callers must not silently
    replace the candidate and claim it as admitted multihyperuniformity.
    """
    start = time.perf_counter()
    counts = hamilton_counts(N)
    if iterations < 0 or not math.isfinite(local_weight) or local_weight <= 0:
        raise ValueError("Nonnegative iterations and positive finite local_weight required")
    dev = torch.device(device)
    # Keep CIC cells shorter than the common local smoothing length. Coarser
    # grids can induce a regular grid imprint while suppressing tested modes.
    grid_size = grid_size or max(16, 2**math.ceil(math.log2(3*N**(1/3))))
    rng = np.random.default_rng(seed)
    initial = rng.random((N, 3))
    labels_np = rng.permutation(np.repeat(np.arange(5), counts))
    points = torch.tensor(initial, device=dev, dtype=torch.float32, requires_grad=True)
    labels = torch.tensor(labels_np, device=dev, dtype=torch.long)
    data = _objective_data(counts, grid_size, chi, dev, points.dtype)
    optimizer = torch.optim.Adam([points], lr=.10/N**(1/3))
    history = []
    for step in range(iterations):
        optimizer.param_groups[0]["lr"] = (.01+.09*.5*(1+math.cos(math.pi*step/max(1, iterations-1))))/N**(1/3)
        optimizer.zero_grad(set_to_none=True)
        loss, low, local = _loss(points, labels, grid_size, data, spectral, local_weight)
        if not torch.isfinite(loss):
            raise RuntimeError("Nonfinite geometry objective; no retry")
        loss.backward()
        optimizer.step()
        with torch.no_grad():
            points.remainder_(1)
        if step == 0 or step == iterations-1 or (step+1) % 20 == 0:
            history.append({"step": step+1, "loss": float(loss.detach()),
                            "CIC_low_k": float(low.detach()), "local_density": float(local.detach())})
    if dev.type == "cuda":
        torch.cuda.synchronize(dev)
    finished = points.detach()
    validation = validate_geometry(finished, labels, chi=chi, seed=seed+99871,
                                   grid_size=grid_size) if validate else None
    return {"coordinates": finished, "labels": labels, "box_length": N**(1/3),
            "validation": validation, "history": history,
            "construction": {"version": VERSION, "seed": seed, "N": N, "iterations": iterations,
                             "spectral": spectral, "chi_requested": chi, "local_weight": local_weight,
                             "grid_size": grid_size, "device": str(dev), "dtype": "float32",
                             "initialization": "numpy PCG64 uniform plus Hamilton-label permutation",
                             "initial_coordinates": initial.tolist() if N <= 32 else None,
                             "cuda_scatter_nondeterminism": dev.type == "cuda",
                             "elapsed_seconds_including_exact_validation": time.perf_counter()-start}}
