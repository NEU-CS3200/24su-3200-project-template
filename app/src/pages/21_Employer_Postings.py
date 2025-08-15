import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime, date

st.set_page_config(layout='wide')

SideBarLinks()

st.title('🆕 Create Co-op Posting')

logger.info("Loading Create Co-op Posting page")

# API configuration
API_BASE_URL = "http://web-api:4000"

# Get the user_id from session state (use real session state in production)
employer_user_id = 37 #st.session_state.get("user_id", 37)  # Default to 37 for demo

if employer_user_id is None:
    st.error("User not logged in. Please return to home and log in.")
    st.stop()

# Function to fetch available skills
def fetch_skills():
    try:
        response = requests.get(f"{API_BASE_URL}/skills")
        logger.info(f"Fetching skills: status_code={response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Skills data received: {len(data)} skills")
            return data
        else:
            logger.warning(f"Failed to fetch skills, status code: {response.status_code}")
            return []
    except Exception as e:
        logger.error(f"Error fetching skills: {e}")
        return []

# Function to get next available co-op position ID (thread-safe)
def get_next_coop_position_id():
    try:
        # Use the dedicated endpoint for getting next ID
        response = requests.get(f"{API_BASE_URL}/coopPositions/nextId")
        logger.info(f"Getting next position ID: status_code={response.status_code}")

        if response.status_code == 200:
            data = response.json()
            next_id = data.get('nextId', 1)
            logger.info(f"Next position ID: {next_id}")
            return next_id
        else:
            logger.warning(f"Failed to get next ID from API, falling back to positions endpoint")
            # Fallback to the original method if the new endpoint fails
            return get_next_id_fallback()
    except Exception as e:
        logger.error(f"Error getting next position ID: {e}")
        return get_next_id_fallback()

# Fallback method using existing positions endpoint
def get_next_id_fallback():
    try:
        response = requests.get(f"{API_BASE_URL}/positions")
        if response.status_code == 200:
            positions = response.json()
            if positions:
                max_id = max([pos.get('coopPositionId', 0) for pos in positions])
                return max_id + 1
            else:
                return 1
        else:
            logger.warning(f"Positions endpoint failed with status {response.status_code}")
            return 1
    except Exception as e:
        logger.error(f"Error in fallback ID generation: {e}")
        return 1

