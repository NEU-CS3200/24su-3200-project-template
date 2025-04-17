##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('CampusPerks')
st.write('\n\n')
st.write('### HI! Which user would you like to log in as?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

if st.button("Act as Beth, a Local Business Owner", 
             type='primary', 
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'local_business_owner'
    st.session_state['first_name'] = 'Beth'
    logger.info("Logging in as Local Business Owner Persona")
    st.switch_page('pages/3_Business_Owner_Home.py')

if st.button("Act as Bharat, a Budget-Conscious Student", 
             type='primary', 
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'budget_student'
    st.session_state['first_name'] = 'Bharat'
    logger.info("Logging in as Budget-Conscious Student Persona")
    st.switch_page('pages/1_Student_User_Home.py')

if st.button("Act as Glen, a Club Leader", 
             type='primary', 
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'club_leader'
    st.session_state['first_name'] = 'Glen'
    logger.info("Logging in as Club Leader Persona")
    st.switch_page('pages/2_Club_Leader_Home.py')

if st.button("Act as John, a System Administrator", 
             type='primary', 
             use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'system_admin'
    st.session_state['first_name'] = 'John'
    logger.info("Logging in as System Administrator Persona")
    st.switch_page('pages/4_Admin_Home.py')

