from biased_coin import biased_coin_flip

def generate_erdos_renyi_gnp(n, p):
    adj_list = {i: set() for i in range(n)} 
    #dictionary comprehension, the key is 1 to n-1, the value is a list of djacent nodes(empty in the beginning)
    edge_list = [] #list of edges, each edge is a tuple of two nodes

    history = [] #used for visualisation

    for i in range(n):
        new_edges = [] #stores the edges created during this step
        for j in range(i + 1, n):
            if biased_coin_flip(p): 
                # if the biased coin flip returns True, add an edge between i and j
                adj_list[i].add(j) 
                adj_list[j].add(i) 
                edge_list.append((i, j))
                new_edges.append((i, j))
        history.append({"node": i, "edges": new_edges})

    return adj_list, edge_list, history

def graph_info(n: int, edge_list: list, adj_list: dict):
    m = len(edge_list)  # number of edges
    degrees = [len(adj_list[i]) for i in range(n)]  # degree of each node
    return {
        "n": n,
        "m": m,
        "degrees": degrees,
        "avg_degree": sum(degrees) / n if n > 0 else 0,
        "min_degree": min(degrees) if degrees else 0,
        "max_degree": max(degrees) if degrees else 0
    }

if __name__ == "__main__":
    n = 3
    p = 0.3
    adj_list,  edge_list, history  = generate_erdos_renyi_gnp(n, p)
    print("Adjacency List:", adj_list)
    print("Edge List:", edge_list)
    print("Graph Info:", graph_info(n, edge_list, adj_list))
