import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
from datetime import datetime as dt,time
#from streamlit_calendar import calendar

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.title('Update your major')

st.write('Enter your information in the form below:')

with st.form("Update Major"):
    fname = st.text_input('First Name: ')
    lname = st.text_input('Last Name: ')
    email = st.text_input('Email: ')
    major = st.text_input('Updated Major: ')

    # Two submit buttons: one for adding and one for deleting
    submitted = st.form_submit_button('Update')

if submitted:
    data = {}
    data['first_name'] = fname    
    data['last_name'] = lname 
    data['email'] = email 
    st.write("Updating the major for you:", data)

    # Send the put request! 
    response = requests.put(f'http://api:4000/s/students/{fname}/{lname}/{email}/{major}', json=data)

    # Check the response from the server
    if response.status_code == 200:
        st.success('Major updated!')
    elif response.status_code == 404:
        st.error('Student not found!')
    else:
        st.error(f'Failed to update major: {response.status_code}')
