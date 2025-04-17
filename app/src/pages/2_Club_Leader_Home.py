import streamlit as st
from modules.nav import SideBarLinks

# Page config and sidebar links
st.set_page_config(page_title="Club Leader Dashboard", layout="wide")
SideBarLinks(show_home=True)

# Greeting
st.title("Welcome, Glen! 🎉")
st.subheader("Plan great events and save money for your club!")

# Feature navigation buttons
st.markdown("### 🔧 Quick Actions")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔍 Filter Discounts by Category"):
        st.switch_page("pages/21_Club_Filter_Discounts.py")
with col2:
    if st.button("📚 View Educational Discounts"):
        st.switch_page("pages/22_Club_Educational_Discounts.py")
with col3:
    if st.button("🔥 See Popular Deals"):
        st.switch_page("pages/23_Club_Popular_Deals.py")

# Usage tip
st.info("Tip: Use bookmarks to save discounts while you browse and revisit them before events!")

# Coming soon teaser
st.markdown("---")
st.markdown("### 📅 Coming Soon for Club Leaders")
st.markdown("""
- Sort discounts by savings  
- Filter by food, merch, or educational category  
- See popular discounts used by students at your college  
- Save and review bookmarked discounts before making decisions  
""")

# Footer
st.markdown("---")
st.caption("CampusPerks • Helping clubs plan smarter, cheaper, and faster.")
