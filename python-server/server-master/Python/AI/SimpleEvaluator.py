from time import time
from typing import Any, Tuple, List, Optional, Dict
import random
from db.db_connector import DBConnector
from trial_result import TrialResult
import numpy as np
from trial_mode_utils import qserver_ask_for_question_recommendation

from AI.ai_utils import compute_nd_nnd_coords

from pandas import DataFrame
import pandas

class PlayerEvaluator:
    """
        This class is in charge of two things:

            - Understand the ability of the player
            - Proposing the trials to match their ability
    """
    def __init__(self) -> None:
        pass
    
    def set_running_results(self, running_results: List[Any]) -> None:
        """
            initialize stats to be used when they're available even without db
        """
        self.running_results = running_results

    def get_stats(self, type: int) -> Any:
        """
            Simple function to return the level of the current player (if evaluator contains several stats, differentiate with type)
        """
        pass

    def get_labels_for_stats(self, type: int) -> Any:
        """
            returns the labels of the statistics (differentiate with type)
        """
        return "stat1", "stat2"

    def get_main_stat(self) -> Any:
        """
            Simple function to return the main current statistic (i.e. filtering or sharpening, or error prob for PDEP) 
        """

    def get_stats_as_str(self) -> str:
        """
            Simple function to return the level of the current player in a printable format
        """
        pass
    
    def plot_stats(self, day: int):
        """
            define how to plot the current evaluator's statistics
        """
    def plot_stats3D(self, days:int, stats_snapshots: List[Any]):
        """
            receive the snapshots of the estimated statistics over time and plot their growth
        """
    def get_info_as_string(self) -> str:
        """
            get more informations regarding the last trial sent as string
        """
    
    def get_info(self) -> List[Any]:
        """
            get more informations regarding the last trial sent as string
        """

    def get_trial(self) -> List[Any]:
        """
            Function to return a trial depending on the current state of the evaluator
        """
        pass
    
    def set_trial(self, trial: List[Any]) -> None:
        """
            Function that has to be called to force the use of a custom trial instead of letting the evaluator decide the next trial through get_trial
        """
        pass

    def save_trial(self, save_file: str, trial: List[float], correct: bool, decision_time: float, commit: float = False) -> None:
        """
            method to be called in order to store the computed trials in a file for future testing use
        """
        pass

    def update_statistics(self) -> None:
        """
            after get_trial or set_trial has been called, use this function to update the player statistics based on the player response
        """
        pass

    def get_question_type(self) -> bool:
        """
            this method returns the type of question (i.e. whether we want the child to select the fence with more or fewer animals).

            False -> more animals
            True  -> fewer animals
        """

        #default behaviour: return False
        return True

    def db_update(self, db: DBConnector, player_id: int, results_to_add: List[TrialResult]):
        """
            function to be called for proper update of the db
        """
        pass
    
    def db_set_running_results(self, db: DBConnector, player_id: int) -> None:
        """
            Function for understanding the current level/history of the player by fetching it from the db
        """
        pass

    
