import os

def save_graph_txt(
    edge_list: list[tuple],
    n: int,
    graph_type: str,
    filepath: str,
):
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True) #making directory 
    # if it doesn't exist os.path.dirname(filepath): Extracts the folder path from the destination filename
    # or ".": If the folder path is empty (i.e., the file is in the current directory), use "." to represent the current directory.
    # exist_ok=True : If the directory already exists, don't raise an error; just continue.

    with open(filepath, "w") as f:
        # Header line carries all data needed for reconstruction.
        f.write(f"# graph_type={graph_type} n={n} m={len(edge_list)}\n")
        for u, v in edge_list:
            f.write(f"{u} {v}\n")

    print(f"  Saved {graph_type.upper()} graph: {len(edge_list)} edges ; in {filepath}")

def _header_str(line: str, key: str):
    # extract a string value for 'key=VALUE' from a line, or None
    for token in line.split():
        if token.startswith(f"{key}="):
            return token.split("=", 1)[1]
    return None

def _header_value(line: str, key: str):
    # extract an integer value for 'key=VALUE' from a line, or None
    for token in line.split():
        if token.startswith(f"{key}="):
            try:
                return int(token.split("=", 1)[1])
            except ValueError:
                return None
    return None


def _parse_header(line: str) -> tuple[int, str]:
    # extract n and graph_type from a header comment line
    n = _header_value(line, "n")
    graph_type = _header_str(line, "graph_type")
    if n is None:
        raise ValueError(f"Could not parse 'n' from header: {line!r}")
    return n, graph_type or "unknown"

def _build_adjacency_list(n: int, edge_list: list[tuple]) -> dict:
   # build an adjacency list from the edge list
   # every node is visited, even unocnnected ones

    adj_list = {i: set() for i in range(n)}
    for u, v in edge_list:
        adj_list[u].add(v)
        adj_list[v].add(u)
    return adj_list

def load_graph_txt(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Graph file not found: {filepath}")

    edge_list = []
    n = None
    graph_type = "unknown"

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                # Parse header: # graph_type=er n=500 m=2481
                n, graph_type = _parse_header(line)
            else:
                u, v = map(int, line.split())
                edge_list.append((u, v))

    if n is None:
        raise ValueError(f"Graph file missing header with 'n': {filepath}")
    adj_list = _build_adjacency_list(n, edge_list)
    return n, graph_type, edge_list, adj_list

def adjacency_list_to_edge_list(adj_list: dict) -> list[tuple]:
    
    # convert an adjacency list back to a deduplicated edge list.
    # might be useful in simulation?
    edges = set()
    for u, neighbours in adj_list.items():
        for v in neighbours:
            edges.add((min(u, v), max(u, v)))
    return sorted(edges)

