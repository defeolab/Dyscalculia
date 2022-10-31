from typing import Any, Dict, Tuple
from AI.PlayerSimulator import PlayerSimulator
from AI.ai_plot import plot_trials
from AI.ai_utils import get_mock_trials
import numpy as np
from distributions import GaussianThreshold, UniformOutput
import math
import pandas
import numpy as np


from AI.player_evaluate import SimpleEvaluator
from transform_matrix import TransformMatrix

def init_running_results() -> Dict[str, Any]:
    running_results = {}

    running_results["filtering_total"] = 0 # total number of filtering trials
    running_results["filtering_correct"] = 0
    running_results["filtering_acc"] = -1 
    running_results["filtering_diff"] = 0.1
    running_results["filtering_total_time"] = 0 # average time of responding to a filtering trial
    running_results["filtering_avg_time"] = -1 # average time of responding to a filtering trial
    running_results["filtering_history"] = []

    running_results["sharpening_total"] = 0 # total number of sharpening trials
    running_results["sharpening_correct"] = 0
    running_results["sharpening_acc"] = -1 
    running_results["sharpening_diff"] = 0.1
    running_results["sharpening_total_time"] = 0 # average time of responding to a sharpening trial
    running_results["sharpening_avg_time"] = -1 # average time of responding to a sharpening trial
    running_results["sharpening_history"] = []

    return running_results

class SimulatedClient:
    def __init__(self, filtering_diff: float, sharpening_difficulty: float, alpha: float = 10.0, sigma: float = 0.05, mock_trials: bool = False):
        self.filtering_diff = filtering_diff
        self.sharpening_diff = sharpening_difficulty
        self.lookup_table = pandas.read_csv("./dataset/lookup_table.csv")
        self.alpha = alpha
        self.sigma = sigma
        self.mock_trials = mock_trials

    def run(self, trials: int, plot: bool, history_size: int = 10) -> None:
        self.player = PlayerSimulator(self.alpha, self.sigma)
        self.player_evaluator = SimpleEvaluator(self.lookup_table, 1, trials, history_size, alt_mode_weight=0.5)

        self.player_evaluator.set_running_results(init_running_results())
        mode = "filtering"

        performance = []

        proposed_trials = []
        corrects = []
        times = []

        if self.mock_trials:
            mock_trials = get_mock_trials(trials)
            trials = len(mock_trials)

        for i in range(0, trials):
            
            trial = mock_trials[i] if self.mock_trials else self.player_evaluator.get_trial()[0]

            correct, decision_time = self.player.predict(trial)

            proposed_trials.append(trial)
            corrects.append(correct)
            times.append(decision_time)

            if self.mock_trials == False:
                self.player_evaluator.update_statistics(correct, decision_time)

            performance.append(correct)

        
        if plot:
            plot_trials(self.player, proposed_trials, corrects, times)
        else:
            print(f"Dummy client run, performance: {performance}, running results: {self.player_evaluator.running_results}")
        

    def predict_trial(self, trial: pandas.Series) -> Tuple[int, float]:
        correct = 1
        #simple predictor, if aggregated trial difficulty is higher than player ability just mispredict
        if self.player_evaluator.last_diffs[0] + self.player_evaluator.last_diffs[1] > self.sharpening_diff + self.filtering_diff:
            correct = 0
        
        return correct, 500.0




#LEGACY   
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
            nv.append(np.log10(results[1]/results[0])) # number_of_chickens
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