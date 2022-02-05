# Plotting setup
import matplotlib.pyplot as plt

# Package imports
import numpy as np
import pandas as pd
import geopandas
import math
import datetime
import mpl_toolkits
#from mpl_toolkits.basemap import Basemap



#in this file we import the data used in my earthquakes paper. Then we clean it and use it!
#and convert into other data frames that are used in our analysis





# Link to current data 
url = "https://www.kaggle.com/mohitkr05/global-significant-earthquake-database-from-2150bc"

# Read CSV data from the file I downloaded
earthquakes = pd.read_csv('EarthquakeData.csv')


#now we clean earthquakes

#we find rows that actually have a value
#for LONGITUDE
goodValues = []

for i in range(len(earthquakes["LONGITUDE"])):
    #print(i)
    if i != 305 and earthquakes["LATITUDE"][i] != '       ':
        if not math.isnan(float(earthquakes["LONGITUDE"][i])):
            goodValues += [i]

#select rows that have a real
#longitude coordinate
earthquakes = earthquakes.iloc[goodValues].reset_index()


earthquakes["LONGITUDE"] = earthquakes["LONGITUDE"].astype(float)
earthquakes["LATITUDE"] = earthquakes["LATITUDE"].astype(float)


#new quakes is what we use for most of the analysis
new_quakes = earthquakes.query("YEAR >= 2000")


#we filter out all regions that have less than 20 observations
by_region = new_quakes.groupby("REGION_CODE").mean()[["EQ_PRIMARY", "LATITUDE", "LONGITUDE"]]
by_region["COUNT"] = new_quakes.groupby("REGION_CODE").size()
by_region["RATE"] = by_region["COUNT"]/21
by_region = by_region.query("COUNT > 20").reset_index()
list_of_regions = by_region["REGION_CODE"].tolist()
new_quakes = new_quakes.assign(VALID_REGION = new_quakes["REGION_CODE"].isin(list_of_regions))
new_quakes = new_quakes.query("VALID_REGION == True").reset_index()




#only region codes were recorded in the data set, so now we need to make a 
#column with the region names. This part sucked.
region_names = []
for i in range(len(new_quakes["REGION_CODE"])):
    if new_quakes["REGION_CODE"][i] == 10:
        region_names += ["Central, Western and S. Africa"]
    if new_quakes["REGION_CODE"][i] == 15:
        region_names += ["Northern Africa"]
    if new_quakes["REGION_CODE"][i] == 20:
        region_names += ["Antarctica"]
    if new_quakes["REGION_CODE"][i] == 30:
        region_names += ["East Asia"]
    if new_quakes["REGION_CODE"][i] == 40:
        region_names += ["Central Asia and Caucasus"]
    if new_quakes["REGION_CODE"][i] == 50:
        region_names += ["Kamchatka and Kuril Islands"]
    if new_quakes["REGION_CODE"][i] == 60:
        region_names += ["S. and SE. Asia and Indian Ocean"]
    if new_quakes["REGION_CODE"][i] == 70:
        region_names += ["Atlantic Ocean"]
    if new_quakes["REGION_CODE"][i] == 80:
        region_names += ["Bering Sea"]
    if new_quakes["REGION_CODE"][i] == 90:
        region_names += ["Carribean"]
    if new_quakes["REGION_CODE"][i] == 100:
        region_names += ["Central America"]
    if new_quakes["REGION_CODE"][i] == 110:
        region_names += ["Eastern Europe"]
    if new_quakes["REGION_CODE"][i] == 120:
        region_names += ["Northern and Western Europe"]
    if new_quakes["REGION_CODE"][i] == 130:
        region_names += ["Southern Europe"]
    if new_quakes["REGION_CODE"][i] == 140:
        region_names += ["Middle East"]
    if new_quakes["REGION_CODE"][i] == 150:
        region_names += ["North America and Hawaii"]
    if new_quakes["REGION_CODE"][i] == 160:
        region_names += ["South America"]
    if new_quakes["REGION_CODE"][i] == 170:
        region_names += ["Central and South Pacific"]
        
new_quakes["REGION_NAME"] = region_names



#now we make a proper date column
new_quakes["DATE"] = new_quakes["YEAR"].apply(str)+"-"+new_quakes["MONTH"].apply(int).apply(str)+"-"+new_quakes["DAY"].apply(int).apply(str)
new_quakes["DATE"] = pd.to_datetime(new_quakes["DATE"])

