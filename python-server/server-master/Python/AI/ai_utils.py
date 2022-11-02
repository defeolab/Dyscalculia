import numpy as np
import math
import numpy.random
import scipy as sp
from scipy import integrate

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

def vcol(vec: np.ndarray) -> np.ndarray:
    return vec.reshape((vec.size,1))


def PAD_find_trial(target_error_prob: float, target_error_diff: float, decision_matrix: np.ndarray, boundary_vector: np.ndarray, sigma: float):
    
    a = float(boundary_vector[1]/boundary_vector[0])
    ax = lambda x: x*a

    integral_bound = 5

    def compute_error_probability(nd_variable: float, nnd_variable: float):
        """
            this function computes the approximated probability that the player defined by the decision_matrix (filtering) 
            and the sigma_coefficient (sharpening) predicts the trial defined by nd and nnd variables incorrectly
        """

        gauss_func = lambda y,x : math.exp(-0.5*(1/(sigma**2))*(((x-nd_variable)**2)+((y-nnd_variable)**2)))

        total_area = integrate.dblquad(gauss_func, -integral_bound,integral_bound,-integral_bound,integral_bound)
        error_area_quad2 =  integrate.dblquad(gauss_func, -integral_bound,0, ax, integral_bound)
        error_area_quad4 = integrate.dblquad(gauss_func, 0, integral_bound, -integral_bound, ax)

        return (error_area_quad2+error_area_quad4)/total_area
    





