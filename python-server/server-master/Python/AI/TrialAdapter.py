from pandas import read_csv
import math
from typing import List, Any
from AI.ai_utils import to_mock_trial

class TrialAdapter:
    """
        This class is used by the PAD_Evaluator to translate a point in the nd-nnd space (chosen by the evaluator) into
        an actual trial among the ones usable from the client
    
    """


    def __init__(self, mock: bool, use_table: bool = True, norm_feats: bool = True):
        self.mock = mock
        self.lookup_table = read_csv("./dataset/lookup_table.csv")
        self.use_table = use_table
        self.norm_feats = norm_feats

        if norm_feats:
            #normalize the lookup table
            max_nd = self.lookup_table['nd_LogRatio'].abs().max()
            max_nnd = self.lookup_table['nnd_LogRatio'].abs().max()

            self.lookup_table['nd_LogRatio'] = self.lookup_table['nd_LogRatio']/max_nd
            self.lookup_table['nnd_LogRatio'] = self.lookup_table['nnd_LogRatio']/max_nnd

    def find_trial(self, target_nd_coord: float, target_nnd_coord: float) -> List[Any]:
        
        self.lookup_table["DistanceFromTarget"] = (((self.lookup_table["nd_LogRatio"])-target_nd_coord)**2) + (((self.lookup_table["nnd_LogRatio"])-target_nnd_coord)**2)

        r = self.lookup_table.sort_values(by=['DistanceFromTarget']).iloc[0]

        #print(f"{target_nd_coord} - {closest_trial['nd_LogRatio']} : {target_nnd_coord} - {closest_trial['nnd_LogRatio']}")

        matrix = []
        matrix.append([float(r["NumLeft"]), float(r["NumRight"]), float(r["FieldAreaLeft"]), float(r["FieldAreaRight"]), float(r["ItemSurfaceAreaLeft"]), float(r["ItemSurfaceAreaRight"]),4,8,float(r["nd_LogRatio"]), float(r["nnd_LogRatio"])])
        
        #print(matrix)
        return matrix if self.mock==False else [to_mock_trial(target_nd_coord, target_nnd_coord)]



if __name__ == "__main__":
    t = TrialAdapter(False)

    t.find_trial(0.5, 0.5)