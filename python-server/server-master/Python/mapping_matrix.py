'''
dummy_trials_matrix = [
    0 --> "area_1_circle_radius", 
    1 --> "area_1_size_of_chicken",
    2 --> "area_1_average_space_between", 
    3 --> "area_1_number_of_chickens", 
    4 --> "area_2_circle_radius", 
    5 --> "area_2_size_of_chicken", 
    6 --> "area_2_average_space_between", 
    7 --> "area_2_number_of_chickens"
    ]
'''
n = 5

def matrix_circle_radius():
    trials_matrix = []
    average_space_between = 1.5 
    size_of_chicken = 0.5 
    
    # circle_radius range is [0.2, 0.5, 0.8, 1.1, 1.4]
    # number_of_chickens range is [1, 3, 5, 7, 9]
    
    for i in range (n):
        if (i == 0):
            circle_radius = 0.2
        else:
            circle_radius += 0.3
        number_of_chickens = 1 #(random.randint(8, 15)) 
        circle_radius2 = 0.2
        number_of_chickens2 = 1
        
        for j in range (n):
            if(j == 0):
                circle_radius2 = 0.2
            else:
                circle_radius2 += 0.3
            number_of_chickens = 1
            number_of_chickens2 = 1
            
            for k in range(n):
                if(k == 0):
                    number_of_chickens = 1
                else: 
                    number_of_chickens += 2
                number_of_chickens2 = 1
                
                for l in range(n):
                    if(l == 0):
                        number_of_chickens2 = 1
                    else: 
                        number_of_chickens2 += 2
            
                    trials_list = []
                    
                    trials_list.append(circle_radius)
                    trials_list.append(size_of_chicken)
                    trials_list.append(average_space_between)
                    trials_list.append(number_of_chickens)
                    trials_list.append(circle_radius2)
                    trials_list.append(size_of_chicken)
                    trials_list.append(average_space_between)
                    trials_list.append(number_of_chickens2)
                    
                    trials_matrix.append(trials_list)
                    
    return (trials_matrix)

def matrix_size_chickens():
    trials_matrix = []
    circle_radius = 0.1
    average_space_between = 1.5 
    
    for i in range (n):
        if (i == 0):
            size_of_chicken = 0.1
        else:
            size_of_chicken += 0.1
        
        size_of_chicken2 = 0.1
        number_of_chickens = 1 #(random.randint(8, 15)) 
        number_of_chickens2 = 1

        
        for j in range (n):
            if(j == 0):
                size_of_chicken2 = 0.1
            else:
                size_of_chicken2 += 0.1
            number_of_chickens = 1
            number_of_chickens2 = 1
            
            for k in range(n):
                if(k == 0):
                    number_of_chickens = 1
                else: 
                    number_of_chickens += 1
                
                for l in range(n):
                    if(l == 0):
                        number_of_chickens2 = 1
                    else: 
                        number_of_chickens2 += 1
            
                    trials_list = []
                    
                    trials_list.append(circle_radius)
                    trials_list.append(size_of_chicken)
                    trials_list.append(average_space_between)
                    trials_list.append(number_of_chickens)
                    trials_list.append(circle_radius)
                    trials_list.append(size_of_chicken2)
                    trials_list.append(average_space_between)
                    trials_list.append(number_of_chickens2)
                    
                    trials_matrix.append(trials_list)
    return (trials_matrix)

def matrix_space_between():
    trials_matrix = []
    average_space_between = -0.3 #round (random.uniform(1,2), 1)
    circle_radius = 0.1
    size_of_chicken = 0.5
    
    # number_of_chickens = 2, poi crescita a +3 (stabile)
    
    for i in range (n):
        if (i == 0):
            average_space_between = 0.2
        else:
            average_space_between += 0.5
        average_space_between2 = 0.2
        number_of_chickens = 2 #(random.randint(8, 15)) 
        number_of_chickens2 = 2
        
        for j in range (n):
            if(j == 0):
                average_space_between2 = 0.2
            else:
                average_space_between2 += 0.3
            number_of_chickens = 2
            number_of_chickens2 = 2
            
            for k in range(n):
                if(k == 0):
                    number_of_chickens = 2
                else: 
                    number_of_chickens += 3
                number_of_chickens2 = 2
                
                for l in range(n):
                    if(l == 0):
                        number_of_chickens2 = 2
                    else: 
                        number_of_chickens2 += 3
            
                    trials_list = []
                    
                    trials_list.append(circle_radius)
                    trials_list.append(size_of_chicken)
                    trials_list.append(average_space_between)
                    trials_list.append(number_of_chickens)
                    trials_list.append(circle_radius)
                    trials_list.append(size_of_chicken)
                    trials_list.append(average_space_between2)
                    trials_list.append(number_of_chickens2)
                    
                    trials_matrix.append(trials_list)
                    
    return (trials_matrix)
    
def matrix_on_indicator(indicator):
    if indicator == 1:
        return matrix_circle_radius()
    elif indicator == 2:
        return matrix_size_chickens()
    else: 
        return matrix_space_between()