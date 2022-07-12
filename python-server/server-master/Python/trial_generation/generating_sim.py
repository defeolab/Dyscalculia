import random
import math
from turtle import left
import numpy as np

class Chicken() :
    def __init__(self, pos, size) -> None:
        self.pos = pos
        self.size = size
        self.center = (pos[0] - size/2, pos[1] - size/2)
    
def check_pos_validity(pos,  colle, chicken_size, radius, center) :
    chicken_center = pos + chicken_size/2

    # Check if chicken does not fall outside of 
    if (np.linalg.norm(chicken_center - center)) > radius - 20 - chicken_size/2 : return False

    # Check if chicken does not hit any other chicken
    for exists in colle:
        exists_center = exists + chicken_size/2
        if ((np.linalg.norm(chicken_center - exists_center)) < chicken_size+1) :
            return False
    
    return True


def generate_positions(radius, center1, center2, difficulty, max_chickens = 40) :

    # Computing a number of chickens to be consistent with difficulty
    first_choice = random.randint(2, max_chickens)
    second_choice = int(first_choice/difficulty)

    # Computing maximum chicken size
    field_area = math.pi * (radius)**2
    max_chicken_size = field_area/max(first_choice, second_choice)
    max_chicken_size = int(math.sqrt(max_chicken_size/math.pi)) 

    
    chicken_size = random.randrange(10, max_chicken_size)
    # Computing valid random positions
    first_positions = []
    second_positions = []

    if random.random() > 0.5 :
        first_choice, second_choice = second_choice, first_choice

    for chicken in range(first_choice) :
        pos = np.array((random.randint(center1[0] - radius, center1[0] + radius), random.randint(center1[1] - radius, center1[1] + radius)))
        while(not check_pos_validity(pos, first_positions, chicken_size, radius, center1)):
            pos = np.array((random.randint(center1[0] - radius, center1[0] + radius), random.randint(center1[1] - radius, center1[1] + radius)))
        first_positions.append(pos)


    for chicken in range(second_choice) :
        pos = np.array((random.randint(center2[0] - radius, center2[0] + radius), random.randint(center2[1] - radius, center2[1] + radius)))
        while(not check_pos_validity(pos, second_positions, chicken_size, radius, center2)):
            pos = np.array((random.randint(center2[0] - radius, center2[0] + radius), random.randint(center2[1] - radius, center2[1] + radius)))
        second_positions.append(pos)

    
    # if random.random() > 0.5 :
    #     return first_choice, second_choice
    
    # else :
    #     return second_choice, first_choice
    return first_positions, second_positions, chicken_size