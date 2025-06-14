#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import pytz


# In[2]:


# Load Excel file
file_path = "GooglePlayStore_Analysis_Top10Apps.xlsx.xlsx"
excel_data = pd.ExcelFile(file_path)

# Load relevant sheet (usually 'googleplaystore')
df = excel_data.parse('googleplaystore')


# In[3]:


# Drop rows with crucial missing values
df = df.dropna(subset=['Category', 'Rating', 'Reviews', 'Installs', 'Size', 'Last Updated'])

# Convert 'Rating' and 'Reviews' to numeric
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')

# Clean 'Installs' and convert to float
df['Installs'] = df['Installs'].str.replace('[+,]', '', regex=True).astype(float)

# Convert 'Size' to MB
def convert_size(size):
    if 'M' in size:
        return float(size.replace('M', ''))
    elif 'k' in size:
        return float(size.replace('k', '')) / 1024
    else:
        return np.nan

df['Size_MB'] = df['Size'].apply(convert_size)

# Convert 'Last Updated' to datetime
df['Last Updated'] = pd.to_datetime(df['Last Updated'], errors='coerce')


# In[4]:


df_filtered = df[
    (df['Rating'] >= 4.0) &
    (df['Size_MB'] >= 10) &
    (df['Last Updated'].dt.month == 1)
]


# In[5]:


top_categories = df_filtered.groupby('Category').agg({
    'Rating': 'mean',
    'Reviews': 'sum',
    'Installs': 'sum'
}).reset_index()

# Get top 10 categories by installs
top_categories = top_categories.sort_values(by='Installs', ascending=False).head(10)


# In[6]:


# Check current IST time
ist = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(ist)

if 15 <= current_time.hour < 17:
    plt.figure(figsize=(14, 6))
    
    x = top_categories['Category']
    ratings = top_categories['Rating']
    reviews = top_categories['Reviews'] / 1e6  # in millions

    bar_width = 0.4
    indices = range(len(x))

    plt.bar([i - bar_width/2 for i in indices], ratings, width=bar_width, label='Average Rating', color='skyblue')
    plt.bar([i + bar_width/2 for i in indices], reviews, width=bar_width, label='Total Reviews (Millions)', color='salmon')

    plt.xlabel('App Category')
    plt.ylabel('Value')
    plt.title('Top 10 App Categories by Installs (Filtered)\nAvg Rating vs Total Reviews')
    plt.xticks(indices, x, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()
else:
    print("⏳ Graph not shown: This chart is only viewable between 3 PM and 5 PM IST.")


# In[ ]:




