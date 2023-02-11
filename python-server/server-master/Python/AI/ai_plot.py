

import enum
from AI.PlayerSimulator import PlayerSimulator
from typing import List, Tuple, Any, Callable
import matplotlib.pyplot as plt
from AI.ai_utils import angle_between, unit_vector, vcol
from AI.ai_consts import *
import numpy as np
import os
from datetime import date
from mpl_toolkits import mplot3d
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from tabulate import tabulate
from matplotlib.patches import Arc
from matplotlib.lines import Line2D
import math


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

    def save_np_array(self, arrays: Tuple[List[Any], str], root_type: str = "main"):
        root = self.root if root_type == "main" else self.monthly_root

        for (data, name) in arrays:
            savepath = os.path.join(root, f"{name.replace(' ', '_')}.npy")
            a = np.array(data)
            np.save(savepath, a)

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
        with open(plain_file, 'w') as f:
            f.write("\n")
            f.write(table_plain)
            f.write("\n")
        
        tex_file = os.path.join(root, f"{prefix}_tex.tex")
        with open(tex_file, 'w') as f:
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
                estimated_std: np.ndarray = None,
                plot_fs: bool = False,
                title: str = None,
                plot_norm: bool = False):

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
            transform_mat = np.linalg.inv(np.array([[boundary_vector[0], boundary_vector[1]], [boundary_vector[1], -boundary_vector[0]]]))
            trial_vec = np.dot(transform_mat, vcol(np.array([coord[0], coord[1]])))
            trial_vec = trial_vec[0]*np.array(boundary_vector)
            ax.plot([trial_vec[0], coord[0]], [trial_vec[1], coord[1]], color="orange")
        #print(f">>{coord}")
        
    if plot_stats is not None:
        plot_stats(plt)
    
    if plot_fs:
        line_1 = Line2D([0,0], [0,1], linewidth=1, linestyle = "-", color="green")
        line_2 = Line2D([0,boundary_vector[0]], [0,boundary_vector[1]], linewidth=1, linestyle = "-", color="red")

        angle_plot = get_angle_plot(line_1, line_2, 0.7, color="red")
        angle_text = get_angle_text(angle_plot) 
        #ax.add_line(line_1)
        #ax.add_line(line_2)
        ax.add_patch(angle_plot) # To display the angle arc
        #ax.text(*angle_text) # To display the angle value

        line_1 = Line2D([0,0], [0,-1], linewidth=1, linestyle = "-", color="green")
        line_2 = Line2D([0,-boundary_vector[0]], [0,-boundary_vector[1]], linewidth=1, linestyle = "-", color="red")

        angle_plot = get_angle_plot(line_1, line_2, 0.7, color="red")
        angle_text = get_angle_text(angle_plot) 
        #ax.add_line(line_1)
        #ax.add_line(line_2)
        ax.add_patch(angle_plot) # To display the angle arc
        #ax.text(*angle_text) # To display the angle value
    
    if plot_norm:
        norm = np.array(unit_vector([boundary_vector[1],-boundary_vector[0]]))
        plt.arrow(0,0,norm[0], norm[1], width=0.01)
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
    if title is not None:
        plt.title(title)
        
    if figsaver is None:
        plt.show()
    else:
        figsaver.save_day()
"""
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
"""
def plot_stats( statlist: List[List[float]], 
                length: int,
                labels: List[str] = ['local_accuracy', 'cumulative_accuracy'],
                main_stat: str = "alpha",
                figsaver: FigSaver = None,
                lim_bounds: List[float] = [-0.1, MAX_SIGMA+0.1],
                save_as_ndarray: bool = True,
                title: str = None,
                xlabel: str = None):

    fig = plt.figure()
    ax = fig.gca()
    x = np.linspace(1, length, length)

    colors = ["green", "red", "blue", "orange", "brown", "pink", "gray", "teal", "yellow", "purple", "magenta"]
    to_save = []
    to_save.append((x, f"x_data_{main_stat}"))
    for i, dl in enumerate(statlist):
        ax.plot(x, dl, color= colors[i], label=labels[i])
        to_save.append((dl, labels[i]))
    
    if title is None:
        plt.title(f"Plot for {main_stat}")
    else:
        plt.title(title)

    ax.legend()

    if xlabel is None:
        plt.xlabel("trial")
    else:
        plt.xlabel(xlabel)

    if main_stat == "alpha":
        plt.ylabel("alpha (degrees)")
    elif main_stat == "sigma":
        plt.ylabel("sigma (ND-NND units)")
    else: 
        plt.ylabel(main_stat)

    plt.ylim(lim_bounds)
    plt.grid(True)
    

    if figsaver is None:
        plt.show()
    else:
        figsaver.save_summary_stats(f"{labels[0]}-{labels[1]}")
        if save_as_ndarray:
            figsaver.save_np_array(to_save, "main")
    

