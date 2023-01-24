import numpy as np
import matplotlib.pyplot as plt
 
# creating the dataset
data = {'Drowned in 1768':2, "Drowned in 1769": 1, 'Frozen in 1769':2, "Died in 1769": 2, "Died in 1770": 5, "Died in 1771": 26}
causes = list(data.keys())
values = list(data.values())
  
fig = plt.figure(figsize = (10, 5))
 
# creating the bar plot
plt.bar(causes, values, color ='maroon',
        width = 0.4)
 
plt.xlabel("Cause of death")
plt.ylabel("No. of people who died")
plt.show()