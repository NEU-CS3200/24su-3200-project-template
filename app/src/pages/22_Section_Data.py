import logging
import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

SideBarLinks()

# ----------- this just gets the sections that a given professor is teaching 
st.title('See My Students')
st.write('')
st.write('Feel free to sort by section in the data below')
with st.form("Section Data "):
  prof_email = st.text_input('Email: ')

  submitted = st.form_submit_button('Submit')

st.write('')
if submitted:
    st.write(f"Your Email: {prof_email}")
    try:
        # ---- turn this into a header 
        st.write("Here are the current sections:")
        students_data = requests.get(f'http://api:4000/sec/{prof_email}/students').json()
        st.dataframe(students_data)

    except:
        st.write("Could not connect to the database to get your students, you may not be teaching a section.")
