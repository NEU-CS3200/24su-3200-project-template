import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

# Page config and layout
st.set_page_config(page_title="Admin: Analytics Overview", layout="wide")
SideBarLinks(show_home=True)

st.title("📊 Platform Analytics")
st.caption("Usage insights for student engagement and business performance.")

# --- Simulated Bookmark Data (replace with API calls)
bookmarked_discounts = [
    {"code": "COFFEE20", "count": 42},
    {"code": "PASTRY10", "count": 27},
    {"code": "BOOKS15", "count": 33},
    {"code": "GYM50", "count": 19},
    {"code": "ESPRESSO25", "count": 13},
]

user_category_groups = [
    {"category": "Food", "users": 83},
    {"category": "Books", "users": 46},
    {"category": "Fitness", "users": 28},
    {"category": "Clothing", "users": 22},
    {"category": "Electronics", "users": 17},
]

# --- Section 1: Top Bookmarked Discounts
st.markdown("### ⭐ Most Popular Discounts")
bm_df = pd.DataFrame(bookmarked_discounts)
st.bar_chart(bm_df.set_index("code"))

# --- Section 2: User Preference by Category
st.markdown("### 🧑‍🎓 User Preferences by Category")
cat_df = pd.DataFrame(user_category_groups)
st.bar_chart(cat_df.set_index("category"))

# --- Summary Cards
st.markdown("### 📋 Summary Stats")
col1, col2 = st.columns(2)
with col1:
    st.metric("Top Discount", bm_df.sort_values(by="count", ascending=False).iloc[0]['code'])
    st.metric("Most Engaged Category", cat_df.sort_values(by="users", ascending=False).iloc[0]['category'])
with col2:
    st.metric("Total Discount Codes", len(bm_df))
    st.metric("Tracked Categories", len(cat_df))

st.markdown("---")
st.caption("CampusPerks • Analytics to help you grow smarter.")