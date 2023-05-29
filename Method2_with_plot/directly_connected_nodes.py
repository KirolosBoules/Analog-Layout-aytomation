import numpy as np

def directly_connected_nodes(wires,Vias_coord,Wire_Widths,node_idx):
    directly_connected = []
    width_bet_nodes2=[]
    width_bet_nodes=np.array([])
    wire_idx=0
    for wire_idx,wire in enumerate(wires):
        wire_nodes = []
        for node in Vias_coord:
            x, y ,z= node
            if z==wire[2]:
                layer=wire[2]
            # print('layer=',layer1,'wire_idx=',wire_idx)
                if wire[0][0] <= x <= wire[1][0] and wire[0][1] <= y <= wire[1][1]:
                # Calculate the distance and corresponding width
                    width = Wire_Widths[wire_idx]
                    distance = np.sqrt((node[0]-wire[0][0])**2 + (node[1]-wire[0][1])**2)
                    wire_nodes.append((node_idx[node], distance, width))

        wire_nodes.sort(key=lambda x: x[1])
        n = len(wire_nodes)
        if n > 1:
            selected_nodes = [wire_nodes[i][0] for i in range(n)]
            for i in range(n-1):
                # Add the corresponding width to the directly connected nodes
                width = min(wire_nodes[i][2], wire_nodes[i+1][2])
                width_bet_nodes=np.append(width_bet_nodes,width)
                width_bet_nodes2.append((selected_nodes[i], selected_nodes[i+1],width))
                directly_connected.append((selected_nodes[i], selected_nodes[i+1]))

    return width_bet_nodes , width_bet_nodes2 ,directly_connected
                
    #******************