import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Rescue Agencies with Least Adoptions')

st.write('\n\n')
st.write('### Hi Alex, here are the agencies with the least adoptions.')

# Fetching the data from the api
data = {} 
try:
  data = requests.get('http://api:4000/a/agencies').json()
except:
  st.write("Could not connect to database to retrieve agencies!")

st.dataframe(data)
