import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

st.session_state['authenticated'] = False
SideBarLinks(show_home=True)

st.title('The Profs App')

st.write('\n\n')
st.write('### HI! As which user would you like to log in?')

if st.button("Act as John, a Political Strategy Advisor", 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'pol_strat_advisor'
    st.session_state['first_name'] = 'John'
    st.switch_page('pages/00_Pol_Strat_Home.py')

if st.button('Act as Mohammad, an USAID worker', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'usaid_worker'
    st.session_state['first_name'] = 'Mohammad'
    st.switch_page('pages/10_USAID_Worker_Home.py')

if st.button('Act as System Administrator', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'administrator'
    st.session_state['first_name'] = 'SysAdmin'
    st.switch_page('pages/20_Admin_Home.py')



