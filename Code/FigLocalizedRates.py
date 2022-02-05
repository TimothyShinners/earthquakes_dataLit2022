# Plotting setup
import matplotlib.pyplot as plt

# Package imports
import numpy as np
import pandas as pd
import geopandas
import math
import datetime
import mpl_toolkits


#this file plots the localized estimated rate of earthquakes per year for each 
#date for each region. Be sure to run DataCleaning.py first!




center_date = datetime.date(2000, 1, 1)

step = datetime.timedelta(days = 1)

window_radius = 365

localizedRates = pd.DataFrame()

dates = []


for i in range(len(list_of_datasets)):
    center_date = datetime.date(2000, 1, 1) + datetime.timedelta(days = window_radius)
    rates = [] #rates are earthquakes per year
    
    while center_date < datetime.date(2021, 1, 1)-datetime.timedelta(days = window_radius):
        
        dates += [center_date]

        rates += [365 * count_quakes_in_interval(center_date,
                                           window_radius,
                                           list_of_datasets[i]["DATE"]) / (2*window_radius)]


        center_date = center_date + step
    
    if i == 0:
        localizedRates["DATES"] = dates
    
    region = str(list_of_datasets[i]["REGION_CODE"][0])
    
    localizedRates[region] = rates

fig, axs = plt.subplots(3,4)

for i in range(len(list_of_datasets)):
    axs[i//4, i%4].plot(localizedRates["DATES"], localizedRates.iloc[:,i+1], color = "black")
    if i%4 == 0:
        axs[i//4, i%4].set_ylabel('Earthquakes Per Year')
    
    if i >= 7:
        axs[i//4, i%4].set_xlabel('Date')
        axs[i//4, i%4].xaxis.set_major_locator(plt.MaxNLocator(3))
    else:
        axs[i//4, i%4].axes.get_xaxis().set_visible(False)
    
    axs[i//4, i%4].set_title(list_of_datasets[i]["REGION_NAME"][0])
    
    if i == 0:
        axs[i//4, i%4].set_title("Africa")
    if i == 3:
        axs[i//4, i%4].set_title("Southeast Asia")
    if i == 5:
        axs[i//4, i%4].set_title("Western Europe")
    if i == 2:
        axs[i//4, i%4].set_title("Central Asia")
    if i == 8:
        axs[i//4, i%4].set_title("North America/Hawaii")
    
    
fig.set_size_inches(18.5/1.5, 10.5/1.5)
fig.delaxes(axs[2][3])

plt.savefig('localizedRates.pdf', bbox_inches='tight')