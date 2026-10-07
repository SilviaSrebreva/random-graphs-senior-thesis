def get_degrees(adj_list):
    return [len(neighbours) for neighbours in adj_list.values()]

def molloy_reed_criterion(degrees):
    # Molloy-Reed criterion
    # a random graph with a given degree distribution
    # has a giant component(with high probability) iff
    # <k^2> - 2<k> > 0,   equivalently   kappa = <k^2> / <k> > 2
    # where <x> means the average of x over all nodes

    # IMPORTANT: This criterion is proven for graphs where only the
    # degree sequence is fixed and edges are random.
    # It is theoretically valid for ER graphs.
    # For BA graphs, kappa should be reported as a descriptive
    # statistic only, not interpreted as a threshold test.

    n = len(degrees)
    if n == 0:
        raise ValueError("degree sequence is empty")

    mean_k = sum(degrees) / n
    mean_k2 = sum(k * k for k in degrees) / n

    if mean_k == 0:
        return {"mean_k": 0, "mean_k2": 0, "kappa": 0, "giant_component": False}

    kappa = mean_k2 / mean_k
    return {
        "mean_k": mean_k,
        "mean_k2": mean_k2,
        "kappa": kappa,
        "giant_component": kappa > 2
    }
    # we use a dictionary to return multiple values, 
    # so that we can access them by name instead of by index

#might add giant_componnet_size function as well 