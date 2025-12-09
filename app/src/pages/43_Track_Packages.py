import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://api:4000/t"

st.title('📍 Track My Packages')


user_id = st.session_state.get('user_id', 8)

try:
    response = requests.get(f"{API_BASE}/track_package/{user_id}")
    packages = response.json()
    
    if packages:

        tab1, tab2, tab3 = st.tabs(["📦 On The Way", "✅ Delivered", "⏳ Processing"])
        
        with tab1:
            in_transit = [p for p in packages if p.get('DateShipped') and not p.get('DateArrived')]
            
            if in_transit:
                st.subheader(f"{len(in_transit)} package(s) on the way")
                
                with st.container(height=500, border=True):
                    for pkg in in_transit:
                        with st.expander(f"📦 {pkg['Title']}", expanded=True):
                            cols = st.columns(2)
                            
                            with cols[0]:
                                st.write(f"**Order ID:** {pkg['OrderID']}")
                                st.write(f"**Carrier:** {pkg.get('Carrier', 'N/A')}")
                                st.write(f"**Tracking #:** {pkg.get('TrackingNum', 'N/A')}")
                            
                            with cols[1]:
                                st.write(f"**Shipped:** {pkg.get('DateShipped', 'N/A')}")
                                st.info("📦 Package is on its way!")
            else:
                st.info("No packages currently in transit.")
        
        with tab2:
            delivered = [p for p in packages if p.get('DateArrived')]
            
            if delivered:
                st.subheader(f"{len(delivered)} package(s) delivered")
                
                with st.container(height=500, border=True):
                    for pkg in delivered:
                        with st.expander(f"✅ {pkg['Title']}", expanded=False):
                            cols = st.columns(2)
                            
                            with cols[0]:
                                st.write(f"**Order ID:** {pkg['OrderID']}")
                                st.write(f"**Shipped:** {pkg.get('DateShipped', 'N/A')}")
                            
                            with cols[1]:
                                st.write(f"**Delivered:** {pkg.get('DateArrived', 'N/A')}")
                                st.success("✅ Delivered!")
            else:
                st.info("No delivered packages yet.")
        
        with tab3:
            processing = [p for p in packages if not p.get('DateShipped')]
            
            if processing:
                st.subheader(f"{len(processing)} order(s) being prepared")
                
                with st.container(height=500, border=True):
                    for pkg in processing:
                        with st.expander(f"⏳ {pkg['Title']}", expanded=False):
                            st.write(f"**Order ID:** {pkg['OrderID']}")
                            st.write(f"**Requested:** {pkg.get('RequestDate', 'N/A')}")
                            st.warning("⏳ Preparing to ship...")
            else:
                st.info("No orders currently processing.")
    else:
        st.info("No packages to track. Place an order to get started!")
        
except Exception as e:
    st.error(f"Could not connect to database to get package tracking: {str(e)}")