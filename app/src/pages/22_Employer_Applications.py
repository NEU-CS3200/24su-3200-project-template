import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime, date
import pandas as pd

st.set_page_config(layout='wide')
SideBarLinks()

logger.info("Loading Employer Applications page")

# API configuration
API_BASE_URL = "http://web-api:4000"

# Get the user_id from session state
employer_user_id = 37#st.session_state.get("user_id", None)

if employer_user_id is None:
    st.error("User not logged in. Please return to home and log in.")
    st.stop()

# For demo purposes, use employer 37 who has positions in the database
# In production, this would use the actual logged-in employer ID
if employer_user_id == 1:  # If logged in as student, use employer 37 for demo
    employer_user_id = 37

# Function to fetch employer's co-op positions
def fetch_employer_positions(employer_id):
    """Fetch all co-op positions created by the employer"""
    try:
        response = requests.get(f"{API_BASE_URL}/employers/{employer_id}/positions")
        logger.info(f"Fetching employer positions: status_code={response.status_code}")

        if response.status_code == 200:
            positions = response.json()
            logger.info(f"Found {len(positions)} positions for employer {employer_id}")
            return positions

        return []
    except Exception as e:
        logger.error(f"Error fetching employer positions: {e}")
        return []

# Function to fetch applications with student details for a specific position
def fetch_position_applications_with_students(position_id):
    """Fetch all applications with student details for a specific co-op position"""
    try:
        response = requests.get(f"{API_BASE_URL}/applications/{position_id}/with-students")
        logger.info(f"Fetching applications with students for position {position_id}: status_code={response.status_code}")

        if response.status_code == 200:
            applications = response.json()
            logger.info(f"Found {len(applications)} applications for position {position_id}")
            return applications
        return []
    except Exception as e:
        logger.error(f"Error fetching applications for position {position_id}: {e}")
        return []

# Function to update application status
def update_application_status(application_id, new_status):
    """Update the status of an application"""
    try:
        response = requests.put(
            f"{API_BASE_URL}/applications/{application_id}/status",
            json={"status": new_status}
        )
        logger.info(f"Updating application {application_id} status to {new_status}: status_code={response.status_code}")

        if response.status_code == 200:
            result = response.json()
            logger.info(f"Successfully updated application status: {result}")
            return True, result
        else:
            error_msg = response.json().get('error', 'Unknown error')
            logger.error(f"Failed to update application status: {error_msg}")
            return False, error_msg

    except Exception as e:
        logger.error(f"Error updating application status: {e}")
        return False, str(e)

# Function to aggregate all applications for employer
def fetch_all_employer_applications(employer_id):
    """Aggregate all applications across all employer positions"""
    try:
        employer_positions = fetch_employer_positions(employer_id)
        all_applications = []

        for position in employer_positions:
            position_id = position.get('coopPositionId')
            if position_id:
                applications = fetch_position_applications_with_students(position_id)

                # Filter out draft applications and enrich with position details
                for app in applications:
                    # Skip draft applications
                    if app.get('status', '').lower() == 'draft':
                        continue

                    # Add position details from the position data
                    app['positionTitle'] = position.get('title', 'Unknown Position')
                    app['companyName'] = position.get('companyName', 'Unknown Company')
                    app['hourlyPay'] = position.get('hourlyPay', 0)
                    app['deadline'] = position.get('deadline', None)
                    app['location'] = position.get('location', 'Unknown Location')
                    app['industry'] = position.get('industry', 'Unknown Industry')

                    # Student details are already included from the API
                    app['studentName'] = f"{app.get('firstName', 'Unknown')} {app.get('lastName', 'Student')}"
                    app['studentEmail'] = app.get('email', 'unknown@email.com')
                    app['studentMajor'] = app.get('major', 'Unknown Major')
                    app['gradYear'] = app.get('gradYear', 'Unknown')

                    all_applications.append(app)

        logger.info(f"Total applications found: {len(all_applications)}")
        return all_applications

    except Exception as e:
        logger.error(f"Error aggregating employer applications: {e}")
        return []

# Initialize session state for refresh trigger
if 'refresh_applications' not in st.session_state:
    st.session_state.refresh_applications = False

# Fetch all applications for the employer
all_applications = fetch_all_employer_applications(employer_user_id)

# Reset refresh trigger
if st.session_state.refresh_applications:
    st.session_state.refresh_applications = False
    st.rerun()

# Page header
st.title("📋 Application Management")
st.subheader("Manage applications for your co-op positions")

if not all_applications:
    st.info("No applications found for your posted positions.")
    st.markdown("""
    **Possible reasons:**
    - No co-op positions have been posted yet
    - No students have applied to your positions
    - Applications are still being processed

    Please check back later or contact support if you believe this is an error.
    """)
    st.stop()

# Convert to DataFrame for easier manipulation
df = pd.DataFrame(all_applications)

# Summary statistics
st.markdown("### 📊 Application Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Applications", len(df))

with col2:
    submitted_count = len(df[df['status'] == 'Submitted']) if 'status' in df.columns else 0
    st.metric("Submitted", submitted_count)

with col3:
    under_review_count = len(df[df['status'] == 'Under Review']) if 'status' in df.columns else 0
    st.metric("Under Review", under_review_count)

with col4:
    accepted_count = len(df[df['status'] == 'Accepted']) if 'status' in df.columns else 0
    st.metric("Accepted", accepted_count)

st.markdown("---")

# Filters and search
st.markdown("### 🔍 Filter Applications")
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    # Status filter
    status_options = ["All"] + list(df['status'].unique()) if 'status' in df.columns else ["All"]
    selected_status = st.selectbox("Filter by Status", status_options)

