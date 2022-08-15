import math

def diff_coef(i, x, y):
    try:
        if (x > 0 and y >= 0) or (x < 0 and y <= 0):
            k = math.atan(y/x)
        elif (x < 0 and y >= 0) or (x > 0 and y <= 0):
            k = math.pi - abs(math.atan(y/x))
        a = math.degrees(abs((math.pi/4)-k))
    except:
        return -1
    return a

######### CALCULATE FILTERING DIFFICULT COEFFICIENT #########
import pandas as pd
import numpy as np
import math

trial_list = pd.read_excel("/Users/Enterprise/Desktop/OneDrive/Essex/Dyscalculia/Dyscalculia/python-server/server-master/Python/dataset/diff_coefficients.xlsx")

ratio_lr_nv = []
logratio_nv = []
log_norm_nv = []
ratio_lr_nn = []
logratio_nn = []
coeff_filtering = []
x_list = []
y_list = []

# 0 - field area
# 1 - item surface area

select_nnv = 0
left_nnv = "FieldAreaLeft" if select_nnv == 0 else "ItemSurfaceAreaLeft"
right_nnv = "FieldAreaRight" if select_nnv == 0 else "ItemSurfaceAreaRight"

for index, trial in trial_list.iterrows():
    ratio_lr_nn.append(trial[right_nnv]/trial[left_nnv])
    logratio_nn.append(math.log(ratio_lr_nn[index]))
    ratio_lr_nv.append(trial["NumRight"]/trial["NumLeft"])
    logratio_nv.append(math.log(ratio_lr_nv[index]))

maxabslognn = max(logratio_nn, key=abs)
maxabslognv = max(logratio_nv, key=abs)
# print("\nMAX ABS LOG nonnum:\t {}".format(maxabslognn))
# print("MAX ABS LOG num:\t {}\n".format(maxabslognv))

for index, log_ratio in enumerate(logratio_nn):
    y_list.append(log_ratio/maxabslognn)

for index, log_ratio in enumerate(logratio_nv):
    try:
        x_list.append(log_ratio/maxabslognv)
    except:
        pass
    coeff_filtering.append(diff_coef(index, x_list[index], y_list[index]))

lookup_table = pd.read_csv("trial_lookup.csv")
lookup_table["Diff_coeff_filtering"] = coeff_filtering
# Negative values make reference to invalid cases.
lookup_table["Diff_coeff_filtering"] = lookup_table["Diff_coeff_filtering"] /lookup_table["Diff_coeff_filtering"].abs().max()

lookup_table.drop(["Unnamed: 10", "Unnamed: 11"], axis = 1, inplace=True)
lookup_table.to_csv("trial_lookup_filtering_coeff.csv")
