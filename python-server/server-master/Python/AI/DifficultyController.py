import numpy as np
from typing import Tuple

class DifficultyController:
    def __init__(self, update_step: int, difficulty: str, init_prob: float, init_perceived_diff) -> None:
        self.update_step = update_step
        self.history = np.array(([False for i in range(0, update_step)]))

        self.memory = 6 if difficulty == "regular" else 14
        self.prob_choice_iteration = 0
        self.prob_history = np.array([3 for i in range(0, self.memory)])
        self.target_probs = np.array([0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9]) if difficulty == "regular" else np.array([0.1, 0.1, 0.1, 0.1,0.1, 0.2, 0.2, 0.2,0.2,0.2, 0.3,0.3, 0.3, 0.4,0.4, 0.6, 0.7, 0.8])
        self.target_error_prob = init_prob
        self.target_perceived_diff = init_perceived_diff
        self.mode = "support"
    
    def get_difficulty_parameters(self)-> Tuple[float, float]:
        return self.target_error_prob, self.target_perceived_diff
    
    def update_difficulty_parameters(self, iteration: int)-> None:
        if iteration%self.update_step == 0:
            self.prob_choice_iteration+=1
            #choose a balanced target error probability based on previously selected ones
            unused_probs_i = []
            for i in range(self.target_probs.shape[0]):
                if i not in self.prob_history:
                    unused_probs_i.append(i)
            unused_probs_i = np.array(unused_probs_i)
            next_prob_i = np.random.choice(unused_probs_i)

            self.prob_history[self.prob_choice_iteration%self.memory] = next_prob_i
            self.target_error_prob = self.target_probs[next_prob_i]