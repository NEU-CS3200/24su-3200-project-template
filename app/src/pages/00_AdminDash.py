import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()
user_id = st.session_state.get('user_id', 1)

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    max-width: 95%;
}

/* Page title */
.title {
    color: #328E6E;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

/* Section subtitle */
.section-subtitle {
    color: #328E6E;
    font-size: 22px;
    font-weight: 600;
    text-align: center;
    margin-bottom: 10px;
}

/* Buttons*/
div.stButton > button {
    background-color: #328E6E;
    color: #E1EEBC;
    height: 4em;
    width: 100%;
    font-size: 22px;
    font-weight: bold;
    border-radius: 12px;
    border: none;
}

div.stButton > button:hover {
    background-color: #2a7359;
    border-color: #328E6E;
}

/* Center columns properly */
[data-testid="column"] {
    display: flex;
    justify-content: center;
    align-items: center;
}

</style>
""", unsafe_allow_html=True)
st.markdown(f'<div class="title">👋 Welcome, {st.session_state.get("first_name", "Admin")}!</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">What would you like to do today?</div>', unsafe_allow_html=True)
st.write("")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🚨 Report Management"):
        st.switch_page("pages/10_Reports_Management.py")

with col1:
    if st.button("👥 User Management"):
        logger.info("Navigating to User Roles page")
        st.switch_page("pages/10_Admin_User_Tools.py")

with col2:
    if st.button("🧹 Item Cleanup"):
        logger.info("Navigating to Item Cleanup Tools")
        st.switch_page("pages/10_Item_Cleanup.py")

