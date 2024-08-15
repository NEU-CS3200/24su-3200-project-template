import logging
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title(f"Welcome, Professor {st.session_state.get('first_name', 'Professor')}!")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('Update student groups',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_ML_Model_Mgmt.py')
if st.button('See my students',
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Section_Data.py')


