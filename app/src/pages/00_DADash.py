import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

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
st.markdown(f'<div class="title">👋 Welcome, {st.session_state.get("first_name", "Data Analyst")}!</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">What would you like to do today?</div>', unsafe_allow_html=True)
st.write("")

if st.button('📦 View Listings & Category Stock', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/01_DA_Listings.py')

if st.button('🚨 Check Late Shipments', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/02_DA_Shipments.py')

if st.button('📈 User Metrics', 
             type='primary',
             use_container_width=True):
    st.switch_page('pages/03_DA_UserMetrics.py')