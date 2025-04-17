import streamlit as st
# from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks(show_home=True)



st.write("# About CampusPerks")

st.markdown (
    """
   Introducing CampusPerks, the ultimate app for connecting students with local business discounts! Our app empowers businesses to create exclusive discounts for students in their area, while providing students with a comprehensive database of money-saving opportunities. 
    """
        )
