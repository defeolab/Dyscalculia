from AI.ai_utils import angle_between, unit_vector, vcol
import numpy as np
from typing import Any, List, Tuple
import math

class PlayerSimulator:
    def __init__(self, alpha: float, sigma: float):
        self.alpha = alpha
        self.sigma = sigma


        self.boundary_vector = unit_vector(np.array([-math.sin(math.radians(alpha)), math.cos(math.radians(alpha))]))

        #basis in the decision boundary space
        self.transform_mat =np.linalg.inv(np.array([[self.boundary_vector[0], self.boundary_vector[1]], [self.boundary_vector[1], -self.boundary_vector[0]]]))
        

        
    
    def predict(self, trial: List[Any]) -> Tuple[bool, float]:
        #print(trial)
        nd_coord = trial[6]
        nnd_coord = trial[7]

        is_right = nd_coord > 0
        #sharpening effect: add random noise
        nd_coord += np.random.normal(scale=self.sigma)
        nnd_coord += np.random.normal(scale=self.sigma)

        trial_vec = unit_vector(np.array([nd_coord, nnd_coord]))

        
        #transform vector in the decision space
        trial_vec = np.dot(self.transform_mat, vcol(trial_vec))
        looks_right = trial_vec > 0

        #print(f"nd: {nd_coord} - nnd: {nnd_coord} - tv: {trial_vec} - b: {self.transform_mat}")

        return bool(looks_right[1] == is_right), 2.0


