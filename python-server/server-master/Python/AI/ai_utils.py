import numpy as np
import math
import numpy.random
import scipy as sp
from scipy import integrate
from scipy.optimize import fmin_l_bfgs_b
import random

from typing import Callable, Tuple, List

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    rads = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    return rads

def get_mock_trials(trials: int):
    nd_range = np.linspace(-1.5, 1.5, num = int(math.sqrt(trials)))
    nnd_range = np.linspace(-1.5, 1.5, num = int(math.sqrt(trials)))

    ret = []

    for nd in nd_range:
        for nnd in nnd_range:
            ret.append([-1,-1,-1,-1,-1,-1,-1,-1,nd, nnd])

    return ret


def compute_nd_nnd_coords(trial_left: List[float], trial_right: List[float]) -> Tuple[float, float]:
    #formula specified by previous thesis writers
    #NND = (0.577+0.467∗Number)∗(FA/Number) +(0.487+0.473∗Number)∗ISA
    nnd_right = (0.577+0.467*trial_right[0])*(trial_right[1]/trial_right[0]) + (0.487+0.473*trial_right[0])*trial_right[2]
    nnd_left = (0.577+0.467*trial_left[0])*(trial_left[1]/trial_left[0]) + (0.487+0.473*trial_left[0])*trial_left[2]

    return np.log10(trial_right[0]/trial_left[0]), np.log10(nnd_right/nnd_left)

def vcol(vec: np.ndarray) -> np.ndarray:
    return vec.reshape((vec.size,1))

def compute_error_probability(nd_variable: float, nnd_variable: float, sigma: float, integral_bound:float, ax: Callable):
    """
        this function computes the approximated probability that the player defined by the decision_matrix (filtering) 
        and the sigma_coefficient (sharpening) predicts the trial defined by nd and nnd variables incorrectly
    """

    gauss_func = lambda y,x : math.exp(-0.5*(1/(sigma**2))*(((x-nd_variable)**2)+((y-nnd_variable)**2)))

    total_area, _ = integrate.dblquad(gauss_func, -integral_bound,integral_bound,-integral_bound,integral_bound)

    if nd_variable < 0:
        error_area, _ =  integrate.dblquad(gauss_func, -integral_bound, integral_bound, ax, integral_bound)
    else:
        error_area, _ =  integrate.dblquad(gauss_func, -integral_bound, integral_bound,-integral_bound, ax)

    return error_area/total_area

def compute_perceived_difficulty(trial_vec: np.ndarray, decision_matrix: np.ndarray, max_decision_score: float):
        
    #transform vector in the decision space
    trial_vec = np.dot(decision_matrix, vcol(trial_vec))

    decision_score = float(trial_vec[1])

    #normalize
    decision_score = decision_score/max_decision_score
    return 1-decision_score

def PAD_find_trial(target_error_prob: float, target_perceived_diff: float, decision_matrix: np.ndarray, boundary_vector: np.ndarray, sigma: float) -> Tuple[float, float,float]:
    
    a = float(boundary_vector[1]/boundary_vector[0])
    ax = lambda x: x*a

    integral_bound = 5
    max_decision_score = 2*math.sqrt(2)
    nd_bound = 2
    nnd_bound = 2

    prob_func = lambda x, y: compute_error_probability(x,y, sigma, integral_bound, ax)
    diff_func = lambda x: compute_perceived_difficulty(x, decision_matrix, max_decision_score)
    
    def optimality_score(trial_vec: np.ndarray):
        return np.abs(target_error_prob-prob_func(trial_vec[0], trial_vec[1])) #+(target_perceived_diff-diff_func(trial_vec)) 
    
    #better to chose the quadrant where to search (i.e. congruent or incongruent trial)
    #this is to avoid the solver to get stuck (the points in the axis are not differentiable, gradients are weird)
    """
    congruent = bool(random.getrandbits(1))
    congruent = False if target_error_prob > 0.5 else True
    if congruent:
        bounds = [(0.1, nd_bound ), (0, nnd_bound)]
        x0 = np.array([np.random.uniform(0.05, nd_bound), np.random.uniform(0, nnd_bound)])
    else:
        bounds = [(-nd_bound, -0.1 ), (0, nnd_bound)]
        x0 = np.array([np.random.uniform(-nd_bound, -0.05), np.random.uniform(0, nnd_bound)])
    """
    bounds = [(-nd_bound, nd_bound ), (0, nnd_bound)]
    x0 = np.array([np.random.uniform(-nd_bound, nd_bound), np.random.uniform(0, nnd_bound)])

    x, last_val, d = fmin_l_bfgs_b(optimality_score, x0, approx_grad = True, iprint=0, bounds = bounds, maxiter=2000)

    return x[0], x[1], last_val




