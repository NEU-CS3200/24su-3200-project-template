import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('# View Price of Homes Based on Area')

listing_state = st.text_input("Enter Listings state to fetch specific listings details", "")

url = 'http://localhost:4000/l/tenLeastExpensive'

# Conditionally make API request based on user input for specific user details
if listing_state:
    specific_url = f"{url}/{listing_state}"
    try:
        response = requests.get(specific_url)
        if response.status_code == 200:
            user_data = response.json()
            st.write("Successfully fetched data listing state:")
            st.dataframe(user_data)  # Displaying specific user data in JSON format for clarity
        else:
            st.error(f"Failed to retrieve data for listing ID {listing_state}. Status code: {response.status_code}")
            st.text("Response:" + response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while trying to connect to the API to fetch listing ID {listing_state}:")
        st.text(str(e))

url = 'http://localhost:4000/a/areasname'
listing_area = st.text_input("Enter Listings area to fetch specific area details", "")
# Conditionally make API request based on user input for specific area
if listing_area:
    specific_url = f"{url}/{listing_area}"
    try:
        response = requests.get(specific_url)
        if response.status_code == 200:
            user_data = response.json()
            st.write("Successfully fetched data listing area:")
            st.dataframe(user_data)  # Displaying specific user data in JSON format for clarity
        else:
            st.error(f"Failed to retrieve data for listing ID {listing_area}. Status code: {response.status_code}")
            st.text("Response:" + response.text)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while trying to connect to the API to fetch listing ID {listing_state}:")
        st.text(str(e))

url = 'http://localhost:4000/a/areas'
# Conditionally make API request based on user input for specific area
try:
    response = requests.get(url)
    if response.status_code == 200:
        user_data = response.json()
        st.write("Successfully fetched data listing area:")
        st.dataframe(user_data)  # Displaying specific user data in JSON format for clarity
    else:
        st.error(f"Failed to retrieve data for listing ID {listing_area}. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error(f"An error occurred while trying to connect to the API to fetch listing ID {listing_state}:")
    st.text(str(e))