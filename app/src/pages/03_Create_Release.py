import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests
import time

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Create a Release")

with st.container(border=True):
    st.subheader("Release Details")
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Release Title", max_chars=100)
        release_type = st.selectbox("Release Type", options=["Single", "Album", "EP"])
    with col2:
        release_date = st.date_input("Release Date", min_value=st.session_state.get('today', '2024-01-01'))

st.subheader("Track List")
with st.expander("Add Track #1"):
    t_title = st.text_input("Track Title", max_chars=100)
    t_genre = st.text_input("Track Genre", max_chars=100)
    t_isrc = st.text_input("Track ISRC", max_chars=100)

if st.button("Publish Release", type="primary", use_container_width=True):
    if not title or not t_title:
        st.error("Please provide both a Release Title and at least one Track Title.")
    else:
        release_data = {
        "title": title,
        "type": release_type,
        "release_date": release_date.strftime('%Y-%m-%d'),
        "tracks": [
            {
                "title": t_title,
                "genre": t_genre,
                "isrc_code": t_isrc
            }
        ],
        "assets": []
        }
        try:
            response = requests.post(f"http://web-api:4000/releases/{st.session_state['artist_id']}", json=release_data)
            if response.status_code == 201:
                st.success("Release created successfully!")
                st.session_state['new_release_id'] = response.json().get('rel_id')
                time.sleep(1)
                st.switch_page("pages/01_Artist_Library.py")
            else:
                st.error(f"Failed to create release: {response.text}")
        except Exception as e:
            logger.error(f"Error creating release: {e}")
            st.error("An error occurred while creating the release. Please try again.")