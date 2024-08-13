import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Rescue Agency Manager, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Update Pet Medical History', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Manager_Med_His_View.py')

if st.button('Put up a Pet for Adoption', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_Manager_Adoption_Add.py')

if st.button("View Status of Pending Adoptions",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Manager_Adoption_View.py')