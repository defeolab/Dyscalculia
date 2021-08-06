# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 21:25:36 2021

@author: oyekp
"""
import numpy as np
import pandas as pd
import random
import math
import matplotlib.pyplot as plt

def generate_random_trial_matrix(n):
    trials_matrix = []
    for i in range (n):
        ratio = round (random.uniform(0.2,2), 1)
        average_space_between = round (random.uniform(1,2), 1)
        size_of_chicken = round (random.uniform(0.5,2), 1)
        total_area_occupied = round (random.uniform(2,3))
        circle_radius = round (math.sqrt(total_area_occupied / math.pi), 1)
        number_of_chickens = random.randint(2, 8)
        number_of_chickens2 = round (int(number_of_chickens * ratio))
    
        trials_list1 = []
        
        trials_list1.append(circle_radius)
        trials_list1.append(size_of_chicken)
        trials_list1.append(average_space_between)
        
        trials_list2 = [i * ratio for i in trials_list1]
        trials_list1.append(number_of_chickens)
        trials_list1.extend(trials_list2)
        trials_list1.append(number_of_chickens2)
        trials_list1.append(ratio)
     
        trials_matrix.append(trials_list1)
    return trials_matrix
            
class DummyClientHandler():
    
    def __init__ (self, trials_matrix):
        self.trials_matrix = trials_matrix
    
    def Run(self, n):
        results_array = []
        for i in range (n):
            answer = self.Correct(self.trials_matrix)
            results_array.append (answer)
        print ('Result Array: ' + str(results_array))
        Dataframe = self.GenerateDataframe(results_array)
        print (Dataframe)
        return self.Analysis(self.trials_matrix)
    
    def Correct(self, trials_matrix):
        for i in range (0, len(self.trials_matrix)):
            return (np.random.randint(2))
    
        
    def GenerateDataframe(self, results_array):
        for i in range(0, len(self.trials_matrix)):
            self.trials_matrix[i].append(results_array[i])
    
            trials_table = pd.DataFrame (self.trials_matrix)
            trials_table.columns = ["area_1_circle_radius", "area_1_size_of_chicken",
                            "area_1_average_space_between", "area_1_number_of_chickens", 
                            "area_2_circle_radius", "area_2_size_of_chicken", 
                            "area_2_average_space_between", "area_2_number_of_chickens", 
                            "ratio", "correct"]
        print (trials_table)   
    
    def Analysis (self, trials_matrix):
        a = []
        d = []
        c = []
        
        my_colors = {0:'red',1:'green'}
        for results in trials_matrix:
            a.append(math.log(results[7]/results[3]))
            d.append(math.log(results[5]/results[1]))
            c.append(results[9])
            
        # Plot various projections of the samples.
        for i in range (len(a)):
            plt.scatter(a[i] , d[i], color = my_colors.get(c[i]))   
                  
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
        