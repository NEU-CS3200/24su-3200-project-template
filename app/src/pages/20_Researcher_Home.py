import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Researcher Home Page')

if st.button('View Adoption Sites with Least Adoptions', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Least_Adoptions.py')

if st.button('View Pets with Least Interest', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Least_Interest.py')

if st.button('View Most Surrendered Pets', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/23_Most_Surrendered.py')