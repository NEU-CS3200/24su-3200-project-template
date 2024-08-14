import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome TA, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Find students with my availability', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Prediction.py')

if st.button('Find students with my specialty', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_API_Test.py')

if st.button("Update my information",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Classification.py')
