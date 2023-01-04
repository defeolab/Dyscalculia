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

    def get_trial(self) -> Tuple[np.ndarray, float]:
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

    def second_pass_estimation(self, alpha_data: List[float], sigma_data: List[float])-> Tuple[List[float], List[float], List[np.ndarray]]:
        n_samples = len(alpha_data)
        trials = np.array(self.trials[-n_samples:])
        predictions = np.array(self.predictions[-n_samples:])

        ret_alphas = []
        ret_sigmas = []
        ret_norms = []

        for i in range(0, n_samples):
            lower_bound, upper_bound = fetch_estimation_window(i, alpha_data, sigma_data, self.max_trials_to_consider)
            target_trials = trials[lower_bound:upper_bound]
            target_predictions = predictions[lower_bound:upper_bound]

            #print(f"target with shape {target_trials.shape}, max was {self.max_trials_to_consider}, maxL was {trials.shape}, i: {i}")
            if self.denoiser_type == "OneClassSVM":
                (curr_alpha, curr_sigma, curr_norm) = produce_estimate_denoising_OCSVM(target_trials, target_predictions)

            elif self.denoiser_type == "simple_denoising":
                prev_norm = ret_norms[i-1] if i != 0 else np.array(unit_vector([-1, 1]))
                prev_sigma = ret_sigmas[i-1] if i != 0 else 0.3
                (curr_alpha, curr_sigma, curr_norm) = produce_estimate_simple_denoising(target_trials, target_predictions, prev_norm, prev_sigma)


            ret_alphas.append(curr_alpha)
            ret_sigmas.append(curr_sigma)
            ret_norms.append(curr_norm)
        
        return ret_alphas, ret_sigmas, ret_norms

#unused
class ASE_Estimator(Estimator_Interface):
    def __init__(self, n_trials_per_cycle: int = 10, max_trials_to_consider: int = 90):
        super().__init__()
        self.n_trials_per_cycle = n_trials_per_cycle
        self.max_trials_to_consider = max_trials_to_consider
        self.i = 0

    def get_trial(self) -> Tuple[np.ndarray, float]:
        random_scalar = np.random.normal(scale = self.curr_sigma)
        return random_scalar*self.target_line, random_scalar

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
            self.prev_sigma = prev_sigma
            self.i+=1
            return (self.curr_alpha, prev_sigma, self.curr_bv), "estimate"
        else:
            #process last trial
            self.i += 1

            self.sigma_trials.append(self.trials[-1])
            self.sigma_predictions.append(self.predictions[-1])

            e_trials, e_predictions = mirror_trials_list(np.array(self.sigma_trials), np.array(self.sigma_predictions))

            (c_trials, c_predictions), (w_trials, w_predictions) = simple_denoising_fixed_boundary(e_trials, e_predictions, self.curr_bv)

            ith_sigma = compute_sharpening_std_loglikelihood(c_trials, c_predictions, w_trials, w_predictions, self.curr_bv)
            ith_sigma = np.clip(ith_sigma, 0.02, 1.0)
            if self.i % self.n_trials_per_cycle == 0:
                #end of estimation phase
                #reestimate alpha with sigma knowledge

                trials = np.array(self.trials[-(self.max_trials_to_consider + self.n_trials_per_cycle):])
                predictions = np.array(self.predictions[-(self.max_trials_to_consider + self.n_trials_per_cycle):])
                e_trials, e_predictions = mirror_trials_list(trials, predictions)
                (_, _), (_,_), self.curr_bv = simple_denoising_clean_trials(e_trials, e_predictions, 1, self.curr_bv, ith_sigma)

                final_alpha = math.degrees(angle_between(np.array([0,1]),self.curr_bv))
                #print("end")
                self.i = 0
                return (final_alpha, ith_sigma, self.curr_bv), "support"

            else:
                #print("not end")
                #in between of estimation phase
                self.curr_sigma = (self.curr_sigma + ith_sigma)/2
                return (self.curr_alpha, self.prev_sigma, self.curr_bv), "estimate"


