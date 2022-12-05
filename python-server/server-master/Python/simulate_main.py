import unittest
from AI.ai_utils import *
from AI.TrialAdapter import TrialAdapter
from AI.ai_plot import plot_trials, FigSaver
from AI.PDEP_Evaluator import PDEP_Evaluator
from dummy_client_handler import SimulatedClient
import time
import os
import winsound

BASE_PATH_FOR_PICS = "C:\\Users\\fblan\\Desktop\\thesis_pics"
BASE_PATH_FOR_SAVING_TRIALS = "C:\\Users\\fblan\\Dyscalculia\\python-server\\server-master\\Python\\AI\\precomputed_data"

class SimulationsRunner(unittest.TestCase):
    def __init__(   self, days:int, trials_per_day:int, fig_interval: int, evaluator: str, kids_ds: bool, 
                    update_evaluator_stats:bool, update_child: bool, suite_name: str, target_prob: float, 
                    target_diff: Tuple[float,float], mode:str, save_trials: bool, save_plots: bool,
                    alphas: List[float], sigmas: List[float], mock: bool, estimate_step: int, child_alpha_std: float,
                    child_sigma_std: float, child_improve_step: int ):
        
        self.days = days
        self.trials_per_day = trials_per_day
        self.interval = fig_interval
        self.evaluator = evaluator
        self.kids_ds = kids_ds
        self.add_date = False
        self.update_evaluator_stats = update_evaluator_stats
        self.update_child = update_child
        self.target_prob = target_prob
        self.target_diff = target_diff
        self.mode = mode
        self.save_trials = save_trials
        self.save_plots = save_plots
        self.alphas = alphas
        self.sigmas = sigmas
        self.mock = mock
        self.estimate_step = estimate_step
        self.child_alpha_std = child_alpha_std
        self.child_sigma_std = child_sigma_std
        self.child_improve_step = child_improve_step

        self.base_root = os.path.join(BASE_PATH_FOR_PICS, self.evaluator)
        self.base_root = os.path.join(self.base_root, suite_name)
        if os.path.exists(self.base_root) == False and self.save_plots:
            os.mkdir(self.base_root)

        self.save_root = os.path.join(BASE_PATH_FOR_SAVING_TRIALS, self.evaluator)
        self.save_root = os.path.join(self.save_root, suite_name)
        if os.path.exists(self.save_root) == False and self.save_trials:
            os.mkdir(self.save_root)
        
    
    def simulation_suite(self):

        for alpha in self.alphas:
            for sigma in self.sigmas:
                exp_name = f"alpha_{alpha}_sigma_{int(sigma*100)}"
                save_file = os.path.join(self.save_root, exp_name) if self.save_trials else None
                handler = SimulatedClient(0.5,0.5, alpha=alpha, sigma=sigma, evaluator=self.evaluator, kids_ds=kids_ds, save_file=save_file)
                
                handler.player.improve_alpha_std = self.child_alpha_std
                handler.player.improve_sigma_std = self.child_sigma_std
                handler.player.improve_interval = self.child_improve_step
                
                if self.evaluator == "PDEP":
                    handler.player_evaluator.target_error_prob = self.target_prob
                    handler.player_evaluator.trial_adapter.mock = self.mock
                    handler.player_evaluator.estimate_step = self.estimate_step
                else:
                    handler.player_evaluator.running_results['filtering_diff'] = self.target_diff[0]
                    handler.player_evaluator.running_results['sharpening_diff'] = self.target_diff[1]
                    handler.player_evaluator.mode = mode
                    handler.player_evaluator.always_update_step = True
                figsaver = FigSaver(self.base_root, exp_name, interval=self.interval) if self.save_plots else None
                handler.simulate_player_cycle(self.days, self.trials_per_day, False, self.update_evaluator_stats,self.update_child, figsaver=figsaver)

    
if __name__ == "__main__":

    alphas = [
        [10, 30, 60],
        [45]
        ]
    sigmas = [
        [0.10, 0.20, 0.4],
        [0.1, 0.2, 0.3, 0.4, 0.5],
        [0.5],
        [0.2]
        ]

    probs = [0.10, 0.30, 0.80]
    diffs = [(0.1,0.1), (0.4, 0.4), (0.8, 0.8), (0.95,0.95)]
    modes = ["filtering", "sharpening"]

    days = 60
    trials_per_day = 6
    interval = 5

    evaluator = "PDEP"
    kids_ds = False
    add_date = False
    update_evaluator_stats = True

    update_child = False
    child_alpha_std = 0.5
    child_sigma_std = 0.05
    child_improve_step = 1

    target_prob = probs[2]
    target_diff = diffs[0]
    mode = modes[0]
    save_trials = False
    save_plots = True
    alpha_i = 1
    sigma_i = 3
    mock = True
    estimate_step = 6

    suite_name = "ASDll_test"

    sr = SimulationsRunner( days, trials_per_day, interval, evaluator, kids_ds, update_evaluator_stats, update_child, suite_name, 
                            target_prob, target_diff, mode, save_trials, save_plots, alphas[alpha_i], sigmas[sigma_i], mock, estimate_step,
                            child_alpha_std, child_sigma_std, child_improve_step)

    start_time = time.time()

    sr.simulation_suite()

    duration = 1000  # milliseconds
    freq = 440  # Hz
    winsound.Beep(freq, duration)
    print("--- %s seconds ---" % (time.time() - start_time))