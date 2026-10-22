import json
import numpy as np
import pytest

from larp.geometry import (
    Geometry, array_hash, certify_geometry, common_window_centers,
    finite_difference_gradient_check, generate_geometry, geometry_objective,
    hamilton_counts, integer_modes, load_geometry, matched_energy,
    mark_features, minimum_image, periodic_distances, relabel_geometry,
    save_geometry, spectral_amplitudes, structure_factors,
    toroidal_voronoi_areas, window_statistics,
)


@pytest.mark.parametrize("N,expected", [(400, [163,85,68,50,34]),
    (1600,[651,338,274,201,136]), (6400,[2605,1351,1094,806,544])])
def test_hamilton_exact_preregistered_counts(N, expected):
    assert hamilton_counts(N).tolist() == expected
    assert np.all(hamilton_counts(N, equal=True) == N//5)


def test_minimum_image_boundary():
    assert np.allclose(minimum_image(np.array([[19., -19.], [10., -10.]]), 20), [[-1,1],[10,-10]])
    assert periodic_distances(np.array([[.1,.1]]), np.array([[19.9,.1]]),20)[0,0] == pytest.approx(.2)


def test_modes_400_and_fixed_physical_cutoff():
    assert integer_modes(20).tolist() == [[1,0],[0,1],[1,1],[1,-1],[2,0],[0,2]]
    for L in (20,40,80):
        modes = integer_modes(L)
        assert np.max(np.linalg.norm(2*np.pi/L*modes,axis=1)) <= np.pi/5+1e-12
        assert all(x>0 or x==0 and y>0 for x,y in modes)


def test_objective_gradient_and_periodicity_with_active_repulsion():
    rng=np.random.default_rng(37)
    points=rng.uniform(0,20,(60,2))
    points[0]=[.08,.1]; points[1]=[19.96,.1]
    labels=np.repeat(np.arange(5),12)
    assert finite_difference_gradient_check(points,labels,20,coordinates=20)["passed"]
    f,g,info=geometry_objective(points,labels,20,details=True)
    assert info["active_pairs"] >= 1
    shifted_f,shifted_g=geometry_objective(points+np.array([20,-40]),labels,20)
    assert f == pytest.approx(shifted_f,abs=1e-12)
    assert np.allclose(g,shifted_g,atol=1e-12)
    assert np.allclose(g.sum(axis=0),0,atol=1e-12)
    assert finite_difference_gradient_check(points,labels,20,coordinates=20,kind="hu")["passed"]


def test_amplitude_identity_and_bound():
    rng=np.random.default_rng(21)
    points=rng.uniform(0,20,(400,2))
    labels=np.repeat(np.arange(5),hamilton_counts(400))
    amplitudes=spectral_amplitudes(points,labels,20)
    assert np.allclose(amplitudes[:5].sum(axis=0),amplitudes[5])
    S=structure_factors(points,labels,20)
    assert np.all(S[5] <= S[:5].sum(axis=0)+1e-12)


def test_seed_geometry_immutability_and_artifact_roundtrip(tmp_path):
    a=generate_geometry(100,11,"poisson")
    b=generate_geometry(100,11,"poisson")
    c=generate_geometry(100,12,"poisson")
    assert a.hashes == b.hashes
    assert a.hashes["points"] != c.hashes["points"]
    with pytest.raises(ValueError): a.points[0,0]=1
    with pytest.raises(ValueError): a.points.setflags(write=True)
    with pytest.raises(TypeError): a.metadata["kind"]="changed"
    path=tmp_path/"geometry.npz"
    save_geometry(a,path)
    assert load_geometry(path).hashes == a.hashes
    save_geometry(b,path)
    with pytest.raises(FileExistsError): save_geometry(c,path)


def test_mark_controls_preserve_exact_points_and_counts():
    geometry=generate_geometry(400,1101,"poisson")
    for control in ("shuffle","clustered"):
        changed=relabel_geometry(geometry,control)
        assert changed.hashes["points"] == geometry.hashes["points"]
        assert np.array_equal(np.bincount(changed.labels),np.bincount(geometry.labels))
        assert not np.array_equal(changed.labels,geometry.labels)
        assert changed.metadata["certificate"]["scientific_admissible"] is False
    assert np.array_equal(relabel_geometry(geometry,"shuffle").labels,relabel_geometry(geometry,"shuffle").labels)


def test_window_centers_common_and_variance_formula():
    geometry=generate_geometry(100,9,"grid",equal=True)
    centers=common_window_centers(geometry.L)
    assert array_hash(centers)==array_hash(common_window_centers(geometry.L))
    stats=window_statistics(geometry,centers)
    p=np.pi*np.array([.5,1,2,3,4,5])**2/100
    assert np.allclose(stats["union"]["binomial_reference"],100*p*(1-p))
    assert len(stats["E"]["variance_ratio"])==6


def test_uncertified_poisson_and_grid_bragg_fail():
    poisson=generate_geometry(400,1101,"poisson")
    cert=certify_geometry(poisson,detailed=False)
    assert set(cert["components"])=={"A","B","C","D","E","union"}
    assert cert["passed"] is False
    assert cert["scientific_admissible"] is False
    grid=generate_geometry(400,1101,"grid",equal=True)
    cert_grid=certify_geometry(grid,detailed=False)
    # First lattice Bragg peak is outside |k|<=pi, but components can have
    # strong lower-frequency peaks. The union itself fails no low-k test.
    assert cert_grid["minimum_distance_passed"]
    assert cert_grid["components"]["union"]["restricted_max_S"] < 1e-20


def test_reduced_geometry_budget_never_admissible():
    with pytest.raises(ValueError): generate_geometry(100,11,"mhu",adam_steps=1)
    geometry=generate_geometry(100,11,"mhu",test_only=True,adam_steps=2,lbfgs_iterations=1,max_restarts=1,detailed_certificate=False)
    assert geometry.metadata["test_only"]
    assert not geometry.metadata["certificate"]["scientific_admissible"]


def test_voronoi_toroidal_area():
    geometry=generate_geometry(100,99,"poisson")
    area=toroidal_voronoi_areas(geometry.points,geometry.L)
    assert len(area)==100
    assert np.all(area>0)
    assert area.sum()==pytest.approx(100,abs=1e-7)


def test_equal_grid_balanced_sublattice():
    geometry=generate_geometry(400,19,"grid",equal=True)
    balanced=relabel_geometry(geometry,"grid_balanced")
    xy=np.floor(geometry.points).astype(int)
    assert np.array_equal(balanced.labels,(xy[:,0]+2*xy[:,1])%5)
    assert balanced.hashes["points"]==geometry.hashes["points"]
    assert np.bincount(balanced.labels).tolist()==[80]*5


def test_matched_energy_requires_each_class_spectral_loss_and_counts():
    reference={"directed_type_edge_matrix":np.ones((5,5))*20,
               "homotypic_pair_bins":np.ones((5,4))*10,
               "class_mean_outdegree":np.ones(5)*6}
    feature={**reference,"component_mean_low_k_S":np.ones(5)*.5}
    assert matched_energy(feature,reference)==0
    feature["component_mean_low_k_S"]=np.array([0,.5,.5,.5,.5])
    assert matched_energy(feature,reference)==pytest.approx(1)
    feature["component_mean_low_k_S"]=np.ones(5)*.5
    feature["class_mean_outdegree"]=np.array([6.2,6,6,6,6])
    assert matched_energy(feature,reference)==pytest.approx(1)


def test_matched_control_failure_is_explicit_and_never_relabels_X():
    from larp.graphs import knn_graph
    geometry=generate_geometry(100,1101,"grid",equal=True)
    edges=knn_graph(geometry.points,geometry.L)
    with pytest.raises(RuntimeError,match="SCIENTIFIC_BLOCKER"):
        relabel_geometry(geometry,"matched",edge_index=edges)
    control=relabel_geometry(geometry,"matched",edge_index=edges,test_only=True,proposals=2,restarts=1)
    assert control.hashes["points"]==geometry.hashes["points"]
    assert control.metadata["annealing"]["long_wave_mechanism_identifiable"] is False
    assert np.array_equal(np.bincount(control.labels),np.bincount(geometry.labels))


def test_incremental_mark_statistics_equal_full_recomputation():
    from larp.graphs import knn_graph
    from larp.geometry import _MarkAnnealingState
    geometry=generate_geometry(100,117,"poisson")
    edges=knn_graph(geometry.points,geometry.L)
    reference=mark_features(geometry,geometry.labels,edges)
    state=_MarkAnnealingState(geometry,geometry.labels,"matched",edges,reference)
    rng=np.random.default_rng(47)
    for _ in range(60):
        i,j=map(int,rng.integers(100,size=2))
        if state.labels[i]==state.labels[j]: continue
        state.swap(i,j)
        full=mark_features(geometry,state.labels,edges)
        assert np.array_equal(state.directed_pairs,full["directed_type_edge_matrix"])
        assert np.array_equal(state.homotypic,full["homotypic_pair_bins"])
        assert np.allclose(state.degree_sum/state.counts,full["class_mean_outdegree"])
        assert state.energy()==pytest.approx(matched_energy(full,reference),abs=1e-10)
        state.swap(i,j)
        assert np.array_equal(state.labels,geometry.labels)
