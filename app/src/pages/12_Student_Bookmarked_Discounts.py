import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(page_title="My Bookmarks", layout="wide")
SideBarLinks(show_home=True)

bks = st.session_state.get("bookmarks", [])
all_deals = st.session_state.get("student_discounts", [])
saved = [d for d in all_deals if d["id"] in bks]

st.title("📚 My Saved Discounts")

if not saved:
    st.info("No bookmarks yet. Go browse and ⭐ save your favorites!")
else:
    st.markdown(f"### ⭐ {len(saved)} Bookmarked Deals")
    for d in saved:
        key = f"rm_{d['id']}"
        with st.expander(f"{d['store']} — {d['percent']}% off {d['item']}"):
            st.write(f"**Category:** {d['category']}")
            st.write(f"**Expires:** {d['end']}")
            if st.button("🗑️ Remove Bookmark", key=key):
                st.session_state.bookmarks.remove(d["id"])
                st.success("Removed. Refresh to update.")

st.markdown("---")
st.caption("CampusPerks • Your personal savings hub.")
