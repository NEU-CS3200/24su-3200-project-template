import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('🏢Employer Dashboard')

logger.info("Loading Employer Home page")

# API configuration
API_BASE_URL = "http://web-api:4000"

# Get the user_id from session state (use real session state in production)
employer_user_id = 37 #st.session_state.get("user_id", 37), Default to 37 for demo

if employer_user_id is None:
    st.error("User not logged in. Please return to home and log in.")
    st.stop()

# We'll get the company_profile_id from the user data
company_profile_id = None


# Function to fetch user data from API
def fetch_user_data(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        logger.info(f"Fetching user data for {user_id}: status_code={response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"User data received: {data}")
            return data[0] if data else None
        else:
            logger.warning(f"Failed to fetch user data, status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error fetching user data: {e}")
        return None
   
# Function to fetch company data from API
def fetch_company_data(company_profile_id):
    try:
        response = requests.get(f"{API_BASE_URL}/companyProfiles/{company_profile_id}")
        logger.info(f"Fetching company data for {company_profile_id}: status_code={response.status_code}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Company data received: {data}")
            return data[0] if data else None
        else:
            logger.warning(f"Failed to fetch company data, status code: {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error fetching company data: {e}")
        return None

# Function to update user data via API
def update_user_data(user_data):
    try:
        response = requests.put(f"{API_BASE_URL}/users", json=user_data)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error updating user data: {e}")
        return False
   
# Function to update company data via API
def update_company_data(company_data, company_id):
    try:
        # Use the existing endpoint from users routes
        update_data = {
            "id": company_id,
            "name": company_data["name"],
            "bio": company_data["bio"],
            "industry": company_data["industry"],
            "website_link": company_data["websiteLink"]
        }
        response = requests.put(f"{API_BASE_URL}/users/companyProfiles/create/{company_id}", json=update_data)
        logger.info(f"Updating company data: status_code={response.status_code}")
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error updating company data: {e}")
        return False

# Fetch user data first to get company profile ID
user_data = fetch_user_data(employer_user_id)

# Get company profile ID from user data
if user_data and user_data.get('companyProfileId'):
    company_profile_id = user_data.get('companyProfileId')
    company_data = fetch_company_data(company_profile_id)
else:
    company_data = None

if user_data:
    # Header
    st.subheader(f"Welcome back, {user_data['firstName']} {user_data['lastName']}!")

    # Display user info
    st.info(f"👤 **Email:** {user_data.get('email', 'Not provided')} | 📞 **Phone:** {user_data.get('phone', 'Not provided')}")

    # Company Information Form
    if company_data:
        with st.form("company_form"):
            st.subheader("Company Information")
            col1 = st.columns(1)[0]

            with col1:
                company_name = st.text_input("Company Name", value=company_data.get("name", ""))
                bio = st.text_area("Company Description", value=company_data.get("bio", ""), height=100)
                industry = st.text_input("Industry", value=company_data.get("industry", ""))
                website_link = st.text_input("Website", value=company_data.get("websiteLink", ""))

            company_submitted = st.form_submit_button("Update Company Profile", type="primary", use_container_width=True)
           
            if company_submitted:
                company_update_data = {
                    "name": company_name,
                    "bio": bio,
                    "industry": industry,
                    "websiteLink": website_link
                }

                if update_company_data(company_update_data, company_profile_id):
                    st.success("✅ Company profile updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update company profile")
    else:
        st.warning("⚠️ No company profile associated with this employer account.")
        st.info("Contact your administrator to associate a company profile with your account.")

    # Personal Information Form (separate form)
    with st.form("personal_form"):
        st.subheader("Personal Information")
        personal_col1 = st.columns(1)[0]

        with personal_col1:
            first_name = st.text_input("First Name", value=user_data.get("firstName", ""))
            last_name = st.text_input("Last Name", value=user_data.get("lastName", ""))
            email = st.text_input("Email", value=user_data.get("email", ""))
            phone = st.text_input("Phone", value=user_data.get("phone", ""))
           
            personal_submitted = st.form_submit_button("Update Personal Profile", type="primary", use_container_width=True)
           
            if personal_submitted:
                personal_update_data = {
                    "userId": employer_user_id,
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "phone": phone,
                    # Add required fields for the PUT /users endpoint
                    "major": user_data.get("major", ""),
                    "minor": user_data.get("minor", ""),
                    "college": user_data.get("college", ""),
                    "gradYear": user_data.get("gradYear", ""),
                    "grade": user_data.get("grade", ""),
                    "gender": user_data.get("gender", ""),
                    "race": user_data.get("race", ""),
                    "nationality": user_data.get("nationality", ""),
                    "sexuality": user_data.get("sexuality", ""),
                    "disability": user_data.get("disability", "")
                }
               
                if update_user_data(personal_update_data):
                    st.success("✅ Personal profile updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update personal profile")

else:
    st.error("Unable to load user data. Please try again later.")