import numpy as np
import pytest

from larp.geometry import generate_geometry, relabel_geometry, minimum_image
from larp.graphs import (build_graph, directed_degree_preserving_swaps, directed_distances,
    graph_metrics, grid_cardinal_graph, hop_type_coverage, knn_graph,
    periodic_delaunay_graph, random_regular_graph, small_world_graph, validate_edge_index)


def test_knn_exact_incoming_direction_and_periodic_neighbor():
    points=np.array([[.1,0.],[9.9,0.],[5.,0.],[5.,1.]])
    edges=knn_graph(points,10,k=1)
    assert (edges[:,edges[1]==0].ravel()==[1,0]).all()
    assert (edges[:,edges[1]==1].ravel()==[0,1]).all()
    assert np.bincount(edges[1]).tolist()==[1]*4
    assert len(set(map(tuple,edges.T)))==4


def test_knn_contract_labels_and_ties_deterministic():
    geometry=generate_geometry(400,1101,"grid")
    edges=knn_graph(geometry.points,geometry.L)
    shuffle=relabel_geometry(geometry,"shuffle")
    assert edges.shape==(2,2400)
    validate_edge_index(edges,400,k=6)
    assert np.array_equal(edges,knn_graph(shuffle.points,shuffle.L))
    assert np.array_equal(edges,knn_graph(geometry.points,geometry.L))
    # Cardinal sites precede any diagonal site: ID hashes only break ties.
    for i in range(400):
        sources=edges[0,edges[1]==i]
        lengths=np.linalg.norm(minimum_image(geometry.points[sources]-geometry.points[i],geometry.L),axis=1)
        assert np.sum(np.isclose(lengths,1))==4
        assert np.allclose(np.sort(lengths)[4:],np.sqrt(2))


def test_directed_paths_follow_sources_to_targets():
    edges=np.array([[0,1,2],[1,2,3]])
    distances=directed_distances(edges,4)
    assert distances[0,3]==3
    assert np.isinf(distances[3,0])
    metrics=graph_metrics(edges,4)
    assert metrics["SCC_count"]==4
    assert metrics["finite_diameter"]==3
    assert metrics["inaccessible_fraction"]==pytest.approx(.5)
    assert metrics["reciprocity"]==0


def test_periodic_delaunay_generic_topology_and_translation():
    geometry=generate_geometry(100,51,"poisson")
    edges,diagnostics=periodic_delaunay_graph(geometry.points,geometry.L,return_diagnostics=True)
    validate_edge_index(edges,100)
    assert edges.shape==(2,600)
    assert diagnostics["translation_invariance"]=="PASS"
    assert diagnostics["generic_torus_3N_edges"]
    assert graph_metrics(edges,100,spectral=False)["reciprocity"]==1
    translated=(geometry.points+np.array([1.7,3.2]))%geometry.L
    assert np.array_equal(edges,periodic_delaunay_graph(translated,geometry.L))


def test_ecological_cardinal_and_small_world_remote_rules():
    geometry=generate_geometry(100,51,"grid")
    cardinal=grid_cardinal_graph(geometry.points,geometry.L)
    validate_edge_index(cardinal,100,k=4)
    causal=small_world_graph(geometry.points,geometry.L,22,regime="causal")
    ecological=small_world_graph(geometry.points,geometry.L,22,regime="ecological")
    validate_edge_index(causal,100,k=6)
    validate_edge_index(ecological,100,k=6)
    for i in range(100):
        neighbors=ecological[0,ecological[1]==i]
        local=set(cardinal[0,cardinal[1]==i])
        assert local.issubset(set(neighbors))
        remote=np.asarray([j for j in neighbors if j not in local])
        d=np.linalg.norm(minimum_image(geometry.points[remote]-geometry.points[i],geometry.L),axis=1)
        assert np.all(d>=geometry.L/4)


def test_regular_degree_connected_seed_reproducible():
    edges,diag=random_regular_graph(100,29,return_diagnostics=True)
    validate_edge_index(edges,100,k=6)
    assert np.bincount(edges[0]).tolist()==[6]*100
    assert np.array_equal(edges,random_regular_graph(100,29))
    assert not np.array_equal(edges,random_regular_graph(100,30))
    assert diag["connected"]
    assert graph_metrics(edges,100,spectral=False)["SCC_count"]==1


def test_degree_swaps_do_not_repair_or_change_each_node_degree():
    geometry=generate_geometry(100,1101,"poisson")
    edges=knn_graph(geometry.points,geometry.L)
    swapped=directed_degree_preserving_swaps(edges,100,91,proposals=1000,test_only=True)
    validate_edge_index(swapped,100,k=6)
    assert np.array_equal(np.bincount(edges[0],minlength=100),np.bincount(swapped[0],minlength=100))
    assert np.array_equal(np.bincount(edges[1],minlength=100),np.bincount(swapped[1],minlength=100))
    assert not np.array_equal(edges,swapped)


def test_hop_coverage_is_incoming_receptive_field():
    edges=np.array([[0,1,2,3],[1,2,3,4]])
    labels=np.arange(5)
    result=hop_type_coverage(edges,labels,5,hops=(1,2,4))
    counts=np.array(result["1"]["counts_by_node_and_type"])
    assert counts[1].tolist()==[1,1,0,0,0]
    assert counts[0].tolist()==[1,0,0,0,0]
    assert np.array(result["4"]["counts_by_node_and_type"])[4].tolist()==[1]*5


def test_build_graph_names_and_validation_failures():
    geometry=generate_geometry(100,1,"grid")
    assert build_graph(geometry).shape==(2,600)
    assert build_graph(geometry,"cardinal").shape==(2,400)
    for bad in (np.array([[0],[0]]),np.array([[0,0],[1,1]]),np.array([[0],[100]])):
        with pytest.raises(ValueError): validate_edge_index(bad,100)

