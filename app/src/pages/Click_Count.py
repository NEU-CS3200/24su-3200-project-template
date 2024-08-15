import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("Click Counter")


# Fetch the data from the route
url = "http://api:4000/hc/hotel_clicks"
response = requests.get(url)
response.raise_for_status()
data_json = response.json()
data = pd.DataFrame(data_json)

# Check if the required columns are present
if 'name' in data.columns and 'total_clicks' in data.columns:
    # Streamlit app
    st.title('Top 5 Hotel Clicks Data')
    
    # Display a bar chart
    st.bar_chart(data.set_index('name')['total_clicks'])
else:
    st.error("Expected columns 'name' and 'total_clicks' not found in the data.")


# Fetch the data from the route
url = "http://api:4000/rc/restaurant_clicks"
response = requests.get(url)
response.raise_for_status()
data_json = response.json()
data = pd.DataFrame(data_json)

# Check if the required columns are present
if 'name' in data.columns and 'total_clicks' in data.columns:
    # Streamlit app
    st.title('Top 5 Restaurant Clicks Data')
    
    # Display a bar chart
    st.bar_chart(data.set_index('name')['total_clicks'])
else:
    st.error("Expected columns 'name' and 'total_clicks' not found in the data.")


# Fetch the data from the route
url = "http://api:4000/ac/attraction_clicks"
response = requests.get(url)
response.raise_for_status()
data_json = response.json()
data = pd.DataFrame(data_json)

# Check if the required columns are present
if 'name' in data.columns and 'total_clicks' in data.columns:
    # Streamlit app
    st.title('Top 5 Attraction Clicks Data')
    
    # Display a bar chart
    st.bar_chart(data.set_index('name')['total_clicks'])
else:
    st.error("Expected columns 'name' and 'total_clicks' not found in the data.")



# Creating tabs for each bar graph
tab1, tab2, tab3 = st.tabs(["Hotels", "Restaurants", "Attractions"])
data = np.random.randn(10, 1)

tab1.subheader("Top 5 hotels with the most clicks")
tab1.line_chart(data)

tab2.subheader("Top 5 restaurants with the most clicks")
tab2.write(data)


tab3.subheader("Top 5 attractions with the most clicks")
tab3.write(data)