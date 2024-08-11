import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    This is the application for BarkFontenot's team project!

    Our app PetFetch, a Petalytics application, is designed to help pet rescue agencies, adopters, and researchers!
    
    """
        )
