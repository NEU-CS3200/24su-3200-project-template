import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Rescue Agencies with Least Adoptions')

st.write('\n\n')
st.write('### Hi Alex, here are the agencies with the least adoptions.')

# Fetching the data from the api
data = {} 
try:
  data = requests.get('http://api:4000/a/petagencies').json()
except:
  st.write("Could not connect to database to retrieve agencies!")

df = pd.DataFrame(data)

# Sorting the data
df_sorted = df.sort_values(by='Total_Adoptions')

st.bar_chart(df_sorted, x="agencyName", y="Total_Adoptions", color="#89CFF0", horizontal=True)
