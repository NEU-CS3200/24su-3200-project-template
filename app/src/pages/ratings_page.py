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
st.write('Here are some recommendations')
st.write('')
st.write('')

with st.form("Choose the restaurant rating you would like to visit today:"):
    rating = st.number_input("List restaurant rating", min_value=1, step=1, format="%d")

    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            response = requests.post(f"http://api:4000/t/restaurant_rating/{rating}").json()
            st.dataframe(response)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")
