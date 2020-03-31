#!/usr/bin/env python
# coding: utf-8

# <div class="alert alert-block alert-info">
# <h2> Comments </h2>
# </div>
# 
# Hi Martin,
# 
# I have checked you work and left comments in such cells. Cells are of two types:
# 
# <div class="alert alert-block alert-danger">
# <p> <strong> A red colored cell </strong> indicates that you need to improve or adjust part of the project above. </p>
# </div>
# <div class="alert alert-block alert-info">
# <p> <strong> A blue colored cell </strong> indicates that no improvements are needed in the cells above. May include some suggestions and recommendations.</p>
# </div>
# 
# Hope it all will be clear to you :)
# 
# You did a good job 😀. You  understand what you are doing and why, also can make right conclusions - which is great 👍.
# 
# Thank you for keeping your notebook clean and structured, with clear explanations :)
# 
# The project is accepted :)
# 
# *Good luck!*
# 
# ------------

# # Step 1 - Open the data file and study the general information
# 1. First we import libraries, open files and study the data. 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st


# In[2]:


df_megaline_calls = pd.read_csv('/datasets/megaline_calls.csv')
df_megaline_internet = pd.read_csv('/datasets/megaline_internet.csv')
df_megaline_messages = pd.read_csv('/datasets/megaline_messages.csv')
df_megaline_tariffs = pd.read_csv('/datasets/megaline_tariffs.csv')
df_megaline_users = pd.read_csv('/datasets/megaline_users.csv')


# In[3]:


print(df_megaline_calls.head())
print(df_megaline_calls.info())


# In[4]:


print(df_megaline_internet.head())
print(df_megaline_internet.info())


# In[5]:


print(df_megaline_messages.head())
print(df_megaline_messages.info())


# In[6]:


print(df_megaline_tariffs.head())
print(df_megaline_tariffs.info())


# In[7]:


print(df_megaline_users.head())
print(df_megaline_users.info())


# The data is separated in five tables, all with same key 'user_id'. We will join them.
# We need to deal with nulls, dates and data type, integers and strings, and check they are all possible data.
# Dataframe df_megaline_tariffs is all set.

# <div class="alert alert-block alert-info">
# <h2> Comments </h2>
# </div>
# 
# Good :)
# 
# ------------

# # Step 2 - Prepare the data
# 
# Correcting colums.

# Table 1: df_megaline_calls = id, user_id, call_date, duration,  137735 entries

# In[8]:


print(df_megaline_calls['id'].unique())
print(df_megaline_calls['id'].value_counts())


# In[9]:


print(df_megaline_calls['user_id'].unique())
print(df_megaline_calls['user_id'].value_counts())


# In[10]:


print(df_megaline_calls['call_date'].unique())
df_megaline_calls['call_date']=pd.to_datetime(df_megaline_calls['call_date'], format='%Y-%m-%d')
df_megaline_calls['month'] = pd.DatetimeIndex(df_megaline_calls['call_date']).month
df_megaline_calls['year'] = pd.DatetimeIndex(df_megaline_calls['call_date']).year
df_megaline_calls['weekday'] = df_megaline_calls['call_date'].dt.weekday
print(df_megaline_calls['call_date'].value_counts())
print(df_megaline_calls['month'].value_counts())
print(df_megaline_calls['year'].value_counts())
print(df_megaline_calls['weekday'].value_counts())


# In[11]:


print(df_megaline_calls['duration'].unique())
print(df_megaline_calls['duration'].value_counts())


# Conclusions from first subtable: The ID datas are okay. The call date was turm to date-time and separated to year, month and week-day. Many calls have 0.0 duration (almost 1/5 from the rows), probably since calls were not answered or it is for Ipads. No nulls to deal with.

# Table 2: df_megaline_internet = id, user_id, session_date, mb_used, 104825 entries

# In[12]:


print(df_megaline_internet['id'].unique())
print(df_megaline_internet['id'].value_counts())


