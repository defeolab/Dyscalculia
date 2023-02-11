import pygad
import numpy as np
import math
import scipy as sp
from scipy import integrate
from scipy.optimize import fmin_l_bfgs_b
from AI.ai_utils import *


from typing import Callable, Tuple, List

import warnings

warnings.filterwarnings("ignore", message="The integral is probably divergent, or slowly convergent.")



#constants for genetic algorithm
N_GENERATIONS = 10                   #iterations of the algorithm
N_PARENTS_MATING = 4                #number of parents selected for mating
SOL_PER_POP = 6                     #number of individuals in surviving population
N_GENES = 2                         #length of the genome (2: nd and nnd)
PARENT_SELECTION_TYPE = "sss"
KEEP_PARENTS = 1
CROSSOVER_TYPE = "single_point"

MUTATION_TYPE = "random"
MUTATION_PERCENT_GENES = 10

#paramteres for error probability computation
PROBABILITY_COMPUTATION_TYPE = "1d" #"1d" for the one dimensional approximation, "2d" for the two dimensional integral approximation


def compute_error_probability_2d(trial_vec: np.ndarray, sigma: float, integral_bound:float, ax: Callable):
    """
        this function computes the approximated probability that the player defined by the decision_matrix (filtering) 
        and the sigma_coefficient (sharpening) predicts the trial defined by nd and nnd variables incorrectly
    """

    gauss_func = lambda y,x : math.exp(-0.5*(1/(sigma**2))*(((x-trial_vec[0])**2)+((y-trial_vec[1])**2)))

    total_area, _ = integrate.dblquad(gauss_func, -integral_bound,integral_bound,-integral_bound,integral_bound)

    if trial_vec[0] < 0:
        error_area, _ =  integrate.dblquad(gauss_func, -integral_bound, integral_bound, ax, integral_bound)
    else:
        error_area, _ =  integrate.dblquad(gauss_func, -integral_bound, integral_bound,-integral_bound, ax)

    return error_area/total_area

def compute_error_probability_1d(trial_vec:np.ndarray, sigma: float, transform_mat: np.ndarray):
    dist = np.dot(transform_mat, vcol(trial_vec))[1, 0]

    if (trial_vec[0] > 0 and dist > 0) or (trial_vec[0]<0 and dist <0):
        return  (1-custom_erf(np.abs(dist), sigma))/2
    else:
        val = custom_erf(np.abs(dist), sigma)
        return val + (1-val)/2
    
def global_fitness_score(trial_vec: np.ndarray, target_error_prob: float, target_perceived_diff: float, sigma: float, transform_mat: np.ndarray, max_dec_score: float):
    return  np.abs(target_error_prob-compute_error_probability_1d(trial_vec, sigma,transform_mat)) + \
            0.2*np.abs(target_perceived_diff-compute_perceived_difficulty(trial_vec, transform_mat, max_dec_score)) 
    
def global_ga_fitness(trial_vec: np.ndarray, trial_idx: int, target_error_prob: float,  target_perceived_diff:float, sigma:float, transform_mat:np.ndarray):
    return np.clip(1/global_fitness_score(trial_vec, target_error_prob, target_perceived_diff, sigma, transform_mat),0.001, 1000)

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

    if PROBABILITY_COMPUTATION_TYPE == "2d":
        prob_func = lambda x: compute_error_probability_2d(x, sigma, integral_bound, ax)
    else:
        prob_func = lambda x: compute_error_probability_1d(x,sigma,decision_matrix)

    diff_func = lambda x: compute_perceived_difficulty(x, decision_matrix, max_decision_score)
    
    def fitness_score(trial_vec: np.ndarray):
        return  np.abs(target_error_prob-prob_func(trial_vec)) + \
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