

import enum
from AI.PlayerSimulator import PlayerSimulator
from typing import List, Tuple, Any, Callable
import matplotlib.pyplot as plt
from AI.ai_utils import angle_between, unit_vector
import numpy as np
import os
from datetime import date
from mpl_toolkits import mplot3d
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from tabulate import tabulate



class FigSaver:
    def __init__(self, base_root: str,exp_name: str, add_date:bool=False, interval: int=5, figname: str = None) -> None:
        self.root = os.path.join(base_root, exp_name) if figname is None else base_root
        self.monthly_root = os.path.join(self.root, "monthly")
        self.figname = figname
        if add_date:
            today = date.today()
            self.root = os.path.join(self.root, today.strftime("%Y-%m-%d"))

        if os.path.exists(self.root) == False and figname is None:
            os.mkdir(self.root)
            if os.path.exists(self.monthly_root) == False:
                os.mkdir(self.monthly_root)

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

    def save_summary_stats(self, name: str, root_type: str = "main"):
        root = self.root if root_type == "main" else self.monthly_root
        figpath = os.path.join(root, f"{name}.png")
        plt.savefig(figpath, format= "png")
        plt.close()

    def save_player_cycle_3D(self, ax):
        elev = [0, 60, 90]
        az = [10, 45, 75]

        for e in elev:
            for a in az:
                figpath=os.path.join(self.root, f"PC3D_{e}_{a}.png")
        
                ax.view_init(e,a)
                plt.savefig(figpath, format = "png")
        plt.close()
    
    def save_table(self, data: List[Any], headers: List[str], prefix: str, root_type: str = "main"):
        root = self.root if root_type == "main" else self.monthly_root
        table_plain = tabulate(data, headers, tablefmt="grid")
        table_tex = tabulate(data, headers, tablefmt="latex")

        plain_file = os.path.join(root, f"{prefix}_plain.txt")
        with open(plain_file, 'a') as f:
            f.write("\n")
            f.write(table_plain)
            f.write("\n")
        
        tex_file = os.path.join(root, f"{prefix}_tex.tex")
        with open(tex_file, 'a') as f:
            f.write("\n")
            f.write(table_tex)
            f.write("\n")



        


def plot_trials(boundary_vector: np.ndarray, 
                trials: List[List[Any]], 
                corrects: List[bool], 
                annotations: List[float], 
                ann_str: bool = False, 
                plot_stats: Callable = None, 
                plot_dist: bool = False, 
                norm_lim: bool = True, 
                sharp_std: float = None, 
                figsaver: FigSaver = None,
                estimated_boundary: np.ndarray = None, 
                estimated_std: np.ndarray = None):

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

def plot_stats( local_accuracies: List[float], 
                cumulative_accuracies: List[float], 
                days: int, 
                labels: List[str] = ['local_accuracy', 'cumulative_accuracy'], 
                figsaver: FigSaver = None,
                lim_bounds: List[float] = [-0.1, 1.1],
                write_avg_dists: bool = False):
    fig = plt.figure()
    ax = fig.gca()

    x = np.linspace(1, days, days)

    ax.plot(x, local_accuracies, color= 'green', label=labels[0])
    ax.plot(x, cumulative_accuracies, color= 'red', label=labels[1])

    if write_avg_dists:
        la = np.array(local_accuracies)
        ca = np.array(cumulative_accuracies)
        d = np.abs(la-ca).sum()/la.shape[0]
        plt.title(f"Avg dist: {d}")

    ax.legend()

    plt.ylim(lim_bounds)
    plt.grid(True)
    if figsaver is None:
        plt.show()
    else:
        figsaver.save_summary_stats(f"{labels[0]}-{labels[1]}")

