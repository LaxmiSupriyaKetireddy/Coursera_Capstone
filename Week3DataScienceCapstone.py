
# coding: utf-8

# ### Data Science Capstone Week 3

# In[2]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

#!conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

get_ipython().system(u"conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab")
import folium # map rendering library

print('Libraries imported.')


# #### Install the Beautiful soap and requests for Web scraping

# In[3]:


get_ipython().system(u'pip install BeautifulSoup4')
get_ipython().system(u'pip install requests')


# In[4]:


from bs4 import BeautifulSoup
#from tabulate import tabulate
import urllib.request
import csv


# #### Taking the html from the wikipedia page. Then create a beautiful_soup object

# In[5]:


data = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M")
beautiful_soup = BeautifulSoup(data.text, "html.parser")


# In[6]:


print(beautiful_soup)


# In[7]:


### filtering out the tables 


# In[8]:


table = beautiful_soup.find("table", {"class": "wikitable sortable"}).tbody
print(table)


# In[11]:


rows = table.find_all("tr")
print("rows are:", rows)


# In[12]:


columns = [v.text.replace("\n", "") for v in rows[0].find_all("th")]
print("columns are:", columns)


# In[15]:


df = pd.DataFrame(columns=columns)
for i in range(1, len(rows)):
    tds = rows[i].find_all("td")
    
    if len(tds) == 3:
        values = [tds[0].text, tds[1].text, tds[2].text.replace("\n", "")]
    
    else:
        values = [td.text for td in tds]
    
    df = df.append(pd.Series(values, index = columns), ignore_index = True)
    
    


# #### Reading the dataset into the data frame

# In[16]:


canada_df = pd.DataFrame(data = df,columns = columns)
canada_df.head()


# #### Filtering out the Borough which are not assigned. Ignore cells with a borough that is Not assigned

# In[17]:


canada_final = canada_df[canada_df["Borough"] != "Not assigned"]
canada_final


# In[18]:


canada_final.loc[canada_final["Neighbourhood"]== "Not assigned"]


# #### More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma as shown in row 11 in the above table

# In[23]:


df1 = canada_final.groupby(["Postcode"]).count()
df1


# In[25]:


canada_group = canada_final.groupby(["Postcode", "Borough"])["Neighbourhood"].apply(", ".join).reset_index()
canada_group


# #### If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough. So for the 9th cell in the table on the Wikipedia page, the value of the Borough and the Neighborhood columns will be Queen's Park.

# In[26]:


canada_final[canada_final["Neighbourhood"]== "Not assigned"]


# In[27]:


canada_final.replace("Not assigned", "Queen's Park", inplace=True) 


# In[28]:


canada_final[canada_final["Borough"]== "Queen's Park"]


# #### Value counts

# In[29]:


canada_final["Borough"].value_counts()


# In[30]:


canada_final["Neighbourhood"].value_counts()


# ### Statistics of the dataframe

# In[33]:


canada_final.describe()


# ### Initial checks of the dataframe

# In[34]:


def DF_initial_observations(df):
    '''Gives basic details of columns in a dataframe : Data types, distinct values, NAs and sample'''
    if isinstance(df, pd.DataFrame):
        total_na=0
        for i in range(len(df.columns)):        
            total_na+= df.isna().sum()[i]
        print('Dimensions : %d rows, %d columns' % (df.shape[0],df.shape[1]))
        print("Total NA values : %d" % (total_na))
        print('%38s %10s     %10s %10s %15s' % ('Column name', ' Data Type', '# Distinct', ' NA values', ' Sample value'))
        for i in range(len(df.columns)):
            col_name = df.columns[i]
            sampl = df[col_name].sample(1)
            sampl.apply(pd.Categorical)
            sampl_p = str(sampl.iloc[0,])
            print('%38s %10s :   %10d  %10d %15s' % (df.columns[i],df.dtypes[i],df.nunique()[i],df.isna().sum()[i], sampl_p))
    else:
        print('Expected a DataFrame but got a %15s ' % (type(data)))


# In[35]:


DF_initial_observations(canada_final)


# ### Shape of the dataframe

# In[37]:


canada_final.shape

