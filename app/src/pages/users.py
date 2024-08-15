import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

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

data = {
    'address': address,
    'username': username,
    'email': email
}

logger.info(f'address = {data["address"]}')
logger.info(f'username = {data["username"]}')
logger.info(f'email = {data["email"]}')

if st.button('Update!',
             type='primary',
             use_container_width=True):
    st.write(data)
    try:
        response = requests.put(f'http://api:4000/u/update_account/{st.session_state["id"]}', json = data)
        st.success("Account information updated successfully!")
    except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

#delete trip based on trip name

option = st.selectbox(
     "Which trip would you like to delete?",
    (f''' SELECT name 
        FROM trip
         WHERE user_id = {st.session_state["id"]}
         '''),
    index=None,
     placeholder="Select trip...",
 )

st.write("You selected:", option)

