import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown (
    """
    This is a demo app for CS 3200 Course Project.  

    The goal of this demo is to provide information on the tech stack 
    being used as well as demo some of the features of the various platforms. 

    **Our demo app is... ProjectPal!**

    **What is it?**
    ProjectPal is an app designed to streamline group project coordination for students. Instead of the risk of being put with random group members you might not be able to get along with, students will be able to handpick their group members as well as seamlessly communicate on when and where to meet.

    **What does it do?**
    Offers an easy and convenient way to get to know potential group members backgrounds when choosing groups to ensure everyone has a group they’re happy with
    Makes coordinating meetings between group members or between a group and a TA easier by making schedules transparent

    **There are three user types (Student, TA, & Professor), so feel free to play around!** 


    Made by Spring Yan, Nathaniel Yee, Blythe Berlinger, Corey Wang, David Ku | August 2024.
    """
)
