from AI.ai_utils import angle_between, unit_vector
import numpy as np
from typing import Any, List, Tuple
import math

class PlayerSimulator:
    def __init__(self, alpha: float, sigma: float):
        self.alpha = alpha
        self.sigma = sigma


        self.boundary_vector = unit_vector(np.array([-math.sin(math.radians(alpha)), math.cos(math.radians(alpha))]))

    
    def predict(self, trial: List[Any]) -> Tuple[bool, float]:
        #print(trial)
        nd_coord = trial[6]
        nnd_coord = trial[7]
        
        #sharpening effect: add random noise
        #nd_coord += np.random.normal(scale=self.sigma)
        #nnd_coord += np.random.normal(scale=self.sigma)

        trial_vec = unit_vector(np.array([nd_coord, nnd_coord]))

        if nnd_coord*nd_coord >0:
            #congruent even after noise
            return True, 2.0
        elif nnd_coord > 0:
            #incongruent, 4th quadrant
            return np.all((trial_vec>(-self.boundary_vector))), 2.0
        else:
            #incongruent, 2nd quadrant
            return np.all((trial_vec>self.boundary_vector)), 2.0