with filter_col2:
    # Position filter
    position_options = ["All"] + list(df['positionTitle'].unique()) if 'positionTitle' in df.columns else ["All"]
    selected_position = st.selectbox("Filter by Position", position_options)

with filter_col3:
    # Search by student name or major
    search_term = st.text_input("Search by Student Name/Major", placeholder="Enter search term...")

# Apply filters
filtered_df = df.copy()

if selected_status != "All":
    filtered_df = filtered_df[filtered_df['status'] == selected_status]

if selected_position != "All":
    filtered_df = filtered_df[filtered_df['positionTitle'] == selected_position]

if search_term:
    search_mask = (
        filtered_df['studentName'].str.contains(search_term, case=False, na=False) |
        filtered_df['studentMajor'].str.contains(search_term, case=False, na=False)
    )
    filtered_df = filtered_df[search_mask]

st.markdown("---")

# Display applications
st.markdown(f"### 📋 Applications ({len(filtered_df)} found)")

if filtered_df.empty:
    st.info("No applications match your current filters.")
else:
    # Display applications in cards
    for idx, application in filtered_df.iterrows():
        with st.container():
            # Create card layout
            card_col1, card_col2, card_col3, card_col4 = st.columns([2, 2, 2, 1])

            with card_col1:
                st.markdown(f"**👤 {application.get('studentName', 'Unknown Student')}**")
                st.write(f"📧 {application.get('studentEmail', 'No email')}")
                st.write(f"🎓 {application.get('studentMajor', 'Unknown Major')}")
                st.write(f"📅 Grad Year: {application.get('gradYear', 'Unknown')}")
                if 'gpa' in application and application['gpa']:
                    st.write(f"⭐ GPA: {application['gpa']}")

            with card_col2:
                st.markdown(f"**💼 {application.get('positionTitle', 'Unknown Position')}**")
                st.write(f"🏢 {application.get('companyName', 'Unknown Company')}")
                st.write(f"📍 {application.get('location', 'Unknown Location')}")
                st.write(f"💰 ${application.get('hourlyPay', 0)}/hour")
                if application.get('deadline'):
                    st.write(f"⏰ Deadline: {application['deadline']}")

            with card_col3:
                # Application details
                app_date = application.get('dateTimeApplied', 'Unknown Date')
                if app_date != 'Unknown Date':
                    try:
                        # Format the date if it's a valid datetime string
                        if 'GMT' in str(app_date):
                            # Handle GMT format from API
                            formatted_date = datetime.strptime(app_date.split(' GMT')[0], '%a, %d %b %Y %H:%M:%S').strftime('%Y-%m-%d')
                        else:
                            formatted_date = datetime.fromisoformat(str(app_date).replace('Z', '+00:00')).strftime('%Y-%m-%d')
                        st.write(f"📅 Applied: {formatted_date}")
                    except:
                        st.write(f"📅 Applied: {app_date}")
                else:
                    st.write(f"📅 Applied: {app_date}")

                # Status with color coding
                status = application.get('status', 'Unknown')
                if status == 'Accepted':
                    st.success(f"✅ {status}")
                elif status == 'Rejected':
                    st.error(f"❌ {status}")
                elif status == 'Under Review':
                    st.warning(f"👁️ {status}")
                else:
                    st.info(f"📝 {status}")

                # Resume indicator
                if application.get('resume'):
                    st.write("📄 Resume: Available")
                else:
                    st.write("📄 Resume: Not provided")

                # Cover letter excerpt
                cover_letter = application.get('coverLetter', '')
                if cover_letter:
                    excerpt = cover_letter[:100] + "..." if len(cover_letter) > 100 else cover_letter
                    st.write(f"📝 Cover Letter: {excerpt}")

            with card_col4:
                # Action buttons based on application status
                status = application.get('status', 'Unknown')
                application_id = application.get('applicationId', idx)

                # Accept/Reject buttons for actionable applications
                if status in ['Submitted', 'Under Review']:
                    col_accept, col_reject = st.columns(2)

                    with col_accept:
                        if st.button("✅", key=f"accept_{application_id}", use_container_width=True, type="primary"):
                            with st.spinner("Accepting application..."):
                                success, result = update_application_status(application_id, "Accepted")
                                if success:
                                    st.success("Application accepted!")
                                    st.session_state.refresh_applications = True
                                    st.rerun()
                                else:
                                    st.error(f"Failed to accept application: {result}")

                    with col_reject:
                        if st.button("❌", key=f"reject_{application_id}", use_container_width=True):
                            with st.spinner("Rejecting application..."):
                                success, result = update_application_status(application_id, "Rejected")
                                if success:
                                    st.success("Application rejected!")
                                    st.session_state.refresh_applications = True
                                    st.rerun()
                                else:
                                    st.error(f"Failed to reject application: {result}")

                # View Student Profile button
                st.markdown("---")
                if st.button(f"👤 View Profile", key=f"profile_{application_id}", use_container_width=True):
                    # Set the selected student ID in session state
                    st.session_state["selected_student_id"] = application.get('studentId', None)
                    st.session_state["selected_application_id"] = application_id

                    # Navigate to candidate profile page
                    st.switch_page("pages/23_Employer_Candidates.py")

        st.markdown("---")

# Additional information
st.markdown("### ℹ️ Need Help?")
st.info("""
**Tips for managing applications:**
- Use the filters above to focus on specific types of applications
- Click "View Profile" to see detailed student information
- Applications are automatically updated when students submit new ones
- Contact support if you notice any issues with application data
""")