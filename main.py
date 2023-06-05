import os
import pyvista
import cv2
import numpy as np
import pytesseract
import webcolors
import serial
import time


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
output_folder = os.path.join(project_folder, 'output_images')
os.makedirs(output_folder, exist_ok=True)
image_path = os.path.join(project_folder, 'maps', 'map19.png')
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
    building_info.append([int(round(center_x)), int(round(center_y)), w])


# Print the starting positions of buildings
print('-------------------------------------------------------------------------------------------------------------\n')
print('Map Dimension: ' + str(image.shape[0]) + 'x'+ str(image.shape[1]))
for i in range (0,len(building_info),1):
    print('--------------------')
    print('Building ' + str(i+1) + ': ')
    print('Coordinates: (' + str(int(building_info[i][0])) + ',' + str(int(building_info[i][1])) +')')
    # Crop the image to the area of the building
    cropped = image[int(building_info[i][1]-building_info[i][2]/2):int(building_info[i][1]+building_info[i][2]/2), int(building_info[i][0]-building_info[i][2]/2):int(building_info[i][0]+building_info[i][2]/2)]
    #resized = cv2.resize(cropped, None, fx=20, fy=20, interpolation=cv2.INTER_CUBIC)
    #Recognize the text from the cropped image
    text = pytesseract.image_to_string(cropped, config='--psm 7 digits')
    #Add found text with OCR to building_info
    try:
        building_info[i].append(int(text))
    except ValueError:
        building_info[i].append(0)
    
    print(f"Height: {building_info[i][3]}")

    #cv2.imshow('Grayscale Image', cropped)
    filename = os.path.join(output_folder, f'building_{i+1}.png')
    cv2.imwrite(filename, cropped)

    #pixel_color = (image[int(building_info[i][0]-int(building_info[i][2]/2)),int(building_info[i][1])])
    pixel_color_BGR = (image[int(building_info[i][1]), int(building_info[i][0]-building_info[i][2]/2.5)])
    pixel_color = pixel_color_BGR[::-1] # reverse the order of channels, making it RGB
    building_info[i].append(pixel_color)
    print(pixel_color)
    print(closest_color(pixel_color))

#Create simplified robot output array
robot_output = []
for i in building_info:
    robot_output.append((int(i[0]), int(i[1]), i[3]))

# create a serial object
ser = serial.Serial('COM5', 9600) # substitute 'COM3' with your Arduino's port
#time.sleep(2)  # give the connection a second or two to establish                 #ENABLE AFTER DEVELOPING

# open text file in write mode to clear it
with open("output.txt", "w") as f:
    pass

# open text file in append mode
with open("output.txt", "a") as f:
    for building in robot_output:
        # convert building info to a comma-separated string
        str_out = ','.join(map(str, building))
        if ser.is_open:
            # encode the string to bytes and send it over serial
            ser.write((str_out + '\n').encode())
            # write the same data to the text file
            f.write(str_out + '\n')
        else:
            print("Serial connection is not open!")

# close the serial connection
ser.close()

print('-------------------------------------------------------------------------------------------------------------\n' + str(building_info) + '\n')
print('-------------------------------------------------------------------------------------------------------------\n' + str(robot_output) + '\n')



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
colors = []
for pos in building_info:
    counter += 1
    x_coord = pos[1] 
    y_coord = pos[0]
    building_height = pos[3]*15
    building_width = pos[2]
    building_length = pos[2]
    
    
    building = pyvista.Cylinder(radius = building_width/2, height= building_height, direction = (0,0,1), center=(x_coord,y_coord, building_height/2))
    
    color = pos[4]
    normalized_color = tuple([c/255 for c in color])  # normalize color values

    # Add the building to the plotter with its color
    plotter.add_mesh(building, color=normalized_color, show_edges=True, line_width=1, smooth_shading= True, show_scalar_bar=False)
    
    label_text = f"Building {counter}: \n({int(y_coord)}, {int(x_coord)}), \nH: {pos[3]}"
    labels.append((label_text))
    points.append((x_coord-building_width/6, y_coord+building_length/6, building_height*1.5))

    line = pyvista.Line(pointa=(x_coord, y_coord, building_height), pointb=(x_coord-building_width/6, y_coord+building_length/6, building_height*1.5), resolution=1)
    plotter.add_mesh(line, show_scalar_bar=False)




merged = map.merge(modelBuildings)
# merged.rotate_x(270)
# merged.rotate_y(270)
# merged.rotate_z(270)






actor = plotter.add_point_labels(points,labels,italic=False,font_size=10,point_color='red',point_size=1,render_points_as_spheres=True,always_visible=True,shadow=True)
#plotter.camera_position = 'iso'

plotter.enable_anti_aliasing('ssaa')
_ = plotter.add_axes(line_width=5, labels_off=True)
plotter.add_mesh(merged, show_edges=True, line_width=1, smooth_shading= True, show_scalar_bar=False)
plotter.show_grid()


print('\nChoose 3D Visualization Type: \n1- Freeview \n2- Rotation GIF (This takes around 30 seconds to render)')
userchoice = input()
if userchoice == '1':
    plotter.show(auto_close= True)
if userchoice == '2':
    # Open a gif
    plotter.open_gif("rotation.gif", fps=20)
    # Determine the center of your map for the camera to orbit
    orbit_center = map.center
    # Define a vector for the camera position. This will be updated in the loop.
    orbit_radius = 2*max(image.shape[0], image.shape[1])  # use the larger dimension of the image as the orbit radius
    camera_position = [orbit_center[0], orbit_center[1], orbit_center[2] + orbit_radius * np.sqrt(2) / 2]
    # Define the number of frames
    nframe = 360  # 36 frames will result in 10 degrees per frame
    # Rotate the camera and write a frame for each updated position
    for i in range(nframe):
        plotter.camera_position = [camera_position, orbit_center, [0, 0, 1]]  # sets camera position, focal point, and view up
        plotter.render()  # render the scene
        plotter.write_frame()  # write the frame
        # Update the camera position for the next frame. This creates a 10 degree rotation per frame.
        camera_position = [orbit_center[0] + orbit_radius * np.sin(np.radians(i * 1)), 
                    orbit_center[1] - orbit_radius * np.cos(np.radians(i * 1)), 
                    orbit_center[2] + orbit_radius * np.sqrt(2) / 2]
    # Close and finalize the gif
    plotter.close()
