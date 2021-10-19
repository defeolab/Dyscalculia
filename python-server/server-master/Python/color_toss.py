# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 19:30:19 2021

@author: Client
"""

import numpy as np

def ColorToss(probability):
    # perform the binomial distribution (return 0 or 1)
    result = np.random.binomial(1, probability)
    
    # return flip to be added to numpy array
    return result