import random 

def generate_ba(n,m):
    #n - total number of nodes, 
    # m - edges with which each node contributes

    # will think of how to make the graph reproducable 
    # so that i an use it later on when comparing, for now just 
    # working on the BA generation textbook-wise
    if m < 1:
        raise ValueError("m must be >= 1, got {}".format(m))
    #each node should have at least one connection
    if n <= m:
        raise ValueError("n must be greater than m, got n={} m={}".format(n, m))

    m0 = m + 1
    #m0 is a requirement for the graph algorithm to work mathematically
    #thanks to m0 we guarantee there are at east m nodes for the new node to attach to
    #each node in the start seed graph has degree m>0, this it is nonempty, again mathematical requirement
    edge_list = []
    adj_list = {i: set() for i in range(n)}

    history = [] #used for visualisation
    original_edges = []



    for i in range(m0):
        for j in range(i + 1, m0):
            edge_list.append((i, j))
            original_edges.append((i, j))
            adj_list[i].add(j)
            adj_list[j].add(i)

    history.append({"node": None, "edges": original_edges})

    # we make a list T that will store the edges as many times as their degree is
    # this way with just appending to this list T we can then check degree easily 

    T = []
    for i in range(m0):
        degree_i = len(adj_list[i])
        for count in range(degree_i):
            T.append(i)

   

    # i need to do preferentaial attachment next

    #preferential attachment follows
    for new_node in range(m0, n):
        chosen = set() #set has no duplicates, item in set can be found easily
        while len(chosen) < m:
            i = random.randrange(len(T))
            candidate = T[i]
            if candidate not in chosen:
                chosen.add(candidate)

        new_edges = []
        for element in chosen:
            u = min(element, new_node)
            v = max(element, new_node)
            #we check min max to keep consistency of how we add edges, 
            # thus we avoid storing two edges that are technicaly the same
            edge_list.append((u, v))
            new_edges.append((u, v))

            adj_list[element].add(new_node)
            adj_list[new_node].add(element)

            T.append(new_node)
            T.append(element)
                        
        history.append({"node": new_node, "edges": new_edges})

    return adj_list, edge_list, history

if __name__ == "__main__":
    n = 10
    m = 2
    adj_list,  edge_list, history = generate_ba(n, m)
    print("Adjacency List:", adj_list)
    print("Edge List:", edge_list)
    #print("Graph Info:", graph_info(n, edge_list, adj_list))
