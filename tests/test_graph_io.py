from graph_io import (
    Node, Edge,
    save_graph_txt, load_graph_txt,
    save_graph_json, load_graph_json,
)

# tmp_path is a temporary folder that pytest gives,
# so the tests never touch data/ or results/


# PRIMARY

def test_txt_save_then_load(tmp_path):
    edge_list = [(0, 1), (1, 2), (2, 3)]
    filepath = str(tmp_path / "graph.edgelist")

    save_graph_txt(edge_list, 5, "er", filepath)
    n, graph_type, loaded_edges, adj_list = load_graph_txt(filepath)

    assert n == 5
    assert graph_type == "er"
    assert loaded_edges == edge_list
    assert adj_list[1] == {0, 2}
    assert adj_list[4] == set() # node 4 has no edges but is still in the graph


def test_json_save_then_load_with_states(tmp_path):
    edges = [Edge(0, 1), Edge(1, 2)]
    nodes = [Node(0, "S"), Node(1, "I"), Node(2, "R")]
    filepath = str(tmp_path / "graph.json")

    save_graph_json(edges, nodes, 3, "ba", filepath)
    n, graph_type, loaded_nodes, edge_objs, edge_list, adj_list = load_graph_json(filepath)

    assert n == 3
    assert graph_type == "ba"
    assert edge_list == [(0, 1), (1, 2)]
    assert [node.state for node in loaded_nodes] == ["S", "I", "R"]
    assert adj_list[1] == {0, 2}


# SECONDARY

def test_load_missing_txt_raises(tmp_path):
    try:
        load_graph_txt(str(tmp_path / "does_not_exist.edgelist"))
        assert False, "should have raised FileNotFoundError"
    except FileNotFoundError:
        pass


def test_load_missing_json_raises(tmp_path):
    try:
        load_graph_json(str(tmp_path / "does_not_exist.json"))
        assert False, "should have raised FileNotFoundError"
    except FileNotFoundError:
        pass


def test_txt_header_without_n_raises(tmp_path):
    filepath = tmp_path / "bad.edgelist"
    filepath.write_text("# graph_type=er\n0 1\n") # header has no n=
    try:
        load_graph_txt(str(filepath))
        assert False, "should have raised ValueError"
    except ValueError:
        pass
