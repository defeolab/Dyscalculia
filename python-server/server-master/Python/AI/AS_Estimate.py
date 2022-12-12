import numpy as np
from sklearn.model_selection import KFold
from sklearn.svm import OneClassSVM
from sklearn.svm import LinearSVC
from typing import Tuple, List
from AI.AS_functionals import *
from AI.ai_utils import *
import math

class Estimator_Interface:
    def __init__(self):
        self.trials: List[np.ndarray] = []
        self.predictions: List[bool] = []

    def get_trial(self) -> np.ndarray:
        pass

    def append_trial(self, trial: List[float], mode: str) -> None:
        self.trials.append(trial)

    def append_prediction(self, predicted_right: bool, mode: str) -> None:
        self.predictions.append(predicted_right)

    def produce_estimate(self, prev_norm: np.ndarray, prev_sigma: np.ndarray) -> Tuple[float, float, np.ndarray, str]:
        pass


class ASD_Estimator(Estimator_Interface):
    """
        Alpha and sigma estimator based on anomaly detection (denoising):
            first, the trials that are misinterpreted due to sharpening effect are detected through anomaly detection.
            then, filtering is found from the trials that were not misinterpreted.
            finally, sharpening std is derived from the found alpha and the misinterpreted samples

        Can come in several versions:
            for now only shallow detection through OneClassSVM
    """


    def __init__(self, max_trials_to_consider: int = 50, denoiser_type: str = "OneClassSVM"):
        super().__init__()
        self.max_trials_to_consider = max_trials_to_consider
        self.denoiser_type = denoiser_type

    def produce_estimate(self, prev_norm: np.ndarray, prev_sigma: np.ndarray) -> Tuple[float, float, np.ndarray, str]:
        """
            Given the previous trials, perform alpha and sigma estimation
        """
        trials = np.array(self.trials[-self.max_trials_to_consider:])
        predictions = np.array(self.predictions[-self.max_trials_to_consider:])


        if self.denoiser_type == "OneClassSVM":
            return produce_estimate_denoising_OCSVM(trials, predictions), "support"

        elif self.denoiser_type == "simple_denoising":
            return produce_estimate_simple_denoising(trials, predictions, prev_norm, prev_sigma), "support"
            


        return 45.0, 0.1, unit_vector(np.array([-1,1])), "support"        


#TODO estimator with esplicit trial suggestion like professor asked
class ASE_Estimator(Estimator_Interface):
    def __init__(self, n_trials_per_cycle: int = 10, max_trials_to_consider: int = 90):
        super().__init__()
        self.n_trials_per_cycle = n_trials_per_cycle
        self.max_trials_to_consider = max_trials_to_consider
        self.i = 0

    def get_trial(self) -> np.ndarray:
        random_scalar = np.random.normal(scale = self.curr_sigma)
        return random_scalar*self.target_line

    def produce_estimate(self, prev_norm: np.ndarray, prev_sigma: np.ndarray) -> Tuple[float, float, np.ndarray, str]:
        
        if self.i == 0:
            #start estimation phase
            trials = np.array(self.trials[-self.max_trials_to_consider:])
            predictions = np.array(self.predictions[-self.max_trials_to_consider:])
            e_trials, e_predictions = mirror_trials_list(trials, predictions)
            (_, _), (_,_), self.curr_bv = simple_denoising_clean_trials(e_trials, e_predictions, 1, prev_norm, prev_sigma)

            self.curr_alpha = math.degrees(angle_between(np.array([0,1]),self.curr_bv))

            self.target_line = np.array([self.curr_bv[1], -self.curr_bv[0]])

            self.sigma_trials = []
            self.sigma_predictions = []

            self.curr_sigma = prev_sigma

            return self.curr_alpha, prev_sigma, self.curr_bv, "estimate"
        else:
            #process last trial
            self.i += 1

            self.sigma_trials.append(self.trials[-1])
            self.sigma_predictions.append(self.predictions[-1])

            e_trials, e_predictions = mirror_trials_list(np.array(self.sigma_trials), np.array(self.sigma_predictions))

            (c_trials, c_predictions), (w_trials, w_predictions) = simple_denoising_fixed_boundary(e_trials, e_predictions, self.curr_bv)

            ith_sigma = compute_sharpening_std_loglikelihood(c_trials, c_predictions, w_trials, w_predictions, self.curr_bv)

            if self.i % self.n_trials_per_cycle == 0:
                #end of estimation phase
                #reestimate alpha with sigma knowledge

                trials = np.array(self.trials[-(self.max_trials_to_consider + self.n_trials_per_cycle):])
                predictions = np.array(self.predictions[-(self.max_trials_to_consider + self.n_trials_per_cycle):])
                e_trials, e_predictions = mirror_trials_list(trials, predictions)
                (_, _), (_,_), self.curr_bv = simple_denoising_clean_trials(e_trials, e_predictions, 1, self.curr_bv, ith_sigma)

                final_alpha = math.degrees(angle_between(np.array([0,1]),self.curr_bv))

                return final_alpha, ith_sigma, self.curr_bv, "support"

            else:
                #in between of estimation phase
                self.curr_sigma += 0.05 if ith_sigma > self.curr_sigma else -0.05
                return self.curr_alpha, self.curr_sigma, self.curr_bv, "estimate"


