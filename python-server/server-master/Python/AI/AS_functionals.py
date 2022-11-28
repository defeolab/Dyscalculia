import numpy as np
from sklearn.model_selection import KFold
from sklearn.svm import OneClassSVM
from sklearn.svm import LinearSVC
from typing import Tuple, List
from AI.AS_functionals import *
from AI.ai_utils import *
import math
from AI.ai_plot import plot_trials, plot_histograms

DEBUG_D = True
DEBUG_S = False

def mirror_trials_list(trials: List[np.ndarray], predictions: List[bool]) -> Tuple[List[np.ndarray], List[bool]]:
    n_t = []
    n_p = []

    for t, p in zip(trials,predictions):
        n_t.append(t)
        n_p.append(p)
        n_t.append(-t)
        n_p.append(p == False)
    
    return np.array(n_t), np.array(n_p)


def compute_sharpening_std(c_trials: np.ndarray, c_predictions: np.ndarray, w_trials: np.ndarray, w_predictions: np.ndarray, norm: np.ndarray) -> float:
    n = c_trials.shape[0] + w_trials.shape[0]

    transform_mat=np.linalg.inv(np.array([[norm[0], norm[1]], [norm[1], -norm[0]]]))

    dists = np.dot(transform_mat, w_trials.T)[1, :]
    sigma = 2*math.sqrt( (1/(n-1)) * np.sum(2*dists**2) )

    if DEBUG_S:
        cdists = np.dot(transform_mat, c_trials.T)[1,:]
        plot_histograms([cdists, dists])


    return sigma




def simple_denoising_clean_trials(trials: np.ndarray, predictions: np.ndarray, iterations: int) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray],  np.ndarray]:
    c_trials = trials
    c_predictions = predictions
    c_indexes =np.array([i for i in range(0, predictions.shape[0])])
    
    w_trials = []
    w_predictions = []
    w_indexes = []
    model = None
    for i in range(0, iterations):
        model = LinearSVC(dual=False)
        model.fit(c_trials, c_predictions)

        lw_indexes = model.predict(c_trials) != c_predictions
        if np.any(lw_indexes) == False:
            break
        
        w_indexes.append(c_indexes[lw_indexes])

        c_trials = c_trials[lw_indexes == False]
        c_predictions = c_predictions[lw_indexes == False]
        c_indexes = c_indexes[lw_indexes == False]

    for lw in w_indexes:
        for i in lw:
            w_trials.append(trials[i])
            w_predictions.append(predictions[i])

    w_trials = np.array(w_trials)
    w_predictions = np.array(w_predictions)
    model = LinearSVC(dual=False)
    model.fit(c_trials, c_predictions)
    norm = unit_vector(np.array([-model.coef_[0][1], model.coef_[0][0]]))
    
    if DEBUG_D:
        t,c,a = return_plottable_list(c_trials, c_predictions)
        plot_trials(norm, t, c, a, ann_str=True)

        t,c,a = return_plottable_list(w_trials, w_predictions)
        plot_trials(norm, t, c, a, ann_str=True)  
    
    
    

    return (c_trials, c_predictions), (w_trials, w_predictions), norm


def produce_estimate_simple_denoising(trials: np.ndarray, predictions: np.ndarray)-> Tuple[float, float]:

    e_trials, e_predictions = mirror_trials_list(trials, predictions)
    
    (c_trials, c_predictions), (w_trials, w_predictions), norm = simple_denoising_clean_trials(e_trials, e_predictions, 5)

    alpha =  math.degrees(angle_between(np.array([0,1]), norm))
    sigma = compute_sharpening_std(c_trials, c_predictions, w_trials, w_predictions, norm)

    return alpha, sigma, norm




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

    

    if DEBUG_D:
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

    angle =  math.degrees(angle_between(norm, np.array([0,1])))

    return angle, 0.1