new_quakes = new_quakes.sort_values("DATE")


#calculate the waiting times
waiting_times = [new_quakes["DATE"][0] - new_quakes["DATE"][0]]

for i in range(len(new_quakes['YEAR']) - 1):
    waiting_times += [new_quakes["DATE"][i+1] - new_quakes["DATE"][i]]
    
new_quakes = new_quakes.assign(WAITING_TIME = waiting_times)
new_quakes["WAITING_TIME"] = new_quakes["WAITING_TIME"].dt.days







#now we need a different data frame per region. We store these in a list
list_of_datasets = []

for region in list_of_regions:
    query = "REGION_CODE == "+str(region)
    list_of_datasets += [new_quakes.query(query).reset_index(drop=True)]


#need to define a function
def find_next_quake(starting_date, df):
    #starting date is a datetime
    #df is a pandas data frame with a DATE column of dates
    #and it must be sorted with oldest dates being first!
    for i in range(len(df["DATE"])):
        if starting_date <= df["DATE"][i]:
            wait_time = df["DATE"][i] - starting_date
            #print(wait_time, "bb", wait_time.days)
            return wait_time.days
        
    return None


#now we calculate region-specific waiting times
for i in range(len(list_of_datasets)):
    #for each region, we want a pandas column of waiting times
    #the waiting times indicate how long we waited for that row's quake
    waiting_times = [list_of_datasets[i]["DATE"][0] - list_of_datasets[i]["DATE"][0]]
    
    for j in range(len(list_of_datasets[i]['YEAR']) - 1):
        waiting_times += [list_of_datasets[i]["DATE"][j+1] - list_of_datasets[i]["DATE"][j]]
        
    list_of_datasets[i] = list_of_datasets[i].assign(WAITING_TIME = waiting_times)
    list_of_datasets[i]["WAITING_TIME"] = list_of_datasets[i]["WAITING_TIME"].dt.days



#now we are looking at quakes per year
regions = []
for i in range(len(list_of_datasets)):
    regions += [list_of_datasets[i]["REGION_CODE"][0]]

quakes_per_year = pd.DataFrame()
quakes_per_year["YEAR"] = range(2000, 2021)

for i in range(len(list_of_datasets)):
     
    count = []
    
    for j in range(2000, 2021):
        count += [list_of_datasets[i].query("YEAR == "+str(j)).shape[0]]
        
    quakes_per_year[str(list_of_datasets[i]["REGION_CODE"][0])] = count
    
fig, axs = plt.subplots(3,4)


for i in range(len(list_of_datasets)):
    
    list_of_datasets[i] = list_of_datasets[i].sort_values("DATE")
    
    window = int(len(list_of_datasets[i]["DATE"]) / 5)
    
    list_of_datasets[i]["WAIT_TIME_SMOOTH"] = list_of_datasets[i]["WAITING_TIME"].rolling(window).mean()
    
    list_of_datasets[i]["WAIT_TIME_SMOOTH_INVERSE"] = list_of_datasets[i]["WAIT_TIME_SMOOTH"] ** (-1)
    




#now we are trying to calculate localized rate parameters, so we need a function
def count_quakes_in_interval(center_date, #date
                             window_radius, #integer
                             dates_col): #column of dates
    
    count = 0
    
    for i in range(len(dates_col)):
        if dates_col[i] >= center_date - datetime.timedelta(days = window_radius):
            if dates_col[i] <= center_date + datetime.timedelta(days = window_radius):
                
                count += 1
                
    return(count)

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










#rate_matrix was a terrible name for this in retrospect. It 
#does not contain rates. It contains our test statistic for 
#each pair of regions
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



#now we look at maxes and miins
#first we find maxes
m = np.copy(rate_matrix)
maxims = []

for i in range(len(list_of_datasets)):
    m[i][i] = math.inf*-1

