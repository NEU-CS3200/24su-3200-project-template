import streamlit as st
from datetime import date
from modules.nav import SideBarLinks

# Page config
st.set_page_config(page_title="Admin: Discount Manager", layout="wide")
SideBarLinks(show_home=True)

# --- Simulated Discount Data
if "admin_discounts" not in st.session_state:
    st.session_state.admin_discounts = [
        {
            "id": 101,
            "store": "Campus Cafe",
            "code": "COFFEE20",
            "percent": 20,
            "category": "Food",
            "start": "2025-04-01",
            "end": "2025-04-20"
        },
        {
            "id": 102,
            "store": "BookBarn",
            "code": "BOOKS15",
            "percent": 15,
            "category": "Books",
            "start": "2025-04-05",
            "end": "2025-04-25"
        }
    ]

st.title("🛠️ Admin: Manage Discounts")
st.caption("Create, update, and clean up discount entries.")

# --- Add New Discount Form
st.markdown("### ➕ Add New Discount")
with st.form("add_discount_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        store = st.text_input("Store Name")
        code = st.text_input("Discount Code")
    with col2:
        percent = st.slider("Discount Percent", 5, 90, 20)
        category = st.selectbox("Category", ["Food", "Books", "Fitness", "Electronics", "Clothing"])
    with col3:
        start_date = st.date_input("Start Date", date.today())
        end_date = st.date_input("End Date", date.today())

    submitted = st.form_submit_button("Add Discount")
    if submitted and store and code:
        new_id = max(d["id"] for d in st.session_state.admin_discounts) + 1
        st.session_state.admin_discounts.append({
            "id": new_id,
            "store": store,
            "code": code,
            "percent": percent,
            "category": category,
            "start": str(start_date),
            "end": str(end_date)
        })
        st.success(f"Discount {code} added for {store}!")

# --- Manage Existing Discounts
st.markdown("### ✏️ Current Discounts")
for d in st.session_state.admin_discounts:
    with st.expander(f"{d['store']} – {d['code']} ({d['percent']}% off, ends {d['end']})"):
        col1, col2 = st.columns(2)
        with col1:
            new_end = st.date_input(f"New End Date (ID {d['id']})", value=date.fromisoformat(d['end']), key=f"end_{d['id']}")
            new_category = st.selectbox("Reassign Category", ["Food", "Books", "Fitness", "Electronics", "Clothing"],
                                        index=["Food", "Books", "Fitness", "Electronics", "Clothing"].index(d["category"]),
                                        key=f"cat_{d['id']}")
        with col2:
            if st.button("💾 Save Changes", key=f"save_{d['id']}"):
                d["end"] = str(new_end)
                d["category"] = new_category
                st.success("Discount updated!")

        if st.button("🗑️ Remove Discount", key=f"delete_{d['id']}"):
            st.session_state.admin_discounts.remove(d)
            st.warning("Discount deleted!")
            st.experimental_rerun()

# Footer
st.markdown("---")
st.caption("CampusPerks • Full control for platform discounts.")