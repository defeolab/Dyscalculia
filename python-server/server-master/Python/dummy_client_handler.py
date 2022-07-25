import numpy as np
from distributions import GaussianThreshold, UniformOutput
import math
     
class DummyClientHandler:
    
    def __init__ (self, trials_matrix):
        self.trials_matrix = trials_matrix
    
    def Run(self, trials_matrix, nnd_selector, alpha, sigma):
        response_vector = []
        
        response_vector = self.ChildSimulator(self.trials_matrix, nnd_selector
                                              , alpha, sigma, mu = 0) 
        
        for i in range(len(trials_matrix)):
            trials_matrix[i].append(response_vector[i])
        
        return response_vector

    def diff_coef_filtering(x, y):
        if (x > 0 and y >= 0) or (x < 0 and y <= 0):
            k = math.degrees(math.atan(y/x))
        elif (x < 0 and y > 0) or (x > 0 and y < 0):
            k = math.pi - abs(math.atan(y/x))
        a = math.degrees(abs((math.pi/4)-k))
        return a

# ChildSimulator evaluates each trial in the trials matrix, applies Filtering or
# Sharpening effect or both, depending on the values of alpha and sigma passed as 
# parameter, and RETURNS a vector that contains, for each trial, if that trial is
# correct or incorrect
    def ChildSimulator(self, trials_matrix, nnd_selector, alpha, sigma, mu):        
        nv = []  # nv --> NUMERICAL VARIABLE
        nnv = []  # nnv --> NON-NUMERICAL VARIABLE
        correct_vector = [] # records if the specific trial has been correct or not
        
        added_alpha = alpha + 90
        rad_alpha = np.deg2rad(added_alpha)   # converted in radiants
        coeff = math.tan(rad_alpha)
        
        for results in trials_matrix:
            nv.append(np.log10(results[1]/results[0]))      # number_of_chickens
            if nnd_selector == 1:
                nnv.append(np.log10(results[3]/results[2])) # field_area
            elif nnd_selector == 2:
                nnv.append(np.log10(results[5]/results[4])) # item_surface_area
                
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