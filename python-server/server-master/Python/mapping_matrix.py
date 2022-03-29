'''
dummy_trials_matrix = [
    area_1_number_of_chickens = array[0] 
    area_2_number_of_chickens = array[1] 
    area_1_field_area = array[2]
    area_2_field_area = array[3]
    area_1_item_surface_area = array[4]
    area_2_item_surface_area = array[5]
    chicken_show_time = array[6]
    max_trial_time = array[7]
    ]
'''

# INITIALIZATION of an empty trial_matrix and the nnd_number (can be changed)
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
                        
                        trials_row.append(nv1)
                        trials_row.append(nv2)
                        trials_row.append(nnd1)
                        trials_row.append(nnd2)
                        
                        temp_matrix.append(trials_row)
                        
    return temp_matrix

# dummy_matrix_generator function takes as parameter the nnd_selector and the 
# nnd_number. Depending on the selector passed, the function computes a trials 
# matrix, by exploiting another function, called partial_matrix_generator, 
# thanks to which the matrix is computed by maintaining some parameters fixed 
# and some other instead vary, and the variation is computed thanks to 
# partial_matrix_generator function, called inside.
# The parameters that remain fixed and the one that vary (which is always a 
# non-numerical value, alongside the numerical one) are decided by the 
# nnd_selector given as parameter: if nnd_selector is equal to 1, then field_area
# value varies; if it is equal to 2, it is the viceversa.
# nnd_number parameter controls the number of trials to compute which will be
# equal to the nnd_number elevated to 4.

def dummy_matrix_generator(nnd_selector, nnd_number):
    if nnd_selector == 1:
        # nnd_selector = 1 means we want to vary the value of field_area as 
        # nnd, alongside the numerical value, number_of_chickens. The other,
        # item_surface_area, is fixed
        item_surface_area = 10
        temp_matrix = partial_matrix_generator(0.2, 0.3, 0.2, 0.3, nnd_number
                                      , 1, 2, 1, 2)
        
        # We scan the obtained partial matrix, and for each row, we append the
        # various fields in the right position in the matrix
        for row in temp_matrix:
            trials_list = []
            trials_list.append(row[0])
            trials_list.append(row[1])
            trials_list.append(row[2])
            trials_list.append(row[3])
            trials_list.append(item_surface_area)
            trials_list.append(item_surface_area)
            
            trials_matrix.append(trials_list)
        
    elif nnd_selector == 2:
        # nnd_selector = 1 means we want to vary the value of 
        # item_surface_area as nnd, alongside the numerical value, 
        # number_of_chickens. The other, field_area, is fixed.
        field_area = 300
        temp_matrix = partial_matrix_generator(0.1, 0.1, 0.1, 0.1, nnd_number
                                      , 1, 1, 1, 1)
        
        # We scan the obtained partial matrix, and for each row, we append the
        # various fields in the right position in the matrix
        for row in temp_matrix:
            trials_list = []
            trials_list.append(row[0])
            trials_list.append(row[1])            
            trials_list.append(field_area)
            trials_list.append(field_area)
            trials_list.append(row[2])
            trials_list.append(row[3])
            
            trials_matrix.append(trials_list)
            
    # print(trials_matrix)            
    return trials_matrix