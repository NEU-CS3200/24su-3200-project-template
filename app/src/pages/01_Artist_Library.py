import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout='wide')

SideBarLinks()

def get_releases():
    try:
        response = requests.get(f"http://web-api:4000/artists/{st.session_state['artist_id']}")
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching artist releases: {e}")
        return None

releases = get_releases()
releases_data = releases.get('releases', [])

st.title(f"Library")


# This takes you to the creation page
if st.button("➕ Upload New Release", type="primary", use_container_width=True):
    st.switch_page("pages/03_Create_Release.py")

st.divider()

upcoming_statuses = ['Approved', 'Processing']
upcoming = [r for r in releases_data if r.get('status') in upcoming_statuses]
recent = [r for r in releases_data if r.get('status') == 'Released']


st.subheader("🗓️ Upcoming and In-Progress Releases")
if not upcoming:
    st.info("No releases currently approved or processing.")
else:
    for r in upcoming:
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
            c1.write(f"**{r['title']}**")

            status_color = ":orange[" if r['status'] == 'Processing' else ":green["
            c2.write(f"Status: {status_color}{r['status']}]")

            c3.write(f"Date: {r.get('release_date', 'TBD')}")
            
            if c4.button("Edit", key=f"up_{r['rel_id']}"):
                st.session_state['editing_release'] = r
                st.switch_page("pages/04_Edit_Release.py")
st.write("")

st.subheader("💿 Recent Releases")
if not recent:
    st.info("No releases have been released yet.")
    for r in recent:
        with st.container(border=True):
            rc1, rc2, rc3 = st.columns([3, 2, 1])
            rc1.write(f"**{r['title']}**")
            rc2.write(f"Released on: {r['release_date']}")
            
            if rc3.button("Edit", key=f"rec_{r['rel_id']}"):
                st.session_state['editing_release'] = r
                st.switch_page("pages/04_Edit_Release.py")