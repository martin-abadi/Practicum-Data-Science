#!/usr/bin/env python
# coding: utf-8

# <div style="border:solid green 4px; padding: 20px">Hi there! I can clearly see the work you've done on your project, it is the time to review the results. My critical comments are highlighted with <span style='color: red;'>red</span>,  less urgent remarks are in <span style='color: #ebd731;'>yellow</span>, recommendations and extra information - in <span style='color: green;'>green</span>.</div>

# # Research on apartment sales ads
# 
# You will have the data from a real estate agency. It is an archive of sales ads for realty in St. Petersburg, Russia, and the surrounding areas collected over the past few years. You’ll need to learn how to determine the market value of real estate properties. Your task is to define the parameters. This will make it possible to build an automated system that is capable of detecting anomalies and fraudulent activity.
# 
# There are two different types of data available for every apartment for sale. The first type is a user’s input. The second type is received automatically based upon the map data. For example, the distance from the downtown area, airport, the nearest park or body of water. 

# ### Step 1. Open the data file and study the general information. 

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

real_estate_data = pd.read_csv('/datasets/real_estate_data.csv',sep='\t')
print(real_estate_data.head())
print(real_estate_data.info())


# ### Conclusion

# The data needs to be process in order to work with. Capslocks, duplicates, information that is not helpful, time not in format, null, and more.

# <div style="border:solid green 4px; padding: 20px">Good. You might also want to add some description to your columns.</div>

# ### Step 2. Data preprocessing

# Every column is going to be check, if it has null we will treat, impossible data too, and long unique data we will try to categorize.

# In[3]:


print(real_estate_data['balcony'].unique())
real_estate_data['balcony'] = real_estate_data['balcony'].fillna(0.0)
print(real_estate_data['balcony'].unique())
print(real_estate_data['balcony'].value_counts())


# In[ ]:


print(real_estate_data['ceiling_height'].unique())
print(real_estate_data['ceiling_height'].max())
print(real_estate_data['ceiling_height'].min())
print(real_estate_data['ceiling_height'].value_counts())

real_estate_data.drop(real_estate_data[real_estate_data['ceiling_height'] > 6.0].index , inplace=True)
real_estate_data.drop(real_estate_data[real_estate_data['ceiling_height'] < 2.0].index , inplace=True)

print(real_estate_data['ceiling_height'].value_counts())
print(real_estate_data['ceiling_height'].unique())

ceil_mean = real_estate_data['ceiling_height'].mean()
real_estate_data['ceiling_height'] = real_estate_data['ceiling_height'].fillna(ceil_mean)

print(real_estate_data['ceiling_height'].unique())


# In[ ]:


print(real_estate_data['days_exposition'].unique())
real_estate_data.dropna(subset=['days_exposition'], inplace=True)
print(real_estate_data['days_exposition'].unique())
print(real_estate_data['days_exposition'].max())
print(real_estate_data['days_exposition'].min())

def days_exposition_to_group(row):
    income = row['days_exposition']/365
    if income <= 1. :
        return 'new'
    elif income <= 2.:
        return 'normal'
    return 'old'

real_estate_data['days_exposition_group'] = real_estate_data.apply(days_exposition_to_group, axis=1)
print(real_estate_data['days_exposition_group'].value_counts())


# In[ ]:


print(real_estate_data['first_day_exposition'].unique())
real_estate_data['first_day_exposition']= pd.to_datetime(real_estate_data['first_day_exposition'], format='%Y-%m-%dT%H:%M:%S')


# In[ ]:


print(real_estate_data['floor'].unique())
print(real_estate_data['floor'].value_counts())


# In[ ]:


print(real_estate_data['cityCenters_nearest'].unique())
print(real_estate_data['cityCenters_nearest'].value_counts())
print(real_estate_data['cityCenters_nearest'].max())
print(real_estate_data['cityCenters_nearest'].min())

def cityCenters_to_group(row):
    income = row['cityCenters_nearest']
    if income <= 2000. :
        return 'on_center'
    elif income <= 10000.:
        return 'close_range'
    elif income <= 20000.:
        return 'far_range'
    return 'suburb_range'

real_estate_data['cityCenters_group'] = real_estate_data.apply(cityCenters_to_group, axis=1)
print(real_estate_data['cityCenters_group'].value_counts())


# In[ ]:


