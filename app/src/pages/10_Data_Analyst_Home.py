import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

st.title(f"Data Analyst Dashboard: {st.session_state['first_name']} {st.session_state['last_name']}")

# Fetch the user_id we set in Home.py
user_id = st.session_state.get('user_id')

if not user_id:
    st.error("User ID not found. Please log in again.")
    st.stop()

# Fetch Label-Wide Roster Performance (User Story 6)
st.write("### Roster Performance Overview")
try:
    response = requests.get(f"http://web-api:4000/users/{user_id}/artists/performance")
    if response.status_code == 200:
        roster_data = response.json()
        if roster_data:
            df = pd.DataFrame(roster_data)
            df = df[['stage_name', 'number_of_streams', 'number_of_listeners', 'number_of_active_releases']]
            df.columns = ['Artist', 'Total Streams', 'Unique Listeners', 'Active Releases']
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.write("### Deep Dive Analysis")
            st.write("Select an artist below to view their detailed metrics on the other pages.")
            
            artist_map = {artist['stage_name']: artist['artist_id'] for artist in roster_data}
            selected_artist_name = st.selectbox("Select Artist for Analysis:", options=list(artist_map.keys()))
            
            st.session_state['selected_artist_id'] = artist_map[selected_artist_name]
            st.session_state['selected_artist_name'] = selected_artist_name
            
        else:
            st.info("There are currently no artists assigned to your data analysis roster.")
    else:
        st.error(f"Failed to fetch roster data: {response.status_code}")
except Exception as e:
    st.error(f"API Connection Error: {e}")