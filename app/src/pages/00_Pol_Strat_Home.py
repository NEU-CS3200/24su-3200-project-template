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

if st.button('Fill Out A Form',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/01_World_Bank_Viz.py')

if st.button('Join A Group and Schedule Meetings',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/02_Map_Demo.py')

student_data = requests.get('http://api:4000/sa/students').json()
try:
  st.dataframe(student_data)
except:
  st.write("Could not connect to db to retrive students!")
