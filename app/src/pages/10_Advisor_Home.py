import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')
SideBarLinks()

logger.info("Loading Advisor Home page")

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

if advisor_data:
    
        st.header("Your Advisor Profile")

        with st.form("advisor_profile_form"):
            st.subheader("Personal Information")
            col1, col2 = st.columns(2)

            with col1:
                first_name = st.text_input("First Name", value=advisor_data.get("firstName", ""))
                last_name = st.text_input("Last Name", value=advisor_data.get("lastName", ""))

            with col2:
                email = st.text_input("Email", value=advisor_data.get("email", ""))
                phone = st.text_input("Phone", value=advisor_data.get("phone", ""))

            st.subheader("Demographics")
            demo_col1, demo_col2 = st.columns(2)

            with demo_col1:
                gender_options = ["Male", "Female", "Non-binary", "Prefer not to say", "Other"]
                gender_index = 0
                if advisor_data.get("gender") in gender_options:
                    gender_index = gender_options.index(advisor_data.get("gender"))
                gender = st.selectbox("Gender", gender_options, index=gender_index)

                race_options = ["White", "Asian", "Black/African American", "Hispanic/Latino",
                               "Native American", "Pacific Islander", "Mixed", "Prefer not to say"]
                race_index = 0
                if advisor_data.get("race") in race_options:
                    race_index = race_options.index(advisor_data.get("race"))
                race = st.selectbox("Race/Ethnicity", race_options, index=race_index)

            with demo_col2:
                nationality_options = ["American", "International", "Prefer not to say"]
                nationality_index = 0
                if advisor_data.get("nationality") in nationality_options:
                    nationality_index = nationality_options.index(advisor_data.get("nationality"))
                nationality = st.selectbox("Nationality", nationality_options, index=nationality_index)

                sexuality_options = ["Heterosexual", "LGBTQ+", "Prefer not to say"]
                sexuality_index = 0
                if advisor_data.get("sexuality") in sexuality_options:
                    sexuality_index = sexuality_options.index(advisor_data.get("sexuality"))
                sexuality = st.selectbox("Sexual Orientation", sexuality_options, index=sexuality_index)

            disability_options = ["None", "ADHD", "Anxiety", "Dyslexia", "Depression", "Autism", "Prefer not to say"]
            disability_index = 0
            if advisor_data.get("disability") in disability_options:
                disability_index = disability_options.index(advisor_data.get("disability"))
            disability = st.selectbox("Disability Status", disability_options, index=disability_index)

            submitted = st.form_submit_button("Update Profile", type="primary", use_container_width=True)

            if submitted:
                update_data = {
                    "userId": advisor_user_id,
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "phone": phone,
                    "gender": gender,
                    "race": race,
                    "nationality": nationality,
                    "sexuality": sexuality,
                    "disability": disability if disability != "None" else None
                }

                if update_advisor_data(advisor_user_id, update_data):
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update profile")


else:
    st.error("Unable to load advisor data. Please try again later.")
    st.info("If this problem persists, please contact the system administrator.")