import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

BASE = "http://web-api:4000"

st.title("Help Requests Panel")

col1, col2 = st.columns(2)
with col1:
    view = st.selectbox("Filter", ["All Requests", "Unresolved Only"])
with col2:
    sort_by = st.selectbox("Sort By", ["Priority (Unresolved First)", "Newest First"])

st.divider()

try:
    url = f"{BASE}/help_requests/status" if view == "Unresolved Only" else f"{BASE}/help_requests"
    resp = requests.get(url)

    if resp.status_code == 200:
        reqs = resp.json()

        if sort_by == "Priority (Unresolved First)":
            reqs = sorted(reqs, key=lambda x: x.get("status", 1))

        st.write(f"**{len(reqs)} request(s) found**")

        if reqs:
            df = pd.DataFrame(reqs)
            df["status"] = df["status"].map({1: "✅ Resolved", 0: "🔴 Unresolved"})
            st.dataframe(
                df[["request_id", "submitted_user_id", "description", "status", "assigned_admin_id", "created_at"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No requests found.")

        # Single request lookup
        st.divider()
        st.subheader("Look Up Request by ID")
        single_req_id = st.number_input("Request ID", min_value=1, step=1, key="single_req_lookup")
        if st.button("Fetch Request", type="primary"):
            try:
                sr = requests.get(f"{BASE}/help_requests/{single_req_id}")
                if sr.status_code == 200:
                    req = sr.json()
                    req["status"] = "✅ Resolved" if req["status"] == 1 else "🔴 Unresolved"
                    st.dataframe(pd.DataFrame([req])[["request_id", "submitted_user_id", "description", "status", "assigned_admin_id", "created_at"]], use_container_width=True, hide_index=True)
                elif sr.status_code == 404:
                    st.warning(f"No request found with ID {single_req_id}.")
                else:
                    st.error("Failed to fetch request.")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to API: {e}")

        # Update a request
        st.divider()
        st.subheader("Update Help Request")
        col1, col2, col3 = st.columns(3)
        with col1:
            req_id = st.number_input("Request ID", min_value=1, step=1)
        with col2:
            new_status = st.selectbox(
                "Status", [0, 1], format_func=lambda x: "Unresolved" if x == 0 else "Resolved"
            )
        with col3:
            new_admin = st.number_input("Assigned Admin ID", min_value=1, step=1)

        if st.button("Update Request", type="primary"):
            r = requests.put(
                f"{BASE}/help_requests/{req_id}",
                json={"status": new_status, "assigned_admin_id": new_admin},
            )
            if r.status_code == 200:
                st.success("Request updated.")
                st.rerun()
            else:
                st.error(f"Failed: {r.text}")

        # Create a new help request
        st.divider()
        st.subheader("Create Help Request")
        col1, col2 = st.columns(2)
        with col1:
            new_user_id = st.number_input("User ID", min_value=1, step=1, key="new_req_user")
            new_admin_id = st.number_input("Assign Admin ID", min_value=1, step=1, key="new_req_admin")
        with col2:
            new_desc = st.text_area("Description")

        if st.button("Submit Help Request", type="primary"):
            if not new_desc:
                st.warning("Description is required.")
            else:
                r = requests.post(
                    f"{BASE}/help_requests",
                    json={"submitted_user_id": new_user_id, "description": new_desc, "assigned_admin_id": new_admin_id},
                )
                if r.status_code == 201:
                    st.success(f"Help request created. ID: {r.json().get('request_id')}")
                    st.rerun()
                else:
                    st.error(f"Failed: {r.text}")

        # Analytics
        st.divider()
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Admin Workload")
            ar = requests.get(f"{BASE}/help_requests/by-admin")
            if ar.status_code == 200:
                data = ar.json()
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
                else:
                    st.info("No data.")

        with col2:
            st.subheader("Top Users with Issues")
            ur = requests.get(f"{BASE}/help_requests/by-user")
            if ur.status_code == 200:
                data = ur.json()
                if data:
                    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
                else:
                    st.info("No data.")
    else:
        st.error("Failed to fetch help requests.")

except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to API: {e}")
