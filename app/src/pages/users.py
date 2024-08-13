import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome, {st.session_state['first_name']}.")
st.write('')
st.write('')

if st.button('Plan your next trip',
              type = 'primary',
              use_container_width = True):
   st.switch_page('pages/trip.py')

address = st.columns(1)
with address:
    address = st.input('Address:')