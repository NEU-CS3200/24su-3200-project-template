import streamlit as st
import requests
import pandas as pd
import pydeck as pdk
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')
SideBarLinks()

# Ensure an artist is selected
if 'selected_artist_id' not in st.session_state:
    st.warning("Please select an artist from the Data Analyst Dashboard first.")
    st.stop()

artist_id = st.session_state['selected_artist_id']
user_id = st.session_state['user_id']
artist_name = st.session_state['selected_artist_name']

st.title(f"Listener Locations: {artist_name}")

try:
    response = requests.get(f"http://web-api:4000/artists/{artist_id}/locations?user_id={user_id}")
    
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)

            # Ensure coordinates are numeric for the map
            df['latitude'] = pd.to_numeric(df['latitude'])
            df['longitude'] = pd.to_numeric(df['longitude'])

            # Scale listener count to a fixed pixel size (5–40px range)
            max_listeners = df['total_listeners'].max()
            df['radius_px'] = (df['total_listeners'] / max_listeners * 35 + 5).astype(int)

            st.write("### Geographic Listener Distribution")
            st.write("The map below shows where this artist's listeners are concentrated. Larger circles indicate a higher number of unique listeners.")

            # Calculate a dynamic center point based on the data
            center_lat = df['latitude'].mean()
            center_lon = df['longitude'].mean()

            # Set up the PyDeck Map Layer
            layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["longitude", "latitude"],
                get_color=[200, 30, 0, 160],
                get_radius="radius_px",
                radius_units="pixels",
                pickable=True,
                auto_highlight=True
            )

            # Define the initial viewport
            view_state = pdk.ViewState(
                latitude=center_lat,
                longitude=center_lon,
                zoom=2,
                pitch=0,
            )

            # Render the map
            st.pydeck_chart(pdk.Deck(
                map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
                layers=[layer],
                initial_view_state=view_state,
                tooltip={"html": "<b>City:</b> {city}, {country} <br/> <b>Listeners:</b> {total_listeners}"}
            ))

            # Display the raw data table
            st.write("### Location Data Breakdown")
            display_df = df[['city', 'country', 'total_listeners']].sort_values(by='total_listeners', ascending=False)
            display_df.columns = ['City', 'Country', 'Total Listeners']
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
        else:
            st.info("No location data available for this artist yet.")
    else:
        st.error("Failed to load location data.")
except Exception as e:
    st.error(f"API Connection Error: {e}")