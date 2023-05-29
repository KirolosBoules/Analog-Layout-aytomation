import matplotlib.pyplot as plt
from shapely.geometry import LineString
import numpy as np
import networkx as nx
import random
import math
import time

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

# Define initial temperature, cooling rate and number of iterations
initial_temp = 1000
cooling_rate = 0.03
num_iterations = 2000

#USER INPUTS 




num_layers = int(input("Enter the number of layers: "))
i_total = float(input("Enter the total current (in mA ): "))
source_nodes = input("Enter the source nodes (comma-separated): ")
destination_nodes = input("Enter the destination nodes (comma-separated): ")
source_nodes = [int(x.strip()) for x in source_nodes.split(",")]
destination_nodes = [int(x.strip()) for x in destination_nodes.split(",")]
grid_start = (0, 0)
grid_end = (50,50)
wire_width=3
spacing=3
grid_x1, grid_y1 = grid_start
grid_x2, grid_y2 = grid_end

start_time = time.time()
wires , _=generate_wires(num_layers,wire_width,spacing,grid_start,grid_end)
iter=0
best_solution = 1000
best_cost = 1000
for i in range(num_iterations):
    #fig, ax = plt.subplots()
    Wire_Widths ,results_x , results_y =wire_widths_calc_plot(wires) # Calculate Wire Width annd plot them
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

    # PLOTTING VIAS
    '''
    for center in Via_centers:
        x=center[0]
        y=center[1]
        w=h=1 # standard width and height of Via
        ax.add_patch(plt.Rectangle((x - w/2, y - h/2), w, h, linewidth=1, edgecolor='r', facecolor='y'))

    for n in range (num_layers):
        for node, node_num in node_idx.items():
            if node[2]==n+1 :
                ax.text(node[0]+(n-0.5), node[1]+(n-0.5), str(node_num), ha='center', va='center', fontsize=12)


    #plt.axis('equal')
    # set aspect ratio
    #plt.gca().set_aspect('equal', adjustable='box')

    # display the plot
    #plt.show()
    '''

    paths , I_Max , different_paths = SD_worst_path_calc(source_nodes,destination_nodes,all_connected_nodes,width_bet_nodes2,Vias_connected,Number_of_Vias,num_layers)
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




    signed_sum_currents = {}
    rail_sum_currents=[]
    for item in currents:
        if (item[0], item[1]) in signed_sum_currents:
            signed_sum_currents[(item[0], item[1])] += item[2]
        else:
            signed_sum_currents[(item[0], item[1])] = item[2]
    signed_sum_currents = [(k[0], k[1], v) for k, v in signed_sum_currents.items()] #write in that form (node1 , node2 ,sum of all currents that will path)

    for num in signed_sum_currents:
        rail_sum_currents.append((num[0],num[1],abs(num[2])))


    _,_, EM_violations , _ , width_V = required_widths_calc(rail_sum_currents,I_Max,Vias_connected,Vias_coord ,wires)
    if EM_violations == 0 :
        end_time = time.time()
        total_time = end_time - start_time
        print("Total time taken:", total_time, "seconds")
    # Define the initial solution
    #initial solution 
    '''
    new_widths = New_widths(wires,paths , Worst_EM ,currents_destination , required_widths , Vias_coord , width_V , i_total , all_res_nodes )
    print ('Worst_EM',Worst_EM)
    New_wires_widths = []
    for i in range(len(new_widths)):
        New_wires_widths.append(max(new_widths[i], Wire_Widths[i]))
    print('New_wires_widths',New_wires_widths)
    '''

    def cost_function(EM_violations):
        
        cost = 0
        for violation in (EM_violations):
            
            cost +=violation[2] - violation[3]
        print('Cost=', cost)
        return cost

    def neighbor(New_wires_widths):
        # Select a random wire
        wire_idx = random.randint(0, len(New_wires_widths) - 1)
        old_width = New_wires_widths[wire_idx]
        # Randomly increase or decrease the width by a small amount
        new_width = old_width + random.uniform(0 , 0.5)
        new_width = max(1, new_width) # Width must be at least 3
        # Create a new solution with the updated wire width
        new_solution =  New_wires_widths.copy()
        new_solution[wire_idx] = new_width
        return new_solution

    def acceptance_probability(old_cost, new_cost, temperature):
        if new_cost < old_cost:
            return 1.0
        else:
            return math.exp((old_cost - new_cost) / temperature)

    # Initialize the current solution and cost
    current_solution= Wire_Widths
    current_cost = cost_function(EM_violations)

    # Initialize the best solution and cost

    
    # Loop through the iterations
    ####for i in range(num_iterations):
        
    # Generate a new solution
    new_solution = neighbor(current_solution)
    

    wires = Updated_wires (grid_start , grid_end , spacing , wire_width, num_layers ,new_solution)    

    _,_, EM_violations , _ ,_= required_widths_calc(rail_sum_currents,I_Max,Vias_connected,Vias_coord ,wires)

    # Calculate the cost of the new solution
    new_cost = cost_function(EM_violations)
    # Calculate the acceptance probability
    ap = acceptance_probability(current_cost, new_cost, initial_temp)
    # Decide whether to accept the new solution
    if ap > random.uniform(0, 1):
        current_solution = new_solution
        current_cost = new_cost
    # Keep track of the best solution found so far
    if current_cost < best_cost:
        best_solution = current_solution
        best_cost = current_cost
    # Cool the temperature
    initial_temp = initial_temp * (1 - cooling_rate)
    
    iter+=1
    print('Iteration ',iter)
    # Print the best solution found
    print("best solution", best_solution)
    print("Best cost: ", best_cost)


