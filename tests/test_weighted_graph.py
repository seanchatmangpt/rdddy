import pytest

from practice.shortest_path_weighted_graph import WeightedGraph, dijkstra_with_min_edges


def test_simple_path():
    graph = WeightedGraph(4)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 2)
    graph.add_edge(2, 3, 3)
    distance, edges = dijkstra_with_min_edges(graph, 0, 3)
    assert distance == 6
    assert edges == 3


def test_path_with_equal_weights_different_edges():
    graph = WeightedGraph(3)
    graph.add_edge(0, 1, 2)
    graph.add_edge(1, 2, 2)
    graph.add_edge(0, 2, 4)  # Shorter path in terms of edges but equal weight
    distance, edges = dijkstra_with_min_edges(graph, 0, 2)
    assert distance == 4
    assert edges == 1


def test_no_path_exists():
    graph = WeightedGraph(3)
    graph.add_edge(0, 1, 1)
    # No edge from 1 to 2 or from 0 to 2
    distance, edges = dijkstra_with_min_edges(graph, 0, 2)
    assert distance == float("inf")
    assert edges == float("inf")


def test_loop_in_graph():
    graph = WeightedGraph(4)
    graph.add_edge(0, 1, 1)
    graph.add_edge(1, 2, 2)
    graph.add_edge(2, 1, 1)  # Creates a loop
    graph.add_edge(2, 3, 4)
    distance, edges = dijkstra_with_min_edges(graph, 0, 3)
    assert distance == 7
    assert edges == 3
