import math 

trials_matrix = []

# This function accepts as a paramater the original trials matrix, passed from 
# the main, the one made of Number, Field Area and Item Surface Area, and
# applies some transformations in order to obtain a matrix that is compatible 
# with the game, meaning that the matrix must include circle_radius, size_of_chicken
# and average_space_between parameters, and not field_area and item_surface_area

# The trials_matrix will be made of the following fields:
    
        # --> First and second columns are called area_1_circle_radius and
        # area_2_circle_radius and those define the circle radius of both areas
        
        # --> Third and fourth columns are called area_1_size_of_chicken and
        # area_2_size_of_chicken, so define how big the chicken must be in that area
        
        # --> Fifth and sixth columns are called area_1_average_space_between and
        # area_2_average_space_between, define the space that separes one chicken 
        # by another one, on average, in each area
        
        # --> Seventh and eighth colums are called area_1_number_of_chickens and
        # area_2_number_of_chickens, which tells us how many chickens must be showed
        # in each area
        
        # --> Nineth column is called chicken_show_time, indicates how long the 
        # chickens are shown on the screen
        
        # --> Tenth column is called max_trial_time and defines the total duration 
        # of the game / trial

def TransformMatrix(trials_matrix_original):
    
    for row in trials_matrix_original:
        area_1_circle_radius = ((0.006) * math.sqrt(row[2]))
        area_2_circle_radius = ((0.006) * math.sqrt(row[3]))
        
        area_1_size_of_chicken = 0.57 * math.sqrt(row[4])
        area_2_size_of_chicken = 0.57 * math.sqrt(row[5])
        
        area_1_average_space_between = (0.167 * area_1_size_of_chicken) + 0.183
        area_2_average_space_between = (0.167 * area_2_size_of_chicken) + 0.183
        
        trials_row = []
        
        trials_row.append(area_1_circle_radius)
        trials_row.append(area_2_circle_radius)
        trials_row.append(area_1_size_of_chicken)
        trials_row.append(area_2_size_of_chicken)
        trials_row.append(area_1_average_space_between)
        trials_row.append(area_2_average_space_between)
        trials_row.append(row[0])   # Number of Chicken 1
        trials_row.append(row[1])   # Number of Chicken 2
        trials_row.append(row[6])
        trials_row.append(row[7])
        trials_row.append(row[8])   # ND   
        trials_row.append(row[9])   # NND
        trials_row.append(row[10])  # type of question (greater fence/smaller fence)
        
        trials_matrix.append(trials_row)
    
    return trials_matrix