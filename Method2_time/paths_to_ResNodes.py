def paths_to_ResNodes (all_res_nodes , paths):
    NODE=[]
    rev_NODE=[]
    all_res_nodes_dict = {k: v for k, v in all_res_nodes}
    circuit_set = set()
    for path in paths:
        for i in range(len(path)-1):
            node = (path[i], path[i+1])
            rev_node = (path[i+1], path[i])
            if node in all_res_nodes_dict or rev_node in all_res_nodes_dict:
                circuit_set.add((node, all_res_nodes_dict.get(node, all_res_nodes_dict.get(rev_node))))
            NODE.append(node)
            rev_NODE.append(rev_node)
    circuit = list(circuit_set)

    return circuit , NODE , rev_NODE





