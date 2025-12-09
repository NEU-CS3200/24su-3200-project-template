import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://api:4000/d"

st.title("🚨 Late Shipments Alert")

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("🗓️ Delayed Shipments")
    
    try:
        get_late_shipments = requests.get(f"{API_BASE}/shipments/delay")
        late_shipments_data = get_late_shipments.json()

        if late_shipments_data:
            if isinstance(late_shipments_data, list):
                st.error(f"**⚠️ {len(late_shipments_data)} shipments are overdue!**")
                
                with st.container(height=500, border=True):
                    for shipment in late_shipments_data:
                        with st.expander(f"📦 Shipment ID: {shipment.get('ShippingID', 'N/A')}", expanded=False):
                            cols = st.columns(2)
                            
                            with cols[0]:
                                st.write(f"**Shipping ID:** {shipment.get('ShippingID', 'N/A')}")
                                st.write(f"**Date Shipped:** {shipment.get('DateShipped', 'N/A')}")
                                st.write(f"**Date Arrived:** {shipment.get('DateArrived', 'Not yet')}")
                            
                            with cols[1]:
                                st.write(f"**Delivery Time:** {shipment.get('DeliveryTime', 'N/A')} days")
                                st.error("⚠️ Above average delivery time")
            else:
                st.write(late_shipments_data)
        else:
            st.success("✅ No late shipments! All deliveries are on time.")
            
    except Exception as e:
        st.error(f"Could not connect to database to get late shipments: {str(e)}")

with right_col:
    st.subheader("Shipment Stats")
    
    try:
        get_late_shipments = requests.get(f"{API_BASE}/shipments/delay")
        late_shipments_data = get_late_shipments.json()
        
        with st.container(border=True):
            if late_shipments_data and isinstance(late_shipments_data, list):
                df = pd.DataFrame(late_shipments_data)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Late Shipments", len(late_shipments_data))
                
                with col2:
                    if 'DeliveryTime' in df.columns:
                        avg_delay = df['DeliveryTime'].mean()
                        st.metric("Avg Delay", f"{avg_delay:.1f} days")
                
                st.divider()
                
                if 'DeliveryTime' in df.columns:
                    st.caption("Delivery Time Distribution")
                    st.bar_chart(df['DeliveryTime'], height=200)
            else:
                st.success("No delays!")
                
    except Exception as e:
        st.error("Could not load shipment statistics")

st.divider()

# Additional analysis
st.subheader("📈 Shipment Trends")

try:
    get_late_shipments = requests.get(f"{API_BASE}/shipments/delay")
    late_shipments_data = get_late_shipments.json()
    
    if late_shipments_data and isinstance(late_shipments_data, list):
        df = pd.DataFrame(late_shipments_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container(border=True):
                st.caption("Late Shipments Details")
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        with col2:
            with st.container(border=True):
                st.caption("Key Insights")
                
                if 'DeliveryTime' in df.columns:
                    max_delay = df['DeliveryTime'].max()
                    min_delay = df['DeliveryTime'].min()
                    
                    st.write(f"**Longest delay:** {max_delay} days")
                    st.write(f"**Shortest delay:** {min_delay} days")
                    st.write(f"**Total affected:** {len(df)} shipments")
                    
except Exception as e:
    st.error(f"Could not load shipment trends: {str(e)}")