# In[13]:


print(df_megaline_internet['user_id'].unique())
print(df_megaline_internet['user_id'].value_counts())


# In[14]:


print(df_megaline_internet['session_date'].unique())
df_megaline_internet['session_date']=pd.to_datetime(df_megaline_internet['session_date'], format='%Y-%m-%d')
df_megaline_internet['month'] = pd.DatetimeIndex(df_megaline_internet['session_date']).month
df_megaline_internet['year'] = pd.DatetimeIndex(df_megaline_internet['session_date']).year
df_megaline_internet['weekday'] = df_megaline_internet['session_date'].dt.weekday
print(df_megaline_internet['session_date'].value_counts())
print(df_megaline_internet['month'].value_counts())
print(df_megaline_internet['year'].value_counts())
print(df_megaline_internet['weekday'].value_counts())


# In[15]:


print(df_megaline_internet['mb_used'].unique())
print(df_megaline_internet['mb_used'].value_counts())
df_megaline_internet['mb_used'] = df_megaline_internet['mb_used'].fillna(0.0)
print(df_megaline_internet['mb_used'].mean())
print(df_megaline_internet['mb_used'].max())
print(df_megaline_internet['mb_used'].min())


# 'id' and 'user_id' seem okay. We change the date to date-time and separated to year, month and week-day. Aat 'mb_used' there are no null, and 0.0 variables may be reasonable since sometimes older people doesn't know how to use the internet.

# Table 3: df_megaline_messages =  id, user_id, message_date, 76051 entries

# In[16]:


print(df_megaline_messages['id'].unique())
print(df_megaline_messages['id'].value_counts())


# In[17]:


print(df_megaline_messages['user_id'].unique())
print(df_megaline_messages['user_id'].value_counts())


# In[18]:


print(df_megaline_messages['message_date'].unique())
df_megaline_messages['message_date']=pd.to_datetime(df_megaline_messages['message_date'], format='%Y-%m-%d')
df_megaline_messages['message_date']=pd.to_datetime(df_megaline_messages['message_date'], format='%Y-%m-%d')
df_megaline_messages['month'] = pd.DatetimeIndex(df_megaline_messages['message_date']).month
df_megaline_messages['year'] = pd.DatetimeIndex(df_megaline_messages['message_date']).year
df_megaline_messages['weekday'] = df_megaline_messages['message_date'].dt.weekday
print(df_megaline_messages['message_date'].value_counts())
print(df_megaline_messages['month'].value_counts())
print(df_megaline_messages['year'].value_counts())
print(df_megaline_messages['weekday'].value_counts())


# Again, 'id' and 'user_id' seem okay. We change the date to date-time at 'message_date' and separated to year, month and week-day.

# Table 5: df_megaline_users = user_id, first_name, last_name, age, city, reg_date, tariff, churn_date, 500 entries

# In[19]:


print(df_megaline_users['user_id'].unique())
print(df_megaline_users['user_id'].value_counts())


# In[20]:


print(df_megaline_users['first_name'].unique())
print(df_megaline_users['first_name'].value_counts())


# In[21]:


print(df_megaline_users['last_name'].unique())
print(df_megaline_users['last_name'].value_counts())


# In[22]:


print(df_megaline_users['age'].unique())
print(df_megaline_users['age'].value_counts())


# In[23]:


print(df_megaline_users['city'].unique())
print(df_megaline_users['city'].value_counts())


# In[24]:


print(df_megaline_users['reg_date'].unique())
df_megaline_users['reg_date']=pd.to_datetime(df_megaline_users['reg_date'], format='%Y-%m-%d')
df_megaline_users['reg_month'] = pd.DatetimeIndex(df_megaline_users['reg_date']).month
df_megaline_users['reg_year'] = pd.DatetimeIndex(df_megaline_users['reg_date']).year
df_megaline_users['reg_weekday'] = df_megaline_users['reg_date'].dt.weekday
print(df_megaline_users['reg_date'].value_counts())
print(df_megaline_users['reg_month'].value_counts())
print(df_megaline_users['reg_year'].value_counts())
print(df_megaline_users['reg_weekday'].value_counts())


