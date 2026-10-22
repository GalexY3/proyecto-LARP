"""Finite local propagation, exact symmetries, matching and actual gradients."""
import numpy as np
import pytest
import torch

from larp.model import LARPModel


def graph_fixture(n=10):
    edge = torch.stack((torch.arange(n - 1), torch.arange(1, n)))
    dist = torch.ones(n - 1)
    labels = torch.arange(n) % 5
    x = torch.randn(2, n, 25, generator=torch.Generator().manual_seed(190))
    return x, edge, dist, labels


@pytest.mark.parametrize("variant", ["G", "T", "F"])
@pytest.mark.parametrize("output_dim", [1, 8])
def test_parameter_count_and_finite_backward(variant, output_dim):
    model = LARPModel(variant, output_dim)
    assert model.parameter_count == model.expected_parameter_count
    assert model.parameter_count == (12228 if variant == "G" else 12244) + 33 * output_dim
    x, edge, dist, labels = graph_fixture()
    output = model(x, edge, dist, labels, steps=3)
    assert output.shape == (2, 10, output_dim)
    assert torch.isfinite(output).all()
    output.square().mean().backward()
    # All actual parameter tensors participate; F uses all five labels here.
    for parameter in model.parameters():
        assert parameter.requires_grad and parameter.grad is not None
        assert torch.isfinite(parameter.grad).all()
        assert torch.count_nonzero(parameter.grad) > 0


def test_resource_parameter_increment():
    for variant in ("G", "T", "F"):
        standard = LARPModel(variant, 1)
        resource = LARPModel(variant, 1, input_dim=29)
        assert resource.parameter_count - standard.parameter_count == 128
        if variant != "G":
            assert resource.parameter_count == 12405


def test_shared_initialization_and_global_rng_unchanged():
    torch.manual_seed(141)
    before = torch.random.get_rng_state().clone()
    models = [LARPModel(v, 8, seed=2101) for v in ("G", "T", "F")]
    assert torch.equal(before, torch.random.get_rng_state())
    for module in ("encoder", "message", "update1", "update2", "readout1", "readout2", "normalization"):
        for left, right in zip(getattr(models[0], module).parameters(), getattr(models[2], module).parameters()):
            assert torch.equal(left, right)
    assert torch.equal(models[1].q, models[2].q)
    assert not torch.equal(models[1].encoder.weight, LARPModel("T", seed=2102).encoder.weight)


def test_G_mark_invariance_outputs_loss_and_gradients_exact():
    model = LARPModel("G", 1)
    x, edge, dist, labels = graph_fixture()
    shuffled = labels.flip(0)
    first = model(x, edge, dist, labels, steps=3)
    first.square().mean().backward()
    gradients = {name: p.grad.clone() for name, p in model.named_parameters()}
    model.zero_grad(set_to_none=True)
    second = model(x, edge, dist, shuffled, steps=3)
    second.square().mean().backward()
    assert torch.equal(first, second)
    for name, parameter in model.named_parameters():
        assert torch.equal(parameter.grad, gradients[name])
    assert torch.equal(first, model(x, edge, dist, None, steps=3))


@pytest.mark.parametrize("variant", ["T", "F"])
@pytest.mark.parametrize("collapse_lambda", [0.0, 0.5, 1.0])
def test_type_renaming_is_exact_including_gradients(variant, collapse_lambda):
    model = LARPModel(variant, 1)
    permutation = torch.tensor([3, 0, 4, 1, 2])
    renamed = model.renamed_copy(permutation)
    x, edge, dist, labels = graph_fixture()
    # Unequal counts ensure frequencies are correctly relabeled too.
    labels = torch.tensor([0, 0, 0, 0, 1, 1, 2, 2, 3, 4])
    output = model(x, edge, dist, labels, steps=3, collapse_lambda=collapse_lambda)
    renamed_output = renamed(x, edge, dist, permutation[labels], steps=3, collapse_lambda=collapse_lambda)
    assert torch.equal(output, renamed_output)
    output.square().mean().backward()
    renamed_output.square().mean().backward()
    for name, parameter in model.named_parameters():
        gradient = dict(renamed.named_parameters())[name].grad
        if name == "q" or (variant == "F" and name.startswith("adapter_")):
            gradient = gradient[permutation]
        assert torch.equal(parameter.grad, gradient)


def test_forward_receptive_field_and_direction_are_exact():
    model = LARPModel("T", 1)
    x, edge, dist, labels = graph_fixture()
    altered = x.clone()
    altered[:, 0, 1] += 2
    base, changed = model(x, edge, dist, labels, steps=2), model(altered, edge, dist, labels, steps=2)
    assert torch.equal(base[:, 3:], changed[:, 3:])
    assert not torch.equal(base[:, 2], changed[:, 2])
    # Source/target convention: changing node 9 cannot affect node 0 in this DAG.
    altered = x.clone()
    altered[:, 9, 1] += 2
    assert torch.equal(base[:, :9], model(altered, edge, dist, labels, steps=2)[:, :9])


def test_batch_isolation_exact():
    model = LARPModel("F", 1)
    x, edge, dist, labels = graph_fixture()
    altered = x.clone()
    altered[1] += 20
    assert torch.equal(model(x, edge, dist, labels, steps=3)[0],
                       model(altered, edge, dist, labels, steps=3)[0])


def test_dead_nodes_have_no_encoder_state_message_or_readout():
    model = LARPModel("T", 1)
    x, edge, dist, labels = graph_fixture()
    alive = torch.ones(10, dtype=torch.bool)
    alive[1] = False
    first, states = model(x, edge, dist, labels, steps=4, alive=alive, return_states=True)
    changed = x.clone()
    changed[:, 1] += 100
    assert torch.equal(first, model(changed, edge, dist, labels, steps=4, alive=alive))
    assert all(torch.count_nonzero(state[:, 1]) == 0 for state in states)
    assert torch.count_nonzero(first[:, 1]) == 0
    # The dead intermediate node also prevents source 0 reaching node 2.
    changed = x.clone()
    changed[:, 0] += 100
    assert torch.equal(first[:, 2:], model(changed, edge, dist, labels, steps=4, alive=alive)[:, 2:])


def test_zero_neighbor_mean_and_edge_mask():
    model = LARPModel("G", 1)
    x, edge, dist, labels = graph_fixture()
    masked = model(x, edge, dist, labels, steps=3, edge_alive=torch.zeros(len(dist), dtype=torch.bool))
    empty = model(x, edge[:, :0], dist[:0], labels, steps=3)
    assert torch.equal(masked, empty)


def test_M1_mixes_complete_functions_not_adapter_factors():
    model = LARPModel("F", 1)
    x, _, _, labels = graph_fixture()
    z, message, encoded = x[..., :32] if x.shape[-1] >= 32 else torch.randn(2, 10, 32), torch.randn(2, 10, 32), torch.randn(2, 10, 32)
    functions = model.complete_type_increments(z, message, encoded)
    assert functions.shape == (5, 2, 10, 32)
    for c in range(5):
        assert torch.equal(functions[c], model.increment(z, message, encoded, torch.full_like(labels, c)))
    # At lambda=0 intervention is exactly the preregistered original model.
    x, edge, dist, labels = graph_fixture()
    assert torch.equal(model(x, edge, dist, labels, steps=2),
                       model(x, edge, dist, labels, steps=2, collapse_lambda=0))
