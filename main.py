import os
import random
import webbrowser

from ER_generator import generate_erdos_renyi_gnp
from BA_generator import generate_ba
from graph_io import save_graph_txt, save_graph_json, load_graph_txt, Node, Edge
from molloy_reed import get_degrees, molloy_reed_criterion, critical_fraction
from attack_simulation import simulate_attack, save_results_csv
from SIR import run_sir, save_sir_csv
from plotting import plot_robustness, plot_sir
from ER_graph_visualiser import visualise_er
from BA_graph_visualiser import visualise_ba

# parameters
SEED = 42 # seems to be a convention to use 42, i read spomething about The Hitchhiker’s Guide to the Galaxy lol
n = 1000 # not too big, runs quckly
m = 2 # BA: edges each new node brings
p = 2 * m / (n - 1) # ER: chosen so both graphs have the same average degree (2m)
beta = 0.05 # SIR: chance to infect a neighbour in one step
gamma = 0.1 # SIR: chance to recover in one step
max_steps = 200 # SIR: stop after this many steps

# we go Generation(optional) -> Load -> Molloy-Reed
#  -> Attack Simulation -> SIR -> Plotting


random.seed(SEED)

# GENERATION - only if the graph files don't exist yet
print("Step 1: Graphs")
if not os.path.exists("data/er_graph.edgelist"):
    print("    generating ER graph")
    er_adj, er_edges, er_history = generate_erdos_renyi_gnp(n, p)
    save_graph_txt(er_edges, n, "er", "data/er_graph.edgelist")
    save_graph_json([Edge(u, v) for u, v in er_edges], [Node(i) for i in range(n)], n, "er", "data/er_graph.json")
else:
    print("    ER graph already exists, not generating it again")

if not os.path.exists("data/ba_graph.edgelist"):
    print("    generating BA graph")
    ba_adj, ba_edges, ba_history = generate_ba(n, m)
    save_graph_txt(ba_edges, n, "ba", "data/ba_graph.edgelist")
    save_graph_json([Edge(u, v) for u, v in ba_edges], [Node(i) for i in range(n)], n, "ba", "data/ba_graph.json")
else:
    print("    BA graph already exists, not generating it again")

# LOAD - always work on the saved graphs
print("Step 2: Loading graphs from data/er_graph.edgelist and data/ba_graph.edgelist")
n_er, er_type, er_edges, er_adj = load_graph_txt("data/er_graph.edgelist")
n_ba, ba_type, ba_edges, ba_adj = load_graph_txt("data/ba_graph.edgelist")

# seed again, so the simulations below get the same random numbers
# no matter if the graphs were generated in this run
random.seed(SEED)

# MOLLOY-REED
# get_degrees() turns the graph into a list with each node's number of neighbours
# molloy_reed_criterion() calculates kappa and if the giant component exists
# critical_fraction() calculates the critical fraction of nodes that need to be removed to destroy the giant component
# all of this will be used in plotting
print("Step 3: Molloy-Reed")
er_mr = molloy_reed_criterion(get_degrees(er_adj))
ba_mr = molloy_reed_criterion(get_degrees(ba_adj))
er_fc = critical_fraction(er_mr["kappa"])
ba_fc = critical_fraction(ba_mr["kappa"])
print("ER: kappa =", er_mr["kappa"], "giant component:", er_mr["giant_component"], "f_c =", er_fc)
print("BA: kappa =", ba_mr["kappa"], "giant component:", ba_mr["giant_component"], "f_c =", ba_fc)

# ATTACK SIMULATION - works on a copy, so er_adj and ba_adj stay the same
print("Step 4: Attack simulation (targeted and random)")
save_results_csv(simulate_attack(er_adj, n_er, "targeted"), "results/er_targeted.csv")
save_results_csv(simulate_attack(er_adj, n_er, "random"), "results/er_random.csv")
save_results_csv(simulate_attack(ba_adj, n_ba, "targeted"), "results/ba_targeted.csv")
save_results_csv(simulate_attack(ba_adj, n_ba, "random"), "results/ba_random.csv")

# SIR - start from a random node, so a BA hub isn't picked on purpose
print("Step 5: SIR")
# in the future maybe have multiple nodes infected at the start,
# or a random fraction of nodes, but for now this is the basis
er_start = [random.choice(list(er_adj.keys()))] # one random node is infected at the start
ba_start = [random.choice(list(ba_adj.keys()))] # in a list, because run_sir expects a list

er_results, er_states = run_sir(er_adj, beta, gamma, er_start, max_steps)
ba_results, ba_states = run_sir(ba_adj, beta, gamma, ba_start, max_steps)

save_sir_csv(er_results, "results/er_sir.csv")
save_sir_csv(ba_results, "results/ba_sir.csv")

# SAVE the graph together with the final state of every node (not over the original files)
# json format is used so the node states can be stored as well
er_nodes = [Node(i, er_states[i]) for i in range(n_er)]
ba_nodes = [Node(i, ba_states[i]) for i in range(n_ba)]
save_graph_json([Edge(u, v) for u, v in er_edges], er_nodes, n_er, er_type, "results/er_graph_sir.json")
save_graph_json([Edge(u, v) for u, v in ba_edges], ba_nodes, n_ba, ba_type, "results/ba_graph_sir.json")

# PLOTTING
print("Step 6: Plotting")
plot_robustness(er_fc)
plot_sir()
print("    plots saved in figures/")

# ask if the plots should be opened in the browser
answer = input("Do you want to open the html graphs? Press 1 for yes: ")
if answer.strip() == "1":
    for name in ["robustness", "er_sir", "ba_sir"]:
        webbrowser.open("file://" + os.path.abspath(f"figures/{name}.html"))

# ask if the tkinter visualiser should be opened (small graph, same as running the visualiser files)
answer = input("Do you want to see the tkinter visualiser? 1 for ER, 2 for BA, anything else for no: ")
if answer.strip() == "1":
    visualise_er(10, 0.3)
elif answer.strip() == "2":
    visualise_ba(10, 2)
