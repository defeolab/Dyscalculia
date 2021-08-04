import numpy as np
from trial import Trial
import math
import random

mu = np.array([0, 0])


def generate_correlated_trials(number_of_trials, next_correlation, settings):

    r = np.array([
        [next_correlation, -0.1],
        [-0.1, next_correlation],
    ])

    min_trial_data = [settings.ratio_min, settings.average_space_between_min, settings.size_of_chicken_min, settings.total_area_occupied_min]
    max_trial_data = [settings.ratio_max, settings.average_space_between_max, settings.size_of_chicken_max, settings.total_area_occupied_max]

    data = np.random.multivariate_normal(mu, r, size=number_of_trials)
    while np.isnan(data[0][0]):
        data = np.random.multivariate_normal(mu, r, size=number_of_trials)

    trials = list()
    index = 0
    max_data_value = max(map(max, data))
    min_data_value = min(map(min, data))
    for raw_trial in data:
        raw_trial_data = list()
        for i in range(0, 4):
            new_min = min_trial_data[i]
            new_max = max_trial_data[i]
            value = raw_trial[index]
            new_value = (new_max-new_min)/(max_data_value-min_data_value)*(value-max_data_value)+new_max
            raw_trial_data.append(new_value)
            index = 1 if index == 0 else 0

        ratio = raw_trial_data[0]
        average_space_between = raw_trial_data[1]
        size_of_chicken = raw_trial_data[2]
        total_area_occupied = raw_trial_data[3]
        circle_radius = math.sqrt(total_area_occupied / math.pi)
        chicken_show_time = random.uniform(settings.chicken_show_time_min, settings.chicken_show_time_max)
        max_trial_time = random.uniform(settings.max_trial_time_min, settings.max_trial_time_max)
        number_of_chickens = random.randint(2, 8)
        trials.append(Trial(None, None, circle_radius, size_of_chicken, average_space_between, ratio, chicken_show_time, max_trial_time, number_of_chickens))
    return trials
