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
st.header('Input Your Data Below')

# You can access the session state to make a more customized/personalized app experience
st.write(f"### Hi, {st.session_state['first_name']}.")

# create a text entry field
with st.form("Input Your Student Data"):
    f_name = st.text_input("What's your First name?")
    l_name = st.text_input("What's your Last name?")
    email = st.text_input("Enter your NU Email?")
    major = st.text_input("Enter your Major")
    interests = st.text_input("What are you interested in?")
    year = st.selectbox("What year are you",options=(1,2,3,4,5))
    dorm = st.selectbox("Do you live on or Off Campus?",options=('True','False'))

    # insert into availiblity table
    time = st.selectbox(label = 'What Time Of Day?',options=('Morning','Afternoon','Night'))
    days = st.multiselect("What Days Can you Meet?",
                          options=('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'))

    submitted = st.form_submit_button("Submit")

    if submitted:
        data = {}
        data['f_name'] = f_name
        data['l_name'] = l_name
        data['email'] = email
        data['major'] = major
        data['interests'] = interests
        data['year'] = year
        data['dorm'] = dorm

        response = requests.post('http://api:4000/s/students',json=data)

        if response.status_code == 200:
            st.write("Form Submitted Sucessfully")
        else:
            st.write("Failed to Submit")



