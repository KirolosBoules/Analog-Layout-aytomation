import numpy as np

def Lap_Matrix(Resistance_bet_nodes):
    n = max(max(pair) for pair in [r[0] for r in Resistance_bet_nodes]) + 1  # Number of nodes (including the ground node)
    adj_matrix = np.zeros((n, n))
    for r in Resistance_bet_nodes:
        i, j = r[0]
        res = r[1]
        adj_matrix[i, j] = adj_matrix[j, i] = 1/res

# Define the diagonal degree matrix
    deg_matrix = np.diag(adj_matrix.sum(axis=1))

# Define the Laplacian matrix
    lap_matrix = deg_matrix - adj_matrix

# Create a NetworkX graph object and add edges from the adjacency matrix
# Define the Laplacian matrix

# Compute the eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(lap_matrix)

# Find the nonzero eigenvalues
    Ei_values = eigenvalues[np.abs(eigenvalues) > 1e-10]

# Find the indices of the nonzero eigenvalues
    nonzero_indices = np.where(np.abs(eigenvalues) > 1e-10)[0]

# Extract the corresponding eigenvectors
    nonzero_eigenvectors = eigenvectors[:, nonzero_indices]
    Ei_vec=np.transpose(nonzero_eigenvectors)

    return Ei_vec ,Ei_values , adj_matrix , lap_matrix 
 



