import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Update Pet Medical History')

# Get the list of pets from the API
pets = requests.get('http://api:4000/p/pets').json()

# Create a dropdown to select a pet based on the pet's id to update the medical history
pet_id = st.selectbox("Select a Pet ID to Update Medical History", [pet['petID'] for pet in pets])
  