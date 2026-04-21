import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

import requests

st.set_page_config(layout='wide')

SideBarLinks()

st.title(f"Artist Stats")

artist_id = st.session_state.get('artist_id')

try:
    stream_resp = requests.get(f"http://web-api:4000/artists/{artist_id}/streaming-stats")

    plat_resp = requests.get(
        f"http://web-api:4000/artists/{artist_id}/platforms")

    
    
    if stream_resp.status_code == 200 and plat_resp.status_code == 200:
        streaming_data = stream_resp.json()
        platform_data = plat_resp.json()

        st.subheader("💰 Earnings Summary")
        if isinstance(platform_data, list) and len(platform_data) > 0:
            total_rev = sum(float(item['total_revenue']) for item in platform_data if item['total_revenue'] is not None)
            st.metric(label="Total Lifetime Revenue", value=f"${total_rev:,.2f}")
        else:
            st.info("No revenue data recorded yet.")

        st.divider()

        st.subheader("💿 Track Performance (Monthly)")
        if streaming_data:
            df_streams = pd.DataFrame(streaming_data)
            chart_data = df_streams.pivot_table(
                index='month', 
                columns='title', 
                values='total_streams', 
                aggfunc='sum'
            ).fillna(0)
            st.bar_chart(chart_data)
        else:
            st.info("No streaming history found.")

        st.divider()

        st.subheader("🌐 Top Platforms by Earnings")
        if isinstance(platform_data, list) and len(platform_data) > 0:
            df_plat = pd.DataFrame(platform_data)
            st.table(df_plat[['platform_name', 'total_streams', 'total_revenue']].rename(columns={
                'platform_name': 'Platform',
                'total_streams': 'Streams',
                'total_revenue': 'Earnings ($)'
            }))
        else:
            st.info("No platform breakdown available.")
            
    else:
        st.error(f"Failed to fetch data (Status: {stream_resp.status_code}, {plat_resp.status_code})")

except Exception as e:
    st.error(f"Connection error: {e}")