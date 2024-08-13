import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests
import matplotlib.pyplot as plt

SideBarLinks()

st.write("# View All Adoption Data")
adoption_data = requests.get('http://api:4000/adp/adoptions').json()
df = pd.DataFrame(adoption_data)
df = df[['name', 'petID', 'firstName', 'lastName', 'adopterID', 'email', 'phone', 'adoption_date',\
        'adoptionID', 'adoptionStatus']]
df.rename(columns={'name': 'Pet Name'}, inplace=True)

st.write("### Adoption Status Tracker")
# Graphical Representation of Adoption Status
adoption_status = df['adoptionStatus'].value_counts()

# Set colors
colors = ['indianred', 'lightgreen', 'gold']

plt.figure(figsize=(8, 4)) 
plt.bar(adoption_status.index, adoption_status.values, color=colors)
plt.ylabel('Count')
plt.xticks(rotation='horizontal')

st.pyplot(plt)

# Displaying the chart after the graph
st.write("### Chart of all Adoption Data")
st.write(df)