# Starting point of AI

import pandas as pd
import random
import math
from matplotlib import pyplot as plt

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

from distributions import GaussianThreshold, UniformOutput

numpy_array = []

fa_array_left = []
isa_array_left = []
num_array_left = []

fa_array_right = []
isa_array_right = []
num_array_right = []

fa_array_ratio = []
isa_array_ratio = []
num_array_ratio = []

dataSet_left = []
dataSet_right = []
dataSet_ratio = []

# Time Array
t = np.linspace(0, 20, 100)

fig = plt.figure()

fig1 = plt.figure()

fig2 = plt.figure()

fig3 = plt.figure()

ax = fig3.add_subplot(111)

x = np.linspace(-5, 5, 100)

ax_l = fig.add_subplot(1, 1, 1, projection='3d')
ax_l.set_xlabel('Field Area - L')
ax_l.set_ylabel('Item Surface Area - L')
ax_l.set_zlabel('Number of Chickens - L')

ax_l.view_init(20, 20)

ax_r = fig1.add_subplot(1, 1, 1, projection='3d')
ax_r.set_xlabel('Field Area - R')
ax_r.set_ylabel('Item Surface Area - R')
ax_r.set_zlabel('Number of Chickens - R')

ax_r.view_init(20, 20)

ax_ratio = fig2.add_subplot(1, 1, 1, projection='3d')
ax_ratio.set_xlabel('Field Area - Ratio')
ax_ratio.set_ylabel('Item Surface Area - Ratio')
ax_ratio.set_zlabel('Number of Chickens - Ratio')

ax_ratio.view_init(20, 20)

def animate_func_left(num):
    ax_l.clear()  # Clears the figure to update the line, point,   
                # title, and axes
    # Updating Trajectory Line (num+1 due to Python indexing)
    ax_l.plot3D(dataSet_left[0, :num+1], dataSet_left[1, :num+1], 
              dataSet_left[2, :num+1], c='blue')
    # Updating Point Location 
    ax_l.scatter(dataSet_left[0, num], dataSet_left[1, num], dataSet_left[2, num], 
               c='blue', marker='o')
    # Adding Constant Origin
    ax_l.plot3D(dataSet_left[0, 0], dataSet_left[1, 0], dataSet_left[2, 0],     
               c='black', marker='o')

    # Adding Figure Labels
    ax_l.set_title('Trajectory \nTime = ' + str(np.round(t[num],    
                 decimals=2)) + ' sec')

    ax_l.set_xlabel('FA - L')
    ax_l.set_ylabel('ISA - L')
    ax_l.set_zlabel('Num - L')
    
def animate_func_right(num):
    ax_r.clear()  # Clears the figure to update the line, point,   
                # title, and axes
    # Updating Trajectory Line (num+1 due to Python indexing)
    ax_r.plot3D(dataSet_right[0, :num+1], dataSet_right[1, :num+1], 
              dataSet_right[2, :num+1], c='blue')
    # Updating Point Location 
    ax_r.scatter(dataSet_right[0, num], dataSet_right[1, num], dataSet_right[2, num], 
               c='blue', marker='o')
    # Adding Constant Origin
    ax_r.plot3D(dataSet_right[0, 0], dataSet_right[1, 0], dataSet_right[2, 0],     
               c='black', marker='o')

    # Adding Figure Labels
    ax_r.set_title('Trajectory \nTime = ' + str(np.round(t[num],    
                 decimals=2)) + ' sec')

    ax_r.set_xlabel('FA - R')
    ax_r.set_ylabel('ISA - R')
    ax_r.set_zlabel('Num - R')
    
def animate_func_ratio(num):
    ax_ratio.clear()  # Clears the figure to update the line, point,   
                # title, and axes
    # Updating Trajectory Line (num+1 due to Python indexing)
    ax_ratio.plot3D(dataSet_ratio[0, :num+1], dataSet_ratio[1, :num+1], 
              dataSet_ratio[2, :num+1], c='blue')
    # Updating Point Location 
    ax_ratio.scatter(dataSet_ratio[0, num], dataSet_ratio[1, num], dataSet_ratio[2, num], 
               c='blue', marker='o')
    # Adding Constant Origin
    ax_ratio.plot3D(dataSet_ratio[0, 0], dataSet_ratio[1, 0], dataSet_ratio[2, 0],     
               c='black', marker='o')

    # Adding Figure Labels
    ax_ratio.set_title('Trajectory \nTime = ' + str(np.round(t[num],    
                 decimals=2)) + ' sec')

    ax_ratio.set_xlabel('Field Area - Ratio')
    ax_ratio.set_ylabel('Item Surface Area - Ratio')
    ax_ratio.set_zlabel('Number of Chickens - Ratio')
    