def plot_monthly_stats( statlist: List[List[float]], 
                        tpd: int,
                        month_n: int,
                        days: int = 30,
                        labels: List[str] = ['local_accuracy', 'cumulative_accuracy'], 
                        figsaver: FigSaver = None,
                        lim_bounds: List[float] = [-0.1, 1.1]):
    
    if figsaver is None:
        return

    fig = plt.figure()
    ax = fig.gca()
    daily_statlist = []

    x = np.linspace(1, days, days)

    for l in statlist:
        daily_stat = vec_reshape_by_day(l, tpd)
        reduced = []
        for ds in daily_stat:
            reduced.append(sum(ds)/tpd)
        daily_statlist.append(reduced)
    
    colors = ["green", "red", "blue", "orange", "yellow"]

    for i, dl in enumerate(daily_statlist):
        ax.plot(x, dl, color= colors[i], label=labels[i])

    plt.title(f"Month n° {month_n}")

    ax.legend()

    plt.xlabel("day")

    plt.ylim(lim_bounds)
    plt.grid(True)
    
    figsaver.save_summary_stats(f"{month_n}-{labels[0]}-{labels[1]}", "monthly")

def vec_reshape_by_day(vec: List[Any], trials_per_day: int):
    ret = []
    for i in range(0, int(len(vec)/trials_per_day)):
        to_add = []
        for j in range(0, trials_per_day):
            to_add.append(vec[i*trials_per_day + j])
        ret.append(to_add)
    return ret

def make_tables( main_stat: List[float],
                secondary_stats: List[List[float]],
                tpd: int,
                n_months: int,
                days: int = 30,
                main_label: str = "alpha",
                secondary_labels: List[str] = ['local accuracy', 'cumulative accuracy'], 
                figsaver: FigSaver = None):

    main_monthly_stat = vec_reshape_by_day(main_stat, days*tpd)

    secondary_monthly_stats = []

    for stat in secondary_stats:
        secondary_monthly_stat = vec_reshape_by_day(stat, days*tpd)
        secondary_monthly_stats.append(secondary_monthly_stat)

    data = []
    main_monthly_stat = np.array(main_monthly_stat)
    secondary_monthly_stats = np.array(secondary_monthly_stats)
    for i in range(0, n_months):
        monthly_data = [i+1]
        #print(main_monthly_stat[i])
        for stat in secondary_monthly_stats:
            #print(stat[i])
            dist = np.abs(main_monthly_stat[i]-stat[i])
            avg_dist = np.average(dist)
            dist_std = np.std(dist)
            max_dist = np.max(dist)
            monthly_data.append(avg_dist)
            monthly_data.append(dist_std)
            monthly_data.append(max_dist)
        
        data.append(monthly_data)

    last_row = ["All"]

    main_all_data = np.array(main_stat)
    secondary_all_data = np.array(secondary_stats)
    for stat in secondary_all_data:
        dist = np.abs(main_all_data-stat)
        avg_dist = np.average(dist)
        dist_std = np.std(dist)
        max_dist = np.max(dist)
        last_row.append(avg_dist)
        last_row.append(dist_std)
        last_row.append(max_dist)

    data.append(last_row)
    
    header = ["Month"]

    header_additions = ["Avg Dist", "Dist Std", "Max Dist"]
    for i, stat in enumerate(secondary_monthly_stats):
        for addition in header_additions:
            header.append(secondary_labels[i] + " "+ addition)

    if figsaver is not None:
        figsaver.save_table(data, header, main_label,root_type = "monthly")
    else:
        print(tabulate(data, header, tablefmt="fancy_grid"))



def separate_by_day(vec: List[Any], trials_per_day: int):
    i=0
    ret = []
    for e in vec:
        to_add = []
        for j in range(0, trials_per_day):
            to_add.append(e)
        ret.append(to_add)
    return ret

def filter_trials_per_day(trials: np.ndarray, corrects: np.ndarray, tpd: int, max_tpd: int):
    ret_t = []
    ret_c = []

    for day in range(0, int(len(trials)/tpd)):
        for td in range(0, max_tpd):
            ret_t.append(trials[day*tpd + td])
            ret_c.append(corrects[day*tpd + td])

    return np.array(ret_t), np.array(ret_c)

