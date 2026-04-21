import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

PAYOUT_API = "http://web-api:4000/payoutProfiles"
ASSET_API  = "http://web-api:4000/assets"

st.title("\U0001f4c0 Release Overview")
st.write("View all payout profiles and assets for a release in one place.")

st.divider()

release_id = st.number_input("Enter Release ID", min_value=1, step=1, value=1)

if st.button("Load Release", type="primary"):
    st.session_state["overview_release_id"] = release_id

if "overview_release_id" not in st.session_state:
    st.info("Enter a Release ID above and click Load Release.")
    st.stop()

rid = st.session_state["overview_release_id"]

payout_col, asset_col = st.columns(2)

# ── Payout Profiles ───────────────────────────────────────────────────────────

with payout_col:
    st.markdown("### \U0001f4b8 Payout Profiles")
    try:
        r = requests.get(f"{PAYOUT_API}/release/{rid}")
        if r.status_code == 200:
            profiles = r.json()
            if not profiles:
                st.info("No payout profiles for this release.")
            else:
                release_title = profiles[0].get("release_title", f"Release {rid}")
                artist_name   = profiles[0].get("artist_name", "Unknown Artist")
                st.caption(f"**{artist_name}** — {release_title}")

                total_split = sum(float(p["split_percentage"]) for p in profiles)
                st.metric("Total Collaborators", len(profiles))
                remaining = 100 - total_split
                if remaining > 0:
                    delta_str = f"{remaining:.2f}% remaining"
                elif remaining == 0:
                    delta_str = "Fully allocated"
                else:
                    delta_str = f"{abs(remaining):.2f}% over-allocated"
                st.metric("Total Split Allocated", f"{total_split:.2f}%", delta=delta_str)

                for p in profiles:
                    with st.expander(f"{p['collab_email']} — {p['role']} ({p['split_percentage']}%)"):
                        st.write(f"**Payout ID:** {p['payout_id']}")
                        st.write(f"**Email:** {p['collab_email']}")
                        st.write(f"**Role:** {p['role']}")
                        st.write(f"**Split:** {p['split_percentage']}%")
        elif r.status_code == 404:
            st.warning("No payout profiles found for this release.")
        else:
            st.error(f"Error loading payout profiles: {r.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to API: {e}")

# ── Assets ────────────────────────────────────────────────────────────────────

with asset_col:
    st.markdown("### \U0001f4c2 Assets")
    try:
        r = requests.get(f"{ASSET_API}/release/{rid}")
        if r.status_code == 200:
            assets = r.json()
            if not assets:
                st.info("No assets for this release.")
            else:
                STATUS_LABEL = {0: "⏳ Pending", 1: "✅ Complete"}

                release_title = assets[0].get("release_title", f"Release {rid}")
                artist_name   = assets[0].get("artist_name", "Unknown Artist")
                st.caption(f"**{artist_name}** — {release_title}")

                audio_files   = [a for a in assets if a["file_type"] == "Audio"]
                artwork_files = [a for a in assets if a["file_type"] == "Artwork"]
                credits_files = [a for a in assets if a["file_type"] == "Credits"]

                m1, m2, m3 = st.columns(3)
                m1.metric("Audio Files", len(audio_files))
                m2.metric("Artwork Files", len(artwork_files))
                m3.metric("Credits Files", len(credits_files))

                for a in assets:
                    status_label = STATUS_LABEL.get(int(a["upload_status"]), str(a["upload_status"]))
                    with st.expander(f"{a['file_type']} — {status_label} (ID {a['asset_id']})"):
                        st.write(f"**Asset ID:** {a['asset_id']}")
                        st.write(f"**Artist:** {a.get('artist_name', 'Unknown Artist')}")
                        st.write(f"**File Type:** {a['file_type']}")
                        st.write(f"**Status:** {status_label}")
                        st.write(f"**File URL:** {a['file_url']}")
        elif r.status_code == 404:
            st.warning("No assets found for this release.")
        else:
            st.error(f"Error loading assets: {r.status_code}")
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to API: {e}")
