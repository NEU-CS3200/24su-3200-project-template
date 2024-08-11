# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st

#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon='🏠')

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Examples for Role of Realtor ------------------------
def RealtorHomeNav():
    st.sidebar.page_link("pages/00_Realtor_Home.py", label="Realtor Home", icon='👤')

def ViewPropertiesNav():
    st.sidebar.page_link("pages/01_View_Properties.py", label="View Properties", icon='🏠')

def EditPropertiesNav():
    st.sidebar.page_link("pages/02_Add_Edit_Properties.py", label="Add/Edit Properties", icon='🔧')

## ------------------------ Examples for Role of usaid_worker ------------------------
def AreaPriceNav():
    st.sidebar.page_link("pages/11_Area_Price.py", label="View Area Pricing", icon='🏙️')

def FuturePriceNav():
    st.sidebar.page_link("pages/12_Future_Outcomes.py", label="Predict Future Prices", icon='📈')

def PreviousDataNav():
    st.sidebar.page_link("pages/13_Previous_Data.py", label="Previous Data", icon='🌆')

#### ------------------------ System Admin Role ------------------------
def AdminPageNav():
    st.sidebar.page_link("pages/20_Admin_Home.py", label="System Admin", icon='🖥️')
    st.sidebar.page_link("pages/21_Data_View.py", label='View Data', icon='🏢')


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

        # Show pages for realtor role
        if st.session_state['role'] == 'realtor':
            RealtorHomeNav()
            ViewPropertiesNav()
            EditPropertiesNav()

        # If the user role is user, show the Api Testing page
        if st.session_state['role'] == 'user':
            AreaPriceNav()
            FuturePriceNav()
            PreviousDataNav()
        
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

