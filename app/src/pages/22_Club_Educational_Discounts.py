import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import datetime

st.set_page_config(page_title="Educational Discounts", layout="wide")
SideBarLinks(show_home=True)

username = st.session_state.get("username", "guest_user")
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

try:
    resp = requests.get("http://localhost:5000/api/discounts", params={"category": "books"})
    resp.raise_for_status()
    edu_discounts = resp.json()
except:
    edu_discounts = [
        {"discountId": 301, "storeId": 11, "storeName": "Campus Bookstore",    "percentOff": 20, "item": "Algorithms Text",      "startDate": "2025-04-01", "endDate": "2025-05-01", "college": "Northeastern University"},
        {"discountId": 302, "storeId": 12, "storeName": "Academic Press",      "percentOff": 15, "item": "Linear Algebra",        "startDate": "2025-04-05", "endDate": "2025-05-05", "college": "Boston University"},
        {"discountId": 303, "storeId": 13, "storeName": "Scholars Shop",       "percentOff": 25, "item": "Data Science Manual",   "startDate": "2025-04-10", "endDate": "2025-06-01", "college": "Harvard University"},
        {"discountId": 304, "storeId": 14, "storeName": "Tech Texts",          "percentOff": 10, "item": "Python Programming",    "startDate": "2025-04-01", "endDate": "2025-04-30", "college": "MIT"},
        {"discountId": 305, "storeId": 15, "storeName": "Engineering Emporium","percentOff": 30, "item": "Circuit Analysis",      "startDate": "2025-04-12", "endDate": "2025-05-12", "college": "Northeastern University"},
        {"discountId": 306, "storeId": 16, "storeName": "Book Haven",          "percentOff": 18, "item": "Organic Chemistry",     "startDate": "2025-04-15", "endDate": "2025-05-15", "college": "Boston University"},
        {"discountId": 307, "storeId": 17, "storeName": "Campus Bookstore",    "percentOff": 22, "item": "Discrete Math",         "startDate": "2025-04-18", "endDate": "2025-05-18", "college": "Harvard University"},
        {"discountId": 308, "storeId": 18, "storeName": "Scholars Shop",       "percentOff": 12, "item": "Statistics 101",        "startDate": "2025-04-20", "endDate": "2025-05-20", "college": "MIT"},
        {"discountId": 309, "storeId": 19, "storeName": "Academic Press",      "percentOff": 28, "item": "Database Systems",      "startDate": "2025-04-22", "endDate": "2025-06-01", "college": "Northeastern University"},
        {"discountId": 310, "storeId": 20, "storeName": "Tech Texts",          "percentOff": 16, "item": "AI Fundamentals",       "startDate": "2025-04-25", "endDate": "2025-05-25", "college": "Boston University"},
    ]

try:
    sr = requests.get("http://localhost:5000/api/stores")
    sr.raise_for_status()
    stores = sr.json()
except:
    stores = [
        {"storeId":11,"name":"Campus Bookstore","locationStreet":"360 Huntington Ave","locationCity":"Boston","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1001","website":"campusbooks.edu"},
        {"storeId":12,"name":"Academic Press",  "locationStreet":"123 College Rd",   "locationCity":"Boston","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1002","website":"acadpress.com"},
        {"storeId":13,"name":"Scholars Shop",   "locationStreet":"500 Scholar Ln",   "locationCity":"Cambridge","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1003","website":"scholarshop.org"},
        {"storeId":14,"name":"Tech Texts",      "locationStreet":"1 Tech Way",       "locationCity":"Cambridge","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1004","website":"techtexts.io"},
        {"storeId":15,"name":"Engineering Emporium","locationStreet":"75 Engr Pl","locationCity":"Boston","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1005","website":"engemporium.com"},
        {"storeId":16,"name":"Book Haven",      "locationStreet":"42 Haven St",      "locationCity":"Boston","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1006","website":"bookhaven.net"},
        {"storeId":17,"name":"Campus Bookstore","locationStreet":"360 Huntington Ave","locationCity":"Boston","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1001","website":"campusbooks.edu"},
        {"storeId":18,"name":"Scholars Shop",   "locationStreet":"500 Scholar Ln",   "locationCity":"Cambridge","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1003","website":"scholarshop.org"},
        {"storeId":19,"name":"Academic Press",  "locationStreet":"123 College Rd",   "locationCity":"Boston","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1002","website":"acadpress.com"},
        {"storeId":20,"name":"Tech Texts",      "locationStreet":"1 Tech Way",       "locationCity":"Cambridge","locationState":"MA","locationCountry":"USA","phoneNo":"617-555-1004","website":"techtexts.io"},
    ]

colleges = ["All"] + sorted({d["college"] for d in edu_discounts})
college_choice = st.selectbox("Filter by College", colleges)

filtered = edu_discounts if college_choice == "All" else [d for d in edu_discounts if d["college"] == college_choice]

st.title("📚 Educational Discounts")
st.markdown(f"### 🎯 {len(filtered)} Discounts Found")

for d in filtered:
    did = d["discountId"]
    sid = d["storeId"]
    with st.expander(f"{d['storeName']} — {d['percentOff']}% off {d['item']}"):
        st.write(f"**College:** {d['college']}")
        st.write(f"**Expires:** {d['endDate']}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("📍 Store Info", key=f"info_{did}"):
                store = next((s for s in stores if s["storeId"] == sid), None)
                if store:
                    st.write(f"{store['name']}")
                    st.write(f"{store['locationStreet']}, {store['locationCity']}, {store['locationState']}")
                    st.write(f"📞 {store['phoneNo']}   🌐 {store['website']}")
                else:
                    st.write("Store information not available.")
        with c2:
            if did in st.session_state.bookmarks:
                st.success("✅ Bookmarked")
            elif st.button("⭐ Bookmark", key=f"bm_{did}"):
                st.session_state.bookmarks.append(did)
                try:
                    requests.post(
                        "http://localhost:5000/api/savedDiscounts",
                        json={"username": username, "discountId": did}
                    )
                except:
                    pass
                st.success("Saved!")

st.markdown("---")
st.caption("CampusPerks • Fueling your club’s learning")
