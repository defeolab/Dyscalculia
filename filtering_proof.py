import math
from cv2 import pointPolygonTest
import numpy as np

def diff_coef(x, y):
    # Gets K which stands for the angle between the coordinate
    #       and the X axis.
    k = math.atan(y/x)
    # Calculates the limits that define the cuadrants 
    limit = (math.pi)/4
    # Get the difficulty coefficient depending on the cuadrant.
    if (x > 0 and y >= 0) or (x < 0 and y <= 0):
        if k >= limit:
            return k - limit
        else:
            return limit - k
    elif (x < 0 and y > 0) or (x > 0 and y < 0):
        if abs(k) >= limit:
            return k + limit
        else:
            return -limit - k

# Generate the angles that will define the circle points as test coordinates for the 
#       difficulty coefficiente calculation method.
circle_points = np.arange(0,2*math.pi,2*math.pi/16)
# Input the radio of the test circle to calculate the test coordinates.
radius = float(input("Input radio of circle: "))

for angle in circle_points:
    # Generate coordinates
    x, y = radius*math.cos(angle), radius*math.sin(angle)
    # Handle the coordinates that are so close to the axis, that they should be considered
    #       as part of each respective axis.
    if x < 0.001 and x > -0.001:
        x = 0
    if y < 0.001 and y > -0.001:
        y = 0
    # There is no way the numerical variables ratio can be 0 because that would mean that
    #       there is no animals in the corrals. These combinations are deemed not possible.
    if x == 0.0: 
        print("angle: {}\t x: {}\t\t / y: {}\t / COMBINATION NOT POSSIBLE ".format(round(angle,2), round(x,3), round(y,3)))
    # print("x: {}\t - y: {}\t - coefficient: {}".format(x, y, diff_coef(x, y)))
    else: 
        print("angle: {}\t x: {}\t / y: {}\t / coefficient: {}".format(round(angle,2), round(x,3), round(y,3), round(diff_coef(x, y), 4)))