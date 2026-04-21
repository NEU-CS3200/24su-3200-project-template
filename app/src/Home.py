# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout='wide')
st.session_state['authenticated'] = False

SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

logger.info("Loading the Home page of the app")
st.title('Audiovate')
st.write('#### Hi! As which user would you like to log in?')

def get_artists():
    try:
        response = requests.get("http://web-api:4000/artists")
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching artists: {e}")
        return []

def get_all_users():
    try:
        response = requests.get("http://web-api:4000/users")
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return []

all_artists = get_artists()
all_users = get_all_users()

st.markdown("### Artist")
if all_artists:
    artist_map = {
    f"{a.get('first_name', 'Unknown')} {a.get('last_name', '')}": a
    for a in all_artists
}
    selected_name = st.selectbox("Choose an artist", options=list(artist_map.keys()), index=0)

    if st.button("Act as Artist", type="primary", use_container_width=True):
        # Find the matching record to get the ID
        user_data = next(a for a in all_artists if f"{a['first_name']} {a['last_name']}" == selected_name)
    
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'artist'
        st.session_state['artist_id'] = user_data['artist_id']
        st.session_state['first_name'] = user_data['first_name']
        st.switch_page('pages/00_Artist_Home.py')

st.divider()

st.markdown("### Data Analyst")

data_analysts = [u for u in all_users if u.get('role', '').lower() == 'data analyst']
if data_analysts:
    data_analyst_map = {f"{da['first_name']} {da['last_name']}": da for da in data_analysts}
    selected_data_analyst = st.selectbox("Choose a data analyst", options=list(data_analyst_map.keys()), key="data_analyst_select")

    if st.button("Act as Data Analyst", type="primary", use_container_width=True):
        data = data_analyst_map[selected_data_analyst]
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'data_analyst'
        st.session_state['data_analyst_id'] = data['user_id']
        st.session_state['user_id'] = data['user_id']
        st.session_state['first_name'] = data['first_name']
        st.session_state['last_name'] = data['last_name']
        st.switch_page('pages/10_Data_Analyst_Home.py')

st.divider()

st.markdown("### System Admin")
admins = [u for u in all_users if u.get('role', '').lower() == 'admin']
if admins:
    admin_map = {f"{a['first_name']} {a['last_name']}": a for a in admins}
    selected_admin = st.selectbox("Choose a system admin", options=list(admin_map.keys()), key="admin_select")

    if st.button("Act as Admin", type="primary", use_container_width=True):
        data = admin_map[selected_admin]
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'administrator'
        st.session_state['admin_id'] = data['user_id']
        st.session_state['first_name'] = data['first_name']
        st.session_state['last_name'] = data['last_name']
        st.switch_page('pages/20_System_Admin_Home.py')

st.divider()

st.markdown("### Label Head")
label_heads = [u for u in all_users if u.get('role', '').lower() == 'label head']
if label_heads:
    label_head_map = {f"{lh['first_name']} {lh['last_name']}": lh for lh in label_heads}
    selected_label_head = st.selectbox("Choose a label head", options=list(label_head_map.keys()), key="label_head_select")

    if st.button("Act as Label Head", type="primary", use_container_width=True):
        data = label_head_map[selected_label_head]
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'label_head'
        st.session_state['label_head_id'] = data['user_id']
        st.session_state['first_name'] = data['first_name']
        st.session_state['last_name'] = data['last_name']

        logger.info("Logging in as Label Head Persona")
        st.switch_page('pages/30_Label_Head_Home.py')