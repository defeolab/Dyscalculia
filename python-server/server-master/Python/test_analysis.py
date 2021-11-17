# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:00:57 2021

@author: Client
"""

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# generate sample points
num_pts = 500
sample_xs = np.random.uniform(-1, 1, size=num_pts)
sample_ys = np.random.uniform(-1, 1, size=num_pts)

# define distribution
mean = 0
sigma = 0.45

# figure out "normalized" pdf vals at sample points
max_pdf = stats.norm.pdf(mean, mean, sigma)
sample_pdf_vals = stats.norm.pdf(sample_xs, mean, sigma) / max_pdf

# which ones are under the curve?
under_curve = sample_ys < sample_pdf_vals

# get pdf vals to plot
x = np.linspace(-1, 1, 1000)
pdf_vals = stats.norm.pdf(x, mean, sigma) / max_pdf

# plot the samples and the curve
colors = np.array(['cyan' if b else 'red' for b in under_curve])
plt.scatter(sample_xs, sample_ys, c=colors)
plt.plot(x, pdf_vals)