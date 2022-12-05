

import enum
from AI.PlayerSimulator import PlayerSimulator
from typing import List, Tuple, Any, Callable
import matplotlib.pyplot as plt
from AI.ai_utils import angle_between, unit_vector
import numpy as np
import os
from datetime import date
from mpl_toolkits import mplot3d

class FigSaver:
    def __init__(self, base_root: str,exp_name: str, add_date:bool=False, interval: int=5, figname: str = None) -> None:
        self.root = os.path.join(base_root, exp_name) if figname is None else base_root
        self.figname = figname
        if add_date:
            today = date.today()
            self.root = os.path.join(self.root, today.strftime("%Y-%m-%d"))

        if os.path.exists(self.root) == False and figname is None:
            os.mkdir(self.root)
        self.interval = interval
        self.i = 0

    def save_day(self):
        #print("AAAA")
        if self.i % self.interval == 0:
            figpath = os.path.join(self.root, f"{self.i}.png") if self.figname is None else os.path.join(self.root, f"{self.figname}.png") 
            #print(figpath)
            plt.savefig(figpath, format= "png")
            plt.close()
        self.i+=1

    def save_summary_stats(self, name: str):
        figpath = os.path.join(self.root, f"{name}.png")
        plt.savefig(figpath, format= "png")
        plt.close()


def plot_trials(boundary_vector: np.ndarray, trials: List[List[Any]], corrects: List[bool], 
                annotations: List[float], ann_str: bool = False, plot_stats: Callable = None, 
                plot_dist: bool = False, norm_lim: bool = True, sharp_std: float = None, figsaver: FigSaver = None,
                estimated_boundary: np.ndarray = None, estimated_std: np.ndarray = None):

    if figsaver is not None:
        #just a speedup, avoid plotting if you're not going to show or save the figure
        if figsaver.i % figsaver.interval != 0:
            figsaver.i +=1
            return

    fig = plt.figure()
    ax = fig.gca()

    vec= 5*boundary_vector
    
    ax.plot([vec[0], -vec[0]], [vec[1], -vec[1]])
    if estimated_boundary is not None:
        eb = estimated_boundary*5
        ax.plot([eb[0], -eb[0]], [eb[1], -eb[1]], color= 'orange')

    colors = {True: 'green', False: 'red'}

    coords = list(map(lambda x: x[8:],trials))


    for i, coord in enumerate(coords):
        #print(corrects[i])
        ax.scatter(coord[0], 
            coord[1], 
            color = colors[corrects[i]])
        #ax.text(coord[0]-0.1, coord[1]+0.1, str(round(times[i],2)), color = colors[corrects[i]])

        if sharp_std is not None:
            circle = plt.Circle((coord[0], coord[1]), radius = sharp_std, alpha = 0.2)
            ax.add_patch(circle)
            #ax.scatter(coord[0], coord[1], color = "blue", alpha=0.1, marker="o", s=sharp_std*1000)
        if estimated_std is not None:
            circle = plt.Circle((coord[0], coord[1]), radius = estimated_std, alpha = 0.2, color= 'orange')
            ax.add_patch(circle)
            #ax.scatter(coord[0], coord[1], color = "blue", alpha=0.1, marker="o", s=sharp_std*1000)


        if ann_str:
            ax.annotate(annotations[i], (coord[0], coord[1]), color= "red")
        else:    
            ax.annotate(str(round(annotations[i],2)), (coord[0], coord[1]), color="red")
        
        if plot_dist:
            proj = [boundary_vector[0] * coord[0], boundary_vector[1]*coord[1]]
            ax.plot([proj[0], coord[0]], [proj[1], coord[1]], color="red")
        #print(f">>{coord}")
        
    if plot_stats is not None:
        plot_stats(plt)

    
    ax.axis("equal")
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')

    if norm_lim:
        plt.xlim([-1, 1])
        plt.ylim([-1,1])
    else:
        plt.xlim([-2, 2])
        plt.ylim([-2,2])
        
    #plt.xlabel("Numerical dimension", loc="left")
    #plt.ylabel("Non numerical dimension", loc="bottom")
    plt.grid(False)

    if figsaver is None:
        plt.show()
    else:
        figsaver.save_day()

def plot_stats( local_accuracies: List[float], cumulative_accuracies: List[float], days: int, 
                labels: List[str] = ['local_accuracy', 'cumulative_accuracy'], figsaver: FigSaver = None,
                lim_bounds: List[float] = [-0.1, 1.1]):
    fig = plt.figure()
    ax = fig.gca()

    x = np.linspace(1, days, days)

    ax.plot(x, local_accuracies, color= 'green', label=labels[0])
    ax.plot(x, cumulative_accuracies, color= 'red', label=labels[1])

    ax.legend()

    plt.ylim(lim_bounds)
    plt.grid(True)
    if figsaver is None:
        plt.show()
    else:
        figsaver.save_summary_stats(f"{labels[0]}-{labels[1]}")

def separate_by_day(vec: List[Any], trials_per_day: int):
    i=0
    ret = []
    for e in vec:
        to_add = []
        for j in range(0, trials_per_day):
            to_add.append(e)
        ret.append(to_add)
    return ret

def plot_player_cycle3D(boundary_vectors: List[np.ndarray], sigmas: List[float], trials: List[List[Any]], corrects: List[bool],
                        trials_per_day:int, norm_lim: bool = True, figsaver: FigSaver = None, plot_eval_stats: Callable = None):
    n_days = len(boundary_vectors)
    corrects = np.array(corrects)
    incorrects = corrects == False

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    #plot trials
    zline = np.array([d for d in range(0, n_days) for t in range(0,trials_per_day)])
    xline = np.array(list(map(lambda x: x[8],trials)))
    yline = np.array(list(map(lambda x: x[9],trials)))

    #corrects
    zline_c = zline[corrects]
    xline_c = xline[corrects]
    yline_c = yline[corrects] 
    ax.scatter3D(xline_c, yline_c, zline_c, color="green")
    #incorrects
    zline_i = zline[incorrects]
    xline_i = xline[incorrects]
    yline_i = yline[incorrects] 
    ax.scatter3D(xline_i, yline_i, zline_i, color="red")
    

    #plot optimal boundary
    ys = np.linspace(-1, 1, 10)
    zs = np.linspace(-1, n_days, 10)

    Y, Z = np.meshgrid(ys, zs)
    X = np.array([0 for i in range(0,10)])

    ax.plot_surface(X, Y, Z, color= "gray", alpha = 0.5)

    #plot X plane
    xs = np.linspace(-1, 1, 10)
    zs = np.linspace(-1, n_days, 10)

    X, Z = np.meshgrid(xs, zs)
    Y = np.array([0 for i in range(0,10)])

    ax.plot_surface(X, Y, Z, color= "gray", alpha = 0.5)

    #plot child evolution
    for i, bv in enumerate(boundary_vectors):
        zline = [i, i]
        xline = [-bv[0],bv[0]]
        yline = [-bv[1],bv[1]]
        ax.plot3D(xline, yline, zline, color= "orange", alpha = 0.8)
    
    if norm_lim:
        plt.xlim([-1, 1])
        plt.ylim([-1,1])
    else:
        plt.xlim([-2, 2])
        plt.ylim([-2,2])
    plt.show()


def plot_histograms(data: List[np.ndarray]):
    colors = ["red", "green", "blue","orange" , "gray", "orange"]

    for i,d in enumerate(data):
        plt.hist(d, color = colors[i], alpha = 0.6, histtype="bar", bins=50)

    plt.show()