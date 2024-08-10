import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

st.title('Home Finder')

st.write('\n\n')
st.write('As which user would you like to log in?')

if st.button("Act as Bob Smith, Realtor", 
            type = 'primary', 
            use_container_width=True):
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



