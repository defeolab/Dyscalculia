import numpy as np
from sklearn.model_selection import KFold
from sklearn.svm import OneClassSVM
from sklearn.svm import LinearSVC
from typing import Tuple, List
from AI.AS_functionals import *
from AI.ai_utils import *
import math
from AI.ai_plot import plot_trials, plot_histograms
import scipy as sp
import os

DEBUG_D = False
DEBUG_S = False
DEBUG_PC = False
PATH_FOR_C_ABLATION = ".\\AI\\precomputed_data\\PDEP\\C_ablation"
PERFORM_ABLATION = False
C = 100

PATH_FOR_CONST = ".\\AI\\precomputed_data\\PDEP\\consts\\C.npy"

STD_COMPUTATION = "ll" #can be "ll" for loglilkelihood, "basic" for fetched formula 

#load constants from file
filepath = os.path.join(PATH_FOR_C_ABLATION, "best_Cs.npy")
BEST_CS : np.ndarray = np.load(filepath)

filepath = os.path.join(PATH_FOR_C_ABLATION, "configs.npy")
CONFIGS : np.ndarray = np.load(filepath)
CONFIGS[:, 0]/=90
CONFIGS[:, 1]/=0.5


filepath = os.path.join(PATH_FOR_C_ABLATION, "Cs.npy")
CS : np.ndarray = np.load(filepath)

filepath = os.path.join(PATH_FOR_C_ABLATION, "errors_by_Cs.npy")
ERR_CS : np.ndarray = np.load(filepath)

def mirror_trials_list(trials: List[np.ndarray], predictions: List[bool]) -> Tuple[List[np.ndarray], List[bool]]:
    n_t = []
    n_p = []

    for t, p in zip(trials,predictions):
        n_t.append(t)
        n_p.append(p)
        n_t.append(-t)
        n_p.append(p == False)
    
    return np.array(n_t), np.array(n_p)


def compute_sharpening_std_basic(c_trials: np.ndarray, c_predictions: np.ndarray, w_trials: np.ndarray, w_predictions: np.ndarray, norm: np.ndarray) -> float:
    n = c_trials.shape[0] + w_trials.shape[0]

    transform_mat=np.linalg.inv(np.array([[norm[0], norm[1]], [norm[1], -norm[0]]]))

    if w_trials.shape[0] != 0:
        dists = np.dot(transform_mat, w_trials.T)[1, :]
        sigma = 2*math.sqrt( (1/(n-1)) * np.sum(2*dists**2) )
    else:
        sigma = 0.05
    if DEBUG_S:
        cdists = np.dot(transform_mat, c_trials.T)[1,:]
        plot_histograms([cdists, dists])


    return sigma

def compute_log_likelihood(c_dists:np.ndarray, w_dists: np.ndarray, sigma:float) -> float:
    def custom_erf(x: np.ndarray) -> np.ndarray:
        return 0.5*sp.special.erf(x/(math.sqrt(2)*sigma)) - 0.5*sp.special.erf(-x/(math.sqrt(2)*sigma))
        #return 0.5 + 0.5*sp.special.erf(x/math.sqrt(2)*sigma)

    def correct_trial_likelihood(x: np.ndarray) -> np.ndarray:
        v = custom_erf(x)
        return np.clip(v + (1-v)/2, 0.0001, 0.9999)
    
    def wrong_trial_likelihood(x: np.ndarray) -> np.ndarray:
        v= 1-custom_erf(x)
        return np.clip(v/2, 0.0001, 0.9999)

    corrects_ll = np.log(correct_trial_likelihood(np.abs(c_dists))).sum() if c_dists.shape[0]>0 else 0.0
    wrongs_ll = np.log(wrong_trial_likelihood(np.abs(w_dists))).sum() if w_dists.shape[0]>0 else 0.0

    #print(f"-----{sigma}-----")
    #print(corrects_ll)
    #print(wrongs_ll)
    
    return corrects_ll + wrongs_ll
    


def compute_sharpening_std_loglikelihood(c_trials: np.ndarray, c_predictions: np.ndarray, w_trials: np.ndarray, w_predictions: np.ndarray, norm: np.ndarray) -> float:
    n = c_trials.shape[0] + w_trials.shape[0]

    transform_mat=np.linalg.inv(np.array([[norm[0], norm[1]], [norm[1], -norm[0]]]))
    c_dists = np.dot(transform_mat, c_trials.T)[1, :] if c_trials.shape[0] >0 else np.array([])
    w_dists = np.dot(transform_mat, w_trials.T)[1, :] if w_trials.shape[0] >0 else np.array([])


    n_sigmas = 20
    considered_sigmas = np.linspace(0.05, 0.60, n_sigmas)
    lls = np.ones(n_sigmas)

    for i,s in enumerate(considered_sigmas):
        ll = compute_log_likelihood(c_dists, w_dists, s)
        lls[i] = ll
    
    best_ll_i = np.argmax(lls)
    #print(lls)
    return considered_sigmas[best_ll_i]