# In[25]:


print(df_megaline_users['tariff'].unique())
print(df_megaline_users['tariff'].value_counts())


# In[26]:


print(df_megaline_users['churn_date'].unique())
df_megaline_users['churn_date']=pd.to_datetime(df_megaline_users['churn_date'], format='%Y-%m-%d')
df_megaline_users['month'] = pd.DatetimeIndex(df_megaline_users['churn_date']).month
df_megaline_users['year'] = pd.DatetimeIndex(df_megaline_users['churn_date']).year
df_megaline_users['weekday'] = df_megaline_users['churn_date'].dt.weekday
print(df_megaline_users['churn_date'].value_counts())
print(df_megaline_users['month'].value_counts())
print(df_megaline_users['year'].value_counts())
print(df_megaline_users['weekday'].value_counts())


# 'churn_date' & 'reg_date' were changed to date-time. all other parameters seem okay.

# <div class="alert alert-block alert-info">
# <h2> Comments </h2>
# </div>
# 
# Okay :)
# 
# Are there any fully duplicated observations in the datasets?
# 
# ------------

# 2.1 - The number of calls made and minutes spent per month for each user.

# In[27]:


df_gb_megaline_calls = df_megaline_calls.groupby(['user_id','month']).agg({'duration':'sum','user_id':'count'})
df_gb_megaline_calls.columns = ['duration','total_calls']
# df_gb_megaline_calls = df_gb_megaline_calls.groupby(['user_id','month','duration','total_calls']).size()
print(df_gb_megaline_calls.head())


# 2.2 - The number of SMS sent per month for each user.

# In[28]:


df_gb_megaline_messages = df_megaline_messages.groupby(['user_id','month']).agg({'user_id':'count'}).rename(columns={'id':'month'})
df_gb_megaline_messages.columns = ['messages']
# df_gb_megaline_messages = df_gb_megaline_messages.groupby(['user_id','month','messages']).size()
print(df_gb_megaline_messages.head())


# 2.3 - The amount of traffic used per month for each user.

# In[29]:


df_gb_megaline_internet = df_megaline_internet.groupby(['user_id','month']).agg({'mb_used':'sum'}).rename(columns={'id':'month'})
df_gb_megaline_internet.columns = ['mb_used']
# df_gb_megaline_internet = df_gb_megaline_internet.groupby(['user_id','month','mb_used']).size()
print(df_gb_megaline_internet.head())


# <div class="alert alert-block alert-info">
# <h2> Comments </h2>
# </div>
# 
# Good :)
# 
# Before summing up calls durations and Mb used you need to round all values up, because it is company's policy. By not doing so you cut company's real profit :(
# 
# ------------

# 2.4 - The monthly profit from each of the users.

# First we merge all tables

# In[30]:


df_gb_megaline_cal = df_megaline_calls.groupby(['user_id','month']).agg({'duration':'sum'})
print(df_gb_megaline_cal.head())
user_plan = df_megaline_users[['user_id','tariff']]


# In[31]:


df_users_usage = pd.concat([df_gb_megaline_cal,df_gb_megaline_messages,df_gb_megaline_internet],axis=1).reset_index().merge(user_plan,on='user_id')
df_users_usage.columns = ['user_id','month','minutes','sms','traffic','tariff']


# In[32]:


df_users_usage.head()


# In[33]:


df_users_usage.fillna(0, inplace=True)
print(df_users_usage.info())
print(df_users_usage.head())


# In[34]:


# user_plan['tariff'] = user_plan['tariff'].astype(str)
# user_plan.info()


# Second we will calculate for each user if he exceeded the plan usage

# In[35]:


