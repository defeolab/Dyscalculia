# 'TRIAL' class
# It must take as argument every parameter needed to create a trial
# The Trial must be created in a way that is Unity-compatible, meaning that the
# passed parameter are the ones that are useful for the Unity client (circle radius, 
# size of chickens and average space between, alongside the number of course)

import json
from area_data import AreaData

class Trial:
    def __init__(self, area_1_data = None, area_2_data = None, 
                 area_1_circle_radius = None, area_2_circle_radius = None,
                 area_1_size_of_chicken = None, area_2_size_of_chicken = None,
                 area_1_average_space_between = None, area_2_average_space_between = None,
                 area_1_number_of_chickens = None, area_2_number_of_chickens = None,
                 chicken_show_time = None, max_trial_time = None   ):
        
        if area_1_data is None or area_2_data is None:
            self.area1Data = AreaData(area_1_circle_radius, area_1_size_of_chicken, area_1_average_space_between, area_1_number_of_chickens)
            self.area2Data = AreaData(area_2_circle_radius, area_2_size_of_chicken, area_2_average_space_between, area_2_number_of_chickens)
        else:
            self.area1Data = area_1_data
            self.area2Data = area_2_data
            
        self.chickenShowTime = chicken_show_time
        self.maxTrialTime = max_trial_time
                
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)