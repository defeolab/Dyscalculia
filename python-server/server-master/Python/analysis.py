import matplotlib.pyplot as plt
from db.db_connector import DBConnector
import math


db = DBConnector()

results = db.get_results(1)
print(results)

n = []
d = []
c = []
my_colors = {0:'red',1:'green'}
for result in results:
    n.append(math.log(result.trial_data.area2Data.numberOfChickens/result.trial_data.area1Data.numberOfChickens))
    d.append(math.log(result.trial_data.area2Data.sizeOfChicken/result.trial_data.area1Data.sizeOfChicken))
    c.append(result.correct)
print (n)   
print (d) 
# Plot various projections of the samples.
for i in range (len(n)):
   plt.scatter(n[i] , d[i], color = my_colors.get(c[i]))   
          
plt.ylabel('log(d2/d1)')
plt.xlabel('log(n2/n1)')
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.grid(True)
       
ax = plt.gca()
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')


plt.show()