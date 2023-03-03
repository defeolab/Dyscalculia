from AI.PDEP_functionals import PDEP_find_trial
import numpy as np

class PDEP_TrialProposer:
    def __init__(self) -> None:
        pass
    
    def find_trial(self,target_error_prob:float,target_perceived_diff:float, transform_mat:np.ndarray, boundary_vector:np.ndarray, sigma:float, norm_feats:bool):
        return PDEP_find_trial(target_error_prob,target_perceived_diff, transform_mat, boundary_vector,sigma,norm_feats)