"""Prospective spectral conditioning repair; frozen v1 remains unchanged."""
from __future__ import annotations
import math
import time
import numpy as np
import torch
from . import scale3d_geometry as v1

VERSION = "scale3d_cic_multicomponent_inverse_k2_v2"


def objective_data(counts, grid_size, chi, device, dtype):
    data = v1._objective_data(counts, grid_size, chi, device, dtype)
    x = torch.fft.fftfreq(grid_size, device=device, dtype=dtype)*grid_size
    z = torch.fft.rfftfreq(grid_size, device=device, dtype=dtype)*grid_size
    kx,ky,kz = torch.meshgrid(x,x,z,indexing="ij")
    norm2 = kx.square()+ky.square()+kz.square()
    # Approximate coordinate-space curvature scales as |k|^2. Normalize
    # separately for all six components; E[S]=1 still gives expected loss 1.
    weights = data["spectral_weights"]/norm2.clamp_min(1)[None]
    data["spectral_weights"] = weights/weights.sum((-3,-2,-1),keepdim=True)
    return data


@torch.no_grad()
def full_band_audit(points, labels, validation, chi):
    """Continuous FP64 Fourier over EVERY admitted mode; no FFT proxy."""
    points = points.detach().to(dtype=torch.float64)
    labels = labels.detach()
    full_pass = True
    for component,record in zip(range(-1,5),validation["components"]):
        p = points if component == -1 else points[labels == component]
        modes,_ = v1.reciprocal_modes(len(p),chi)
        S = v1.exact_structure_factor(p,torch.as_tensor(modes,device=p.device)).cpu().numpy()
        norms = np.sum(modes*modes,axis=1)
        record["exact_full_band_mean"] = float(S.mean())
        record["exact_full_band_max"] = float(S.max())
        record["exact_full_band_modes"] = len(modes)
        record["shell_profile"] = [{"norm_squared":int(r),"modes":int(np.sum(norms==r)),
             "mean":float(S[norms==r].mean()),"max":float(S[norms==r].max())} for r in np.unique(norms)]
        full_pass &= record["exact_full_band_mean"] <= validation["finite_mean_threshold"]
    validation["full_band_audit_float64"] = True
    validation["finite_low_k_pass"] = bool(validation["finite_low_k_pass"] and full_pass)
    validation["original_sampled_gate_retained"] = True
    return validation


def generate(seed, N, device="cpu", *, iterations=600, spectral=True, chi=.12,
             local_weight=.15, grid_size=None, validate=True):
    start = time.perf_counter()
    counts = v1.hamilton_counts(N)
    if iterations < 0 or not math.isfinite(local_weight) or local_weight <= 0:
        raise ValueError("Nonnegative iterations and positive finite local_weight required")
    dev = torch.device(device)
    grid_size = grid_size or max(16,2**math.ceil(math.log2(3*N**(1/3))))
    rng = np.random.default_rng(seed)
    initial = rng.random((N,3))
    labels_np = rng.permutation(np.repeat(np.arange(5),counts))
    points = torch.tensor(initial,device=dev,dtype=torch.float32,requires_grad=True)
    labels = torch.tensor(labels_np,device=dev,dtype=torch.long)
    data = objective_data(counts,grid_size,chi,dev,points.dtype)
    optimizer = torch.optim.Adam([points],lr=.10/N**(1/3))
    history = []
    for step in range(iterations):
        optimizer.param_groups[0]["lr"] = (.01+.09*.5*(1+math.cos(math.pi*step/max(1,iterations-1))))/N**(1/3)
        optimizer.zero_grad(set_to_none=True)
        loss,low,local = v1._loss(points,labels,grid_size,data,spectral,local_weight)
        if not torch.isfinite(loss):raise RuntimeError("Nonfinite geometry objective; no retry")
        loss.backward();optimizer.step()
        with torch.no_grad():points.remainder_(1)
        if step == 0 or step == iterations-1 or (step+1)%20 == 0:
            history.append({"step":step+1,"loss":float(loss.detach()),
                            "CIC_inverse_k2_low":float(low.detach()),"local_density":float(local.detach())})
    if dev.type == "cuda":torch.cuda.synchronize(dev)
    finished = points.detach()
    validation = None
    if validate:
        validation = v1.validate_geometry(finished,labels,chi=chi,seed=seed+99871,grid_size=grid_size)
        validation["audit_implementation_version"] = validation["version"]
        validation["version"] = VERSION
        full_band_audit(finished,labels,validation,chi)
    return {"coordinates":finished,"labels":labels,"box_length":N**(1/3),"validation":validation,"history":history,
        "construction":{"version":VERSION,"seed":seed,"N":N,"iterations":iterations,"spectral":spectral,
            "chi_requested":chi,"local_weight":local_weight,"grid_size":grid_size,"device":str(dev),
            "dtype":"float32","spectral_weighting":"inverse integer norm squared, separately normalized",
            "initialization":"numpy PCG64 uniform plus Hamilton-label permutation",
            "cuda_scatter_nondeterminism":dev.type=="cuda",
            "elapsed_seconds_including_exact_validation":time.perf_counter()-start}}
