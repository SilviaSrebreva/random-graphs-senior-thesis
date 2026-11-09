import random

from ER_generator import generate_erdos_renyi_gnp
from BA_generator import generate_ba


def check_graph(n, adj_list, edge_list):
    # helper: adj_list and edge_list describe the same simple graph

    # no self-loops
    for u, v in edge_list:
        assert u != v

    # no duplicate edges ((0, 1) and (1, 0) count as the same edge)
    sorted_edges = [(min(u, v), max(u, v)) for u, v in edge_list]
    assert len(set(sorted_edges)) == len(edge_list)

    # every edge is in the adj_list in both directions
    for u, v in edge_list:
        assert v in adj_list[u]
        assert u in adj_list[v]

    # degrees add up to 2 * edges, so the adj_list has no extra edges
    total_degree = sum(len(adj_list[node]) for node in adj_list)
    assert total_degree == 2 * len(edge_list)

    assert len(adj_list) == n


# PRIMARY

def test_ba_number_of_edges():
    random.seed(5)
    n, m = 100, 2
    adj_list, edge_list, history = generate_ba(n, m)
    # seed clique of m + 1 nodes has m(m+1)/2 edges, then every other node brings m
    assert len(edge_list) == m * (m + 1) // 2 + (n - m - 1) * m


def test_er_p_0_has_no_edges():
    adj_list, edge_list, history = generate_erdos_renyi_gnp(20, 0)
    assert edge_list == []


def test_er_p_1_is_complete():
    n = 20
    adj_list, edge_list, history = generate_erdos_renyi_gnp(n, 1)
    assert len(edge_list) == n * (n - 1) // 2
    for node in adj_list:
        assert len(adj_list[node]) == n - 1 # connected to everyone else


# SECONDARY

def test_ba_bad_m_or_n_raises():
    for n, m in [(10, 0), (2, 2), (3, 5)]: # m < 1, n == m, n < m
        try:
            generate_ba(n, m)
            assert False, "should have raised ValueError"
        except ValueError:
            pass


def test_ba_every_node_has_degree_at_least_m():
    random.seed(5)
    n, m = 100, 3
    adj_list, edge_list, history = generate_ba(n, m)
    for node in adj_list:
        assert len(adj_list[node]) >= m


def test_er_and_ba_are_simple_graphs():
    random.seed(5)
    adj_list, edge_list, history = generate_erdos_renyi_gnp(100, 0.05)
    check_graph(100, adj_list, edge_list)

    adj_list, edge_list, history = generate_ba(100, 2)
    check_graph(100, adj_list, edge_list)
