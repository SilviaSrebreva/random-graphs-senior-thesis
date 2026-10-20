def get_degrees(adj_list):
    return [len(neighbours) for neighbours in adj_list.values()]

def molloy_reed_criterion(degrees):
    # Molloy-Reed criterion
    # a random graph with a given degree distribution
    # has a giant component(with high probability) iff
    # <k^2> - 2<k> > 0, equivalently kappa = <k^2> / <k> > 2

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

def critical_fraction(kappa):
    # fraction of nodes we can remove at random before the giant component disappears
    # f_c = 1 - 1 / (kappa - 1), (Cohen et al. 2000)
    if kappa <= 2:
        return 0 # there is no giant component to begin with
    return 1 - 1 / (kappa - 1)

# might add giant_componnet_size function as well - done in union_find.py in rebuild method