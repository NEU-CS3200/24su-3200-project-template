import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Employer, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('View Position Openings', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Position_Openings.py')

if st.button('Search Students', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_Student_Search.py')

if st.button("View Applications",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Application_Review.py')

if st.button('Create Position Opening', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Position_Opening_Creation.py')

if st.button('Create Help Tickets', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Create_Ticket.py')