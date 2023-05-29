import math

def calc_minimum_rect_area(num_small_rects, small_rect_area, spacing):
    # Calculate the width and height of each small rectangle
    small_rect_width = small_rect_height = math.sqrt(small_rect_area)
    
    # Calculate the number of small rectangles that can fit per row
    small_rects_per_row = math.ceil(math.sqrt(num_small_rects))
    
    # Calculate the number of rows needed to fit all the small rectangles
    num_rows = math.ceil(float(num_small_rects) / small_rects_per_row)
    
    # Calculate the width and height of the rectangle that can contain all the small rectangles
    width = (small_rects_per_row - 1) * spacing + small_rect_area*small_rects_per_row
    height = (num_rows - 1) * spacing + small_rect_area*small_rects_per_row
    
    # Return the minimum area of the rectangle that can contain all the small rectangles
    return width , height

