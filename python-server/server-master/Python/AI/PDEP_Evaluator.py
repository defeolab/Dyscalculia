from AI.SimpleEvaluator import PlayerEvaluator
from AI.ai_utils import unit_vector, PDEP_find_trial
from typing import Any

from AI.TrialAdapter import TrialAdapter
from typing import List, Any

import numpy as np
import math

class PDEP_Evaluator(PlayerEvaluator):
    """
        Perceived-Difficulty-Error-Probability Evaluator: 
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


    def __init__(self, init_alpha: float, init_sigma: float, init_prob: float = 0.30, init_perceived_diff: float = 0.1, norm_feats: bool=True, update_step: int=5, mock: bool = True):
        self.trial_adapter = TrialAdapter(mock,True, norm_feats)
        self.alpha = init_alpha
        self.sigma = init_sigma
        self.target_error_prob = init_prob
        self.target_perceived_diff = init_perceived_diff
        self.norm_feats = norm_feats

        self.mode = "support"

        self.boundary_vector = unit_vector(np.array([-math.sin(math.radians(self.alpha)), math.cos(math.radians(self.alpha))]))

        #basis in the decision boundary space
        self.transform_mat =np.linalg.inv(np.array([[self.boundary_vector[0], self.boundary_vector[1]], [self.boundary_vector[1], -self.boundary_vector[0]]]))

        #variables used during update phase
        self.iteration = 0
        self.update_step = update_step
        self.history = np.array(([False for i in range(0, update_step)])) 

    def get_stats(self) -> Any:
        return self.target_error_prob, self.target_perceived_diff
    
    def get_main_stat(self) -> Any:
        return self.target_error_prob

    def get_stats_as_str(self) -> str:
        return f"alpha: {self.alpha}, sigma: {self.sigma}"

    def plot_stats(self, day: int):
        def func(plt):
            plt.title(f"Day {day}, error prob {round(self.target_error_prob,2)}")

        return func
    
    def get_info_as_string(self) -> str:
        return f"lv - {round(self.last_value,2)}"
    
    def get_trial(self) -> List[Any]:
        """
            After the current sharpening and filtering ability of the player has been estimated,
            the aim of the evaluator is to propose trials with an estimated probability of error as
            similar as possible to the target_error_prob while also having a similar perceived difficulty
            to the target one (for now, as low as possible).
            This is meant to support the growth of mathematical skills of the child
        """

        nd_variable, nnd_variable, self.last_value = PDEP_find_trial(self.target_error_prob,self.target_perceived_diff, self.transform_mat, self.boundary_vector, self.sigma, self.norm_feats)

        trial = self.trial_adapter.find_trial(nd_variable, nnd_variable)

        return trial
    
    def update_statistics(self, correct: bool, decision_time: float) -> None:
        """
            update the target error probability and the target perceived difficulty according to the response from the last trial

            for now just increase/decrease probability
        """

        self.iteration+=1
        self.history[self.iteration%self.update_step] = correct

        if self.iteration%self.update_step == 0:
            #after a set number of trials, check the accuracy
            avg = np.average(self.history)
            print(f"avg was {avg}")

            #if accuracy was lower than expected, lower target error prob
            self.target_error_prob += 0.05 if avg>self.target_error_prob else -0.05

            #eliminate the 0.5 error probability as its perceived difficulty is too high (trials exactly on decision boundary)
            if np.abs(self.target_error_prob-0.5) <0.02:
                print("wut")
                self.target_error_prob = 0.55 if avg> 0.5 else 0.45


if __name__ == "__main__":
    ev = PDEP_Evaluator(0.1,0.1)