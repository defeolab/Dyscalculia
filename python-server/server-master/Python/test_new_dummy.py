# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 16:42:47 2021

@author: Client
"""

# Prova dummy client con i cambi logici miei

import numpy as np
import matplotlib.pyplot as plt
from color_toss import ColorToss, UniformOutput
import math
     
class DummyClientHandlerNew():
    
    # MODIFICHE FATTE QUA RISPETTO A PRIMA
    
    # 1. Rimozione della chiamata alla funzione 'Correct'. Inutile, perchè correct determinava
    # la correttezza o meno del trial ma in modo randomico, quindi completamente scollegato
    # rispetto al sistema dei colori sviluppato nelle funzioni di Sharpening e Filtering
    
    # 2. Rimozione della chiamata a GenerateDataFrame. Inutile anche quella, in quanto 
    # non genera più alcun dataframe, ma semplicemente faceva l'append del response vector
    # alla trials matrix, cosa che si puà agilmente fare nella funzione Run direttamente.
    
    def __init__ (self, connection, db, player_id, trials_matrix):
        self.trials_matrix = trials_matrix
    
    def Run(self, trials_matrix, indicator):
        response_vector = []
        
        # Valori scelti per SIGMA: 0, 0.1, 0.2, 0.3
        # Valori scelti per ALPHA: 15, 30, 45
        
        # response_vector = self.SharpeningAnalysis(self.trials_matrix, indicator, 
        # mu = 0, sigma = 0.4)
        # response_vector = self.FilteringAnalysis(self.trials_matrix, indicator, alpha = 45)
        response_vector = self.Analysis(self.trials_matrix, indicator, alpha = 45, mu = 0, sigma = 0.3)
        
        for i in range(len(trials_matrix)):
            trials_matrix[i].append(response_vector[i])
        
        return response_vector
    
    def SharpeningAnalysis (self, trials_matrix, indicator, mu, sigma):
        nv = []  # nv --> NUMERICAL VARIABLE
        nnv = []  # nnv --> NON-NUMERICAL VARIABLE
        c = []
        
        my_colors = {0:'green', 1:'red'}
        
        for results in trials_matrix:
            nv.append(np.log10(results[7]/results[3])) #number_of_chickens
            if indicator == 1:
                nnv.append(np.log10(results[4]/results[0])) #circle_radius
            elif indicator == 2:
                nnv.append(np.log10(results[5]/results[1])) #size_of_chicken
            else:
                nnv.append(np.log10(results[6]/results[2])) #average_space_between
            # c.append(results[8])
            
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
                c.append(col_res)
            else:
                col_res = 1
                c.append(col_res)
            
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
        return c
        
    def FilteringAnalysis (self, trials_matrix, indicator, alpha):
        
        nv = []  # nv --> NUMERICAL VARIABLE
        nnv = []  # nnv --> NON-NUMERICAL VARIABLE
        c = []
        
        fig = plt.figure()
        added_alpha = alpha + 90
        rad_alpha = np.deg2rad(added_alpha)   # converted in radiants
        coeff = math.tan(rad_alpha) 
        ax = fig.add_subplot(1, 1, 1)
        x = np.linspace(-5, 5, 100)
        
        my_colors = {0: 'green', 1: 'red', 2: 'blue'}
        
        for results in trials_matrix:
            nv.append(np.log10(results[7]/results[3])) #number_of_chickens
            if indicator == 1:
                nnv.append(np.log10(results[4]/results[0])) #circle_radius
            elif indicator == 2:
                nnv.append(np.log10(results[5]/results[1])) #size_of_chicken
            else:
                nnv.append(np.log10(results[6]/results[2])) #average_space_between
            # c.append(results[8])
            
        for i in range (len(nv)):
            if((nnv[i] - (coeff * nv[i])) == 0):
                plt.scatter(nv[i], nnv[i], color = my_colors.get(2))
                c.append(2)
            elif( ((nnv[i] - (coeff * nv[i]) > 0) and (( (nnv[i] > 0) and (nv[i] < 0) ))) 
                 or ((nnv[i] - (coeff * nv[i]) < 0) and (( (nnv[i] < 0) and (nv[i] > 0) ))) 
                 ):
                plt.scatter(nv[i], nnv[i], color = my_colors.get(1))
                c.append(1)
            elif(nv[i] == 0):
                c.append(3)
                continue
            else:
                plt.scatter(nv[i], nnv[i], color = my_colors.get(0))
                c.append(0)
        
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
        
        return c
        
    def Analysis (self, trials_matrix, indicator, alpha, mu, sigma):
        # This function is in charge of computing, firstly, 
        # the filtering effect, later the sharpening one only on
        # the trials that have been calssified as correct
        
        nv = []  # nv --> NUMERICAL VARIABLE
        nnv = []  # nnv --> NON-NUMERICAL VARIABLE
        c = []
        
        fig = plt.figure()
        added_alpha = alpha + 90
        rad_alpha = np.deg2rad(added_alpha)   # converted in radiants
        coeff = math.tan(rad_alpha) 
        ax = fig.add_subplot(1, 1, 1)
        x = np.linspace(-5, 5, 100)
        
        my_colors = {0: 'green', 1: 'red', 2: 'blue'}
        
        for results in trials_matrix:
            nv.append(np.log10(results[7]/results[3])) #number_of_chickens
            if indicator == 1:
                nnv.append(np.log10(results[4]/results[0])) #circle_radius
            elif indicator == 2:
                nnv.append(np.log10(results[5]/results[1])) #size_of_chicken
            else:
                nnv.append(np.log10(results[6]/results[2])) #average_space_between
            
        for i in range (len(nv)):
            if (alpha != 0 and sigma != 0):
                # Filtering effect first
                if((nnv[i] - (coeff * nv[i])) == 0):
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(2))
                    c.append(2)
                elif( ((nnv[i] - (coeff * nv[i]) > 0) and (( (nnv[i] > 0) and (nv[i] < 0) ))) 
                     or ((nnv[i] - (coeff * nv[i]) < 0) and (( (nnv[i] < 0) and (nv[i] > 0) ))) 
                     ):
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(1))
                    c.append(1)
                elif(nv[i] == 0):
                    c.append(3)
                    continue
                else:
                    # Sharpening effect here
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
                        c.append(col_res)
                    else:
                        col_res = 1
                        c.append(col_res)
                
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(col_res))
            elif (alpha == 0 and sigma != 0):
                if (nv[i] == 0):
                    c.append(3)
                    continue
                else:
                    # Sharpening effect only
                    uniform_output = UniformOutput()
                    gaussian_threshold = ColorToss(mu, sigma, nv[i])
                    
                    if(uniform_output > gaussian_threshold):
                        col_res = 0
                        c.append(col_res)
                    else:
                        col_res = 1
                        c.append(col_res)
                
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(col_res)) 
                    
            elif(alpha != 0 and sigma == 0):
                # Filtering effect only
                if((nnv[i] - (coeff * nv[i])) == 0):
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(2))
                    c.append(2)
                elif( ((nnv[i] - (coeff * nv[i]) > 0) and (( (nnv[i] > 0) and (nv[i] < 0) ))) 
                     or ((nnv[i] - (coeff * nv[i]) < 0) and (( (nnv[i] < 0) and (nv[i] > 0) ))) 
                     ):
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(1))
                    c.append(1)
                elif(nv[i] == 0):
                    c.append(3)
                    continue
                else:
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(0))
                    c.append(0)
                
            elif(alpha == 0 and sigma == 0):
                if (nv[i] == 0):
                    c.append(3)
                    continue
                else:
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(0)) 
                    c.append(0)
                
        ax.spines['left'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['bottom'].set_position('zero')
        ax.spines['top'].set_color('none')
        
        plt.plot(x, coeff*x, '-y')
        
        plt.xlim([-1, 1])
        plt.ylim([-1, 1])
        plt.grid(True)
        
        plt.title("Filtering + Sharpening Effect")
        
        plt.show()
        print("C: \n")
        print(c)
        return c