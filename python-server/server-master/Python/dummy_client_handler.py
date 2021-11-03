# -*- coding: utf-8 -*-
"""
Created on Fri Jul 30 21:25:36 2021

@author: oyekp
"""
import numpy as np
import matplotlib.pyplot as plt
from color_toss import ColorToss, UniformOutput
import math
     
class DummyClientHandler():
    
    def __init__ (self, connection, db, player_id, trials_matrix):
        self.trials_matrix = trials_matrix
    
    def Run(self, trials_matrix, indicator):
        response_vector = []
        
        for i in range (len(trials_matrix)):

            answer = self.Correct(self.trials_matrix)
            response_vector.append (answer)

        self.GenerateDataframe(response_vector)
        # self.SharpeningAnalysis(self.trials_matrix, indicator)
        self.FilteringAnalysis(self.trials_matrix, indicator)
        
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
        #       "correct"]        
    
    def SharpeningAnalysis (self, trials_matrix, indicator):
        nv = []  # nv --> NUMERICAL VARIABLE
        nnv = []  # nnv --> NON-NUMERICAL VARIABLE
        c = []
        
        mu = 0
        sigma = 1   # capacità di discriminare del bambino (effetto sharpening)
                    # più il bimbo è grande, migliore sarà la sua capacità di 
                    # discriminare
        
        my_colors = {0:'green', 1:'red'}
        
        for results in trials_matrix:
            nv.append(np.log10(results[7]/results[3])) #number_of_chickens
            if indicator == 1:
                nnv.append(np.log10(results[4]/results[0])) #circle_radius
            elif indicator == 2:
                nnv.append(np.log10(results[5]/results[1])) #size_of_chicken
            else:
                nnv.append(np.log10(results[6]/results[2])) #average_space_between
            c.append(results[8])
        
        # This was just to verify that I could obtain x^4
        # print("LUNGHEZZA VETTORE A")
        # print(len(nv))
        # print("LUNGHEZZA VETTORE D")
        # print(len(nnv))
            
        for i in range (len(nv)):
            # ColorToss takes the values that define the Gaussian curve
            # alongside the nv[i] (i-th numerical value), returning a 
            # probability value. Depending on that probability, we
            # decide how to color the points
            uniform_output = UniformOutput()
            gaussian_threshold = ColorToss(mu, sigma, nv[i])
            # gaussian_threshold va da 0 e 0.5
            
            # -1 probab = 0.1, a 0 varrà 0.5, mai 1
            # asse y metà pallini rossi metà verdi,
            # ai lati dovrebbero essere tutti verdi
            
            # if (uniform_output > gaussian_threshold):
            # colore rosso (col_res = rosso)
            # else colore verde
            if(uniform_output > gaussian_threshold):
                col_res = 0
            else:
                col_res = 1
            
            plt.scatter(nv[i], nnv[i], color = my_colors.get(col_res))
                  
        plt.xlim([-1, 1])
        plt.ylim([-1, 1])
        plt.grid(True)
        plt.title("Sharpening Effect")
       
        ax = plt.gca()
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
    
        plt.show()
        
    def FilteringAnalysis (self, trials_matrix, indicator):
        
        nv = []  # nv --> NUMERICAL VARIABLE
        nnv = []  # nnv --> NON-NUMERICAL VARIABLE
        c = []
        
        fig = plt.figure()
        alpha = 30              # alpha is the angle in degrees
        alpha = alpha + 90
        rad_alpha = np.deg2rad(alpha)   # converted in radiants
        coeff = math.tan(rad_alpha) 
        ax = fig.add_subplot(1, 1, 1)
        x = np.linspace(-5,5,100)
        
        my_colors = {0:'green', 1:'red', 2: 'green'}
        
        for results in trials_matrix:
            nv.append(np.log10(results[7]/results[3])) #number_of_chickens
            if indicator == 1:
                nnv.append(np.log10(results[4]/results[0])) #circle_radius
            elif indicator == 2:
                nnv.append(np.log10(results[5]/results[1])) #size_of_chicken
            else:
                nnv.append(np.log10(results[6]/results[2])) #average_space_between
            c.append(results[8])
            
        for i in range (len(nv)):
            if((nnv[i] - (coeff * nv[i])) == 0):
                plt.scatter(nv[i], nnv[i], color = my_colors.get(2))
            elif( ((nnv[i] - (coeff * nv[i]) > 0) and (( (nnv[i] > 0) and (nv[i] < 0) ))) 
                 or ((nnv[i] - (coeff * nv[i]) < 0) and (( (nnv[i] < 0) and (nv[i] > 0) ))) 
                 or (nv[i] == 0)):
                plt.scatter(nv[i], nnv[i], color = my_colors.get(1))
            else:
                plt.scatter(nv[i], nnv[i], color = my_colors.get(0))
        
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        
        plt.plot(x, coeff*x, '-y')
        
        plt.xlim([-1, 1])
        plt.ylim([-1, 1])
        plt.grid(True)
        
        plt.title("Filtering Effect")
        
        plt.show()