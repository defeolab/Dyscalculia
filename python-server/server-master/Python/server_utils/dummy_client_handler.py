from typing import Any, Dict, Tuple, List
from AI.PlayerSimulator import PlayerSimulator
from AI.ai_plot import plot_trials, plot_stats, FigSaver, plot_player_cycle3D, plot_monthly_stats, make_tables, average_by_day
from AI.ai_utils import get_mock_trials, save_npy
import numpy as np
import math
import pandas
import numpy as np
import time

from AI.SimpleEvaluator import SimpleEvaluator
from AI.PDEP_Evaluator import PDEP_Evaluator
from AI.ai_consts import *
import os

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
    def __init__(   self, 
                    filtering_diff: float, 
                    sharpening_difficulty: float, 
                    alpha: float = 10.0, 
                    sigma: float = 0.05, 
                    mock_trials: bool = False, 
                    norm_feats: bool = True, 
                    evaluator: str = "PDEP", 
                    kids_ds: bool=False, 
                    save_file: str = None,
                    estimation_duration: int = 10,
                    estimator_type: str = "ASD",
                    init_evaluator: bool = False,
                    estimator_max_trials: int = 180,
                    estimator_min_trials: int = 30,
                    improver_type: str = "linear",
                    improver_parameters: List[float] = [1, 0.01, 5],
                    difficulty: str = "regular"):

        self.filtering_diff = filtering_diff
        self.sharpening_diff = sharpening_difficulty
        self.lookup_table = pandas.read_csv("./dataset/lookup_table.csv")
        self.alpha = alpha
        self.sigma = sigma
        self.mock_trials = mock_trials
        self.norm_feats = norm_feats
        self.player = PlayerSimulator(self.alpha, self.sigma, improver_type=improver_type, improver_parameters=improver_parameters)
        self.save_file = save_file
        self.evaluator = evaluator

        if self.save_file is not None:
            self.save_folder = os.path.relpath(os.path.join(self.save_file, os.pardir))

        if evaluator == "simple":
            self.player_evaluator = SimpleEvaluator(self.lookup_table, 1, 5, alt_mode_weight=0.5, kids_ds=kids_ds,)
            self.player_evaluator.set_running_results(init_running_results())
        elif evaluator == "PDEP":
            init_alpha = self.alpha if init_evaluator else 45
            init_sigma = self.sigma if init_evaluator else 0.3
            self.player_evaluator = PDEP_Evaluator(init_alpha, init_sigma, norm_feats=norm_feats,kids_ds=kids_ds, estimation_duration=estimation_duration, estimator_type=estimator_type, estimator_max_trials=estimator_max_trials, estimation_min_trials=estimator_min_trials, difficulty=difficulty)

    def run(self, trials: int, plot: bool, history_size: int = 10) -> None:

        mode = "filtering"

        performance = []

        proposed_trials = []
        corrects = []
        times = []
        anns = []
        if self.mock_trials:
            mock_trials = get_mock_trials(trials, self.norm_feats)
            trials = len(mock_trials)

        for i in range(0, trials):
            
            trial = mock_trials[i] if self.mock_trials else self.player_evaluator.get_trial()[0]

            correct, (decision_time, looks_right) = self.player.predict(trial)

            proposed_trials.append(trial)
            corrects.append(correct)
            times.append(decision_time)

            if self.mock_trials == False:
                self.player_evaluator.update_statistics(correct, decision_time)
            anns.append("")
            performance.append(correct)

        
        if plot:
            plot_trials(self.player.boundary_vector, proposed_trials, corrects, anns, norm_lim=self.norm_feats, ann_str=True, sharp_std=None, plot_fs=True, title=f"Alpha = {self.alpha}°; Sigma = {self.sigma} u")
        else:
            print(f"Dummy client run, performance: {performance}, running results: {self.player_evaluator.running_results}")
        

    def simulate_player_cycle(  self, days: int, 
                                trials_per_day: int, 
                                plot_each_day: bool, 
                                update_evaluator_stats: bool,
                                update_child:bool, 
                                figsaver: FigSaver = None,
                                make_plots: bool = True):

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

        month_n = 1

        monthly_data = []

        label1 = self.player_evaluator.get_labels_for_stats(0)
        alpha_labels = [f"estimated {label1[0]}", f"actual {label1[0]}", f"second pass {label1[0]}"]
        sigma_labels = [f"estimated {label1[1]}", f"actual {label1[1]}", f"second pass {label1[1]}"]
        accuracy_labels = [f"Local accuracy", "Cumulative accuracy"]
        alpha_bounds = [-5, MAX_ALPHA+5]
        sigma_bounds = [-0.1, MAX_SIGMA+0.1]
        accuracy_bounds = [-0.1, 1.1]

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

                if update_child:
                    bv, sig = self.player.apply_improvement()

            if self.save_file is not None:
                self.player_evaluator.save_trial(self.save_file, [], False, -1, commit= True)

            sim_boundary_vectors.append(self.player.boundary_vector)
            sim_sigmas.append(self.player.sigma)

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

            
            month_n+=1 if day%30==0 else 0

        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} finished run with starting parameters: {self.alpha}-{self.sigma}")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} final evaluator stats are: {self.player_evaluator.get_stats_as_str()}")

        if make_plots:
            plot_stats([local_accuracies, cumulative_accuracies], days, figsaver=figsaver, labels=["local accuracy", "cumulative accuracy"], main_stat="accuracy", lim_bounds=accuracy_bounds, xlabel="day")
            label1 = self.player_evaluator.get_labels_for_stats(0)
            if self.evaluator == "PDEP":
                sp_alpha, sp_sigma, sp_norms = self.player_evaluator.second_pass_estimation(t1_stat1_history, t1_stat2_history) if update_evaluator_stats else ([], [], [-1,1])


            for i in range(0, month_n-1):

                plot_monthly_stats( [   
                                        t1_stat1_history[i*trials_per_day*30: (i+1)*trials_per_day*30], 
                                        sim_alpha_history[i*trials_per_day*30: (i+1)*trials_per_day*30], 
                                        sp_alpha[i*trials_per_day*30: (i+1)*trials_per_day*30]
                                    ], 
                                    trials_per_day, i+1, labels=alpha_labels, figsaver=figsaver, lim_bounds=alpha_bounds, main_stat="alpha")
                plot_monthly_stats( [
                                        t1_stat2_history[i*trials_per_day*30: (i+1)*trials_per_day*30], 
                                        sim_sigma_history[i*trials_per_day*30: (i+1)*trials_per_day*30],
                                        sp_sigma[i*trials_per_day*30: (i+1)*trials_per_day*30]
                                    ], 
                                    trials_per_day, i+1, labels=sigma_labels, figsaver=figsaver, lim_bounds=sigma_bounds, main_stat="sigma")
            
            
            plot_monthly_stats( [t1_stat1_history,sim_alpha_history,sp_alpha],trials_per_day, -1, labels=alpha_labels, figsaver=figsaver, lim_bounds=alpha_bounds, main_stat="alpha", length = days)
            plot_monthly_stats( [t1_stat2_history,sim_sigma_history,sp_sigma],trials_per_day, -1, labels=sigma_labels, figsaver=figsaver, lim_bounds=sigma_bounds, main_stat="sigma", length=days)
            #plot_monthly_stats( [t2_stat1_history, t2_stat2_history], trials_per_day, -1, main_stat="accuracy",labels=self.player_evaluator.get_labels_for_stats(1), figsaver=figsaver, lim_bounds=accuracy_bounds )
        
            plot_stats([t1_stat1_history, sim_alpha_history], days*trials_per_day, labels=alpha_labels[0:2], figsaver=figsaver, lim_bounds=[-5, 95], main_stat="alpha")
            plot_stats([t1_stat2_history, sim_sigma_history], days*trials_per_day, labels=sigma_labels[0:2], figsaver=figsaver, main_stat="sigma")
        

            plot_stats([t1_stat1_history, sim_alpha_history, sp_alpha], days*trials_per_day, labels=alpha_labels, figsaver=figsaver, lim_bounds=[-5, 95], main_stat="alpha")
            plot_stats([t1_stat2_history, sim_sigma_history,sp_sigma], days*trials_per_day, labels=sigma_labels, figsaver=figsaver, main_stat="sigma")
        
            plot_stats([t2_stat1_history, t2_stat2_history], days*trials_per_day, labels=self.player_evaluator.get_labels_for_stats(1), figsaver=figsaver, main_stat="accuracy", lim_bounds=accuracy_bounds)

            #normalized plot for alpha, sigma and accuracy
            norm_slope_alpha = abs(round((self.player.improver.slope_alpha/MAX_ALPHA)*trials_per_day, 4))*100
            norm_slope_sigma = abs(round((self.player.improver.slope_sigma/MAX_SIGMA)*trials_per_day, 4))*100

            plot_stats  (   [   
                                average_by_day(sp_alpha, trials_per_day)/MAX_ALPHA,
                                1-(average_by_day(sp_sigma, trials_per_day)/MAX_SIGMA),
                                cumulative_accuracies
                            ],
                            days,
                            ["Estimated Non-Numerical Interference (NNI)", "Estimated Numerical Acuity (NA)", "Cumulative Accuracy"], 
                            main_stat="NNI Score - NA score - Accuracy %",
                            lim_bounds=[-0.1, 1.1],
                            save_as_ndarray=False,
                            title= f"Daily NNI decrease = {norm_slope_alpha}%; Daily NA gain = {norm_slope_sigma}%",
                            xlabel="days",
                            figsaver=figsaver
                        )
            if update_evaluator_stats:
                make_tables(sim_alpha_history, [t1_stat1_history, sp_alpha], trials_per_day, n_months=month_n-1, main_label="alpha", secondary_labels=["FP", "SP"], figsaver=figsaver)
                make_tables(sim_sigma_history, [t1_stat2_history, sp_sigma], trials_per_day, n_months=month_n-1, main_label="sigma", secondary_labels=["FP", "SP"], figsaver=figsaver)
            
            if self.evaluator == "PDEP":
                plot_player_cycle3D(sim_boundary_vectors, e_bvs, sim_sigmas, e_sigmas, proposed_trials, corrects, trials_per_day, figsaver= figsaver)
        
            if self.save_file is not None:
                #save alpha and sigma estimations over time
                save_npy(self.save_folder, t1_stat1_history, "fp_alpha")
                save_npy(self.save_folder, sp_alpha, "sp_alpha")
                save_npy(self.save_folder, sim_alpha_history, "sim_alpha")
                save_npy(self.save_folder, t1_stat2_history, "fp_sigma")
                save_npy(self.save_folder, sp_sigma, "sp_sigma")
                save_npy(self.save_folder, sim_sigma_history, "sim_sigma")

        return (t1_stat1_history, t1_stat2_history), (sim_alpha_history, sim_sigma_history), (self.player_evaluator.estimator.trials, self.player_evaluator.estimator.predictions)
