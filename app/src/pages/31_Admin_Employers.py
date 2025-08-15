import os, requests, pandas as pd, streamlit as st
from modules.nav import SideBarLinks

# ---- Config ----
BASE_API = os.getenv("BASE_API", "http://web-api:4000")
COOP_API = f"{BASE_API}/coopPositions"
TIMEOUT = 10

st.set_page_config(page_title="Employer Accounts • Coopalytics", layout="wide")
SideBarLinks()
st.title("🏢 Employer Accounts")

# ---- Helpers ----
def get_json(url):
  r = requests.get(url, timeout=TIMEOUT); r.raise_for_status(); return r.json()


# ---- Load data ----
try:
    counts_df = pd.DataFrame(get_json(f"{COOP_API}/employerJobCounts"))
except Exception as e:
    counts_df = pd.DataFrame()
    st.error(f"Could not load employer job counts: {e}")

# ---- Top stats ----
col1, col2, col3 = st.columns(3)
total_employers  = counts_df["employerId"].nunique() if not counts_df.empty else 0
active_employers = counts_df[counts_df["numJobs"] > 0]["employerId"].nunique() if not counts_df.empty else 0
zero_job_employers = total_employers - active_employers

col1.metric("Total Employers", total_employers)
col2.metric("Active (≥1 job)", active_employers)
col3.metric("No Jobs Yet", zero_job_employers)

st.divider()

# ---- Filters / search ----
with st.container():
   fcol1, fcol2 = st.columns([3,1])
   query = fcol1.text_input("Search employers (name/company)", value="")
   sort_by = fcol2.selectbox("Sort by", ["numJobs ↓","numJobs ↑","lastName A→Z","company A→Z"], index=0)

view = counts_df.copy()
if not view.empty:
    # compose display name and filter
    view["employerName"] = (view["firstName"].fillna("") + " " + view["lastName"].fillna("")).str.strip()
    if query:
        q = query.lower()
        view = view[
            view["employerName"].str.lower().str.contains(q, na=False) |
            view["companyName"].str.lower().str.contains(q, na=False)
        ]
    #view = view[view["numJobs"] >= min_jobs]

    # sorting
    if sort_by == "numJobs ↓":
        view = view.sort_values(["numJobs","lastName","firstName"], ascending=[False,True,True])
    elif sort_by == "numJobs ↑":
        view = view.sort_values(["numJobs","lastName","firstName"], ascending=[True,True,True])
    elif sort_by == "lastName A→Z":
        view = view.sort_values(["lastName","firstName"])
    else:  # company A→Z
        view = view.sort_values(["companyName","lastName","firstName"])

st.subheader("Accounts")
if view.empty:
    st.info("No employers match your filters.")
else:
    show = view[["employerId","employerName","companyName","numJobs"]].rename(
        columns={
            "employerId":"Employer ID",
            "employerName":"Employer",
            "companyName":"Company",
            "numJobs":"# Jobs"
        }
    )
    st.dataframe(show, use_container_width=True)

st.caption("Data source: /api/coopPositions/employerJobCounts")