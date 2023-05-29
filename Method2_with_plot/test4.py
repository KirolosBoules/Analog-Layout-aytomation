import math
rail_currents =  [(1, 2, 2.65), (1, 14, 1.35), (2, 3, 0.99), (2, 15, 1.66), (3, 16, 0.99), (6, 7, 1.35), (6, 19, 1.35), 
(7, 8, 0.99), (7, 20, 1.66), (8, 21, 0.99), (14, 19, 1.35), (15, 20, 1.66), (16, 21, 0.99)]
parallel_resistances=[]
node_idx=2
i_total=4
for i in range(len(rail_currents)):
    a=rail_currents[i][2] + rail_currents[node_idx][2]
    for j in range(len(rail_currents)):
        b= rail_currents[j][2]
        if any(math.isclose(a, x, rel_tol=0.05) for x in [b]) or any(math.isclose(a, x, rel_tol=0.05) for x in [i_total]) :
            parallel_resistances.append(rail_currents[i])

print(parallel_resistances)