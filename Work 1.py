#!/usr/bin/env python
# coding: utf-8

# ## Commets from reviewer
# 
# <span style="color:green"> Hi! Congratulations on your first project :)I know that first work is the hardest one. You did a good job, however some things are missing. Please find my comments in the Markdown cells with green text. Make necessary adjustments to your work, answer my questions and send it back. Good luck! :) </span>

# ## Analyzing borrowers’ risk of defaulting
# 
# Your project is to prepare a report for a bank’s loan division. You’ll need to find out if a customer’s marital status and number of children has an impact on whether they will default on a loan. The bank already has some data on customers’ credit worthiness.
# 
# Your report will be considered when building a **credit scoring** of a potential customer. A ** credit scoring ** is used to evaluate the ability of a potential borrower to repay their loan.

# ### Step 1. Open the data file and have a look at the general information. 

# In[17]:


import pandas as pd
credit_scoring = pd.read_csv('/datasets/credit_scoring_eng.csv')
print(credit_scoring.head(10))
print(credit_scoring.info())


# ### Conclusion

# The data needs to be process in order to work with. Capslocks, duplicates, information that is not helpful, and more.

# ### Step 2. Data preprocessing

# ### Processing missing values

# In[10]:


# print(credit_scoring['children'].unique())
# print(credit_scoring['days_employed'].unique())
# print(credit_scoring['dob_years'].unique())
# print(credit_scoring['education'].unique())
# print(credit_scoring['education_id'].unique())
# print(credit_scoring['family_status'].unique())
# print(credit_scoring['family_status_id'].unique())
# print(credit_scoring['gender'].unique())
# print(credit_scoring['income_type'].unique())
# print(credit_scoring['debt'].unique())
# print(credit_scoring['total_income'].unique())
# print(credit_scoring['purpose'].unique())
# print(credit_scoring['gender'].value_counts())
# print(credit_scoring['children'].value_counts())
# age_data = credit_scoring[credit_scoring['dob_years']>0]
# age_data_avg = age_data['dob_years'].mean()
# print(age_data_avg)
# child_data = credit_scoring[credit_scoring['children']>=0]
# child_data = child_data[child_data['children']<6]
# child_data_avg = child_data['children'].mean()
# print(child_data_avg)
# #looking for nulls
# print('children',credit_scoring[credit_scoring['children'].isnull()].count())
# print('days_employed',credit_scoring[credit_scoring['days_employed'].isnull()].count())
# print('dob_years',credit_scoring[credit_scoring['dob_years'].isnull()].count())
# print('education',credit_scoring[credit_scoring['education'].isnull()].count())
# print('education_id',credit_scoring[credit_scoring['education_id'].isnull()].count())
# print('family_status',credit_scoring[credit_scoring['family_status'].isnull()].count())
# print('family_status_id',credit_scoring[credit_scoring['family_status_id'].isnull()].count())
# print('gender',credit_scoring[credit_scoring['gender'].isnull()].count())
# print('income_type',credit_scoring[credit_scoring['income_type'].isnull()].count())
# print('debt',credit_scoring[credit_scoring['debt'].isnull()].count())
# print('total_income',credit_scoring[credit_scoring['total_income'].isnull()].count())
# print('purpose',credit_scoring[credit_scoring['purpose'].isnull()].count())
print(credit_scoring['days_employed'].value_counts())


# ### Conclusion

# No Nan or None values seen so far.
# The age and the children has some incorrect/impossible numbers. We will replace them with plus, or with the average of kids, or even delete those rows.
# Days employee are in minus and as floats, we will turn to int.
# Someones age is 0, will give him the average age.
# The gender has somebody not decided.. we will change him/her to the biggest group (female).
# Is difficult to see all the incomes and days employed, so we will make sure that if there is a zero, a null or a minus we will change them.
# Age average 43.
# The columns that have Nan values are: 'total_income' and 'days_employed'.
# 

# <span style="color:green"> How did you check for None or Nan? .nunique() or .value_counts() don't include NA by default

# ### Data type replacement

# In[21]:


