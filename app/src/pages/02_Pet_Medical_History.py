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
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Pet Medical History')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# Import the petID you want to view the medical history for
pet_id = st.number_input("Import the petID of the pet you would like the medical history of", step=1)

# Show the medical history for the selected pet
if st.button('Submit'):
    # Send GET request to API
    response = requests.get(f'http://api:4000/m/med/{pet_id}')

    # Check if the response is successful
    if response.status_code == 200:
        medical_history = response.json()

        # Display the medical history in a table
        st.write(pd.DataFrame(medical_history))
    else:
        st.error('Failed to fetch medical history.')
