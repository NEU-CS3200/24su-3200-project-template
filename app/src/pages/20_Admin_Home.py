import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('System Admin Home Page')

if st.button('View User and Listing Data', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Data_View.py')