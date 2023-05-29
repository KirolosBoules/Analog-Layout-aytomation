import matplotlib.pyplot as plt
from shapely.geometry import LineString
import numpy as np
import networkx as nx
import math as math
# Functions #
from generate_wires import generate_wires
from calc_Via_rects import calc_Via_rects
from find_all_paths import find_all_paths_bidirectional
from calc_minimum_rect_area import calc_minimum_rect_area


#wire_height = grid_y2 - grid_y1
# get the number of layers from the user
num_layers = int(input("Enter the number of layers: "))
# create wires for each layer
grid_start = (0, 0)
grid_end = (20,20)
wire_width=3
spacing=1
grid_x1, grid_y1 = grid_start
grid_x2, grid_y2 = grid_end

wires=generate_wires(num_layers,wire_width,spacing,grid_start,grid_end)
print(wires)
Wire_Widths=np.array([])
results_x = np.array([])
results_y = np.array([])
fig, ax = plt.subplots()



# Calculate Wire Width annd plot them
for wire in wires:
    x1, y1 = wire[0]
    x2, y2 = wire[1]
    layer = wire[2]
    voltage = wire[3]
    if layer % 2 != 0:
        width = abs(x2 - x1)
        Center_x = (x1 + x2) / 2
        results_x = np.append(results_x, (Center_x, layer, voltage))
        results_x = np.reshape(results_x, (-1, 3))
        results_x = list(map(tuple, results_x))
    else:
        width = abs(y2 - y1)
        Center_y = (y1 + y2) / 2
        results_y = np.append(results_y, (Center_y, layer, voltage))
        results_y = np.reshape(results_y, (-1, 3))
        results_y = list(map(tuple, results_y))
    Wire_Widths=np.append(Wire_Widths,width)  # append width to the list for the corresponding layer
    #WireWidth = np.concatenate(WireWidth, axis=0).reshape(num_layers,-1)  # concatenate along columns and reshape to 2D array
    if voltage == 1:
        ax.add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='r', facecolor='red'))
    else:
        ax.add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='b', facecolor='blue'))

#**************************************************#

Vias_coord = []
for i in results_x:
     for j in results_y:
        if i[2] == j[2]:
                Vias_coord.append((i[0], j[0], i[1]))
                Vias_coord.append((i[0], j[0], j[1]))
Vias_coord = list(set(Vias_coord))


node_idx = {}
for i, node in enumerate(Vias_coord):
    node_idx[node] = i+1

Vias_connected=[]
for idx1 ,node1 in enumerate(Vias_coord):
    for idx2 ,node2 in enumerate(Vias_coord):
        if node1[0]==node2[0] and node1[1]==node2[1] and node1[2]+1==node2[2]:
            Vias_connected.append((idx1+1,idx2+1))
Number_of_Vias=[]
Via_centers=[]
for Via in Vias_connected :
    x1,y1,z1=Vias_coord[Via[0]-1]
    x2,y2,z2=Vias_coord[Via[1]-1]
    wire_idx = 0
    for wire_idx , wire in enumerate(wires):
        if wire[0][0] <= x1 <= wire[1][0] and wire[0][1] <= y1 <= wire[1][1] and z1==wire[2]:
            # Calculate the corresponding width
                width1 = Wire_Widths[wire_idx]
        if wire[0][0] <= x2 <= wire[1][0] and wire[0][1] <= y2 <= wire[1][1] and z2==wire[2]:
            # Calculate the corresponding width
                width2 = Wire_Widths[wire_idx]

    num_vias , Via_center =calc_Via_rects(width1,width2,(x1,y1),1,0.25)
    Via_centers.extend(Via_center)
    Number_of_Vias.append(num_vias)


for center in Via_centers:
    x=center[0]
    y=center[1]
    w=h=1 # standard width and height of Via
    ax.add_patch(plt.Rectangle((x - w/2, y - h/2), w, h, linewidth=1, edgecolor='r', facecolor='yellow'))

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
#******************
all_connected_nodes = directly_connected + Vias_connected
num_nodes=len(all_connected_nodes)

Length=np.array([])
for i in range (len(directly_connected)):
    a,b=directly_connected[i]
    x_co1 , y_co1,z=Vias_coord[a-1]
    x_co2 , y_co2,z=Vias_coord[b-1]
    x_co3 = x_co2 - x_co1
    y_co3 = y_co2 - y_co1
    L_res=np.sqrt((x_co3)**2+(y_co3)**2)
    Length=np.append(Length,L_res)
