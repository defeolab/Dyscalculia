import numpy as np
from sklearn.model_selection import KFold
from sklearn.svm import OneClassSVM
from sklearn.svm import LinearSVC
from typing import Tuple, List
from AI.AS_functionals import *
from AI.ai_utils import *
import math
from AI.ai_plot import plot_trials

DEBUG = True

def mirror_trials_list(trials: List[np.ndarray], predictions: List[bool]) -> Tuple[List[np.ndarray], List[bool]]:
    n_t = []
    n_p = []

    for t, p in zip(trials,predictions):
        n_t.append(t)
        n_p.append(p)
        n_t.append(-t)
        n_p.append(p == False)
    
    return np.array(n_t), np.array(n_p)

def produce_estimate_no_denoising(trials: np.ndarray, predictions: np.ndarray)-> Tuple[float, float]:
    model = LinearSVC()

    e_trials, e_predictions = mirror_trials_list(trials, predictions)

    model.fit(e_trials, e_predictions)

    norm = unit_vector(np.array([-model.coef_[0][1], model.coef_[0][0]]))

    angle =  math.degrees(np.dot(norm, np.array([0,1])))

    return angle, 0.1




def denoise_data_OCSVM(trials: np.ndarray, predictions: np.ndarray) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:

    right_trials = trials[predictions == 1]
    left_trials = trials[predictions == 0]

    model = OneClassSVM(kernel="linear", gamma = 0.001, nu = 0.03)
    model.fit(left_trials)
    mask_left = model.predict(left_trials)

    model = OneClassSVM(kernel="linear", gamma = 0.001, nu = 0.03)
    model.fit(right_trials)
    mask_right = model.predict(right_trials)

    safe_t_right = right_trials[mask_right == 1]
    safe_t_left = left_trials[mask_left == 1]
    
    anomaly_t_right = right_trials[mask_right == -1]
    anomaly_t_left = left_trials[mask_left == -1]

    ret_t_safe = np.concatenate((safe_t_right, safe_t_left), axis = 0)
    ret_p_safe = np.array([True for i in range(0, safe_t_right.shape[0])] + [False for i in range(0, safe_t_left.shape[0])])

    ret_t_anomaly = np.concatenate((anomaly_t_right, anomaly_t_left), axis = 0)
    ret_p_anomaly = np.array([True for i in range(0, anomaly_t_right.shape[0])] + [False for i in range(0, anomaly_t_left.shape[0])])

    

    if DEBUG:
        t,c,a = return_plottable_list(ret_t_safe, ret_p_safe)
        plot_trials([-1,1], t, c, a, ann_str=True)

        t,c,a = return_plottable_list(ret_t_anomaly, ret_p_anomaly)
        plot_trials([-1,1], t, c, a, ann_str=True)

        


    return (ret_t_safe, ret_p_safe), (ret_t_anomaly, ret_p_anomaly)





def produce_estimate_denoising_OCSVM(trials: np.ndarray, predictions: np.ndarray)-> Tuple[float, float]:
    model = LinearSVC()

    (safe_trials, safe_predictions), (anomaly_trials, anomaly_predictions) = denoise_data_OCSVM(trials, predictions)

    e_trials, e_predictions = mirror_trials_list(safe_trials, safe_predictions)

    model.fit(e_trials, e_predictions)

    norm = unit_vector(np.array([-model.coef_[0][1], model.coef_[0][0]]))

    angle =  math.degrees(np.dot(norm, np.array([0,1])))

    return angle, 0.1




