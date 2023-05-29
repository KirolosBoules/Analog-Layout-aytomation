def find_all_paths(start, end, edges):
    paths = []
    visited = set()
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node == end:
            paths.append(path)
        elif node not in visited:
            visited.add(node)
            for edge in edges:
                if node in edge:
                    next_node = edge[1] if edge[0] == node else edge[0]
                    new_path = list(path)
                    new_path.append(next_node)
                    queue.append(new_path)
    return paths

def find_all_paths_bidirectional(start, end, edges):
    forward_paths = find_all_paths(start, end, edges)
    reversed_edges = [(edge[1], edge[0]) for edge in edges]
    reversed_paths = find_all_paths(end, start, reversed_edges)
    return forward_paths + [path[::-1] for path in reversed_paths]