Rsheet=1
R_bet_nodes=Rsheet*Length/width_bet_nodes

defined_Res = list(zip(directly_connected, R_bet_nodes))

#*********************Plotting*************************

plt.xlim(grid_x1, grid_x2)
plt.ylim(grid_y1, grid_y2)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

Res_Vias=[]
#///////////////////IR-Calculation///////////////////////////
for N,via in enumerate (Vias_connected) : 
    Res_Vias.append(((via[0], via[1]), 0.2/Number_of_Vias[N]))

all_res_nodes=Res_Vias+defined_Res


#**************Plotting*******/
G = nx.Graph()
for edge, resistance in all_res_nodes:
    node1, node2 = edge
    G.add_edge(node1, node2, weight=resistance)

# Draw the graph using NetworkX and matplotlib
pos = nx.circular_layout(G)  # Layout the nodes in a circle
nx.draw(G, pos, with_labels=True, node_color='white', node_size=800, font_size=16, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v):f"{w:.1f}" for (u,v,w) in G.edges(data='weight')})
plt.axis('equal')
plt.show()



#/////////////////////////////EM Calculation //////////////

EM_violations = []
for i in range(1, num_nodes + 1):
    for j in range(i + 1, num_nodes + 1):
        paths = find_all_paths_bidirectional(i, j, all_connected_nodes)
        if len(paths) == 0:
            continue
        paths = list(set([tuple(path) for path in paths]))

 # Get user input for i_total and source/destination nodes
i_total = float(input("Enter the total current (in Amperes): "))
source_nodes = input("Enter the source nodes (comma-separated): ")
destination_nodes = input("Enter the destination nodes (comma-separated): ")

# Convert user input to list of integers
source_nodes = [int(x.strip()) for x in source_nodes.split(",")]
destination_nodes = [int(x.strip()) for x in destination_nodes.split(",")]

worst_paths=[]
EM_violations = []
i_worst_MAT=[]
for source_node in source_nodes:
    for destination_node in destination_nodes:
        paths = find_all_paths_bidirectional(source_node, destination_node, all_connected_nodes)
        if len(paths) == 0:
            continue
        paths = list(set([tuple(path) for path in paths]))

        R_one_path = np.zeros([])
        R_path = np.zeros([])
        Path_cond = []
        I_Max = []
        required_widths=[]
        for path in paths:
            resistance = 0
            for k in range(len(path) - 1):
                for l, node2 in enumerate(width_bet_nodes2):
                    if (path[k] == node2[0] and path[k+1] == node2[1]) or (path[k] == node2[1] and path[k+1] == node2[0]):
                        W = node2[2]
                        i_max = 0.9 * (W * 0.9 - 0.002)
                        R = R_bet_nodes[l]
                        resistance += R 
                        I_Max.append((path[k],path[k+1],i_max))
                    # Check if the current width is lower than the required width

                for l, node2 in enumerate(Vias_connected):
                    if (path[k] == node2[0] and path[k+1] == node2[1]) or (path[k] == node2[1] and path[k+1] == node2[0]):
                        numOfVias = Number_of_Vias[l]
                        i_max = 0.04 * numOfVias
                        R = 0.2 / numOfVias  # constant for vias
                        resistance += R 
                        I_Max.append((path[k],path[k+1],i_max))

            Path_cond.append(1 / resistance)
                    

                # calculate total conductance
        G_total = sum(Path_cond)
                
           # calculate current in each path
        I_paths = []
        for i, cond in enumerate (Path_cond):
            I_paths.append(i_total * (cond / G_total))
            V_drop=(I_paths[i]/cond)
            #print('V_drop', V_drop)

        i_worst = max(I_paths) #path holds the max current
        i_worst_index = I_paths.index(i_worst)
        i_worst_MAT.append(i_worst)

        # calculatin EM violation for all paths 
        for k, path in enumerate(paths):
            for l in range(len(path) - 1):
                for node2 in I_Max:
                    if (path[l] == node2[0] and path[l+1] == node2[1]) or (path[l] == node2[1] and path[l+1] == node2[0]):
                        if I_paths[k] >= node2[2]:
                            EM_violations.append((path[l], path[l+1], I_paths[k], node2[2]))
                          
            
        worst_paths.append(paths[i_worst_index])
        

print ("worst Paths",worst_paths)
print ("worst_current",i_worst_MAT)


rail_currents = []
for n, path in enumerate (worst_paths):
    for i in range(len(path)-1):
        rail_currents.append((path[i], path[i+1], i_worst_MAT[n])) # write in that form (node1 , node2 , scurrent)

rail_sum_currents = {}


for item in rail_currents:
    if (item[0], item[1]) in rail_sum_currents:
        rail_sum_currents[(item[0], item[1])] += item[2]
    else:
        rail_sum_currents[(item[0], item[1])] = item[2]

rail_sum_currents = [(k[0], k[1], v) for k, v in rail_sum_currents.items()] #write in that form (node1 , node2 ,sum of all currents that will path)




# calculatin EM violation for all paths
new_widthsV=np.zeros(len(wires)) 
for  node in (rail_sum_currents): 
        for node2 in I_Max:
            if (node[0] == node2[0] and node[1] == node2[1]) or (node[0] == node2[1] and node[1] == node2[0]) :
                if node[2] >= node2[2]: # if i > imax
                    print ("EM Violation between ",node[0],"and ",node[1],"With current :",node[2] ,"exceeding the max: ",node2[2])
                    for idx,via in enumerate (Vias_connected) : 
                        if  (node[0] == via[0] and node[1] == via[1]):
                            numOFvia_required=node[2]/0.04
                            width,h=calc_minimum_rect_area(numOFvia_required,1,0.25)
                            x1=Vias_coord[node[0]-1][0]
                            y1=Vias_coord[node[0]-1][1]
                            z1=Vias_coord[node[0]-1][2]    
                            x2=Vias_coord[node[1]-1][0]
                            y2=Vias_coord[node[1]-1][1]
                            z2=Vias_coord[node[1]-1][2]
                            
                            for wire_idx , wire in enumerate(wires):
                                if wire[0][0] <= x1 <= wire[1][0] and wire[0][1] <= y1 <= wire[1][1] and z1==wire[2]:
                                    # Calculate the corresponding width
                                        new_widthsV[wire_idx] = width
                                if wire[0][0] <= x2 <= wire[1][0] and wire[0][1] <= y2 <= wire[1][1] and z2==wire[2]:
                                    # Calculate the corresponding width
                                        new_widthsV[wire_idx] = width


                        else:
                            required_width = ((node[2] / 0.9) + 0.002) / 0.9
                            required_widths.append((node[0], node[1],required_width))



# Calculating EM violations and updating widths
for violation in EM_violations:
    for l, node2 in enumerate(width_bet_nodes2):
        if (violation[0] == node2[0] and violation[1] == node2[1]) or (violation[0] == node2[1] and violation[1] == node2[0]):
            W = node2[2]
            i_max = 0.9 * (W * 0.9 - 0.002)
            if violation[2] >= i_max:
                W = math.ceil(violation[2] / (0.9 * 0.9) + 0.002 / 0.9)
                if W > node2[2]:
                    required_widths.append((violation[0], violation[1], W))

    for l, node2 in enumerate(Vias_connected):
        if (violation[0] == node2[0] and violation[1] == node2[1]) or (violation[0] == node2[1] and violation[1] == node2[0]):
            numOfVias = Number_of_Vias[l]
            i_max = 0.04 * numOfVias
            if violation[2] >= i_max:
                W = math.ceil(0.2 / (violation[2] / numOfVias))
                required_widths.append((violation[0], violation[1], W))

new_widths=np.zeros(len(wires))
for width in required_widths:
    x1=Vias_coord[width[0]-1][0]
    y1=Vias_coord[width[0]-1][1]
    z1=Vias_coord[width[0]-1][2]    
    x2=Vias_coord[width[1]-1][0]
    y2=Vias_coord[width[1]-1][1]
    z2=Vias_coord[width[1]-1][2]
    for wire_idx , wire in enumerate(wires):
        if wire[0][0] <= x1 <= wire[1][0] and wire[0][1] <= y1 <= wire[1][1] and z1==wire[2]:
            # Calculate the corresponding width
                new_widths[wire_idx] = width[2]
        if wire[0][0] <= x2 <= wire[1][0] and wire[0][1] <= y2 <= wire[1][1] and z2==wire[2]:
            # Calculate the corresponding width
                new_widths[wire_idx] = width[2]
print(required_widths)
print(new_widths)
print(new_widthsV)

New_widths = []
for i in range(len(new_widths)):
    New_widths.append(max(new_widths[i], new_widthsV[i]))
print(New_widths)

        
        

