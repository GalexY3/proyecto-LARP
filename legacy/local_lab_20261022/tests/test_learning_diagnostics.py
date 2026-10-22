import numpy as np
import torch

from larp.data import register_ports
from larp.geometry import generate_geometry
from larp.learning_diagnostics import PATTERNS, bind_cases, finite_gate, graph_context, make_cases, select_common_pool


def test_direct_local_has_two_independent_bits_and_no_role_channels():
    geometry = generate_geometry(N=400, seed=1101, kind="grid")
    context = graph_context(geometry)
    batch = bind_cases(context, make_cases([[0, -1, -1]]), "direct_local")
    destination = int(context["ports"].indices[0])
    assert torch.equal(batch["inputs"][:, destination, 1:3], torch.tensor(PATTERNS))
    assert torch.count_nonzero(batch["inputs"][:, :, 9:19]) == 0
    assert torch.equal(batch["inputs"][:, :, 0].sum(1), torch.ones(4))
    assert torch.equal(batch["target"].ravel(), torch.tensor([0., 1., 1., 0.]))


def test_separate_interface_preserves_role_payload_and_xor_flips():
    context = graph_context(generate_geometry(N=400, seed=1101, kind="grid"))
    batch = bind_cases(context, make_cases([[0, 1, 2]]), "remote")
    nodes = context["ports"].indices
    assert torch.equal(batch["inputs"][:, nodes[1], 1], torch.tensor(PATTERNS[:, 0]))
    assert torch.equal(batch["inputs"][:, nodes[2], 1], torch.tensor(PATTERNS[:, 1]))
    assert torch.all(batch["inputs"][:, nodes[1], 9] == 1)
    assert torch.all(batch["inputs"][:, nodes[2], 10] == 1)
    assert torch.all(batch["inputs"][:, nodes[0], 14:16] == 1)
    assert torch.equal(batch["inputs"][:, :, 0].sum(1), torch.full((4,), 3.))


def test_unavailable_pool_cannot_silently_expand_hops():
    context = graph_context(generate_geometry(N=400, seed=1101, kind="grid"))
    context["hops"][:] = np.inf
    cfg = {"local_hops": [1, 2], "remote_minimum_physical_distance": 5., "common_destinations": 16}
    pool = select_common_pool({"grid": context}, cfg)
    assert pool["status"] == "DIAGNOSTIC_UNAVAILABLE"
    assert pool["admissible_destination_count"] == 0


def test_success_gate_requires_final_complete_and_finite():
    base = {"status": "COMPLETE", "finite": True, "final": {"accuracy": 1.}}
    assert finite_gate(base)
    assert not finite_gate({**base, "finite": False})
    assert not finite_gate({**base, "status": "RESOURCE_LIMIT"})
    assert not finite_gate({**base, "final": {"accuracy": .75}})
