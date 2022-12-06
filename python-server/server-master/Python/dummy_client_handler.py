from typing import Any, Dict, Tuple
from AI.PlayerSimulator import PlayerSimulator
from AI.ai_plot import plot_trials, plot_stats, FigSaver, plot_player_cycle3D
from AI.ai_utils import get_mock_trials
import numpy as np
from distributions import GaussianThreshold, UniformOutput
import math
import pandas
import numpy as np
import time

from AI.SimpleEvaluator import SimpleEvaluator
from transform_matrix import TransformMatrix
from AI.PDEP_Evaluator import PDEP_Evaluator

from datetime import datetime

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
    def __init__(   self, filtering_diff: float, sharpening_difficulty: float, alpha: float = 10.0, 
                    sigma: float = 0.05, mock_trials: bool = False, norm_feats: bool = True, evaluator: str = "PDEP", 
                    kids_ds: bool=False, save_file: str = None):
        self.filtering_diff = filtering_diff
        self.sharpening_diff = sharpening_difficulty
        self.lookup_table = pandas.read_csv("./dataset/lookup_table.csv")
        self.alpha = alpha
        self.sigma = sigma
        self.mock_trials = mock_trials
        self.norm_feats = norm_feats
        self.player = PlayerSimulator(self.alpha, self.sigma)
        self.save_file = save_file
        self.evaluator = evaluator

        if evaluator == "simple":
            self.player_evaluator = SimpleEvaluator(self.lookup_table, 1, 5, alt_mode_weight=0.5, kids_ds=kids_ds,)
            self.player_evaluator.set_running_results(init_running_results())
        elif evaluator == "PDEP":
            self.player_evaluator = PDEP_Evaluator(self.alpha, self.sigma, norm_feats=norm_feats,kids_ds=kids_ds)

    def run(self, trials: int, plot: bool, history_size: int = 10) -> None:

        
        mode = "filtering"

        performance = []

        proposed_trials = []
        corrects = []
        times = []

        if self.mock_trials:
            mock_trials = get_mock_trials(trials, self.norm_feats)
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
            plot_trials(self.player.boundary_vector, proposed_trials, corrects, times, norm_lim=self.norm_feats)
        else:
            print(f"Dummy client run, performance: {performance}, running results: {self.player_evaluator.running_results}")
        

    def simulate_player_cycle(  self, days: int, trials_per_day: int, plot_each_day: bool, update_evaluator_stats: bool,
                                update_child:bool, figsaver: FigSaver = None):

        performance = []

        proposed_trials = []
        corrects = []
        annotations = []

        local_accuracies = []

        cumulative_accuracies = []
        tot_corrects = 0

        t1_stat1_history = []
        t1_stat2_history = []

        t2_stat1_history = []
        t2_stat2_history = []

        sim_alpha_history = []
        sim_sigma_history = []
        

        sim_boundary_vectors = []
        sim_sigmas = []
        e_sigmas = []
        e_bvs = []

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} starting run with starting parameters: {self.alpha}-{self.sigma}")

        for day in range(1, days+1):
            local_corrects = 0
            for j in range(0, trials_per_day):
                trial = self.player_evaluator.get_trial()[0]
                correct, (decision_time, _) = self.player.predict(trial)
                proposed_trials.append(trial)
                corrects.append(correct)
                annotations.append(self.player_evaluator.get_info_as_string())

                s1,s2 = self.player_evaluator.get_stats(0)
                t1_stat1_history.append(s1)
                t1_stat2_history.append(s2)

                s1,s2 = self.player_evaluator.get_stats(1)
                t2_stat1_history.append(s1)
                t2_stat2_history.append(s2)

                sim_alpha_history.append(self.player.alpha)
                sim_sigma_history.append(self.player.sigma)

                tot_corrects += 1 if correct else 0
                local_corrects += 1 if correct else 0 

                if update_evaluator_stats:
                    self.player_evaluator.update_statistics(correct, decision_time)
                
                if self.save_file is not None:
                    self.player_evaluator.save_trial(self.save_file, trial, correct, decision_time)
            
            if self.save_file is not None:
                self.player_evaluator.save_trial(self.save_file, [], False, -1, commit= True)

            if update_child:
                bv, sig = self.player.random_improvement()
                sim_boundary_vectors.append(bv)
                sim_sigmas.append(sig)

                e_bvs.append(self.player_evaluator.boundary_vector)
                e_sigmas.append(self.player_evaluator.sigma)



            if plot_each_day or figsaver is not None:
                
                boundary = self.player_evaluator.boundary_vector if self.evaluator == "PDEP" else None
                sigma = self.player_evaluator.sigma if self.evaluator == "PDEP" else None

                plot_trials(self.player.boundary_vector, proposed_trials[-trials_per_day :], corrects[-trials_per_day:], annotations[-trials_per_day:], 
                            True, self.player_evaluator.plot_stats(day), norm_lim=self.norm_feats, sharp_std=self.player.sigma, figsaver=figsaver,
                            estimated_boundary=boundary, estimated_std=sigma)
            
            local_accuracies.append(local_corrects/trials_per_day)
            cumulative_accuracies.append(tot_corrects/(day*trials_per_day))
        
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} finished run with starting parameters: {self.alpha}-{self.sigma}")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} final evaluator stats are: {self.player_evaluator.get_stats_as_str()}")
        plot_stats(local_accuracies, cumulative_accuracies, days, figsaver=figsaver)
        label1 = self.player_evaluator.get_labels_for_stats(0)
        alpha_labels = [f"estimated {label1[0]}", f"actual {label1[0]}"]
        sigma_labels = [f"estimated {label1[1]}", f"actual {label1[1]}"]
        
        plot_stats(t1_stat1_history, sim_alpha_history, days*trials_per_day, labels=alpha_labels, figsaver=figsaver, lim_bounds=[-5, 95])
        plot_stats(t1_stat2_history, sim_sigma_history, days*trials_per_day, labels=sigma_labels, figsaver=figsaver)
        
        plot_stats(t2_stat1_history, t2_stat2_history, days*trials_per_day, labels=self.player_evaluator.get_labels_for_stats(1), figsaver=figsaver)

        if self.evaluator == "PDEP":
            plot_player_cycle3D(sim_boundary_vectors, e_bvs, sim_sigmas, e_sigmas, proposed_trials, corrects, trials_per_day, figsaver= figsaver)
        




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