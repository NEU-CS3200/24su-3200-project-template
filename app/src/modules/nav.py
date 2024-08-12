# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🐾')

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🐈‍⬛")

#### ------------------------ potential_adopter role ------------------------
def AdopterPageNav():
    st.sidebar.page_link("pages/00_Adopter_Home.py", label="Adopter Home", icon='🐶')
    st.sidebar.page_link("pages/01_Pet_Data_Viz.py", label="Pet Data Visualization", icon='🐕')
    st.sidebar.page_link("pages/02_Pet_Medical_History.py", label="Pet Medical History", icon='📋')
    st.sidebar.page_link("pages/05_Rescue_Agencies.py", label="Closest Rescue Agencies", icon='🏥')  

## ------------------------ rescue_manager role ------------------------
def RescueManagerPageNav():
    st.sidebar.page_link("pages/10_Rescue_Manager_Home.py", label="Rescue Manager Home", icon='💼')
    st.sidebar.page_link("pages/11_Manager_Med_His_View.py", label="Manager Update Medical History View", icon='📈')
    st.sidebar.page_link("pages/12_Manager_Adoption_View.py", label="Manager Adoption View", icon='🐱')
    st.sidebar.page_link("pages/13_Manager_Pending_Adoptions.py", label="View Pending Adoptions", icon='🙈')

#### ------------------------ researcher Role ------------------------
def ResearcherPageNav():
    st.sidebar.page_link("pages/20_Researcher_Home.py", label="Researcher Home", icon='🥼')
    st.sidebar.page_link("pages/21_Least_Adoptions.py", label='Pets with Least Adoptions', icon='😿')
    st.sidebar.page_link("pages/22_Least_Interest.py", label='Pets with Least Interest', icon='📉')
    st.sidebar.page_link("pages/23_Most_Surrendered.py", label='Most Surrendered Pets', icon='📊')

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in. 
    """    

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", use_column_width=True)

    # If there is no logged in user, redirect to the Home (Landing) page
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page('Home.py')
        
    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:
        # Show the Adopter links if the user is a potential adopter
        if st.session_state['role'] == 'potential_adopter':
            AdopterPageNav()

        # Show the Rescue Manager links if the user is a rescue manager
        if st.session_state['role'] == 'rescue_manager':
            RescueManagerPageNav()
        
        # Show the Researcher links if the user is a researcher
        if st.session_state['role'] == 'researcher':
            ResearcherPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state['role']
            del st.session_state['authenticated']
            st.switch_page('Home.py')

