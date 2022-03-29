# Starting point of AI

import pandas as pd
import random
from matplotlib import pyplot as plt

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

numpy_array = []

fa_array = []
isa_array = []
num_array = []

dataSet = []

# Time Array
t = np.linspace(0, 20, 100)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('Field Area')
ax.set_ylabel('Item Surface Area')
ax.set_zlabel('Number of Chickens')

ax.view_init(20, 20)

def animate_func(num):
    ax.clear()  # Clears the figure to update the line, point,   
                # title, and axes
    # Updating Trajectory Line (num+1 due to Python indexing)
    ax.plot3D(dataSet[0, :num+1], dataSet[1, :num+1], 
              dataSet[2, :num+1], c='blue')
    # Updating Point Location 
    ax.scatter(dataSet[0, num], dataSet[1, num], dataSet[2, num], 
               c='blue', marker='o')
    # Adding Constant Origin
    ax.plot3D(dataSet[0, 0], dataSet[1, 0], dataSet[2, 0],     
               c='black', marker='o')

    # Adding Figure Labels
    ax.set_title('Trajectory \nTime = ' + str(np.round(t[num],    
                 decimals=2)) + ' sec')

    ax.set_xlabel('Field Area')
    ax.set_ylabel('Item Surface Area')
    ax.set_zlabel('Number of Chickens')
    

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
def GenerateNewTrial(i, num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa):
    
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
            fa_array.append(fa)
            isa_array.append(isa)
            num_array.append(num)
            ax.scatter3D(fa, isa, num, marker='<', label="Invalid", c="red")
            return GenerateNewTrial(i, num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa)
        else:
            print(num)
            print(fa)
            print(isa)
            print("point is valid")
            fa_array.append(new_fa)
            isa_array.append(new_isa)
            num_array.append(new_num)
            ax.scatter3D(new_fa, new_isa, new_num, marker='o', label="Valid", c="green")
            return GenerateNewTrial(i, new_num, min_inc_num, new_fa, min_inc_fa, new_isa, min_inc_isa)
    
numDataPoints = len(t)
    
validity = ValidTrial(medium_num, medium_fa, medium_isa) # Medium point returns valid! YAY!

GenerateNewTrial(0, medium_num, min_inc_num, medium_fa, min_inc_fa, medium_isa, min_inc_isa)

line_ani = animation.FuncAnimation(fig, animate_func, interval=100, frames = numDataPoints)

plt.show()

dataSet = np.array([fa_array, isa_array, num_array])

f = r"C://Users/Client/Desktop/animate_func.gif"

writergif = animation.PillowWriter(fps = numDataPoints)
line_ani.save(f, writer=writergif)