import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
import os
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('App Administration Page')

listing_id = st.text_input("Enter Listings ID to fetch specific listings details", "")

database_name = os.getenv('DB_NAME')  

url = 'http://localhost:4000/l/listings'

# Conditionally make API request based on user input for specific user details
if listing_id:
    specific_url = f"{url}/{listing_id}"
    try:
        response = requests.get(specific_url)
        if response.status_code == 200:
            user_data = response.json()
            st.write("Successfully fetched data listing ID:")
            df = pd.DataFrame(user_data)
            df
        else:
            st.error(f"Failed to retrieve data for listing ID {listing_id}. Status code: {response.status_code}")
            st.text("Response:" + response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while trying to connect to the API to fetch listing ID {listing_id}:")
        st.text(str(e))


url = 'http://localhost:4000/u/users'

try:
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        st.write("Successfully fetched User Data")
        df = pd.DataFrame(user_data)
        df
    else:
        st.error(f"Failed to retrieve data for listing ID {listing_id}. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while trying to connect to the API to fetch listing ID {listing_id}:")
    st.text(str(e))