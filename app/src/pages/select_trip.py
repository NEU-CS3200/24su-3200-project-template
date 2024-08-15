# displays all of the users trips
import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Hi, {st.session_state['first_name']}.")
st.write('Here are all your previous trips')
st.write('')
st.write('')

logger.info(f"id = {st.session_state['id']}")

try:
    trips = requests.get(f"http://api:4000/t/trip/{st.session_state['id']}").json()
    st.dataframe(trips)
except:
    st.write("Error!")