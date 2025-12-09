import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import time
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from modules.deactivated import require_active_account

if 'user_id' not in st.session_state:
    st.session_state['user_id'] = 5
require_active_account()

st.set_page_config(layout="wide")
SideBarLinks()
add_logo("assets/FitHublogo.png")

API_BASE = "http://api:4000/s"

st.title("📤 Post a New Listing")

st.subheader("Upload a New Listing")

user_id = st.session_state.get('user_id', 5)

with st.form("upload_listing_form", border=True):
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input("Title *", placeholder="e.g., Vintage Denim Jacket")
        category = st.selectbox(
            "Category *",
            options=["shoes", "t-shirt", "jacket", "dress", "jeans", "sweater", "coat", "skirt", "hoodie", "shirt", "blouse", "pants", "shorts", "top", "vest", "blazer", "tank top"]
        )
        size = st.selectbox(
            "Size *",
            options=["XS", "S", "M", "L", "XL", "XXL"]
        )
        condition = st.selectbox(
            "Condition *",
            options=["Excellent", "Very good", "Good", "Fair"]
        )
    
    with col2:
        description = st.text_area("Description *", placeholder="Describe your item...", height=150)
    
    st.markdown("---")
    
    # Tags selection
    tags_options = ["Y2K", "Chic", "Bohemian", "Preppy", "Retro", "Eclectic", "Sporty", "Edgy", "Minimalist", "Sophisticated", "Urban"]
    selected_tags = st.multiselect("Tags (optional)", options=tags_options, help="Select tags to help others find your item")
    
    st.markdown("---")
    
    submitted = st.form_submit_button("📤 Upload Listing", type="primary", use_container_width=True)
    
    if submitted:
        if not title or not description:
            st.error("Please fill in all required fields (marked with *)")
        else:
            try:
                # Automatically set type to "swap" for swapper listings
                item_type = "swap"
                
                upload_response = requests.post(
                    f"{API_BASE}/upload_listing/",
                    json={
                        "Title": title,
                        "Category": category,
                        "Description": description,
                        "Size": size,
                        "Type": item_type,
                        "Condition": condition,
                        "OwnerID": user_id,
                        "Tags": selected_tags if selected_tags else []
                    }
                )
                
                if upload_response.status_code == 200:
                    st.success(f"✅ Listing uploaded successfully! '{title}' is now available for swap.")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error(f"Failed to upload listing: {upload_response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Unable to connect to the server: {e}")

# Show user's current listings
st.markdown("---")
st.subheader("Your Current Listings")

try:
    my_listings_response = requests.get(f"{API_BASE}/my_items/{user_id}")
    all_listings = my_listings_response.json() if my_listings_response.status_code == 200 else []
    
    # Filter to show only available items (not in active trades)
    my_listings = [listing for listing in all_listings if listing.get('IsAvailable', 0) == 1]
    
    if my_listings:
        st.write(f"You have {len(my_listings)} item(s) listed:")
        with st.container(height=400, border=True):
            for listing in my_listings:
                
                with st.expander(f"{listing['Title']} - {listing.get('Size', 'N/A')} ({listing.get('Condition', 'N/A')})", expanded=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Category:** {listing.get('Category', 'N/A')}")
                        st.write(f"**Type:** {listing.get('Type', 'N/A')}")
                        st.write(f"**Size:** {listing.get('Size', 'N/A')}")
                        st.write(f"**Condition:** {listing.get('Condition', 'N/A')}")
                        st.write(f"**Status:** Available")
                    
                    with col2:
                        st.write(f"**Description:** {listing.get('Description', 'N/A')}")
                        if listing.get('Tags'):
                            st.write(f"**Tags:** {listing.get('Tags', 'None')}")
                        else:
                            st.write("**Tags:** None")
                        if listing.get('ListedAt'):
                            st.write(f"**Listed At:** {listing.get('ListedAt', 'N/A')}")
                        else:
                            st.write("**Listed At:** N/A")
    else:
        st.info("No open listings currently.")
except requests.exceptions.RequestException as e:
    st.error("Unable to load your listings.")
