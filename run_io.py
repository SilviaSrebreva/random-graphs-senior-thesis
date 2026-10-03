from ER_generator import generate_erdos_renyi_gnp
from BA_generator import generate_ba
from graph_io import save_graph_txt, save_graph_json, load_graph_txt, load_graph_json

# generate small graphs
n = 10
er_adj , er_edges, er_history = generate_erdos_renyi_gnp(n, 0.4)
ba_adj, ba_edges, ba_history = generate_ba(n, 2)

# save in both formats
save_graph_txt(er_edges, n, "er", "data/er_graph.edgelist")
save_graph_txt(ba_edges, n, "ba", "data/ba_graph.edgelist")
save_graph_json(er_edges, n, "er", "data/er_graph.json")
save_graph_json(ba_edges, n, "ba", "data/ba_graph.json")

# reload and check if txt and json are the same
n, gtype, edges, adj = load_graph_txt("data/er_graph.edgelist")
print("ER txt loaded: n={}, type={}, edges={}".format(n, gtype, edges))

n, gtype, edges, adj = load_graph_json("data/er_graph.json")
print("ER json loaded: n={}, type={}, edges={}".format(n, gtype, edges))