class SimpleEvaluator(PlayerEvaluator):
    """
        An evaluator subclass that is consistent with the previous ai implementation

        
    """
    def __init__(   self, lookup_table: DataFrame, player_id: int, history_size:int, alt_mode_weight: float = 0.0,
                    fetched_samples: int = 16, selection_factor: int = 4, normalize_vars: bool= True, 
                    old_table: bool = False, kids_ds: bool = False, always_update_step: bool = True):
        self.lookup_table = lookup_table
        self.player_id = player_id
        self.history_size=history_size
        self.alt_mode_weight = alt_mode_weight
        self.fetched_samples = fetched_samples
        self.selected_samples = fetched_samples//selection_factor
        self.mode = "filtering"
        self.normalize_vars = normalize_vars
        self.always_update_step = always_update_step

        if old_table:
            self.lookup_table = pandas.read_csv("./dataset/legacy/lookup_table.csv")

            #we need to compute nd and nnd for this table
            nd = []
            nnd = []
            
            for i, r in self.lookup_table.iterrows():
                #print(f"{r['NumLeft']} - {r['NumRight']}")

                nd_logratio, nnd_logratio = compute_nd_nnd_coords([float(r['NumLeft']), float(r['FieldAreaLeft']),float(r['ItemSurfaceAreaLeft'])],[float(r['NumRight']), float(r['FieldAreaRight']),float(r['ItemSurfaceAreaRight'])])
                nd.append(nd_logratio)
                nnd.append(nnd_logratio)
            
            self.lookup_table['nd_LogRatio'] = nd
            self.lookup_table['nnd_LogRatio'] = nnd
        
        if kids_ds:
            self.lookup_table = pandas.read_csv("./dataset/lookup_table_kids.csv")

        if self.normalize_vars:
            self.max_nd = self.lookup_table['nd_LogRatio'].abs().max()
            self.max_nnd = self.lookup_table['nnd_LogRatio'].abs().max()
    
    def set_running_results(self, running_results: List[Any]) -> None:
        self.both_histories = []
        return super().set_running_results(running_results)

    def db_set_running_results(self, db: DBConnector, player_id: int) -> None:
        self.running_results = db.get_player_stats(player_id, self.history_size)

        self.both_histories = db.fetch_both_histories(player_id, self.history_size)
        
        if len(self.both_histories) >0:
            suggestion = qserver_ask_for_question_recommendation(self.both_histories[-1][0], -1,-1, self.both_histories[:-1])
            self.mode = "filtering" if suggestion[0] == "f" else "sharpening"

    def db_update(self, db: DBConnector, player_id:int, results_to_add: List[TrialResult]):
        #results_to_add[0].difficulty = self.running_results['filtering_diff'] if self.mode == 'filtering' else self.running_results['sharpening_diff']
        #results_to_add[0].mode = self.mode
        db.add_results(self.player_id, results_to_add)
        db.update_player_stats(self.player_id, self.running_results)

    def get_stats(self, type: int) -> Any:
        return self.running_results['filtering_diff'], self.running_results['sharpening_diff']
    
    def get_main_stat(self) -> Any:
        if self.mode == "filtering":
            return self.running_results['filtering_diff']
        else:
            return self.running_results['sharpening_diff']
            
    def get_stats_as_str(self) -> Any:
        return f"{self.running_results['filtering_diff']} - {self.running_results['sharpening_diff']}"
    
    def plot_stats(self, day: int):
        def func(plt):
            plt.title(f"Day {day}, Filtering diff {round(self.running_results['filtering_diff'],2)}, Sharpening diff {round(self.running_results['sharpening_diff'],2)}")

        return func
    def get_trial(self) -> List[Any]:

        if self.mode == "filtering" :
            col = "Diff_coeff_filtering"
            weights = [1-self.alt_mode_weight, self.alt_mode_weight]
        else :
            col = "Difficulty Coefficient"
            weights = [self.alt_mode_weight, 1-self.alt_mode_weight]

        #compute aggregated statistics for current mode
        self.lookup_table['aggregated_diff'] = self.lookup_table['Diff_coeff_filtering']*weights[0] + self.lookup_table['Difficulty Coefficient']*weights[1]

        #find closest trials according to difficulty of current mode 
        target_main_diff = self.running_results[self.mode + "_diff"]
        fetched_trials = self.lookup_table.iloc[(self.lookup_table[col]-target_main_diff).abs().argsort()[:self.fetched_samples]]

        #find the closest trials in terms of aggregated difficulty
        #target_agg_diff = self.running_results['filtering_diff']*weights[0]+self.running_results["sharpening_diff"]*weights[1]
        #fetched_trials = fetched_trials.iloc[(fetched_trials['aggregated_diff']-target_agg_diff).abs().argsort()[:self.selected_samples]]

        # pick a random one among the selected trials
        r = fetched_trials.iloc[random.choice(range(self.selected_samples))]
        
        # generate trial matrices
        matrix = []
        if self.normalize_vars:
            matrix.append([float(r["NumLeft"]), float(r["NumRight"]), float(r["FieldAreaLeft"]), float(r["FieldAreaRight"]), float(r["ItemSurfaceAreaLeft"]), float(r["ItemSurfaceAreaRight"]),4,8,float(r["nd_LogRatio"]/self.max_nd), float(r["nnd_LogRatio"]/self.max_nnd)])
        else:
            matrix.append([float(r["NumLeft"]), float(r["NumRight"]), float(r["FieldAreaLeft"]), float(r["FieldAreaRight"]), float(r["ItemSurfaceAreaLeft"]), float(r["ItemSurfaceAreaRight"]),4,8,float(r["nd_LogRatio"]), float(r["nnd_LogRatio"])])
        #print("NUMBER OF TRIALS SENT: " + str(len(matrix)))

        #store the two difficulties for this trial (not available after client response)
        self.last_diffs = [r['Diff_coeff_filtering'], r['Difficulty Coefficient']]
        return matrix
    
    def get_info_as_string(self) -> str:
        if self.mode == "filtering":
            return f"fd {round(self.last_diffs[0],2)}"
        else:
            return f"sd {round(self.last_diffs[1], 2)}"
    
    def get_info(self) -> List[Any]:
        return self.last_diffs

    def set_trial(self, trial: List[Any]) -> None:

        #for code compatibility
        self.last_diffs = [0.5, 0.5]

    def update_statistics(self, correct: int, decision_time: float) -> None:
        self.running_results[self.mode + "_total"] += 1
        self.running_results[self.mode + "_correct"] += correct
        self.running_results[self.mode + "_acc"] = self.running_results[self.mode + "_correct"] / self.running_results[self.mode + "_total"]
        self.running_results[self.mode + "_total_time"] += decision_time
        self.running_results[self.mode + "_avg_time"] = self.running_results[self.mode + "_total_time"] / self.running_results[self.mode + "_total"]
        self.running_results[self.mode + "_history"].append(correct)

        if len(self.running_results[self.mode + "_history"]) > self.history_size : self.running_results[self.mode + "_history"].pop(0)

        steps = self._old_step(correct, decision_time, self.mode)

        suggestion = qserver_ask_for_question_recommendation('f' if self.mode == "filtering" else "s", correct, decision_time, self.both_histories)

        self.mode = "filtering" if suggestion[0] == "f" else "sharpening"
        self.both_histories = suggestion[1]
        self.both_histories = self.both_histories[-4:]

    def _old_step(self, correct: int, decision_time:float, mode:str) -> Tuple[float, float]:
        if len(self.running_results[self.mode + "_history"]) > self.history_size : self.running_results[self.mode + "_history"].pop(0)
            #print(self.running_results[self.mode + "_history"])

        step = 0.05 # increments difficulty 5% at a time
        if self.always_update_step:
            #Francesco's change, the rest of the code creates problems in the update of statistics
            step = -step if correct == False else step
            self.running_results[self.mode + "_diff"] += step
            self.running_results[self.mode + "_diff"] = float(np.clip(self.running_results[self.mode + "_diff"], 0.05, 0.95))
            return

        if self.running_results[self.mode + "_acc"] >= 0.8 :
            if self.running_results[self.mode + "_diff"] + step < 1 :
                self.running_results[self.mode + "_diff"] += step

        elif self.running_results[self.mode + "_acc"] <= 0.5 :
            if self.running_results[self.mode + "_diff"] - step > 0 :
                self.running_results[self.mode + "_diff"] -= step
        
        return 0.0, 0.0

    def _get_step(self, correct: int, decision_time:float, mode: str) -> Tuple[float, float]:
        
        #base step (represents maximum possible increment)
        base_step = 1

        diff_factor_min = 0.2
        momentum_factor_min = 0.2
        max_show_seconds = 6
        min_time_factor = 0.1

        #take history and decision time into account
        if correct:
            momentum_sh = max((sum(self.running_results['sharpening_history'],0))/self.history_size, momentum_factor_min)
            momentum_fi = max(sum(self.running_results['filtering_history'],0)/self.history_size, momentum_factor_min)

            #bonus for fast response
            time_factor = max((max_show_seconds*1000-decision_time)/(max_show_seconds*1000), min_time_factor)

            sign = 1

            #if the trial was easier than the current ability of the child, decrease the step
            #if instead it was very hard, give a bonus
            diff_factor_fi = max(diff_factor_min, self.last_diffs[0] - self.running_results["filtering_diff"])
            diff_factor_sh = max(diff_factor_min, self.last_diffs[1] - self.running_results["sharpening_diff"])     

        else:
            momentum_sh = max((self.history_size -sum(self.running_results['sharpening_history'],0))/self.history_size,momentum_factor_min)
            momentum_fi = max((self.history_size -sum(self.running_results['filtering_history'],0))/self.history_size, momentum_factor_min)

            #wrong answer, response time is irrelevant
            time_factor=1

            sign = -1

            #if the trial was harder than the current ability of the child, do not penalize too much
            #if instead we tought the child would easily guess correctly, increase the step
            diff_factor_fi = max(diff_factor_min, self.running_results["filtering_diff"] - self.last_diffs[0])
            diff_factor_sh = max(diff_factor_min, self.running_results["sharpening_diff"] - self.last_diffs[1]) 
        
        #take main mode into account
        if mode == "filtering":
            weights = [1-self.alt_mode_weight, self.alt_mode_weight]
        else :
            weights = [self.alt_mode_weight, 1-self.alt_mode_weight]

        step_fi = sign*base_step*momentum_fi*time_factor*weights[0]*diff_factor_fi
        step_sh = sign*base_step*momentum_sh*time_factor*weights[1]*diff_factor_sh

        #print(f"m_fi: {momentum_fi}, t_f: {time_factor}, weights: {weights[0]}, diff_f: {diff_factor_fi}")
        #print(f"m_sh: {momentum_sh}, t_f: {time_factor}, weights: {weights[1]}, diff_f: {diff_factor_sh}")
        steps = [step_fi, step_sh]
        for t_mode, step in zip(["filtering", "sharpening"], steps):
            if self.running_results[t_mode + "_diff"] + step > 1 :
                self.running_results[t_mode + "_diff"] = 0.99
            elif self.running_results[t_mode + "_diff"] + step < 0 :
                self.running_results[t_mode + "_diff"] = 0.01
            else:
                self.running_results[t_mode + "_diff"] += step

        return step_fi, step_sh

        
