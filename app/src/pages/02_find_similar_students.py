import logging
import requests
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
from st_aggrid import AgGrid
SideBarLinks()

# add the logo
add_logo("assets/logo.png", height=400)

# set up the page
st.markdown("# Find Your Similar Students")
st.sidebar.header("Find Students with similar interests")




data_2 = requests.get(f'http://api:4000/sp/speciality/').json()
df = pd.json_normalize(data_2)
speciality = st.selectbox("What attributes are you looking for?",options=(df))

try:
    data = requests.get(f'http://api:4000/s/students/{speciality}').json()
    st.dataframe(data)


except:
    st.write('There are no students that match this criteria')