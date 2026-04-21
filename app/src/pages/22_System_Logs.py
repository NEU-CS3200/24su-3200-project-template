import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

BASE = "http://web-api:4000"

st.title("System Logs Dashboard")

col1, col2 = st.columns([3, 1])
with col1:
    search = st.text_input("Search Logs", placeholder="Search by description...")
with col2:
    errors_only = st.toggle("Errors Only", value=False)

st.divider()

try:
    url = f"{BASE}/system_logs/errors" if errors_only else f"{BASE}/system_logs"
    resp = requests.get(url)

    if resp.status_code == 200:
        logs = resp.json()

        if search:
            logs = [l for l in logs if search.lower() in (l.get("description") or "").lower()]

        st.write(f"**{len(logs)} log entries found**")

        if logs:
            df = pd.DataFrame(logs)
            df["status"] = df["status"].map({1: "✅ Success", 0: "❌ Error"})
            st.dataframe(
                df[["log_id", "timestamp", "description", "log_user_id", "log_admin_id", "status"]],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No logs match your filter.")

        # Recent Errors
        st.divider()
        st.subheader("Recent Errors")
        err_resp = requests.get(f"{BASE}/system_logs/errors")
        if err_resp.status_code == 200:
            errors = err_resp.json()[:5]
            if errors:
                for err in errors:
                    with st.expander(f"Log #{err['log_id']} — {err.get('timestamp', 'N/A')}"):
                        st.write(f"**Description:** {err.get('description', 'N/A')}")
                        st.write(f"**User ID:** {err.get('log_user_id', 'N/A')}")
                        st.write(f"**Admin ID:** {err.get('log_admin_id', 'N/A')}")
            else:
                st.success("No recent errors.")

        # Single log lookup
        st.divider()
        st.subheader("Look Up Log by ID")
        single_log_id = st.number_input("Log ID", min_value=1, step=1, key="single_log_lookup")
        if st.button("Fetch Log", type="primary"):
            try:
                sr = requests.get(f"{BASE}/system_logs/{single_log_id}")
                if sr.status_code == 200:
                    log = sr.json()
                    log["status"] = "✅ Success" if log["status"] == 1 else "❌ Error"
                    st.dataframe(pd.DataFrame([log])[["log_id", "timestamp", "description", "log_user_id", "log_admin_id", "status"]], use_container_width=True, hide_index=True)
                elif sr.status_code == 404:
                    st.warning(f"No log found with ID {single_log_id}.")
                else:
                    st.error("Failed to fetch log.")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to API: {e}")

        # Logs by user
        st.divider()
        st.subheader("Logs by User")
        user_id_input = st.number_input("User ID", min_value=1, step=1, key="user_id_lookup")
        if st.button("Fetch User Logs", type="primary"):
            try:
                ur = requests.get(f"{BASE}/system_logs/user/{user_id_input}")
                if ur.status_code == 200:
                    user_logs = ur.json()
                    if user_logs:
                        udf = pd.DataFrame(user_logs)
                        udf["status"] = udf["status"].map({1: "✅ Success", 0: "❌ Error"})
                        st.dataframe(udf[["log_id", "timestamp", "description", "log_admin_id", "status"]], use_container_width=True, hide_index=True)
                    else:
                        st.info(f"No logs found for user {user_id_input}.")
                else:
                    st.error("Failed to fetch logs for that user.")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to API: {e}")

        # Update log status
        st.divider()
        st.subheader("Update Log Status")
        col1, col2 = st.columns(2)
        with col1:
            log_id = st.number_input("Log ID", min_value=1, step=1)
        with col2:
            new_status = st.selectbox(
                "New Status", [1, 0], format_func=lambda x: "Success" if x == 1 else "Error"
            )
        new_desc = st.text_area("Updated Description (optional)")

        if st.button("Update Log", type="primary"):
            payload = {"status": new_status}
            if new_desc:
                payload["description"] = new_desc
            r = requests.put(f"{BASE}/system_logs/{log_id}", json=payload)
            if r.status_code == 200:
                st.success("Log updated successfully.")
                st.rerun()
            else:
                st.error(f"Failed to update log: {r.text}")
    else:
        st.error("Failed to fetch system logs.")

except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to API: {e}")
