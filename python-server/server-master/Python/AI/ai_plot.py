

import enum
from AI.PlayerSimulator import PlayerSimulator
from typing import List, Tuple, Any, Callable
import matplotlib.pyplot as plt
from AI.ai_utils import angle_between, unit_vector
import numpy as np

def plot_trials(boundary_vector: np.ndarray, trials: List[List[Any]], corrects: List[bool], annotations: List[float], ann_str: bool = False, plot_stats: Callable = None):

    fig = plt.figure()
    ax = fig.gca()

    vec= 5*boundary_vector
    
    ax.plot([vec[0], -vec[0]], [vec[1], -vec[1]])

    colors = {True: 'green', False: 'red'}

    coords = list(map(lambda x: x[8:],trials))
    
    
    for i, coord in enumerate(coords):
        #print(corrects[i])
        ax.scatter(coord[0], coord[1], color = colors[corrects[i]])
        #ax.text(coord[0]-0.1, coord[1]+0.1, str(round(times[i],2)), color = colors[corrects[i]])

        if ann_str:
            ax.annotate(annotations[i], (coord[0], coord[1]), color= "red")
        else:    
            ax.annotate(str(round(annotations[i],2)), (coord[0], coord[1]), color="red")
        #print(f">>{coord}")
        
    if plot_stats is not None:
        plot_stats(plt)

    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')

    plt.xlim([-2, 2])
    plt.ylim([-2,2])
    #plt.xlabel("Numerical dimension", loc="left")
    #plt.ylabel("Non numerical dimension", loc="bottom")
    plt.grid(False)

    plt.show()

def plot_stats(local_accuracies: List[float], cumulative_accuracies: List[float], days: int, labels: List[str] = ['local_accuracy', 'cumulative_accuracy']):
    fig = plt.figure()
    ax = fig.gca()

    x = np.linspace(1, days, days)

    ax.plot(x, local_accuracies, color= 'green', label=labels[0])
    ax.plot(x, cumulative_accuracies, color= 'red', label=labels[1])

    ax.legend()

    plt.ylim([0,1])
    plt.show()

