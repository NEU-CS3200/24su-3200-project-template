import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

st.title('Find students with my availability')
st.write('Enter your information in the form below:')

with st.form("Find students with my availabilty"):
  ta_fname = st.text_input('First Name: ')
  ta_lname = st.text_input('Last Name: ')
  ta_email = st.text_input('Email: ')

  submitted = st.form_submit_button('Submit')

if submitted:
    st.write(f"First Name: {ta_fname}")
    st.write(f"Last Name: {ta_lname}")
    st.write(f"Email: {ta_email}")
    # --- need to get this to return the specfic TA's availability 
    try:
        taId_data = requests.get(f'http://api:4000/t/ta/{ta_fname}/{ta_lname}/{ta_email}').json()
        st.dataframe(taId_data)
    except:
        st.write("Could not connect to the database to retrieve TA ID! Make sure there are no typos in the form.")
