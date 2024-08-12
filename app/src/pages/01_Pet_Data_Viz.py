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
st.header('Adoptable Pet Data')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}!")
st.write('This is a list of pets that are alive and available for adoption.')

try:
    # Get the pets from the database
    pets = requests.get('http://localhost:4000/p/pets').json()

    # Filter the pets where adoption_status = 0 and is_alive = 1
    pets = [pet for pet in pets if pet['adoption_status'] == 0 and pet['is_alive'] == 1]

    st.dataframe(pets)
except requests.exceptions.RequestException as e:
    st.write('Could not connect to database to retrieve pet data')
    st.write(str(e))

    