credit_scoring.loc[credit_scoring['gender'] == 'XNA', 'gender'] = 'F'
credit_scoring.loc[credit_scoring['children'] == -1, 'children'] = 1
credit_scoring.loc[credit_scoring['dob_years'] == 0, 'dob_years'] = 43
credit_scoring.drop(credit_scoring[credit_scoring['children'] == 20 ].index , inplace=True)
credit_scoring.loc[credit_scoring['income_type'] == 'unempoyed', 'income_type'] = 'unemployed'

def replacement_days (row):
    days_employed = row['days_employed']
    years_old = row['dob_years']
    days_employed=abs(days_employed)
    years_employed = days_employed/365
    if years_employed > years_old:
        years_employed = years_old-18
        days_employed = years_employed*365
    return int(days_employed)
    

credit_scoring['days_employed'] = credit_scoring['days_employed'].fillna(0.0)
credit_scoring['days_employed'] = credit_scoring.apply(replacement_days, axis=1)
credit_scoring['total_income'] = credit_scoring['total_income'].fillna(0.0)
print(credit_scoring['days_employed'].unique())
credit_scoring['days_employed'] = credit_scoring['days_employed'].fillna(0.0)
print(credit_scoring['days_employed'].unique())
print(credit_scoring['days_employed'].unique())

# print(credit_scoring['children'].unique())
# print(credit_scoring['dob_years'].unique())
# print(credit_scoring['children'].unique())
# print(credit_scoring['total_income'].unique())
# print(credit_scoring['days_employed'].unique())
# print(credit_scoring['income_type'].unique())


# <span style="color:green"> For days_employed you can also use .abs() method :) In general, agree what you've done here. But please take a look at days_employed closer, it's trickier than it seems

# ### Conclusion

# For children column we trate "-1" as 1, for "20" we dropped de rows.
# The days we remained as float, so we turn it to plus and integers. There are impossible values like working 110 years.
# The gender was changed to F where it appear as "XNA".

# ### Processing duplicates

# In[22]:


credit_scoring['education'] = credit_scoring['education'].str.lower()
def replacement_education (row):
    education = row['education']
    if education == 'academic degree':
        return 4
    elif education == 'masters degree':
        return 3
    elif education == 'bachelor degree':
        return 2
    elif education == 'secondary education':
        return 1
    elif education == 'primary education':
        return 0

def replacement_family_status (row):
    family_status = row['family_status']
    if family_status == 'married':
        return 0
    elif family_status == 'civil partnership':
        return 1
    elif family_status == 'widow / widower':
        return 2
    elif family_status == 'divorced':
        return 3
    elif family_status == 'unmarried':
        return 4

credit_scoring['education_id'] = credit_scoring.apply(replacement_education, axis=1)
credit_scoring['family_status_id'] = credit_scoring.apply(replacement_family_status, axis=1)
print(credit_scoring.tail(10))


credit_scoring = credit_scoring.drop_duplicates()
print(credit_scoring.info())


# <span style="color:green"> Can you please explain why you did this? How does it help you to adress the problem of duplicates?

# ### Conclusion

# Is impossible to check for each row if the 'education_id' or the 'family_status_id' ar consistent with the configuration they belong.
# At the end we will drop the duplicates. 21378 entries from 21524.
# 

# ### Lemmatization

# In[23]:


import nltk
from nltk.stem import WordNetLemmatizer
from collections import Counter

wordnet_lemma = WordNetLemmatizer()
words = credit_scoring['purpose'].unique()
lemmas = [wordnet_lemma.lemmatize(w, pos = 'n') for w in words]
counter = Counter(lemmas)
# print(lemmas)
# print(counter)

def replacement_purpose (row):
    purpose_row = row['purpose']
    if 'hous' in purpose_row:
        return 'house'
    elif 'property' in purpose_row:
        return 'house'
    elif 'real estate' in purpose_row:
        return 'house'
    elif 'car' in purpose_row:
        return 'car'
    elif 'educat' in purpose_row:
        return 'education'
    elif 'university' in purpose_row:
        return 'education'
    elif 'wedding' in purpose_row:
        return 'wedding'
    return purpose_row

credit_scoring['purpose'] = credit_scoring.apply(replacement_purpose, axis=1)
print(credit_scoring['purpose'].unique())


