import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import os
import requests


# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.write("# View All Of Your Current Properties")

# Base URL for user data
base_url = 'http://localhost:4000/u/users'

# Display all users
database_name = os.getenv('DB_NAME')  

url = 'http://localhost:4000/r/realtors'
realtor_id = st.text("Bob Smith, Here are Your Listings")

try:
    specific_url = f"{url}/1"
    response = requests.get(specific_url)
    if response.status_code == 200:
        all_data = response.json()
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all users. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))


listing_id = st.text_input("Enter Listings ID to fetch specific listings details", "")
url = 'http://localhost:4000/l/listings'

# Conditionally make API request based on user input for specific user details
if listing_id:
    specific_url = f"{url}/{listing_id}"
    try:
        response = requests.get(specific_url)
        if response.status_code == 200:
            user_data = response.json()
            st.dataframe(user_data)  # Displaying specific user data in JSON format for clarity
        else:
            st.error(f"Failed to retrieve data for listing ID {listing_id}. Status code: {response.status_code}")
            st.text("Response:" + response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while trying to connect to the API to fetch listing ID {listing_id}:")
        st.text(str(e))