print(real_estate_data['floors_total'].unique())

def floors_to_type(row):
    income = row['floors_total']
    if income <= 3 :
        return 'private_house'
    return 'apartment'

real_estate_data['flor_type'] = real_estate_data.apply(floors_to_type, axis=1)
print(real_estate_data['flor_type'].value_counts())


# In[ ]:


print(real_estate_data['airports_nearest'].unique())
print(real_estate_data['airports_nearest'].max())
print(real_estate_data['airports_nearest'].min())
print(real_estate_data['airports_nearest'].value_counts())

def airport_to_group(row):
    income = row['airports_nearest']
    if income <= 15000. :
        return 'close_range'
    elif income <= 50000.:
        return 'middle_range'
    return 'far_range'

real_estate_data['airport_group'] = real_estate_data.apply(airport_to_group, axis=1)
print(real_estate_data['airport_group'].value_counts())


# In[ ]:


print(real_estate_data['total_images'].unique())

def total_images_to_group(row):
    income = row['total_images']
    if income <= 2 :
        return 'few'
    elif income <= 10:
        return 'medium'
    return 'impressive'

real_estate_data['total_images_group'] = real_estate_data.apply(total_images_to_group, axis=1)
print(real_estate_data['total_images_group'].value_counts())


# In[ ]:


print(real_estate_data['total_area'].unique())
print(real_estate_data['total_area'].max())
print(real_estate_data['total_area'].min())

def total_area_to_group(row):
    income = row['total_area']
    if income <= 50. :
        return 'small'
    elif income <= 100.:
        return 'medium'
    return 'huge'

real_estate_data['total_area_group'] = real_estate_data.apply(total_area_to_group, axis=1)
print(real_estate_data['total_area_group'].value_counts())


# In[ ]:


print(real_estate_data['studio'].unique())


# In[ ]:


print(real_estate_data['rooms'].unique())
real_estate_data.drop(real_estate_data[real_estate_data['rooms'] < 2].index , inplace=True)
print(real_estate_data['rooms'].unique())

def rooms_to_group(row):
    income = row['rooms']
    if income <= 3 :
        return 'small'
    elif income <= 5:
        return 'medium'
    return 'villa'

real_estate_data['rooms_group'] = real_estate_data.apply(rooms_to_group, axis=1)
print(real_estate_data['rooms_group'].value_counts())


# In[ ]:


print(real_estate_data['ponds_nearest'].unique())
real_estate_data['ponds_nearest'] =  real_estate_data['ponds_nearest'].fillna(real_estate_data['ponds_nearest'].mean())
print(real_estate_data['ponds_nearest'].unique())
print(real_estate_data['ponds_nearest'].max())
print(real_estate_data['ponds_nearest'].min())

def ponds_nearest_to_group(row):
    income = row['ponds_nearest']
    if income <= 200 :
        return 'close_range'
    elif income <= 800:
        return 'medium_range'
    return 'far_range'

real_estate_data['ponds_nearest_group'] = real_estate_data.apply(ponds_nearest_to_group, axis=1)
print(real_estate_data['ponds_nearest_group'].value_counts())


# In[ ]:


print(real_estate_data['ponds_around3000'].unique())
real_estate_data['ponds_around3000'] = real_estate_data['parks_around3000'].fillna(0.0)


# In[ ]:


print(real_estate_data['parks_nearest'].unique())
real_estate_data['parks_nearest'].dropna(inplace=True)

def parks_nearest_to_group(row):
    income = row['parks_nearest']/1000
    if income <= 20 :
        return 'close_range'
    elif income <= 500:
        return 'medium_range'
    return 'far_range'

real_estate_data['parks_nearest_group'] = real_estate_data.apply(parks_nearest_to_group, axis=1)
print(real_estate_data['parks_nearest_group'].value_counts())


# In[ ]:


print(real_estate_data['kitchen_area'].unique())
real_estate_data['kitchen_area'].dropna(inplace=True)
print(real_estate_data['kitchen_area'].max())
print(real_estate_data['kitchen_area'].min())

def kitchen_to_group(row):
    income = row['kitchen_area']
    if income <= 5. :
        return 'small'
    elif income <= 15.:
        return 'medium'
    return 'huge'

real_estate_data['kitchen_group'] = real_estate_data.apply(kitchen_to_group, axis=1)
print(real_estate_data['kitchen_group'].value_counts())


