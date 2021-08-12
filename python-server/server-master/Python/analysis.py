import math
import matplotlib.pyplot as plt
from db.db_connector import DBConnector
from trial_util import generate_dummy_random_trial_matrix
#from dummy_client_handler import DummyClientHandler 


db = DBConnector()
flag = 0 # 1 means REAL, 0 means DUMMY
trials_matrix = generate_dummy_random_trial_matrix();
# thread = DummyClientHandler()
# trials_matrix = thread.Analysis()

results = db.get_results(1)
#print(results)

n = []
d = []
c = []

my_colors = {0:'red',1:'green'}

if flag == 1:
    for result in results:
        n.append(math.log(result.trial_data.area2Data.numberOfChickens/result.trial_data.area1Data.numberOfChickens))
        d.append(math.log(result.trial_data.area2Data.sizeOfChicken/result.trial_data.area1Data.sizeOfChicken))
        #d.append(math.log(result.trial_data.area2Data.averageSpaceBetween/result.trial_data.area1Data.averageSpaceBetween))
        #d.append(math.log(result.trial_data.area2Data.circleRadius/result.trial_data.area1Data.circleRadius))
        c.append(result.correct)
else:
    for results in trials_matrix:
        n.append(math.log(results[7]/results[3]))
        d.append(math.log(results[5]/results[1]))
        c.append(results[9])

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