# Plotting setup
import matplotlib.pyplot as plt

# Package imports
import numpy as np
import pandas as pd
import geopandas
import math
import datetime
import mpl_toolkits


#this file plots exponential QQ-plots of the waiting times for each region
#this one sadly didn't fit into the paper
#Be sure to run DataCleaning.py first!


fig, axsQQ = plt.subplots(3,4)

def getQuantileExp(p, rate):
    return -1*math.log(1-p)/rate

for i in range(len(list_of_datasets)):
    
    rate = 1 / list_of_datasets[i]["WAITING_TIME"].mean()
    n = list_of_datasets[i]["WAITING_TIME"].count()-1 #subtract 1 since first obs is zero
    
    list_of_datasets[i] = list_of_datasets[i].sort_values("WAITING_TIME")
    
    Q_theory = [0]
    Q_exp = [0]
    
    for j in range(n):
        Q_exp += [list_of_datasets[i]["WAITING_TIME"][j+1]]
        #print((j+1)/n, rate)
        Q_theory += [getQuantileExp((j)/n, rate)]
        
    list_of_datasets[i]["Q_THEORY"] = Q_theory
    list_of_datasets[i]["Q_EXP"] = Q_exp
    
    
    axsQQ[i//4, i%4].scatter(list_of_datasets[i]["WAITING_TIME"],
                           list_of_datasets[i]["Q_THEORY"], color = "black")
    axsQQ[i//4, i%4].plot(list_of_datasets[i]["WAITING_TIME"],
                         list_of_datasets[i]["WAITING_TIME"], color = "red")
    
    axsQQ[i//4, i%4].axes.get_xaxis().set_visible(False)
    axsQQ[i//4, i%4].axes.get_yaxis().set_visible(False)
    
    axsQQ[i//4, i%4].set_title(list_of_datasets[i]["REGION_NAME"][0])
    
    if i == 0:
        axsQQ[i//4, i%4].set_title("Africa")
    if i == 3:
        axsQQ[i//4, i%4].set_title("Southeast Asia")
    if i == 5:
        axsQQ[i//4, i%4].set_title("Western Europe")
    if i == 2:
        axsQQ[i//4, i%4].set_title("Central Asia")
    if i == 8:
        axsQQ[i//4, i%4].set_title("North America/Hawaii")


fig.set_size_inches(18.5/2, 10.5/2)
fig.delaxes(axsQQ[2][3])
plt.savefig('exp_QQ_plots.pdf', bbox_inches='tight')