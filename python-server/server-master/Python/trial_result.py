# 'TRIAL RESULT' class
# This class is used to analyze and manipulate data receveid back from the Client,
# particularly to manipulate and see the response given by the player, so that it 
# is possible to obtain a response vector made of 1 (in case of correct answers)
# and 0 (in case of incorrect answers)

from trial import Trial
from area_data import AreaData

class TrialResult:

    def __init__(self, difficulty, decision_time, correct, raw_trial_data = None, trial_data = None):
        self.decision_time = decision_time
        self.correct = correct
        self.difficulty = difficulty
        if raw_trial_data != None:
            #print(raw_trial_data)
            raw_data = raw_trial_data["area1Data"]
            area_1_data = AreaData(raw_data["circleRadius"], raw_data["sizeOfChicken"], raw_data["averageSpaceBetween"], raw_data["numberOfChickens"])
            raw_data = raw_trial_data["area2Data"]
            area_2_data = AreaData(raw_data["circleRadius"], raw_data["sizeOfChicken"], raw_data["averageSpaceBetween"], raw_data["numberOfChickens"])
            
            self.trial_data = Trial(area_1_data = area_1_data, area_2_data = area_2_data
                                        , chicken_show_time=raw_trial_data["chickenShowTime"]
                                        , max_trial_time=raw_trial_data["maxTrialTime"])
            
        else:
            self.trial_data = trial_data

    def get_answer(self):
        # probably not needed, at least not until the communication between the client and the server is really working
        # answer = np.random.randint(2)
        return 1 if self.correct else 0
        #return answer
