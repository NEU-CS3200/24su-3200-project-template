import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')
SideBarLinks()

logger.info("Loading Employer Candidates page")

# API configuration
API_BASE_URL = "http://web-api:4000"

# Function to fetch student details
def fetch_student_details(student_id):
    """Fetch student information from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/users/{student_id}")
        logger.info(f"Fetching student details for {student_id}: status_code={response.status_code}")

        if response.status_code == 200:
            student_data = response.json()
            logger.info(f"Student data received: {student_data}")
            return student_data[0] if student_data else None
        else:
            logger.warning(f"Failed to fetch student details, status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error fetching student details: {e}")
        return None

# Function to fetch application details
def fetch_application_details(application_id):
    """Fetch application information from the API"""
    try:
        response = requests.get(f"{API_BASE_URL}/applications/{application_id}/details")
        logger.info(f"Fetching application details for {application_id}: status_code={response.status_code}")

        if response.status_code == 200:
            application_data = response.json()
            logger.info(f"Application data received: {application_data}")
            return application_data
        else:
            logger.warning(f"Failed to fetch application details, status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error fetching application details: {e}")
        return None

# Check if a student was selected from the applications page
selected_student_id = st.session_state.get("selected_student_id", None)
selected_application_id = st.session_state.get("selected_application_id", None)

st.title('👤 Student Profile')

if selected_student_id:
    # Fetch student data and application details
    with st.spinner("Loading student profile..."):
        student_data = fetch_student_details(selected_student_id)
        application_data = None
        if selected_application_id:
            application_data = fetch_application_details(selected_application_id)

    if student_data:
        # Display student name in header
        student_name = f"{student_data.get('firstName', 'Unknown')} {student_data.get('lastName', 'Student')}"
        st.subheader(f"👤 {student_name}")

        # Display application context if available
        if selected_application_id:
            st.info(f"📋 Viewing profile from Application ID: {selected_application_id}")

        # Student Information Section
        st.markdown("### 📊 Student Information")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Personal Details:**")
            st.write(f"• **Name:** {student_name}")
            st.write(f"• **Email:** {student_data.get('email', 'Not provided')}")
            st.write(f"• **Major:** {student_data.get('major', 'Not specified')}")
            if student_data.get('minor'):
                st.write(f"• **Minor:** {student_data.get('minor')}")
            st.write(f"• **Graduation Year:** {student_data.get('gradYear', 'Not specified')}")
            st.write(f"• **Grade Level:** {student_data.get('grade', 'Not specified')}")
            st.write(f"• **College:** {student_data.get('college', 'Not specified')}")
            if student_data.get('phone'):
                st.write(f"• **Phone:** {student_data.get('phone')}")

        with col2:
            st.markdown("**Demographics & Additional Info:**")
            if student_data.get('gender'):
                st.write(f"• **Gender:** {student_data.get('gender')}")
            if student_data.get('race'):
                st.write(f"• **Race:** {student_data.get('race')}")
            if student_data.get('nationality'):
                st.write(f"• **Nationality:** {student_data.get('nationality')}")
            if student_data.get('sexuality'):
                st.write(f"• **Sexuality:** {student_data.get('sexuality')}")
            if student_data.get('disability'):
                st.write(f"• **Disability:** {student_data.get('disability')}")

        # Application Context Section (if available)
        if selected_application_id and application_data:
            st.markdown("### 📋 Application Details")

            col3, col4 = st.columns(2)

            with col3:
                st.markdown("**Application Information:**")
                st.write(f"• **Application ID:** {application_data.get('applicationId', 'N/A')}")

                # Status with color coding
                status = application_data.get('status', 'Unknown')
                if status == 'Accepted':
                    st.success(f"• **Status:** ✅ {status}")
                elif status == 'Rejected':
                    st.error(f"• **Status:** ❌ {status}")
                elif status == 'Under Review':
                    st.warning(f"• **Status:** 👁️ {status}")
                else:
                    st.info(f"• **Status:** 📝 {status}")

                # Format date applied
                date_applied = application_data.get('dateTimeApplied', 'Unknown')
                if date_applied != 'Unknown':
                    try:
                        from datetime import datetime
                        formatted_date = datetime.strptime(date_applied.split(' GMT')[0], '%a, %d %b %Y %H:%M:%S').strftime('%B %d, %Y at %I:%M %p')
                        st.write(f"• **Date Applied:** {formatted_date}")
                    except:
                        st.write(f"• **Date Applied:** {date_applied}")
                else:
                    st.write(f"• **Date Applied:** {date_applied}")

                # Application-specific GPA
                if application_data.get('gpa'):
                    st.write(f"• **GPA (from application):** {application_data.get('gpa')}")

            with col4:
                st.markdown("**Position Applied For:**")
                st.write(f"• **Position:** {application_data.get('positionTitle', 'Unknown Position')}")
                st.write(f"• **Location:** {application_data.get('location', 'Unknown Location')}")
                st.write(f"• **Hourly Pay:** ${application_data.get('hourlyPay', 0)}/hour")
                st.write(f"• **Industry:** {application_data.get('industry', 'Unknown Industry')}")

                # Application deadline
                deadline = application_data.get('deadline', 'Unknown')
                if deadline != 'Unknown':
                    try:
                        formatted_deadline = datetime.strptime(deadline.split(' GMT')[0], '%a, %d %b %Y %H:%M:%S').strftime('%B %d, %Y')
                        st.write(f"• **Application Deadline:** {formatted_deadline}")
                    except:
                        st.write(f"• **Application Deadline:** {deadline}")

            # Documents section
            st.markdown("### 📄 Application Documents")

            doc_col1, doc_col2 = st.columns(2)

            with doc_col1:
                st.markdown("**Resume:**")
                if application_data.get('resume'):
                    with st.expander("View Resume Content"):
                        st.text_area("Resume", application_data.get('resume'), height=200, disabled=True)
                else:
                    st.write("No resume provided")

            with doc_col2:
                st.markdown("**Cover Letter:**")
                if application_data.get('coverLetter'):
                    with st.expander("View Cover Letter"):
                        st.text_area("Cover Letter", application_data.get('coverLetter'), height=200, disabled=True)
                else:
                    st.write("No cover letter provided")

        elif selected_application_id and not application_data:
            st.markdown("### 📋 Application Context")
            st.warning("⚠️ Unable to load application details. The application may not exist or there was an error fetching the data.")
            st.write(f"Application ID: {selected_application_id}")

    else:
        st.error("❌ Unable to load student profile. The student may not exist or there was an error fetching the data.")
        st.write("Please try again or contact support if the issue persists.")

    st.markdown("---")

    # Navigation back to applications
    if st.button("← Back to Applications", use_container_width=True):
        # Clear the selected student from session state
        if "selected_student_id" in st.session_state:
            del st.session_state["selected_student_id"]
        if "selected_application_id" in st.session_state:
            del st.session_state["selected_application_id"]

        st.switch_page("pages/22_Employer_Applications.py")

else:
    st.info("No student selected. Please navigate from the Application Management page to view a specific student profile.")

    if st.button("Go to Application Management", use_container_width=True):
        st.switch_page("pages/22_Employer_Applications.py")