def plot_player_cycle3D(boundary_vectors: List[np.ndarray], 
                        estimated_vectors: List[np.ndarray], 
                        sigmas: List[float],
                        estimated_sigmas: List[float],
                        trials: List[List[Any]], 
                        corrects: List[bool], 
                        trials_per_day:int, 
                        norm_lim: bool = True, 
                        figsaver: FigSaver = None, 
                        plot_eval_stats: bool = True,
                        skip_sigmas: int = 5,
                        skip_bvs: int = 5,
                        max_trials_per_day_plotted: int = 2):
    n_days = len(boundary_vectors)
    corrects = np.array(corrects)

    fig = plt.figure()
    ax = plt.axes(projection='3d')

    tpd = min(trials_per_day, max_trials_per_day_plotted)
    #plot trials
    zline = np.array([d for d in range(0, n_days) for t in range(0,tpd)])
    
    f_trials = trials
    f_corrects = corrects

    if max_trials_per_day_plotted < trials_per_day:
 
        f_trials, f_corrects = filter_trials_per_day(trials, corrects, trials_per_day,max_trials_per_day_plotted)    

    f_incorrects = f_corrects == False

    xline = np.array(list(map(lambda x: x[8],f_trials)))
    yline = np.array(list(map(lambda x: x[9],f_trials)))


    #corrects
    zline_c = zline[f_corrects]
    xline_c = xline[f_corrects]
    yline_c = yline[f_corrects] 
    ax.scatter3D(xline_c, yline_c, zline_c, color="green")
    #incorrects
    zline_i = zline[f_incorrects]
    xline_i = xline[f_incorrects]
    yline_i = yline[f_incorrects] 
    ax.scatter3D(xline_i, yline_i, zline_i, color="red")
    

    #plot optimal boundary
    ys = np.linspace(-1, 1, 10)
    zs = np.linspace(-1, n_days, 10)

    Y, Z = np.meshgrid(ys, zs)
    X = np.array([0 for i in range(0,10)])

    ax.plot_surface(X, Y, Z, color= "gray", alpha = 0.3)

    #plot X plane
    xs = np.linspace(-1, 1, 10)
    zs = np.linspace(-1, n_days, 10)

    X, Z = np.meshgrid(xs, zs)
    Y = np.array([0 for i in range(0,10)])

    ax.plot_surface(X, Y, Z, color= "gray", alpha = 0.3)

    #plot child alpha evolution
    for i, bv in enumerate(boundary_vectors):
        if i % skip_bvs != 0:
            continue
        zline = [i, i]
        xline = [-bv[0],bv[0]]
        yline = [-bv[1],bv[1]]
        ax.plot3D(xline, yline, zline, color= "purple", alpha = 0.6)
    
    #plot evaluator alpha evolution
    for i, bv in enumerate(estimated_vectors):
        if i % skip_bvs != 0:
            continue
        zline = [i, i]
        xline = [-bv[0],bv[0]]
        yline = [-bv[1],bv[1]]
        ax.plot3D(xline, yline, zline, color= "orange", alpha = 0.6)
    
    circle_resolution = 50
    #plot child sigma evolution
    for i, s in enumerate(sigmas):
        if i % skip_sigmas != 0:
            continue
        theta = np.linspace(0, 2 * np.pi, circle_resolution)
        x = s*np.cos(theta)
        y = s*np.sin(theta)
        ax.plot(x, y, [i for j in range(0, circle_resolution)], color = "blue", alpha = 0.6)

    #plot evaluator sigma evolution
    for i, s in enumerate(estimated_sigmas):
        if i % skip_sigmas != 0:
            continue
        theta = np.linspace(0, 2 * np.pi, circle_resolution)
        x = s*np.cos(theta)
        y = s*np.sin(theta)
        ax.plot(x, y, [i for j in range(0, circle_resolution)], color = "red", alpha= 0.6)
    

    if norm_lim:
        plt.xlim([-1, 1])
        plt.ylim([-1,1])
    else:
        plt.xlim([-2, 2])
        plt.ylim([-2,2])

    if figsaver is None:
        plt.show()
    else:
        figsaver.save_player_cycle_3D(ax)


def plot_histograms(data: List[np.ndarray]):
    colors = ["red", "green", "blue","orange" , "gray", "orange"]

    for i,d in enumerate(data):
        plt.hist(d, color = colors[i], alpha = 0.6, histtype="bar", bins=50)

    plt.show()


def plot_ablation_C(configs: np.ndarray, Cs: np.ndarray, best_Cs: np.ndarray):

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    X = configs[:, 0]
    Y = configs[:, 1]

    #print(X)

    Z = best_Cs 


    surf = ax.plot_trisurf(X, Y, Z)

    plt.show()