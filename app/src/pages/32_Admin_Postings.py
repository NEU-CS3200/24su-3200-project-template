import os, requests, pandas as pd, streamlit as st
from modules.nav import SideBarLinks

# ---- Config ----
BASE_API = os.getenv("BASE_API", "http://web-api:4000")
COOP_API = f"{BASE_API}/coopPositions"
TIMEOUT = 10

st.set_page_config(page_title="Review Job Postings • Coopalytics", layout="wide", initial_sidebar_state="expanded")
SideBarLinks()
st.title("📝 Review Job Postings")

# ---- Helpers ----
def get_json(url):
    r = requests.get(url, timeout=TIMEOUT); r.raise_for_status(); return r.json()

def put_json(url, payload=None):
    r = requests.put(url, json=payload or {}, timeout=TIMEOUT); r.raise_for_status(); return r.json()

def delete_json(url):
    r = requests.delete(url, timeout=TIMEOUT); r.raise_for_status(); return r.json()

def flag_json(pos_id, value: int):
    r = requests.put(f"{COOP_API}/{pos_id}/flag/{value}", timeout=TIMEOUT); r.raise_for_status(); return r.json()

def unflag_json(pos_id):
    r = requests.put(f"{COOP_API}/{pos_id}/unflag", timeout=TIMEOUT); r.raise_for_status(); return r.json()

# ---- Load pending ----
try:
    pending = pd.DataFrame(get_json(f"{COOP_API}/pending"))
except Exception as e:
    st.error(f"Could not load pending positions: {e}")
    pending = pd.DataFrame()

# ---- Top bar (metrics + filters) ----
c1, c2, c3, c4 = st.columns([1,1,2,2])

# Calculate metrics from the data
if not pending.empty:
    total_positions = len(pending)
    flagged_count = len(pending[pending['flag'] == 1]) if 'flag' in pending.columns else 0
    approved_count = len(pending[pending['flag'] == 0]) if 'flag' in pending.columns else total_positions
else:
    total_positions = flagged_count = approved_count = 0

c1.metric("Total Positions", total_positions)
c2.metric("🚩 Flagged", flagged_count, delta=f"-{approved_count} approved")

try:
    avg_pay = pd.DataFrame(get_json(f"{COOP_API}/industryAveragePay"))
    c3.metric("Industries", 0 if avg_pay.empty else len(avg_pay))
except Exception:
    c3.metric("Industries", "—")

# Filters
status_filter = c4.selectbox("Status Filter", ["All", "Approved", "Flagged"], index=0)
q = st.text_input("🔍 Search title/company/location", "")
industry_filter = st.selectbox(
    "Industry filter",
    ["All"] + (sorted(pending["industry"].dropna().unique().tolist()) if not pending.empty else ["All"]),
    index=0
)

# Apply filters
view = pending.copy()
if not view.empty:
    view["companyName"] = view.get("companyName", "")

    # Add flag status column for display
    if 'flag' in view.columns:
        view["Status"] = view["flag"].apply(lambda x: "🚩 Flagged" if x == 1 else "✅ Approved")
    else:
        view["Status"] = "✅ Approved"

    # Apply search filter
    if q:
        ql = q.lower()
        view = view[
            view["title"].str.lower().str.contains(ql, na=False) |
            view["companyName"].astype(str).str.lower().str.contains(ql, na=False) |
            view["location"].str.lower().str.contains(ql, na=False)
        ]

    # Apply status filter
    if status_filter == "Approved":
        view = view[view["flag"] == 0] if 'flag' in view.columns else view
    elif status_filter == "Flagged":
        view = view[view["flag"] == 1] if 'flag' in view.columns else view.iloc[0:0]  # Empty dataframe

    # Apply industry filter
    if industry_filter != "All":
        view = view[view["industry"] == industry_filter]

st.divider()

# ---- Table + actions ----
left, right = st.columns([2.2, 1])

