from AI.SimpleEvaluator import PlayerEvaluator
from AI.ai_utils import unit_vector
from AI.PDEP_functionals import PDEP_find_trial
from typing import Any
from AI.AS_Estimate import ASD_Estimator, ASE_Estimator
from trial_result import TrialResult
from AI.DifficultyController import DifficultyController
from AI.Trial_Proposer import PDEP_TrialProposer

from db.db_connector import DBConnector

from AI.TrialAdapter import TrialAdapter
from typing import List, Any, Tuple

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


    def __init__(   self, 
                    init_alpha: float, 
                    init_sigma: float, 
                    init_prob: float = 0.10, 
                    init_perceived_diff: float = 0.1, 
                    norm_feats: bool=True, 
                    update_step: int=5, 
                    mock: bool = False, 
                    kids_ds: bool = False, 
                    difficulty: str = "regular",
                    estimate_step: int = 1, 
                    estimation_min_trials: int = 50,
                    estimator_type: str = "ASD",
                    estimator_max_trials: int = 180,
                    estimation_duration: int = 10):
        self.alpha = init_alpha
        self.sigma = init_sigma
        self.target_error_prob = init_prob
        self.target_perceived_diff = init_perceived_diff
        self.norm_feats = norm_feats
        self.estimation_min_trials = estimation_min_trials
        self.estimate_step = estimate_step

        self.mode = "support" #should always be support, the other mode has been deprecated during development and is supported only for ASE_Estimator

        self.boundary_vector = unit_vector(np.array([-math.sin(math.radians(self.alpha)), math.cos(math.radians(self.alpha))]))

        #basis in the decision boundary space
        self.transform_mat =np.linalg.inv(np.array([[self.boundary_vector[0], self.boundary_vector[1]], [self.boundary_vector[1], -self.boundary_vector[0]]]))

        #variables used during update phase
        self.iteration = 0

        #initialize the PDEP pipeline
        self.difficulty_controller = DifficultyController(update_step, difficulty, init_prob, init_perceived_diff)
        self.trial_proposer = PDEP_TrialProposer()
        self.trial_adapter = TrialAdapter(mock,True, norm_feats, kids_ds)
        if estimator_type == "ASD":
            print("using ASD")
            self.estimator = ASD_Estimator(max_trials_to_consider=estimator_max_trials, min_trials_to_consider=self.estimation_min_trials, denoiser_type="simple_denoising")
        else:
            print("using ASE")
            self.estimator = ASE_Estimator(n_trials_per_cycle=estimation_duration, max_trials_to_consider=estimator_max_trials)
        

    def get_stats(self, type: int) -> Any:
        if type == 0:
            return self.alpha, self.sigma
        elif type == 1:
            return self.target_error_prob, self.target_perceived_diff
        elif type == 3:
            return self.boundary_vector
    
    def get_labels_for_stats(self, type: int) -> Any:
        if type == 0:
            return ["alpha", "sigma"]
        elif type == 1:
            return ["target error probability", "target perceived difficulty"]
    
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
        self.target_error_prob, self.target_perceived_diff = self.difficulty_controller.get_difficulty_parameters()
        nd_variable, nnd_variable, self.last_value = self.trial_proposer.find_trial(self.target_error_prob,self.target_perceived_diff, self.transform_mat, self.boundary_vector, self.sigma, self.norm_feats)

        if self.mode == "estimate":
            #accessed when using ASE_Estimator (deprecated)
            trial, self.last_value = self.estimator.get_trial()
            nd_variable = trial[0]
            nnd_variable = trial[1]

        trial = self.trial_adapter.find_trial(nd_variable, nnd_variable)

        self.estimator.append_trial([trial[0][8], trial[0][9]], self.mode)

        return trial
    
    def update_statistics(self, correct: bool, decision_time: float) -> None:
        """
            update the target error probability and the target perceived difficulty according to the response from the last trial

            for now just increase/decrease probability
        """
        self.iteration+=1
        self.difficulty_controller.history[self.iteration%self.difficulty_controller.update_step] = correct

        self.prev_stats = [self.target_error_prob, self.target_perceived_diff]

        #set the prediction in the estimator
        #print(self.estimator.trials)
        nd = self.estimator.trials[-1][0]
        prediction = True if (nd>0) == correct else False
        self.estimator.append_prediction(prediction, self.mode)

        self.difficulty_controller.update_difficulty_parameters(self.iteration)
            
        if (self.iteration%self.estimate_step ==0 or self.mode == "estimate") and self.iteration > self.estimation_min_trials:
            self.mode = "estimate"
            (self.alpha, self.sigma, self.boundary_vector), self.mode = self.estimator.produce_estimate(self.boundary_vector, self.sigma)
            self.transform_mat =np.linalg.inv(np.array([[self.boundary_vector[0], self.boundary_vector[1]], [self.boundary_vector[1], -self.boundary_vector[0]]]))

        
    def second_pass_estimation(self, alpha_data: List[float], sigma_data: List[float])-> Tuple[List[float], List[float], List[np.ndarray]]:
        return self.estimator.second_pass_estimation(alpha_data, sigma_data)
    
    def save_trial(self, save_file: str, trial: List[float], correct: bool, decision_time: float, commit: bool = False) -> None:
        """
            method to be called in order to store the computed trials in a file for future testing use
        """
        if commit:
            a = np.array(self.trials, dtype=np.float32)
            np.save(save_file, a)
        else:
            nd = trial[8]
            nnd = trial[9]
            sc = 1.0 if correct else 0.0
            t=np.array([nd,nnd, sc, decision_time])
            self.trials.append(t)

    def db_set_running_results(self, db: DBConnector, player_id: int) -> None:
        """
            fetch:
                list of trials and predictions for the estimator
                current alpha and sigma
                current target error probability/perceived difficulty and a reasonable history for it

        """
        trials_query = db.PDEP_fetch_trials_history(player_id)
        prob_window_n = self.difficulty_controller.memory-1

        for i, t in enumerate(trials_query):
            if i == 0:
                self.alpha, self.sigma = t[5], t[6]
                self.boundary_vector = unit_vector(np.array([-math.sin(math.radians(self.alpha)), math.cos(math.radians(self.alpha))]))

            self.estimator.append_trial([t[0], t[1]], "")
            self.estimator.append_prediction(t[2])

            if i % self.difficulty_controller.update_step == 0 and prob_window_n>=0:
                self.difficulty_controller.prob_history[prob_window_n] = np.argmin(np.abs(self.difficulty_controller.target_probs-t[3]))
                prob_window_n-=1
        
        self.difficulty_controller.target_error_prob = self.difficulty_controller.target_probs[self.difficulty_controller.prob_history[self.difficulty_controller.memory-1]]
        self.difficulty_controller.prob_choice_iteration = self.difficulty_controller.memory
        self.iteration = len(self.estimator.predictions)
        self.estimator.trials.reverse()
        self.estimator.predictions.reverse()
        print(f">>>>>>>>>>>{self.iteration}")

        
    def db_update(self, db: DBConnector, player_id: int, results_to_add: List[TrialResult]):
        db.PDEP_add_result( player_id, results_to_add[0], self.estimator.predictions[-1], self.estimator.trials[-1][0], self.estimator.trials[-1][1],
                            self.trial_adapter.recent_ids[-1], self.prev_stats[0], self.prev_stats[1], self.alpha, self.sigma)


if __name__ == "__main__":
    ev = PDEP_Evaluator(0.1,0.1)