import numpy as np
import math
import numpy.random
import scipy as sp
from scipy import integrate
from scipy.optimize import fmin_l_bfgs_b


from typing import Callable, Tuple, List

import warnings

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
