import logging
import requests
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks

SideBarLinks()

# add the logo
add_logo("assets/logo.png", height=400)

# set up the page
st.markdown("# Find Your Similar Students")
st.sidebar.header("Find Students with similar interests")
try:
    student_data = requests.get(f'http://api:4000/s/students/').json()
    st.dataframe(student_data)
except:
    st.write("Doesnt work")

st.selectbox("what attributes should your teammates have",options=('C++','Java'))
