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
    address = st.text_input('New Origin Address:')

username_col = st.columns(1)
with username_col[0]:
    username = st.text_input('New Username:')

email_col = st.columns(1)
with email_col[0]:
    email = st.text_input('New Email:')

logger.info(f'id = {st.session_state['id']}')
logger.info(f'address = {address}')
logger.info(f'username = {username}')
logger.info(f'email = {email}')

if st.button('Update!',
             type='primary',
             use_container_width=True):
    try:
        results = requests.get('http://api:4000/u/update_account').json()
        st.dataframe(results)
    except Exception as e:
        st.error(f"An error occurred: {e}")