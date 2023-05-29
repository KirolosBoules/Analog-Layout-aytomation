from find_all_paths import find_all_paths_bidirectional
import numpy as np

def SD_worst_path_calc(source_nodes,destination_nodes,all_connected_nodes,width_bet_nodes2,Vias_connected,Number_of_Vias, num_layers):
    source_paths=[]
    different_paths=[]
    I_Max = []
    for source_node in source_nodes:
        for destination_node in destination_nodes:
            paths = find_all_paths_bidirectional(source_node, destination_node, all_connected_nodes)
            if len(paths) == 0:
                continue
            paths = list(set([tuple(path) for path in paths]))
            for path in paths: 
                for k in range(len(path) - 1):
                    for l, node2 in enumerate(width_bet_nodes2):
                        if (path[k] == node2[0] and path[k+1] == node2[1]) or (path[k] == node2[1] and path[k+1] == node2[0]):
                            W = node2[2]
                            if num_layers == 1 or num_layers == 2:
                                i_max = 0.9 * (W * 0.9 - 0.002)
                            else:
                                i_max = 0.9 * (W * 0.9 - 0.002) * 2**((num_layers - 2) // 2)

                                I_Max.append((path[k],path[k+1],i_max))
                        # Check if the current width is lower than the required width

                    for l, node2 in enumerate(Vias_connected):
                        if (path[k] == node2[0] and path[k+1] == node2[1]) or (path[k] == node2[1] and path[k+1] == node2[0]):
                            numOfVias = Number_of_Vias[l]
                            i_max = 0.1 * numOfVias # constant for vias
                            I_Max.append((path[k],path[k+1],i_max))

                 
            print(paths)  
            source_paths.append(paths)
    # Append the source_paths list to the parallel_paths list
        different_paths.append(source_paths)
            
    
    return source_paths  , I_Max  ,different_paths
