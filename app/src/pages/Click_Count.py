import logging
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Setup logging
logger = logging.getLogger(__name__)

# Setup Streamlit
SideBarLinks()
st.write("Click Counter")

# Fetch and process Hotel Clicks data
url = "http://api:4000/hc/hotel_clicks"
response = requests.get(url)
response.raise_for_status()
data_json = response.json()
data = pd.DataFrame(data_json)

if 'name' in data.columns and 'total_clicks' in data.columns:
    data_sorted = data.sort_values(by='total_clicks', ascending=False)
else:
    st.error("Expected columns 'name' and 'total_clicks' not found in the data.")
    data_sorted = pd.DataFrame()  

# Fetch and process Restaurant Clicks data
url = "http://api:4000/rc/restaurant_clicks"
response = requests.get(url)
response.raise_for_status()
data_json = response.json()
data = pd.DataFrame(data_json)

if 'name' in data.columns and 'total_clicks' in data.columns:
    data_sorted_restaurants = data.sort_values(by='total_clicks', ascending=False)
else:
    st.error("Expected columns 'name' and 'total_clicks' not found in the data.")
    data_sorted_restaurants = pd.DataFrame()  

# Fetch and process Attraction Clicks data
url = "http://api:4000/ac/attraction_clicks"
response = requests.get(url)
response.raise_for_status()
data_json = response.json()
data = pd.DataFrame(data_json)

if 'name' in data.columns and 'total_clicks' in data.columns:
    data_sorted_attractions = data.sort_values(by='total_clicks', ascending=False)
else:
    st.error("Expected columns 'name' and 'total_clicks' not found in the data.")
    data_sorted_attractions = pd.DataFrame()  

# Creating tabs for each bar graph
tab1, tab2, tab3 = st.tabs(["Hotels", "Restaurants", "Attractions"])

with tab1:
    st.header("Top 5 Hotel Clicks")
    if not data_sorted.empty:
        fig = px.bar(data_sorted.head(5), x='name', y='total_clicks', title="Top 5 Hotel Clicks",
                     labels={'name': 'Hotel Name', 'total_clicks': 'Total Clicks'})
        st.plotly_chart(fig)

with tab2:
    st.header("Top 5 Restaurant Clicks")
    if not data_sorted_restaurants.empty:
        fig = px.bar(data_sorted_restaurants.head(5), x='name', y='total_clicks', title="Top 5 Restaurant Clicks",
                     labels={'name': 'Restaurant Name', 'total_clicks': 'Total Clicks'})
        st.plotly_chart(fig)

with tab3:
    st.header("Top 5 Attraction Clicks")
    if not data_sorted_attractions.empty:
        fig = px.bar(data_sorted_attractions.head(5), x='name', y='total_clicks', title="Top 5 Attraction Clicks",
                     labels={'name': 'Attraction Name', 'total_clicks': 'Total Clicks'})
        st.plotly_chart(fig)
