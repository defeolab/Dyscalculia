from pandas import read_csv
import math
from typing import List, Any
from AI.ai_utils import to_mock_trial

class TrialAdapter:
    """
        This class is used by the PAD_Evaluator to translate a point in the nd-nnd space (chosen by the evaluator) into
        an actual trial among the ones usable from the client
    
    """


    def __init__(self, mock: bool, use_table: bool = True, norm_feats: bool = True, kids_ds: bool = False, memory: int = 30):
        self.mock = mock
        self.use_table = use_table
        self.norm_feats = norm_feats
        self.recent_ids = [1]
        self.memory = memory

        if kids_ds:
            print(f">>>>>>>using kids_ds")
            self.lookup_table = read_csv("./dataset/lookup_table_kids.csv")
        else:
            self.lookup_table = read_csv("./dataset/lookup_table.csv")

        if norm_feats:
            #normalize the lookup table
            max_nd = self.lookup_table['nd_LogRatio'].abs().max()
            max_nnd = self.lookup_table['nnd_LogRatio'].abs().max()

            self.lookup_table['nd_LogRatio'] = self.lookup_table['nd_LogRatio']/max_nd
            self.lookup_table['nnd_LogRatio'] = self.lookup_table['nnd_LogRatio']/max_nnd

    def find_trial(self, target_nd_coord: float, target_nnd_coord: float) -> List[Any]:
        
        self.lookup_table["DistanceFromTarget"] = (((self.lookup_table["nd_LogRatio"])-target_nd_coord)**2) + (((self.lookup_table["nnd_LogRatio"])-target_nnd_coord)**2)

        okay = False
        i = 0
        while okay == False:
            r = self.lookup_table.sort_values(by=['DistanceFromTarget']).iloc[i]
            id = int(r[0])
            i+=1
            if id not in self.recent_ids[-self.memory:] and id +1 not in self.recent_ids[-self.memory:] and id-1 not in self.recent_ids[-self.memory:]:
                okay = True  
        print(int(r[0]))
        #print(f"{target_nd_coord} - {closest_trial['nd_LogRatio']} : {target_nnd_coord} - {closest_trial['nnd_LogRatio']}")

        if self.mock == False:
            self.recent_ids.append(int(r[0]))
        matrix = []
        matrix.append([float(r["NumLeft"]), float(r["NumRight"]), float(r["FieldAreaLeft"]), float(r["FieldAreaRight"]), float(r["ItemSurfaceAreaLeft"]), float(r["ItemSurfaceAreaRight"]),4,8,float(r["nd_LogRatio"]), float(r["nnd_LogRatio"])])
        
        #print(matrix)
        return matrix if self.mock==False else [to_mock_trial(target_nd_coord, target_nnd_coord)]



if __name__ == "__main__":
    t = TrialAdapter(False)

    t.find_trial(0.5, 0.5)