def plot_monthly_stats( statlist: List[List[float]], 
                        tpd: int,
                        month_n: int,
                        days: int = 30,
                        main_stat = "alpha",
                        labels: List[str] = ['local_accuracy', 'cumulative_accuracy'], 
                        figsaver: FigSaver = None,
                        lim_bounds: List[float] = [-0.1, MAX_SIGMA+0.1],
                        length: int = -1,
                        save_as_ndarray: bool = True):
    
    if figsaver is None:
        return

    fig = plt.figure()
    ax = fig.gca()
    daily_statlist = []
    if month_n>=0:
        x = np.linspace(1, days, days)
    else:
        x = np.linspace(1, length, length)

    for l in statlist:
        daily_stat = vec_reshape_by_day(l, tpd)
        reduced = []
        for ds in daily_stat:
            reduced.append(sum(ds)/tpd)
        daily_statlist.append(reduced)
    
    colors = ["green", "red", "blue", "orange", "brown", "pink", "gray", "teal", "yellow", "purple", "magenta"]
    to_save = []
    to_save.append((x, "x_data"))
    for i, dl in enumerate(daily_statlist):
        ax.plot(x, dl, color= colors[i], label=labels[i])
        to_save.append((dl, f"{month_n}_{labels[i]}"))
        
    if month_n >= 0:
        plt.title(f"Month n° {month_n}")
    else:
        plt.title(f"Whole simulation")
        month_n = "All"

    ax.legend()

    plt.xlabel("day")
    if main_stat == "alpha":
        plt.ylabel("alpha (degrees)")
    elif main_stat == "sigma":
        plt.ylabel("sigma (ND-NND units)")
    else: 
        plt.ylabel("accuracy")

    plt.ylim(lim_bounds)
    plt.grid(True)
    
    if figsaver is not None:
        figsaver.save_summary_stats(f"{month_n}-{labels[0]}-{labels[1]}", "monthly")
        if save_as_ndarray:
            figsaver.save_np_array(to_save, "monthly")

def average_by_day(vec: List[Any], trials_per_day: int) -> np.ndarray:
    vec_per_day = vec_reshape_by_day(vec, trials_per_day)
    ret = []

    for v in vec_per_day:
        ret.append(sum(v)/trials_per_day)
    
    return np.array(ret)

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

def plot_gaussian_3D(mean: np.ndarray, std:float):
    gauss_func = lambda y,x : math.exp(-0.5*(1/(std**2))*(((x-mean[0])**2)+((y-mean[1])**2)))
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    #plot optimal boundary
    ys = np.linspace(-1, 1, 10)
    zs = np.linspace(-1, 1, 10)

    Y, Z = np.meshgrid(ys, zs)
    X = np.array([0 for i in range(0,10)])

    ax.plot_surface(X, Y, Z, color= "blue", alpha=0.6)

    zline = [0, 0]
    xline = [-1,1]
    yline = [0,0]
    

    ax.plot3D(xline, yline, zline, color= "red")
    zline = [0, 0]
    yline = [-1,1]
    xline = [0,0]

    ax.plot3D(xline, yline, zline, color= "red")

    ys = np.linspace(-1, 1, 50)
    xs = np.linspace(-1, 1, 50)

    Y, X = np.meshgrid(ys, xs)
    Z = np.zeros(X.shape)

    for i in range(0, X.shape[0]):
        for j in range(0, X.shape[1]):
            Z[i,j] = gauss_func(Y[i,j], X[i,j])

    ax.plot_surface(X, Y, Z, color= "orange", alpha = 0.3)

    plt.show()

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
    ax.set_xlabel('alpha', fontsize=20, rotation=150)
    ax.set_ylabel('sigma', fontsize=20, rotation=150)
    ax.set_zlabel('best C', fontsize=20, rotation=150)
    plt.show()

