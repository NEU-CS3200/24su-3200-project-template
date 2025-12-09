import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    Swap into style with FitHub! Refresh your wardrobe sustainably and 
    affordably through our easy barter system. List pieces to swap or offer up for take,
     and get smart recommendations based on your history. Filter by your preferences, 
     discover new looks, and upgrade your wardrobe like never before. Join the community and 
     start styling smarter.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
