paths = [(1, 2, 3, 16, 13), (1, 14, 19, 24, 13), (1, 2, 15, 12, 13)]

# Identify the series nodes
series_nodes = set(paths[0]).intersection(*paths)

# Group the paths based on series nodes
groups = {}
for path in paths:
    series_node = next((node for node in path if node in series_nodes), None)
    if series_node not in groups:
        groups[series_node] = []
    groups[series_node].append(path)

# Extract the parallel paths for each group
parallel_paths = []
for group in groups.values():
    parallel_nodes = set(group[0]).intersection(*group)
    parallel_paths.append([(node,) + tuple(p[parallel_nodes.index(node)+1:] for p in group) for node in parallel_nodes])

# Combine the series and parallel paths
result = [(tuple(series_nodes), parallel_paths), tuple(path for path in paths if path not in sum(parallel_paths, []))]

print(result)


#paths = [(1, 2, 3, 4,5,13), (1, 6,3,4,9,13), (1, 10,11,12, 13)]

#result =reallocate_paths (paths)
