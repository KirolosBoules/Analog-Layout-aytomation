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

#wires=generate_wires(num_layers,wire_width,spacing,grid_start,grid_end)
wires=[((1, 0), (4.6197176271572395, 20.0), 1, 1), ((5.6197176271572395, 0), (8.61971762715724, 20.0), 1, 2), ((9.61971762715724, 0), (12.61971762715724, 20.0), 1, 1), ((13.61971762715724, 0), (16.61971762715724, 20.0), 1, 2), ((17.61971762715724, 0), (20.61971762715724, 20.0), 1, 1), ((0, 1), (20.61971762715724, 4.0), 2, 1), ((0, 5.0), (20.61971762715724, 8.0), 2, 2), ((0, 9.0), (20.61971762715724, 12.0), 2, 1), ((0, 13.0), (20.61971762715724, 16.0), 2, 2), ((0, 17.0), (20.61971762715724, 20.0), 2, 1)]

Wire_Widths ,results_x , results_y =wire_widths_calc_plot(wires, fig ,ax) # Calculate Wire Width annd plot them
Vias_coord , node_idx , Vias_connected = Vias_calc(results_x , results_y )
Number_of_Vias , Via_centers = number_of_vias_calc( Vias_connected , Vias_coord , wires , Wire_Widths)
width_bet_nodes , width_bet_nodes2 ,directly_connected =directly_connected_nodes(wires,Vias_coord,Wire_Widths,node_idx)
all_connected_nodes = directly_connected + Vias_connected
num_nodes = len(all_connected_nodes)
defined_Res , R_bet_nodes = R_bet_nodes_calc(directly_connected , Vias_coord , width_bet_nodes )

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
    ax.add_patch(plt.Rectangle((x - w/2, y - h/2), w, h, linewidth=1, edgecolor='r', facecolor='yellow'))

plt.ylim(0,20)
plt.xlim(0,38)
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
i_total = float(input("Enter the total current (in Amperes): "))
source_nodes = input("Enter the source nodes (comma-separated): ")
destination_nodes = input("Enter the destination nodes (comma-separated): ")

# Convert user input to list of integers
source_nodes = [int(x.strip()) for x in source_nodes.split(",")]
destination_nodes = [int(x.strip()) for x in destination_nodes.split(",")]


#EM_violations=1



worst_paths , i_worst_MAT , I_Max, EM_violations_bef_sum  = SD_worst_path_calc(source_nodes,destination_nodes,all_connected_nodes,i_total,width_bet_nodes2, R_bet_nodes,Vias_connected,Number_of_Vias)
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

new_widths_V , new_widths_W , required_widths, new_widthsV_Mat,EM_violations_worst = required_widths_calc(rail_sum_currents,I_Max,Vias_connected,Vias_coord ,wires)
all_req_widths=new_widthsV_Mat+required_widths
#for violation in EM_violations:
#    print(f"EM violation between node {violation[0]} and {violation[1]} with current {violation[2]:.4f}A exceeds the maximum allowable current {violation[3]:.4f}A.")


New_widths = []
for i in range(len(new_widths_W)):
    New_widths.append(max(new_widths_W[i], new_widths_V[i]))


New_wires_widths = []
for i in range(len(New_widths)):
    New_wires_widths.append(max(New_widths[i], Wire_Widths[i]))

new_wires = Updated_wires (grid_start , grid_end , spacing , wires ,New_wires_widths)

print ('New wires Coordinates',new_wires)
print ('New Widths',New_wires_widths)