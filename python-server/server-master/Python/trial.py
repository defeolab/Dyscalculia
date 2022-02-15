# 'TRIAL' class
# It must take as argument every parameter needed to create a trial

import json
# import numpy as np 
from area_data import AreaData

class Trial:
    def __init__(self, area_1_data = None, area_2_data = None, area_1_number_of_chickens = None, 
                 area_2_number_of_chickens = None, area_1_field_area = None, area_2_field_area = None,
                 area_1_item_surface_area = None, area_2_item_surface_area = None,
                 chicken_show_time = None, max_trial_time = None):
        
        if area_1_data is None or area_2_data is None:
            self.area1Data = AreaData(area_1_number_of_chickens, area_1_field_area, area_1_item_surface_area)
            self.area2Data = AreaData(area_2_number_of_chickens, area_2_field_area, area_2_item_surface_area)
        else:
            self.area1Data = area_1_data
            self.area2Data = area_2_data
            
        self.chickenShowTime = chicken_show_time
        self.maxTrialTime = max_trial_time
                
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    # def to_array(self):
    #     ratioArea = self.area1Data.circleRadius / self.area2Data.circleRadius()
    #     active_data = self.area1Data if ratioArea == 1 else self.area2Data
    #     return np.array([self.ratio, active_data.averageSpaceBetween, active_data.sizeOfChicken, 
    #           active_data.circleRadius, self.chickenShowTime, self.maxTrialTime, self.ratioArea])