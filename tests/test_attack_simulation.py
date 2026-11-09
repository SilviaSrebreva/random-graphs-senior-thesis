import copy
import random

from attack_simulation import simulate_attack
from ER_generator import generate_erdos_renyi_gnp


def make_graph():
    # a small ER graph with average degree about 4, same seed every time
    random.seed(7)
    n = 200
    adj_list, edge_list, history = generate_erdos_renyi_gnp(n, 4 / (n - 1))
    return n, adj_list


# PRIMARY

def test_original_graph_unchanged():
    n, adj_list = make_graph()
    before = copy.deepcopy(adj_list)

    simulate_attack(adj_list, n, "targeted")
    simulate_attack(adj_list, n, "random")

    assert adj_list == before


def test_stops_at_1_percent_cutoff():
    n, adj_list = make_graph()
    for strategy in ["targeted", "random"]:
        results = simulate_attack(adj_list, n, strategy)
        # results stores touples (fraction_removed, giant_component)
        # the last row is the first one below 1%
        assert results[-1][1] < 0.01 # takes the second value in the last tuple
        # every row before it is still 1% or more
        for x, y in results[:-1]: # a slice meaning "everything from the start up to, but not including, the last item"
            assert y >= 0.01


# SECONDARY

def test_x_goes_up_by_1_over_n_and_giant_never_grows():
    n, adj_list = make_graph()
    for strategy in ["targeted", "random"]:
        results = simulate_attack(adj_list, n, strategy)

        for i in range(len(results)):
            x, y = results[i]
            assert abs(x - (i + 1) / n) < 1e-9 # one more node removed every row
            if i > 0:
                assert y <= results[i - 1][1] # removing nodes can't make the giant bigger
