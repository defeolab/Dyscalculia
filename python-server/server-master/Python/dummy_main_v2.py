# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 21:45:20 2021

@author: oyekp
"""

import random
import math
import pandas as pd
from dummy import GameDummy
import numpy as np
#import matplotlib.pyplot as plt 

trials_matrix = []
correct = []
n = 10
for i in range (n):
    ratio = round (random.uniform(0,2), 1)
    average_space_between = round (random.uniform(1,2), 1)
    size_of_chicken = round (random.uniform(0.5,2), 1)
    total_area_occupied = round (random.uniform(2,3))
    circle_radius = round (math.sqrt(total_area_occupied / math.pi), 1)
    number_of_chickens = random.randint(2, 8)
    number_of_chickens2 = round (int(number_of_chickens * ratio))

    trials_list1 = []
    answer = []
    
    trials_list1.append(circle_radius)
    trials_list1.append(size_of_chicken)
    trials_list1.append(average_space_between)
    
    trials_list2 = [i * ratio for i in trials_list1]
    trials_list1.append(number_of_chickens)
    trials_list1.extend(trials_list2)
    trials_list1.append(number_of_chickens2)
    trials_list1.append(ratio)
     
    trials_matrix.append(trials_list1)
    for i in range (0, len(trials_matrix)):
        answer = np.random.randint(2)
    # answer = GameDummy(trials_matrix)
    correct.append (answer)

trials_table = pd.DataFrame (trials_matrix)
trials_table.columns = ["area_1_circle_radius", "area_1_size_of_chicken","area_1_average_space_between", "area_1_number_of_chickens", "area_2_circle_radius", "area_2_size_of_chicken", "area_2_average_space_between", "area_1_number_of_chickens", "ratio"]
trials_table.loc[:,'correct'] = correct
print (trials_table)    
    