def initial_solution():
    wires=generate_wires(num_layers,wire_width,spacing,grid_start,grid_end)

    print(wires)
    if  ( Worst_EM!=0):

        new_widths = New_widths(wires,paths , Worst_EM ,currents_destination , required_widths , Vias_coord , width_V , i_total , all_res_nodes )
        print ('Worst_EM',Worst_EM)
        New_wires_widths = []
        for i in range(len(new_widths)):
            New_wires_widths.append(max(new_widths[i], Wire_Widths[i]))
        print('New_wires_widths',New_wires_widths)
        wires = Updated_wires (grid_start , grid_end , spacing , wire_width, num_layers ,New_wires_widths)    
    return new_widths,New_wires_widths,wires