with left:
    st.subheader("📌 Co-op Positions Management")
    if view.empty:
        st.info("No positions match your filters.")
    else:
        # Prepare display columns with status
        display_columns = ["coopPositionId", "Status", "title", "companyName", "location", "hourlyPay", "deadline", "industry"]
        available_columns = [col for col in display_columns if col in view.columns]

        show = view[available_columns].sort_values(["deadline","coopPositionId"], ascending=[True, False])

        # Style the dataframe with colors
        def style_status(val):
            if "Flagged" in str(val):
                return 'background-color: #ffebee; color: #c62828'  # Light red background, dark red text
            elif "Approved" in str(val):
                return 'background-color: #e8f5e8; color: #2e7d32'  # Light green background, dark green text
            return ''

        if "Status" in show.columns:
            styled_df = show.style.applymap(style_status, subset=['Status'])
            st.dataframe(styled_df, use_container_width=True, height=420)
        else:
            st.dataframe(show, use_container_width=True, height=420)

with right:
    st.subheader("⚡ Quick Actions")
    pos_id = st.number_input("Position ID", min_value=0, step=1, value=0)
    a1, a2 = st.columns(2)
    a3, a4 = st.columns(2)

    if a1.button("✅ Approve", type="primary", use_container_width=True, disabled=pos_id<=0):
        with st.spinner(f"Approving position {int(pos_id)}..."):
            try:
                result = put_json(f"{COOP_API}/{int(pos_id)}/approve")
                if result.get("ok"):
                    st.success(f"✅ {result.get('message', f'Position {int(pos_id)} approved successfully')}")
                    st.info("Position is now visible to students and available for applications.")
                else:
                    st.warning(f"⚠️ {result.get('message', f'Position {int(pos_id)} was already approved')}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Approve failed: {e}")

    if a2.button("🗑️ Delete", use_container_width=True, disabled=pos_id<=0):
        with st.spinner(f"Deleting position {int(pos_id)}..."):
            try:
                result = delete_json(f"{COOP_API}/{int(pos_id)}")
                if result.get("ok"):
                    st.success(f"🗑️ {result.get('message', f'Position {int(pos_id)} deleted successfully')}")
                    st.info("Position has been permanently removed from the system.")
                else:
                    st.error(f"❌ {result.get('error', 'Delete failed')}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Delete failed: {e}")

    if a3.button("🚩 Flag", use_container_width=True, disabled=pos_id<=0):
        with st.spinner(f"Flagging position {int(pos_id)}..."):
            try:
                result = flag_json(int(pos_id), 1)
                if result.get("ok"):
                    st.success(f"🚩 {result.get('message', f'Position {int(pos_id)} flagged successfully')}")
                    st.info("Position is now hidden from students and marked for review.")
                else:
                    st.error(f"❌ {result.get('error', 'Flag failed')}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Flag failed: {e}")

    if a4.button("✅ Unflag", use_container_width=True, disabled=pos_id<=0):
        with st.spinner(f"Unflagging position {int(pos_id)}..."):
            try:
                result = unflag_json(int(pos_id))
                if result.get("ok"):
                    st.success(f"✅ {result.get('message', f'Position {int(pos_id)} unflagged successfully')}")
                    st.info("Position is now approved and visible to students.")
                else:
                    st.error(f"❌ {result.get('error', 'Unflag failed')}")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Unflag failed: {e}")

st.divider()

# ---- Industry averages (optional context) ----
st.subheader("💸 Industry Average Hourly Pay")
try:
    if 'avg_pay' not in locals():
        avg_pay = pd.DataFrame(get_json(f"{COOP_API}/industryAveragePay"))
    if avg_pay.empty:
        st.caption("No data.")
    else:
        st.dataframe(avg_pay.rename(columns={"industry":"Industry","industryAvgHourlyPay":"Avg $/hr"}), use_container_width=True)
except Exception as e:
    st.caption(f"Could not load averages: {e}")
