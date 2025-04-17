import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd

# Page config and sidebar links
st.set_page_config(page_title="Business Owner Dashboard", layout="wide")
SideBarLinks(show_home=True)

# Page title
st.title("Welcome, Beth! 👋")
st.subheader("Your Business Dashboard")

# Feature navigation buttons
st.markdown("### 🧰 Discount Tools")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("➕ Add/Update Discounts"):
        st.switch_page("pages/31_Business_Manage_Discounts.py")
with col2:
    if st.button("🎓 View College Bookmarks"):
        st.switch_page("pages/32_Business_College_Insights.py")
with col3:
    if st.button("🛑 Manage Active Discounts"):
        st.switch_page("pages/33_Business_Manage_Active_Status.py")


# --- Analytics Section ---
st.markdown("### 📊 Discount Performance")

# Simulated data from 32_Business_Analytics.py
discount_data = [
    {"Discount Code": "COFFEE20", "Item": "Latte", "Views": 124},
    {"Discount Code": "MUFFIN10", "Item": "Blueberry Muffin", "Views": 87},
    {"Discount Code": "ESPRESSO25", "Item": "Espresso", "Views": 193}
]

df = pd.DataFrame(discount_data)
st.dataframe(df, use_container_width=True)

# --- Targeting Insights ---
st.markdown("### 🎯 College Engagement Insights")
st.success("You have high interest from: Northeastern University and Boston University. Consider targeting new offers here!")

# --- Footer ---
st.markdown("---")
st.caption("CampusPerks • Empowering small businesses to connect with students")