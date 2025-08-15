import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Logging setup
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Page setup
st.set_page_config(layout='wide')
SideBarLinks()

logger.info("Loading Coop Positions page")

# Constants
API_BASE_URL = "http://web-api:4000"

# student id from session state
charlie_user_id = st.session_state.get("user_id", None)

if charlie_user_id is None:
    st.error("🚫 User not logged in. Please return to the home page and log in.")
    st.stop()

# Coop Position filter
filter_option = st.selectbox(
    "View positions by:",
    options=["All", "Liked", "Disliked", "Matches Desired Skills"]
)

# Get coopPositionIds based on preference
def get_preference_ids(student_id, preference_value):
    url = f"{API_BASE_URL}/viewpos/{student_id}?preference={'true' if preference_value else 'false'}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            positions = response.json()
            return {pos["coopPositionId"] for pos in positions}
        else:
            logger.error(f"Failed to fetch preference={preference_value} positions: {response.status_code}")
            return set()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching preference={preference_value} positions: {e}")
        return set()

# get positions based on selected filter
def fetch_positions():
    if filter_option == "All":
        url = f"{API_BASE_URL}/positions"
    elif filter_option == "Liked":
        url = f"{API_BASE_URL}/viewpos/{charlie_user_id}?preference=true"
    elif filter_option == "Disliked":
        url = f"{API_BASE_URL}/viewpos/{charlie_user_id}?preference=false"
    elif filter_option == "Matches Desired Skills":
        url = f"{API_BASE_URL}/{charlie_user_id}/desiredSkills"
    else:
        st.warning("Unknown filter selected.")
        return []

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"API request error: {e}")
        return []

# Load position ID preferences only if viewing All
liked_position_ids = set()
disliked_position_ids = set()
if filter_option == "All":
    liked_position_ids = get_preference_ids(charlie_user_id, True)
    disliked_position_ids = get_preference_ids(charlie_user_id, False)

# get and display positions
positions = fetch_positions()

if filter_option == "Matches Desired Skills" and not positions:
    st.info("🔍 No matches found. You may not have any desired skills set in your profile.")

for pos in positions:
    coop_id = pos["coopPositionId"]
    title = pos["title"]

    # Add icons if in viewing all positions
    if filter_option == "All":
        liked = coop_id in liked_position_ids
        disliked = coop_id in disliked_position_ids

        if liked and disliked:
            title += " 👍👎"
        elif liked:
            title += " 👍"
        elif disliked:
            title += " 👎"

    with st.expander(title):
        st.write(f"**Location**: {pos.get('location', 'Not Specified')}")
        st.write(f"**Description**: {pos.get('description', 'N/A')}")
        st.write(f"**Industry**: {pos.get('industry', 'Not Specified')}")
        st.write(f"**Hourly Pay**: ${pos.get('hourlyPay', 'N/A')}/hr")
        
        st.write(f"**Desired GPA**: {pos.get('desiredGPA', 'N/A')}")
        st.write(f"**Deadline**: {pos.get('deadline', 'N/A')}")
        st.write(f"**Start Date**: {pos.get('startDate', 'N/A')}")
        st.write(f"**End Date**: {pos.get('endDate', 'N/A')}")

        st.write(f"**Required Skills ID**: {pos.get('requiredSkillsId', 'None')}")
        st.write(f"**Desired Skills ID**: {pos.get('desiredSkillsId', 'None')}")
        st.write(f"**Flagged**: {'Yes' if pos.get('flag') else 'No'}")

        # like, dislike, and remove preference buttons
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            if st.button("👍 Like", key=f"like_{coop_id}"):
                response = requests.post(f"{API_BASE_URL}/position", json={
                    "studentId": charlie_user_id,
                    "coopPositionId": coop_id,
                    "preference": True
                })
                if response.status_code == 200:
                    st.success("Marked as liked.")
                    st.rerun()
                else:
                    st.error("Failed to save preference.")

        with col2:
            if st.button("👎 Dislike", key=f"dislike_{coop_id}"):
                response = requests.post(f"{API_BASE_URL}/position", json={
                    "studentId": charlie_user_id,
                    "coopPositionId": coop_id,
                    "preference": False
                })
                if response.status_code == 200:
                    st.warning("Marked as disliked.")
                    st.rerun()
                else:
                    st.error("Failed to save preference.")

        with col3:
            if st.button("🗑️ Remove Preference", key=f"remove_{coop_id}"):
                response = requests.delete(f"{API_BASE_URL}/position", json={
                    "studentId": charlie_user_id,
                    "coopPositionId": coop_id
                })
                if response.status_code == 200:
                    st.info("Preference removed.")
                    st.rerun()
                else:
                    st.error("Failed to remove preference.")
