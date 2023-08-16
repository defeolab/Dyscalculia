import pandas
import itertools as it
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA
import numpy as np
from typing import Tuple, List

def get_PCA_pars(valid_values: pandas.DataFrame) -> Tuple[TruncatedSVD, np.ndarray]:
    pars = []
    j=0
    for i,t in valid_values.iterrows():
        pars.append([float(t[1].replace(",", ".")), float(t[2].replace(",", "."))])
        j=i
    pars = np.array(pars)

    #print(i)
    mean = pars.mean(axis=0)
    #print(mean)
    pars = pars/mean
    pca = TruncatedSVD(n_components=1)

    pca.fit(pars)

    return pca, mean

def compute_ND_NND(pca: TruncatedSVD, mean:np.ndarray, t_right: List[float], t_left: List[float]) -> Tuple[float, float]:
    n_right = t_right[0]
    n_left = t_left[0]

    t_right_np = np.array([[t_right[1], t_right[2]]])/mean
    t_left_np = np.array([[t_left[1], t_left[2]]])/mean

    print(t_right_np)

    sd_right = pca.transform(t_right_np)
    sd_left = pca.transform(t_left_np)

    return np.log(n_right/n_left), np.log(sd_right, sd_left) 


if __name__ == "__main__":
    get_PCA_pars(True)

    