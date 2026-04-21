import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests
from datetime import datetime

st.set_page_config(layout='wide')

SideBarLinks()

st.title("📝 Edit Release")

if 'editing_release' not in st.session_state:
    st.warning("No release selected for editing.")
    if st.button("Back to Library"):
        st.switch_page("pages/01_Artist_Library.py")
    st.stop()

release = st.session_state['editing_release']

with st.form("edit_release_form"):
    st.subheader(f"Editing: {release['title']}")

    new_title = st.text_input("Title", value=release['title'])

    try:

        current_date = datetime.strptime(str(release['release_date']), '%a, %d %b %Y %H:%M:%S %Z')
    except ValueError:
        current_date = datetime.strptime(str(release['release_date']), '%Y-%m-%d')
    new_date = st.date_input("Release Date", value=current_date)

    new_type = st.selectbox(
        "Type",
        ["Single", "EP", "Album"],
        index=["Single", "EP", "Album"].index(release['type'])
    )

    new_status = st.selectbox(
        "Status",
        ["Takedown", "Processing", "Approved", "Released"],
        index=["Takedown", "Processing", "Approved", "Released"].index(release['status'])
    )

    submit = st.form_submit_button("Save Changes", type="primary", use_container_width=True)

if submit:
    payload = {
        "title": new_title.strip(),
        "release_date": new_date.strftime('%Y-%m-%d'),
        "type": new_type,
        "status": new_status
    }

    try:
        url = f"http://web-api:4000/release/{release['rel_id']}"
        response = requests.put(url, json=payload)
        
        if response.status_code == 200:
            st.success("Changes saved!")
            # Clean up session state
            del st.session_state['editing_release']
            st.switch_page("pages/01_Artist_Library.py")
        else:
            st.error(f"Update failed: {response.text}")
    except Exception as e:
        st.error(f"Connection error: {e}")

with st.expander("Delete this release"):
    st.write("This action cannot be undone. All tracks and assets associated with this release will be removed.")

    confirm_name = st.text_input(f"Type '{release['title']}' to confirm")


    if st.button("Delete Release", type="primary", use_container_width=True):
        if confirm_name == release['title']:
            try:
                url = f"http://web-api:4000/releases/{release['rel_id']}"
                response = requests.delete(url)
                
                if response.status_code == 200:
                    st.success("Release deleted successfully.")
                    st.switch_page("pages/01_Artist_Library.py")
                else:
                    st.error(f"Delete failed: {response.json().get('error')}")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Confirmation title does not match.")