# In[ ]:


print(real_estate_data['last_price'].unique())
print(real_estate_data['last_price'].max())
print(real_estate_data['last_price'].min())


# In[ ]:


print(real_estate_data['is_apartment'].unique())
real_estate_data['is_apartment'].dropna(inplace=True)
print(real_estate_data['is_apartment'].unique())


# In[ ]:


print(real_estate_data['locality_name'].unique())


# In[ ]:


print(real_estate_data['living_area'].unique())
real_estate_data['living_area'].dropna(inplace=True)
print(real_estate_data['living_area'].max())
print(real_estate_data['living_area'].min())

def living_to_group(row):
    income = row['living_area']
    if income <= 18. :
        return 'small'
    elif income <= 50.:
        return 'medium'
    return 'huge'

real_estate_data['linving_group'] = real_estate_data.apply(living_to_group, axis=1)
print(real_estate_data['linving_group'].value_counts())


# In[ ]:


print(real_estate_data['parks_around3000'].unique())
real_estate_data['parks_around3000'] = real_estate_data['parks_around3000'].fillna(0.0)
print(real_estate_data['parks_around3000'].unique())


# In[ ]:


print(real_estate_data['open_plan'].unique())
print(real_estate_data['open_plan'].value_counts())


# <div style="border:solid red; 4px; padding: 20px">There is no need to implement the whole Step 2 into a single cell. 2-10 rows of code, doing a whole small logical step is just enough for a code cell. Output would be separated and visible. Also it becomes so much easier to debug. Also consider formatting your code with one or two empty lines between logically integral blocks. That comment is applicable to the whole project, not only cell above.</div>

# ### Conclusion

# open_plan: few information for True variables
# parks_nearest: strange information
# studio: only false, not relevant
# Many columns had to many unique values, so I tried to categorize them.
# Columns with null objects that could be fill with a rasonable data like 'mean' for ceiling higt, or 0 for no informations of parks or ponds around 3 km, were filled. But for not rasonable data, there rows where deleted.
# Other data that was impossible, like ceiling hight, was verified to standar information like houses above 2 meters.

# ### Step 3. Make calculations and add them to the table

# In[4]:


def price_per_square_meter(row):
    price = row['last_price']
    meter = row['total_area']
    return (price/meter)

real_estate_data['price_per_square_meter'] = real_estate_data.apply(price_per_square_meter, axis=1)
print(real_estate_data['price_per_square_meter'].value_counts())
print(real_estate_data['price_per_square_meter'].unique())
print(real_estate_data['price_per_square_meter'].max())
print(real_estate_data['price_per_square_meter'].min())


# In[ ]:


def living_area_ratio(row):
    living_area = row['living_area']
    meter = row['total_area']
    return (living_area/meter)

real_estate_data['living_area_ratio'] = real_estate_data.apply(living_area_ratio, axis=1)
print(real_estate_data['living_area_ratio'].value_counts())
print(real_estate_data['living_area_ratio'].unique())
print(real_estate_data['living_area_ratio'].max())
print(real_estate_data['living_area_ratio'].min())


# In[ ]:


def kitchen_area_ratio(row):
    kitchen_area = row['kitchen_area']
    meter = row['total_area']
    return (kitchen_area/meter)

real_estate_data['kitchen_area_ratio'] = real_estate_data.apply(kitchen_area_ratio, axis=1)
print(real_estate_data['kitchen_area_ratio'].value_counts())
print(real_estate_data['kitchen_area_ratio'].unique())
print(real_estate_data['kitchen_area_ratio'].max())
print(real_estate_data['kitchen_area_ratio'].min())


# In[ ]:


def which_floor(row):
    floor = row['floor']
    floors_total = row['floors_total']
    if floor == 1 :
        return 'first'
    elif floor == floors_total:
        return 'last'
    return 'other'

real_estate_data['which_floor'] = real_estate_data.apply(which_floor, axis=1)
print(real_estate_data['which_floor'].value_counts())


# In[ ]:


real_estate_data['weekday'] = real_estate_data['first_day_exposition'].dt.weekday
print(real_estate_data['weekday'].value_counts())
real_estate_data['month'] = pd.DatetimeIndex(real_estate_data['first_day_exposition']).month
print(real_estate_data['month'].value_counts())
real_estate_data['year'] = pd.DatetimeIndex(real_estate_data['first_day_exposition']).year
print(real_estate_data['year'].value_counts())


