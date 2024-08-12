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

st.title('Home Finder')

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('Where you can find your future home')
st.write('\n\n')
st.write('As which user would you like to log in?')


if st.button("Act as Bob Smith, Realtor", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True

    st.session_state['role'] = 'realtor'
    st.session_state['first_name'] = 'Bob'
    st.switch_page('pages/00_Realtor_Home.py')

if st.button('Act as Jayson Tatum, Home Buyer', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'user'
    st.session_state['first_name'] = 'Jayson'
    st.switch_page('pages/10_Home_Buyer_Home.py')

if st.button('Act as System Administrator', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'SysAdmin'
    st.switch_page('pages/20_Admin_Home.py')



