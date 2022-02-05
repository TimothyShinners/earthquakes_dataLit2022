# Plotting setup
import matplotlib.pyplot as plt

# Package imports
import numpy as np
import pandas as pd
import geopandas
import math
import datetime
import mpl_toolkits


#this file plots the map of the earthquakes that were used in our analysis
#Be sure to run DataCleaning.py first!











groups = new_quakes.groupby('REGION_NAME')
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

# Plot
fig, ax = plt.subplots()
ax.margins(0.05) # Optional, just adds 5% padding to the autoscaling

for name, group in groups:
    ax.plot(group.LONGITUDE, group.LATITUDE, marker='o', linestyle='', ms=2, label=name)
ax.legend(loc = "right", bbox_to_anchor = (1.63, 0.5))

world.plot(ax=ax, color='black', edgecolor='black')

plt.savefig('new_quakes_world_map.pdf', bbox_inches='tight')  
plt.show()