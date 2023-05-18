#Simple script to calculate precise coords for photoshop map generations and corresponding real life coordinates

import math

def get_point_on_circle(center, radius, angle_deg):
    h, k = center  # center of the circle
    angle_rad = math.radians(angle_deg)  # convert angle to radians

    x = h + radius * math.cos(angle_rad)
    y = k + radius * math.sin(angle_rad)

    return (x, y)

# usage example:
center = (75, 75)  # center of the circle
radius = 52.5  # radius of the circle
angle = 185  # angle in degrees

point = get_point_on_circle(center, radius, angle)
photoshop_point = (point[0]*10, point[1]*10)
formatted_point = tuple(int(coord) for coord in point)
formatted_photoshop_point = tuple(int(coord-37) for coord in photoshop_point)

print(formatted_point)
print(formatted_photoshop_point)