
import matplotlib.pyplot as plt
from generate_wires import generate_wires
def Updated_wires (grid_start , grid_end , spacing , wire_width, num_layers ,new_widths):

    wires,_=generate_wires(num_layers,wire_width,spacing,grid_start,grid_end)
    grid_x1, grid_y1 = grid_start
    grid_x2, grid_y2 = grid_end
    new_wires = []


    width_incr_V=0
    width_incr_H=0
    for wire in wires :

        (start, end, layer_idx, voltage) = wire
        new_width = new_widths[wires.index(wire)]
        x1=start[0]
        y1=start[1]
        x2=end[0]
        y2=end[1]

        if (y1 == grid_y1 )and ( y2 == grid_y2 ):  # vertical wire
            current_width = x2 - x1
            width_incr_V += new_width-current_width

        else:  # horizontal wire
            current_width = y2-y1
            width_incr_H += new_width-current_width
    for layer in range (num_layers) :
        index_V=0
        index_H=0
        for wire in wires :
            (start, end, layer_idx, voltage) = wire
            if layer == layer_idx-1 :
                new_width = new_widths[wires.index(wire)]
                x1=start[0]
                y1=start[1]
                x2=end[0]
                y2=end[1]

                if (y1 == grid_y1 )and ( y2 == grid_y2 ):  # vertical wire
                    current_width = x2 - x1
                    new_start = (index_V+spacing ,grid_x1)
                    new_end = (new_start[0]+ new_width, grid_y2+width_incr_H)
                    index_V=new_end[0]

                else:  # horizontal wire
                    current_width = y2-y1
                    new_start = (0 , index_H+spacing)
                    new_end = (grid_x2+width_incr_V , new_start[1]+ new_width)
                    index_H=new_end[1]
            

                new_wires.append((new_start, new_end, layer_idx, voltage))

    return new_wires

'''
grid_start = (0, 0)
grid_end = (20,20)
wire_width=3
spacing=1
wires =[((1.0, 0), (4.0, 20), 1, 1), ((4.75, 0), (7.75, 20), 1, 2), ((8.5, 0), (11.5, 20), 1, 1), ((12.25, 0), (15.25, 20), 1, 2), ((16.0, 0), (19.0, 20), 1, 1), ((0, 1.0), (20, 4.0), 2, 1), ((0, 4.75), (20, 7.75), 2, 2), ((0, 8.5), (20, 11.5), 2, 1), ((0, 12.25), (20, 15.25), 2, 2), ((0, 16.0), (20, 19.0), 2, 1)]

new_widths = [3, 11 , 3, 11 , 3, 3, 3, 3, 11. ,11.]
new_wires = Updated_wires (grid_start , grid_end , spacing , wires ,new_widths)
print (new_wires)
'''
