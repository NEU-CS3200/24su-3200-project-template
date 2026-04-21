import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# Ensure an artist is selected
if 'selected_artist_id' not in st.session_state:
    st.warning("Please select an artist from the Manager Dashboard first.")
    st.stop()

artist_id = st.session_state['selected_artist_id']
user_id = st.session_state['user_id']
artist_name = st.session_state['selected_artist_name']

st.title(f"Platform Metrics: {artist_name}")

try:
    # Call the API endpoint we built earlier
    response = requests.get(f"http://web-api:4000/artists/{artist_id}/platforms?user_id={user_id}")
    
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            
            # Create two columns for the charts
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Streams by Platform")
                # Plotly Pie Chart for Streams
                fig_streams = px.pie(df, values='total_streams', names='platform_name', hole=0.4)
                st.plotly_chart(fig_streams, use_container_width=True)
                
            with col2:
                st.subheader("Revenue by Platform ($)")
                # Plotly Bar Chart for Revenue
                fig_rev = px.bar(df, x='platform_name', y='total_revenue', color='platform_name')
                st.plotly_chart(fig_rev, use_container_width=True)
                
            # Raw Data Table
            st.write("### Raw Data")
            st.dataframe(df[['platform_name', 'total_streams', 'total_revenue']], use_container_width=True, hide_index=True)
        else:
            st.info("No streaming data available for this artist yet.")
    else:
        st.error("Failed to load platform data.")
except Exception as e:
    st.error(f"API Connection Error: {e}")