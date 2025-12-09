import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout="wide")
SideBarLinks()
user_id = st.session_state.get('user_id', 1)

API_BASE = "http://api:4000/admin"

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    max-width: 95%;
}

.page-title {
    color: #328E6E;
    font-size: 42px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 10px;
}

.section-title {
    color: #328E6E;
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 10px;
}

div.stButton > button {
    background-color: #328E6E;
    color: #E1EEBC;
    height: 3.5em;
    width: 100%;
    font-size: 20px;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}

div.stButton > button:hover {
    background-color: #2a7359;
}
</style>
""", unsafe_allow_html=True)

st.title("👥 User Management")

tab1, tab2 = st.tabs(["✅ Update User Role", "❌ Deactivate User"])

# TAB 1: Update User Role
with tab1:
    st.markdown('<div class="section-title">Update User Roles</div>', unsafe_allow_html=True)

    try:
        response = requests.get(f"{API_BASE}/users")
        if response.status_code == 200:
            users_data = response.json().get('data', [])

            if users_data:
                with st.container(height=600, border=True):
                    for user in users_data:
                        with st.expander(f"👤 {user.get('Name', 'User')} (ID: {user.get('UserID', 'N/A')})", expanded=False):
                            cols = st.columns(2)

                            with cols[0]:
                                st.write(f"**User ID:** {user.get('UserID', 'N/A')}")
                                st.write(f"**Email:** {user.get('Email', 'N/A')}")
                                st.write(f"**Phone:** {user.get('Phone', 'N/A')}")
                                st.write(f"**Gender:** {user.get('Gender', 'N/A')}")

                            with cols[1]:
                                st.write(f"**Address:** {user.get('Address', 'N/A')}")
                                st.write(f"**DOB:** {user.get('DOB', 'N/A')}")
                                st.write(f"**Current Role:** {user.get('Role', 'N/A')}")

                                if user.get('IsActive'):
                                    st.success("✅ Active")
                                else:
                                    st.warning("⚠️ Inactive")

                            # Role selection and update button
                            user_id = user.get('UserID')
                            new_role = st.selectbox(
                                "Select New Role",
                                ["Admin", "Data Analyst", "Swapper", "Taker"],
                                key=f"role_select_{user_id}"
                            )

                            if st.button("Update Role", key=f"update_role_{user_id}", type="primary"):
                                try:
                                    update_response = requests.put(
                                        f"{API_BASE}/users/{user_id}/role",
                                        json={"role": new_role}
                                    )
                                    if update_response.status_code == 200:
                                        st.success(f"✅ Role updated to {new_role}!")
                                        st.rerun()
                                    else:
                                        st.error(f"Error: {update_response.text}")
                                except Exception as e:
                                    st.error(f"Error updating role: {e}")
            else:
                st.info("No users found in the system.")
        else:
            st.error(f"Error fetching users: {response.status_code}")
    except Exception as e:
        st.error(f"Error connecting to server: {e}")


# TAB 2: Deactivate User
with tab2:
    st.markdown('<div class="section-title">Deactivate Users</div>', unsafe_allow_html=True)

    try:
        response = requests.get(f"{API_BASE}/users")
        if response.status_code == 200:
            users_data = response.json().get('data', [])

            if users_data:
                with st.container(height=600, border=True):
                    for user in users_data:
                        is_active = user.get('IsActive', 0)

                        with st.expander(f"👤 {user.get('Name', 'User')} (ID: {user.get('UserID', 'N/A')})", expanded=False):
                            cols = st.columns(2)

                            with cols[0]:
                                st.write(f"**User ID:** {user.get('UserID', 'N/A')}")
                                st.write(f"**Email:** {user.get('Email', 'N/A')}")
                                st.write(f"**Phone:** {user.get('Phone', 'N/A')}")
                                st.write(f"**Gender:** {user.get('Gender', 'N/A')}")

                            with cols[1]:
                                st.write(f"**Address:** {user.get('Address', 'N/A')}")
                                st.write(f"**DOB:** {user.get('DOB', 'N/A')}")
                                st.write(f"**Role:** {user.get('Role', 'N/A')}")

                                if is_active:
                                    st.success("✅ Active")
                                else:
                                    st.warning("⚠️ Inactive")

                            # Deactivate or Activate button
                            user_id = user.get('UserID')

                            if is_active:
                                if st.button("Deactivate User", key=f"deactivate_{user_id}", type="primary"):
                                    try:
                                        deactivate_response = requests.put(
                                            f"{API_BASE}/users/{user_id}/status",
                                            json={"active": False}
                                        )
                                        if deactivate_response.status_code == 200:
                                            st.success("✅ User deactivated successfully!")
                                            st.rerun()
                                        else:
                                            st.error(f"Error: {deactivate_response.text}")
                                    except Exception as e:
                                        st.error(f"Error deactivating user: {e}")
                            else:
                                if st.button("Activate User", key=f"activate_{user_id}", type="secondary"):
                                    try:
                                        activate_response = requests.put(
                                            f"{API_BASE}/users/{user_id}/status",
                                            json={"active": True}
                                        )
                                        if activate_response.status_code == 200:
                                            st.success("✅ User activated successfully!")
                                            st.rerun()
                                        else:
                                            st.error(f"Error: {activate_response.text}")
                                    except Exception as e:
                                        st.error(f"Error activating user: {e}")
            else:
                st.info("No users found in the system.")
        else:
            st.error(f"Error fetching users: {response.status_code}")
    except Exception as e:
        st.error(f"Error connecting to server: {e}")