def calc_ex_min(df_users):
    minutes = df_users['minutes']
    tariff = df_users['tariff']    
    surf_minutes = 500    
    ultimate_minutes = 3000
    minu = 0
    
    if tariff == "surf":
        if minutes > surf_minutes:
            minu = minutes-surf_minutes
    else:
        if minutes > ultimate_minutes:
            minu = minutes-ultimate_minutes
    return np.ceil(minu)


# In[36]:


def calc_ex_traff(df_users):
    traffic = df_users['traffic']
    tariff = df_users['tariff']    
    surf_traffic = 15*1000      #mega-bite
    ultimate_traffic = 30*1000  #mega-bite
    traf = 0
    
    if tariff == "surf":
        if traffic > surf_traffic:
            traf = traffic-surf_traffic
    else:
        if traffic > ultimate_traffic:
            traf = traffic-ultimate_traffic
    return np.ceil(traf)


# In[37]:


def calc_ex_sms(df_users):
    messages = df_users['sms']
    tariff = df_users['tariff']    
    surf_message = 50    
    ultimate_message = 1000
    mess = 0
    
    if tariff == "surf":
        if messages > surf_message:
            mess = messages-surf_message
    else:
        if messages > ultimate_message:
            mess = messages-ultimate_message
    return np.ceil(mess)


# In[38]:


df_users_usage['exceeding_minutes'] = df_users_usage.apply(calc_ex_min,axis=1)
df_users_usage['exceeding_traffic'] = df_users_usage.apply(calc_ex_traff,axis=1)
df_users_usage['exceeding_sms'] = df_users_usage.apply(calc_ex_sms,axis=1)
print(df_users_usage.head())


# In[39]:


def calc_monthly_profit(df_usage):
    minutes = df_usage['exceeding_minutes']
    traffic = df_usage['exceeding_traffic']
    sms = df_usage['exceeding_sms']
    tariff = df_usage['tariff']
    
    surf_monthly = 20
    surf_minutes = 0.03  
    surf_traffic = 10         # in GB
    surf_message = 0.03
        
    ultimate_monthly = 70
    ultimate_minutes = 0.01
    ultimate_traffic = 7      # in GB
    ultimate_message = 0.01
    
    cur_sum = 0
    if tariff == 'surf':
        cur_sum = cur_sum + surf_monthly
        cur_sum = cur_sum + (surf_message*sms)
        cur_sum = cur_sum + (surf_traffic*(traffic/1000))
        cur_sum = cur_sum + (surf_minutes*minutes)
    else:
        cur_sum = cur_sum + ultimate_monthly
        cur_sum = cur_sum + (ultimate_message*sms)
        cur_sum = cur_sum + (ultimate_traffic*(traffic/1000))
        cur_sum = cur_sum + (ultimate_minutes * minutes)
    return cur_sum


# In[40]:


df_users_usage['profit'] = df_users_usage.apply(calc_monthly_profit,axis=1)
df_rev_per_month = df_users_usage[['user_id','month','profit']]
df_rev_per_month.head()


# <div class="alert alert-block alert-info">
# <h2> Comments </h2>
# </div>
# 
# Good :)
# 
# ------------

# # Step 3 - Analyse the data
# 
# 3.1 - Describe the clients' behavior. For the users of each of the plans, find the number of minutes and SMS and the volume of web traffic they require per month.

# In[41]:


df_tariff_users_usage = df_users_usage.groupby(['tariff','month']).agg({'minutes':'sum','sms':'sum','traffic':'sum'})
df_tariff_users_usage.head()


# 3.2 - Calculate the mean, dispersion and standard deviation. Plot histograms. Describe the distributions.
# 
# First, we will separate the data by tariff.

# In[42]:


df_surf_users_usage = df_users_usage.query('tariff == "surf"')[['user_id','minutes','traffic','sms']].reset_index()
df_ultimate_users_usage = df_users_usage.query('tariff == "ultimate"')[['user_id','minutes','traffic','sms']].reset_index()
df_surf_users_usage.head()
df_ultimate_users_usage.head()