# <div style="border:solid green 4px; padding: 20px">Your custom functions and new columns are absolutely correct.</div>

# ### Step 4. Conduct exploratory data analysis and follow the instructions below:

# 4.1- Carefully investigate the following parameters: square area, price, number of rooms, and ceiling height. Plot a histogram for each parameter.

# In[ ]:


real_estate_data.hist('total_area')
real_estate_data.hist('last_price')
real_estate_data.hist('rooms')
real_estate_data.hist('ceiling_height')
real_estate_data.hist('first_day_exposition')
real_estate_data.hist('days_exposition')


# 4.2- Examine the time it's taken to sell the apartment and plot a histogram. Calculate the mean and median and explain the average time it usually takes to complete a sale. When can a sale be considered to have happened rather quickly or taken an extra long time?

# In[ ]:


print(real_estate_data['days_exposition'].mean())
print(real_estate_data['days_exposition'].median())


# 4.3- Which factors have had the biggest influence on an apartment’s price? Examine whether the value depends on the total square area, number of rooms, floor (top or bottom), or the proximity to the downtown area. Also study the correlation to the publication date: day of the week, month, and year.

# In[ ]:


pd.plotting.scatter_matrix(real_estate_data[['price_per_square_meter','rooms','which_floor','cityCenters_nearest']], figsize=(10,10))
real_estate_data[['year','month','weekday','price_per_square_meter','rooms','which_floor','cityCenters_nearest']].corr()


# 4.4- Select the 10 localities with the largest number of ads then calculate the average price per square meter in these localities. Determine which ones have the highest and lowest housing prices. You can find this data by name in the ’locality_name’ column.

# In[ ]:


largest_places = real_estate_data['locality_name'].value_counts().nlargest(n=10).index.tolist()
data_of_largest = real_estate_data[real_estate_data['locality_name'].isin(largest_places)].reset_index(drop=True)
data_of_largest.groupby(['locality_name'])['price_per_square_meter'].agg(['mean'])


# 4.5- Thoroughly look at apartment offers: Each apartment has information about the distance to the city center. Select apartments in Saint Petersburg (‘locality_name’). Your task is to pinpoint which area is considered to be downtown. In order to do that, create a column with the distance to the city center in km and round to the nearest whole number. Next, calculate the average price for each kilometer and plot a graph to display how prices are affected by the distance to the city center. Find a place on the graph where it shifts significantly. That's the downtown border.

# In[ ]:


sp_data = real_estate_data[real_estate_data['locality_name'] == 'Санкт-Петербург']
sp_data['km_to_cityCenter'] = round(sp_data['cityCenters_nearest']/1000)
# print(sp_data.head())


# 4.6- Select all the apartments in the downtown and examine correlations between the following parameters: total area, price, number of rooms, ceiling height. Also identify the factors that affect an apartment’s price: number of rooms, floor, distance to the downtown area, and ad publication date. Draw your conclusions. Are they different from the overall deductions about the entire city?

# In[ ]:


plt.plot([0, 30], [1.8*10**7, 1*10**7], 'k-')
sp_data.groupby(['km_to_cityCenter'])['last_price'].agg('mean').plot(figsize=(10,5), xticks=np.arange(0,40,2))
pd.plotting.scatter_matrix(real_estate_data[['last_price','cityCenters_nearest','total_area','rooms','ceiling_height']], figsize=(10,10))
real_estate_data[['year','month','weekday','last_price','cityCenters_nearest','total_area','rooms','ceiling_height']].corr()


# <div style="border:solid #ebd731; 4px; padding: 20px"><a href="https://www.python.org/dev/peps/pep-0008/">PEP 8</a> recommends you to place all your imports into your first cell, so other users would have an opportunity to check if their environment is ready to lanch your project or not by a quick glance on it.</div>

# <div style="border:solid #ebd731; 4px; padding: 20px">Also, I don't really understand what is going on here, eventually some of the code is not meant to be commented.</div>

# <div style="border:solid green 4px; padding: 20px">Please fix current issues, so I could review you project once more. See you!</div>

# ### Conclusion

