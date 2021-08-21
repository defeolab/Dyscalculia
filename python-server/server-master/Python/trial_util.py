import numpy as np
import random
import math
from trial import Trial

def convert_trials_to_json(trials):
    message = "["
    for i in range(len(trials)):
        trial = trials[i]
        message += trial.to_json()
        if i != (len(trials) - 1):
            message += ","

    message += "]\n"
    return message


def convert_trials_to_matrix(results):
    first_trial = results[0].trial_data
    matrix = np.array([first_trial.to_array()])
    for i in range(1, len(results)):
        trial = results[i].trial_data
        matrix = np.append(matrix, [trial.to_array()], axis=0)
    return matrix

def convert_matrix_to_trials(matrix):
    trials = []
    for i in range(0, len(matrix)):
        trial = matrix[i]
        trials.append(create_trial_from_array(trial))
    return trials

def create_trial_from_array(array):
    number_of_chickens = random.randint(2, 8)
    return Trial(ratio=array[0], average_space_between=array[1], size_of_chicken=array[2], circle_radius=array[3], chicken_show_time=array[4], max_trial_time=array[5], ratio_area=array[6], number_of_chickens=number_of_chickens)

#create the random matrix for the real game 
def generate_random_trial_matrix():
    n = round(random.uniform(1, 10)) #gives a random length for the rows of the matrix
    trials_matrix = []
    for i in range (n):
        ratio = round (random.uniform(0,2), 1)
        average_space_between = round (random.uniform(1,2), 1)
        size_of_chicken = round (random.uniform(0.5,2), 1)
        circle_radius = round (random.uniform(1,2),1)
        chicken_show_time = round (random.uniform(2,5))
        max_trial_time = round (random.uniform(8,10))
        ratio_area = round (random.randint(0, 1))
        
        trials_list = []
        
        trials_list.append(ratio)
        trials_list.append(average_space_between)
        trials_list.append(size_of_chicken)
        trials_list.append(circle_radius)
        trials_list.append(chicken_show_time)
        trials_list.append(max_trial_time)
        trials_list.append(ratio_area)
         
        trials_matrix.append(trials_list)
    return trials_matrix

#create the matrix for the dummy game 
def generate_dummy_random_trial_matrix():
    n = round(random.uniform(1, 20)) #gives a random length for the rows of the matrix
    trials_matrix = []
    for i in range (n):
        ratio = round (random.uniform(1.1,2), 1)
        average_space_between = round (random.uniform(1,2), 1)
        size_of_chicken = (random.uniform(0.1,2))
        total_area_occupied = round (random.uniform(2,3))
        circle_radius = round (math.sqrt(total_area_occupied / math.pi), 1)
        number_of_chickens = random.randint(8, 15)
        number_of_chickens2 = round (int(number_of_chickens * ratio))
    
        trials_list1 = []
        
        trials_list1.append(circle_radius)
        trials_list1.append(size_of_chicken)
        trials_list1.append(average_space_between)
        
        trials_list2 = [i * ratio for i in trials_list1]
        trials_list1.append(number_of_chickens)
        trials_list1.extend(trials_list2)
        trials_list1.append(number_of_chickens2)
        trials_list1.append(ratio)
 
        trials_matrix.append(trials_list1)
    return trials_matrix