# Function to create co-op position with retry logic for duplicate ID conflicts
def create_coop_position(position_data, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(f"{API_BASE_URL}/createsPos/coopPosition", json=position_data)
            logger.info(f"Creating co-op position (attempt {attempt + 1}): status_code={response.status_code}")

            if response.status_code in (200, 201):
                return True, response.json()
            elif response.status_code == 409:  # Conflict - duplicate ID
                logger.warning(f"Duplicate ID conflict on attempt {attempt + 1}, retrying with new ID...")
                if attempt < max_retries - 1:  # Don't retry on last attempt
                    # Get a new ID and update the position data
                    new_id = get_next_coop_position_id()
                    position_data['coopPositionId'] = new_id
                    logger.info(f"Retrying with new position ID: {new_id}")
                    continue
                else:
                    return False, "Failed to create position after multiple attempts due to ID conflicts"
            else:
                logger.error(f"Failed to create position: {response.status_code} - {response.text}")
                return False, response.text

        except Exception as e:
            logger.error(f"Error creating co-op position (attempt {attempt + 1}): {e}")
            if attempt == max_retries - 1:  # Last attempt
                return False, str(e)

    return False, "Maximum retry attempts exceeded"

# Function to link employer to position
def link_employer_to_position(employer_id, position_id):
    try:
        link_data = {
            "employerId": employer_id,
            "coopPositionId": position_id
        }
        response = requests.post(f"{API_BASE_URL}/createsPos", json=link_data)
        logger.info(f"Linking employer to position: status_code={response.status_code}")
        if response.status_code in (200, 201):
            return True, response.json()
        else:
            logger.error(f"Failed to link employer to position: {response.status_code} - {response.text}")
            return False, response.text
    except Exception as e:
        logger.error(f"Error linking employer to position: {e}")
        return False, str(e)

# Function to fetch user data to get company info
def fetch_user_data(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        if response.status_code == 200:
            data = response.json()
            return data[0] if data else None
        return None
    except Exception as e:
        logger.error(f"Error fetching user data: {e}")
        return None

# Fetch user data and skills
user_data = fetch_user_data(employer_user_id)
available_skills = fetch_skills()

if not user_data:
    st.error("Unable to load user data. Please try again later.")
    st.stop()

# Header
st.subheader(f"👋 Hello, {user_data['firstName']} {user_data['lastName']}!")
st.info("Create a new co-op position for your company.")

# Create the form
with st.form("create_coop_form"):
    st.subheader("📋 Position Details")
    
    # Basic position information
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Position Title*")
        location = st.text_input("Location*")
        hourly_pay = st.number_input("Hourly Pay ($)*", min_value=0.0, value=20.0, step=0.50, format="%.2f")
        industry = st.selectbox("Industry*", [
            "Technology", "Finance", "Healthcare", "Manufacturing", 
            "Consulting", "Education", "Marketing", "Engineering",
            "Biotechnology", "Non-profit", "Other"
        ], index=0)
    
    with col2:
        start_date = st.date_input("Start Date*")
        end_date = st.date_input("End Date*")
        deadline = st.date_input("Application Deadline*")
        desired_gpa = st.number_input("Minimum GPA", min_value=0.0, max_value=4.0, value=3.0, step=0.1, format="%.1f")
    
    # Description
    st.subheader("📝 Position Description")
    description = st.text_area(
        "Job Description*", 
        placeholder="Describe what students can expect in this position",
        height=150
    )
    
    # Skills section
    st.subheader("🛠️ Skills Requirements")

    skill_options = []
    skill_ids = {}

    if available_skills:
        for skill in available_skills:
            skill_display = f"{skill['name']} ({skill['category']})"
            skill_options.append(skill_display)
            skill_ids[skill_display] = skill['skillId']

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Required Skills** (Must have)")
        required_skills = st.multiselect(
            "Select required skills",
            options=skill_options,
            help="Students must have these skills to be eligible"
        )

    with col2:
        st.write("**Desired Skills** (Nice to have)")
        desired_skills = st.multiselect(
            "Select desired skills", 
            options=skill_options,
            help="Preferred skills that would be beneficial"
        )

    if required_skills or desired_skills:
        st.info(f"📋 **Selected:** {len(required_skills)} required, {len(desired_skills)} desired skills")
    
    # Submit button
    submitted = st.form_submit_button("🚀 Create Co-op Position", type="primary", use_container_width=True)
    
    if submitted:
        # Validation
        errors = []
        
        if not title.strip():
            errors.append("Position title is required")
        if not location.strip():
            errors.append("Location is required")
        if not description.strip():
            errors.append("Job description is required")
        if hourly_pay <= 0:
            errors.append("Hourly pay must be greater than 0")
        if start_date >= end_date:
            errors.append("End date must be after start date")
        if deadline >= start_date:
            errors.append("Application deadline must be before start date")
        
        if errors:
            for error in errors:
                st.error(f"❌ {error}")
        else:
            # Get next position ID
            next_position_id = get_next_coop_position_id()

            # Prepare position data
            position_data = {
                "coopPositionId": next_position_id,
                "title": title.strip(),
                "location": location.strip(),
                "description": description.strip(),
                "hourlyPay": float(hourly_pay),
                "requiredSkillsId": skill_ids.get(required_skills[0]) if required_skills else None,
                "desiredSkillsId": skill_ids.get(desired_skills[0]) if desired_skills else None,
                "desiredGPA": float(desired_gpa),
                "deadline": f"{deadline} 23:59:59",
                "startDate": str(start_date),
                "endDate": str(end_date),
                "flag": False,
                "industry": industry
            }
            
            # Create the position
            with st.spinner("Creating co-op position..."):
                success, result = create_coop_position(position_data)

            if success:
                # Link employer to position
                with st.spinner("Linking position to your account..."):
                    link_success, link_result = link_employer_to_position(employer_user_id, next_position_id)

                if link_success:
                    st.success("🎉 Co-op position created successfully!")
                    st.balloons()

                    # Display summary
                    st.subheader("📊 Position Summary")
                    summary_col1, summary_col2 = st.columns(2)

                    with summary_col1:
                        st.write(f"**Position ID:** {next_position_id}")
                        st.write(f"**Title:** {title}")
                        st.write(f"**Location:** {location}")
                        st.write(f"**Industry:** {industry}")
                        st.write(f"**Hourly Pay:** ${hourly_pay:.2f}")

                    with summary_col2:
                        st.write(f"**Start Date:** {start_date}")
                        st.write(f"**End Date:** {end_date}")
                        st.write(f"**Application Deadline:** {deadline}")
                        st.write(f"**Minimum GPA:** {desired_gpa}")
                        if required_skills:
                            if len(required_skills) == 1:
                                st.write(f"**Required Skill:** {required_skills[0]}")
                            else:
                                st.write(f"**Required Skills:** {required_skills[0]} (+{len(required_skills)-1} more)")
                        if desired_skills:
                            if len(desired_skills) == 1:
                                st.write(f"**Desired Skill:** {desired_skills[0]}")
                            else:
                                st.write(f"**Desired Skills:** {desired_skills[0]} (+{len(desired_skills)-1} more)")

                    st.info("💡 Students can now view and apply to this position!")

                    # Store success state in session state for button outside form
                    st.session_state.position_created_successfully = True
                    st.session_state.created_position_id = next_position_id

                else:
                    st.error(f"❌ Position created but failed to link to employer: {link_result}")
                    st.info("Please contact support to resolve this issue.")
            else:
                st.error(f"❌ Failed to create co-op position: {result}")
                st.info("Please check your input and try again.")

# Option to create another position (outside the form)
if st.session_state.get('position_created_successfully', False):
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("➕ Create Another Position", type="secondary", use_container_width=True):
            # Clear the success state and rerun to reset the form
            st.session_state.position_created_successfully = False
            if 'created_position_id' in st.session_state:
                del st.session_state.created_position_id
            st.rerun()
