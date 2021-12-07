import numpy as np
import matplotlib.pyplot as plt
from distributions import GaussianThreshold, UniformOutput
import math
     
class DummyClientHandler:
    
    def __init__ (self, trials_matrix):
        self.trials_matrix = trials_matrix
    
    def Run(self, trials_matrix, nnd_selector, alpha):
        response_vector = []
        
        # Chosen values for SIGMA: 0, 0.1, 0.2, 0.3
        # Chosen values for ALPHA: 15, 30, 45
        # response_vector = self.Analysis(self.trials_matrix, nnd_selector, alpha = 30
        #                                 , mu = 0, sigma = 0.3)
        response_vector = self.ChildSimulator(self.trials_matrix, nnd_selector
                                              , alpha, mu = 0, sigma = 0.3)
        
        for i in range(len(trials_matrix)):
            trials_matrix[i].append(response_vector[i])
        
        return response_vector

# ChildSimulator evaluates each trial in the trials matrix, applies Filtering or
# Sharpening effect or both, depending on the values of alpha and sigma passed as 
# parameter, and RETURNS a vector that contains, for each trial, if that trial is
# correct or incorrect
    def ChildSimulator(self, trials_matrix, nnd_selector, alpha, mu, sigma):        
        nv = []  # nv --> NUMERICAL VARIABLE
        nnv = []  # nnv --> NON-NUMERICAL VARIABLE
        correct_vector = []
        
        added_alpha = alpha + 90
        rad_alpha = np.deg2rad(added_alpha)   # converted in radiants
        coeff = math.tan(rad_alpha) 
        
        for results in trials_matrix:
            nv.append(np.log10(results[7]/results[6])) #number_of_chickens
            if nnd_selector == 1:
                nnv.append(np.log10(results[1]/results[0])) #circle_radius
            elif nnd_selector == 2:
                nnv.append(np.log10(results[3]/results[2])) #size_of_chicken
            else:
                nnv.append(np.log10(results[5]/results[4])) #average_space_between
                
        for i in range (len(nv)):
            if (alpha != 0 and sigma != 0):
                # Filtering effect first
                if((nnv[i] - (coeff * nv[i])) == 0):
                    correct_vector.append(1)
                elif( ((nnv[i] - (coeff * nv[i]) > 0) and (( (nnv[i] > 0) and (nv[i] < 0) ))) 
                     or ((nnv[i] - (coeff * nv[i]) < 0) and (( (nnv[i] < 0) and (nv[i] > 0) ))) 
                     ):
                    correct_vector.append(1)
                elif(nv[i] == 0):
                    # No plot
                    correct_vector.append(1)
                    continue
                else:
                    # Sharpening effect here
                    uniform_output = UniformOutput()
                    gaussian_threshold = GaussianThreshold(mu, sigma, nv[i])
                    # gaussian_threshold is between 0 and 0.5
                    
                    # -1 probabability = 0.1, in 0 it is 0.5, never 1
                    # y-axis: half results must be wrong, half correct,
                    # on the edges, results must be mostly correct
                    
                    # if (uniform_output > gaussian_threshold):
                    # colore rosso (col_res = rosso)
                    # else colore verde
                    if(uniform_output > gaussian_threshold):
                        result = 0
                        correct_vector.append(result)
                    else:
                        result = 1
                        correct_vector.append(result)
                
            elif (alpha == 0 and sigma != 0):
                if (nv[i] == 0):
                    # No plot
                    correct_vector.append(1)
                    continue
                else:
                    # Sharpening effect only
                    uniform_output = UniformOutput()
                    gaussian_threshold = GaussianThreshold(mu, sigma, nv[i])
                    
                    if(uniform_output > gaussian_threshold):
                        result = 0
                        correct_vector.append(result)
                    else:
                        result = 1
                        correct_vector.append(result)
                
                    
            elif(alpha != 0 and sigma == 0):
                # Filtering effect only
                if((nnv[i] - (coeff * nv[i])) == 0):
                    correct_vector.append(1)
                elif( ((nnv[i] - (coeff * nv[i]) > 0) and (( (nnv[i] > 0) and (nv[i] < 0) ))) 
                     or ((nnv[i] - (coeff * nv[i]) < 0) and (( (nnv[i] < 0) and (nv[i] > 0) ))) 
                     ):
                    correct_vector.append(1)
                elif(nv[i] == 0):
                    # No plot
                    correct_vector.append(1)
                    continue
                else:
                    correct_vector.append(0)
                
            elif(alpha == 0 and sigma == 0):
                if (nv[i] == 0):
                    # No plot
                    correct_vector.append(1)
                    continue
                else:
                    correct_vector.append(0)
        
        return correct_vector


    
    def Analysis (self, trials_matrix, nnd_selector, alpha, mu, sigma):
        # This function is in charge of computing, firstly, 
        # the filtering effect, later the sharpening one only on
        # the trials that have been classified as correct
        
        nv = []  # nv --> NUMERICAL VARIABLE
        nnv = []  # nnv --> NON-NUMERICAL VARIABLE
        c = []
        
        fig = plt.figure()
        added_alpha = alpha + 90
        rad_alpha = np.deg2rad(added_alpha)   # converted in radiants
        coeff = math.tan(rad_alpha) 
        ax = fig.add_subplot(1, 1, 1)
        x = np.linspace(-5, 5, 100)
        
        my_colors = {0: 'green', 1: 'red'}
        
        for results in trials_matrix:
            nv.append(np.log10(results[7]/results[6])) #number_of_chickens
            if nnd_selector == 1:
                nnv.append(np.log10(results[1]/results[0])) #circle_radius
            elif nnd_selector == 2:
                nnv.append(np.log10(results[3]/results[2])) #size_of_chicken
            else:
                nnv.append(np.log10(results[5]/results[4])) #average_space_between
            
        for i in range (len(nv)):
            if (alpha != 0 and sigma != 0):
                # Filtering effect first
                if((nnv[i] - (coeff * nv[i])) == 0):
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(1))
                    c.append(1)
                elif( ((nnv[i] - (coeff * nv[i]) > 0) and (( (nnv[i] > 0) and (nv[i] < 0) ))) 
                     or ((nnv[i] - (coeff * nv[i]) < 0) and (( (nnv[i] < 0) and (nv[i] > 0) ))) 
                     ):
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(1))
                    c.append(1)
                elif(nv[i] == 0):
                    # No plot
                    c.append(1)
                    continue
                else:
                    # Sharpening effect here
                    uniform_output = UniformOutput()
                    gaussian_threshold = GaussianThreshold(mu, sigma, nv[i])
                    # gaussian_threshold is between 0 and 0.5
                    
                    # -1 probabability = 0.1, in 0 it is 0.5, never 1
                   # y-axis: half results must be wrong, half correct,
                   # on the edges, results must be mostly correct
                    
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
                    # No plot
                    c.append(1)
                    continue
                else:
                    # Sharpening effect only
                    uniform_output = UniformOutput()
                    gaussian_threshold = GaussianThreshold(mu, sigma, nv[i])
                    
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
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(1))
                    c.append(1)
                elif( ((nnv[i] - (coeff * nv[i]) > 0) and (( (nnv[i] > 0) and (nv[i] < 0) ))) 
                     or ((nnv[i] - (coeff * nv[i]) < 0) and (( (nnv[i] < 0) and (nv[i] > 0) ))) 
                     ):
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(1))
                    c.append(1)
                elif(nv[i] == 0):
                    # No plot
                    c.append(1)
                    continue
                else:
                    plt.scatter(nv[i], nnv[i], color = my_colors.get(0))
                    c.append(0)
                
            elif(alpha == 0 and sigma == 0):
                if (nv[i] == 0):
                    # No plot
                    c.append(1)
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
        return c