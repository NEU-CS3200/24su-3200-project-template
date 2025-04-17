import streamlit as st
from modules.nav import SideBarLinks

# Page config first!
st.set_page_config(page_title="Admin: User Interactions", layout="wide")
SideBarLinks(show_home=True)

# 🔥 Simulated log data (replace later with API)
interaction_data = [
    {"user": "emmafoley", "action": "Used discount CODE123", "time": "2025-04-10 14:23"},
    {"user": "johnsmith", "action": "Joined club ArtSociety", "time": "2025-04-10 15:02"},
    {"user": "janedoe", "action": "Viewed store Starbucks", "time": "2025-04-10 15:45"},
    {"user": "markspencer", "action": "Checked out item Laptop", "time": "2025-04-10 16:00"},
    {"user": "janedoe", "action": "Used discount BOOKS15", "time": "2025-04-11 10:01"},
    {"user": "emmafoley", "action": "Bookmarked Espresso deal", "time": "2025-04-11 10:03"},
]

# Simulated user profile data
user_profiles = {
    "emmafoley": {
        "first_name": "Emma",
        "last_name": "Foley",
        "email": "emma@um.edu",
        "college": "UMiami",
        "club": "Book Club"
    },
    "johnsmith": {
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@fordham.edu",
        "college": "Fordham",
        "club": "Chess Club"
    },
    "janedoe": {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@nu.edu",
        "college": "Northeastern",
        "club": "Art Society"
    },
}

# Title
st.title("🧾 Admin Dashboard")

# Tabs
tab1, tab2 = st.tabs(["📜 User Interactions", "👤 Search Users"])

# --- Tab 1: User Interaction Log ---
with tab1:
    st.caption("View recent platform activity from all users.")
    search_query = st.text_input("🔍 Filter interactions by username or action", "")

    if search_query:
        filtered = [
            log for log in interaction_data
            if search_query.lower() in log["user"].lower() or search_query.lower() in log["action"].lower()
        ]
    else:
        filtered = interaction_data

    if filtered:
        for entry in filtered:
            st.markdown(f"""
                <p style='font-size:14px;'>
                <strong>👤 User:</strong> {entry['user']}<br>
                <strong>📝 Action:</strong> {entry['action']}<br>
                <strong>⏰ Time:</strong> {entry['time']}
                </p>
                <hr style="border: 0.5px solid #666;">
            """, unsafe_allow_html=True)
    else:
        st.info("No interactions match your search.")

# --- Tab 2: Search Users ---
with tab2:
    st.caption("Search, edit, or delete user profiles.")
    selected_user = st.text_input("🔍 Enter username to search", "").strip()

    if selected_user:
        user_key = selected_user.lower()
        user = user_profiles.get(user_key)

        if user:
            st.success(f"User '{selected_user}' found!")

            # Editable fields
            first = st.text_input("First Name", value=user["first_name"])
            last = st.text_input("Last Name", value=user["last_name"])
            email = st.text_input("Email", value=user["email"])
            college = st.text_input("College", value=user["college"])
            club = st.text_input("Club", value=user["club"])

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Changes"):
                    user_profiles[user_key] = {
                        "first_name": first,
                        "last_name": last,
                        "email": email,
                        "college": college,
                        "club": club,
                    }
                    st.success("✅ User profile updated.")
            with col2:
                if st.button("🗑️ Delete User", type="primary"):
                    del user_profiles[user_key]
                    st.warning(f"🚨 User '{selected_user}' deleted.")
        else:
            st.warning("🚫 No user found with that username.")

# Footer
st.markdown("---")
st.caption("CampusPerks • Admin tools for better visibility and platform management.")
