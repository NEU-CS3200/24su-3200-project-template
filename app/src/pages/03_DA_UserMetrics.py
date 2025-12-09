import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://api:4000/d"

st.title("📈 User Metrics & Analytics")

# User Growth by Demographics
st.subheader("User Growth by Demographics")

with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
    with col2:
        age_min = st.number_input("Min Age", min_value=0, max_value=110, value=18)
    with col3:
        age_max = st.number_input("Max Age", min_value=0, max_value=110, value=65)

    if st.button("Analyze Demographics", type="primary"):
        try:
            get_users_demo = requests.get(f"{API_BASE}/users/{gender}/{age_min}/{age_max}")
            users_data = get_users_demo.json()

            if users_data:
                st.success(f"✅ Found {len(users_data)} users")

                df = pd.DataFrame(users_data)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    with st.container(border=True):
                        st.dataframe(df, use_container_width=True, hide_index=True)
                
                with col2:
                    with st.container(border=True):
                        if 'Age' in df.columns:
                            st.caption("Age Distribution")
                            age_counts = df['Age'].value_counts().sort_index()
                            st.bar_chart(age_counts, height=300)
            else:
                st.info("No users found matching criteria")

        except Exception as e:
            st.error(f"Could not connect to database to get user demographic information: {str(e)}")

st.divider()

# All Users & Engagement Side by Side
col1, col2 = st.columns(2)

with col1:
    st.subheader("👤 All Users")
    
    try:
        get_users = requests.get(f"{API_BASE}/users")
        users_data = get_users.json()

        if users_data:
            with st.container(height=500, border=True):
                for user in users_data:
                    with st.expander(f"👤 {user.get('Name', 'User')}", expanded=False):
                        cols = st.columns(2)

                        with cols[0]:
                            st.write(f"**User ID:** {user.get('UserID', 'N/A')}")
                            st.write(f"**Email:** {user.get('Email', 'N/A')}")
                            st.write(f"**Phone:** {user.get('Phone', 'N/A')}")
                            st.write(f"**Gender:** {user.get('Gender', 'N/A')}")

                        with cols[1]:
                            st.write(f"**Address:** {user.get('Address', 'N/A')}")
                            st.write(f"**DOB:** {user.get('DOB', 'N/A')}")
                            st.write(f"**Role:** {user.get('Role', 'N/A')}")
                            
                            if user.get('IsActive'):
                                st.success("✅ Active")
                            else:
                                st.warning("⚠️ Inactive")
        else:
            st.info("No users found")
            
    except Exception as e:
        st.error(f"Could not connect to database to get users: {str(e)}")

with col2:
    st.subheader("📊 User Engagement")
    
    try:
        get_engagement = requests.get(f"{API_BASE}/users/engagement")
        engagement_data = get_engagement.json()

        if engagement_data:
            df = pd.DataFrame(engagement_data)
            
            with st.container(border=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Total Received", int(df['OrdersReceived'].sum()))
                with col2:
                    st.metric("Total Given", int(df['OrdersGiven'].sum()))
                
                st.divider()
                
                st.caption("Most Engaged Users")
                df['TotalOrders'] = df['OrdersReceived'] + df['OrdersGiven']
                top_users = df.nlargest(5, 'TotalOrders')
                chart_data = top_users[['OrdersReceived', 'OrdersGiven']].set_index(top_users['UserID'])
                st.bar_chart(chart_data, height=250)
            
            st.divider()
            
            with st.container(border=True):
                st.caption("Full Engagement Data")
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No engagement data available")
            
    except Exception as e:
        st.error(f"Could not connect to database to get engagement metrics: {str(e)}")