# ### Conclusion

# The purpose of a loan was separated in 4 main categories: house, car, education and wedding.

# ### Categorizing Data

# In[24]:


print('The mean of income is: {:.2f}'.format(credit_scoring['total_income'].mean()))
print('The median of income is: {:.2f}'.format(credit_scoring['total_income'].median()))
print('The minimun of income is: {:.2f}'.format(credit_scoring['total_income'].min()))

print(credit_scoring['total_income'].median())

def income_to_group(row):
    income = row['total_income']
    if income <= 100000 :
        return 'poor'
    elif income <= 300000:
        return 'middle_class'
    return 'high_class'
def age_to_group(row):
    age = row['dob_years']
    if age <= 30 :
        return 'young'
    elif age <= 50:
        return 'adult'
    return 'old'
def children_to_group(row):
    child = row['children']
    if child == 0 :
        return 0
    return 1

credit_scoring['income_group'] = credit_scoring.apply(income_to_group, axis=1)
credit_scoring['age_group'] = credit_scoring.apply(age_to_group, axis=1)
credit_scoring['children_group'] = credit_scoring.apply(children_to_group, axis=1)

print(credit_scoring['income_group'].value_counts())
print(credit_scoring['age_group'].value_counts())
print(credit_scoring['children_group'].value_counts())


# ### Conclusion

# As in normal life, we get a Normal distribution, where most of the people are in the middle class, and the others on the wings.
# The children colum will be clasified as with or without children.
# These three were the only columns remained to categorize. The others were already categorize when processing the data.

# <span style="color:green">  Good job on categorization and lemmatization 

# ### Step 3. Answer these questions

# - Is there a relation between having kids and repaying a loan on time?

# In[25]:


kid_table = credit_scoring.groupby('children_group').count()
# print(kid_table['debt'])
debt_table = credit_scoring.groupby('debt').count()
# print(debt_table['children_group'])
children_debt_table = credit_scoring.groupby(['children_group','debt']).size()
print(children_debt_table)
no_kid_no_debt = 13086
no_kid_yes_debt = 1063
yes_kid_no_debt = 6698
yes_kid_yes_debt = 678
no_kid = no_kid_no_debt + no_kid_yes_debt
yes_kid = yes_kid_no_debt + yes_kid_yes_debt
no_debt = no_kid_no_debt + yes_kid_no_debt
yes_debt = no_kid_yes_debt + yes_kid_yes_debt
prob_no_kid_no_debt = no_kid_no_debt/no_kid
prob_no_kid_yes_debt = no_kid_yes_debt/no_kid
prob_yes_kid_no_debt = yes_kid_no_debt/yes_kid
prob_yes_kid_yes_debt = yes_kid_yes_debt/yes_kid

print('The probability of people without children to repay a loan is: {:.2f}'.format(prob_no_kid_no_debt))
print('The probability of people without children to not repay a loan is: {:.2f}'.format(prob_no_kid_yes_debt))
print('The probability of people with children to repay a loan is: {:.2f}'.format(prob_yes_kid_no_debt))
print('The probability of people with children to not repay a loan is: {:.2f}'.format(prob_yes_kid_yes_debt))


# ### Conclusion

# Having children or not, does not have much influence wether people repay the loan, since both group have very similar percentages. We can see that no having children has a very small advantage on repaying a loan o time.

# - Is there a relation between marital status and repaying a loan on time?

# In[26]:


