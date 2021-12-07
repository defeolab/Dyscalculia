# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 13:40:28 2021

@author: oyekp
"""
# import random
# import math
from trial_util import convert_matrix_to_trials



def PlayGame (self, trials_matrix):
    # trials_matrix = [[1.7, 1.3, 1.0, 1.0, 2, 9, 1]]
    #                 , [1.3, 1.9, 1.6, 0.8, 4, 9, 0], [1.8, 1.0, 1.5, 0.8, 5, 9, 1], [1.3, 1.8, 0.6, 1.0, 4, 10, 1], [1.5, 1.7, 1.7, 1.0, 5, 9, 0], [1.8, 1.7, 0.7, 0.8, 4, 10, 1], [1.3, 1.0, 1.3, 0.8, 4, 9, 1], [1.6, 1.6, 1.6, 0.8, 3, 9, 1], [1.9, 1.7, 0.9, 1.0, 4, 9, 1], [1.4, 1.3, 1.3, 0.8, 4, 10, 0], [1.4, 1.3, 0.7, 0.8, 3, 9, 1], [1.5, 1.6, 2.0, 0.8, 3, 9, 1], [1.9, 1.6, 1.0, 1.0, 2, 9, 1], [1.6, 1.0, 0.6, 0.8, 3, 10, 1], [1.2, 1.3, 1.1, 0.8, 2, 9, 1], [1.2, 1.2, 0.7, 0.8, 5, 10, 1], [1.3, 1.1, 1.4, 1.0, 4, 8, 1], [1.6, 1.6, 2.0, 1.0, 4, 9, 1], [1.9, 1.1, 1.4, 1.0, 3, 9, 1], [1.2, 1.5, 1.6, 1.0, 4, 9, 0]]
    # trials_matrix = []
    # n = 10
    # for i in range (n):
    #       ratio = round (random.uniform(1,2), 1)
    #       average_space_between = round (random.uniform(1,2), 1)
    #       size_of_chicken = round (random.uniform(0.5,2), 1)
    #       total_area_occupied = round (random.uniform(2,3))
    #       circle_radius = round (math.sqrt(total_area_occupied / math.pi), 1)
    #       chicken_show_time = round (random.uniform(2,5))
    #       max_trial_time = round (random.uniform(8,10))
    #       ratio_area = round (random.randint(0, 1))

    #       trials_list = []
    
    #       trials_list.append(ratio)
    #       trials_list.append(average_space_between)
    #       trials_list.append(size_of_chicken)
    #       trials_list.append(circle_radius)
    #       trials_list.append(chicken_show_time)
    #       trials_list.append(max_trial_time)
    #       trials_list.append(ratio_area)
     
    #       trials_matrix.append(trials_list)
    #       #print (trials_matrix)
     
    return convert_matrix_to_trials(trials_matrix) 