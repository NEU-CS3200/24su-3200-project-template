import logging
import streamlit as st
import requests
from modules.nav import SideBarLinks

# Setup
st.set_page_config(layout='wide')
SideBarLinks()
logger = logging.getLogger(__name__)
logger.info("Loading Applications page")

API_BASE_URL = "http://web-api:4000"
user_id = st.session_state.get("user_id", None)

if user_id is None:
    st.error("🚫 User not logged in. Please return to the home page and log in.")
    st.stop()

# Create tabs 
tab1, tab2 = st.tabs(["📄 Application Status", "📝 Apply to New Position"])

# Existing applications tab
with tab1:
    st.subheader("📄 My Applications")

    try:
        res = requests.get(f"{API_BASE_URL}/student/{user_id}/applications")
        if res.status_code == 200:
            apps = res.json()              
            if not apps:
                st.info("No applications submitted yet.")
            else:
                for app in apps:
                    # Assign individual fields to variables for clarity
                    position_title = app.get('positionTitle', 'Unknown Position')
                    application_status = app.get('applicationStatus', 'Unknown Status')
                    date_applied = app.get('dateTimeApplied', 'N/A')
                    gpa = app.get('gpa', 'N/A')
                    resume = app.get('resume', 'N/A')
                    cover_letter = app.get('coverLetter', 'N/A')

                    with st.expander(f"{position_title} — {application_status}"):
                        st.markdown(f"**Applied on:** `{date_applied}`")
                        st.markdown(f"**GPA:** `{gpa}`")
                        st.markdown("**Resume:**")
                        st.code(resume)
                        st.markdown("**Cover Letter:**")
                        st.code(cover_letter)
        else:
            st.error(f"Could not fetch applications. Server returned status code {res.status_code}")
    except Exception as e:
        st.error(f"Error fetching applications: {e}")

# Apply to new position tab
with tab2:
    st.subheader("📝 Submit a New Application")

    try:
        pos_res = requests.get(f"{API_BASE_URL}/positions")
        if pos_res.status_code == 200:
            positions = pos_res.json()
            pos_map = {f"{pos['title']} (ID: {pos['coopPositionId']})": pos['coopPositionId'] for pos in positions}

            if not pos_map:
                st.warning("No co-op positions are currently available.")
            else:
                pos_label = st.selectbox("Select a Position", list(pos_map.keys()))
                selected_pos_id = pos_map[pos_label]

                resume = st.text_area("Paste your resume here", height=150)
                cover_letter = st.text_area("Paste your cover letter here", height=150)
                gpa = st.number_input("Your GPA", min_value=0.0, max_value=4.0, step=0.01, format="%.2f")

                if st.button("📤 Submit Application"):
                    data = {
                        "studentId": user_id,
                        "coopPositionId": selected_pos_id,
                        "resume": resume,
                        "coverLetter": cover_letter,
                        "gpa": gpa,
                        "status": "Submitted"
                    }

                    try:
                        submit_res = requests.post(f"{API_BASE_URL}/applications/new", json=data)
                        if submit_res.status_code == 201:
                            st.success("Application submitted successfully!")
                            st.rerun()
                        else:
                            error_info = submit_res.json().get("error", "No error message returned")
                            st.error(f"Failed to submit application. Reason: {error_info}")
                    except Exception as e:
                        st.error(f"Exception occurred during submission: {e}")
        else:
            st.error("Failed to fetch positions.")
    except Exception as e:
        st.error(f"Error: {e}")
