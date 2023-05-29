# Calculate the total width of all wires (including the spacing)
import matplotlib.pyplot as plt
import numpy as np

new_widths = [3.0, 3.0, 6.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 6.0]
results_x = np.array([])
results_y = np.array([])
grid_start = (0, 0)
grid_end = (20,20)

grid_x1, grid_y1 = grid_start
grid_x2, grid_y2 = grid_end
# Create a new list of wires with updated widths



def generate_wires(num_layers, wire_widths, spacing, grid_start, grid_end):
    grid_x1, grid_y1 = grid_start
    grid_x2, grid_y2 = grid_end
    wire_height = grid_y2 - grid_y1
    num_wires = len(wire_widths)
    wire_centers = np.linspace(grid_x1 + spacing + wire_widths[0] / 2,
                               grid_x2 - spacing - wire_widths[-1] / 2,
                               num_wires)

    wires = []
    for layer_idx in range(1, num_layers + 1):
        voltage = 1  # start with VDD
        if layer_idx % 2 == 0:
            # create wires in the y direction
            for i, center_y in enumerate(wire_centers):
                wire_width = wire_widths[i % len(wire_widths)]
                x1, y1 = (grid_x1, center_y - wire_width / 2)
                x2, y2 = (grid_x2, center_y + wire_width / 2)
                wires.append(((x1, y1), (x2, y2), layer_idx, voltage))  # add layer index and voltage
                voltage = 3 - voltage  # switch between VDD and GND
        else:
            # create wires in the x direction
            for i, center_x in enumerate(wire_centers):
                wire_width = wire_widths[i % len(wire_widths)]
                x1, y1 = (center_x - wire_width / 2, grid_y1)
                x2, y2 = (center_x + wire_width / 2, grid_y2)
                wires.append(((x1, y1), (x2, y2), layer_idx, voltage))  # add layer index and voltage
                voltage = 3 - voltage  # switch between VDD and GND
    return wires

wires=generate_wires(2,new_widths,1,(0,0),(30,30))
print(wires)
fig, ax = plt.subplots()

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
  # append width to the list for the corresponding layer
    #WireWidth = np.concatenate(WireWidth, axis=0).reshape(num_layers,-1)  # concatenate along columns and reshape to 2D array
    if voltage == 1:
        ax.add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='r', facecolor='red'))
    else:
        ax.add_patch(plt.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=1, edgecolor='b', facecolor='blue'))

plt.xlim(grid_x1, grid_x2)
plt.ylim(grid_y1, grid_y2)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()