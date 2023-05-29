def Vias_calc(results_x , results_y ):

    Vias_coord_notSorted = []
    for i in results_x:
        for j in results_y:
            if i[2] == j[2]:
                    Vias_coord_notSorted.append((i[0], j[0], i[1]))
                    Vias_coord_notSorted.append((i[0], j[0], j[1]))
    Vias_coord_notSorted = list(set(Vias_coord_notSorted))
    
    Vias_coord = sorted(Vias_coord_notSorted, key=lambda node: (node[2], node[0] ,node[1]))

    node_idx = {}
    for i, node in enumerate(Vias_coord):
        node_idx[node] = i+1

    # Reassign node indices based on the sorted order

    Vias_connected=[]
    for idx1 ,node1 in enumerate(Vias_coord):
        for idx2 ,node2 in enumerate(Vias_coord):
            if node1[0]==node2[0] and node1[1]==node2[1] and node1[2]+1==node2[2]:
                Vias_connected.append((idx1+1,idx2+1))

    return Vias_coord , node_idx , Vias_connected