def UploadDataFromExcelDataset():
    # Uploading data from excel file
    data = pd.read_excel("./dataset/dataset_for_server.xlsx", dtype = {'NumChickens': int, 'FieldArea': float, 'ItemSurfaceArea': float})
    df = pd.DataFrame(data, columns = ['NumChickens','FieldArea', 'ItemSurfaceArea'])
    
    numpy_array = df.to_numpy()
    
    return numpy_array

# Control function, to check whether the point (represented by the three 
# coordinates, Number-Fa-ISA) is a valid point, i.e. it is below the curve,
# or not. Returns 1 for a valid point, 0 otherwise
def ValidTrial(number, fa, isa):
    
    dataset = UploadDataFromExcelDataset()
    isValid = 0
    
    for i in range(len(dataset)):
        if(number <= dataset[i][0]):
            # Number ok. Check for FA validity
            print("Number ok")
            if(fa <= dataset[i][1]):
                # FA ok. Check for ISA validity
                print("FA ok")
                if(isa <= dataset[i][2]):
                    # ISA ok. The point is valid, break the loop
                    print("ISA ok --> Point valid")
                    print(dataset[i][0])
                    print(dataset[i][1])
                    print(dataset[i][2])
                    isValid = 1
                    break
                else:
                    # if ISA is not valid, continue to the next iteration
                    print("ISA not ok")
                    continue
            else:
                # if FA is not valid, continue to the next iteration
                print("FA not ok")
                continue
        else:
            # if number is not valid, continue to the next iteration
            print("number not ok")
            continue
        
    # Reaching the end of the loop means that no match is found, so isValid is 0,
    # as it was set at the beginning
    return isValid

# Starting values: giving them some constant values (they're assigned by looking
# at the space of possible combinations)
# representing the space to plot the point --> trajectory
medium_num = 20
medium_fa = 28889
medium_isa = 149.28

# Minimum increment for FA and ISA is defined as Max + Min divided by 100
def MinimumIncrement(min_value, max_value):
    return (min_value + max_value) / 100

min_inc_num = 1
min_inc_fa = MinimumIncrement(5625, 40000)
min_inc_isa = MinimumIncrement(19.24, 307.79)

# This function represents the generation of a new trial, checking its validity.
# Taking the starting values (medium points of NUmber, FA and ISA), and the
# minimum increments, there's a RANDOM GENERATION of a number, which can assume
# values -1, 0, 1, one for each dimension:
    # if -1, then we take the dimension and subtract the minimum increment of that dimension
    # if 0, nothing happens, i.e. the dimension remains as it is
    # if 1, then we take the dimension and sum the minimum increment of that dimension
# Check if the new generated point is valid or not. If so, then the point will
# be used as new point, otherwise we recurse this function to find a new point,
# with three new randomic numbers
def GenerateNewTrialLeft(i, num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa):
    
    while (i < 257):        
        i = i + 1
        
        new_num = num
        new_fa = fa
        new_isa = isa
        
        random_dim_1 = random.randint(0, 2) - 1 # for number
        random_dim_2 = random.randint(0, 2) - 1 # for FA
        random_dim_3 = random.randint(0, 2) - 1 # for ISA
        
        # Tener traccia delle coordinate di prima
        if (random_dim_1 == -1):
            new_num = num - min_inc_num
        elif (random_dim_1 == 1):
            new_num = num + min_inc_num
            
        if (random_dim_2 == -1):
            new_fa = fa - min_inc_fa
        elif (random_dim_2 == 1):
            new_fa = fa + min_inc_fa
            
        if (random_dim_3 == -1):
            new_isa = isa - min_inc_isa
        elif (random_dim_3 == 1):
            new_isa = isa + min_inc_isa
            
        pointIsValid = ValidTrial(num, fa, isa)
        if(pointIsValid == 0 or num < 0):
            fa_array_left.append(fa)
            isa_array_left.append(isa)
            num_array_left.append(num)
            ax_l.scatter3D(fa, isa, num, marker='<', label="Invalid", c="red")
            return GenerateNewTrialLeft(i, num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa)
        else:
            print(num)
            print(fa)
            print(isa)
            print("point is valid")
            fa_array_left.append(new_fa)
            isa_array_left.append(new_isa)
            num_array_left.append(new_num)
            ax_l.scatter3D(new_fa, new_isa, new_num, marker='o', label="Valid", c="green")
            return GenerateNewTrialLeft(i, new_num, min_inc_num, new_fa, min_inc_fa, new_isa, min_inc_isa)
        
