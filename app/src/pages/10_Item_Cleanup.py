import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()
add_logo("assets/FitHublogo.png")
user_id = st.session_state.get('user_id', 1)
API_BASE = "http://api:4000/admin"

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    max-width: 95%;
}

.page-title {
    color: #328E6E;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}

.section-title {
    color: #328E6E;
    font-size: 26px;
    font-weight: 600;
    margin-top: 20px;
}

div.stButton > button {
    background-color: #328E6E;
    color: #E1EEBC;
    height: 3.5em;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}

div.stButton > button:hover {
    background-color: #2a7359;
}

</style>
""", unsafe_allow_html=True)

st.title("🧹 Item Cleanup")

tab1, tab2 = st.tabs(["All Items", "Duplicate Items"])
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

# TAB 1: ALL ITEMS
with tab1:
    st.markdown('<div class="section-title">All listings</div>', unsafe_allow_html=True)

    try:
        response = requests.get(f"{API_BASE}/items")
        if response.status_code == 200:
            all_items = response.json()

            if all_items:
                st.success(f"Found {len(all_items)} total items in the system.")

                with st.container(height=600, border=True):
                    for item in all_items:
                        category = item.get('Category', '')
                        emoji = get_category_emoji(category)

                        with st.expander(f"{emoji} {item.get('Title', 'Item')} (ID: {item.get('ItemID', 'N/A')})", expanded=False):
                            cols = st.columns(2)
                            with cols[0]:
                                st.write(f"**Item ID:** {item.get('ItemID', 'N/A')}")
                                st.write(f"**Category:** {item.get('Category', 'N/A')}")
                                st.write(f"**Description:** {item.get('Description', 'N/A')}")
                                st.write(f"**Size:** {item.get('Size', 'N/A')}")
                                st.write(f"**Condition:** {item.get('Condition', 'N/A')}")
                            with cols[1]:
                                st.write(f"**Type:** {item.get('Type', 'N/A')}")
                                st.write(f"**Owner ID:** {item.get('OwnerID', 'N/A')}")
                                st.write(f"**Tags:** {item.get('Tags', 'N/A')}")
                                st.write(f"**Listed At:** {item.get('ListedAt', 'N/A')}")

                            # Delete button for this specific item
                            item_id = item.get('ItemID')
                            if st.button(f"Delete Item Now", key=f"delete_item_{item_id}", type="primary"):
                                try:
                                    delete_resp = requests.delete(f"{API_BASE}/items/{item_id}")
                                    if delete_resp.status_code == 200:
                                        st.success(f"Item {item_id} deleted successfully!")
                                        st.rerun()
                                    else:
                                        st.error(f"Error deleting item: {delete_resp.text}")
                                except Exception as e:
                                    st.error(f"Error deleting item: {e}")
            else:
                st.info("No items found in the system.")
        else:
            st.error(f"Error fetching items: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error connecting to server: {e}")

# TAB 2: DUPLICATE ITEMS
with tab2:
    st.markdown('<div class="section-title">Duplicate Items</div>', unsafe_allow_html=True)

    try:
        # Fetch duplicate items
        response = requests.get(f"{API_BASE}/items/duplicates")
        if response.status_code == 200:
            duplicate_items = response.json().get('data', [])  # ← FIXED HERE


            if duplicate_items:
                st.warning(f"Found {len(duplicate_items)} duplicate items that can be cleaned up.")

                with st.container(height=500, border=True):
                    for item in duplicate_items:
                        category = item.get('Category', '')
                        emoji = get_category_emoji(category)

                        with st.expander(f"{emoji} {item.get('Title', 'Item')} (ID: {item.get('ItemID', 'N/A')}) - Duplicate", expanded=False):
                            cols = st.columns(2)
                            with cols[0]:
                                st.write(f"**Item ID:** {item.get('ItemID', 'N/A')}")
                                st.write(f"**Category:** {item.get('Category', 'N/A')}")
                                st.write(f"**Description:** {item.get('Description', 'N/A')}")
                                st.write(f"**Size:** {item.get('Size', 'N/A')}")
                                st.write(f"**Condition:** {item.get('Condition', 'N/A')}")
                            with cols[1]:
                                st.write(f"**Type:** {item.get('Type', 'N/A')}")
                                st.write(f"**Owner ID:** {item.get('OwnerID', 'N/A')}")
                                st.write(f"**Duplicate Count:** {item.get('DuplicateCount', 'N/A')}")

                # Delete all duplicates button
                st.markdown("---")
                if st.button("Delete Duplicate Items", use_container_width=True, type="primary"):
                    try:
                        delete_resp = requests.delete(f"{API_BASE}/items/duplicates")
                        if delete_resp.status_code == 200:
                            result = delete_resp.json()
                            st.success(f"Successfully removed {result.get('deleted_count', 0)} duplicate item(s)!")
                            st.rerun()
                        else:
                            st.error(f"Error deleting duplicates: {delete_resp.text}")
                    except Exception as e:
                        st.error(f"Error deleting duplicates: {e}")
            else:
                st.success("No duplicate items found!")
        else:
            st.error(f"Error fetching duplicates: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Error connecting to server: {e}")
