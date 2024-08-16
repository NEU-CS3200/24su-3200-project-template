import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Hi, {st.session_state['first_name']}.")
st.write('Get recommendations based on your desired rating!')
st.write('')
st.write('')

with st.form("Find a restaurant with rating the you would like to visit today:"):
    city_name = st.text_input("What city are you traveling to?")
    rating = st.number_input("Whats the lowest rating you want the restaurant to be? (1-5)", min_value=1, max_value = 5, step=1, format="%d")
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            response = requests.get(f"http://api:4000/r/restaurant_rating/{rating}/{city_name}").json()
            st.dataframe(response)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

with st.form("Find a hotel with the rating you would like to visit today:"):
    city_name = st.text_input("What city are you traveling to?")
    rating = st.number_input("Whats the lowest rating you want the hotel to be? (1-5)", min_value=1, max_value = 5, step=1, format="%d")
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            response = requests.get(f"http://api:4000/h/rating/{city_name}/{rating}").json()
            st.dataframe(response)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}") 

with st.form("Find an attraction with the rating you would like to visit today:"):
    city_name = st.text_input("What city are you traveling to?")
    rating = st.number_input("Whats the lowest rating you want the attraction to be? (1-10)", min_value=1, max_value = 10, step=1, format="%d")
    
    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            response = requests.get(f"http://api:4000/a/rating/{city_name}/{rating}").json()
            st.dataframe(response)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}") 