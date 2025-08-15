import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

# set up
st.set_page_config(layout='wide')
SideBarLinks()

logger.info("Loading Student Home page")

# Charlie Stout's userId from database
API_BASE_URL = "http://web-api:4000"

# user_id from session state
charlie_user_id = st.session_state.get("user_id", None)

if charlie_user_id is None:
    st.error("User not logged in. Please return to home and log in.")
    st.stop()

# Function to get user data from API
def fetch_user_data(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}")
        logger.info(f"Fetching user data from API: status_code={response.status_code}")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"User data received: {data}")
            return data
        else:
            logger.error(f"Failed to fetch user data, status code: {response.status_code}, response: {response.text}")
        return None
    except Exception as e:
        logger.error(f"Error fetching user data: {e}")
        # Fallback data if API is not available
        return {
            'userId': 1,
            'firstName': 'Charlie',
            'lastName': 'Stout',
            'email': 'c.stout@student.edu',
            'phone': '555-0101',
            'major': 'Computer Science',
            'minor': 'Mathematics',
            'college': 'Khoury College of Computer Sciences',
            'gradYear': '2026',
            'grade': 'Junior',
            'gender': None,
            'race': None,
            'nationality': None,
            'sexuality': None,
            'disability': None
        }

# Function to get user skills from API
def fetch_user_skills(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}/skills")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"Error fetching user skills: {e}")
        return []

# Function to get application summary from API
def fetch_application_summary(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/student/{user_id}/applications/summary")
        logger.info(f"Fetching application summary from API: status_code={response.status_code}")
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Application summary data received: {data}")
            return data
        else:
            logger.warning(f"Failed to fetch application summary, status code: {response.status_code}")
        return []
    except Exception as e:
        logger.error(f"Error fetching application summary: {e}")
        return []

# Function to get recent applications from API
def fetch_recent_applications(user_id):
    try:
        response = requests.get(f"{API_BASE_URL}/users/{user_id}/recent-applications")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"Error fetching recent applications: {e}")
        return []

# Function to update user data via API
def update_user_data(user_data):
    try:
        response = requests.put(f"{API_BASE_URL}/users", json=user_data)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error updating user data: {e}")
        return False

# Function to get all available skills from API
def fetch_all_skills():
    try:
        response = requests.get(f"{API_BASE_URL}/skills")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"Error fetching all skills: {e}")
        return []

# Function to update user skills
def update_user_skills(user_id, updated_skills, removed_skills):
    try:
        update_data = {
            "updated_skills": list(updated_skills.values()),
            "removed_skills": removed_skills
        }
        response = requests.put(f"{API_BASE_URL}/users/{user_id}/skills", json=update_data)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error updating user skills: {e}")
        return False

# Function to add new skills to user profile
def add_user_skills(user_id, new_skills):
    try:
        response = requests.post(f"{API_BASE_URL}/users/{user_id}/skills", json={"skills": new_skills})
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Error adding user skills: {e}")
        return False

# Get user data and related information
user_data = fetch_user_data(charlie_user_id)
if isinstance(user_data, list) and len(user_data) > 0:
    user_data = user_data[0]

user_skills = fetch_user_skills(charlie_user_id)
app_summary = fetch_application_summary(charlie_user_id)
recent_applications = fetch_recent_applications(charlie_user_id)

