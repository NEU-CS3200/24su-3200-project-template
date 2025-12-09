import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import time
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()
add_logo("assets/FitHublogo.png")

# Log swapper my swaps access
logger.info(f"My Swaps loaded by {st.session_state.get('first_name', 'Unknown')}")

API_BASE = "http://api:4000/s"

st.title('🔄 My Swaps & Tracking')
user_id = st.session_state.get('user_id', 5)

# Get swap tracking data
response = requests.get(f"{API_BASE}/track_swap/{user_id}")
if response.status_code == 200:
    try:
        swaps = response.json()
    except:
        swaps = []
else:
    swaps = []

if swaps:
    left_col, right_col = st.columns([2, 1])
    
    with right_col:
        st.subheader("Summary")
        with st.container(border=True):
            total_swaps = len(swaps)
            delivered = len([s for s in swaps if s.get('Status') == 'Delivered'])
            in_transit = len([s for s in swaps if s.get('Status') == 'In Transit'])
            pending = len([s for s in swaps if s.get('Status') == 'Pending'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Swaps", total_swaps)
                st.metric("In Transit", in_transit)
            with col2:
                st.metric("Delivered", delivered)
                st.metric("Pending", pending)
    
    with left_col:
        tab1, tab2, tab3 = st.tabs(["⏳ Pending", "📦 In Transit", "✅ Delivered"])
        
        with tab1:
            pending_swaps = [s for s in swaps if s.get('Status') == 'Pending']
            if pending_swaps:
                for swap in pending_swaps:
                    with st.container(border=True):
                        direction = swap.get('SwapDirection', 'Unknown')
                        st.write(f"**Swap #{swap['OrderID']}** - {direction}")
                        st.write(f"Created: {swap.get('CreatedAt', 'N/A')}")
                        
                        # Combined details dropdown
                        your_item = swap.get('YourItem')
                        their_item = swap.get('TheirItem')
                        with st.expander("📋 Item Details", expanded=False):
                            detail_col1, detail_col2 = st.columns(2)
                            
                            with detail_col1:
                                st.write("**Your Item**")
                                if your_item:
                                    if your_item.get('Category'):
                                        st.write(f"**Category:** {your_item['Category']}")
                                    if your_item.get('Size'):
                                        st.write(f"**Size:** {your_item['Size']}")
                                    if your_item.get('Condition'):
                                        st.write(f"**Condition:** {your_item['Condition']}")
                                    if your_item.get('Description'):
                                        st.write(f"**Description:** {your_item['Description']}")
                                    if your_item.get('Tags'):
                                        st.write(f"**Tags:** {your_item['Tags']}")
                            
                            with detail_col2:
                                st.write("**Their Item**")
                                if their_item:
                                    if their_item.get('Category'):
                                        st.write(f"**Category:** {their_item['Category']}")
                                    if their_item.get('Size'):
                                        st.write(f"**Size:** {their_item['Size']}")
                                    if their_item.get('Condition'):
                                        st.write(f"**Condition:** {their_item['Condition']}")
                                    if their_item.get('Description'):
                                        st.write(f"**Description:** {their_item['Description']}")
                                    if their_item.get('Tags'):
                                        st.write(f"**Tags:** {their_item['Tags']}")
                        
                        st.warning("Preparing to ship...")
                        
                        if direction == 'Sending':
                            if st.button("Cancel Swap", key=f"cancel_{swap['OrderID']}", type="secondary"):
                                cancel_response = requests.put(
                                    f"{API_BASE}/trades/{swap['OrderID']}/cancel",
                                    params={'user_id': user_id}
                                )
                                if cancel_response.status_code == 200:
                                    st.toast(f"Swap #{swap['OrderID']} cancelled", icon="🚫")
                                    time.sleep(1.5)
                                    st.rerun()
            else:
                st.info("No pending swaps")
        
        with tab2:
            in_transit_swaps = [s for s in swaps if s.get('Status') == 'In Transit']
            if in_transit_swaps:
                for swap in in_transit_swaps:
                    with st.container(border=True):
                        direction = swap.get('SwapDirection', 'Unknown')
                        st.write(f"**Swap #{swap['OrderID']}** - {direction}")
                        st.write(f"Shipped: {swap.get('DateShipped', 'N/A')}")
                        
                        if swap.get('Carrier') and swap.get('TrackingNum'):
                            st.caption(f"📦 {swap['Carrier']} - {swap['TrackingNum']}")
                        
                        # Combined details dropdown
                        your_item = swap.get('YourItem')
                        their_item = swap.get('TheirItem')
                        with st.expander("📋 Item Details", expanded=False):
                            detail_col1, detail_col2 = st.columns(2)
                            
                            with detail_col1:
                                st.write("**Your Item**")
                                if your_item:
                                    if your_item.get('Category'):
                                        st.write(f"**Category:** {your_item['Category']}")
                                    if your_item.get('Size'):
                                        st.write(f"**Size:** {your_item['Size']}")
                                    if your_item.get('Condition'):
                                        st.write(f"**Condition:** {your_item['Condition']}")
                                    if your_item.get('Description'):
                                        st.write(f"**Description:** {your_item['Description']}")
                                    if your_item.get('Tags'):
                                        st.write(f"**Tags:** {your_item['Tags']}")
                            
                            with detail_col2:
                                st.write("**Their Item**")
                                if their_item:
                                    if their_item.get('Category'):
                                        st.write(f"**Category:** {their_item['Category']}")
                                    if their_item.get('Size'):
                                        st.write(f"**Size:** {their_item['Size']}")
                                    if their_item.get('Condition'):
                                        st.write(f"**Condition:** {their_item['Condition']}")
                                    if their_item.get('Description'):
                                        st.write(f"**Description:** {their_item['Description']}")
                                    if their_item.get('Tags'):
                                        st.write(f"**Tags:** {their_item['Tags']}")
                        
                        st.info("Package is on its way!")
            else:
                st.info("No swaps currently in transit")
        
        with tab3:
            delivered_swaps = [s for s in swaps if s.get('Status') == 'Delivered']
            if delivered_swaps:
                for swap in delivered_swaps:
                    with st.container(border=True):
                        direction = swap.get('SwapDirection', 'Unknown')
                        st.write(f"**Swap #{swap['OrderID']}** - {direction}")
                        st.write(f"Delivered: {swap.get('DateArrived', 'N/A')}")
                        
                        if swap.get('Carrier') and swap.get('TrackingNum'):
                            st.caption(f"📦 {swap['Carrier']} - {swap['TrackingNum']}")
                        
                        # Combined details dropdown
                        your_item = swap.get('YourItem')
                        their_item = swap.get('TheirItem')
                        with st.expander("📋 Item Details", expanded=False):
                            detail_col1, detail_col2 = st.columns(2)
                            
                            with detail_col1:
                                st.write("**Your Item**")
                                if your_item:
                                    if your_item.get('Category'):
                                        st.write(f"**Category:** {your_item['Category']}")
                                    if your_item.get('Size'):
                                        st.write(f"**Size:** {your_item['Size']}")
                                    if your_item.get('Condition'):
                                        st.write(f"**Condition:** {your_item['Condition']}")
                                    if your_item.get('Description'):
                                        st.write(f"**Description:** {your_item['Description']}")
                                    if your_item.get('Tags'):
                                        st.write(f"**Tags:** {your_item['Tags']}")
                            
                            with detail_col2:
                                st.write("**Their Item**")
                                if their_item:
                                    if their_item.get('Category'):
                                        st.write(f"**Category:** {their_item['Category']}")
                                    if their_item.get('Size'):
                                        st.write(f"**Size:** {their_item['Size']}")
                                    if their_item.get('Condition'):
                                        st.write(f"**Condition:** {their_item['Condition']}")
                                    if their_item.get('Description'):
                                        st.write(f"**Description:** {their_item['Description']}")
                                    if their_item.get('Tags'):
                                        st.write(f"**Tags:** {their_item['Tags']}")
                        
                        st.success("Delivered!")
            else:
                st.info("No delivered swaps yet")

else:
    st.info("You have no swaps yet. Browse listings to initiate a swap!")
