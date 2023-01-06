from typing import Tuple, Any, List
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

#utility functions for other files
def find_best_fit(data_x: np.ndarray, data_y: np.ndarray) -> Tuple[Any, str]:
    target_funcs = [_fit_poly_1D, _fit_poly_2D]
    func_label = ["poly_1D", "poly_2D"]

    pars_list = []
    qualities = np.zeros(len(target_funcs))

    for i, func in enumerate(target_funcs):
        pars, quality = func(data_x, data_y)
        pars_list.append(pars)
        qualities[i] = quality

    best_fit_i = np.argmin(qualities)

    return pars_list[best_fit_i], func_label[best_fit_i]

def poly_fitted_data_from_parameters(data_x: np.ndarray, pars: List[float]) -> np.ndarray:
    val = np.zeros(data_x.shape[0])
    max_deg = len(pars)-1

    for i in range(0, len(pars)):
        val += np.power(data_x, max_deg-i)*pars[i]
    
    return val


def _fit_poly_1D(data_x: np.ndarray, data_y: np.ndarray)-> Tuple[Any, float]:
    #calculate best 1D polynomial description of the data and return its quality in terms of avg distance
    pars = np.polyfit(data_x, data_y, 1)
    fitted_values = poly_fitted_data_from_parameters(data_x, pars)

    return pars, np.linalg.norm(fitted_values-data_y)

def _fit_poly_2D(data_x: np.ndarray, data_y: np.ndarray)-> Tuple[Any, float]:
    #calculate best 2D polynomial description of the data and return its quality in terms of avg distance
    pars = np.polyfit(data_x, data_y, 2)

    fitted_values = poly_fitted_data_from_parameters(data_x, pars)

    return pars, np.linalg.norm(fitted_values-data_y)
    
