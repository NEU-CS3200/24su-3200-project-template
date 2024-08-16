import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import numpy as np
import requests
from modules.nav import SideBarLinks

SideBarLinks()

st.title("Find students on campus")
st.write('')
st.write('**Let us help you find classmates in your section who are on-campus!**')
st.write('Enter your information in the form below:')
with st.form("ON CAMPUS"):
  email = st.text_input('Email: ')

  submitted = st.form_submit_button('Submit')

if submitted:
    st.write(f"Email: {email}")
    # --- need to get this to return the student id to the get this sections
    try:
        # ---- turn this into a header 
        st.write("Here are students in your section that live on-campus:")
        data = requests.get(f'http://api:4000/s/students/{email}/on-campus').json()
        st.dataframe(data)
    except:
        st.write("Could not connect to the database to retrieve student id! Make sure there are no typos in the form.")