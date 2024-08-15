import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
import pandas as pd
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

# Streamlit app
st.title('Hotel Clicks Data')

# Display a bar chart
st.bar_chart(data, x="name", y="hotel_clicks", color="site", stack=False)
