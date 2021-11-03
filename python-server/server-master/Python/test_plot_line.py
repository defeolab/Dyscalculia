# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 14:36:27 2021

@author: Client
"""

import matplotlib.pyplot as plt
import numpy as np
import math

fig = plt.figure()
alpha = 45
alpha = alpha + 90
rad_alpha = np.deg2rad(alpha)
coeff = math.tan(rad_alpha)
ax = fig.add_subplot(1, 1, 1)
x = np.linspace(-5,5,100)

#  y = f(x) = a*x + b
# point P with coordinates (xp,yp)
# yp - ( a * xp + b ) < 0

xp = -0.5
yp = 0.3

if(yp - (coeff * xp) == 0):
    plt.scatter(xp, yp, color = 'blue')
elif((yp - (coeff * xp) > 0) and ((yp > 0) and (xp < 0)) or ((yp < 0) and (xp > 0))):
    plt.scatter(xp, yp, color = 'red')
else:
    plt.scatter(xp, yp, color = 'green')


ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

plt.plot(x, coeff*x, '-r', label='y=2x+1')
plt.legend(loc='upper left')

plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.grid(True)

plt.show()