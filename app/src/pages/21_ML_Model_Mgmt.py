import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Update Page')

st.write('## Update Students and Groups')
st.write('Use the forms below to update groups and assign students to groups.')

# Step 1: Enter Professor ID to fetch relevant sections
professor_id = st.text_input('Enter Professor ID:')
