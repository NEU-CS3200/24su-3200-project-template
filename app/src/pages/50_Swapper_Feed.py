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

# Log swapper feed access
logger.info(f"Swapper Feed loaded by {st.session_state.get('first_name', 'Unknown')}")

API_BASE = "http://api:4000/s"

st.title("👕 Swapper Feed")

# BROWSE LISTINGS
st.subheader("Filter Listings")
with st.container(border=True):
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            category_filter = st.selectbox(
                "Select Category",
                options=["All", "shoes", "t-shirt", "jacket", "dress", "jeans", "sweater", "coat", "skirt", "hoodie", "shirt", "blouse", "pants", "shorts", "top", "vest", "blazer", "tank top"]
            )

        with col2:
            size_filter = st.selectbox(
                "Select Size",
                options=["All", "XS", "S", "M", "L", "XL", "XXL"]
            )

        with col3:
            condition_filter = st.multiselect(
                "Select Condition(s)",
                options=["Excellent", "Very good", "Good", "Fair"]
            )

        with col4:
            tags_filter = st.multiselect(
                "Select Tags",
                options=["Y2K", "Chic", "Bohemian", "Preppy", "Retro", "Eclectic", "Sporty", "Edgy", "Minimalist", "Sophisticated", "Urban"]
            )

user_id = st.session_state.get('user_id', 5)

params = {}
if category_filter != "All":
    params['category'] = category_filter
if size_filter != "All":
    params['size'] = size_filter
if condition_filter:
    params['condition'] = ','.join(condition_filter)
if tags_filter:
    params['tags'] = ','.join(tags_filter)

# exclude user's own items
if params:
    params['user_id'] = user_id
    response = requests.get(f"{API_BASE}/listings/filter_swaps", params=params)
else:
    #no filters applied
    response = requests.get(f"{API_BASE}/listings/filter_swaps", params={'user_id': user_id})

try:
    if response.status_code == 200:
        listings = response.json()
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        listings = []
except Exception as e:
    st.error(f"Error parsing response: {e}")
    listings = []


if listings:
    st.success(f"Found {len(listings)} listings matching your criteria.")

    # Category emoji mapping
    category_emojis = {
        'shoes': '👟',
        't-shirt': '👕',
        'jacket': '🧥',
        'dress': '👗',
        'jeans': '👖',
        'sweater': '🧶',
        'coat': '🧥',
        'skirt': '👗',
        'hoodie': '🧥',
        'shirt': '👔',
        'blouse': '👔',
        'pants': '👖',
        'shorts': '🩳',
        'top': '👚',
        'vest': '🎽',
        'blazer': '👔',
        'tank top': '👕'
    }
    
    def get_category_emoji(category):
        if category:
            category_lower = str(category).lower()
            return category_emojis.get(category_lower, '👕')
        return '👕'

    with st.container(height = 600, border = True):
        for item in listings:
            category = item.get('Category', '')
            emoji = get_category_emoji(category)
            with st.expander(f"{emoji} {item.get('Title', 'Item')}", expanded=False):
                cols = st.columns(2)
                with cols[0]:
                    st.write(f"**Category:** {item.get('Category', 'N/A')}")
                    st.write(f"**Description:** {item.get('Description', 'N/A')}")
                    st.write(f"**Size:** {item.get('Size', 'N/A')}")
                    st.write(f"**Condition:** {item.get('Condition', 'N/A')}")
                with cols[1]:
                    st.write(f"**Owner:** {item.get('OwnerName', 'N/A')}")
                    st.write(f"**Tags:** {item.get('Tags', 'N/A')}")
                    st.write(f"**Listed At:** {item.get('ListedAt', 'N/A')}")

                item_id = item.get('ItemID')
                user_id = st.session_state.get('user_id', 5)
                
                if st.button(f"Initiate Swap", key=f"swap_{item_id}", type="primary"):
                    # Store the desired item in session state to show swap modal
                    st.session_state['swap_desired_item_id'] = item_id
                    st.session_state['swap_desired_item'] = item
                    st.rerun()
                
                # Show swap modal if an item was selected
                if 'swap_desired_item_id' in st.session_state and st.session_state.get('swap_desired_item_id') == item_id:
                    with st.container(border=True):
                        st.write(f"**Swap for: {item.get('Title', 'Item')}**")
                        
                        # Get user's available items for swap
                        try:
                            my_items_response = requests.get(f"{API_BASE}/my_items/{user_id}")
                            my_items = my_items_response.json() if my_items_response.status_code == 200 else []
                            
                            if my_items:
                                st.write("**Select one of your items to swap:**")
                                
                                # Display items in a more user-friendly way
                                for idx, my_item in enumerate(my_items):
                                    with st.container(border=True):
                                        col1, col2 = st.columns([3, 1])
                                        with col1:
                                            st.write(f"**{my_item['Title']}**")
                                            st.write(f"Category: {my_item.get('Category', 'N/A')} | Size: {my_item.get('Size', 'N/A')} | Condition: {my_item.get('Condition', 'N/A')}")
                                            if my_item.get('Description'):
                                                st.caption(my_item['Description'])
                                        with col2:
                                            if st.button("Select", key=f"select_{item_id}_{my_item['ItemID']}", type="primary"):
                                                # Initiate swap with selected item
                                                swap_response = requests.post(
                                                    f"{API_BASE}/initiate_swap/",
                                                    json={
                                                        "desired_item_id": item_id,
                                                        "offered_item_id": my_item['ItemID'],
                                                        "requester_id": user_id
                                                    }
                                                )
                                                if swap_response.status_code == 201:
                                                    st.success(f"Swap request sent for: {item['Title']}")
                                                    del st.session_state['swap_desired_item_id']
                                                    del st.session_state['swap_desired_item']
                                                    time.sleep(1.5)
                                                    st.rerun()
                                                else:
                                                    st.error(f"Failed to initiate swap: {swap_response.text}")
                                
                                if st.button("Cancel", key=f"cancel_swap_{item_id}"):
                                    del st.session_state['swap_desired_item_id']
                                    del st.session_state['swap_desired_item']
                                    st.rerun()
                            else:
                                st.warning("⚠️ You don't have any items available for swap.")
                                st.info("Go to 'Post Listing' to upload an item first!")
                                if st.button("Close", key=f"close_{item_id}"):
                                    del st.session_state['swap_desired_item_id']
                                    del st.session_state['swap_desired_item']
                                    st.rerun()
                        except requests.exceptions.RequestException as e:
                            st.error("Unable to connect to the server.")

else:
    st.info("No listings found matching your criteria.")
