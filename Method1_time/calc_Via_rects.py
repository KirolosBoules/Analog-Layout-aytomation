#calc_Via_rects
import math

def calc_Via_rects(large_rect_width, large_rect_height , large_rect_center, small_rect_area, spacing):
  
    # Calculate the width and height of the small rectangle
    Via_width = Via_height= math.sqrt(small_rect_area)
    
    # Calculate the spacing between adjacent small rectangles
    spacing_x = spacing + Via_width
    spacing_y = spacing + Via_height
    
    # Calculate the number of small rectangles that can fit in each dimension
    num_small_rects_x = int((large_rect_width - Via_width) / spacing_x) + 1
    num_small_rects_y = int((large_rect_height - Via_height) / spacing_y) + 1
    
    # Calculate the coordinates of the center of each small rectangle
# Calculate the coordinates of the center of each small rectangle
    small_rect_centers = []
    for i in range(num_small_rects_x):
        for j in range(num_small_rects_y):
            # Calculate the remaining space on each side of the large rectangle
            remaining_x = large_rect_width - (num_small_rects_x - 1) * spacing_x - Via_width
            remaining_y = large_rect_height - (num_small_rects_y - 1) * spacing_y - Via_height
            
            # Calculate the x and y values of the center of the current small rectangle
            x = large_rect_center[0] - (large_rect_width / 2) + (i * spacing_x) + (Via_width / 2) + remaining_x / 2
            y = large_rect_center[1] - (large_rect_height / 2) + (j * spacing_y) + (Via_height / 2) + remaining_y / 2
            
            small_rect_centers.append((x, y))
            
    # Return the number of small rectangles and their centers
    return len(small_rect_centers), small_rect_centers