if user_data:
    # Header
    st.title("🎓 Student Dashboard")
    st.subheader(f"Welcome back, {user_data['firstName']}!")
    
    # Tabs for initial student profile view
    tab1, tab2, tab3 = st.tabs(["📋 Profile", "📊 Quick Stats", "🛠️ Skills Management"])
    
    # Initial student profile view that can be updated
    with tab1:
        st.header("Your Profile")
        
        with st.form("profile_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Personal Information")
                first_name = st.text_input("First Name", value=user_data.get("firstName", ""))
                last_name = st.text_input("Last Name", value=user_data.get("lastName", ""))
                email = st.text_input("Email", value=user_data.get("email", ""))
                phone = st.text_input("Phone", value=user_data.get("phone", ""))
                
            with col2:
                st.subheader("Academic Information")
                major_options = ["Computer Science", "Data Science", "Information Systems", "Cybersecurity", 
                               "Business", "Marketing", "Finance", "International Business", "Mechanical Engineering", 
                               "Biomedical Engineering", "Electrical Engineering", "Environmental Engineering", 
                               "Physics", "Biology", "Chemistry", "Psychology", "Design", "Mathematics", 
                               "Economics", "Art", "Spanish", "Sociology", "History"]
                
                major_index = 0
                if user_data.get("major") in major_options:
                    major_index = major_options.index(user_data.get("major"))
                major = st.selectbox("Major", major_options, index=major_index)
                
                minor_options = ["None"] + major_options
                minor_index = 0
                if user_data.get("minor") in minor_options:
                    minor_index = minor_options.index(user_data.get("minor"))
                minor = st.selectbox("Minor", minor_options, index=minor_index)
                
                college_options = ["College of Arts, Media and Design", "Bouvé College of Health Sciences", 
                                 "D'Amore-McKim School of Business", "Khoury College of Computer Sciences", 
                                 "College of Engineering", "College of Science", "College of Social Sciences and Humanities"]
                college_index = 0
                current_college = user_data.get("college", "")
                if current_college in college_options:
                    college_index = college_options.index(current_college)
                college = st.selectbox("College", college_options, index=college_index)
                
                grad_year_options = ["2024", "2025", "2026", "2027"]
                grad_year_index = 0
                if user_data.get("gradYear") in grad_year_options:
                    grad_year_index = grad_year_options.index(user_data.get("gradYear"))
                grad_year = st.selectbox("Graduation Year", grad_year_options, index=grad_year_index)
                
                grade_options = ["Sophomore", "Junior", "Senior"]
                grade_index = 0
                if user_data.get("grade") in grade_options:
                    grade_index = grade_options.index(user_data.get("grade"))
                grade = st.selectbox("Current Grade", grade_options, index=grade_index)
            
            st.subheader("Demographics")
            demo_col1, demo_col2 = st.columns(2)

            with demo_col1:
                gender_options = ["Male", "Female", "Non-binary", "Prefer not to say", "Other"]
                gender_index = 0
                if user_data.get("gender") in gender_options:
                    gender_index = gender_options.index(user_data.get("gender"))
                gender = st.selectbox("Gender", gender_options, index=gender_index)

                race_options = ["White", "Asian", "Black/African American", "Hispanic/Latino",
                               "Native American", "Pacific Islander", "Mixed", "Prefer not to say"]
                race_index = 0
                if user_data.get("race") in race_options:
                    race_index = race_options.index(user_data.get("race"))
                race = st.selectbox("Race/Ethnicity", race_options, index=race_index)

            with demo_col2:
                nationality_options = ["American", "International", "Prefer not to say"]
                nationality_index = 0
                if user_data.get("nationality") in nationality_options:
                    nationality_index = nationality_options.index(user_data.get("nationality"))
                nationality = st.selectbox("Nationality", nationality_options, index=nationality_index)

                sexuality_options = ["Heterosexual", "LGBTQ+", "Prefer not to say"]
                sexuality_index = 0
                if user_data.get("sexuality") in sexuality_options:
                    sexuality_index = sexuality_options.index(user_data.get("sexuality"))
                sexuality = st.selectbox("Sexual Orientation", sexuality_options, index=sexuality_index)

            disability_options = ["None", "ADHD", "Anxiety", "Dyslexia", "Depression", "Autism", "Prefer not to say"]
            disability_index = 0
            if user_data.get("disability") in disability_options:
                disability_index = disability_options.index(user_data.get("disability"))
            disability = st.selectbox("Disability Status", disability_options, index=disability_index)
            
            submitted = st.form_submit_button("Update Profile", type="primary", use_container_width=True)
            
            if submitted:
                update_data = {
                    "userId": charlie_user_id,
                    "firstName": first_name,
                    "lastName": last_name,
                    "email": email,
                    "phone": phone,
                    "major": major,
                    "minor": minor if minor != "None" else None,
                    "college": college,
                    "gradYear": grad_year,
                    "grade": grade,
                    "gender": gender,
                    "race": race,
                    "nationality": nationality,
                    "sexuality": sexuality,
                    "disability": disability if disability != "None" else None
                }
                
                if update_user_data(update_data):
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to update profile")

    # General Stats for the student on their application process
    with tab2:
        st.header("📊 Quick Stats")

        # Calculate metrics from real data
        total_applications = sum(item.get('ApplicationCount', 0) for item in app_summary) if app_summary else 0
        under_review = next((item.get('ApplicationCount', 0) for item in app_summary if item.get('status') == 'Under Review'), 0)
        submitted = next((item.get('ApplicationCount', 0) for item in app_summary if item.get('status') == 'Submitted'), 0)

        # Get GPA from most recent application
        latest_gpa = "N/A"
        if recent_applications:
            latest_gpa = recent_applications[0].get('gpa', 'N/A')

        # Display metrics in a clean layout
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            st.metric(label="📝 Applications Submitted", value=str(total_applications), delta="Total")

        with metric_col2:
            st.metric(label="👁️ Under Review", value=str(under_review), delta="Pending")

        with metric_col3:
            st.metric(label="📄 Recently Submitted", value=str(submitted), delta="Awaiting Review")

        with metric_col4:
            st.metric(label="⭐ GPA", value=str(latest_gpa), delta="Latest Application")
        
        # Skills section that can be updated by the student
        st.subheader("🛠️ Your Skills Profile")
        st.caption("Based on your profile and experience")

        if user_skills:
            # Group skills by category
            skills_by_category = {}
            for skill in user_skills:
                category = skill['category']
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill)

            # Display skills in columns
            categories = list(skills_by_category.keys())
            if len(categories) >= 3:
                skill_col1, skill_col2, skill_col3 = st.columns(3)
                cols = [skill_col1, skill_col2, skill_col3]
            elif len(categories) == 2:
                skill_col1, skill_col2 = st.columns(2)
                cols = [skill_col1, skill_col2]
            else:
                cols = [st]

            for i, category in enumerate(categories):
                col = cols[i % len(cols)]
                with col:
                    st.markdown(f"**{category}**")
                    for skill in skills_by_category[category]:
                        proficiency = skill['proficiencyLevel']
                        progress_value = proficiency / 5.0  # Convert 1-5 scale to 0-1

                        # Convert proficiency to text
                        proficiency_text = {1: "Beginner", 2: "Basic", 3: "Intermediate", 4: "Advanced", 5: "Expert"}
                        level_text = proficiency_text.get(proficiency, "Unknown")

                        st.write(f"{skill['name']} ({level_text})")
                        st.progress(progress_value)
        else:
            st.info("No skills data available. Please contact your advisor to update your skills profile.")

    with tab3:
        # Skills Management Section
        st.header("🛠️ Skills Management")

        if user_skills:
            # Group skills by category
            skills_by_category = {}
            for skill in user_skills:
                category = skill['category']
                if category not in skills_by_category:
                    skills_by_category[category] = []
                skills_by_category[category].append(skill)

            # Create skills management form
            with st.form("skills_form"):
                st.subheader("📝 Edit Your Skills & Proficiency Levels")

                # Display skills grouped by category
                updated_skills = {}
                skills_to_remove = []

                for category, skills in skills_by_category.items():
                    st.markdown(f"**{category}**")

                    for skill in skills:
                        col1, col2, col3 = st.columns([3, 2, 1])

                        with col1:
                            st.write(f"• {skill['name']}")

                        with col2:
                            # Proficiency level slider (1-5)
                            proficiency = st.slider(
                                f"Level",
                                min_value=1,
                                max_value=5,
                                value=skill['proficiencyLevel'],
                                key=f"skill_{skill['skillId']}_proficiency",
                                help="1=Beginner, 2=Novice, 3=Intermediate, 4=Advanced, 5=Expert"
                            )
                            updated_skills[skill['skillId']] = {
                                'skillId': skill['skillId'],
                                'proficiencyLevel': proficiency
                            }

                        with col3:
                            # Remove skill checkbox
                            if st.checkbox("Remove", key=f"remove_skill_{skill['skillId']}"):
                                skills_to_remove.append(skill['skillId'])

                    st.markdown("")  # Add spacing between categories

                # Save skills changes button
                skills_submitted = st.form_submit_button("💾 Save Skills Changes", type="primary", use_container_width=True)

                if skills_submitted:
                    # Filter out skills marked for removal
                    final_skills = {k: v for k, v in updated_skills.items() if k not in skills_to_remove}

                    if update_user_skills(charlie_user_id, final_skills, skills_to_remove):
                        st.success("✅ Skills updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update skills")

        # Add New Skills Section
        st.markdown("---")
        st.subheader("➕ Add New Skills")

        # get all available skills for adding
        all_skills = fetch_all_skills()
        if all_skills:
            # Filter out skills user already has
            current_skill_ids = [skill['skillId'] for skill in user_skills] if user_skills else []
            available_skills = [skill for skill in all_skills if skill['skillId'] not in current_skill_ids]

            if available_skills:
                with st.form("add_skills_form"):
                    # Group available skills by category for easier selection
                    available_by_category = {}
                    for skill in available_skills:
                        category = skill['category']
                        if category not in available_by_category:
                            available_by_category[category] = []
                        available_by_category[category].append(skill)

                    selected_skills = []

                    for category, skills in available_by_category.items():
                        st.markdown(f"**{category}**")

                        for skill in skills:
                            col1, col2 = st.columns([3, 2])

                            with col1:
                                if st.checkbox(skill['name'], key=f"add_skill_{skill['skillId']}"):
                                    with col2:
                                        proficiency = st.slider(
                                            "Proficiency",
                                            min_value=1,
                                            max_value=5,
                                            value=3,
                                            key=f"new_skill_{skill['skillId']}_proficiency",
                                            help="1=Beginner, 2=Novice, 3=Intermediate, 4=Advanced, 5=Expert"
                                        )
                                        selected_skills.append({
                                            'skillId': skill['skillId'],
                                            'proficiencyLevel': proficiency
                                        })

                        st.markdown("")  

                    # Add selected skills button
                    add_skills_submitted = st.form_submit_button("➕ Add Selected Skills", type="secondary", use_container_width=True)

                    if add_skills_submitted and selected_skills:
                        if add_user_skills(charlie_user_id, selected_skills):
                            st.success(f"✅ Added {len(selected_skills)} new skills!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to add skills")
                    elif add_skills_submitted and not selected_skills:
                        st.warning("⚠️ Please select at least one skill to add")
            else:
                st.info("🎉 You have all available skills! Great job!")
        else:
            st.error("❌ Unable to load available skills")


else:
    st.error("Unable to load user data. Please try again later.")