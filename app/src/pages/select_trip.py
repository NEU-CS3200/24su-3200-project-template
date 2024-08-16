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
    
    if not trip_info:
        st.write("You have no past trips.")
    else:
        st.dataframe(trip_info)
except:
    st.write("Error!")

# trip_col = st.columns(1)
# with trip_col[0]:
#     trip = st.text_input('Trip name of trip to delete:')

#delete trip based on trip name

result = requests.get(f'http://api:4000/t/trip_name/{st.session_state["id"]}').json()
option = st.selectbox(
     "Which trip would you like to delete?",
    result,
    index=None,
    placeholder="Select trip...",
 )
st.write("You selected:", option)

if st.button('Delete old trip?', type='primary', use_container_width=True):
    try:
        result = requests.delete(f'http://api:4000/t/trip/{option}')
        st.write("Successfully deleted!")
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")