def find_expected_optimal_C(prev_norm: np.ndarray, prev_sigma: float) -> float:
    if PERFORM_ABLATION:
        val = np.load(PATH_FOR_CONST)[0]
        return val
    prev_alpha =  math.degrees(angle_between(np.array([0,1]), prev_norm))
    
    dists = ((CONFIGS - np.array([prev_alpha/90, prev_sigma/0.5]))**2).sum(axis=1)
    curr_config_i = np.argmin(dists)

    
    return CS[BEST_CS[curr_config_i]]

def simple_denoising_clean_trials(trials: np.ndarray, predictions: np.ndarray, iterations: int, prev_norm: np.ndarray, prev_sigma: float) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray],  np.ndarray]:
    c_trials = trials
    c_predictions = predictions
    c_indexes =np.array([i for i in range(0, predictions.shape[0])])
    
    w_trials = []
    w_predictions = []
    w_indexes = []
    model = None
    target_C = find_expected_optimal_C(prev_norm, prev_sigma)
    for i in range(0, iterations):
        model = LinearSVC(dual=False, C= target_C)
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
    model = LinearSVC(dual=False, C= target_C)
    model.fit(c_trials, c_predictions)
    norm = unit_vector(np.array([-model.coef_[0][1], model.coef_[0][0]]))

    if abs(norm[0]) + abs(norm[1]) == abs(norm[0] + norm[1]):
        norm[0] = -0.1
        norm[1] = 0.9
        norm = unit_vector(norm)
    
    if DEBUG_D:
        t,c,a = return_plottable_list(c_trials, c_predictions)
        plot_trials(np.array([-1,1]), t, c, a, ann_str=True, estimated_boundary=norm)

        t,c,a = return_plottable_list(w_trials, w_predictions)
        plot_trials(np.array([-1,1]), t, c, a, ann_str=True, estimated_boundary=norm)  
    

    return (c_trials, c_predictions), (w_trials, w_predictions), norm

def simple_denoising_fixed_boundary(trials: np.ndarray, predictions: np.ndarray, norm: np.ndarray) -> Tuple[Tuple[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
    transform_mat=np.linalg.inv(np.array([[norm[0], norm[1]], [norm[1], -norm[0]]]))
    dists = np.dot(transform_mat, trials.T)[1, :]

    denoising_pred = (dists > 0) == predictions

    c_trials = trials[denoising_pred]
    c_preds = predictions[denoising_pred]

    w_trials = trials[denoising_pred == False]
    w_preds = predictions[denoising_pred == False]

    return (c_trials, c_preds), (w_trials, w_preds)

def produce_estimate_simple_denoising(trials: np.ndarray, predictions: np.ndarray, prev_norm: np.ndarray, prev_sigma: float)-> Tuple[float, float]:
        
    e_trials, e_predictions = mirror_trials_list(trials, predictions)
    
    if np.all(predictions) or np.all(predictions == False):
        #the recent trials contain only predictions for either left or right, data is not good enough to estimate boundary
        #Last detected boundary is reproposed instead

        norm = prev_norm
        (c_trials, c_predictions), (w_trials, w_predictions) = simple_denoising_fixed_boundary(e_trials, e_predictions, norm)
    else:
        (c_trials, c_predictions), (w_trials, w_predictions), norm = simple_denoising_clean_trials(e_trials, e_predictions, 1, prev_norm, prev_sigma)

    if DEBUG_D:
        t,c,a = return_plottable_list(e_trials, e_predictions)
        plot_trials(np.array([-1,1]), t, c, a, ann_str=True, estimated_boundary=norm)

    alpha =  math.degrees(angle_between(np.array([0,1]), norm))

    if w_trials.shape[0] == 0:
        #the recent trials and the predicted boundary did not detect any mispredicted sample due to sharpening
        #to be safe, the last detected sigma is reproposed
        sigma = prev_sigma 
    elif STD_COMPUTATION == "basic":
        sigma = compute_sharpening_std_basic(c_trials, c_predictions, w_trials, w_predictions, norm)
    elif STD_COMPUTATION == "ll":
        sigma = compute_sharpening_std_loglikelihood(c_trials, c_predictions, w_trials, w_predictions, norm)
    else:
        assert True == False, f"no sharpening computation selected"


    if DEBUG_PC and (alpha > 70 or alpha <25 or np.abs(sigma - prev_sigma) > 0.3):
        t,c,a = return_plottable_list(trials, predictions)
        plot_trials(prev_norm, t, c, a, ann_str=True, estimated_boundary=norm, sharp_std=prev_sigma, estimated_std=sigma)

        t,c,a = return_plottable_list(c_trials, c_predictions)
        plot_trials(norm, t, c, a, ann_str=True)

        t,c,a = return_plottable_list(w_trials, w_predictions)
        plot_trials(norm, t, c, a, ann_str=True)



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




