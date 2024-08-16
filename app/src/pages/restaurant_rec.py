import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title('Based on your cuisine preferences, here are our recommendations!')

city_name = st.text_input("What city are you traveling to?")

options = {}

if city_name:
    try:
        # Fetch the cuisines based on the city name
        response = requests.get(f'http://api:4000/r/cuisine/{city_name}').json()
        options = response

    except requests.exceptions.RequestException as e:
        st.write(f"An error occurred: {e}")

# Display the selectbox only if options are available
if options:
    option = st.selectbox(
        "Which cuisine would you like to eat?",
        options,
        index=None,
        placeholder="Select cuisine..."
    )
    st.write("You selected:", option)
else:
    if city_name:
        st.write("Please enter a valid city name to see available cuisines.")

if st.button('Find restaurants?', type='primary', use_container_width=True):
    try:
        result = requests.get(f'http://api:4000/r/restaurant_cuisine/{option}/{city_name}').json()
        st.dataframe(result)
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")

# result = requests.get(f'http://api:4000/r/cuisine/{city_name}').json()
# option = st.selectbox(
#      "Which cuisine would you like to eat?",
#     result,
#     index=None,
#     placeholder="Select cuisine...",
#  )
# st.write("You selected:", option)