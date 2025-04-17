import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(page_title="Student Dashboard", layout="wide")
SideBarLinks(show_home=True)

username = st.session_state.get("username", "guest_user")
first_name = st.session_state.get("first_name", "Student")

st.title(f"Welcome back, {first_name}! 🎓")
st.subheader("Find and save the best deals for your budget.")

st.markdown("### 🔧 Quick Actions")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔍 Browse Discounts"):
        st.switch_page("pages/11_Student_Browse_Discounts.py")
with c2:
    if st.button("📚 My Bookmarks"):
        st.switch_page("pages/12_Student_Bookmarked_Discounts.py")
with c3:
    if st.button("⏳ Expiring Soon"):
        st.switch_page("pages/13_Student_Available_Discounts.py")

st.info("Tip: Browse by category or store, then ⭐ bookmark to save deals.")
