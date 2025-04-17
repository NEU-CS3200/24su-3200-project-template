# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st
import os

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🏠')

def AboutPageNav():
    st.sidebar.page_link("pages/0_About.py", label="About", icon="🧠")

#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/4_Admin_Home.py", label="System Admin", icon='🖥️')


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in. 
    """    

    # add a logo to the sidebar always
    logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "CampusPerks_Logo.jpg")
    st.sidebar.image(logo_path, width=150)

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
        if st.session_state['role'] == 'pol_strat_advisor':
            PolStratAdvHomeNav()
            WorldBankVizNav()
            MapDemoNav()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state['role'] == 'usaid_worker':
            PredictionNav()
            ApiTestNav() 
            ClassificationNav()
        
        # If the user is an administrator, give them access to the administrator pages
        if st.session_state['role'] == 'administrator':
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state['role']
            del st.session_state['authenticated']
            st.switch_page('Home.py')

