import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('# View Price of Homes Based on Area')

url = 'http://localhost:4000/l/tenMostExpensive'
try:
    response = requests.get(url)
    if response.status_code == 200:
        all_data = response.json()
        st.write("Successfully connected to the API.")
        st.write("ten most expensive listings:")
        st.dataframe(all_data)  # Displaying all user data in a dataframe
    else:
        st.error(f"Failed to retrieve all users. Status code: {response.status_code}")
        st.text("Response:" + response.text)
except requests.exceptions.RequestException as e:
    st.error("An error occurred while trying to connect to the API to fetch all users:")
    st.text(str(e))

