import numpy as np
import math
import numpy.random
import scipy as sp
from scipy import integrate
from scipy.optimize import fmin_l_bfgs_b
import random
import pygad

from typing import Callable, Tuple, List

import warnings
warnings.filterwarnings("ignore", message="The integral is probably divergent, or slowly convergent.")

#constants for genetic algorithm
N_GENERATIONS = 5                   #iterations of the algorithm
N_PARENTS_MATING = 4                #number of parents selected for mating
SOL_PER_POP = 6                     #number of individuals in surviving population
N_GENES = 2                         #length of the genome (2: nd and nnd)
PARENT_SELECTION_TYPE = "sss"
KEEP_PARENTS = 1
CROSSOVER_TYPE = "single_point"

MUTATION_TYPE = "random"
MUTATION_PERCENT_GENES = 10


def to_mock_trial(nd: float, nnd: float):
    return [-1,-1,-1,-1,-1,-1,-1,-1,nd, nnd]

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

def return_plottable_list( list, corrects=None):
        nl =  []
        for r in list:
            nl.append(to_mock_trial(r[0], r[1]))
        if corrects is None:
            c = [True for i in range(0, len(nl))]
        else:
            c=[]
            for b in corrects:
                c.append(b)
        a = ["" for i in range(0, len(nl))]

        return nl, c, a

def get_mock_trials(trials: int, norm_feats:bool):
    bounds = [-0.75, 0.75] if norm_feats else [-1.5, 1.5]

    nd_range = np.linspace(bounds[0], bounds[1], num = int(math.sqrt(trials)))
    nnd_range = np.linspace(bounds[0], bounds[1], num = int(math.sqrt(trials)))

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

    decision_score = float(np.abs(trial_vec[1]))

    #normalize
    decision_score = decision_score/max_decision_score
    return 1-decision_score

def PDEP_find_trial(target_error_prob: float, target_perceived_diff: float, decision_matrix: np.ndarray, boundary_vector: np.ndarray, sigma: float, norm_feats: bool) -> Tuple[float, float,float]:
    
    a = float(boundary_vector[1]/boundary_vector[0])
    ax = lambda x: x*a

    integral_bound = 5
    max_decision_score = 2*math.sqrt(2)
    if norm_feats:
        nd_bound = 1
        nnd_bound = 1
    else:
        nd_bound = 2
        nnd_bound = 2

    prob_func = lambda x, y: compute_error_probability(x,y, sigma, integral_bound, ax)
    diff_func = lambda x: compute_perceived_difficulty(x, decision_matrix, max_decision_score)
    
    def fitness_score(trial_vec: np.ndarray):
        return  np.abs(target_error_prob-prob_func(trial_vec[0], trial_vec[1])) + \
                0.2*np.abs(target_perceived_diff-diff_func(trial_vec)) 
    
    def ga_fitness(trial_vec: np.ndarray, trial_idx: int):
        return np.clip(1/fitness_score(trial_vec),0.001, 1000)
    
    
    """
    #solution using gradiant based solver
    bounds = [(-nd_bound, nd_bound ), (0, nnd_bound)]
    x0 = np.array([np.random.uniform(-nd_bound, nd_bound), np.random.uniform(0, nnd_bound)])

    solution, solution_fitness, solution_idx = fmin_l_bfgs_b(fitness_score, x0, approx_grad = True, 
                    iprint=0, bounds = bounds, maxiter=2000)
    """

    gene_space = [{'low': -nd_bound, 'high': nd_bound}, {'low': 0, 'high': nnd_bound}]

    #solution with GA
    ga_instance = pygad.GA(num_generations=N_GENERATIONS,
                       num_parents_mating=N_PARENTS_MATING,
                       fitness_func=ga_fitness,
                       sol_per_pop=SOL_PER_POP,
                       num_genes=N_GENES,
                       gene_space=gene_space,
                       parent_selection_type=PARENT_SELECTION_TYPE,
                       keep_parents=KEEP_PARENTS,
                       crossover_type=CROSSOVER_TYPE,
                       mutation_type=MUTATION_TYPE,
                       mutation_percent_genes=MUTATION_PERCENT_GENES,
                       suppress_warnings=True)

    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    solution_fitness = 1/solution_fitness

    #search space is only in the top part of the nd - nnd space to help computations. Randomly mirror it in order to get the specular trial
    if np.random.uniform(0, 1) >0.5:
        solution = -solution

    return solution[0], solution[1], solution_fitness




