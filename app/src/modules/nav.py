# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🏠')

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

### -------------------------Sidebar for Regular User -------------------------------------
def PlanTrip():
    st.sidebar.page_link("pages/select_trip.py", label = "Select Trip", icon = "🗒️")

def SelectTrip():
    st.sidebar.page_link("pages/plan_trip.py", label = "Plan Trip", icon = "✈️")

def UpdateAccount():
    st.sidebar.page_link("pages/users.py", label = "Update Account", icon = "🌟")

def Ratings():
    st.sidebar.page_link("pages/ratings_page.py", label = "Ratings", icon = "💯")



#### ------------------------ Marketing Analysis ------------------------
def adminpagenav():
    st.sidebar.page_link("pages/admin_home.py", label="Admin Home Page", icon='🖥️')

def Click_Count():
    st.sidebar.page_link("pages/Click_Count.py", label="Click Count Graphs", icon='📈')

def marketing_campaign():
    st.sidebar.page_link("pages/marketing_campaign.py", label="Marketing Campaign for Hotels", icon = "🗒️")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in. 
    """    

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width = 150)

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
            PlanTrip()
            SelectTrip()
            UpdateAccount()

        # If the user role is usaid worker, show the Api Testing page
        if st.session_state['role'] == 'intern':
            PlanTrip()
            Ratings()
            UpdateAccount()
        
        # If the user is an administrator, give them access to the administrator pages
        if st.session_state['role'] == 'administrator':
            adminpagenav()
            Click_Count()
            marketing_campaign()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state['role']
            del st.session_state['authenticated']
            st.switch_page('Home.py')

