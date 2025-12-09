import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from datetime import datetime

st.set_page_config(layout="wide")
SideBarLinks()

API_BASE = "http://api:4000/admin"


st.title("🚨 Report Management")
st.subheader("All Reports")
user_id = st.session_state.get('user_id', 1)

# Initialize session state
if 'reports' not in st.session_state:
    st.session_state.reports = None

status = st.selectbox("Status", ["all", "pending", "resolved"])

# Function to fetch reports
def fetch_reports(status_filter):
    try:
        response = requests.get(f"{API_BASE}/reports?status={status_filter}")
        if response.status_code == 200:
            return response.json().get('data', [])
    except Exception as e:
        st.error(f"Failed to fetch reports: {str(e)}")
    return None

if st.button("Get Reports", type="primary"):
    st.session_state.reports = fetch_reports(status)

# Display reports if they exist
if st.session_state.reports is not None:
    reports = st.session_state.reports

    if reports:
        st.write(f"Found **{len(reports)} {status} reports**")

        with st.container():
            for idx, report in enumerate(reports):
                with st.expander(f"Report #{report.get('ReportID', 'N/A')} — Severity {report.get('Severity', 'N/A')}"):
                    st.write(f"**Reported Item:** {report.get('ReportedItem', 'N/A')}")
                    st.write(f"**Reported User:** {report.get('ReportedUser', 'N/A')}")
                    st.write(f"**Note:** {report.get('Note', 'N/A')}")
                    st.write(f"**Resolved:** {'Yes' if report.get('Resolved') else 'No'}")
                    if report.get('ResolvedAt'):
                        st.write(f"**Resolved At:** {report['ResolvedAt']}")

                    st.markdown("---")
                    is_resolved = report.get('Resolved')
                    report_id = report.get('ReportID')

                    if is_resolved:
                        # Show disabled button for resolved reports
                        st.button(f"✓ Resolved", key=f"resolved_{report_id}", disabled=True)
                    else:
                        # Show active button for unresolved reports
                        if st.button(f"Mark as Resolved", key=f"resolve_{report_id}", type="primary"):
                            try:
                                resp = requests.put(
                                    f"{API_BASE}/reports/{report_id}/resolve"
                                )
                                if resp.status_code == 200:
                                    # Refetch reports with current filter instead of updating in place
                                    st.session_state.reports = fetch_reports(status)
                                    st.success("Report marked as resolved!")
                                    st.rerun()
                                else:
                                    st.error("Failed to update report")
                            except Exception as e:
                                st.error(f"Error: {str(e)}")
    else:
        st.info(f"No {status} reports found")