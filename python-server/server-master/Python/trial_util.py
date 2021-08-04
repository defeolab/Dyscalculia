import numpy as np
import random
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