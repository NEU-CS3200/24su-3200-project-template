import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks()

API = "http://web-api:4000/artists/leaderboard"

st.title("\U0001f3c6 Artist Leaderboard")
st.write("Top earning artists on the platform ranked by total streaming revenue.")

st.divider()

limit = st.slider("Number of artists to show", min_value=3, max_value=25, value=10, step=1)

try:
    r = requests.get(API, params={"limit": limit})
    if r.status_code == 200:
        artists = r.json()

        if not artists:
            st.info("No artist data found.")
        else:
            # ── Top 3 podium metrics ───────────────────────────────────────
            top = artists[:3]
            cols = st.columns(len(top))
            medals = ["\U0001f947", "\U0001f948", "\U0001f949"]
            for col, artist, medal in zip(cols, top, medals):
                with col:
                    st.metric(
                        label=f"{medal} {artist['stage_name']}",
                        value=f"${artist['total_revenue']:,.2f}",
                        delta=f"{artist['total_streams']:,} streams"
                    )

            st.divider()

            # ── Full leaderboard table ─────────────────────────────────────
            st.subheader("Full Rankings")

            for artist in artists:
                rank = artist["rank"]
                if rank == 1:
                    medal = "\U0001f947"
                elif rank == 2:
                    medal = "\U0001f948"
                elif rank == 3:
                    medal = "\U0001f949"
                else:
                    medal = f"#{rank}"

                with st.expander(
                    f"{medal} {artist['stage_name']} — ${artist['total_revenue']:,.2f} revenue"
                ):
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Total Revenue", f"${artist['total_revenue']:,.2f}")
                    c2.metric("Total Streams", f"{artist['total_streams']:,}")
                    c3.metric("Releases", artist['release_count'])

    else:
        st.error(f"Failed to load leaderboard: {r.status_code}")

except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to API: {e}")
