import random
import json
import numpy as np
from area_data import AreaData


class Trial:

    def __init__(self, area_1_data=None, area_2_data=None, circle_radius=None
                 , size_of_chicken=None, average_space_between=None, ratio=None
                 , chicken_show_time=None, max_trial_time=None, number_of_chickens=None
                 , ratio_area=None):
        
        if area_1_data is None or area_2_data is None:
            if ratio_area == None:
                ratio_area = random.choice([0, 1])
            if ratio_area == 0:
                area_2_chickens = int(number_of_chickens * ratio)
                if area_2_chickens == number_of_chickens:
                    if ratio > 1.0:
                        area_2_chickens += 1
                    else:
                        number_of_chickens += 1
                self.area1Data = AreaData(circle_radius, size_of_chicken, average_space_between, number_of_chickens)
                self.area2Data = AreaData(circle_radius * ratio, size_of_chicken * ratio, average_space_between * ratio, area_2_chickens)
                self.ratioArea = 1
            else:
                area_1_chickens = int(number_of_chickens * ratio)
                if area_1_chickens == number_of_chickens:
                    if ratio > 1.0:
                        number_of_chickens += 1
                    else:
                        area_1_chickens += 1
                self.area1Data = AreaData(circle_radius * ratio, size_of_chicken * ratio, average_space_between * ratio, area_1_chickens)
                self.area2Data = AreaData(circle_radius, size_of_chicken, average_space_between, number_of_chickens)
                self.ratioArea = 0
        else:
            self.area1Data = area_1_data
            self.area2Data = area_2_data
            self.ratioArea = ratio_area
        self.ratio = ratio
        self.chickenShowTime = chicken_show_time
        self.maxTrialTime = max_trial_time

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_array(self):
        active_data = self.area1Data if self.ratioArea == 1 else self.area2Data
        return np.array([self.ratio, active_data.averageSpaceBetween, active_data.sizeOfChicken, active_data.circleRadius
                        , self.chickenShowTime, self.maxTrialTime, self.ratioArea])