def GenerateNewTrialRight(i, num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa):
    
    while (i < 257):        
        i = i + 1
        
        new_num = num
        new_fa = fa
        new_isa = isa
        
        random_dim_1 = random.randint(0, 2) - 1 # for number
        random_dim_2 = random.randint(0, 2) - 1 # for FA
        random_dim_3 = random.randint(0, 2) - 1 # for ISA
        
        # Tener traccia delle coordinate di prima
        if (random_dim_1 == -1):
            new_num = num - min_inc_num
        elif (random_dim_1 == 1):
            new_num = num + min_inc_num
            
        if (random_dim_2 == -1):
            new_fa = fa - min_inc_fa
        elif (random_dim_2 == 1):
            new_fa = fa + min_inc_fa
            
        if (random_dim_3 == -1):
            new_isa = isa - min_inc_isa
        elif (random_dim_3 == 1):
            new_isa = isa + min_inc_isa
            
        pointIsValid = ValidTrial(num, fa, isa)
        if(pointIsValid == 0 or num < 0):
            fa_array_right.append(fa)
            isa_array_right.append(isa)
            num_array_right.append(num)
            ax_r.scatter3D(fa, isa, num, marker='<', label="Invalid", c="red")
            return GenerateNewTrialRight(i, num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa)
        else:
            print(num)
            print(fa)
            print(isa)
            print("point is valid")
            fa_array_right.append(new_fa)
            isa_array_right.append(new_isa)
            num_array_right.append(new_num)
            ax_r.scatter3D(new_fa, new_isa, new_num, marker='o', label="Valid", c="green")
            return GenerateNewTrialRight(i, new_num, min_inc_num, new_fa, min_inc_fa, new_isa, min_inc_isa)
        
        
def CalculateRatio():
    i = 0
    for i in range(len(fa_array_left)):   
        temp_fa = 4 * np.log2(fa_array_left[i] / fa_array_right[i])
        temp_isa = 2 * np.log2(isa_array_left[i] / isa_array_right[i])
        if(num_array_left[i] is not 0 and num_array_right[i] is not 0):
            temp_num = 1 * np.log2(num_array_left[i] / num_array_right[i])
        else :
            temp_num = 0           
        
        fa_array_ratio.append(temp_fa)
        isa_array_ratio.append(temp_isa)
        num_array_ratio.append(temp_num)
        
        fa_array_ratio.append(-temp_fa)
        isa_array_ratio.append(-temp_isa)
        num_array_ratio.append(-temp_num)
        
        fa_array_ratio.append(-temp_fa)
        isa_array_ratio.append(temp_isa)
        num_array_ratio.append(temp_num)
        
        fa_array_ratio.append(temp_fa)
        isa_array_ratio.append(-temp_isa)
        num_array_ratio.append(temp_num)
        
        fa_array_ratio.append(temp_fa)
        isa_array_ratio.append(temp_isa)
        num_array_ratio.append(-temp_num)
        
        
    for i in range(len(fa_array_ratio)):
        random_num = random.randint(0, 1)
        if (random_num > 0.8):
            ax_ratio.scatter(fa_array_ratio[i], isa_array_ratio[i], num_array_ratio[i], c = "blue")
        
