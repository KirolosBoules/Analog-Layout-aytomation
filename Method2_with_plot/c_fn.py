import numpy as np
from Lap_Matrix import Lap_Matrix
Paths=[((1, 2),1), ((2,8),1) ,((2,3),1),((3,4),1),((5,4),1)]
#[(1, 2, 3, 26, 13), (1, 14, 19, 12, 13), (1, 2, 15, 12, 13)]

# Define the adjacency matrix of the graph representing the circuit
A = np.array ( [ [0. , 0. , 0. , 0. ,1.,  1.,  0.,  0.,  0.],
 [0. , 0. , 0. , 0. ,0.,  0.,  0.,  0.,  0.],
[0. , 0. , 0. , 0. ,0.,  0.,  0.,  0.,  0.],
 [ 0. , 0., 1.,  0.,  0.,  0. , 0. , 0. , 1.]] )

# Compute the Laplacian matrix of the graph
D = np.diag(np.sum(A, axis=1))
L = D - A
# Compute the pseudo-inverse of the Laplacian matrix
L_plus = np.linalg.pinv(L)

# Compute the matrix P
I = np.eye(A.shape[0])
P = L_plus.dot(I)

# Find the parallel paths between nodes 1 and 6
s = 0
t = 4
parallel_paths = []
for i in range(P.shape[0]):
    if P[s, i] != 0 and P[t, i] != 0:
        parallel_paths.append(i)
print("Parallel paths between nodes {} and {}: {}".format(s+1, t+1, parallel_paths))

# Find the series paths between nodes 1 and 6
series_paths = []
for i in range(P.shape[0]):
    if i != s and i != t:
        if P[s, i] != 0 and P[i, t] != 0:
            series_paths.append(i)
print("Series paths between nodes {} and {}: {}".format(s+1, t+1, series_paths))
print(L)