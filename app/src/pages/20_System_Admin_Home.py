import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Welcome, {st.session_state.get('first_name', 'Rigby')} 🖥️")
st.write("### System Admin Dashboard — What would you like to do today?")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🚨 System Logs")
    st.write("View, filter, and update system activity logs. Monitor errors and track platform events in real time.")
    if st.button("View System Logs", type="primary", use_container_width=True):
        st.switch_page("pages/22_System_Logs.py")

with col2:
    st.subheader("🎟️ Help Requests")
    st.write("Review and resolve user-submitted help tickets. Assign admins and track resolution status.")
    if st.button("Manage Help Requests", type="primary", use_container_width=True):
        st.switch_page("pages/23_Help_Requests.py")

with col3:
    st.subheader("📊 Platform Monitor")
    st.write("Track releases currently in processing and see which artists are most active on the platform.")
    if st.button("Open Platform Monitor", type="primary", use_container_width=True):
        st.switch_page("pages/24_Platform_Monitor.py")
