# Uploading data from excel file

import pandas as pd
import random

# data = pd.read_excel (r'C:\Users\Ron\Desktop\Product List.xlsx') 
# df = pd.DataFrame(data, columns= ['Product','Price'])
# print (df)

numpy_array = []

def UploadDataFromExcelDataset():
    data = pd.read_excel("./dataset/dataset_for_server.xlsx", dtype = {'NumChickens': int, 'FieldArea': float, 'ItemSurfaceArea': float})
    df = pd.DataFrame(data, columns = ['NumChickens','FieldArea', 'ItemSurfaceArea'])
    
    numpy_array = df.to_numpy()
    
    return numpy_array

def FindMinAndMaxValuesFromDataset():
    numpy_array = UploadDataFromExcelDataset()
    
    return_array = []
    
    max_num = 0
    max_fa = 0
    max_isa = 0
 
    for i in range(len(numpy_array)):
        # Scan every single element of the matrix
        # Find the max of any of those three parameters 
        if(max_num < numpy_array[i][0]):
            max_num = numpy_array[i][0]
        
        if(max_fa < numpy_array[i][1]):
            max_fa = numpy_array[i][1]
            
        if(max_isa < numpy_array[i][2]):
            max_isa = numpy_array[i][2]
            
    min_num = max_num
    min_fa = max_fa
    min_isa = max_isa
    
    for i in range(len(numpy_array)):
        # Scan every single element of the matrix
        # Find the min of any of those three parameters 
        if(min_num > numpy_array[i][0]):
            min_num = numpy_array[i][0]
        
        if(min_fa > numpy_array[i][1]):
            min_fa = numpy_array[i][1]
            
        if(min_isa > numpy_array[i][2]):
            min_isa = numpy_array[i][2]
            
    return_array.append(max_num)
    return_array.append(max_fa)
    return_array.append(max_isa)     
    return_array.append(min_num)
    return_array.append(min_fa)
    return_array.append(min_isa)
     
    return return_array      


# Generate Randomically 3 numbers: 
    # The first one will be the number of chickens
    # The second one will be the field area
    # the third one will be the item surface area    
def GenerateRandomNumberFAandISA():
    max_and_min_array = FindMinAndMaxValuesFromDataset()
    
    random_array = []
        
    random_num = random.random()*(max_and_min_array[0] - max_and_min_array[3]) + max_and_min_array[3]
    random_fa = random.random()*(max_and_min_array[1] - max_and_min_array[4]) + max_and_min_array[4]
    random_isa = random.random()*(max_and_min_array[2] - max_and_min_array[5]) + max_and_min_array[5]
    
    random_array.append(random_num)
    random_array.append(random_fa)
    random_array.append(random_isa)
    
    return random_array

def FunzioneTemp():
    matrice_temp = [[20, 16717, 60], [10, 2400, 160], [4, 8300, 170], [10, 5000, 307.79]]
    
    return matrice_temp


def GenerateNewTrial():
    numpy_array = UploadDataFromExcelDataset()
    # random_array = GenerateRandomNumberFAandISA()
    matrice_temp = FunzioneTemp()

    # Ora arriva la parte divertente
    
    for i in range(len(matrice_temp)):
        for j in range(len(numpy_array)):
            if(matrice_temp[i][0] < numpy_array[j][0]):
                print('Numero ok')
                print(matrice_temp[i][0])
                print(numpy_array[j][0])
                if(matrice_temp[i][1] < numpy_array[j][1]):
                    print("Field area ok")
                    print(matrice_temp[i][1])
                    print(numpy_array[j][1])
                    if(matrice_temp[i][2] < numpy_array[j][2]):
                        print("Isa ok")
                        print(matrice_temp[i][2])
                        print(numpy_array[j][2])
                        #print(j)
                        #print(i)
                    
            else:
                print(j) 
                # print("Continuo a cercare")
        
            
    return numpy_array     


numpy_array = GenerateNewTrial()