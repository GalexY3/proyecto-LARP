import numpy as np
import torch
from larp.scale3d_train import SpatialNetwork,graph_data,world,features_at,observations,targets


def fixture():
    rng=np.random.default_rng(9)
    x=torch.tensor(rng.random((40,3)),dtype=torch.float32)
    z=torch.arange(40)%5
    q=torch.tensor(rng.random((7,3)),dtype=torch.float32)
    g,_=graph_data(x,z,q,4,'cpu')
    return g,q


def test_marked_observations_do_not_leak_hidden_channels():
    phi=torch.eye(4)
    coeff=torch.arange(20,dtype=torch.float32).reshape(1,5,4)
    z=torch.tensor([0,1,2,3])
    torch.testing.assert_close(observations(coeff,phi,z),torch.tensor([[0.,5.,10.,15.]]))


def test_identical_models_geometry_match_and_receive_gradients():
    g,q=fixture();torch.manual_seed(3)
    first=SpatialNetwork(12,2);second=SpatialNetwork(12,2)
    second.load_state_dict(first.state_dict())
    obs=torch.randn(2,40)
    a=first(obs,g,q,2);b=second(obs,g,q,2)
    torch.testing.assert_close(a,b)
    assert a.shape==(2,7,5)
    a.square().mean().backward()
    assert all(p.grad is not None and torch.isfinite(p.grad).all() for p in first.parameters())


def test_cubic_tasks_and_random_worlds_are_common_and_periodic():
    modes=torch.tensor([[1.,0.,0.],[0.,1.,0.]])
    points=torch.tensor([[.2,.3,.4],[.9,.1,.8]])
    torch.testing.assert_close(features_at(points,modes),features_at(points+1,modes),atol=1e-6,rtol=1e-6)
    a=world(12,2,2,'cpu');b=world(12,2,2,'cpu')
    torch.testing.assert_close(a,b)
    f=torch.tensor([[[2.,3.,4.,5.,6.]]])
    torch.testing.assert_close(targets(f,2),torch.tensor([[[6.,12.,20.,30.,48.]]]))
