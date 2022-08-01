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
left_nnv = "FALeft" if select_nnv == 0 else "ISALeft"
right_nnv = "FARight" if select_nnv == 0 else "ISARight"

for index, trial in trial_list.iterrows():
    ratio_lr_nn.append(trial[right_nnv]/trial[left_nnv])
    logratio_nn.append(math.log(ratio_lr_nn[index]))
    ratio_lr_nv.append(trial["NumRight"]/trial["NumLeft"])
    logratio_nv.append(math.log(ratio_lr_nv[index]))

maxabslognn = max(logratio_nn, key=abs)
maxabslognv = max(logratio_nv, key=abs)
print("\nMAX ABS LOG nonnum:\t {}".format(maxabslognn))
print("MAX ABS LOG num:\t {}\n".format(maxabslognv))

for index, log_ratio in enumerate(logratio_nn):
    y_list.append(log_ratio/maxabslognn)

for index, log_ratio in enumerate(logratio_nv):
    try:
        x_list.append(log_ratio/maxabslognv)
    except:
        pass
    coeff_filtering.append(diff_coef(index, x_list[index], y_list[index]))

trial_list["Ratio L/R"] = ratio_lr_nv
trial_list["LogRatio"] = logratio_nv
trial_list["RatioNN"] = ratio_lr_nn
trial_list["LogRatioNN"] = logratio_nn
trial_list["X"] = x_list
trial_list["Y"] = y_list
trial_list["Coeff_F"] = coeff_filtering

trial_list =trial_list.drop(['Log - Norm', 'Coeff_S'], axis=1)
trial_list.to_excel("python-server/server-master/Python/dataset/diff_coefficients_filtering_coeff.xlsx")