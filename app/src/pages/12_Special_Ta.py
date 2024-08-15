import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.title('My Specialty')
st.write('**Find students in your section that need help with your specialty!**')
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
        # ----- eventually want to add a button to go to update information page 
        st.write("These are your listed specialties:")
        ta_data = requests.get(f'http://api:4000/t/ta/{ta_fname}/{ta_lname}/{ta_email}/special').json()
        st.dataframe(ta_data)
    except:
        st.write("Could not connect to the database to retrieve TA id! Make sure there are no typos in the form.")
    try: 
        st.write("These students may need your help:")
        help_data = requests.get(f'http://api:4000/t/ta/{ta_fname}/{ta_lname}/{ta_email}/students').json()
        st.dataframe(help_data)
    except:
        st.write("Could not connect to the database to retrieve TA id! Make sure there are no typos in the form.")

