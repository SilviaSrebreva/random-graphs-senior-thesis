from union_find import UnionFind


# PRIMARY

def test_largest_component():
    # two components {0, 1, 2} and {3, 4}, and node 5 on its own
    uf = UnionFind(6)
    assert uf.rebuild(6, [(0, 1), (1, 2), (3, 4)]) == 3


def test_connected_and_not_connected():
    uf = UnionFind(6)
    uf.rebuild(6, [(0, 1), (1, 2), (3, 4)])
    assert uf.find(0) == uf.find(2) # same component
    assert uf.find(0) != uf.find(3) # different components
    assert uf.find(5) == 5          # node 5 is alone, so it is its own root


def test_empty_graph():
    # no nodes at all
    uf = UnionFind(0)
    assert uf.rebuild(0, []) == 0


# SECONDARY

def test_no_edges():
    # every node is on its own, so the largest component is 1
    uf = UnionFind(5)
    assert uf.rebuild(5, []) == 1
