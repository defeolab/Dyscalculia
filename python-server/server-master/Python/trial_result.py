from trial import Trial
from area_data import AreaData
# import numpy as np

class TrialResult:

    def __init__(self, decision_time, correct, raw_trial_data = None, trial_data = None):
        self.decision_time = decision_time
        self.correct = correct
        if raw_trial_data != None:
            print(raw_trial_data)
            raw_data = raw_trial_data["area1Data"]
            area_1_data = AreaData(raw_data["numberOfChickens"], raw_data["fieldArea"], raw_data["itemSurfaceArea"])
            raw_data = raw_trial_data["area2Data"]
            area_2_data = AreaData(raw_data["numberOfChickens"], raw_data["fieldArea"], raw_data["itemSurfaceArea"])
            
            self.trial_data = Trial(area_1_data = area_1_data, area_2_data = area_2_data
                                        , chicken_show_time=raw_trial_data["chickenShowTime"]
                                        , max_trial_time=raw_trial_data["maxTrialTime"])
            
        else:
            self.trial_data = trial_data

    def get_answer(self):
        # probably not needed, at least not until the communication between the client and the server is really working
        #answer = np.random.randint(2)
        return 1 if self.correct else 0
        #return answer
