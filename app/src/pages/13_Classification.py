import logging
logger = logging.getLogger(__name__)
import streamlit as st
import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

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
    st.write(f"Email: {ta_email}")
    st.write(f"Day: {avail_day}")
    st.write(f"Time: {avail_time}")
    # ----- add in routing functionality