maritage_debt_table = credit_scoring.groupby(['family_status','debt']).size()
print(maritage_debt_table)
civil_no_debt = 3789
civil_yes_debt = 388
divorced_no_debt = 1110
divorced_yes_debt = 85
married_no_debt = 11449
married_yes_debt = 931
unmarried_no_debt = 2539
unmarried_yes_debt = 274
widow_no_debt = 897
widow_yes_debt = 63
civil = civil_no_debt + civil_yes_debt
divorced = divorced_no_debt + divorced_yes_debt
married = married_no_debt + married_yes_debt
unmarried = unmarried_no_debt + unmarried_yes_debt
widow = widow_no_debt + widow_yes_debt
prob_civil_no_debt = civil_no_debt/civil
prob_civil_yes_debt = civil_yes_debt/civil
prob_divorced_no_debt = divorced_no_debt/divorced
prob_divorced_yes_debt = divorced_yes_debt/divorced
prob_married_no_debt = married_no_debt/married
prob_married_yes_debt = married_yes_debt/married
prob_unmarried_no_debt = unmarried_no_debt/unmarried
prob_unmarried_yes_debt = unmarried_yes_debt/unmarried
prob_widow_no_debt = widow_no_debt/widow
prob_widow_yes_debt = widow_yes_debt/widow
print('The probability of people with status of civil partnership to repay a loan is: {:.2f}'.format(prob_civil_no_debt))
print('The probability of people with status of civil to not repay a loan is: {:.2f}'.format(prob_civil_yes_debt))
print('The probability of people with status of divorced to repay a loan is: {:.2f}'.format(prob_divorced_no_debt))
print('The probability of people with status of divorced to not repay a loan is: {:.2f}'.format(prob_divorced_yes_debt))
print('The probability of people with status of married to repay a loan is: {:.2f}'.format(prob_married_no_debt))
print('The probability of people with status of married to not repay a loan is: {:.2f}'.format(prob_married_yes_debt))
print('The probability of people with status of unmarried to repay a loan is: {:.2f}'.format(prob_unmarried_no_debt))
print('The probability of people with status of unmarried to not repay a loan is: {:.2f}'.format(prob_unmarried_yes_debt))
print('The probability of people with status of widow/widower to repay a loan is: {:.2f}'.format(prob_widow_no_debt))
print('The probability of people with status of widow/widower to not repay a loan is: {:.2f}'.format(prob_widow_yes_debt))


# ### Conclusion

# Also here we can see that almost all percentages are prety the same, where repaying the loan is above 90% for each family status. Divorce and widow people had better percentage to repay a loan on time, whether unmarried people had the worst probability of repaying a loan on time.

# - Is there a relation between income level and repaying a loan on time?

# In[27]:


income_group_debt_table = credit_scoring.groupby(['income_group','debt']).size()
print(income_group_debt_table)
high_class_no_debt = 2043
high_class_yes_debt = 174
middle_class_no_debt = 13632
middle_class_yes_debt = 1213
poor_no_debt = 4109
poor_yes_debt = 354
high_class = high_class_no_debt + high_class_yes_debt
middle_class = middle_class_no_debt + middle_class_yes_debt
poor = poor_no_debt + poor_yes_debt
prob_high_class_no_debt = high_class_no_debt/high_class
prob_high_class_yes_debt = high_class_yes_debt/high_class
prob_middle_class_no_debt = middle_class_no_debt/middle_class
prob_middle_class_yes_debt = middle_class_yes_debt/middle_class
prob_poor_no_debt = poor_no_debt/poor
prob_poor_yes_debt = poor_yes_debt/poor

print('The probability of people from high class to repay a loan is: {:.2f}'.format(prob_high_class_no_debt))
print('The probability of people from high class to not repay a loan is: {:.2f}'.format(prob_high_class_yes_debt))
print('The probability of people from middle class to repay a loan is: {:.2f}'.format(prob_middle_class_no_debt))
print('The probability of people from middle class to not repay a loan is: {:.2f}'.format(prob_middle_class_yes_debt))
print('The probability of people from poor class to repay a loan is: {:.2f}'.format(prob_poor_no_debt))
print('The probability of people from poor class to not repay a loan is: {:.2f}'.format(prob_poor_yes_debt))


# ### Conclusion

# Surprisingly, the classes have no difference on repaying a loan on time.

# - How do different loan purposes affect on-time repayment of the loan?

# In[28]:


