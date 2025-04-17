import streamlit as st
from modules.nav import SideBarLinks

if "club_discounts" not in st.session_state:
    st.session_state.club_discounts = [
        {"id": 201, "store": "Cafe 123",   "item": "Coffee",    "percent": 15, "category": "Food"},
        {"id": 202, "store": "Uni Books",   "item": "Textbook",  "percent": 25, "category": "Books"},
        {"id": 203, "store": "Club Shop",  "item": "Trophy",    "percent": 10, "category": "Merch"},
        {"id": 204, "store": "Tech Store", "item": "USB Drive", "percent": 20, "category": "Tech"},
        {"id": 205, "store": "Spirit Wear","item": "T-Shirt",   "percent": 30, "category": "Merch"},
    ]

if "club_stores_info" not in st.session_state:
    st.session_state.club_stores_info = [
        {"name": "Cafe 123",   "address": "123 College Ave, Boston, MA", "phone": "617‑555‑1001", "website": "cafe123.example.com"},
        {"name": "Uni Books",   "address": "456 Campus Rd, Boston, MA",  "phone": "617‑555‑1002", "website": "unibooks.example.com"},
        {"name": "Club Shop",  "address": "789 Club Ln, Boston, MA",    "phone": "617‑555‑1003", "website": "clubshop.example.com"},
        {"name": "Tech Store", "address": "321 Tech Pkwy, Boston, MA",   "phone": "617‑555‑1004", "website": "techhub.example.com"},
        {"name": "Spirit Wear","address": "654 Spirit St, Boston, MA",   "phone": "617‑555‑1005", "website": "spiritwear.example.com"},
    ]

st.set_page_config(page_title="Filter Discounts", layout="wide")
SideBarLinks(show_home=True)

if st.button("📋 Show All Stores"):
    st.markdown("### 🏬 All CampusPerks Stores")
    for s in st.session_state.club_stores_info:
        st.markdown(f"**{s['name']}**  \n- Address: {s['address']}  \n- Phone: {s['phone']}  \n- Web: {s['website']}")
    st.markdown("---")

st.title("🔍 Filter Discounts by Category")

cats = ["All"] + sorted({d["category"] for d in st.session_state.club_discounts})
choice = st.selectbox("Category", cats)

if choice == "All":
    filtered = st.session_state.club_discounts
else:
    filtered = [d for d in st.session_state.club_discounts if d["category"] == choice]

st.markdown(f"### 🎯 {len(filtered)} Discounts Found")

if filtered:
    for d in filtered:
        key_info = f"info_{d['id']}"
        with st.expander(f"{d['store']} — {d['percent']}% off {d['item']} ({d['category']})"):
            st.write(f"**Store:** {d['store']}")
            st.write(f"**Item:** {d['item']}")
            st.write(f"**Discount:** {d['percent']}%")
            if st.checkbox("Show Store Info", key=key_info):
                info = next((s for s in st.session_state.club_stores_info if s["name"] == d["store"]), None)
                if info:
                    st.write(f"• Address: {info['address']}")
                    st.write(f"• Phone: {info['phone']}")
                    st.write(f"• Website: {info['website']}")
else:
    st.info("No discounts match this category.")

st.markdown("---")
st.caption("CampusPerks • Helping clubs save on event essentials")
