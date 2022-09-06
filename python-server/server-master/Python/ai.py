# Artificial Intelligence

import pandas as pd
import random

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
            if(fa <= dataset[i][1]):
                # FA ok. Check for ISA validity
                if(isa <= dataset[i][2]):
                    # ISA ok. The point is valid, set the isValid variable and break the loop
                    isValid = 1
                    break
                else:
                    # if ISA is not valid, continue to the next iteration
                    continue
            else:
                # if FA is not valid, continue to the next iteration
                continue
        else:
            # if number is not valid, continue to the next iteration
            continue
        
    # Reaching the end of the loop means that no match is found, so isValid is 0,
    # as it was set at the beginning
    return isValid

# Minimum increment for FA and ISA is defined as Max + Min divided by 100
def MinimumIncrement(min_value, max_value):
    return (min_value + max_value) / 100

def GenerateNewTrialLeft(num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa):
    
    left_array = []
    
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
        
    pointIsValid = ValidTrial(new_num, new_fa, new_isa)
    
    if(pointIsValid == 0 or num < 0):
        return GenerateNewTrialLeft(num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa)
    else:
        print(new_num)
        print(new_fa)
        print(new_isa)
        print("point is valid")
        
        left_array.append(new_num)
        left_array.append(new_fa)
        left_array.append(new_isa)
        
        # ax_l.scatter3D(new_fa, new_isa, new_num, marker='o', label="Valid", c="green")
        
        return left_array

def GenerateNewTrialRight(num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa):
    
    right_array = []
    
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
        
    pointIsValid = ValidTrial(new_num, new_fa, new_isa)
    
    if(pointIsValid == 0 or num < 0):
        return GenerateNewTrialLeft(num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa)
    else:
        print(new_num)
        print(new_fa)
        print(new_isa)
        print("point is valid")
        
        right_array.append(new_num)
        right_array.append(new_fa)
        right_array.append(new_isa)
        
        # ax_l.scatter3D(new_fa, new_isa, new_num, marker='o', label="Valid", c="green")
        
        return right_array

# Function to evaluate the difficulty of the trial (for now, I just evaluate the 
# difficulty of the numerical variable)
def TrialDifficulty(left_array, right_array, correct):
    new_parameters = []
    
    # Number is in position 0, so I must check on that position for these arrays
    # I received as parameter
    
    if(left_array[0] / right_array[0] == 0.1 and correct == 0):
        # augment the difficulty because that was an easy trial and the answer was correct
        # --> choose two new numbers
        left_number = 10
        right_number = 12
        new_left_array = GenerateNewTrialLeft(left_number, 1, left_array[1], 456.25, left_array[2], 3.27)
        new_right_array = GenerateNewTrialRight(right_number, 1, right_array[1], 456.25, right_array[2], 3.27)
        
    new_parameters.append(new_left_array)
    new_parameters.append(new_right_array)
    
    return new_parameters
        
def UploadDifficultyCoefficient():
    # Uploading data from excel fileù
    numpy_column = []
    
    data = pd.read_excel("./dataset/diff_coefficients.xlsx", 
                         dtype = {'NumLeft': int, 'FieldAreaLeft': float, 'ItemSurfaceAreaLeft': float,
                                  'NumRight': int, 'FieldAreaRight': float, 'ItemSurfaceAreaRight': float,
                                  'Ratio L/R': float, 'LogRatio': float, 'Log - Normalized': float, "Difficulty Coefficient": float})
    df = pd.DataFrame(data, columns = ['NumLeft','FieldAreaLeft', 'ItemSurfaceAreaLeft',
                                       'NumRight', 'FieldAreaRight', 'ItemSurfaceAreaRight',
                                       'Ratio L/R', 'LogRatio', 'Log - Normalized',
                                       'Difficulty Coefficient'])
    
    numpy_array = df.to_numpy()
    
    for i in range(len(numpy_array)):
        numpy_column.append(round(numpy_array[i][9], 2))
    
    return numpy_array

# La funzione deve selezionare una entry nella tabella in base al coefficiente di difficoltà
# La prima selezione avviene con coefficiente di difficoltà pari a 0.5, poi si tiene in consi-
# derazione la correttezza della risposta: se è corretta, si aumenta il coeff di difficoltà
# quindi si seleziona una entry che corrisponde a un coeff più alto, se no si scende

