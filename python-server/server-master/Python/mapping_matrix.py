'''
dummy_trials_matrix = [
    area_1_circle_radius = array[0] 
    area_2_circle_radius = array[1] 
    area_1_size_of_chicken = array[2]
    area_2_size_of_chicken = array[3]
    area_1_average_space_between = array[4]
    area_2_average_space_between = array[5]
    area_1_number_of_chickens = array[6]
    area_2_number_of_chickens = array[7]
    chicken_show_time = array[8]
    max_trial_time = array[9]
    ]
'''

# INITIALIZATION of an empty trial_matrix and the nnd_number (can be changed)
# spostare nnd_number nel main.py
nnd_number = 5
trials_matrix = []

# This function has the purpose of taking the initial value of the first and 
# the second nnd, as well as the first and the second nv, alongside their step,
# that is the way they are incremented. And finally it takes the nnd_number,
# which is needed to guide the for cycle.
def partial_matrix_generator(nnd1_start, nnd1_step, nnd2_start, nnd2_step, nnd_number
                    , nv1_start, nv1_step, nv2_start, nv2_step):
    temp_matrix = []
    nnd1 = 0
    for i in range (nnd_number + 1):
        if (i == 1):
            nnd1 = nnd1_start
        else:
            nnd1 += nnd1_step
            
            for k in range(nnd_number):
                if (k == 0):
                    nnd2 = nnd2_start
                else:
                    nnd2 += nnd2_step
                    
                for j in range(nnd_number):
                    if (j == 0):
                        nv1 = nv1_start
                    else:
                        nv1 += nv1_step
                        
                    for l in range(nnd_number):
                        if (l == 0):
                            nv2 = nv2_start
                        else: 
                            nv2 += nv2_step
                            
                        trials_row = []
                        
                        trials_row.append(nnd1)
                        trials_row.append(nnd2)
                        trials_row.append(nv1)
                        trials_row.append(nv2)
                        
                        temp_matrix.append(trials_row)
                        
    return temp_matrix

# dummy_matrix_generator function takes as parameter the nnd_selector. Depending 
# on the selector passed, the function computes a trials matrix, by exploiting 
# another function, called partial_matrix_generator, thanks to which the matrix 
# is computed by maintaining some parameters fixed and some other instead vary, 
# and the variation is computed thanks to partial_matrix_generator.
# The parameters that remain fixed and the one that vary (which is always a 
# non-numerical value, alongside the numerical one) are decided by the 
# nnd_selector given as parameter.
def dummy_matrix_generator(nnd_selector):
    if nnd_selector == 1:
        # nnd_selector = 1 means we want to vary the value of circle_radius as 
        # nnd, alongside the numerical value, number_of_chickens. The others,
        # average_space_between and size_of_chicken, are fixed
        average_space_between = 1.5 
        size_of_chicken = 5 
        temp_matrix = partial_matrix_generator(0.2, 0.3, 0.2, 0.3, nnd_number
                                      , 1, 2, 1, 2)
        
        # We scan the obtained partial matrix, and for each row, we append the
        # various fields in the right position in the matrix
        for row in temp_matrix:
            trials_list = []
            trials_list.append(row[0])
            trials_list.append(row[1])
            trials_list.append(size_of_chicken)
            trials_list.append(size_of_chicken)
            trials_list.append(average_space_between)
            trials_list.append(average_space_between)
            trials_list.append(row[2])
            trials_list.append(row[3])
            
            trials_matrix.append(trials_list)
        
    elif nnd_selector == 2:
        # nnd_selector = 2 means we want to vary the value of size_of_chicken as 
        # nnd, alongside the numerical value, number_of_chickens. The others,
        # circle_radius and average_space_between, are fixed
        circle_radius = 0.1
        average_space_between = 1.5 
        temp_matrix = partial_matrix_generator(0.1, 0.1, 0.1, 0.1, nnd_number
                                      , 1, 1, 1, 1)
        
        # We scan the obtained partial matrix, and for each row, we append the
        # various fields in the right position in the matrix
        for row in temp_matrix:
            trials_list = []
            trials_list.append(circle_radius)
            trials_list.append(circle_radius)
            trials_list.append(row[0])
            trials_list.append(row[1])
            trials_list.append(average_space_between)
            trials_list.append(average_space_between)
            trials_list.append(row[2])
            trials_list.append(row[3])
            
            trials_matrix.append(trials_list)
        
    elif nnd_selector == 3: 
        # nnd_selector = 3 means we want to vary the value of average_space_between  
        # as nnd, alongside the numerical value, number_of_chickens. The others,
        # circle_radius and size_of_chicken, are fixed
        circle_radius = 0.1
        size_of_chicken = 5
        temp_matrix = partial_matrix_generator(0.2, 0.5, 0.2, 0.5, nnd_number
                                      , 2, 3, 2, 3)
        
        # We scan the obtained partial matrix, and for each row, we append the
        # various fields in the right position in the matrix
        for row in temp_matrix:
            trials_list = []
            trials_list.append(circle_radius)
            trials_list.append(circle_radius)
            trials_list.append(size_of_chicken)
            trials_list.append(size_of_chicken)
            trials_list.append(row[0])
            trials_list.append(row[1])
            trials_list.append(row[2])
            trials_list.append(row[3])
            
            trials_matrix.append(trials_list)
            
    # print(trials_matrix)            
    return trials_matrix