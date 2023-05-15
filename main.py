import os
import pyvista
import cv2
import numpy as np
import pytesseract
import webcolors


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def closest_color(requested_color):
    min_colors = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = name
    return min_colors[min(min_colors.keys())]



# Load map image
project_folder = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(project_folder, 'maps', 'map15.png')
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a binary image. Ignore first return value "threshold value" with _ placeholder, store second return value "thresholded image" in "binary" variable. 
_, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours in the binary image
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow('Grayscale Image', gray) # TEST
cv2.imshow('Grayscale Image', image) # TEST
# Iterate contours, append into building_info
building_info = []

for i in range (len(contours)-1,-1,-1):
    # Get the bounding rectangle for the contour
    x, y, w, h = cv2.boundingRect(contours[i])
    center_x = x + w/2
    center_y = y + h/2
    # Append the top-left corner of the bounding rectangle to the list
    building_info.append([center_x, center_y, w, h])


# Print the starting positions of buildings
print('-------------------------------------------------------------------------------------------------------------\n' + str(building_info) + '\n')
print('Map Dimension: ' + str(image.shape[0]) + 'x'+ str(image.shape[1]))
for i in range (0,len(building_info),1):
    print('--------------------')
    print('Building ' + str(i+1) + ': ')
    print('Coordinates: (' + str(int(building_info[i][0])) + ',' + str(int(building_info[i][1])) +')')
    # Crop the image to the area of the building
    cropped = image[int(building_info[i][0]-building_info[i][3]/1.5):int(building_info[i][0]+building_info[i][3]), int(building_info[i][1]-building_info[i][2]/1.5):int(building_info[i][1]+building_info[i][2])]
    resized = cv2.resize(cropped, None, fx=20, fy=20, interpolation=cv2.INTER_CUBIC)
    # Recognize the text from the cropped image
    text = pytesseract.image_to_string(resized, config='--psm 6 digits')
    building_info[i].append(int(text))
    print(f"Height: {building_info[i][4]}")
    cv2.imshow('Grayscale Image', resized)
    #pixel_color = (image[int(building_info[i][0]-int(building_info[i][2]/2)),int(building_info[i][1])])
    pixel_color = (image[int(building_info[i][0]+2),int(building_info[i][1])])
    print(closest_color(pixel_color))


### PyVista 3D Visualization
theme = pyvista.themes.DefaultTheme()
theme.background = 'dimgrey'
theme.color = 'plum'
theme.edge_color = 'white'
theme.render_points_as_spheres = True
plotter = pyvista.Plotter(border= True, border_width= 50, border_color= 'plum', line_smoothing= True, polygon_smoothing= True, lighting= 'light kit', theme= theme)

map = pyvista.Plane(center=(image.shape[0]/2, image.shape[1]/2, 0), i_size=image.shape[0], j_size=image.shape[1],i_resolution=image.shape[0], j_resolution=image.shape[1])


modelBuildings = []
labels = []
points = []
counter = 0
for pos in building_info:
    counter += 1
    x_coord = pos[1] 
    y_coord = pos[0]
    building_height = pos[4]*7.5
    building_width = pos[2]
    building_length = pos[3]
    
    #modelBuildings.append(pyvista.Cube( x_length=building_width, y_length=building_length, z_length=building_height, center=(x_coord,y_coord, building_height/2) ))
    modelBuildings.append(pyvista.Cylinder(radius = building_width/2, height= building_height, direction = (0,0,1), center=(x_coord,y_coord, building_height/2)))
    label_text = f"Building {counter}: \n({int(x_coord)}, {int(y_coord)})"
    labels.append((label_text))
    points.append((x_coord-building_width/6, y_coord+building_length/6, building_height*1.5))
    modelBuildings.append(pyvista.Line(pointa=(x_coord, y_coord, building_height), pointb=(x_coord-building_width/6, y_coord+building_length/6, building_height*1.5), resolution=1))




merged = map.merge(modelBuildings)
# merged.rotate_x(270)
# merged.rotate_y(270)
# merged.rotate_z(270)






actor = plotter.add_point_labels(points,labels,italic=False,font_size=10,point_color='red',point_size=1,render_points_as_spheres=True,always_visible=True,shadow=True)
#plotter.camera_position = 'iso'

plotter.enable_anti_aliasing('ssaa')
_ = plotter.add_axes(line_width=5, labels_off=True)
plotter.add_mesh(merged, show_edges=True, line_width=1, smooth_shading= True)
plotter.show_grid()

plotter.show(auto_close= True)






# ---Rotate Test Start---
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
# --- Rotate Test End --- 