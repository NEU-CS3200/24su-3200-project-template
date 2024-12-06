import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")

SideBarLinks()

st.title("System Admin Home Page")

if st.button("View Help Tickets", type="primary", use_container_width=True):
    st.switch_page("pages/22_View_Tickets.py")

if st.button("View Login Stats", type="primary", use_container_width=True):
    st.switch_page("pages/24_View_Logins.py")

if st.button("Run Query", type="primary", use_container_width=True):
    st.switch_page("pages/23_Run_Query.py")
