import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Marcus')} \U0001f3b5")
st.write("### Label Head Dashboard — What would you like to do today?")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("\U0001f4b8 Royalty Splits")
    st.write("Add collaborators, adjust split percentages, and manage payout profiles for your releases.")
    if st.button("Manage Royalty Splits", type="primary", use_container_width=True):
        logger.info("Navigating to Royalty Splits")
        st.switch_page("pages/31_Royalty_Splits.py")

with col2:
    st.subheader("\U0001f4c2 Asset Tracker")
    st.write("Monitor audio files, artwork, and credits across your roster. Track upload status in one place.")
    if st.button("Track Assets", type="primary", use_container_width=True):
        logger.info("Navigating to Asset Tracker")
        st.switch_page("pages/32_Asset_Tracker.py")

with col3:
    st.subheader("\U0001f4c0 Release Overview")
    st.write("View the complete picture for any release — all payout profiles and assets side by side.")
    if st.button("View Release Overview", type="primary", use_container_width=True):
        logger.info("Navigating to Release Overview")
        st.switch_page("pages/33_Release_Overview.py")
