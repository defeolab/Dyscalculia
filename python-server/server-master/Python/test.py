# Starting point of AI

import pandas as pd
import random

numpy_array = []

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
    

# Quando la funzione funziona, si fa un altro progettino
# Calcolo punto medio (val medio di N (32), val medio di FA (una cosa a metà)
# e val medio di ISA (una cosa a metà) --> a penna)
# Definire incremento minimo di N, FA e ISA.
# Alla funzione do il punto medio e mi deve dare true.
# Parto dal punto medio, e x ogni dim creo un numero random (-1, 0, +1)
# Se 0, il nuovo punto NON HA VARIAZIONE, se +1, il nuovo punto sarà punto medio + inc minimo
# Se -1 il nuovo punto sarà punto medio - inc minimo.
# Questo punto che trovo lo do alla funzione: se la funzione dice ok, allora quello
# sarà il nostro punto, altrimenti si genera un nuovo punto con tre nuovi valori random.

# The following function should calculate the medium point between a max and a min
def MediumPoint(min_value, max_value):
    return (min_value + max_value) / 2

# Starting values: giving them some constant values (guardare lo spazio a occhio)
# representing the space to plot the point --> trajectory
medium_num = MediumPoint(1, 112)
medium_fa = MediumPoint(5625, 40000)
medium_isa = MediumPoint(19.24, 307.79)


def MinimumIncrement(min_value, max_value):
    return (min_value + max_value) / 100

def GenerateNewTrial(num, min_inc_num, fa, min_inc_fa, isa, min_inc_isa):
    random_dim_1 = random.randint(0, 2) - 1 # for number
    random_dim_2 = random.randint(0, 2) - 1 # for FA
    random_dim_3 = random.randint(0, 2) - 1 # for ISA
    
    if (random_dim_1 == -1):
        num = num - min_inc_num
    elif (random_dim_1 == 1):
        num = num + min_inc_num
        
    if (random_dim_2 == -1):
        fa = fa - min_inc_fa
    elif (random_dim_2 == 1):
        fa = fa + min_inc_fa
        
    if (random_dim_3 == -1):
        isa = isa - min_inc_isa
    elif (random_dim_3 == 1):
        isa = isa + min_inc_isa
        
    pointIsValid = ValidTrial(num, fa, isa)
    if(pointIsValid == 0):
        print("The point is invalid. Run again this function")
    else:
        print("point is valid")
    
validity = ValidTrial(21, medium_fa, medium_isa)
print(validity)