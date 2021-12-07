import numpy as np
import matplotlib.pyplot as plt
import math

def PlotTrials(response_vector, trials_matrix, alpha, nnd_selector):
    nv = []  # nv --> NUMERICAL VARIABLE
    nnv = []  # nnv --> NON-NUMERICAL VARIABLE
        
    fig = plt.figure()
    added_alpha = alpha + 90
    rad_alpha = np.deg2rad(added_alpha)   # converted in radiants
    coeff = math.tan(rad_alpha) 
    ax = fig.add_subplot(1, 1, 1)
    x = np.linspace(-5, 5, 100)
    
    my_colors = {0: 'green', 1: 'red'}
    
    for results in trials_matrix:
        nv.append(np.log10(results[7]/results[6])) #number_of_chickens
        if nnd_selector == 1:
            nnv.append(np.log10(results[1]/results[0])) #circle_radius
        elif nnd_selector == 2:
            nnv.append(np.log10(results[3]/results[2])) #size_of_chicken
        else:
            nnv.append(np.log10(results[5]/results[4])) #average_space_between
            
    for i in range (len(response_vector)):
        if(nv[i] == 0):
            continue
        else:
            plt.scatter(nv[i], nnv[i], color = my_colors.get(response_vector[i]))
        
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    
    plt.plot(x, coeff*x, '-y')
    
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])
    plt.grid(True)
    
    plt.title("Filtering + Sharpening Effect (PlotTrials function)")
    
    plt.show()    