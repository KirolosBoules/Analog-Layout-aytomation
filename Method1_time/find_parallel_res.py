import math

def find_parallel_res(signed_currents, node, i_total):
    parallel_resistances = set()
    rail_currents = []

    for num in signed_currents:
        rail_currents.append((num[0], num[1], round(abs(num[2]), 2)))
    print('positive rail currents ', rail_currents)
    
    for i, tup in enumerate(rail_currents):
        if tup[:2] == node or tup[:2] == (node[1], node[0]):
            node_idx = i
    
    for i in range(len(rail_currents)):
        a = rail_currents[i][2] + rail_currents[node_idx][2]
        for j in range(len(rail_currents)):
            b = rail_currents[j][2]
            if any(math.isclose(a, x, rel_tol=0.05) for x in [b]) or any(math.isclose(a, x, rel_tol=0.05) for x in [i_total]):
                parallel_resistances.add(rail_currents[i])

    parallel_resistances = list(parallel_resistances)
    print('parallel resistance', parallel_resistances)
    return parallel_resistances