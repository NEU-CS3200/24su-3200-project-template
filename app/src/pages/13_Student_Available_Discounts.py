import streamlit as st
from datetime import datetime, timedelta
from modules.nav import SideBarLinks

st.set_page_config(page_title="Expiring Soon", layout="wide")
SideBarLinks(show_home=True)

deals = st.session_state.get("student_discounts", [])
threshold = datetime.today() + timedelta(days=7)

def as_dt(s):
    try:
        return datetime.fromisoformat(s)
    except:
        return datetime.max

expiring = [d for d in deals if as_dt(d["end"]) <= threshold]
expiring.sort(key=lambda d: as_dt(d["end"]))

if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

st.title("⏳ Deals Expiring Soon")

if not expiring:
    st.info("No upcoming expirations in the next 7 days.")
else:
    st.markdown(f"### 🔔 {len(expiring)} Deals Ending Soon")
    for d in expiring:
        key = f"ex_{d['id']}"
        with st.expander(f"{d['store']} — {d['percent']}% off {d['item']} (ends {d['end']})"):
            if d["id"] in st.session_state.bookmarks:
                st.success("✅ Already Bookmarked")
            else:
                if st.button("⭐ Bookmark", key=key):
                    st.session_state.bookmarks.append(d["id"])
                    st.success("Saved!")

st.markdown("---")
st.caption("CampusPerks • Stay ahead and save before it's too late.")
