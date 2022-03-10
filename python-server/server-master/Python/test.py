import pandas as pd
import random

numpy_array = []

def UploadDataFromExcelDataset():
    # Uploading data from excel file
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


# Generate Randomically 3 numbers, taken in the interval between the max and the min: 
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

# Control function, to check whether the point (represented by the three 
# coordinates, Number-Fa-ISA) is a valid point, i.e. it is below the curve,
# or not. Returns 1 for a valid point, 0 otherwise
def ValidTrial(number, fa, isa):
    
    dataset = UploadDataFromExcelDataset()
    isValid = 0
    
    for i in range(len(dataset)):
        if(number < dataset[i][0]):
            # Number ok. Check for FA validity
            print("Number ok")
            if(fa < dataset[i][1]):
                # FA ok. Check for ISA validity
                print("FA ok")
                if(isa < dataset[i][2]):
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
    
validity = ValidTrial(10, 5000, 307.79)
print(validity)

def GenerateNewTrial():
    # Funzione di controllo NOME: ValidTrial(Number, FA, ISA)
    # INPUT: number, FA, ISA
    # OUTPUT: boolean --> 0 non ammissibile, 1 ammissibile
    
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