# Plotting setup
import matplotlib.pyplot as plt

# Package imports
import numpy as np
import pandas as pd
import geopandas
import math
import datetime
import mpl_toolkits



#This code plots a heat map of the matrix that contains our test 
#statistic for every ij pair of regions, as seen in our paper
#Be sure to run DataCleaning.py first!




for i in range(len(list_of_datasets)):
    for j in range(len(list_of_datasets)):
        current_region = list_of_datasets[i]
        waiting_times = []
        expected_waiting_times = []


        for k in range(len(current_region["DATE"])):
            #print(i, j, k, current_region["DATE"])
            starting_date = current_region["DATE"][k]
            
            if min(localizedRates["DATES"]) <= starting_date and max(localizedRates["DATES"]) >= starting_date:
                region = list_of_datasets[j]
                next_quake = find_next_quake(starting_date, region)
                if next_quake is not None:

                    waiting_times += [next_quake]
                    
                    rate = float(localizedRates[localizedRates["DATES"] == starting_date].iloc[:,j+1])
                    
                    if rate == 0:
                        rate += 0.0001

                    expected_waiting_times += [(365)/rate] #waiting time in days
        
        #print("waiting times", waiting_times)
        #print("exp waiting times", expected_waiting_times)
        #raise
        
        stat = []
        
        for k in range(len(waiting_times)):
            if waiting_times[k] == 0:
                waiting_times[k] += 0.0001
            stat += [(waiting_times[k] / expected_waiting_times[k])]
            
        mean_stat = sum(stat)/len(stat)
        
        rate_matrix[i][j] = mean_stat
        
for i in range(len(list_of_datasets)):
    rate_matrix[i][i] = math.nan




plt.imshow(rate_matrix, interpolation='nearest')
plt.colorbar() 
plt.axis("off")
plt.savefig('indicatorRatios.pdf', bbox_inches='tight')