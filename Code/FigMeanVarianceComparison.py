# Plotting setup
import matplotlib.pyplot as plt

# Package imports
import numpy as np
import pandas as pd
import geopandas
import math
import datetime
import mpl_toolkits


#this file plots the mean earthquakes per year vs the variance o
#f earthquakes per year for each region, as seen in our paper
#Be sure to run DataCleaning.py first!

mean_quakes_per_year = []
var_quakes_per_year = []
fig, ax = plt.subplots(1,1)

for i in range(len(list_of_datasets)):
    mean_quakes_per_year += [quakes_per_year.iloc[:,i+1].mean()]
    var_quakes_per_year += [quakes_per_year.iloc[:,i+1].var()]
    
ax.scatter(mean_quakes_per_year, var_quakes_per_year, color = "black")
ax.plot([0,20],[0,20], color = "red")
ax.set_ylabel('Variance')
ax.set_xlabel('Mean')

plt.savefig('mean_v_var.pdf', bbox_inches='tight')