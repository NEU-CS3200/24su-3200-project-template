import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Find students with my availability')

with st.form("Find students with my availabilty"):
  ta_fname = st.text_input('First Name: ')
  ta_lname = st.text_input('Last Name: ')
  ta_email = st.text_input('Email: ')

  submitted = st.form_submit_button('Submit')

if submitted:
  st.write(f"First Name: {ta_fname}")
  st.write(f"Last Name: {ta_lname}")
  st.write(f"Email: {ta_email}")

  # --- still need to connect id to api!
ta_data = requests.get('http://api:4000/t/ta/1').json()
try:
  st.dataframe(ta_data)
except:
  st.write("Could not connect to db to retrive ta data!")