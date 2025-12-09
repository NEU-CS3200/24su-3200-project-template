# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

#### ------------------------ Admin ------------------------
def AdminHomeNav():
    st.sidebar.page_link("pages/00_AdminDash.py", label= "Admin Home")
def ReportsManagementNav():
    st.sidebar.page_link("pages/10_Reports_Management.py", label="Report Management", icon="🚨")
def AdminUsers():
    st.sidebar.page_link("pages/10_Admin_User_Tools.py", label="User Management", icon="👥")
def ItemCleanupNav():
    st.sidebar.page_link("pages/10_Item_Cleanup.py", label="Item Cleanup", icon="🧹")


#### ------------------------ Data Analyst------------------------
def DataAnalystNav():
    st.sidebar.page_link("pages/00_DADash.py", label = "Data Analyst Home")

def DAListingsNav():
    st.sidebar.page_link("pages/01_DA_Listings.py", label="View Listings & Stock", icon="📦")

def DAShipmentsNav():
    st.sidebar.page_link("pages/02_DA_Shipments.py", label="Check Late Shipments", icon="🚨")

def DAUserMetricsNav():
    st.sidebar.page_link("pages/03_DA_UserMetrics.py", label="Analyze User Metrics", icon="👥")

#### ------------------------ Swapper------------------------
def SwapperNav():
    st.sidebar.page_link("pages/00_SwapperDash.py", label = "Swapper Home")

def SwapperFeed():
    st.sidebar.page_link("pages/50_Swapper_Feed.py", label = "Browse Feed", icon="👕" )

def SwapperSwaps():
    st.sidebar.page_link("pages/52_My_Swaps.py", label = "My Swaps", icon="🔄")

def SwapperPostListing():
    st.sidebar.page_link("pages/51_Swapper_Post_Listing.py", label = "Post Listing", icon="📤")


#### ------------------------ Taker------------------------
def TakerNav():
    st.sidebar.page_link("pages/00_TakerDash.py", label = "Taker Home")

def TakerFeed():
    st.sidebar.page_link("pages/40_Browse_Listings.py", label = "Browse Feed", icon="👕" )

def TakerOrders():
    st.sidebar.page_link("pages/41_My_Orders.py", label = "View My Orders", icon="📦")

def TakerRecommendations():
    st.sidebar.page_link("pages/42_Recommendations.py", label = "Recommendations", icon="✨")






# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):

    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/FitHublogo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:


        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "admin":
            AdminHomeNav()
            ReportsManagementNav()
            AdminUsers()
            ItemCleanupNav()

        # If the user is a data analyst, give them access to the data analyst pages
        if st.session_state["role"] == "analyst":
            DataAnalystNav()
            DAListingsNav()
            DAShipmentsNav()
            DAUserMetricsNav()

        #If the user is a swapper, give them access to the swapper pages
        if st.session_state["role"] == "swapper":
            SwapperNav()
            SwapperFeed()
            SwapperPostListing()
            SwapperSwaps()

        #If the user is a taker, give them access to the taker pages
        if st.session_state["role"] == "taker":
            TakerNav()
            TakerFeed()
            TakerOrders()
            TakerRecommendations()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout", key="logout_button"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")