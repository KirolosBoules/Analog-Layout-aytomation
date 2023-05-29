new_widths = [3.0, 3.0, 6.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 6.0]
wires=[((1.0, 0), (4.0, 20), 1, 1), ((4.75, 0), (7.75, 20), 1, 2), ((8.5, 0), (11.5, 20), 1, 1), ((12.25, 0), (15.25, 20), 1, 2), ((16.0, 0), (19.0, 20), 1, 1), ((0, 1.0), (20, 
4.0), 2, 1), ((0, 4.75), (20, 7.75), 2, 2), ((0, 8.5), (20, 11.5), 2, 1), ((0, 12.25), (20, 15.25), 2, 2), ((0, 16.0), (20, 19.0), 2, 1)]
new_wires = []
spacing=1
for wire, new_width in zip(wires, new_widths):
    (x1, y1), (x2, y2), layer, voltage = wire
    if x1 == x2:  # vertical wire
        center_x = (x1 + x2) / 2
        y_diff = (y2 - y1 - new_width) / 2
        y1 = y1 + y_diff
        y2 = y2 - y_diff
        x1 += spacing
        x2 -= spacing
    else:  # horizontal wire
        center_y = (y1 + y2) / 2
        x_diff = (x2 - x1 - new_width) / 2
        x1 = x1 + x_diff
        x2 = x2 - x_diff
        y1 += spacing
        y2 -= spacing
    new_wires.append(((x1, y1), (x2, y2), layer, voltage))

print (new_wires)