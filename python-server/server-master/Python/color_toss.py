# import numpy as np
import scipy.stats as stats
import random

def UniformOutput():
    # perform the binomial distribution (return 0 or 1)
    # uniform_output = np.random.binomial(1, probability)
    uniform_output = random.uniform(0, 1)
    
    # return flip to be added to numpy array
    return uniform_output

def ColorToss(mu, sigma, nv):
    # Funzione threshold (da cominciare con la retta, poi 
    # poi sostituire con la gaussiana)
    # perform the Gaussian distribution
    res = 0.25 * stats.norm(mu, sigma).pdf(nv)
    
    # return flip to be added to numpy array
    return res