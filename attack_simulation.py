import os
import copy
import random

from graph_io import load_graph_txt, adjacency_list_to_edge_list
from max_heap import MaxHeap
from union_find import UnionFind

# we remove nodes one by one and watch how the giant component shrinks
# "targeted" - always remove the node with the highest degree (an attack on the hubs)
# "random" - remove a random node

def simulate_attack(adj_list, n, strategy):
    # copy the graph so removing nodes doesn't change the original adj_list
    # deepcopy also copies the sets inside, a normal copy would share them
    working_adj = copy.deepcopy(adj_list)

    heap = MaxHeap()
    heap.build(working_adj)
    uf = UnionFind(n)
    results = []
    removed = 0

    while working_adj: # an empty dict counts as False, so this stops when no nodes are left

        # pick the node to remove
        if strategy == "targeted":
            node, degree = heap.extract_max()
        else:
            node = random.choice(list(working_adj.keys()))
            # the heap is only used to find the highest degree node,
            # so in the random strategy we don't need to update it

        # remove the node and all its edges
        for neighbour in working_adj[node]:
            working_adj[neighbour].remove(node)
            if strategy == "targeted":
                heap.update_key(neighbour, -1) # neighbour lost one edge

        del working_adj[node]
        removed = removed + 1 

        # find the size of the giant component in what is left
        surviving_edges = adjacency_list_to_edge_list(working_adj) # this is for easier readibility of the code
        
        giant = uf.rebuild(n, surviving_edges)
        if not working_adj:
            giant = 0 # every node is removed, otherwise a removed node would count as size 1

        fraction_removed = removed / n
        results.append((fraction_removed, giant / n))

        # stop once the giant component is basically gone (less than 1% of the nodes)
        if giant < 0.01 * n:
            break

    return results


def save_results_csv(results, filepath):
    # will use in plotting
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True) # same as in graph_io
    with open(filepath, "w") as f:
        f.write("fraction_removed,giant_component\n")
        for x, y in results:
            f.write(f"{x},{y}\n")


if __name__ == "__main__":
    # load_graph_txt returns n, graph_type, edge_list, adj_list
    n_er, er_type, er_edges, er_adj = load_graph_txt("data/er_graph.edgelist")
    n_ba, ba_type, ba_edges, ba_adj = load_graph_txt("data/ba_graph.edgelist")

    er_targeted = simulate_attack(er_adj, n_er, "targeted")
    er_random = simulate_attack(er_adj, n_er, "random")
    ba_targeted = simulate_attack(ba_adj, n_ba, "targeted")
    ba_random = simulate_attack(ba_adj, n_ba, "random")

    all_results = [
        ("er_targeted", er_targeted),
        ("er_random", er_random),
        ("ba_targeted", ba_targeted),
        ("ba_random", ba_random),
    ]

    for name, results in all_results:
        save_results_csv(results, f"results/{name}.csv")
        print("saved", name, "-", len(results), "nodes removed")
