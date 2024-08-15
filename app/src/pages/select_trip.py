# displays all of the users trips
import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Hi, {st.session_state['first_name']}.")
st.write('Here are all your previous trips')
st.write('')
st.write('')

try:
    trip_info = requests.get(f"http://api:4000/t/trip/{st.session_state['id']}").json()
    st.dataframe(trip_info)
except:
    st.write("Error!")

if st.button('Delete old trip?', type='primary', use_container_width=True):
    try:
        result = requests.get(f'http://api:4000/f/price/{flight_budget}').json()
        st.dataframe(result)
        st.write('worked')
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")