import logging
import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

SideBarLinks()

# ----------- this just gets the sections that a given professor is teaching 
st.title('See Student Submissions')
st.write('')
st.write('View Student Submissions Below')
with st.form("Submission Data "):
  prof_id = st.text_input('ID: ')

  submitted = st.form_submit_button('Submit')

st.write('')
if submitted:
    st.write(f"Your ID: {prof_id}")
    try:
        # Fetch student submissions from the API
        st.write("Here are the current submissions:")
        submissions_data = requests.get(f'http://api:4000/sub/professors/{prof_id}/submissions').json()
        st.dataframe(pd.DataFrame(submissions_data))

    except Exception as e:
        st.write(f"Could not connect to the database to get student submissions. Error: {str(e)}")


