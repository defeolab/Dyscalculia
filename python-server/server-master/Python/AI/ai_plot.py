

import enum
from AI.PlayerSimulator import PlayerSimulator
from typing import List, Tuple, Any
import matplotlib.pyplot as plt
from AI.ai_utils import angle_between, unit_vector
import numpy as np

def plot_trials(player: PlayerSimulator, trials: List[List[Any]], corrects: List[bool], times: List[float]):

    fig = plt.figure()
    ax = fig.gca()

    vec= 5*player.boundary_vector
    
    ax.plot([vec[0], -vec[0]], [vec[1], -vec[1]])

    colors = {True: 'green', False: 'red'}

    coords = list(map(lambda x: x[8:],trials))
    
    
    for i, coord in enumerate(coords):
        #print(corrects[i])
        ax.scatter(coord[0], coord[1], color = colors[corrects[i]])
        #ax.text(coord[0]-0.1, coord[1]+0.1, str(round(times[i],2)), color = colors[corrects[i]])
        ax.annotate(str(round(times[i],2)), (coord[0], coord[1]))
        #print(f">>{coord}")
        

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