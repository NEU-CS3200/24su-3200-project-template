import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(page_title="Deactivate Discounts", layout="wide")
SideBarLinks(show_home=True)

st.title("🛑 Manage Active Discounts")
st.write("Deactivate old or irrelevant discounts to keep your listings up to date.")

# Simulated discounts with 'active' status
if "discounts_with_status" not in st.session_state:
    st.session_state.discounts_with_status = [
        {"id": 201, "item": "Iced Coffee", "percent": 15, "active": True},
        {"id": 202, "item": "Pastry Pack", "percent": 10, "active": True},
        {"id": 203, "item": "Cold Brew", "percent": 20, "active": False},
    ]

# Toggle active status
for discount in st.session_state.discounts_with_status:
    with st.expander(f"{discount['item']} — {discount['percent']}% off"):
        current = "✅ Active" if discount["active"] else "❌ Inactive"
        st.markdown(f"**Current Status:** {current}")
        toggle = st.checkbox("Mark as Active", value=discount["active"], key=f"toggle_{discount['id']}")
        discount["active"] = toggle

st.success("Changes are stored in session — integrate with backend to persist.")

st.markdown("---")
st.caption("Only active discounts are shown to students in the app.")
