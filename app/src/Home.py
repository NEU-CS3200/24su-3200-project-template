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

st.title('Getaway Guru')

st.write('\n\n')
st.write('### Select the user you would like to login as:')

if st.button("Act as Alice, a Student", 
            type = 'primary', 
            use_container_width=True):
    # when user clicks the button, they are now considered authenticated
    st.session_state['authenticated'] = True
    # we set the role of the current user
    st.session_state['role'] = 'pol_strat_advisor'
    st.session_state['first_name'] = 'Alice'
<<<<<<< HEAD
    st.switch_page('pages/trip.py')
    st.session_state['first_name'] = 'Alice'
    st.switch_page('pages/trip.py')
=======
    st.switch_page('pages/users.py')
>>>>>>> 2dbc7765ac074f52e2c8cd845bcb3ae281028fcd

if st.button('Act as Thomas, an Marketing Analyst', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'usaid_worker'
    st.session_state['first_name'] = 'Thomas'
    st.switch_page('pages/10_USAID_Worker_Home.py')

if st.button('Act as Janice, an intern planning a company trip', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'Janice'
    st.switch_page('pages/20_Admin_Home.py')



