# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 21:25:36 2021

@author: oyekp
"""
import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt

            
class DummyClientHandler():
    
    def __init__ (self, connection, db, player_id, trials_matrix):
        self.trials_matrix = trials_matrix
    
    def Run(self, trials_matrix, indicator):
        response_vector = []
        
        for i in range (len(trials_matrix)):

            answer = self.Correct(self.trials_matrix)
            response_vector.append (answer)

        self.GenerateDataframe(response_vector)
        self.Analysis(self.trials_matrix, indicator)
        
        return response_vector

    
    def Correct(self, trials_matrix):
        for i in range (0, len(self.trials_matrix)):
            return (np.random.randint(2))
    
        
    def GenerateDataframe(self, response_vector):
        for i in range(0, len(self.trials_matrix)):
            self.trials_matrix[i].append(response_vector[i])
        return self.trials_matrix
    
        #     trials_table = pd.DataFrame (self.trials_matrix)
        #     trials_table.columns = [
        #       "area_1_circle_radius", 
        #       "area_1_size_of_chicken",
        #       "area_1_average_space_between", 
        #       "area_1_number_of_chickens", 
        #       "area_2_circle_radius", 
        #       "area_2_size_of_chicken", 
        #       "area_2_average_space_between", 
        #       "area_2_number_of_chickens", 
        #       "ratio", 
        #       "correct"]
        # print (trials_table) 
        # return (trials_table)
    
    def Analysis (self, trials_matrix, indicator):
        a = []
        d = []
        c = []
        
        my_colors = {0:'red',1:'green'}
        
        # indagare meglio su math.log function, per vedere 
        # se è in base 10 o meno
        
        for results in trials_matrix:
            a.append(np.log10(results[7]/results[3])) #number_of_chickens
            if indicator == 1:
                d.append(np.log10(results[4]/results[0])) #circle_radius
            elif indicator == 2:
                d.append(np.log10(results[5]/results[1])) #size_of_chicken
            else:
                d.append(np.log10(results[6]/results[2])) #average_space_between
            c.append(results[9])
        
        # This was just to verify that I could obtain x^4
        print("LUNGHEZZA VETTORE A")
        print(len(a))
        print("LUNGHEZZA VETTORE D")
        print(len(d))
            
        # Plot various projections of the samples.

        for i in range (len(a)):
            plt.scatter(a[i], d[i], color = my_colors.get(c[i]))   

                  
        # plt.ylabel('log(d2/d1)')
        # plt.xlabel('log(n2/n1)')
        plt.xlim([-1, 1])
        plt.ylim([-1, 1])
        plt.grid(True)
       
        ax = plt.gca()
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
               
        plt.show()  