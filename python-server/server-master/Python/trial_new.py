# New 'TRIAL' class
# It must take as argument every single parameter of the game and set the trial consequently

import json
import numpy as np 
from area_data import AreaData

class Trial_New:
    def __init__(self, area_1_data=None, area_2_data=None, area_1_circle_radius=None, 
                 area_2_circle_radius=None, area_1_size_of_chicken=None, 
                 area_2_size_of_chicken=None, area_1_average_space_between=None, 
                 area_2_average_space_between=None, area_1_number_of_chickens=None, 
                 area_2_number_of_chickens=None, 
                 chicken_show_time=None, max_trial_time=None):
        
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
    
    def to_array(self):
        ratioArea = self.area1Data.circleRadius / self.area2Data.circleRadius()
        active_data = self.area1Data if ratioArea == 1 else self.area2Data
        return np.array([self.ratio, active_data.averageSpaceBetween, active_data.sizeOfChicken, 
              active_data.circleRadius, self.chickenShowTime, self.maxTrialTime, self.ratioArea])

    # def to_array(self):
    #     active_data = self.area1Data if self.ratioArea == 1 else self.area2Data
    #     return np.array([self.ratio, active_data.averageSpaceBetween, active_data.sizeOfChicken, 
    #           active_data.circleRadius, self.chickenShowTime, self.maxTrialTime, self.ratioArea])
        
# Perchè questa funzione? A che mi serve? Perchè Fletcher restituiva SOLO l'active data?
# DA VEDERE COSA LA FUNZIONE PASSA A UNITY (vedere client_handler.py)
               