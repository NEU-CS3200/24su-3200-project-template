import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Adopter, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Pet Data to View Options', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Pet_Data_Viz.py')

if st.button('View Pet Medical History', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Pet_Medical_History.py')

if st.button('View Rescue Agencies Near Me',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/05_Rescue_Agencies.py')