for i in range(5):
    argmax = m.argmax()
    maxims += [[argmax//len(rate_matrix),argmax%len(rate_matrix)]]
    m[argmax//len(rate_matrix),argmax%len(rate_matrix)] = math.inf*-1
    
mins = []
m = np.copy(rate_matrix)

for i in range(len(list_of_datasets)):
    m[i][i] = math.inf

for i in range(5):
    argmin = m.argmin()
    mins += [[argmin//len(rate_matrix),argmin%len(rate_matrix)]]
    m[argmin//len(rate_matrix),argmin%len(rate_matrix)] = math.inf




#now we make bootstrap samples. This next chuunk takes a stupid long time to run
bootstrap_size = 1000

np.random.seed(6789)

mins_bootstrap_samps = []

for i in range(len(mins)):
    print(i)
    j = mins[i][1]
    bootstrap_sample = []

    for jj in range(bootstrap_size):
        
        waiting_times = []
        expected_waiting_times = []
        
        for k in range(len(list_of_datasets[mins[i][0]]["DATE"])):
            #print(i, j, k, current_region["DATE"])
            starting_date = pd.to_datetime(localizedRates["DATES"].sample(1).apply(str).item())

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
        
        bootstrap_sample += [mean_stat]
        
    mins_bootstrap_samps += [bootstrap_sample]
    
    
    

maxs_bootstrap_samps = []

for i in range(len(maxims)):
    print(i)
    j = maxims[i][1]
    bootstrap_sample = []

    for jj in range(bootstrap_size):
        
        waiting_times = []
        expected_waiting_times = []
        
        for k in range(len(list_of_datasets[maxims[i][0]]["DATE"])):
            #print(i, j, k, current_region["DATE"])
            starting_date = pd.to_datetime(localizedRates["DATES"].sample(1).apply(str).item())

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
        
        bootstrap_sample += [mean_stat]
        
    maxs_bootstrap_samps += [bootstrap_sample]



#functions to calculate p values
def get_mins_p_val(value, bootstrap_samp):
    count = 0
    for i in range(len(bootstrap_samp)):
        if bootstrap_samp[i] <= value:
            count += 1
            
    p_value = count/len(bootstrap_samp) #proportion where bootstrap is more extreme than observation
    
    return(p_value)

def get_maxs_p_val(value, bootstrap_samp):
    count = 0
    for i in range(len(bootstrap_samp)):
        if bootstrap_samp[i] >= value:
            count += 1
            
    p_value = count/len(bootstrap_samp) #proportion where bootstrap is more extreme than observation
    
    return(p_value)



mins_p_values = []
maxs_p_values = []

for i in range(len(mins)):
    mins_p_values += [get_mins_p_val(rate_matrix[mins[i][0]][mins[i][1]], mins_bootstrap_samps1000[i])]
    
for i in range(len(maxims)):
    maxs_p_values += [get_maxs_p_val(rate_matrix[maxims[i][0]][maxims[i][1]], maxs_bootstrap_samps1000[i])]


#this next bit is just for getting those one-week probabilities in the last paragraph
waitingTimes_0_to_7 = []
waitingTimes_7_to_7 = []
waitingTimes_sim_to_7 = []



region = list_of_datasets[7]

for k in range(len(list_of_datasets[7]["DATE"])):
    starting_date = list_of_datasets[7]["DATE"][k] + datetime.timedelta(days=1)

    next_quake = find_next_quake(starting_date, region)

    if next_quake is not None:

        waitingTimes_7_to_7 += [next_quake]


for k in range(len(list_of_datasets[0]["DATE"])):
    starting_date = list_of_datasets[0]["DATE"][k]

    next_quake = find_next_quake(starting_date, region)

    if next_quake is not None:

        waitingTimes_0_to_7 += [next_quake]


for k in range(1000):
    #print(i, j, k, current_region["DATE"])
    starting_date = pd.to_datetime(localizedRates["DATES"].sample(1).apply(str).item())
    
    next_quake = find_next_quake(starting_date, region)

    if next_quake is not None:
        waitingTimes_sim_to_7 += [next_quake]



timeSpan = 7
count1 = 0
count2 = 0
count3 = 0

for i in range(len(waitingTimes_0_to_7)):
    if waitingTimes_0_to_7[i] <= timeSpan:
        count1 += 1
        
count1 = count1 / len(waitingTimes_0_to_7)

for i in range(len(waitingTimes_7_to_7)):
    if waitingTimes_7_to_7[i] <= timeSpan:
        count2 += 1
        
count2 = count2 / len(waitingTimes_7_to_7)

for i in range(len(waitingTimes_sim_to_7)):
    if waitingTimes_sim_to_7[i] <= timeSpan:
        count3 += 1
        
count3 = count3 / len(waitingTimes_sim_to_7)

print(count1, count2, count3)

#ok now we are done :)

