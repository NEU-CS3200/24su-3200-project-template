import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")


st.markdown (
    """
    This is a demo app for CS 3200 Course Project HomeFinder.  
    This product provides buyers, sellers, and realtors with
    market data and predictive analytics to determine the best
    time to buy or sell a home. It features a user-friendly 
    interface with a local area map and future home valuation 
    predictions, offering a comprehensive solution for real 
    estate needs. 
    Stay tuned for more information and features to come!
    """
        )