purpose_debt_table = credit_scoring.groupby(['purpose','debt']).size()
print(purpose_debt_table)
car_no_debt = 3898
car_yes_debt = 401
education_no_debt = 3638
education_yes_debt = 369
house_no_debt = 10024
house_yes_debt = 780
wedding_no_debt = 2156
wedding_yes_debt = 183
car = car_no_debt + car_yes_debt
education = education_no_debt + education_yes_debt
house = house_no_debt + house_yes_debt
wedding = wedding_no_debt + wedding_yes_debt
prob_car_no_debt = car_no_debt/car
prob_car_yes_debt = car_yes_debt/car
prob_education_no_debt = education_no_debt/education
prob_education_yes_debt = education_yes_debt/education
prob_house_no_debt = house_no_debt/house
prob_house_yes_debt = house_yes_debt/house
prob_wedding_no_debt = wedding_no_debt/wedding
prob_wedding_yes_debt = wedding_yes_debt/wedding
print('The probability of people with purpose of buying a car to repay a loan is: {:.2f}'.format(prob_car_no_debt))
print('The probability of people with purpose of buying a car to not repay a loan is: {:.2f}'.format(prob_car_yes_debt))
print('The probability of people with purpose of paying for education to repay a loan is: {:.2f}'.format(prob_education_no_debt))
print('The probability of people with purpose of paying for education to not repay a loan is: {:.2f}'.format(prob_education_yes_debt))
print('The probability of people with purpose of buying a house to repay a loan is: {:.2f}'.format(prob_house_no_debt))
print('The probability of people with purpose of buying a house to not repay a loan is: {:.2f}'.format(prob_house_yes_debt))
print('The probability of people with purpose of paying for a wedding to repay a loan is: {:.2f}'.format(prob_wedding_no_debt))
print('The probability of people with purpose of paying for a wedding to not repay a loan is: {:.2f}'.format(prob_wedding_yes_debt))


# ### Conclusion

# Also here we can see that almost all percentages are prety the same, where repaying the loan is above 91% for each purpose of the loan. People who took a loan in order to by a house had better percentage to repay a loan on time, whether buying a car or paying for educations (usually smaller loans..) had the worst probability of repaying a loan on time.

# <span style="color:green"> This step is nice!

# ### Step 4. General conclusion

# The project consisted in preparing a report for a bank’s loan division. We took data on customers’ credit worthiness that the bank already collected. We first openned it and then had a look at the general information. We then preprocess the data, making sure we could work with it. I classified the data that came from numbers, characters, words and sentences, made sure they make sence and are apropriate for data on customers’ credit worthiness.
# The purpose of this project is to involve the report to be considered when building a credit scoring of a potential customer. A credit scoring is used to evaluate the ability of a potential borrower to repay their loan.
# The general conclusion is that by the data we had, and the checks we made, repaying a loan on time had almost same percentage for each different classifier, what made it difficult to make a good information review. Further we will need to check cross information, or we will need to take other parameters that could help better to have a more clear separation beween people repaying loan on time.

# <span style="color:green"> Your general conclusion should describe the research that you've done: the data you've been working with, its distirbution, main points from previous conclusions and answers to the research questions. :) </span>
# 

# ### Project Readiness Checklist
# 
# Put 'x' in the completed points. Then press Shift + Enter.

# - [x]  file open;
# - [ ]  file examined;
# - [ ]  missing values defined;
# - [ ]  missing values are filled;
# - [ ]  an explanation of which missing value types were detected;
# - [ ]  explanation for the possible causes of missing values;
# - [ ]  an explanation of how the blanks are filled;
# - [ ]  replaced the real data type with an integer;
# - [ ]  an explanation of which method is used to change the data type and why;
# - [ ]  duplicates deleted;
# - [ ]  an explanation of which method is used to find and remove duplicates;
# - [ ]  description of the possible reasons for the appearance of duplicates in the data;
# - [ ]  highlighted lemmas in the values of the loan purpose column;
# - [ ]  the lemmatization process is described;
# - [ ]  data is categorized;
# - [ ]  an explanation of the principle of data categorization;
# - [ ]  an answer to the question "Is there a relation between having kids and repaying a loan on time?";
# - [ ]  an answer to the question " Is there a relation between marital status and repaying a loan on time?";
# - [ ]   an answer to the question " Is there a relation between income level and repaying a loan on time?";
# - [ ]  an answer to the question " How do different loan purposes affect on-time repayment of the loan?"
# - [ ]  conclusions are present on each stage;
# - [ ]  a general conclusion is made.

# In[ ]:




