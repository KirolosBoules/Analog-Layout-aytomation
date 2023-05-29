
import numpy as np
from Lap_Matrix import Lap_Matrix

def compute_currents(INPUT_node , OUTPUT_node ,total_current ,circuit):
    # Define the circuit as a list of edges and resistances

    # Determine the number of nodes in the circuit
    Ei_vec ,Ei_values , _ , L = Lap_Matrix(circuit)
    from Res_bet_two_nodes import Rxy
    R_eq=Rxy(INPUT_node, OUTPUT_node , Ei_vec, Ei_values)
    lap_matrix = L[1:, 1:]
    # Define the current vector
    I = np.zeros(len(lap_matrix))
     # Negative terminal of voltage source
    I[OUTPUT_node-1] = -total_current  # OUTPUT current at node 7
    I[INPUT_node-1] = total_current   # INPUT current at node 1
# Solve the system of linear equations to get the current values
    C = np.linalg.pinv(lap_matrix) @ (I)
    # Compute the currents between each pair of nodes
    currents = {}
    for i in range(len(lap_matrix)):
        for j in range(i+1, len(lap_matrix)):
            if lap_matrix[i, j] != 0:
                curr = (C[i] - C[j]) * lap_matrix[i, j]
                currents[(i+1, j+1)] = round(curr,2)
            
    current_list = [(k[0], k[1], v) for k, v in currents.items()]
    return current_list ,R_eq

#------------------------------------------------------------------