def SelectTrial(prev_parameters = None, correct = None):
    
    selected_combination = []
    
    data = pd.read_excel("./dataset/diff_coefficients.xlsx", 
                         dtype = {'NumLeft': int, 'FieldAreaLeft': float, 'ItemSurfaceAreaLeft': float,
                                  'NumRight': int, 'FieldAreaRight': float, 'ItemSurfaceAreaRight': float,
                                  'Ratio L/R': float, 'LogRatio': float, 'Log - Normalized': float, "Difficulty Coefficient": float})
    
    df = pd.DataFrame(data, columns = ['NumLeft','FieldAreaLeft', 'ItemSurfaceAreaLeft',
                                       'NumRight', 'FieldAreaRight', 'ItemSurfaceAreaRight',
                                       'Ratio L/R', 'LogRatio', 'Log - Normalized',
                                       'Difficulty Coefficient'])
    
    possible_combination_matrix = df.to_numpy()
    
    if correct == None:
        for i in range(len(possible_combination_matrix)):
            if(round(possible_combination_matrix[i][9], 1) == 0.5):
                selected_combination.append(possible_combination_matrix[i][0]) # NumLeft
                selected_combination.append(possible_combination_matrix[i][1]) # FieldAreaLeft
                selected_combination.append(possible_combination_matrix[i][2]) # ItemSurfaceAreaLeft
                selected_combination.append(possible_combination_matrix[i][3]) # NumRight
                selected_combination.append(possible_combination_matrix[i][4]) # FieldAreaRight
                selected_combination.append(possible_combination_matrix[i][5]) # ItemSurfaceAreaRight
                selected_combination.append(possible_combination_matrix[i][6]) # Ratio L/R (prob non serve)
                selected_combination.append(possible_combination_matrix[i][7]) # LogRatio (prob non serve)
                selected_combination.append(possible_combination_matrix[i][8]) # Log - Normalized (prob non serve)
                selected_combination.append(possible_combination_matrix[i][9]) # Difficulty Coefficient
                
                break
                
                
    else:
        if (correct == 0):
            new_difficulty_coefficient = prev_parameters[9] + 0.1
            
            for i in range(len(possible_combination_matrix)):
                if(round(possible_combination_matrix[i][9], 1) == round(new_difficulty_coefficient, 1)):
                    selected_combination.append(possible_combination_matrix[i][0]) # NumLeft
                    selected_combination.append(possible_combination_matrix[i][1]) # FieldAreaLeft
                    selected_combination.append(possible_combination_matrix[i][2]) # ItemSurfaceAreaLeft
                    selected_combination.append(possible_combination_matrix[i][3]) # NumRight
                    selected_combination.append(possible_combination_matrix[i][4]) # FieldAreaRight
                    selected_combination.append(possible_combination_matrix[i][5]) # ItemSurfaceAreaRight
                    selected_combination.append(possible_combination_matrix[i][6]) # Ratio L/R (prob non serve)
                    selected_combination.append(possible_combination_matrix[i][7]) # LogRatio (prob non serve)
                    selected_combination.append(possible_combination_matrix[i][8]) # Log - Normalized (prob non serve)
                    selected_combination.append(possible_combination_matrix[i][9]) # Difficulty Coefficient
                    
                    break
                    
        elif (correct == 1):
            new_difficulty_coefficient = prev_parameters[9] - 0.1
            
            for i in range(len(possible_combination_matrix)):
                if(round(possible_combination_matrix[i][9], 1) == round(new_difficulty_coefficient, 1)):
                    selected_combination.append(possible_combination_matrix[i][0]) # NumLeft
                    selected_combination.append(possible_combination_matrix[i][1]) # FieldAreaLeft
                    selected_combination.append(possible_combination_matrix[i][2]) # ItemSurfaceAreaLeft
                    selected_combination.append(possible_combination_matrix[i][3]) # NumRight
                    selected_combination.append(possible_combination_matrix[i][4]) # FieldAreaRight
                    selected_combination.append(possible_combination_matrix[i][5]) # ItemSurfaceAreaRight
                    selected_combination.append(possible_combination_matrix[i][6]) # Ratio L/R (prob non serve)
                    selected_combination.append(possible_combination_matrix[i][7]) # LogRatio (prob non serve)
                    selected_combination.append(possible_combination_matrix[i][8]) # Log - Normalized (prob non serve)
                    selected_combination.append(possible_combination_matrix[i][9]) # Difficulty Coefficient
                    
                    break
                    
                    
    return selected_combination
            
            
        

    
# compute the max unbalancing left/right and do the log of this max unbalancing and take the abs
# THIS IS THE MAX DIFFICULTY POSSIBLE; then, INPUT to trialdiff function the max easiness, defined as the log
# of two most different numbers in abs value; the max difficulty is in principle 0, in practise it must be
# the abs of the smallest ratio of the number.

# PROVARE A COMPUTARE LA EASINESS DIRETTAMENTE NELL'EXCEL, tramite log.
# computare il log dei numeri più distanti, poi normalizzare ogni numero, cioè dividendo ogni altro possibile
# risultato per quel numero lì. I risultati saranno tra 0 e 1, dove 0 indica più facile e 1 più difficile.