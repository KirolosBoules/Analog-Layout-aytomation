import numpy as np
def R_bet_nodes_calc(directly_connected , Vias_coord , width_bet_nodes ):
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

    return defined_Res , R_bet_nodes