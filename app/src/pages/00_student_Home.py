import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests


st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Student, {st.session_state['first_name']}.")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Update your major',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_prefrence_form.py')

if st.button('Find students based on specialty',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_find_similar_students.py')

if st.button('Find students on campus',
             type='primary', use_container_width=True):
  st.switch_page('pages/03_find_oc.py')

if st.button('Scheduling and Task List',
             type='primary',use_container_width=True):
  st.switch_page('pages/Scheduler_Tracker.py')

