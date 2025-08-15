import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.header("👥 Student Management")

logger.info("Loading Advisor Student Management page")

# API configuration
API_BASE_URL = "http://web-api:4000"

# Get the user_id from session state
advisor_user_id = st.session_state.get("user_id", None)

if advisor_user_id is None:
    st.error("User not logged in. Please return to home and log in.")
    st.stop()

# Function to fetch advisor data from API
def fetch_advisor_data(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        logger.info(f"Fetching advisor data from API: status_code={response.status_code}")
        if response.status_code == 200:
            data = response.json()
            return data[0] if data else None
        return None
    except Exception as e:
        logger.error(f"Error fetching advisor data: {e}")
        # Fallback data if API is not available
        return {
            'userId': 31,
            'firstName': 'Sarah',
            'lastName': 'Martinez',
            'email': 's.martinez@neu.edu',
            'phone': '555-0301',
            'college': 'NEU',
            'industry': 'Academic',
            'gender': 'Female',
            'race': 'Hispanic',
            'nationality': 'American',
            'sexuality': 'Heterosexual',
            'disability': None
        }

# Function to fetch advisor's assigned students from API
def fetch_advisor_students(advisor_id):
    try:
        response = requests.get(f"{API_BASE_URL}/advisors/{advisor_id}/students")
        logger.info(f"Fetching advisor students from API: status_code={response.status_code}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"Error fetching advisor students: {e}")
        # Fallback data if API is not available
        return [
            {
                'userId': 1,
                'firstName': 'Charlie',
                'lastName': 'Stout',
                'email': 'c.stout@student.edu',
                'phone': '555-0101',
                'major': 'Computer Science',
                'minor': 'Mathematics',
                'college': 'Khoury College of Computer Sciences',
                'gradYear': '2026',
                'grade': 'Junior'
            },
            {
                'userId': 2,
                'firstName': 'Liam',
                'lastName': 'Williams',
                'email': 'l.williams@student.edu',
                'phone': '555-0102',
                'major': 'Business',
                'minor': 'Economics',
                'college': 'D\'Amore-McKim School of Business',
                'gradYear': '2025',
                'grade': 'Senior'
            },
            {
                'userId': 3,
                'firstName': 'Sophia',
                'lastName': 'Brown',
                'email': 's.brown@student.edu',
                'phone': '555-0103',
                'major': 'Mechanical Engineering',
                'minor': 'Physics',
                'college': 'College of Engineering',
                'gradYear': '2027',
                'grade': 'Sophomore'
            }
        ]

# Function to fetch student application statistics
def fetch_student_application_stats(student_id):
    try:
        response = requests.get(f"{API_BASE_URL}/student/{student_id}/applications/summary")
        logger.info(f"Fetching student application stats from API: status_code={response.status_code}")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Student application stats received: {data}")
            return data
        else:
            logger.warning(f"Failed to fetch student application stats, status code: {response.status_code}")
        return []
    except Exception as e:
        logger.error(f"Error fetching student application stats: {e}")
        return []

# Function to update advisor data
def update_advisor_data(advisor_id, advisor_data):
    try:
        response = requests.put(f"{API_BASE_URL}/advisors/{advisor_id}/profile", json=advisor_data)
        logger.info(f"Updating advisor profile: status_code={response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error updating advisor data: {e}")
        return False

# Function to update student flag status
def update_student_flag(advisor_id, student_id, flagged):
    try:
        response = requests.put(f"{API_BASE_URL}/advisors/{advisor_id}/students/{student_id}/flag",
                               json={"flagged": flagged})
        logger.info(f"Updating student flag: status_code={response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error updating student flag: {e}")
        return False

# Fetch data
advisor_data = fetch_advisor_data(advisor_user_id)
advisor_students = fetch_advisor_students(advisor_user_id)

# Display advisor information
if advisor_data:
    st.write(f"**Name:** {advisor_data.get('firstName', '')} {advisor_data.get('lastName', '')}")
    st.write(f"**Email:** {advisor_data.get('email', '')}")
    st.write(f"**Phone:** {advisor_data.get('phone', '')}")
    

st.markdown("---")

# Display students
if advisor_students:
    st.subheader(f"Your Advisees ({len(advisor_students)} students)")

    # Search and filter functionality
    search_col1, search_col2 = st.columns([2, 1])

    with search_col1:
        search_term = st.text_input("🔍 Search students by name or major", placeholder="Enter student name or major...")

    with search_col2:
        grad_years = sorted(list(set([student.get('gradYear', '') for student in advisor_students if student.get('gradYear')])))
        selected_year = st.selectbox("Filter by Graduation Year", ["All"] + grad_years)

    # Filter students based on search and year
    filtered_students = advisor_students

    if search_term:
        filtered_students = [
            student for student in filtered_students
            if search_term.lower() in f"{student.get('firstName', '')} {student.get('lastName', '')}".lower()
            or search_term.lower() in student.get('major', '').lower()
        ]

    if selected_year != "All":
        filtered_students = [
            student for student in filtered_students
            if student.get('gradYear') == selected_year
        ]

    st.markdown("---")

    # Display students in cards
    for i, student in enumerate(filtered_students):
        # Check if student is flagged
        is_flagged = student.get('flagged', False)

        # Create container with conditional styling for flagged students
        if is_flagged:
            with st.container():
                st.markdown("""
                <div style="border: 2px solid #ff6b6b; border-radius: 10px; padding: 15px; background-color: #fff5f5;">
                """, unsafe_allow_html=True)

                col1, col2, col3, col4 = st.columns([2, 2, 1.5, 0.5])

                with col1:
                    st.markdown(f"**🚩 {student.get('firstName', '')} {student.get('lastName', '')}**")
                    st.write(f"📧 {student.get('email', '')}")
                    st.write(f"📱 {student.get('phone', '')}")

                with col2:
                    st.write(f"🎓 **Major:** {student.get('major', '')}")
                    if student.get('minor'):
                        st.write(f"📚 **Minor:** {student.get('minor', '')}")
                    st.write(f"🏫 **College:** {student.get('college', '')}")
                    st.write(f"📅 **Graduation:** {student.get('gradYear', '')} ({student.get('grade', '')})")

                with col3:
                    # Fetch detailed application stats for this student
                    app_stats = fetch_student_application_stats(student.get('userId'))

                    # Create status counts
                    status_counts = {item.get('status', ''): item.get('ApplicationCount', 0) for item in app_stats} if app_stats else {}
                    under_review = status_counts.get('Under Review', 0)
                    submitted = status_counts.get('Submitted', 0)
                    rejected = status_counts.get('Rejected', 0)

                    # Display detailed metrics in a compact layout
                    st.markdown("**Application Status:**")
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("📋 Review", under_review)
                    with metric_col2:
                        st.metric("📤 Submit", submitted)
                    with metric_col3:
                        st.metric("❌ Reject", rejected)

                with col4:
                    # Flag toggle
                    if st.button("🚩 Unflag", key=f"unflag_{student.get('userId')}", use_container_width=True):
                        if update_student_flag(advisor_user_id, student.get('userId'), False):
                            st.success("Student unflagged!")
                            st.rerun()
                        else:
                            st.error("Failed to unflag student")

                st.markdown("</div>", unsafe_allow_html=True)
        else:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 2, 1.5, 0.5])

                with col1:
                    st.markdown(f"**{student.get('firstName', '')} {student.get('lastName', '')}**")
                    st.write(f"📧 {student.get('email', '')}")
                    st.write(f"📱 {student.get('phone', '')}")

                with col2:
                    st.write(f"🎓 **Major:** {student.get('major', '')}")
                    if student.get('minor'):
                        st.write(f"📚 **Minor:** {student.get('minor', '')}")
                    st.write(f"🏫 **College:** {student.get('college', '')}")
                    st.write(f"📅 **Graduation:** {student.get('gradYear', '')} ({student.get('grade', '')})")

                with col3:
                    # Fetch detailed application stats for this student
                    app_stats = fetch_student_application_stats(student.get('userId'))

                    # Create status counts
                    status_counts = {item.get('status', ''): item.get('ApplicationCount', 0) for item in app_stats} if app_stats else {}
                    under_review = status_counts.get('Under Review', 0)
                    submitted = status_counts.get('Submitted', 0)
                    rejected = status_counts.get('Rejected', 0)

                    # Display detailed metrics in a compact layout
                    st.markdown("**Application Status:**")
                    metric_col1, metric_col2, metric_col3 = st.columns(3)
                    with metric_col1:
                        st.metric("📋 Review", under_review)
                    with metric_col2:
                        st.metric("📤 Submit", submitted)
                    with metric_col3:
                        st.metric("❌ Reject", rejected)

                with col4:
                    # Flag toggle
                    if st.button("🏳️ Flag", key=f"flag_{student.get('userId')}", use_container_width=True):
                        if update_student_flag(advisor_user_id, student.get('userId'), True):
                            st.success("Student flagged!")
                            st.rerun()
                        else:
                            st.error("Failed to flag student")

        st.markdown("---")

else:
    st.info("No students assigned to you at this time.")