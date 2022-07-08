import math
from cv2 import pointPolygonTest
import numpy as np

def diff_coef(x, y):
    k = math.atan(y/x)
    # print(k)
    limit = (math.pi)/4
    # print(limit)
    if (x > 0 and y >= 0) or (x < 0 and y <= 0):
        if k >= limit:
            # print(1.1)
            return k - limit
        else:
            # print(1.2)
            return limit - k
    elif (x < 0 and y > 0) or (x > 0 and y < 0):
        if abs(k) >= limit:
            # print(2.1)
            return k + limit
        else:
            # print(2.2)
            return -limit - k

circle_points = np.arange(0,2*math.pi,2*math.pi/16)
# print(circle_points)
radius = float(input("Input radio of circle: "))

for angle in circle_points:
    x, y = radius*math.cos(angle), radius*math.sin(angle)
    if x < 0.001 and x > -0.001:
        x = 0
    if y < 0.001 and y > -0.001:
        y = 0
    if x == 0.0: 
        print("angle: {}\t x: {}\t\t / y: {}\t / COMBINATION NOT POSSIBLE ".format(round(angle,2), round(x,3), round(y,3)))
    # print("x: {}\t - y: {}\t - coefficient: {}".format(x, y, diff_coef(x, y)))
    else: 
        print("angle: {}\t x: {}\t / y: {}\t / coefficient: {}".format(round(angle,2), round(x,3), round(y,3), round(diff_coef(x, y), 4)))