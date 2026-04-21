import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

API = "http://web-api:4000/assets"

st.title("\U0001f4c2 Asset Tracker")
st.write("Monitor audio files, artwork, and credits across your roster. Filter, upload, update, and remove assets.")

st.divider()

# ── Filters ───────────────────────────────────────────────────────────────────

st.subheader("Browse Assets")

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    file_type_filter = st.selectbox("Filter by File Type", ["All", "Audio", "Artwork", "Credits"])
with filter_col2:
    status_filter = st.selectbox("Filter by Upload Status", ["All", "Pending (0)", "Complete (1)"])
with filter_col3:
    release_filter = st.number_input("Filter by Release ID (0 = all)", min_value=0, step=1, value=0)

# ── Fetch assets ──────────────────────────────────────────────────────────────

try:
    if release_filter > 0:
        response = requests.get(f"{API}/release/{release_filter}")
    else:
        params = {}
        if file_type_filter != "All":
            params["file_type"] = file_type_filter
        if status_filter != "All":
            params["upload_status"] = 0 if status_filter.startswith("Pending") else 1
        response = requests.get(f"{API}/", params=params)

    if response.status_code == 200:
        assets = response.json()

        if not assets:
            st.info("No assets found matching the selected filters.")
        else:
            st.write(f"**{len(assets)} asset(s) found**")

            STATUS_LABEL = {0: "⏳ Pending", 1: "✅ Complete"}

            for a in assets:
                release_title = a.get("release_title") or f"Release {a['asset_release_id']}"
                artist_name   = a.get("artist_name", "Unknown Artist")
                status_label  = STATUS_LABEL.get(a["upload_status"], str(a["upload_status"]))
                expander_label = f"ID {a['asset_id']} — {a['file_type']} | {status_label} | {artist_name} — {release_title}"

                with st.expander(expander_label):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Artist:** {artist_name}")
                        st.write(f"**File Type:** {a['file_type']}")
                        st.write(f"**Upload Status:** {status_label}")
                    with col2:
                        st.write(f"**Release:** {release_title} (ID {a['asset_release_id']})")
                        st.write(f"**File URL:** {a['file_url']}")

                    # ── Inline edit ──
                    st.write("**Edit this asset:**")
                    edit_col1, edit_col2, edit_col3 = st.columns(3)
                    with edit_col1:
                        new_url = st.text_input("File URL", value=a['file_url'], key=f"url_{a['asset_id']}")
                    with edit_col2:
                        new_type = st.selectbox(
                            "File Type", ["Audio", "Artwork", "Credits"],
                            index=["Audio", "Artwork", "Credits"].index(a['file_type']),
                            key=f"type_{a['asset_id']}"
                        )
                    with edit_col3:
                        new_status = st.selectbox(
                            "Upload Status", ["Pending (0)", "Complete (1)"],
                            index=int(a['upload_status']),
                            key=f"status_{a['asset_id']}"
                        )

                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("Save Changes", key=f"save_{a['asset_id']}"):
                            payload = {
                                "file_url": new_url,
                                "file_type": new_type,
                                "upload_status": 0 if new_status.startswith("Pending") else 1,
                            }
                            r = requests.put(f"{API}/{a['asset_id']}", json=payload)
                            if r.status_code == 200:
                                st.success("Asset updated.")
                                st.rerun()
                            else:
                                st.error(f"Update failed: {r.json().get('error', r.text)}")
                    with btn_col2:
                        if st.button("Delete", key=f"del_{a['asset_id']}", type="secondary"):
                            r = requests.delete(f"{API}/{a['asset_id']}")
                            if r.status_code == 200:
                                st.success("Asset deleted.")
                                st.rerun()
                            else:
                                st.error(f"Delete failed: {r.json().get('error', r.text)}")
    else:
        st.error(f"Failed to load assets: {response.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to API: {e}")
    st.info("Make sure the API server is running on http://web-api:4000")

st.divider()

# ── Upload new asset ──────────────────────────────────────────────────────────

st.subheader("\U0001f4e4 Upload New Asset")

with st.form("add_asset_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_url = st.text_input("File URL", placeholder="https://storage.example.com/track.mp3")
        new_type = st.selectbox("File Type", ["Audio", "Artwork", "Credits"])
    with col2:
        new_release_id = st.number_input("Release ID", min_value=1, step=1, value=1)

    submitted = st.form_submit_button("Upload Asset", type="primary", use_container_width=True)

    if submitted:
        if not new_url:
            st.error("File URL is required.")
        else:
            payload = {"file_url": new_url, "file_type": new_type}
            try:
                r = requests.post(f"{API}/release/{new_release_id}", json=payload)
                if r.status_code == 201:
                    st.success(f"Asset uploaded! Asset ID: {r.json().get('asset_id')}")
                    st.rerun()
                else:
                    st.error(f"Upload failed: {r.json().get('error', r.text)}")
            except requests.exceptions.RequestException as e:
                st.error(f"Could not connect to API: {e}")
