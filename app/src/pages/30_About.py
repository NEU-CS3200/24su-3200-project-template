import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    This is a travel app for CS 3200 Course Project.  

    The goal of this travel app is to help you plan your next vacation based on your preferences!

    ✈️ Happy Traveling! ✈️
    """
        )
