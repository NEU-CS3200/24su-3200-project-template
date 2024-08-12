import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Fitness Enthusiast, {st.session_state['first_name']}.")
st.write("")
st.write("")
st.write("### What would you like to do today?")

if st.button("Edit Profile", type="primary", use_container_width=True):
    st.switch_page("pages/01_Edit_Profile.py")

if st.button("Generate Recommendations", type="primary", use_container_width=True):
    st.switch_page("pages/02_Generate_Recommendations.py")
