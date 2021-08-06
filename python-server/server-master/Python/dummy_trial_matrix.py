# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 19:25:07 2021

@author: Client
"""

import random
import math
from dummy_client_handler import GameDummy

trials_matrix = []
correct = []

def generate_random_trial_matrix():
    
    trials_matrix = []
    n = 20
    
    for i in range (n):
        ratio = round (random.uniform(0.2,2), 1)
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
        answer = GameDummy(trials_matrix)
        correct.append (answer)
        
    return trials_matrix