import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
from datetime import datetime as dt
from streamlit_calendar import calendar
SideBarLinks()

# add the logo
add_logo("assets/logo.png", height=400)

# set up the page
st.markdown("# Find Your Group")
st.sidebar.header("Find Your Group Here")

# Create a scheduling calendar
now = dt.now()
try:
    meetings = st.date_input(label='Schedule Meetings: ',
                value=(dt(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute),
                        dt(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute)),
                key='#date_range',
                help="The start and end date time")
    st.write('Start: ', dts[0], "End: ", dts[1])

except:
    pass
