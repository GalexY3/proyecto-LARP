"""The tied recurrent LARP block (contract F/G), without global communication.

All outputs are raw logits at every substrate node. A caller must select the
registered output ports; removed ports are failures, not sigmoid(0) predictions.
The optional collapse intervention mixes *complete increment functions* (J5).
"""
from __future__ import annotations

import math
from copy import deepcopy

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


# Numeric keys, never Python's process-dependent hash. Base modules keep the
# same initialization across G/T/F and 25/29 channel branches at identical seed.
MODULE_KEYS = {"encoder": 101, "message": 102, "distance": 103,
               "update1": 104, "update2": 105, "readout1": 106,
               "readout2": 107, "q": 108, "adapter_u": 109,
               "adapter_v": 110}


def _generator(seed: int, name: str) -> torch.Generator:
    value = int(np.random.SeedSequence([int(seed), MODULE_KEYS[name]])
                .generate_state(1, dtype=np.uint64)[0])
    return torch.Generator(device="cpu").manual_seed(value % (2**63 - 1))


class LARPModel(nn.Module):
    """G: shared q/rank10; T: type q/rank10; F: type q/five rank2.

    ``edge_index[0]`` is source and ``edge_index[1]`` is target. The update is
    synchronous: an input can influence only nodes at directed distance <= T.
    ``alive`` may be [N] or [B,N], and ``edge_alive`` [E] or [B,E]. No edge is
    created by these masks. Labels are computationally invisible in G.
    """

    def __init__(self, variant: str = "T", output_dim: int = 8,
                 input_dim: int = 25, seed: int = 2101):
        super().__init__()
        variant = variant.upper()
        if variant not in {"G", "T", "F"}:
            raise ValueError("variant must be G, T or F")
        if input_dim not in {25, 29} or output_dim < 1:
            raise ValueError("input_dim must be 25 or 29; output_dim positive")
        self.variant, self.output_dim, self.input_dim = variant, output_dim, input_dim
        self.seed, self.d, self.rank = int(seed), 32, 2 if variant == "F" else 10
        # Module constructors consume RNG internally; keep the external RNG intact.
        with torch.random.fork_rng(devices=[]):
            self.encoder = nn.Linear(input_dim, 32)
            self.normalization = nn.LayerNorm(32, eps=1e-5)
            self.message = nn.Linear(32, 32)
            self.distance_weight = nn.Parameter(torch.empty(32))
            self.update1 = nn.Linear(100, 64)
            self.update2 = nn.Linear(64, 32)
            self.readout1 = nn.Linear(32, 32)
            self.readout2 = nn.Linear(32, output_dim)
            self.q = nn.Parameter(torch.empty(4 if variant == "G" else (5, 4)))
            adapter_shape_u = (5, 32, 2) if variant == "F" else (32, 10)
            adapter_shape_v = (5, 2, 32) if variant == "F" else (10, 32)
            self.adapter_u = nn.Parameter(torch.empty(adapter_shape_u))
            self.adapter_v = nn.Parameter(torch.empty(adapter_shape_v))
        # An arithmetic identity key follows global renaming. It has no learned
        # capacity and affects only reduction order in the conditional M1 assay.
        self.register_buffer("function_ids", torch.arange(5, dtype=torch.long))
        self.reset_parameters()

    def reset_parameters(self) -> None:
        for name in ("encoder", "message", "update1", "update2", "readout1", "readout2"):
            layer = getattr(self, name)
            nn.init.xavier_uniform_(layer.weight, gain=1.0, generator=_generator(self.seed, name))
            nn.init.zeros_(layer.bias)
        # w_r is a 32x1 principal linear without its own bias.
        with torch.no_grad():
            nn.init.xavier_uniform_(self.distance_weight.view(32, 1),
                                    generator=_generator(self.seed, "distance"))
            nn.init.ones_(self.normalization.weight)
            nn.init.zeros_(self.normalization.bias)
            if self.variant == "G":
                self.q.zero_()
            else:
                self.q.normal_(0, 0.02, generator=_generator(self.seed, "q"))
                self.q.sub_(self.q.mean(dim=0, keepdim=True))
            self.adapter_u.normal_(0, 1 / math.sqrt(32),
                                   generator=_generator(self.seed, "adapter_u"))
            self.adapter_v.normal_(0, 1 / math.sqrt(32),
                                   generator=_generator(self.seed, "adapter_v"))

    @property
    def parameter_count(self) -> int:
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    @property
    def expected_parameter_count(self) -> int:
        return (12228 if self.variant == "G" else 12244) + 33 * self.output_dim + 32 * (self.input_dim - 25)

    @property
    def adapter_mac_per_node(self) -> int:
        return 2 * 32 * self.rank

    def _adapter(self, z: torch.Tensor, labels: torch.Tensor | None) -> torch.Tensor:
        if self.variant != "F":
            return F.linear(torch.tanh(F.linear(z, self.adapter_v)), self.adapter_u) / math.sqrt(self.rank)
        u, v = self.adapter_u[labels], self.adapter_v[labels]
        hidden = torch.tanh(torch.einsum("nrd,bnd->bnr", v, z))
        return torch.einsum("ndr,bnr->bnd", u, hidden) / math.sqrt(self.rank)

    def increment(self, z: torch.Tensor, message: torch.Tensor, encoded: torch.Tensor,
                  labels: torch.Tensor | None) -> torch.Tensor:
        q = self.q.expand(z.shape[0], z.shape[1], 4) if self.variant == "G" else self.q[labels].unsqueeze(0).expand(z.shape[0], -1, -1)
        base = self.update2(F.silu(self.update1(torch.cat((z, message, encoded, q), dim=-1))))
        return base + self._adapter(z, labels)

    def complete_type_increments(self, z: torch.Tensor, message: torch.Tensor,
                                 encoded: torch.Tensor) -> torch.Tensor:
        """Return [5,B,N,32] complete f_c at identical state/input/message."""
        if self.variant == "G":
            raise ValueError("M1 type-function intervention is only defined for T/F")
        functions = {}
        for c in torch.argsort(self.function_ids).tolist():
            functions[c] = self.increment(z, message, encoded,
                           torch.full((z.shape[1],), c, device=z.device, dtype=torch.long))
        return torch.stack([functions[c] for c in range(5)])

    def forward(self, inputs: torch.Tensor, edge_index: torch.Tensor,
                edge_dist: torch.Tensor, labels: torch.Tensor | None,
                steps: int = 16, alive: torch.Tensor | None = None,
                edge_alive: torch.Tensor | None = None,
                collapse_lambda: float = 0.0,
                return_states: bool = False):
        if inputs.ndim != 3 or inputs.shape[-1] != self.input_dim:
            raise ValueError("inputs must have shape [B,N,input_dim]")
        if steps < 0 or not 0 <= collapse_lambda <= 1:
            raise ValueError("steps nonnegative and collapse_lambda in [0,1] required")
        if collapse_lambda and self.variant == "G":
            raise ValueError("collapse is defined only for T/F")
        b, n, _ = inputs.shape
        edge_index = torch.as_tensor(edge_index, dtype=torch.long, device=inputs.device)
        if edge_index.ndim != 2 or edge_index.shape[0] != 2:
            raise ValueError("edge_index must be [2,E], source then target")
        source, target = edge_index
        if edge_index.numel() and (int(edge_index.min()) < 0 or int(edge_index.max()) >= n):
            raise ValueError("edge IDs out of range")
        edge_dist = torch.as_tensor(edge_dist, dtype=inputs.dtype, device=inputs.device).reshape(-1)
        if len(edge_dist) != len(source):
            raise ValueError("one distance per directed edge required")
        if self.variant != "G":
            labels = torch.as_tensor(labels, dtype=torch.long, device=inputs.device)
            if labels.shape != (n,) or torch.any((labels < 0) | (labels > 4)):
                raise ValueError("labels must contain one class 0..4 per node")
        live = torch.ones((b, n), dtype=torch.bool, device=inputs.device) if alive is None else torch.as_tensor(alive, dtype=torch.bool, device=inputs.device).expand(b, n)
        arc_live = live[:, source] & live[:, target]
        if edge_alive is not None:
            arc_live = arc_live & torch.as_tensor(edge_alive, dtype=torch.bool, device=inputs.device).expand(b, len(source))
        count = inputs.new_zeros((b, n))
        count.index_add_(1, target, arc_live.to(inputs.dtype))
        count = count.clamp_min(1).unsqueeze(-1)
        live_float = live.unsqueeze(-1).to(inputs.dtype)
        encoded = self.encoder(inputs) * live_float
        h = encoded
        edge_feature = torch.log1p(edge_dist).view(1, -1, 1) * self.distance_weight.view(1, 1, 32)
        states = [h] if return_states else None
        frequencies = None
        if collapse_lambda:
            frequencies = torch.bincount(labels, minlength=5).to(inputs.dtype) / n
        for _ in range(steps):
            z = self.normalization(h)
            # Matrix multiplication once per node; expand only the transformed state.
            node_message = self.message(z)
            messages = torch.tanh(node_message[:, source] + edge_feature)
            messages = messages * arc_live.unsqueeze(-1).to(inputs.dtype)
            aggregated = inputs.new_zeros((b, n, 32))
            aggregated.index_add_(1, target, messages)
            aggregated = aggregated / count
            increment = self.increment(z, aggregated, encoded, labels)
            if collapse_lambda:
                functions = self.complete_type_increments(z, aggregated, encoded)
                canonical_order = torch.argsort(self.function_ids)
                mean_function = (functions[canonical_order]
                                 * frequencies[canonical_order, None, None, None]).sum(0)
                increment = (1 - collapse_lambda) * increment + collapse_lambda * mean_function
            h = (h + 0.1 * increment) * live_float
            if return_states:
                states.append(h)
        logits = self.readout2(F.silu(self.readout1(h))) * live_float
        return (logits, states) if return_states else logits

    def rename_types_(self, permutation) -> "LARPModel":
        """Move parameters so new_labels=permutation[old_labels] is a symmetry.

        Counts/frequency metadata must be renamed along with labels by callers.
        This operation is a diagnostic on a frozen model, not an optimizer step.
        """
        permutation = torch.as_tensor(permutation, dtype=torch.long, device=self.q.device)
        if permutation.shape != (5,) or sorted(permutation.tolist()) != list(range(5)):
            raise ValueError("a permutation of 0..4 is required")
        if self.variant != "G":
            with torch.no_grad():
                old_q = self.q.clone()
                self.q[permutation] = old_q
                old_ids = self.function_ids.clone()
                self.function_ids[permutation] = old_ids
                if self.variant == "F":
                    old_u, old_v = self.adapter_u.clone(), self.adapter_v.clone()
                    self.adapter_u[permutation], self.adapter_v[permutation] = old_u, old_v
        return self

    def renamed_copy(self, permutation) -> "LARPModel":
        return deepcopy(self).rename_types_(permutation)
