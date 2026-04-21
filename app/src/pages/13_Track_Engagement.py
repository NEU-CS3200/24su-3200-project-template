import streamlit as st
import requests
import pandas as pd
import plotly.express as px
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

st.title(f"Track Engagement: {artist_name}")
st.write("Analyze track performance to help design effective concert setlists and marketing campaigns.")

try:
    response = requests.get(f"http://web-api:4000/artists/{artist_id}/tracks/engagement?user_id={user_id}")
    
    if response.status_code == 200:
        data = response.json()
        if data:
            df = pd.DataFrame(data)
            
            # Clean up potential None values and ensure numeric
            df['total_streams'] = pd.to_numeric(df['total_streams']).fillna(0)
            df['number_of_skips'] = pd.to_numeric(df['number_of_skips']).fillna(0)
            
            # Calculate the skip rate safely (avoid dividing by zero)
            df['skip_rate_pct'] = 0.0
            mask = df['total_streams'] > 0
            df.loc[mask, 'skip_rate_pct'] = (df.loc[mask, 'number_of_skips'] / df.loc[mask, 'total_streams']) * 100
            
            # Round for cleaner display
            df['skip_rate_pct'] = df['skip_rate_pct'].round(2)
            
            # Sort by skip rate to easily see worst vs best performers
            df = df.sort_values(by='skip_rate_pct', ascending=False)
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Skip Rates by Track")
                st.caption("Higher percentage means the track is skipped more often.")
                fig_skips = px.bar(
                    df, 
                    x='skip_rate_pct', 
                    y='song_title', 
                    orientation='h',
                    color='skip_rate_pct',
                    color_continuous_scale='Reds'
                )
                fig_skips.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig_skips, use_container_width=True)
                
            with col2:
                st.subheader("Total Streams vs Skips")
                st.caption("Compare absolute stream counts to skip counts.")
                fig_scatter = px.scatter(
                    df,
                    x='total_streams',
                    y='number_of_skips',
                    hover_name='song_title',
                    size='total_streams',
                    color='skip_rate_pct',
                    color_continuous_scale='Reds'
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

            # Raw Data Table
            st.write("### Engagement Data")
            display_df = df[['song_title', 'total_streams', 'number_of_skips', 'skip_rate_pct']]
            display_df.columns = ['Track Title', 'Total Streams', 'Total Skips', 'Skip Rate (%)']
            st.dataframe(display_df, use_container_width=True, hide_index=True)

        else:
            st.info("No track engagement data available for this artist yet.")
    else:
        st.error("Failed to load engagement data.")
except Exception as e:
    st.error(f"API Connection Error: {e}")