def PlotPlane():
    correct_vector = [] # records if the specific trial has been correct or not
    
    alpha = 15
    sigma = 0.2
    mu = 0
    
    added_alpha = alpha + 90
    rad_alpha = np.deg2rad(added_alpha)   # converted in radiants
    coeff = math.tan(rad_alpha) 
            
    for i in range (len(num_array_ratio)):
        if (alpha != 0 and sigma != 0):
            # Filtering effect first
            if((fa_array_ratio[i] - (coeff * num_array_ratio[i])) == 0):
                plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "red")
                correct_vector.append(1)
            elif( ((fa_array_ratio[i] - (coeff * num_array_ratio[i]) > 0) and (( (fa_array_ratio[i] > 0) and (num_array_ratio[i] < 0) ))) 
                 or ((fa_array_ratio[i] - (coeff * num_array_ratio[i]) < 0) and (( (fa_array_ratio[i] < 0) and (num_array_ratio[i] > 0) ))) 
                 ):
                plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "red")
                correct_vector.append(1)
            elif(num_array_ratio[i] == 0):
                # No plot
                correct_vector.append(1)
                continue
            else:
                # Sharpening effect here
                uniform_output = UniformOutput()
                gaussian_threshold = GaussianThreshold(mu, sigma, num_array_ratio[i])
                # gaussian_threshold is between 0 and 0.5
                
                # -1 probabability = 0.1, in 0 it is 0.5, never 1
                # y-axis: half results must be wrong, half correct,
                # on the edges, results must be mostly correct
                
                # if (uniform_output > gaussian_threshold):
                # colore rosso (col_res = rosso)
                # else colore verde
                if(uniform_output > gaussian_threshold):
                    result = 0
                    plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "green")
                    correct_vector.append(result)
                else:
                    result = 1
                    plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "red")
                    correct_vector.append(result)
            
        elif (alpha == 0 and sigma != 0):
            if (num_array_ratio[i] == 0):
                # No plot
                correct_vector.append(1)
                continue
            else:
                # Sharpening effect only
                uniform_output = UniformOutput()
                gaussian_threshold = GaussianThreshold(mu, sigma, num_array_ratio[i])
                
                if(uniform_output > gaussian_threshold):
                    result = 0
                    plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "green")
                    correct_vector.append(result)
                else:
                    result = 1
                    plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "red")
                    correct_vector.append(result)
                
        elif(alpha != 0 and sigma == 0):
            # Filtering effect only
            if((fa_array_ratio[i] - (coeff * num_array_ratio[i])) == 0):
                plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "red")
                correct_vector.append(1)
            elif( ((fa_array_ratio[i] - (coeff * num_array_ratio[i]) > 0) and (( (fa_array_ratio[i] > 0) and (num_array_ratio[i] < 0) ))) 
                 or ((fa_array_ratio[i] - (coeff * num_array_ratio[i]) < 0) and (( (fa_array_ratio[i] < 0) and (num_array_ratio[i] > 0) ))) 
                 ):
                plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "red")
                correct_vector.append(1)
            elif(num_array_ratio[i] == 0):
                # No plot
                correct_vector.append(1)
                continue
            else:
                plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "green")
                correct_vector.append(0)
            
        elif(alpha == 0 and sigma == 0):
            if (num_array_ratio[i] == 0):
                # No plot
                correct_vector.append(1)
                continue
            else:
                plt.scatter(num_array_ratio[i], fa_array_ratio[i], c = "green")
                correct_vector.append(0)
    
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    
    plt.plot(x, coeff*x, '-y')
    
    plt.xlim([-1, 1])
    plt.ylim([-1, 1])
    plt.grid(True)
    
    plt.title("Filtering + Sharpening Effect on FA_Ratio/Num_Ratios")
    
numDataPoints = len(t)
    
validity = ValidTrial(medium_num, medium_fa, medium_isa) # Medium point returns valid! YAY!

GenerateNewTrialLeft(0, medium_num, min_inc_num, medium_fa, min_inc_fa, medium_isa, min_inc_isa)
GenerateNewTrialRight(0, medium_num, min_inc_num, medium_fa, min_inc_fa, medium_isa, min_inc_isa)

CalculateRatio()
PlotPlane()

line_ani_left = animation.FuncAnimation(fig, animate_func_left, interval=100, frames = numDataPoints)
line_ani_right = animation.FuncAnimation(fig1, animate_func_right, interval=100, frames = numDataPoints)
line_ani_ratio = animation.FuncAnimation(fig2, animate_func_ratio, interval=100, frames = numDataPoints)

plt.show()

dataSet_left = np.array([fa_array_left, isa_array_left, num_array_left])
dataSet_right = np.array([fa_array_right, isa_array_right, num_array_right])
dataSet_ratio = np.array([fa_array_ratio, isa_array_ratio, num_array_ratio])

f_l = r"C://Users/Client/Desktop/todeleteL.gif"
f_r = r"C://Users/Client/Desktop/todeleteR.gif"
f_R = r"C://Users/Client/Desktop/todeleteRat.gif"

writergif_l = animation.PillowWriter(fps = numDataPoints)
line_ani_left.save(f_l, writer=writergif_l)

writergif_r = animation.PillowWriter(fps = numDataPoints)
line_ani_right.save(f_r, writer=writergif_r)

writergif_ratio = animation.PillowWriter(fps = numDataPoints)
line_ani_ratio.save(f_R, writer=writergif_ratio)