For surf information:
# In[43]:


surf_minutes_mean = np.mean(df_surf_users_usage['minutes'])
surf_minutes_std = np.std(df_surf_users_usage['minutes'])
surf_traffic_mean = np.mean(df_surf_users_usage['traffic'])
surf_traffic_std = np.std(df_surf_users_usage['traffic'])
surf_sms_mean = np.mean(df_surf_users_usage['sms'])
surf_sms_std = np.std(df_surf_users_usage['sms'])
print('The mean of minutes "surf" users talk per month is: {:.2f}, and the standart deviasion is: {:.2f}'.format(surf_minutes_mean,surf_minutes_std))
print('The mean of volume of web traffic "surf" users use per month is: {:.2f}, and the standart deviasion is: {:.2f}'.format(surf_traffic_mean,surf_traffic_std))
print('The mean of SMS "surf" users sent per month is: {:.2f}, and the standart deviasion is: {:.2f}'.format(surf_sms_mean,surf_sms_std))


# For ultimate information:

# In[44]:


ultimate_minutes_mean = np.mean(df_ultimate_users_usage['minutes'])
ultimate_minutes_std = np.std(df_ultimate_users_usage['minutes'])
ultimate_traffic_mean = np.mean(df_ultimate_users_usage['traffic'])
ultimate_traffic_std = np.std(df_ultimate_users_usage['traffic'])
ultimate_sms_mean = np.mean(df_ultimate_users_usage['sms'])
ultimate_sms_std = np.std(df_ultimate_users_usage['sms'])
print('The mean of minutes "ultimate" users talk per month is: {:.2f}, and the standart deviasion is: {:.2f}'.format(ultimate_minutes_mean,ultimate_minutes_std))
print('The mean of volume of web traffic "ultimate" users use per month is: {:.2f}, and the standart deviasion is: {:.2f}'.format(ultimate_traffic_mean,ultimate_traffic_std))
print('The mean of SMS "ultimate" users sent per month is: {:.2f}, and the standart deviasion is: {:.2f}'.format(ultimate_sms_mean,ultimate_sms_std))


# ## Conclusion
# Both users kind have very near use, no matter their plan. The std. is high in comparision to the mean in each group, meaning that the customers are very extremate one of each other.
# Surf users only exceed in average there web monthly package amount... but sms, and call minutes are in average underneeth the upper bound, while Ultimate users do not exceed any theme and they even don't get almost to the upper-bound.

# <div class="alert alert-block alert-info">
# <h2> Comments </h2>
# </div>
# 
# Good :)
# 
# ------------

# 3.3 - Plot histograms

# In[45]:


df_surf_users_usage.hist(column='minutes', bins=50, alpha=0.5) 
df_ultimate_users_usage.hist(column='minutes', bins=50, alpha=0.5)


# In[46]:


df_surf_users_usage.hist(column='traffic', bins=50, alpha=0.5) 
df_ultimate_users_usage.hist(column='traffic', bins=50, alpha=0.5)


# In[47]:


df_surf_users_usage.hist(column='sms', bins=50, alpha=0.5) 
df_ultimate_users_usage.hist(column='sms', bins=50, alpha=0.5)


# ## Conclusion
# As we said before, both users kind have very near use density, no matter their plan. The parameter with bigger diferention is the sms, where the ultimate users use a little bit more.

# 3.4 - Describe the distributions
# 
# Where the distribution of the minutes and traffic use seem to have a normal distributin, the sms distribution is more as from the union distribution.

# <div class="alert alert-block alert-info">
# <h2> Comments </h2>
# </div>
# 
# Good :)
# 
# You can plot same values of the tariffs on the same histogram to make comparison easier :)
# 
# *P.S. Use [subplots](https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.subplot.html) to plot graphs inline :)*
# 
# ------------

