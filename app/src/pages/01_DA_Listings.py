import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://api:4000/d"

st.title("📦 Listings & Category Stock")

# All Listings
st.subheader("All Available Listings")
try:
    get_listings = requests.get(f"{API_BASE}/listings")
    listings = get_listings.json()

    if listings:
        st.success(f"**{len(listings)} listings found**")
        
        with st.container(height=500, border=True):
            for listing in listings:
                with st.expander(f"🏷️ {listing.get('Title', listing.get('ListingID', 'Item'))}", expanded=False):
                    cols = st.columns(2)

                    items = list(listing.items())
                    mid = len(items) // 2
                    
                    with cols[0]:
                        for key, value in items[:mid]:
                            st.write(f"**{key}:** {value}")
                    
                    with cols[1]:
                        for key, value in items[mid:]:
                            st.write(f"**{key}:** {value}")
    else:
        st.info("No listings available")
        
except Exception as e:
    st.error(f"Could not connect to database to get listings: {str(e)}")

st.divider()

# Category Stock
st.subheader("👕 Category Stock Analysis")

col1, col2 = st.columns([1, 2])

with col1:
    try:
        get_listings_category = requests.get(f"{API_BASE}/listings/category")
        category_data = get_listings_category.json()

        if category_data:
            if isinstance(category_data, list):
                df = pd.DataFrame(category_data)
            elif isinstance(category_data, dict):
                df = pd.DataFrame([category_data])
            else:
                df = pd.DataFrame()

            if not df.empty:
                with st.container(border=True):
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # Summary metrics
                    st.divider()
                    total_items = df['AvailableListings'].sum() if 'AvailableListings' in df.columns else 0
                    st.metric("Total Available Items", int(total_items))
            else:
                st.info("No category data available")
        else:
            st.info("No category data available")
            
    except Exception as e:
        st.error(f"Could not connect to database to get category stock: {str(e)}")

with col2:
    try:
        get_listings_category = requests.get(f"{API_BASE}/listings/category")
        category_data = get_listings_category.json()

        if category_data and isinstance(category_data, list):
            df = pd.DataFrame(category_data)
            
            if not df.empty and 'Category' in df.columns and 'AvailableListings' in df.columns:
                with st.container(border=True):
                    st.caption("Category Distribution")
                    chart_data = df.set_index('Category')['AvailableListings']
                    st.bar_chart(chart_data, height=300)
            
    except Exception as e:
        st.error(f"Could not generate category chart: {str(e)}")