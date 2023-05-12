import os
import pyvista
import cv2
import numpy as np

# Load map image
project_folder = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(project_folder, 'maps', 'map8.png')
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a binary image. Ignore first return value "threshold value" with _ placeholder, store second return value "thresholded image" in "binary" variable. 
_, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours in the binary image
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Iterate contours, append into building_info
building_info = []

for i in range (len(contours)-1,-1,-1):
    # Get the bounding rectangle for the contour
    x, y, w, h = cv2.boundingRect(contours[i])
    center_x = x + w/2
    center_y = y + h/2
    # Append the top-left corner of the bounding rectangle to the list
    building_info.append((center_x, center_y, w, h))


# Print the starting positions of buildings
print('-------------------------------------------------------------------------------------------------------------\n' + str(building_info) + '\n')

print('Map Dimension: ' + str(image.shape[0]) + 'x'+ str(image.shape[1]))

for i in range (0,len(building_info),1):
    print('--------------------')
    print('Building ' + str(i+1) + ': ')
    print('Coordinates: (' + str(building_info[i][0]) + ',' + str(building_info[i][1]) +')')
    print('Width: ' + str(building_info[i][2]))
    print('Height: ' + str(building_info[i][3]))






### PyVista 3D Visualization

# Create Map Plane
# map = pyvista.Plane(center=(0.5, 0.5, 0), i_size=1, j_size=image.shape[0] / image.shape[1], i_resolution=20, j_resolution=20)

# map = pyvista.Plane(center=(image.shape[0]/2,image.shape[1]/2, 0), i_size=image.shape[0], j_size=image.shape[1])


map = pyvista.Plane(center=(image.shape[0]/2, image.shape[1]/2, 0), i_size=image.shape[0], j_size=image.shape[1],i_resolution=image.shape[0], j_resolution=image.shape[1])


modelBuildings = []
for pos in building_info:
    # x_coord = pos[0] / (image.shape[1]) * (image.shape[0] / image.shape[1])
    # y_coord = (image.shape[0] - pos[1]) / (image.shape[0])



    x_coord = pos[1] 
    y_coord = pos[0] 



    building_height = pos[3]
    building_width = pos[3]
    building_length = pos[3]
    
    modelBuildings.append(pyvista.Cube(x_length=building_width, y_length=building_length, 
    z_length=building_height, center=(x_coord,y_coord, building_height/2)))
    #z_length=building_height, center=(x_coord-image.shape[0]/2,y_coord-image.shape[1]/2, building_height/2)))
    #modelBuildings.append(modelBuildings.pop().rotate_x(90))

#TEST
#modelBuildings.append(pyvista.Cube(x_length=1, y_length=1, z_length=1, center=(0,0,0)))

merged = map.merge(modelBuildings)
merged.rotate_x(270)
merged.rotate_y(270)
merged.rotate_z(270)
#merged.plot(show_edges=True, line_width=5)


theme = pyvista.themes.DefaultTheme()
theme.background = 'black'
theme.color = 'plum'
theme.edge_color = 'white'
theme.render_points_as_spheres = True

plotter = pyvista.Plotter(border= True, border_width= 50, border_color= 'plum', line_smoothing= True, polygon_smoothing= True, lighting= 'light kit', theme= theme)
plotter.add_mesh(merged, show_edges=True, line_width=3)
plotter.show_grid()
plotter.show()







# # view the scene in isometric perspective
# plotter.view_isometric()

# def rotate():
#     plotter.camera.azimuth(1)

# # add a callback function that rotates the camera and update the render window
# callback_id = plotter.add_callback(rotate, interval=100)

# # show the result in notebook
# plotter.show()

# # when done, you can remove the callback if you want
# plotter.remove_callback(callback_id)