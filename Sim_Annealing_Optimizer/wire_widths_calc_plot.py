import numpy as np
#import matplotlib.pyplot as plt

def wire_widths_calc_plot(wires):
    Wire_Widths=np.array([])
    results_x = np.array([])
    results_y = np.array([])

    for wire in wires:
        x1, y1 = wire[0]
        x2, y2 = wire[1]
        layer = wire[2]
        voltage = wire[3]
        if layer % 2 != 0:
            width = abs(x2 - x1)
            Center_x = (x1 + x2) / 2
            results_x = np.append(results_x, (Center_x, layer, voltage))
            results_x = np.reshape(results_x, (-1, 3))
            results_x = list(map(tuple, results_x))
        else:
            width = abs(y2 - y1)
            Center_y = (y1 + y2) / 2
            results_y = np.append(results_y, (Center_y, layer, voltage))
            results_y = np.reshape(results_y, (-1, 3))
            results_y = list(map(tuple, results_y))
        Wire_Widths=np.append(Wire_Widths,width)  # append width to the list for the corresponding layer
          # concatenate along columns and reshape to 2D array

    return Wire_Widths , results_x , results_y

