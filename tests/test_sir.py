import copy
import random

from SIR import run_sir
from BA_generator import generate_ba


def make_graph():
    random.seed(3)
    adj_list, edge_list, history = generate_ba(200, 2)
    return adj_list


# PRIMARY

def test_beta_0_no_new_infections():
    adj_list = make_graph()
    results, states = run_sir(adj_list, beta=0, gamma=0.1, initial_infected=[0], max_steps=50)

    # only node 0 was ever infected, everyone else is still S
    for node in adj_list:
        if node != 0:
            assert states[node] == "S"
    for row in results:
        assert row["I"] + row["R"] == 1 / 200


def test_gamma_1_everyone_recovers_in_one_step():
    adj_list = make_graph()
    start = [0, 1, 2]
    results, states = run_sir(adj_list, beta=0, gamma=1, initial_infected=start, max_steps=50)

    assert results[1]["I"] == 0     # after one step nobody is infected
    assert results[1]["R"] == 3 / 200
    for node in start:
        assert states[node] == "R"


# SECONDARY

def test_no_initial_infected_single_row():
    adj_list = make_graph()
    results, states = run_sir(adj_list, beta=0.5, gamma=0.1, initial_infected=[], max_steps=50)

    assert len(results) == 1 # only step 0
    assert results[0]["S"] == 1


def test_sir_rules():
    adj_list = make_graph()
    max_steps = 200
    results, states = run_sir(adj_list, beta=0.1, gamma=0.1, initial_infected=[0], max_steps=max_steps)

    for i in range(len(results)):
        row = results[i]
        assert abs(row["S"] + row["I"] + row["R"] - 1) < 1e-9 # compare to 1 with some tolerance for floating point errors 
        if i > 0:
            assert row["S"] <= results[i - 1]["S"] # S never rises
            assert row["R"] >= results[i - 1]["R"] # R never falls

    # if the run ended early, it is because nobody was infected anymore
    if len(results) < max_steps + 1:
        assert "I" not in states.values()


def test_sir_original_graph_unchanged():
    adj_list = make_graph()
    before = copy.deepcopy(adj_list)
    run_sir(adj_list, beta=0.1, gamma=0.1, initial_infected=[0], max_steps=50)
    assert adj_list == before
