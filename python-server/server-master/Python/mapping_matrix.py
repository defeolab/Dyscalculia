"""
Created on Tue Aug 17 10:41:50 2021

@author: oyekp
"""


'''
dummy_trials_matrix = [
    "area_1_circle_radius", 
    "area_1_size_of_chicken",
    "area_1_average_space_between", 
    "area_1_number_of_chickens", 
    "area_2_circle_radius", 
    "area_2_size_of_chicken", 
    "area_2_average_space_between", 
    "area_2_number_of_chickens", 
    "ratio"
    ]
'''
#import random
n = 5
ratio = 1

def matrix_circle_radius():
    trials_matrix = []
    circle_radius = -0.1 #(round (random.uniform(0.1,1),4))
    
    # circle_radius range is [0.2, 0.5, 0.8, 1.1, 1.4]
    # number_of_chickens range is [1, 3, 5, 7, 9]
    for i in range (n):
        circle_radius += 0.3
        number_of_chickens = 1 #(random.randint(8, 15)) 
        average_space_between = 1.5 
        size_of_chicken = 0.5 
        circle_radius2 = 0.2
        number_of_chickens2 = 1
    
        trials_list1 = []
        
        trials_list1.append(circle_radius)
        trials_list1.append(size_of_chicken)
        trials_list1.append(average_space_between)
        trials_list1.append(number_of_chickens)
        trials_list1.append(circle_radius2)
        trials_list1.append(size_of_chicken)
        trials_list1.append(average_space_between)
        trials_list1.append(number_of_chickens2)
        trials_list1.append(ratio)
        
        trials_matrix.append(trials_list1)
        
        for j in range (n-1):
            circle_radius2 += 0.3
            number_of_chickens = 1
            number_of_chickens2 = 1
        
            trials_list2 = []
            
            trials_list2.append(circle_radius)
            trials_list2.append(size_of_chicken)
            trials_list2.append(average_space_between)
            trials_list2.append(number_of_chickens)
            trials_list2.append(circle_radius2)
            trials_list2.append(size_of_chicken)
            trials_list2.append(average_space_between)
            trials_list2.append(number_of_chickens2)
            trials_list2.append(ratio)
            
            trials_matrix.append(trials_list2)
            
            for k in range(n):
                number_of_chickens += 2
                number_of_chickens2 = 1
        
                trials_list3 = []
                
                trials_list3.append(circle_radius)
                trials_list3.append(size_of_chicken)
                trials_list3.append(average_space_between)
                trials_list3.append(number_of_chickens)
                trials_list3.append(circle_radius2)
                trials_list3.append(size_of_chicken)
                trials_list3.append(average_space_between)
                trials_list3.append(number_of_chickens2)
                trials_list3.append(ratio)
                
                trials_matrix.append(trials_list3)
                
                for l in range(n):
                    number_of_chickens2 += 2
            
                    trials_list4 = []
                    
                    trials_list4.append(circle_radius)
                    trials_list4.append(size_of_chicken)
                    trials_list4.append(average_space_between)
                    trials_list4.append(number_of_chickens)
                    trials_list4.append(circle_radius2)
                    trials_list4.append(size_of_chicken)
                    trials_list4.append(average_space_between)
                    trials_list4.append(number_of_chickens2)
                    trials_list4.append(ratio)
                    
                    trials_matrix.append(trials_list4)
                    
    return (trials_matrix)