def plot_comparisons(   root:str,
                        labels:List[str],
                        folder_prefix: str="plot_save_trials_", 
                        suffix_set: List[str] =[str(i) for i in range(0,10+1)], 
                        subfolder_name: str = "alpha_80_sigma_20",
                        metric_name: str = "second_pass_alpha",
                        main_stat: str = "alpha",
                        monthly: bool = False,
                        title: str = None,
                        xlabel: str = None,
                        xlength: int = None,
                        plot_dists: bool = False
                        ):

    x=[]
    stats = []
    actuals = []
    for i, suffix in enumerate(suffix_set):
        if monthly == False:
            path = os.path.join(root, folder_prefix+suffix, subfolder_name, f"{metric_name}.npy")
            if plot_dists:
                dist_path = os.path.join(root, folder_prefix+suffix, subfolder_name, f"actual_{main_stat}.npy")
        else:
            path = os.path.join(root, folder_prefix+suffix, subfolder_name, "monthly", f"-1_{metric_name}.npy")
            if plot_dists:
                dist_path = os.path.join(root, folder_prefix+suffix, subfolder_name, "monthly", f"-1_actual_{main_stat}.npy")
        #print(path)
        if i == 0:
            xpath = os.path.join(root, folder_prefix+suffix, subfolder_name, f"x_data_alpha.npy")
            x = np.load(xpath)

        if plot_dists:
            actual = np.load(dist_path)
            actuals.append(actual)
        y = np.load(path)
        stats.append(y)

    if main_stat == "alpha":
        bounds = [-5, MAX_ALPHA+5]  
    elif main_stat == "sigma": 
        bounds = [-0.1, MAX_SIGMA+0.1]
    else:
        bounds = [-0.1, 1.1]

    length = x.shape[0] if monthly == False else int(x.shape[0]/30) 
    length = xlength if xlength is not None else length 
    plot_stats(stats, length, labels, main_stat=main_stat,save_as_ndarray=False, lim_bounds=bounds, xlabel=xlabel, title=title)

    dists = []
    if plot_dists:
        for stat, act in zip(stats, actuals):
            dists.append(stat - act)

        plot_stats(dists, length, labels, main_stat=main_stat,save_as_ndarray=False, lim_bounds=[-0.2, 0.2] if main_stat == "sigma" else [-10, 10], xlabel=xlabel, title=f"Distance for {main_stat}")
    
def plot_1d_gaussians(trial: List[float], bv: List[float], std:float, i: int):
    transform_mat =np.linalg.inv(np.array([[bv[0], bv[1]], [bv[1], -bv[0]]]))
    trial_vec = np.dot(transform_mat, vcol(np.array(trial)))
    dist = float(trial_vec[1])       

    gauss_func = lambda x : np.exp(-0.5*(1/(std**2))*((x-dist)**2))
    
    fig = plt.figure()
    ax = plt.axes()

    x = np.linspace(-3,0,100)
    y = gauss_func(x)
    ax.plot(x,y)
    color = "green" if (trial[0]<0) else "red"
    ax.fill_between(x, 0, y, color=color)

    x = np.linspace(0,3,100)
    y = gauss_func(x)
    ax.plot(x,y)
    color = "green" if (trial[0]>0) else "red"
    ax.fill_between(x, 0, y, color=color)

    y=np.linspace(0,gauss_func(0),100)
    x=y-y
    ax.plot(x,y,color="black")
    
    plt.xlabel("Distance from decision boundary")
    plt.ylabel("Probability Density")

    title = f"Point {i}: ND > 0" if trial[0]>0 else f"Point {i}: ND < 0"
    plt.title(title)
    plt.xlim([-1.2,1.2])
    plt.grid(True)
    plt.show()

    





#utils related to plots
def get_angle_plot(line1, line2, offset = 1, color = None, origin = [0,0], len_x_axis = 1, len_y_axis = 1):

    l1xy = line1.get_xydata()
    
    # Angle between line1 and x-axis
    y1 = l1xy[1][1] - l1xy[0][1]
    x1 = l1xy[1][0] - l1xy[0][0]
    slope1 = y1 / float(x1)
    # Allows you to use this in different quadrants
    angle1 = math.degrees(math.atan2(y1, x1))
    
    l2xy = line2.get_xydata()
    
    # Angle between line2 and x-axis
    y2 = l2xy[1][1] - l2xy[0][1]
    x2 = l2xy[1][0] - l2xy[0][0]
    slope2 = y2 / float(x2)
    angle2 = math.degrees(math.atan2(y2, x2))
    
    theta1 = min(angle1, angle2)
    theta2 = max(angle1, angle2)
    
    angle = theta2 - theta1
    
    if color is None:
        color = line1.get_color() # Uses the color of line 1 if color parameter is not passed.
    
    return Arc(origin, len_x_axis*offset, len_y_axis*offset, 0, 
               theta1, theta2, color=color, 
               label = 0.1)

def get_angle_text(angle_plot):
    angle = angle_plot.get_label()[:-1] # Excluding the degree symbol
    angle = "%0.2f"%float(angle)+u"\u00b0" # Display angle upto 2 decimal places

    # Get the vertices of the angle arc
    vertices = angle_plot.get_verts()

    # Get the midpoint of the arc extremes
    x_width = (vertices[0][0] + vertices[-1][0]) / 2.0
    y_width = (vertices[0][1] + vertices[-1][1]) / 2.0


    separation_radius = max(x_width/2.0, y_width/2.0)

    return [x_width + separation_radius, y_width + separation_radius, angle]