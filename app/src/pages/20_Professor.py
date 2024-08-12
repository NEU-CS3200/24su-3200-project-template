import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

st.title(f"Welcome Databasing Professor, {st.session_state['first_name']}.")
st.write("")
st.write("")
st.write("### What would you like to do today?")

if st.button("Manage Groups", type="primary", use_container_width=True):
    st.switch_page("pages/21_Manage_Groups.py")

if st.button("Generate Group Recommendations", type="primary", use_container_width=True):
    st.switch_page("pages/22_Group_Recommendations.py")
