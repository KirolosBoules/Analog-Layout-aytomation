paths=[(1, 2, 3, 16, 21, 26, 13), (1, 14, 19, 24, 11, 12, 13), (1, 2, 15, 20, 25, 12, 13)]

nodes = set()
parallel_nodes = set()
for path in paths:
    for node in path:
        if node in nodes:
            parallel_nodes.add(node)
        else:
            nodes.add(node)

for node in parallel_nodes:
    parallel_paths = []
    for path in paths:
        if node in path:
            parallel_paths.append(path)
    if len(parallel_paths) > 1:
        print(f"Node {node} appears in parallel paths:")
        index = parallel_paths[0].index(node)
        parallel_sections = []
        for path in parallel_paths:
            parallel_sections.append(path[index:])
        for i, section in enumerate(parallel_sections):
            print(f"Path {i+1}: {section}")
'''
Node 1 appears in parallel paths:
Node 2 appears in parallel paths:
(1,2)

Node 2 appears in parallel paths:

Path 1: (2, 3, 16, 21, 26, 13)
Path 2: (2, 15, 20, 25, 12, 13)
Node 12 appears in parallel paths:
Path 1: (12, 13)
Path 2: (12, 13)
'''