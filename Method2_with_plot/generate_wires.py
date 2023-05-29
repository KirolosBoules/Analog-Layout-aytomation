import numpy as np

def generate_wires(num_layers,wire_width,spacing, grid_start ,grid_end):
    grid_x1, grid_y1 = grid_start
    grid_x2, grid_y2 = grid_end
    wire_height = grid_y2 - grid_y1
    num_wires = int((grid_x2 - grid_x1) / (wire_width + spacing))
    wire_centers = np.linspace(grid_x1 + spacing + wire_width/2, grid_x2 - spacing - wire_width/2, num_wires)

    wires = []
    for layer_idx in range(1, num_layers+1):
        voltage = 1  # start with VDD
        if layer_idx % 2 == 0:
            # create wires in the y direction
            for center_y in wire_centers:
                x1, y1 = (grid_x1, center_y - wire_width/2)
                x2, y2 = (grid_x2, center_y + wire_width/2)
                wires.append(((x1, y1), (x2, y2), layer_idx, voltage))  # add layer index and voltage
                voltage = 3 - voltage  # switch between VDD and GND
        else:
        # create wires in the x direction
            for center_x in wire_centers:
                 x1, y1 = (center_x - wire_width/2, grid_y1)
                 x2, y2 = (center_x + wire_width/2, grid_y2)
                 wires.append(((x1, y1), (x2, y2), layer_idx, voltage))  # add layer index and voltage
                 voltage = 3 - voltage  # switch between VDD and GND
    return wires