def matrix_size_chickens():
    trials_matrix = []
    size_of_chicken = -0.1 #round (random.uniform(0.5,2), 1)
    
    for i in range (n):
        circle_radius = 0.1
        average_space_between = 1.5 
        size_of_chicken += 0.3
        size_of_chicken2 = 0.1
        number_of_chickens = 2 #(random.randint(8, 15)) 
        number_of_chickens2 = 2
    
        trials_list1 = []
        
        trials_list1.append(circle_radius)
        trials_list1.append(size_of_chicken)
        trials_list1.append(average_space_between)
        trials_list1.append(number_of_chickens)
        trials_list1.append(circle_radius)
        trials_list1.append(size_of_chicken2)
        trials_list1.append(average_space_between)
        trials_list1.append(number_of_chickens2)
        trials_list1.append(ratio)
     
        trials_matrix.append(trials_list1)
        
        for j in range (n-1):
            size_of_chicken2 += 0.3
            number_of_chickens = 2
            number_of_chickens2 = 2
        
            trials_list2 = []
            
            trials_list2.append(circle_radius)
            trials_list2.append(size_of_chicken)
            trials_list2.append(average_space_between)
            trials_list2.append(number_of_chickens)
            trials_list2.append(circle_radius)
            trials_list2.append(size_of_chicken2)
            trials_list2.append(average_space_between)
            trials_list2.append(number_of_chickens2)
            trials_list2.append(ratio)
         
            trials_matrix.append(trials_list2)
            
            for k in range(n):
                number_of_chickens += 3
                number_of_chickens2 = 2
        
                trials_list3 = []
                
                trials_list3.append(circle_radius)
                trials_list3.append(size_of_chicken)
                trials_list3.append(average_space_between)
                trials_list3.append(number_of_chickens)
                trials_list3.append(circle_radius)
                trials_list3.append(size_of_chicken2)
                trials_list3.append(average_space_between)
                trials_list3.append(number_of_chickens2)
                trials_list3.append(ratio)
                
                trials_matrix.append(trials_list3)
                
                for l in range(n):
                    number_of_chickens2 += 3
            
                    trials_list4 = []
                    
                    trials_list4.append(circle_radius)
                    trials_list4.append(size_of_chicken)
                    trials_list4.append(average_space_between)
                    trials_list4.append(number_of_chickens)
                    trials_list4.append(circle_radius)
                    trials_list4.append(size_of_chicken2)
                    trials_list4.append(average_space_between)
                    trials_list4.append(number_of_chickens2)
                    trials_list4.append(ratio)
                    
                    trials_matrix.append(trials_list4)
    return (trials_matrix)

def matrix_space_between():
    trials_matrix = []
    average_space_between = -0.3 #round (random.uniform(1,2), 1)
    
    # number_of_chickens = 2, poi crescita a +3 (stabile)
    
    for i in range (n):
        circle_radius = 0.1
        size_of_chicken = 0.5
        average_space_between += 0.5
        average_space_between2 = 0.2
        number_of_chickens = 2 #(random.randint(8, 15)) 
        number_of_chickens2 = 2
    
        trials_list1 = []
        
        trials_list1.append(circle_radius)
        trials_list1.append(size_of_chicken)
        trials_list1.append(average_space_between)
        trials_list1.append(number_of_chickens)
        trials_list1.append(circle_radius)
        trials_list1.append(size_of_chicken)
        trials_list1.append(average_space_between2)
        trials_list1.append(number_of_chickens2)
        trials_list1.append(ratio)
     
        trials_matrix.append(trials_list1)
        
        for j in range (n-1):
            average_space_between2 += 0.3
            number_of_chickens = 2
            number_of_chickens2 = 2
            
            trials_list2 = []
            
            trials_list2.append(circle_radius)
            trials_list2.append(size_of_chicken)
            trials_list2.append(average_space_between)
            trials_list2.append(number_of_chickens)
            trials_list2.append(circle_radius)
            trials_list2.append(size_of_chicken)
            trials_list2.append(average_space_between2)
            trials_list2.append(number_of_chickens2)
            trials_list2.append(ratio)
         
            trials_matrix.append(trials_list2)
            
            for k in range(n):
                number_of_chickens += 3
                number_of_chickens2 = 2
        
                trials_list3 = []
                
                trials_list3.append(circle_radius)
                trials_list3.append(size_of_chicken)
                trials_list3.append(average_space_between)
                trials_list3.append(number_of_chickens)
                trials_list3.append(circle_radius)
                trials_list3.append(size_of_chicken)
                trials_list3.append(average_space_between2)
                trials_list3.append(number_of_chickens2)
                trials_list3.append(ratio)
                
                trials_matrix.append(trials_list3)
                
                for l in range(n):
                    number_of_chickens2 += 3
            
                    trials_list4 = []
                    
                    trials_list4.append(circle_radius)
                    trials_list4.append(size_of_chicken)
                    trials_list4.append(average_space_between)
                    trials_list4.append(number_of_chickens)
                    trials_list4.append(circle_radius)
                    trials_list4.append(size_of_chicken)
                    trials_list4.append(average_space_between2)
                    trials_list4.append(number_of_chickens2)
                    trials_list4.append(ratio)
                    
                    trials_matrix.append(trials_list4)
    return (trials_matrix)
    
def matrix_on_indicator(indicator):
    if indicator == 1:
        return matrix_circle_radius()
    elif indicator == 2:
        return matrix_size_chickens()
    else: 
        return matrix_space_between()