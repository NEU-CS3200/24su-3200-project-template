import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

API = "http://web-api:4000/payoutProfiles"

st.title("\U0001f4b8 Royalty Splits Manager")
st.write("Add collaborators, update split percentages, and remove payout profiles for your releases.")

st.divider()

# ── Fetch & display all payout profiles ──────────────────────────────────────

st.subheader("Current Payout Profiles")

release_filter = st.number_input("Filter by Release ID (0 = show all)", min_value=0, step=1, value=0)

try:
    if release_filter > 0:
        response = requests.get(f"{API}/release/{release_filter}")
    else:
        response = requests.get(f"{API}/")

    if response.status_code == 200:
        profiles = response.json()

        if not profiles:
            st.info("No payout profiles found.")
        else:
            st.write(f"**{len(profiles)} profile(s) found**")

            for p in profiles:
                release_title = p.get('release_title') or f"Release {p['pp_release_id']}"
                release_label = f"{release_title} (ID {p['pp_release_id']})"
                artist_label  = p.get('artist_name', 'Unknown Artist')
                expander_label = f"ID {p['payout_id']} — {p['collab_email']} | {p['role']} | {p['split_percentage']}% | {artist_label} — {release_title}"
                with st.expander(expander_label):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Collaborator Email:** {p['collab_email']}")
                        st.write(f"**Role:** {p['role']}")
                    with col2:
                        st.write(f"**Split %:** {p['split_percentage']}%")
                        st.write(f"**Artist:** {artist_label}")
                        st.write(f"**Release:** {release_label}")

                    # ── Inline edit ──
                    st.write("**Edit this profile:**")
                    edit_col1, edit_col2, edit_col3 = st.columns(3)
                    with edit_col1:
                        new_email = st.text_input("Email", value=p['collab_email'], key=f"email_{p['payout_id']}")
                    with edit_col2:
                        new_role = st.text_input("Role", value=p['role'], key=f"role_{p['payout_id']}")
                    with edit_col3:
                        new_split = st.number_input(
                            "Split %", min_value=0.0, max_value=100.0, step=0.01,
                            value=float(p['split_percentage']), key=f"split_{p['payout_id']}"
                        )

                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("Save Changes", key=f"save_{p['payout_id']}"):
                            payload = {"collab_email": new_email, "role": new_role, "split_percentage": new_split}
                            r = requests.put(f"{API}/{p['payout_id']}", json=payload)
                            if r.status_code == 200:
                                st.success("Profile updated.")
                                st.rerun()
                            else:
                                st.error(f"Update failed: {r.json().get('error', r.text)}")
                    with btn_col2:
                        if st.button("Delete", key=f"del_{p['payout_id']}", type="secondary"):
                            r = requests.delete(f"{API}/{p['payout_id']}")
                            if r.status_code == 200:
                                st.success("Profile deleted.")
                                st.rerun()
                            else:
                                st.error(f"Delete failed: {r.json().get('error', r.text)}")
    else:
        st.error(f"Failed to load profiles: {response.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to API: {e}")
    st.info("Make sure the API server is running on http://web-api:4000")

st.divider()

# ── Add new payout profile ────────────────────────────────────────────────────

st.subheader("\U0001f4b8 Add New Collaborator")

with st.form("add_payout_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_email = st.text_input("Collaborator Email", placeholder="collaborator@email.com")
        new_role = st.text_input("Role", placeholder="e.g. Producer, Songwriter, Featured Artist")
    with col2:
        new_split = st.number_input("Split Percentage", min_value=0.0, max_value=100.0, step=0.01, value=0.0)
        new_release_id = st.number_input("Release ID", min_value=1, step=1, value=1)

    submitted = st.form_submit_button("Add Collaborator", type="primary", use_container_width=True)

    if submitted:
        if not new_email or not new_role:
            st.error("Email and Role are required.")
        else:
            payload = {
                "collab_email": new_email,
                "role": new_role,
                "split_percentage": new_split,
                "pp_release_id": new_release_id,
            }
            try:
                r = requests.post(f"{API}/", json=payload)
                if r.status_code == 201:
                    st.success(f"Collaborator added! Payout ID: {r.json().get('payout_id')}")
                    st.rerun()
                else:
                    st.error(f"Failed to add collaborator: {r.json().get('error', r.text)}")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to API: {e}")
