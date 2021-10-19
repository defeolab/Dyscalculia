# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 11:24:08 2021

@author: Client
"""

### CODE which was previously used to plot a Gaussian pdf curve

# max_pdf = stats.norm.pdf(mu, mu, sigma)
# sample_pdf_vals = stats.norm.pdf(a[i], mu, sigma) / max_pdf

# under_curve = d[i] < sample_pdf_vals

# x = np.linspace(-1, 1, 1000)
# pdf_vals = stats.norm.pdf(x, mu, sigma) / max_pdf

# color = ('red' if under_curve else 'green')

# plt.scatter(a[i], d[i], c = color)  
# plt.plot(x, pdf_vals)


#########################################################################

# mean_nv = np.mean(nv)
# std_nv = np.std(nv)
# mean_nnv = np.mean(nnv)
# std_nnv = np.std(nnv)

# # Valori per circle radius

# print(mean_nv)  # 5.684 e-18
# print(std_nv)   # 0.478
# print(mean_nnv) # 0
# print(std_nnv)  # 0.422

# y = stats.norm(mean_nv, std_nv).pdf(1)
# print(y) 

# for i in range(len(nv)):
#     x = stats.norm(0, 0.2).pdf(nv[i]);
#     if(x < 0.5):
#         plt.scatter(nv[i], nnv[i], color='green')
#     else:
#         plt.scatter(nv[i], nnv[i], color='red')