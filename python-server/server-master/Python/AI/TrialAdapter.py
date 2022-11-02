from pandas import read_csv
import math
from typing import List, Any

class TrialAdapter:
    """
        This class is used by the PAD_Evaluator to translate a point in the nd-nnd space (chosen by the evaluator) into
        an actual trial among the ones usable from the client
    
    """


    def __init__(self, mock: bool, use_table: bool = True):
        self.mock = mock
        self.lookup_table = read_csv("./dataset/lookup_table.csv")
        self.use_table = use_table

    def find_trial(self, target_nd_coord: float, target_nnd_coord: float) -> List[Any]:
        
        self.lookup_table["DistanceFromTarget"] = (((self.lookup_table["nd_LogRatio"])-target_nd_coord)**2) + (((self.lookup_table["nnd_LogRatio"])-target_nnd_coord)**2)

        closest_trial = self.lookup_table.sort_values(by=['DistanceFromTarget']).iloc[0]

        #print(f"{target_nd_coord} - {closest_trial['nd_LogRatio']} : {target_nnd_coord} - {closest_trial['nnd_LogRatio']}")

        return closest_trial



if __name__ == "__main__":
    t = TrialAdapter(False)

    t.find_trial(0.5, 0.5)