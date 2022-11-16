from AI.ai_utils import angle_between, unit_vector, vcol
import numpy as np
from typing import Any, List, Tuple
import math

class PlayerSimulator:
    def __init__(self, alpha: float, sigma: float, add_decision_noise: bool = False, add_time_noise: bool = False):
        self.alpha = alpha
        self.sigma = sigma
        self.add_decision_noise = add_decision_noise
        self.add_time_noise = add_time_noise

        self.boundary_vector = unit_vector(np.array([-math.sin(math.radians(alpha)), math.cos(math.radians(alpha))]))

        #basis in the decision boundary space
        self.transform_mat =np.linalg.inv(np.array([[self.boundary_vector[0], self.boundary_vector[1]], [self.boundary_vector[1], -self.boundary_vector[0]]]))
                
    
    def predict(self, trial: List[Any]) -> Tuple[bool, float]:
        #print(trial)
        nd_coord = trial[8]
        nnd_coord = trial[9]

        is_right = nd_coord > 0
        #sharpening effect: add random noise
        nd_coord += np.random.normal(scale=self.sigma)
        nnd_coord += np.random.normal(scale=self.sigma)

        trial_vec = np.array([nd_coord, nnd_coord])

        
        #transform vector in the decision space
        trial_vec = np.dot(self.transform_mat, vcol(trial_vec))

        decision_score = float(trial_vec[1])

        decision_score += np.random.normal(scale=0.1) if self.add_decision_noise else 0.0

        looks_right = decision_score > 0

        #print(f"nd: {nd_coord} - nnd: {nnd_coord} - tv: {trial_vec} - b: {self.transform_mat}")

        response_time = self.get_response_time(decision_score)

        return bool(looks_right == is_right), response_time


    def get_response_time(self, decision_score: float) -> float:
        """
            Concept (idea): the perceived difficulty is related to the distance of the trial with respect to the 
                            decision boundary in the nd-nnd space
                            the higher the distance, the lower the perceived difficulty

            result: we can module the response time according to this perceived difficulty

            possible improvements:  take into account features with higher dimensionality from the trial instead of the nd and nnd variable
                                    (i.e. the actual magnitude of the number between the two fences)
                                    make the calculation more realistic (how? maybe with some real data it could be done)

                                    
        """
        perceived_difficulty = np.clip(1/np.abs(decision_score), a_max = 5, a_min = 0.2)

        
        response_time = 2*perceived_difficulty
        response_time += np.random.normal(scale= 1.0) if self.add_time_noise else 0.0

        
        return response_time