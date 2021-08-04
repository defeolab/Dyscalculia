from trial import Trial
from area_data import AreaData
#import numpy as np

class TrialResult:

    def __init__(self, decision_time, correct, raw_trial_data=None, trial_data=None):
        self.decision_time = decision_time
        #self.decision_time = np.random.randint(10000)
        self.correct = correct
        if raw_trial_data != None:
            raw_data = raw_trial_data["area1Data"]
            area_1_data = AreaData(raw_data["circleRadius"], raw_data["sizeOfChicken"], raw_data["averageSpaceBetween"], raw_data["numberOfChickens"])
            raw_data = raw_trial_data["area2Data"]
            area_2_data = AreaData(raw_data["circleRadius"], raw_data["sizeOfChicken"], raw_data["averageSpaceBetween"], raw_data["numberOfChickens"])
            self.trial_data = Trial(area_1_data=area_1_data, area_2_data=area_2_data, ratio=raw_trial_data["ratio"], chicken_show_time=raw_trial_data["chickenShowTime"], max_trial_time=raw_trial_data["maxTrialTime"], ratio_area=raw_trial_data["ratioArea"])
        else:
            self.trial_data = trial_data

    def get_answer(self):
        #answer = np.random.randint(2)
        return 1 if self.correct else 0
        #return answer
