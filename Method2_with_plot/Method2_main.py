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
from required_widths_calc import New_widths
from number_of_vias_calc import number_of_vias_calc
from Vias_calc import Vias_calc
from R_bet_nodes import R_bet_nodes_calc
from updatewires3 import Updated_wires
from paths_to_ResNodes import paths_to_ResNodes
from current_resistance import compute_currents

#USER INPUTS 

num_layers = int(input("Enter the number of layers: "))
grid_start = (0, 0)
grid_end = (50,50)
wire_width=3
spacing=3
grid_x1, grid_y1 = grid_start
grid_x2, grid_y2 = grid_end


wires=generate_wires(num_layers,wire_width,spacing,grid_start,grid_end)

i_total = float(input("Enter the total current (in mA ): "))
source_nodes = input("Enter the source nodes (comma-separated): ")
destination_nodes = input("Enter the destination nodes (comma-separated): ")
source_nodes = [int(x.strip()) for x in source_nodes.split(",")]
destination_nodes = [int(x.strip()) for x in destination_nodes.split(",")]
Worst_EM=1
ITER=1
while (Worst_EM!=0) :
    fig, ax = plt.subplots()
    #wires= [((1, 0), (9.5, 20.0), 1, 1), ((10.5, 0), (13.5, 20.0), 1, 2), ((14.5, 0), (17.5, 20.0), 1, 1), ((18.5, 0), (21.5, 20.0), 1, 2), ((22.5, 0), (25.5, 20.0), 1, 1), ((0, 1), (31.0, 4.0), 2, 1), ((0, 5.0), (31.0, 8.0), 2, 2), ((0, 9.0), (31.0, 12.0), 2, 1), ((0, 13.0), (31.0, 16.0), 2, 2), ((0, 17.0), (31.0, 20.0), 2, 1), ((26.5, 0), (29.5, 20.0), 3, 1), ((30.5, 0), (33.5, 20.0), 3, 2), ((34.5, 0), (37.5, 20.0), 3, 1), ((38.5, 0), (41.5, 20.0), 3, 2), ((42.5, 0), (51.0, 20.0), 3, 1)] 
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
        ax.add_patch(plt.Rectangle((x - w/2, y - h/2), w, h, linewidth=1, edgecolor='r', facecolor='y'))

    for n in range (num_layers):
        for node, node_num in node_idx.items():
            if node[2]==n+1 :
                ax.text(node[0]+(n-0.5), node[1]+(n-0.5), str(node_num), ha='center', va='center', fontsize=12)

    # add labels

    plt.axis('equal')
    # set aspect ratio
    plt.gca().set_aspect('equal', adjustable='box')

    # display the plot
    plt.show()

    '''
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
    '''
    #******************** PLOTTING *************************


    #/////////////////////////////EM Calculation /////////////////////////

    # Get user input for i_total and source/destination nodes

    # Convert user input to list of integers



    #EM_violations=1



    paths , I_Max , different_paths = SD_worst_path_calc(source_nodes,destination_nodes,all_connected_nodes,width_bet_nodes2,Vias_connected,Number_of_Vias)
    print ('paths',paths)

    currents_destination=[]
    currents = []
    all_currents=[]
    R_equivalent=[]
    for destination in paths :
        circuit , NODE ,_ = paths_to_ResNodes (all_res_nodes , destination)
        S = destination [0][0]
        D = destination [0][-1]
        I , R_eq = compute_currents( S , D ,i_total ,circuit)
        currents_destination.append(I)
        currents.extend(I)
        R_equivalent.append(R_eq)
    print('R_eq',R_equivalent)
    
    Total_drop = [i_total * R for R in R_equivalent]
    print ('Total Drop', Total_drop)
    #print (currents)
    #print (currents_destination)



    signed_sum_currents = {}
    rail_sum_currents=[]
    for item in currents:
        if (item[0], item[1]) in signed_sum_currents:
            signed_sum_currents[(item[0], item[1])] += item[2]
        else:
            signed_sum_currents[(item[0], item[1])] = item[2]
    signed_sum_currents = [(k[0], k[1], v) for k, v in signed_sum_currents.items()] #write in that form (node1 , node2 ,sum of all currents that will path)
    #print ('signed_sum_currents',signed_sum_currents)

    for num in signed_sum_currents:
        rail_sum_currents.append((num[0],num[1],abs(num[2])))
    #print ('rail_sum_currents',rail_sum_currents)

    required_widths,new_widthsV_Mat, EM_violations , Worst_EM , width_V = required_widths_calc(rail_sum_currents,I_Max,Vias_connected,Vias_coord ,wires)
    all_req_widths=new_widthsV_Mat+required_widths
    #print ( 'required_widths',required_widths)
    if  ( Worst_EM!=0):

        wire_to_increased = New_widths(wires,paths , Worst_EM ,currents_destination , Vias_coord , i_total , all_res_nodes,wire_width)
        print ('Worst_EM',Worst_EM) 

        for i in range (len(wire_to_increased)):
            if wire_to_increased [i]!=0 :
                wire_to_increased[i]+=1
                wire_width=wire_to_increased[i]
     
        #print ('wire_to_increased',wire_to_increased)

        New_wires_widths = []
        for i in range(len(wire_to_increased)):
            New_wires_widths.append(max(wire_to_increased[i], Wire_Widths[i]))
        print('New_wires_widths',New_wires_widths)
        wires = Updated_wires (grid_start , grid_end , spacing , 3, num_layers ,New_wires_widths)

        #print ('New wires Coordinates',wires)
       
        print ('-----------------------------------ITERATION' ,ITER,'------------------------------------------')
        ITER+=1
    else :
        print ('DONE -------> NO EM Violation')