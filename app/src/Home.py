##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

st.session_state["authenticated"] = False
SideBarLinks()

st.title("Foond!")
st.title("the Food Finder App")

st.write("\n\n")
st.write("#### Which user do you want to log in as?")

if st.button("Emma, the student Fitness Enthusiast", type="primary", use_container_width=True):
    st.session_state["authenticated"] = True
    st.session_state["role"] = "fitness_enthusiast"
    st.session_state["first_name"] = "Emma"
    st.switch_page("pages/00_Fitness_Enthusiast.py")

if st.button("Emilio, the fit Product Manager", type="primary", use_container_width=True):
    st.session_state["authenticated"] = True
    st.session_state["role"] = "product_manager"
    st.session_state["first_name"] = "Emilio"
    st.switch_page("pages/10_Product_Manager.py")

if st.button("Emanuel, the grumpy Databasing Professor", type="primary", use_container_width=True):
    st.session_state["authenticated"] = True
    st.session_state["role"] = "professor"
    st.session_state["first_name"] = "Emanuel"
    st.switch_page("pages/20_Professor.py")
