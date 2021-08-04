# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 21:45:20 2021

@author: oyekp
"""

import random
import math
import pandas as pd
from dummy import GameDummy
import matplotlib.pyplot as plt 

trials_matrix = []
correct = []
n = 10

n_1 = []
d = []
c = []

tmp = 0
tmp1 = 0
tmp2 = 0
tmp3 = 0

my_colors = {0:'red', 1:'green'}

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
    #print(correct)

for i in range(0, len(trials_matrix)):
    trials_matrix[i].append(correct[i])
    
# print(trials_matrix)

trials_table = pd.DataFrame (trials_matrix)
trials_table.columns = ["area_1_circle_radius", "area_1_size_of_chicken",
                        "area_1_average_space_between", "area_1_number_of_chickens", 
                        "area_2_circle_radius", "area_2_size_of_chicken", 
                        "area_2_average_space_between", "area_2_number_of_chickens", 
                        "ratio", "correct"]
# print (trials_table)    

n = []
d = []
c = []

my_colors = {0:'red',1:'green'}

for results in trials_matrix:
    n.append(math.log(results[7]/results[3]))
    d.append(math.log(results[5]/results[1]))
    c.append(results[9])

    
for i in range (len(n)):
    plt.scatter(n[i] , d[i], color = my_colors.get(c[i]))
   
plt.ylabel('log(d2/d1)')
plt.xlabel('log(n2/n1)')
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.grid(True)
       
ax = plt.gca()
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')

plt.show()   