# Most of the house are normal, same ceiling height, same are, price and number of rooms. This is probably since it is the normal population. It takes almost half a year in average to sell the house. The median and the histogram teach us that most of the houses take only 3 month to sell, but some few houses have stron influence to the average since they are waiting allot of time to be selled. We can see that some few months is regular, while more than a year is quiete irregular and something is wrong with the house or it price is too high for what they offer. The outlying values where removed already on task 2. The bigger the house is, the higher is the price. But, since most of the smaller houses are closer to the city center, there price is also pretty high. There is not a correlation to the publication date, they are all under 0.1. The locality the highest housing prices is: 'Санкт-Петербург' (Saint Petersburg) with a mean of- 111512.518781; and the lowest housing prices is: Всеволожск' (Vsevolozhsk) with a mean of- 65336.134341.
# The closer to the city center, the higher is the price. Downtown finishes 9 km from the most centric place of the city and that is the border of the downtown. The number of rooms next to the downtown was very small, meining that small families or people without children live near the downtown.
# Yes we can see that in the last years, smaller houses are being selled, and they are closer to the city center. Also, there prices are getting down and being sell cheaper. The week and the month does not affect.
# It seems that the nearest you are from downtown, the higher is the price, but the still the correlation is weak.

# ### Step 5. Overall conclusion

# The data had allot of information, which some of them helped but some of them were irelevant.
# In the pre-process I clean the data, categorize most of it since allot of the data had to many uniques information.
# The dat had missing values for most of the cities, and the majority of the apartments were from St. Petersburg.
# 
# We learn that the median was under the mean, meaning that most of the apartments are been sell by less than the mean average. Most of the apartments are for the city center, were the number of rooms decreases.
# 
# By ploting the data of Saint Ptersburg, we could learn were ther border of the city-center goes threw. Also we noticed that Saint Ptersburg is the most expensive city for the price per square meter. 
# 
# Moreover, we learned that the prices are gettin down from last years, the houses that are been sailed are smaller than
# 

# ### Project completion checklist
# 
# Mark the completed tasks with 'x'. Then press Shift+Enter.

# - [x]  file opened
# - [ ]  files explored (first rows printed, info() method)
# - [ ]  missing values determined
# - [ ]  missing values filled in
# - [ ]  clarification of the discovered missing values provided
# - [ ]  data types converted
# - [ ]  explanation of which columns had the data types changed and why
# - [ ]  calculated and added to the table: the price per square meter
# - [ ]  calculated and added to the table: the day of the week, month, and year that the ad was published
# - [ ]  calculated and added to the table: which floor the apartment is on (first, last, or other)
# - [ ]  calculated and added to the table: the ratio between the living space and the total area, as well as between the kitchen space and the total area
# - [ ]  the following parameters investigated: square area, price, number of rooms, and ceiling height
# - [ ]  histograms for each parameter created
# - [ ]  task completed: "Examine the time it's taken to sell the apartment and create a histogram. Calculate the mean and median and explain the average time it usually takes to complete a sale. When can a sale be considered extra quick or taken an extra slow?"
# - [ ]  task completed: "Remove rare and outlying values and describe the specific details you've discovered."
# - [ ]  task completed: "Which factors have had the biggest influence on an apartment’s value? Examine whether the value depends on price per meter, number of rooms, floor (top or bottom), or the proximity to the downtown area. Also study the correlation to the ad posting date: day of the week, month, and year. "Select the 10 places with the largest number of ads and then calculate the average price per square foot in these localities. Select the locations with the highest and lowest housing prices. You can find this data by name in the ’*locality_name’* column. "
# - [ ]  task completed: "Thoroughly look at apartment offers: each apartment has information about the distance to the downtown area. Select apartments in Saint Petersburg (*‘locality_name’*). Your task is to pinpoint which area is considered to be downtown. Create a column with the distance to the downtown area in km and round to the nearest whole number. Next, calculate the average price for each kilometer. Build a graph to display how prices are affected by the distance to the downtown area. Define the turning point where the graph significantly changes. This will indicate downtown. "
# - [ ]  task completed: "Select a segment of apartments in the downtown. Analyze this area and examine the following parameters: square area, price, number of rooms, ceiling height. Also identify the factors that affect an apartment’s price (number of rooms, floor, distance to the downtown area, and ad publication date). Draw your conclusions. Are they different from the overall conclusions about the entire city?"
# - [ ]  each stage has a conclusion
# - [ ]  overall conclusion drawn
