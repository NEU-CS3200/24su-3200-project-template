import streamlit as st
from modules.nav import SideBarLinks

# Simulated in-memory discounts
if "discounts" not in st.session_state:
    st.session_state.discounts = [
        {"id": 101, "item": "Latte", "percent": 20},
        {"id": 102, "item": "Muffin", "percent": 10}
    ]

st.set_page_config(page_title="Manage Discounts", layout="wide")
SideBarLinks()

st.title("📋 Manage Your Discounts")

# Section: Add New Discount
st.markdown("### ➕ Add a New Discount")
with st.form("add_discount"):
    new_item = st.text_input("Item Name")
    new_percent = st.number_input("Discount %", min_value=1, max_value=100)
    submitted = st.form_submit_button("Add Discount")
    if submitted and new_item:
        new_id = max(d["id"] for d in st.session_state.discounts) + 1
        st.session_state.discounts.append({"id": new_id, "item": new_item, "percent": new_percent})
        st.success(f"Added: {new_item} at {new_percent}% off!")

# Section: Edit Existing Discounts
st.markdown("### ✏️ Update Existing Discounts")
for discount in st.session_state.discounts:
    with st.expander(f"{discount['item']} — {discount['percent']}% off"):
        new_percent = st.slider(f"Update Discount % for {discount['item']}", 1, 100, discount["percent"], key=discount["id"])
        if new_percent != discount["percent"]:
            discount["percent"] = new_percent
            st.success(f"Updated {discount['item']} to {new_percent}% off!")

# Footer
st.markdown("---")
st.caption("CampusPerks • Help your discounts work harder for your business.")