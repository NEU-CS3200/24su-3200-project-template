import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome User, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('See Prices Based on Area', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Area_Price.py')

if st.button('View Previous Price Data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Previous_Data.py')

if st.button("View Future Home Predictions",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Future_Outcomes.py')