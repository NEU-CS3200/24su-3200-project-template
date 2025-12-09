import streamlit as st
import requests
import time
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://api:4000/t"

st.title('📦 My Orders & Tracking')
user_id = st.session_state.get('user_id', 8)

response = requests.get(f"{API_BASE}/track_package/{user_id}")
if response.status_code == 200:
    try:
        orders = response.json()
    except:
        orders = []
else:
    orders = []

if orders:
    left_col, right_col = st.columns([2, 1])
    
    with right_col:
        st.subheader("📊 Summary")
        with st.container(border=True):
            total_orders = len(orders)
            delivered = len([o for o in orders if o.get('DateArrived')])
            in_transit = len([o for o in orders if o.get('DateShipped') and not o.get('DateArrived')])
            processing = len([o for o in orders if not o.get('DateShipped')])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total", total_orders)
                st.metric("In Transit", in_transit)
            with col2:
                st.metric("Delivered", delivered)
                st.metric("Processing", processing)
    
    with left_col:
        tab1, tab2, tab3 = st.tabs(["⏳ Processing", "📦 In Transit", "✅ Delivered"])
        
        with tab1:
            processing_orders = [o for o in orders if not o.get('DateShipped')]
            if processing_orders:
                for order in processing_orders:
                    with st.container(border=True):
                        st.write(f"**{order['Title']}**")
                        st.write(f"Order #{order['OrderID']} | Requested: {order['RequestDate']}")
                        
                        with st.expander("📋 Item Details", expanded=False):
                            cols = st.columns(2)
                            with cols[0]:
                                if order.get('Category'):
                                    st.write(f"**Category:** {order['Category']}")
                                if order.get('Size'):
                                    st.write(f"**Size:** {order['Size']}")
                                if order.get('Condition'):
                                    st.write(f"**Condition:** {order['Condition']}")
                            with cols[1]:
                                if order.get('Description'):
                                    st.write(f"**Description:** {order['Description']}")
                                if order.get('Tags'):
                                    st.write(f"**Tags:** {order['Tags']}")
                        
                        cols = st.columns([3, 1])
                        with cols[0]:
                            st.warning("⏳ Preparing to ship...")
                        with cols[1]:
                            if st.button("Cancel", key=f"cancel_{order['OrderID']}", type="secondary"):
                                cancel_response = requests.delete(f"{API_BASE}/orders/{order['OrderID']}", params={'user_id': user_id})
                                if cancel_response.status_code == 200:
                                    st.toast(f"Request cancelled: {order['Title']}", icon="🚫")
                                    time.sleep(1.5)
                                    st.rerun()
            else:
                st.info("No orders currently processing")
        
        with tab2:
            in_transit_orders = [o for o in orders if o.get('DateShipped') and not o.get('DateArrived')]
            if in_transit_orders:
                for order in in_transit_orders:
                    with st.container(border=True):
                        st.write(f"**{order['Title']}**")
                        st.write(f"Order #{order['OrderID']} | Shipped: {order.get('DateShipped', 'N/A')}")
                        if order.get('Carrier') and order.get('TrackingNum'):
                            st.caption(f"📦 {order['Carrier']} - {order['TrackingNum']}")
                        
                        with st.expander("📋 Item Details", expanded=False):
                            cols = st.columns(2)
                            with cols[0]:
                                if order.get('Category'):
                                    st.write(f"**Category:** {order['Category']}")
                                if order.get('Size'):
                                    st.write(f"**Size:** {order['Size']}")
                                if order.get('Condition'):
                                    st.write(f"**Condition:** {order['Condition']}")
                            with cols[1]:
                                if order.get('Description'):
                                    st.write(f"**Description:** {order['Description']}")
                                if order.get('Tags'):
                                    st.write(f"**Tags:** {order['Tags']}")
                        
                        st.info("📦 Package is on its way!")
            else:
                st.info("No packages currently in transit")
        
        with tab3:
            delivered_orders = [o for o in orders if o.get('DateArrived')]
            if delivered_orders:
                for order in delivered_orders:
                    with st.container(border=True):
                        st.write(f"**{order['Title']}**")
                        st.write(f"Order #{order['OrderID']} | Delivered: {order['DateArrived']}")
                        if order.get('Carrier') and order.get('TrackingNum'):
                            st.caption(f"📦 {order['Carrier']} - {order['TrackingNum']}")
                        
                        with st.expander("📋 Item Details", expanded=False):
                            cols = st.columns(2)
                            with cols[0]:
                                if order.get('Category'):
                                    st.write(f"**Category:** {order['Category']}")
                                if order.get('Size'):
                                    st.write(f"**Size:** {order['Size']}")
                                if order.get('Condition'):
                                    st.write(f"**Condition:** {order['Condition']}")
                            with cols[1]:
                                if order.get('Description'):
                                    st.write(f"**Description:** {order['Description']}")
                                if order.get('Tags'):
                                    st.write(f"**Tags:** {order['Tags']}")
                        
                        st.success("✅ Delivered!")
            else:
                st.info("No delivered orders yet")

else:
    st.info("You have no orders yet. Browse listings to get started!")