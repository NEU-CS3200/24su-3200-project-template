import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

st.title('PetFetch - A Petalytics Application')

st.write('\n\n')
st.write('### Hi! Which user would you like to log in as?')

if st.button("Act as Clark, a Potential Adopter", 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'potential_adopter'
    st.session_state['first_name'] = 'Clark'
    st.switch_page('pages/00_Adopter_Home.py')

if st.button('Act as Janet, an Agency Rescue Manager', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'rescue_manager'
    st.session_state['first_name'] = 'Janet'
    st.switch_page('pages/10_Rescue_Manager_Home.py')

if st.button('Act as Alex a Pet Researcher', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'researcher'
    st.session_state['first_name'] = 'Alex'
    st.switch_page('pages/20_Researcher_Home.py')



