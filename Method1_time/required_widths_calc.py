from calc_minimum_rect_area import calc_minimum_rect_area
from find_parallel_res import find_parallel_res
from paths_to_ResNodes import paths_to_ResNodes
import numpy as np

def required_widths_calc(rail_sum_currents,I_Max,Vias_connected,Vias_coord ,wires):
    Calc_width = 0
    required_widths=[]
    EM_violations = []
    new_widthsV_Mat=[]
    EM_diff=[]
    new_widthsV=np.zeros(len(wires)) 
    for  node in (rail_sum_currents): 
            for node2 in I_Max:
                if (node[0] == node2[0] and node[1] == node2[1]) or (node[0] == node2[1] and node[1] == node2[0]) :
                    #V_drop.append((node[0], node[1], node[3]))
                    if node[2] > node2[2]: # if i > imax
                        EM_violations.append((node[0], node[1], node[2], node2[2]))
                        EM_diff.append(node[2] - node2[2])
                        print ("EM Violation between ",node[0],"and ",node[1],"With current :",node[2] ,"exceeding the max: ",node2[2])
                    #else :
                    #   EM_diff.append(0)
    if len(EM_violations) != 0:

        Worst_EM = max(EM_diff)
        Worst_EM_idx = EM_diff.index(Worst_EM)
        node = EM_violations [Worst_EM_idx] 
        
        via_found = False
        for via in Vias_connected :          
            if  (node[0] == via[0] and node[1] == via[1]) or (node[0] == via[1] and node[1] == via[0]) :
                via_found = True
                numOFvia_required=node[2]/0.11
                width,h=calc_minimum_rect_area(numOFvia_required,1,0.25)
                Calc_width=width
                x1=Vias_coord[node[0]-1][0]
                y1=Vias_coord[node[0]-1][1]
                z1=Vias_coord[node[0]-1][2]    
                x2=Vias_coord[node[1]-1][0]
                y2=Vias_coord[node[1]-1][1]
                z2=Vias_coord[node[1]-1][2]
                print ("Number of vias",numOFvia_required)
                for wire_idx , wire in enumerate(wires):
                    if wire[0][0] <= x1 <= wire[1][0] and wire[0][1] <= y1 <= wire[1][1] and z1==wire[2]:
                        # Calculate the corresponding width
                            new_widthsV[wire_idx] = width
                            new_widthsV_Mat.append((node[0],node[1],width))
                    if wire[0][0] <= x2 <= wire[1][0] and wire[0][1] <= y2 <= wire[1][1] and z2==wire[2]:
                        # Calculate the corresponding width
                            new_widthsV[wire_idx] = width
                            new_widthsV_Mat.append((node[0],node[1],width))

        
        if not via_found:    
            required_width = ((node[2] / 0.9) + 0.002) / 0.9
            required_widths.append((node[0], node[1],required_width))
    else  :
         required_widths=0
         new_widthsV_Mat=0
         EM_violations=0
         node=0 
         Calc_width = 0  

    return required_widths,new_widthsV_Mat, EM_violations , node , Calc_width

#//////////////////////////////////
def New_widths(wires,paths , Worst_EM ,currents_destination , required_widths , Vias_coord , width_V , i_total , all_res_nodes):
    
    new_widths=np.zeros(len(wires))
    node = (Worst_EM[0], Worst_EM[1])
    for i, destination in enumerate(paths) :
        _ , NODE , rev_NODE = paths_to_ResNodes (all_res_nodes , destination)
        if node in NODE or node in rev_NODE:
            path_idx=i  # to check which destination path does EM exist 
            parallel_resistances =  find_parallel_res(currents_destination[path_idx],node , i_total)

    width_W = required_widths[0][2]
    
    for iterr in [ required_widths , parallel_resistances ]:
        for node in iterr:
            x1=Vias_coord[node[0]-1][0]
            y1=Vias_coord[node[0]-1][1]
            z1=Vias_coord[node[0]-1][2]    
            x2=Vias_coord[node[1]-1][0]
            y2=Vias_coord[node[1]-1][1]
            z2=Vias_coord[node[1]-1][2]
            for wire_idx , wire in enumerate(wires):
                if wire[0][0] <= x1 <= wire[1][0] and wire[0][1] <= y1 <= wire[1][1] and z1==wire[2]:
                    # Calculate the corresponding width
                        new_widths[wire_idx] = max(width_W ,width_V)
                if wire[0][0] <= x2 <= wire[1][0] and wire[0][1] <= y2 <= wire[1][1] and z2==wire[2]:
                    # Calculate the corresponding width
                        new_widths[wire_idx] = max(width_W ,width_V)   
    return   new_widths 