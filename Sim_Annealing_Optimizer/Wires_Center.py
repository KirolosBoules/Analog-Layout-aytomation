def Wires_Center(wires ):
    Center=[]
    for wire in wires:
        x1, y1 = wire[0]
        x2, y2 = wire[1]
        layer = wire[2]

        if layer % 2 != 0:
            Center_x = (x1 + x2) / 2
            Center.append(Center_x)
        else:
            Center_y = (y1 + y2) / 2
            Center.append(Center_y)

    return Center

