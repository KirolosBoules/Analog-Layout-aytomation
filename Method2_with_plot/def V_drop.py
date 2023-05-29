import numpy as np

def required_widths_calc(rail_sum_currents,I_Max,Vias_connected,Vias_coord ,wires , all_res_nodes , Max_drop ):
    required_widths=[]
    EM_violations_worst = []
    V_drop=[]
    new_widthsV=np.zeros(len(wires)) 
    for  node in (rail_sum_currents): 
            for node2 in all_res_nodes :
                if (node[0] == node2[0] and node[1] == node2[1]) or (node[0] == node2[1] and node[1] == node2[0]) :
                    V_drop.append((node[0], node[1], node[2]*node2[2]))
                    if node[2] >= Max_drop[2]: # treshold drop 
                        EM_violations_worst.append((node[0], node[1], node[2], node2[2]))
                        print ("EM Violation between ",node[0],"and ",node[1],"With current :",node[2] ,"exceeding the max: ",node2[2])
                        via_found = False
                        for via in Vias_connected :           
                            if  (node[0] == via[0] and node[1] == via[1]):
                                via_found = True
                                numOFvia_required=node[2]/0.04
                                width,h=calc_minimum_rect_area(numOFvia_required,1,0.25)
                                print ("Number of vias",numOFvia_required)
                                for wire_idx , wire in enumerate(wires):
                                    if wire[0][0] <= x1 <= wire[1][0] and wire[0][1] <= y1 <= wire[1][1] and z1==wire[2]:
                                        # Calculate the corresponding width
                                            new_widthsV[wire_idx] = width
                                    if wire[0][0] <= x2 <= wire[1][0] and wire[0][1] <= y2 <= wire[1][1] and z2==wire[2]:
                                        # Calculate the corresponding width
                                            new_widthsV[wire_idx] = width


                        if not via_found:    
                            required_width = ((node[2] / 0.9) + 0.002) / 0.9
                            required_widths.append((node[0], node[1],required_width))