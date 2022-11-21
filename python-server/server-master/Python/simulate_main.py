import unittest
from AI.ai_utils import *
from AI.TrialAdapter import TrialAdapter
from AI.ai_plot import plot_trials, FigSaver
from AI.PDEP_Evaluator import PDEP_Evaluator
from dummy_client_handler import SimulatedClient
import time
import os

BASE_PATH_FOR_PICS = "C:\\Users\\fblan\\Desktop\\thesis_pics"

class SimulationsRunner(unittest.TestCase):
    def __init__(   self, days:int, trials_per_day:int, fig_interval: int, evaluator: str, kids_ds: bool, 
                    update_evaluator_stats:bool, update_child: bool, suite_name: str, target_prob: float, target_diff: Tuple[float,float], mode:str):
        
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

        self.base_root = os.path.join(BASE_PATH_FOR_PICS, self.evaluator)
        self.base_root = os.path.join(self.base_root, suite_name)
        if os.path.exists(self.base_root) == False:
            os.mkdir(self.base_root)
    
    def simulation_suite(self):
        alphas = [10, 30, 60]
        sigmas = [0.10, 0.20, 0.4]

        for alpha in alphas:
            for sigma in sigmas:

                handler = SimulatedClient(0.5,0.5, alpha=alpha, sigma=sigma, evaluator=self.evaluator, kids_ds=self.kids_ds)
                if self.evaluator == "PDEP":
                    handler.player_evaluator.target_error_prob = self.target_prob
                else:
                    handler.player_evaluator.running_results['filtering_diff'] = self.target_diff[0]
                    handler.player_evaluator.running_results['sharpening_diff'] = self.target_diff[1]
                    handler.player_evaluator.mode = mode

                exp_name = f"alpha_{alpha}_sigma_{int(sigma*100)}"
                figsaver = FigSaver(self.base_root, exp_name, interval=self.interval)
                handler.simulate_player_cycle(self.days, self.trials_per_day, False, self.update_evaluator_stats,self.update_child, figsaver=figsaver)


if __name__ == "__main__":

    probs = [0.10, 0.30, 0.80]
    diffs = [(0.1,0.1), (0.4, 0.4), (0.8, 0.8)]
    modes = ["filtering", "sharpening"]

    days = 60
    trials_per_day = 6
    interval = 15
    evaluator = "simple"
    kids_ds = False
    add_date = False
    update_evaluator_stats = False
    update_child = False
    target_prob = probs[1]
    target_diff = diffs[1]
    mode = modes[0]

    suite_name = "no_update_f40"

    sr = SimulationsRunner(days, trials_per_day, interval, evaluator, kids_ds, update_evaluator_stats, update_child, suite_name, target_prob, target_diff, mode)

    start_time = time.time()

    sr.simulation_suite()

    print("--- %s seconds ---" % (time.time() - start_time))