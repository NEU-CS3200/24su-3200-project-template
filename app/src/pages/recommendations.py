import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title('Based on your preferences, here are our recommendations!')

if st.button('Find your flight!', type='primary', use_container_width=True):
    try:
        result = requests.get(f'http://api:4000/f/flight/{flight_budget}').json()
        st.dataframe(result)
        st.write('worked')
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

if st.button('Find your hotel!', type='primary', use_container_width=True):
    try:
        result = requests.get(f'http://api:4000/h/hotel/{city_name}').json()
        st.dataframe(result)
        st.write('worked')
    except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please input a city name to find a hotel.")

if st.button('Find your attraction!', type='primary', use_container_width=True):
    try:
            result = requests.get(f'http://api:4000/a/attraction/{city_name}').json()
            st.dataframe(result)
            st.write('worked')
    except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please input a city name to find an attraction.")