from AI.SimpleEvaluator import PlayerEvaluator
from AI.ai_utils import unit_vector
from typing import Any

from AI.TrialAdapter import TrialAdapter
from typing import List, Any

import numpy as np
import math

class PAD_Evaluator(PlayerEvaluator):
    """
        Perceived-Actual-Difficulty Evaluator: 
            This evaluator aims at estimating the ability of the player (in terms of 
            filtering and sharpening parameters) and at proposing trials based on 
            their perceived difficulty and their actual difficulty given the estimated player.

            Perceived difficulty:
                It is an estimated measure of how hard it is for the player to give an answer to
                the current trial, regardless of the correctness of the response. For now,
                this is a measure related to the distance of the current trial from the player's
                decision boundary in the nd-nnd space

            Actual difficulty:
                The probability that the player gives an incorrect answer for the problem given
                the estimated filtering and sharpening parameters  
    """


    def __init__(self, init_alpha: float, init_sigma: float, init_prob: float = 0.05, init_perceived_diff: float = 0.2):
        self.trial_adapter = TrialAdapter(False, True)
        self.alpha = init_alpha
        self.sigma = init_sigma
        self.target_error_prob = init_prob
        self.target_perceived_diff = init_perceived_diff

        self.boundary_vector = unit_vector(np.array([-math.sin(math.radians(self.alpha)), math.cos(math.radians(self.alpha))]))

        #basis in the decision boundary space
        self.transform_mat =np.linalg.inv(np.array([[self.boundary_vector[0], self.boundary_vector[1]], [self.boundary_vector[1], -self.boundary_vector[0]]]))

    
    def get_stats(self) -> Any:
        return f"alpha: {self.alpha}, sigma: {self.sigma}"
    
    def get_trial(self) -> List[Any]:
        """
            After the current sharpening and filtering ability of the player has been estimated,
            the aim of the evaluator is to propose trials with an estimated probability of error as
            similar as possible to the target_error_prob while also having a similar perceived difficulty
            to the target one (for now, as low as possible).
            This is meant to support the growth of mathematical skills of the child
        """

        



        return super().get_trial()
    
    def update_statistics(self) -> None:
        return super().update_statistics()

if __name__ == "__main__":
    ev = PAD_Evaluator()