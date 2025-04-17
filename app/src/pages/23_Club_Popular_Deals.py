import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(page_title="Popular Deals", layout="wide")
SideBarLinks(show_home=True)

if "club_popular" not in st.session_state:
    st.session_state.club_popular = [
        {"id": 301, "store": "Campus Cafe",       "item": "Latte",          "percent": 20, "saves": 50, "college": "Northeastern University"},
        {"id": 302, "store": "BU Beans",          "item": "Espresso",       "percent": 25, "saves": 45, "college": "Boston University"},
        {"id": 303, "store": "Harvard Bookstore", "item": "Coursepack",     "percent": 15, "saves": 30, "college": "Harvard University"},
        {"id": 304, "store": "Tech Hub",          "item": "USB Drive",      "percent": 10, "saves": 40, "college": "MIT"},
        {"id": 305, "store": "Campus Cafe",       "item": "Bagel",          "percent": 30, "saves": 35, "college": "Northeastern University"},
        {"id": 306, "store": "BU Bookstore",      "item": "Textbook Rental","percent": 18, "saves": 25, "college": "Boston University"}
    ]

colleges = ["All"] + sorted({d["college"] for d in st.session_state.club_popular})
choice = st.selectbox("Select College", colleges)

if choice == "All":
    filtered = st.session_state.club_popular
else:
    filtered = [d for d in st.session_state.club_popular if d["college"] == choice]

pop = sorted(filtered, key=lambda x: x["saves"], reverse=True)[:3]

st.title("🔥 Popular Deals Among Students")
st.markdown(f"### ⭐ Top {len(pop)} Saved Discounts for {choice}")

for d in pop:
    with st.expander(f"{d['store']} — {d['percent']}% off {d['item']}"):
        st.write(f"Saved **{d['saves']}** times by students at {d['college']}")

st.markdown("---")
st.caption("CampusPerks • Know what students love")
