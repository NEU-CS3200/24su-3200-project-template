# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/90_About.py", label="About", icon="🧠")


#### ------------------------ Student (Charlie Stout) Role ------------------------
def StudentHomeNav():
    st.sidebar.page_link(
        "pages/00_Student_Home.py", label="Student Dashboard", icon="🎓"
    )


def StudentApplicationsNav():
    st.sidebar.page_link(
        "pages/01_Student_Applications.py", label="My Applications", icon="📝"
    )


def StudentPositionsNav():
    st.sidebar.page_link(
        "pages/02_Student_Browse_Positions.py", label="Browse Co-op Positions", icon="🔍"
    )


def StudentAnalyticsNav():
    st.sidebar.page_link(
        "pages/03_Student_Analytics.py", label="Salary & Company Data", icon="📊"
    )

def StudentCalendarNav():
    st.sidebar.page_link(
        "pages/04_Student_Calendar.py", label="Application Calendar", icon="📅"
    )


#### ------------------------ Advisor (Sarah Martinez) Role ------------------------
def AdvisorHomeNav():
    st.sidebar.page_link(
        "pages/10_Advisor_Home.py", label="Advisor Dashboard", icon="👨‍🏫"
    )

def AdvisorStudentManagementNav():
    st.sidebar.page_link(
        "pages/13_Advisor_StudentManagement.py", label="Student Management", icon="👥"
    )


def AdvisorAnalyticsNav():
    st.sidebar.page_link(
        "pages/11_Advisor_Analytics.py", label="Placement Analytics", icon="📈"
    )


def AdvisorCompaniesNav():
    st.sidebar.page_link(
        "pages/12_Advisor_Companies.py", label="Company Partnerships", icon="🏢"
    )


#### ------------------------ Employer (Phoebe Hwang) Role ------------------------
def EmployerHomeNav():
    st.sidebar.page_link(
        "pages/20_Employer_Home.py", label="Employer Dashboard", icon="🏢"
    )


def EmployerPostingsNav():
    st.sidebar.page_link(
        "pages/21_Employer_Postings.py", label="Manage Co-Op Postings", icon="📄"
    )


def EmployerApplicationsNav():
    st.sidebar.page_link(
        "pages/22_Employer_Applications.py", label="Review Applications", icon="👀"
    )


def EmployerCandidatesNav():
    st.sidebar.page_link(
        "pages/23_Employer_Candidates.py", label="Search Candidates", icon="🔎"
    )



#### ------------------------ System Administrator (Kaelyn Dunn) Role ------------------------
def AdminHomeNav():
    st.sidebar.page_link(
        "pages/30_Admin_Home.py", label="Admin Dashboard", icon="⚙️"
    )


def AdminEmployersNav():
    st.sidebar.page_link(
        "pages/31_Admin_Employers.py", label="Manage Employers", icon="🏭"
    )


def AdminPostingsNav():
    st.sidebar.page_link(
        "pages/32_Admin_Postings.py", label="Review Job Postings", icon="✅"
    )


def AdminDEINav():
    st.sidebar.page_link(
        "pages/33_Admin_DEI.py", label="DEI Metrics", icon="🌍"
    )


def AdminAnalyticsNav():
    st.sidebar.page_link(
        "pages/34_Admin_Analytics.py", label="Platform Analytics", icon="📈"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/coopalyticslogo.png", width=300)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Student Navigation (Charlie Stout persona)
        if st.session_state["role"] == "student":
            StudentHomeNav()
            StudentApplicationsNav()
            StudentPositionsNav()
            StudentCalendarNav()
            StudentAnalyticsNav()

        # Advisor Navigation (Sarah Martinez persona)
        if st.session_state["role"] == "advisor":
            AdvisorHomeNav()
            AdvisorStudentManagementNav()
            AdvisorAnalyticsNav()
            AdvisorCompaniesNav()

        # Employer Navigation (Phoebe Hwang persona)
        if st.session_state["role"] == "employer":
            EmployerHomeNav()
            EmployerPostingsNav()
            EmployerApplicationsNav()
            EmployerCandidatesNav()

        # System Administrator Navigation (Kaelyn Dunn persona)
        if st.session_state["role"] == "administrator":
            AdminHomeNav()
            AdminEmployersNav()
            AdminPostingsNav()
            AdminDEINav()
            AdminAnalyticsNav()
        

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")