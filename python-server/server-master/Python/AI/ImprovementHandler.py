from typing import Tuple
import numpy as np

class ImprovementHandler:
    def __init__(self, improve_interval: int, add_noise: bool) -> None:
        self.improve_interval = improve_interval
        self.add_noise = add_noise
        self.number_of_calls = 0
        
    def improve(self,  curr_alpha: float, curr_sigma: float) -> Tuple[float, float]:
        pass
    

class Linear_IH(ImprovementHandler):
    def __init__(self, improve_interval: int, add_noise: bool, slope_alpha: float, slope_sigma: float) -> None:
        super().__init__(improve_interval, add_noise)
        self.slope_alpha = slope_alpha
        self.slope_sigma = slope_sigma

    def improve(self, curr_alpha: float, curr_sigma: float) -> Tuple[float, float]:
        self.number_of_calls += 1
        if self.number_of_calls % self.improve_interval == 0:
            return curr_alpha + self.slope_alpha, curr_sigma + self.slope_sigma
        else:
            return curr_alpha, curr_sigma


class Normal_IH(ImprovementHandler):
    def __init__(self, improve_interval: int, add_noise: bool, alpha_std: float, sigma_std: float) -> None:
        super().__init__(improve_interval, add_noise)
        self.alpha_std = alpha_std
        self.sigma_std = sigma_std
    
    def improve(self, curr_alpha: float, curr_sigma: float) -> Tuple[float, float]:
        self.number_of_calls += 1
        if self.number_of_calls % self.improve_interval == 0:
            next_alpha = curr_alpha - np.abs(np.random.normal(scale= self.alpha_std))
            next_sigma = curr_sigma - np.abs(np.random.normal(scale= self.sigma_std))

            return next_alpha, next_sigma
        else:
            return curr_alpha, curr_sigma