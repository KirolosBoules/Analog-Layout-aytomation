from calc_Via_rects import calc_Via_rects

def number_of_vias_calc( Vias_connected , Vias_coord , wires , Wire_Widths):
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

    return Number_of_Vias , Via_centers