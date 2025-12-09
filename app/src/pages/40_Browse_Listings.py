import streamlit as st
import requests
import time
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://api:4000/t"

st.title("👕 Browse Available Listings")

#FILTERS
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
            options=["All", "S", "M", "L"]
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

params = {}
if category_filter != "All":
    params['category'] = category_filter
if size_filter != "All":
    params['size'] = size_filter
if condition_filter:
    params['condition'] = ','.join(condition_filter)
if tags_filter:
    params['tags'] = ','.join(tags_filter)

if params:
    response = requests.get(f"{API_BASE}/listings/filter_takes", params=params)
else:
    response = requests.get(f"{API_BASE}/listings/filter_takes")

listings = response.json()

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
                    user_id = st.session_state.get('user_id', 8)
                    
                    check_response = requests.get(f"{API_BASE}/check_request/{user_id}/{item_id}")
                    is_requested = check_response.json().get('requested', False)
                    
                    if is_requested:
                        st.info("✅ Already requested")
                    else:
                        if st.button(f"Request Item", key=f"request_{item_id}", type="primary"):
                            response = requests.post(f"{API_BASE}/request_item", json={"item_id": item_id, "user_id": user_id})
                            if response.status_code == 201:
                                st.toast(f"Requested: {item['Title']}", icon="✅")
                                time.sleep(1.5)
                                st.rerun()

else:
    st.info("No listings found matching your criteria.")