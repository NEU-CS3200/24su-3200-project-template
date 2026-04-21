import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Welcome Artist, {st.session_state['first_name']}.")

def get_profile():
    try:
        response = requests.get(f"http://web-api:4000/artists/{st.session_state['artist_id']}")
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching artist profile: {e}")
        return None

profile = get_profile()

if profile:

    if st.button("Go to Library", type="primary", use_container_width=True):
        st.switch_page("pages/01_Artist_Library.py")

    if st.button("View My Stats", type="primary", use_container_width=True):
        st.switch_page("pages/02_Artist_Stats.py")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.header("Your Profile")
        pic_url = profile.get('profile_pic')
        if pic_url and pic_url.strip() != "":
            st.image(pic_url, caption="Profile Picture", width=150)
        else:
            st.image("https://via.placeholder.com/150", caption="No Profile Picture Set", width=150)
        st.write(f"**Bio:** {profile.get('bio', 'No bio yet.')}")
        insta = profile.get('instagram', 'Not linked')
        st.write(f"**Instagram:** [@{insta}](https://instagram.com/{insta})")

    with col2:
        st.header("Edit Profile Information")
        with st.form("edit_profile_form"):
            new_bio = st.text_input("Bio", value=profile.get("bio", ""), max_chars=500)
            new_instagram = st.text_input("Instagram Handle", value=profile.get("instagram", ""), max_chars=100)
            new_profile_pic = st.text_input("Upload New Profile Picture", value=profile.get("profile_pic", ""))
            submit = st.form_submit_button("Save Changes")

            if submit:
                # Handle the form submission
                update_payload = {
                    "bio": new_bio,
                    "instagram": new_instagram,
                    "profile_pic": new_profile_pic
                }
                try:
                    response = requests.put(f"http://web-api:4000/artists/{st.session_state['artist_id']}", json=update_payload)
                    if response.status_code == 200:
                        st.success("Profile updated successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to update profile.")
                except Exception as e:
                    logger.error(f"Error updating artist profile: {e}")
                    st.error("An error occurred while updating your profile.")
