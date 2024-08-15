# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🏠')

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Student Interface ------------------------
def StudentHomeNav():
    st.sidebar.page_link("pages/00_student_Home.py", label="Student Home", icon='👤')

def FormNav():
    st.sidebar.page_link("pages/01_prefrence_form.py", label="Update your major", icon='📋')

def GroupNav():
    st.sidebar.page_link("pages/02_find_similar_students.py", label="Find by specialty", icon='👨‍👨‍👦‍👦')

def SchedulingTaskNav():
    st.sidebar.page_link("pages/Scheduler_Tracker.py", label="Tasks + Scheduling", icon='🗓')

def OnCampusNav():
    st.sidebar.page_link("pages/03_find_oc.py", label="Find by on-campus", icon='🏫')

## ------------------------ Examples for Role of TA ------------------------
def SpecialTaNav():
    st.sidebar.page_link("pages/12_Special_Ta.py", label="Specialty", icon='💡')

def AvailabilityTaNav():
    st.sidebar.page_link("pages/11_Availability_Ta.py", label="Availability", icon='🗓')

def UpdateTANav():
    st.sidebar.page_link("pages/13_Update_Ta.py", label="Update availability", icon='📝')

#### ------------------------ Professor (ADMIN) Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Professor_Home.py", label="Home", icon='🏠')
    st.sidebar.page_link("pages/21_ML_Model_Mgmt.py", label='My Students', icon='📕')
    st.sidebar.page_link("pages/22_Section_Data.py", label="My Sections", icon='🔠')
    st.sidebar.page_link("pages/23_Submission_Data.py", label="Student Submissions", icon='📑')


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in. 
    """    

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width = 200)

    # If there is no logged in user, redirect to the Home (Landing) page
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page('Home.py')
        
    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state['role'] == 'student':
            StudentHomeNav()
            FormNav()
            GroupNav()
            OnCampusNav()
            SchedulingTaskNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state['role'] == 'ta':
            AvailabilityTaNav()
            SpecialTaNav()
            UpdateTANav()
        
        # If the user is an administrator, give them access to the administrator pages
        if st.session_state['role'] == 'professor':
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Change User Type"):
            del st.session_state['role']
            del st.session_state['authenticated']
            st.switch_page('Home.py')

