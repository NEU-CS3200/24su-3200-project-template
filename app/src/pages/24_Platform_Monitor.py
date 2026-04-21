import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

BASE = "http://web-api:4000"

st.title("Platform Activity Monitor")

# Processing Releases (Rigby-2)
st.subheader("Releases Currently Processing")
st.caption("Releases in 'Processing' status that may need attention.")

try:
    resp = requests.get(f"{BASE}/releases", params={"status": "Processing"})
    if resp.status_code == 200:
        releases = resp.json()
        if releases:
            st.dataframe(pd.DataFrame(releases), use_container_width=True, hide_index=True)
        else:
            st.success("No releases currently stuck in processing.")
    else:
        st.error("Failed to fetch processing releases.")
except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to API: {e}")

st.divider()

# Most Active Artists (Rigby-5)
st.subheader("Most Active Artists")
st.caption("Artists ranked by total number of releases submitted.")

try:
    resp = requests.get(f"{BASE}/releases/rankings")
    if resp.status_code == 200:
        rankings = resp.json()
        if rankings:
            df = pd.DataFrame(rankings)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No ranking data available.")
    else:
        st.error("Failed to fetch artist rankings.")
except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to API: {e}")

st.divider()

# Roster Status Overview
st.subheader("Full Roster Status")
st.caption("All releases across the platform with their current status and artist.")

try:
    resp = requests.get(f"{BASE}/releases/roster-status")
    if resp.status_code == 200:
        roster = resp.json()
        if roster:
            st.dataframe(pd.DataFrame(roster), use_container_width=True, hide_index=True)
        else:
            st.info("No roster data available.")
    else:
        st.error("Failed to fetch roster status.")
except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to API: {e}")

