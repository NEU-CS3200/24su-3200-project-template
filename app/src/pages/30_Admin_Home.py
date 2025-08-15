import os, requests, pandas as pd, streamlit as st
from modules.nav import SideBarLinks

# ----- Config -----
BASE_API = os.getenv("BASE_API", "http://web-api:4000")
COOP_API = f"{BASE_API}/coopPositions"
DEI_API  = f"{BASE_API}/api/dei"     # ok if not registered; handled below
TIMEOUT  = 10

st.set_page_config(page_title="Admin • Coopalytics", layout="wide", initial_sidebar_state="expanded")
SideBarLinks()
st.title("⚙️ System Admin Home Page")

# ----- Helpers -----
def get_json(url):
    r = requests.get(url, timeout=TIMEOUT); r.raise_for_status(); return r.json()

# ----- Load data (safe fallbacks) -----
pending_df = pd.DataFrame()
employers_df = pd.DataFrame()
dei_gender  = pd.DataFrame()

try:
    pending_df = pd.DataFrame(get_json(f"{COOP_API}/pending"))
except Exception:
    pending_df = pd.DataFrame()

try:
    employers_df = pd.DataFrame(get_json(f"{COOP_API}/employerJobCounts"))
except Exception:
    employers_df = pd.DataFrame()

try:
    dei_gender = pd.DataFrame(get_json(f"{DEI_API}/representation/gender"))
except Exception:
    dei_gender = pd.DataFrame()

# ----- KPIs -----
c1, c2, c3, c4 = st.columns(4)
c1.metric("Pending Postings", 0 if pending_df.empty else len(pending_df))
active_employers = 0 if employers_df.empty else employers_df[employers_df["numJobs"] > 0]["employerId"].nunique()
c2.metric("Active Employers", active_employers)
total_jobs = 0 if employers_df.empty else int(employers_df["numJobs"].sum())
c3.metric("Total Jobs Posted", total_jobs)

st.divider()

# ----- Quick links -----
st.subheader("🚀 Quick Links")
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/32_Admin_Postings.py",   label="Review Job Postings", icon="✅")
with col2:
    st.page_link("pages/31_Admin_Employers.py",  label="Manage Employers",    icon="🏢")
with col3:
    st.page_link("pages/33_Admin_DEI.py",        label="DEI Metrics",         icon="🌍")

st.divider()

# ----- Tables (preview) -----
left, right = st.columns(2, gap="large")

with left:
    st.subheader("📌 Pending (Top 10)")
    if pending_df.empty:
        st.info("No pending positions.")
    else:
        show = pending_df[["coopPositionId","title","companyName","location","deadline","hourlyPay","industry"]].copy()
        st.dataframe(show.head(10), use_container_width=True)

with right:
    st.subheader("🏢 Employers by Job Count")
    if employers_df.empty:
        st.info("No employer data.")
    else:
        show_e = employers_df[["employerId","firstName","lastName","companyName","numJobs"]].sort_values("numJobs", ascending=False)
        st.dataframe(show_e.head(10), use_container_width=True)