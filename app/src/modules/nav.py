# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def UserProfileNav():
    st.session_state["profile_id"] = st.session_state["id"]
    st.sidebar.page_link("pages/03_User_Profile.py", label="Profile", icon="🖼️")


def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/40_About.py", label="About", icon="🧠")


def CreateTicketNav():
    st.sidebar.page_link(
        "pages/21_Create_Ticket.py", label="Create Help Ticket", icon="🎫"
    )


#### ------------------------ Co-op Advisor Role ------------------------
def CoopAdvisorAdvHomeNav():
    st.sidebar.page_link(
        "pages/00_Coop_Advisor_Home.py", label="Co-op Advisor Home", icon="👤"
    )


def StudentSearchNav():
    st.sidebar.page_link(
        "pages/01_Student_Search.py", label="Student Search", icon="🧑‍🎓"
    )


def EmployerSearchNav():
    st.sidebar.page_link(
        "pages/02_Employer_Search.py", label="Employer Search", icon="🕴️"
    )


#### ------------------------ Emplyer Role ------------------------
def EmployerAdvHomeNav():
    st.sidebar.page_link("pages/10_Employer_Home.py", label="Employer Home", icon="🕴️")


def PositionOpeningsNav():
    st.sidebar.page_link(
        "pages/12_Position_Openings.py", label="Position Openings", icon="💼"
    )


def PositionOpeningsCreateNav():
    st.sidebar.page_link(
        "pages/13_Position_Opening_Creation.py",
        label="Post Position Opening",
        icon="➕",
    )


def StudentSearchNav():
    st.sidebar.page_link(
        "pages/01_Student_Search.py", label="Student Search", icon="🧑‍🎓"
    )


def ApplicationReviewNav():
    st.sidebar.page_link(
        "pages/11_Application_Review.py", label="Applications", icon="📝"
    )


#### ------------------------ Student Role ------------------------
def StudentAdvHomeNav():
    st.sidebar.page_link("pages/30_Student_Home.py", label="Student Home", icon="🧑‍🎓")


def PositionOpeningSearchNav():
    st.sidebar.page_link(
        "pages/31_Position_Opening_Search.py", label="Position Openings", icon="🔎"
    )


def EmployerSearchNav():
    st.sidebar.page_link("pages/02_Employer_Search.py", label="Employers", icon="🕴️")


def ApplicationEditorNav():
    st.sidebar.page_link(
        "pages/11_Application_Review.py", label="Applications", icon="📝"
    )


def ApplicationCreatorNav():
    st.sidebar.page_link(
        "pages/33_Application_Creator.py", label="Create Application", icon="➕"
    )


#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon="🖥️")


def ViewTicketsNav():
    st.sidebar.page_link("pages/22_View_Tickets.py", label="View Tickets", icon="🎫")


def CreateTicketsNav():
    st.sidebar.page_link("pages/21_Create_Ticket.py", label="Create Ticket", icon="🎫")


def RunQueryNav():
    st.sidebar.page_link("pages/23_Run_Query.py", label="Run Query", icon="🔍")


def ViewLogsNav():
    st.sidebar.page_link("pages/24_View_Logins.py", label="View Logs", icon="📜")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:
        UserProfileNav()

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "coop_advisor":
            CoopAdvisorAdvHomeNav()
            StudentSearchNav()
            EmployerSearchNav()
            ApplicationReviewNav()
            PositionOpeningSearchNav()
            CreateTicketNav()

        # If the user role is employer, show the Api Testing page
        if st.session_state["role"] == "employer":
            EmployerAdvHomeNav()
            StudentSearchNav()
            PositionOpeningsNav()
            ApplicationReviewNav()
            PositionOpeningsCreateNav()
            CreateTicketNav()

        # If the user role is student, show student home
        if st.session_state["role"] == "student":
            StudentAdvHomeNav()
            PositionOpeningSearchNav()
            EmployerSearchNav()
            ApplicationEditorNav()
            ApplicationCreatorNav()
            CreateTicketNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "administrator":
            AdminPageNav()
            ViewTicketsNav()
            CreateTicketsNav()
            RunQueryNav()
            ViewLogsNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
