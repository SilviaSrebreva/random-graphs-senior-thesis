from biased_coin import biased_coin_flip

def generate_erdos_renyi_gnp(n, p):
    adj_list = {i: [] for i in range(n)} 
    #dictionary comprehension, the key is 1 to n-1, the value is a list of djacent nodes(empty in the beginning)
    edge_list = [] #list of edges, each edge is a tuple of two nodes

    for i in range(n):
        for j in range(i + 1, n):
            if biased_coin_flip(p): 
                #if the biased coin flip returns True, add an edge between i and j
                adj_list[i].append(j) 
                adj_list[j].append(i) 
                edge_list.append((i, j))

    return adj_list, edge_list

if __name__ == "__main__":
    n = 3
    p = 0.3
    edge_list, adj_list = generate_erdos_renyi_gnp(n, p)
    print("Adjacency List:", adj_list)
    print("Edge List:", edge_list)
