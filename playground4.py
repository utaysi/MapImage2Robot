import cv2
import numpy as np

image = cv2.imread('G:\\My Drive\\School\\Spring 2023\\CMP4992 - Capstone\\Project\\Map Images\\asd-7.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to create a binary image
_, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Find contours in the binary image
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize an empty list to store the starting positions of buildings
building_start_positions = []

# Iterate through the contours
for contour in contours:
    # Get the bounding rectangle for the contour
    x, y, w, h = cv2.boundingRect(contour)

    # Append the top-left corner of the bounding rectangle to the list
    building_start_positions.append((x, y))

# Print the starting positions of buildings
print(building_start_positions)
