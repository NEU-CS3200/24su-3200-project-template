import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(page_title="Admin Dashboard", layout="wide")
SideBarLinks(show_home=True)

st.title("🛡️ Welcome, John!")
st.subheader("Manage users, monitor activity, and optimize platform performance.")

# 🔧 Dashboard Navigation Buttons
st.markdown("### 🧭 Quick Actions")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/41_Admin_User_Interactions.py", label="View Interactions", icon="🧾")
with col2:
    st.page_link("pages/42_Admin_Analytics_Overview.py", label="Analytics Overview", icon="👥")
with col3:
    st.page_link("pages/43_Admin_Discount_Manager.py", label="Discount Manager", icon="📊")

# 💡 Tip Section
st.info("Tip: Use this dashboard to audit engagement, keep user info up to date, and monitor discount effectiveness.")

# 📌 Quick Stats (optional, placeholder version)
st.markdown("---")
st.markdown("### 📋 At a Glance")
col4, col5 = st.columns(2)
with col4:
    st.metric("Total Registered Users", "4")
    st.metric("Total Discounts", "2 Active")
with col5:
    st.metric("Recent Bookmarks", "5+")
    st.metric("Engaged Categories", "5")

# Footer
st.markdown("---")
st.caption("CampusPerks • Admin dashboard for full visibility and control.")