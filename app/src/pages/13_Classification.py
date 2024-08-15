import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests

SideBarLinks()

st.title('Update your information')

st.subheader('Availability')
with st.form("Add new availability time slot"):
  ta_email = st.text_input('Email: ')
  avail_day = st.text_input('Day: ')
  # ----- eventually hopefully this is a dropdown
  avail_time = st.text_input('Time (Morning, Afternoon, or Night): ')

  submitted = st.form_submit_button('Submit')

if submitted:
    data = {}
    data['time_id'] = avail_time
    data['day_id'] = avail_day
    st.write(data)

    requests.post('http://api:4000/a/availability', json=data)



st.subheader('Specialty')
with st.form("Update specialty"):
  ta_email = st.text_input('Email: ')
  ta_special = st.text_input('Updated specialty description: ')

  submitted = st.form_submit_button('Submit')

if submitted:
    st.write(f"Email: {ta_email}")
    st.write(f"Updated specialty description: {ta_special}")
    # ----- add in routing API functionality