import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(page_title="Browse Discounts", layout="wide")
SideBarLinks(show_home=True)

if "student_discounts" not in st.session_state:
    st.session_state.student_discounts = [
        {"id":201,"store":"Cafe 123","item":"Coffee","percent":15,"category":"Food","end":"2025-04-30"},
        {"id":202,"store":"Uni Books","item":"Textbook","percent":25,"category":"Books","end":"2025-05-15"},
        {"id":203,"store":"Gym Gear","item":"Yoga Mat","percent":20,"category":"Fitness","end":"2025-04-25"},
        {"id":204,"store":"Tech Hub","item":"USB Drive","percent":10,"category":"Tech","end":"2025-05-01"},
        {"id":205,"store":"Cloth Co","item":"T-Shirt","percent":30,"category":"Clothing","end":"2025-04-28"}
    ]

deals = st.session_state.student_discounts

search_store = st.text_input("🔎 Search Store")
cats = ["All"] + sorted({d["category"] for d in deals})
choice = st.selectbox("📂 Category", cats)

filtered = deals
if choice != "All":
    filtered = [d for d in filtered if d["category"] == choice]
if search_store:
    filtered = [d for d in filtered if search_store.lower() in d["store"].lower()]

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

st.title("🔍 Browse Discounts")
st.markdown(f"### 🎯 {len(filtered)} Deals Found")

for d in filtered:
    key = f"bk_{d['id']}"
    with st.expander(f"{d['store']} — {d['percent']}% off {d['item']}"):
        st.write(f"**Category:** {d['category']}")
        st.write(f"**Expires:** {d['end']}")
        if d["id"] in st.session_state.bookmarks:
            st.success("✅ Bookmarked")
        else:
            if st.button("⭐ Bookmark", key=key):
                st.session_state.bookmarks.append(d["id"])
                st.success("Saved!")

st.markdown("---")
st.caption("CampusPerks • Helping you save smarter.")
