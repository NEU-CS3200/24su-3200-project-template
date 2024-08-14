import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Hi, {st.session_state['first_name']}. Would you like to update your account information?")
st.write('')
st.write('')

address_col = st.columns(1)
with address_col[0]:
    address = st.text_input('Address:')

logger.info(f'address = {address_col}')