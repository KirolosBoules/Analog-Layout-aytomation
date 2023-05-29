def Rxy(start,end , Ei_vec, Ei_values):
    Node=[start,end]
    total_R=0
    for i in range(len(Ei_values)) :
        R=(1/Ei_values[i])*( Ei_vec[i][Node[0]] - Ei_vec[i][Node[1]] )**2
        total_R += R
    
    return total_R