# # Step 4 - Test the hypotheses
# 
# 4.1 - the average profit from the users of Ultimate and Surf calling plans is different.

# In[48]:


profit_surf = df_users_usage.groupby(['tariff'])['profit'].get_group('surf')
profit_ultimate = df_users_usage.groupby(['tariff'])['profit'].get_group('ultimate')

print('The mean profit of "surf" users is: {:.2f} dollars.'.format(profit_surf.mean()))
print('The mean profit of "ultimate" users is: {:.2f} dollars.'.format(profit_ultimate.mean()))


# In[49]:


alpha = 0.05

results = st.ttest_ind(
        profit_surf, 
        profit_ultimate)
print('p-value:', results.pvalue)

if (results.pvalue<alpha):
    print("We reject the null hypothesis")
else:
    print("We can't reject the null hypothesis")


# ## Conclusion
# Ultimate users pay more in average than surf users, and we can reject the null hypothesis by alpha 0.05 and more (8.516e-09). By the histograms we saw before, users use the same amount of minutes, traffic and messages capacity. 'ultimate' users pay more since their plan is more expensive, but most of them does not use the extra capacity they get.

# 4.2 - The average profit from the users in NY-NJ area is different from that of the users from other regions.

# In[50]:


df_ny_nj_users = df_megaline_users['city'].apply(lambda x: True if 'NY-NJ' in x else False)
list_ny_nj_users = df_megaline_users[df_ny_nj_users]['user_id'].values.tolist()
profit_ny_nj = df_users_usage[df_users_usage['user_id'].isin(list_ny_nj_users)]['profit']
profit_all_others = df_users_usage[~df_users_usage['user_id'].isin(list_ny_nj_users)]['profit']


# In[51]:


print('The mean profit of NY-NJ area users is: {:.2f} dollars.'.format(profit_ny_nj.mean()))
print('The mean profit of all other users is: {:.2f} dollars.'.format(profit_all_others.mean()))


# In[52]:


alpha = 0.05

results = st.ttest_ind(
        profit_ny_nj, 
        profit_all_others)
print('p-value:', results.pvalue)

if (results.pvalue<alpha):
    print("We reject the null hypothesis")
else:
    print("We can't reject the null hypothesis")


# ## Conclusion
# NY-NJ users pay less in average than all other users. They may be smarter and check which plan is better for them and pay less.
# By t-test with alpha 0.5 we can't say we can reject the null hypothesis, but the p-value is so close, we can almost say is almost rejectable.

# <div class="alert alert-block alert-info">
# <h2> Comments </h2>
# </div>
# 
# Okay :)
# 
# You need to state null hypothesis before running a test.
# 
# ------------

# # Step 5 - Overall conclusion
# After recieving 5 different tables, we merged them to take out overall information. The tables needed some refactor of columns specialy with dates.
# 
# After merging the tables, group by plan, users_id and month, we found out that 'ultimate' users pay more than the 'surf' users, even if they use almost the same capacity of sms, call minutes and internet traffic. We could understand this from plots and histograms we made.
# 
# Surf users only exceed in average there web monthly package amount... but sms, and call minutes are in average underneath the upper bound. Ultimate users do not exceed any theme and they even don't get almost to the upper-bound and their plan is over estimated and more expensive using it as normal people.
# 
# At the ende, we compeared between the profit from Surf users and Ultimate user. We saw that by confidence level of alpha = 8.516e-09 we could say that Surf users pay less than Ultimate users.
# When compearing NY-NJ users and all the rest, we could almost say there is a difference between the profit from NY-NJ users, where NY-NJ users pay less. By alpha 0.05 we could not reject the null hyphotesis, but by 0.051 we could.
# 

# <div class="alert alert-block alert-info">
# <h2> Comments </h2>
# </div>
# 
# Okay :)
# 
# So, what does it all mean for the company?
# 
# ------------
