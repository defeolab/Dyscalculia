from time import time
from typing import Any, Tuple, List, Optional, Dict
import random

from pandas import DataFrame

class PlayerEvaluator:
    def __init__(self) -> None:
        pass
    
    def set_running_results(self, running_results: Dict[str, Any]) -> None:
        self.running_results = running_results 

    def get_stats(self) -> Any:
        pass

    def get_trials(self) -> List[Any]:
        pass

    def update_statistics(self) -> None:
        pass

    
class SimpleEvaluator(PlayerEvaluator):
    def __init__(self, lookup_table: DataFrame, player_id: int, num_trials: int, history_size:int, alt_mode_weight: float = 0.0, fetched_samples: int = 16, selection_factor: int = 4):
        self.lookup_table = lookup_table
        self.player_id = player_id
        self.num_trials = num_trials
        self.history_size=history_size
        self.alt_mode_weight = alt_mode_weight
        self.fetched_samples = fetched_samples
        self.selected_samples = fetched_samples//selection_factor
        self.mode = "filtering"

    def get_stats(self) -> Any:
        return self.running_results[self.mode + "_diff"]
    
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
        matrix.append([float(r["NumLeft"]), float(r["NumRight"]), float(r["FieldAreaLeft"]), float(r["FieldAreaRight"]), float(r["ItemSurfaceAreaLeft"]), float(r["ItemSurfaceAreaRight"]),4,8,float(r["nd_LogRatio"]), float(r["nnd_LogRatio"])])
        #print("NUMBER OF TRIALS SENT: " + str(len(matrix)))

        #store the two difficulties for this trial (not available after client response)
        self.last_diffs = [r['Diff_coeff_filtering'], r['Difficulty Coefficient']]
        return matrix

    def update_statistics(self, correct: int, decision_time: float) -> None:
        self.running_results[self.mode + "_total"] += 1
        self.running_results[self.mode + "_correct"] += correct
        self.running_results[self.mode + "_acc"] = self.running_results[self.mode + "_correct"] / self.running_results[self.mode + "_total"]
        self.running_results[self.mode + "_total_time"] += decision_time
        self.running_results[self.mode + "_avg_time"] = self.running_results[self.mode + "_total_time"] / self.running_results[self.mode + "_total"]
        self.running_results[self.mode + "_history"].append(correct)

        if len(self.running_results[self.mode + "_history"]) > self.history_size : self.running_results[self.mode + "_history"].pop(0)

        steps = self._old_step(correct, decision_time, self.mode)

        for t_mode, step in zip(["filtering", "sharpening"], steps):
            if self.running_results[t_mode + "_diff"] + step > 1 :
                self.running_results[t_mode + "_diff"] = 0.99
            elif self.running_results[t_mode + "_diff"] + step < 0 :
                self.running_results[t_mode + "_diff"] = 0.01
            else:
                self.running_results[t_mode + "_diff"] += step
        
        if self.mode == "filtering" :
            self.mode = "sharpening"
        else :
            self.mode = "filtering"
        #print(f"{steps}, {self.running_results['filtering_diff']}, {self.running_results['sharpening_diff']}")
        #print(f"ld: {self.last_diffs}")
        #assert False == True

    def _old_step(self, correct: int, decision_time:float, mode:str) -> Tuple[float, float]:
        if len(self.running_results[self.mode + "_history"]) > self.history_size : self.running_results[self.mode + "_history"].pop(0)
            #print(self.running_results[self.mode + "_history"])

        step = 0.05 # increments difficulty 5% at a time
        if self.running_results[self.mode + "_acc"] >= 0.8 :
            if self.running_results[self.mode + "_diff"] + step < 1 :
                self.running_results[self.mode + "_diff"] += step

        elif self.running_results[self.mode + "_acc"] <= 0.5 :
            if self.running_results[self.mode + "_diff"] - step > 0 :
                self.running_results[self.mode + "_diff"] -= step
        
        if self.mode == "filtering":
            return step, 0.0
        else:
            return 0.0, step
                    
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
        return step_fi, step_sh

        
