#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import pytz


# In[2]:


df = pd.read_csv("googleplaystore.csv")


# In[3]:


np.random.seed(42)
df['sentiment_subjectivity'] = np.random.rand(len(df))


# In[4]:


# Clean size column
df['Size'] = df['Size'].replace('Varies with device', np.nan)
df['Size'] = df['Size'].str.replace('M', '', regex=False).str.replace('k', '', regex=False)
df['Size'] = pd.to_numeric(df['Size'], errors='coerce')


# In[5]:


# Clean installs column
df['Installs'] = df['Installs'].str.replace(',', '').str.replace('+', '', regex=False)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce')


# In[6]:


# Convert Reviews and Rating to numeric
df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')


# In[7]:


# Normalize category names
df['Category'] = df['Category'].str.strip().str.lower()


# In[8]:


# Define target categories
target_categories = ['game', 'beauty', 'business', 'comics', 'communication',
                     'dating', 'entertainment', 'social', 'event']


# In[9]:


# Apply filters
filtered_df = df[
    (df['Rating'] > 3.5) &
    (df['Category'].isin(target_categories)) &
    (df['Reviews'] > 500) &
    (~df['App'].str.contains('s', case=False, na=False)) &
    (df['sentiment_subjectivity'] > 0.5) &
    (df['Installs'] > 50000)
].copy()


# In[10]:


# Translations for display
translation_map = {
    'beauty': 'सौंदर्य',       # Hindi
    'business': 'வணிகம்',     # Tamil
    'dating': 'Verabredung'   # German
}

filtered_df['Translated_Category'] = filtered_df['Category'].replace(translation_map)


# In[11]:


from datetime import datetime
import pytz

# Get current time in IST
ist = pytz.timezone('Asia/Kolkata')
now = datetime.now(ist)
current_hour = now.hour


# In[12]:


import plotly.express as px

# Check if current time is between 5 PM and 7 PM IST
if 17 <= current_hour < 19 and not filtered_df.empty:
    # Assign pink to game category, others get lightblue
    color_map = {cat: 'lightblue' for cat in filtered_df['Translated_Category'].unique()}
    if 'game' in filtered_df['Category'].values:
        color_map['game'] = 'pink'

    # Create bubble chart
    fig = px.scatter(
        filtered_df,
        x='Size',
        y='Rating',
        size='Installs',
        color='Translated_Category',
        hover_name='App',
        size_max=60,
        title='App Size vs Rating (Bubble Chart)',
        color_discrete_map=color_map
    )
    fig.update_layout(
        xaxis_title='App Size (MB)',
        yaxis_title='Average Rating'
    )
    fig.show()

else:
    print(f"⛔ The chart is only visible between 5 PM and 7 PM IST.\n🕒 Current IST time: {now.strftime('%I:%M %p')}")


# In[ ]:




