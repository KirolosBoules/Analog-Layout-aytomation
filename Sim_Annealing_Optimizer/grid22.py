import matplotlib.pyplot as plt
from shapely.geometry import LineString
import numpy as np
import networkx as nx
# Functions #
from generate_wires import generate_wires
from calc_Via_rects import calc_Via_rects
from find_all_paths import find_all_paths_bidirectional
from calc_minimum_rect_area import calc_minimum_rect_area
from wire_widths_calc_plot import wire_widths_calc_plot
from directly_connected_nodes import directly_connected_nodes
from SD_worst_path import SD_worst_path_calc
from required_widths_calc import required_widths_calc
from number_of_vias_calc import number_of_vias_calc
from Vias_calc import Vias_calc
from R_bet_nodes import R_bet_nodes_calc
from updatewires2 import Updated_wires
#USER INPUTS 

num_layers = int(input("Enter the number of layers: "))
grid_start = (0, 0)
grid_end = (20,20)
wire_width=3
spacing=1
grid_x1, grid_y1 = grid_start
grid_x2, grid_y2 = grid_end

fig, ax = plt.subplots()

wires=generate_wires(num_layers,wire_width,spacing,grid_start,grid_end)
#wires= 
Wire_Widths ,results_x , results_y =wire_widths_calc_plot(wires, fig ,ax) # Calculate Wire Width annd plot them
Vias_coord , node_idx , Vias_connected = Vias_calc(results_x , results_y )
Number_of_Vias , Via_centers = number_of_vias_calc( Vias_connected , Vias_coord , wires , Wire_Widths)
width_bet_nodes , width_bet_nodes2 ,directly_connected =directly_connected_nodes(wires,Vias_coord,Wire_Widths,node_idx)
all_connected_nodes = directly_connected + Vias_connected
num_nodes = len(all_connected_nodes)
defined_Res , R_bet_nodes = R_bet_nodes_calc(directly_connected , Vias_coord , width_bet_nodes )

print('node_idx',node_idx)

Res_Vias=[]
for N,via in enumerate (Vias_connected) : 
    Res_Vias.append(((via[0], via[1]), 0.2/Number_of_Vias[N]))

all_res_nodes=Res_Vias+defined_Res

#******************** PLOTTING *************************
# PLOTTING VIAS
for center in Via_centers:
    x=center[0]
    y=center[1]
    w=h=1 # standard width and height of Via
    ax.add_patch(plt.Rectangle((x - w/2, y - h/2), w, h, linewidth=1, edgecolor='r', facecolor='y'))

#plt.ylim(0,20)
#plt.xlim(0,38)
plt.axis('equal')
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

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

#******************** PLOTTING *************************


#/////////////////////////////EM Calculation /////////////////////////

 # Get user input for i_total and source/destination nodes
i_total = float(input("Enter the total current (in mA ): "))
source_nodes = input("Enter the source nodes (comma-separated): ")
destination_nodes = input("Enter the destination nodes (comma-separated): ")

# Convert user input to list of integers
source_nodes = [int(x.strip()) for x in source_nodes.split(",")]
destination_nodes = [int(x.strip()) for x in destination_nodes.split(",")]


#EM_violations=1



worst_paths , i_worst_MAT , I_Max , EM_violations_bef_sum , parallel_paths = SD_worst_path_calc(source_nodes,destination_nodes,all_connected_nodes,i_total,width_bet_nodes2, R_bet_nodes,Vias_connected,Number_of_Vias)
#print ("worst Paths",worst_paths)
#print ("worst_current",i_worst_MAT)

print ('parallel paths',parallel_paths)
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

new_widths_V , new_widths_W ,required_widths, new_widthsV_Mat,EM_violations_worst= required_widths_calc(rail_sum_currents,I_Max,Vias_connected,Vias_coord ,wires)

all_req_widths=new_widthsV_Mat+required_widths
#for violation in EM_violations:
#    print(f"EM violation between node {violation[0]} and {violation[1]} with current {violation[2]:.4f}A exceeds the maximum allowable current {violation[3]:.4f}A.")

##############3
parallel_paths_with_width=[]
for width in all_req_widths :
    for i ,paths in enumerate (parallel_paths) : # parallel paths [[[(1, 2, 3, 16, 21, 26, 13), (1, 14, 19, 24, 11, 12, 13), (1, 2, 15, 20, 25, 12, 13)], [(1, 2, 15, 20, 7), (1, 2, 3, 16, 21, 8, 7), (1, 14, 19, 6, 7)], [(1, 2, 3, 16, 21, 8), (1, 14, 19, 6, 7, 8), (1, 2, 15, 20, 7, 8)]]]
        for path in paths :
            for node in path :
                for l in range(len(node) - 1):
                    if (node[l] == width[0] and node[l+1] == width[1]) or (node[l] == width[1] and node[l+1] == width[0]):
                        parallel_paths_with_width.append((node[l], node[l+1], width[2] ,i ))


max_path_width = np.zeros(len(parallel_paths))
 
for node in parallel_paths_with_width:
    for i in range(len(parallel_paths)):
        if node[3] == i:
            if node[2] > max_path_width[i]:
                max_path_width[i] = node[2]
 
# Create a list of tuples where each tuple contains the max width and its corresponding index (path number)
max_widths = [(max_path_width[i], i) for i in range(len(parallel_paths))]
print("Maximum path width and index: ", max_widths)


P_new_widths=np.zeros(len(wires)) 
for j,width in enumerate (max_widths) :
    for  i , paths in enumerate (parallel_paths) : 
        if width[1] == i  :                                     # parallel paths [[[(1, 2,21, 26, 13), (1, 2, 15, 12, 13)], [(1, 2, 15, 20, 7), (1, 14, 19, 6, 7)], [(1, 2, 3, 16, 21, 8), (1, 2, 15, 20, 7, 8)]]]
            for path in  paths :
                for node in path :
                    for node_idx in node :
                        x1=Vias_coord[node_idx-1][0]
                        y1=Vias_coord[node_idx-1][1]
                        z1=Vias_coord[node_idx-1][2]    
                        for wire_idx , wire in enumerate(wires):
                            if wire[0][0] <= x1 <= wire[1][0] and wire[0][1] <= y1 <= wire[1][1] and z1==wire[2]:
                                # Calculate the corresponding width
                                    P_new_widths[wire_idx] = width[0]

print ('P_new_widths',P_new_widths)            


    


print ('required_widths',required_widths)
print ('parallel_paths_with_width',parallel_paths_with_width)



#############3
'''
New_widths = []
for i in range(len(new_widths_W)):
    New_widths.append(max(new_widths_W[i], new_widths_V[i]))

print ('New Widths_W2',new_widths_W)
'''
New_wires_widths = []
for i in range(len(P_new_widths)):
    New_wires_widths.append(max(P_new_widths[i], Wire_Widths[i]))

new_wires = Updated_wires (grid_start , grid_end , spacing , wires ,New_wires_widths)

print ('New wires Coordinates',new_wires)
print ('New Widths',New_wires_widths)