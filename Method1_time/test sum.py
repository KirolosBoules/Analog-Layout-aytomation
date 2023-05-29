'''
import numpy as np
import networkx as nx
from Lap_Matrix import Lap_Matrix
from Res_bet_two_nodes import Rxy
paths = [((1, 14), 0.05),
((2, 15), 0.05),
((7, 20), 0.05),
((3, 16), 0.05),
((2, 15), 0.05),
((6, 19), 0.05),
((8, 21), 0.05),
((1, 2), 2.5),
((2, 3), 2.5),
((6, 7), 2.5),
((7, 8), 2.5),
((14, 19), 2.5),
((15, 20), 2.5),
((16, 21), 2.5),]

Ei_vec ,Ei_values , adj_matrix , lap_matrix= Lap_Matrix(paths)

R=Rxy(1,7 , Ei_vec, Ei_values)
print (R)

# Set the total current of the circuit

    # Same code as before, returns Ei_vec, Ei_values, adj_matrix, lap_matrix

# Find the current between nodes 1 and 3
node1 = 0
node3 = 1

# Define the voltage vector
V = np.zeros(adj_matrix.shape[0])
V[0] = 1  # Positive terminal of voltage source

# Define the current vector
I = np.zeros(adj_matrix.shape[0])
I[0] = 1  # Positive terminal of voltage source
I[-1] = -1  # Negative terminal of voltage source

# Solve the system of linear equations to get the current values
C = np.linalg.pinv(lap_matrix) @ (V * I)

# Determine the current between nodes 1 and 3
current = C[node1] - C[node3]

print(f"The current between nodes {node1+1} and {node3+1} is {current:.2f} A")

'''

import numpy as np
from Lap_Matrix import Lap_Matrix

# Define the circuit as a list of edges and resistances
circuit   = [((1, 2),5),((2, 3),5),((3, 4),10), (( 1,4),10)]
# Determine the number of nodes in the circuit
Ei_vec ,Ei_values , adj_matrix , L = Lap_Matrix(circuit)
from Res_bet_two_nodes import Rxy
R=Rxy(1,3 , Ei_vec, Ei_values)
print (R)
lap_matrix = L[1:, 1:]
# Define the adjacency matrix and diagonal degree matrix
#adj_matrix = np.zeros((num_nodes, num_nodes))

def compute_currents(lap_matrix,total_current):
    # Define the current vector
    I = np.zeros(len(lap_matrix))
    V = np.zeros(len(lap_matrix))
     # Negative terminal of voltage source
    V[0] = -1
    I[2] = -total_current  # Negative terminal of voltage source
    I[0] = total_current 
# Solve the system of linear equations to get the current values
    C = np.linalg.pinv(lap_matrix) @ (I)
    print (C)
    # Compute the currents between each pair of nodes
    currents = {}
    for i in range(len(lap_matrix)):
        for j in range(i+1, len(lap_matrix)):
            if lap_matrix[i, j] != 0:
                curr = (C[i] - C[j]) * lap_matrix[i, j]
                currents[(i+1, j+1)] = curr
            
    return currents

I = compute_currents(lap_matrix,6)
print(I)

#resistance = circuit[0][1]  # Resistance between nodes 6 and 7
