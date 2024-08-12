# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

import streamlit as st


def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")


def FitnessEnthusiastNav():
    st.sidebar.page_link(
        "pages/00_Fitness_Enthusiast.py", label="Fitness Enthusiast Home", icon="👤"
    )
    st.sidebar.page_link("pages/01_Edit_Profile.py", label="Edit Profile", icon="🏦")
    st.sidebar.page_link(
        "pages/02_Generate_Recommendations.py", label="Generate Recommendations", icon="🗺️"
    )


def ProductManagerNav():
    st.sidebar.page_link("pages/10_Product_Manager.py", label="Product Manager Home", icon="🛜")
    st.sidebar.page_link("pages/11_Analytics.py", label="Analytics", icon="📈")
    st.sidebar.page_link("pages/12_Edit_Restaurant.py", label="Edit Restaurant Details", icon="🌺")


def ProfessorNav():
    st.sidebar.page_link("pages/20_Professor.py", label="Professor Home", icon="🖥️")
    st.sidebar.page_link("pages/21_Manage_Groups.py", label="Manage Groups", icon="🏢")
    st.sidebar.page_link(
        "pages/22_Group_Recommendations.py", label="Generate Group Recommendations", icon="🏢"
    )


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks():
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if st.session_state["authenticated"]:
        if st.session_state["role"] == "fitness_enthusiast":
            FitnessEnthusiastNav()

        if st.session_state["role"] == "product_manager":
            ProductManagerNav()

        if st.session_state["role"] == "professor":
            ProfessorNav()

    if not st.session_state["authenticated"]:
        HomeNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
