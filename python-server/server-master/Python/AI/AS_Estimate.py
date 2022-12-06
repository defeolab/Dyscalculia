import numpy as np
from sklearn.model_selection import KFold
from sklearn.svm import OneClassSVM
from sklearn.svm import LinearSVC
from typing import Tuple, List
from AI.AS_functionals import *
from AI.ai_utils import *
import math

class ASD_Estimator:
    """
        Alpha and sigma estimator based on anomaly detection (denoising):
            first, the trials that are misinterpreted due to sharpening effect are detected through anomaly detection.
            then, filtering is found from the trials that were not misinterpreted.
            finally, sharpening std is derived from the found alpha and the misinterpreted samples

        Can come in several versions:
            for now only shallow detection through OneClassSVM
    """


    def __init__(self, max_trials_to_consider: int = 50, denoiser_type: str = "OneClassSVM"):
        self.trials: List[np.ndarray] = []
        self.predictions: List[bool] = []
        self.max_trials_to_consider = max_trials_to_consider
        self.denoiser_type = denoiser_type

    def get_trial(self) -> Tuple[float, float]:
        pass

    def append_trial(self, trial: List[float]) -> None:
        self.trials.append(trial)

    def append_prediction(self, predicted_right: bool) -> None:
        self.predictions.append(predicted_right)

    def produce_estimate(self, prev_norm: np.ndarray, prev_sigma: np.ndarray) -> Tuple[float, float]:
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