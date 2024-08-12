import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Product Manager, {st.session_state['first_name']}.")
st.write("")
st.write("")
st.write("### What would you like to do today?")

if st.button("View Analytics", type="primary", use_container_width=True):
    st.switch_page("pages/11_Analytics.py")

if st.button("Edit Restaurant Details", type="primary", use_container_width=True):
    st.switch_page("pages/12_Edit_Restaurant.py")
