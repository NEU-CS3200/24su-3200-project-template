import logging
import streamlit as st
import pandas as pd
import numpy as np
import requests
from modules.nav import SideBarLinks
import altair as alt

logger = logging.getLogger(__name__)

st.set_page_config(layout = 'wide')

SideBarLinks()

# ----------- this just gets the sections that a given professor is teaching 
st.title('See Student Submissions')
st.write('')
st.write('**View Student Submissions Below**')
st.write('Enter your email in the form below:')
with st.form("Submission Data "):
  prof_email = st.text_input('Email: ')

  submitted = st.form_submit_button('Submit')

st.write('')
if submitted:
    st.write(f"Your Email: {prof_email}")
    try:
        # Fetch student submissions from the API
        st.write("Here are the current submissions:")
        submissions_data = requests.get(f'http://api:4000/sub/submissions/{prof_email}').json()
        st.dataframe(pd.DataFrame(submissions_data))

    except Exception as e:
        st.write(f"Could not connect to the database to get student submissions. Error: {str(e)}")
    df = pd.DataFrame(submissions_data)

    st.write('')
    # Count the number of submissions per project_id
    submission_counts = df['project_id'].value_counts().reset_index()
    submission_counts.columns = ['project_id', 'submission_count']

    # Bar chart: Project ID vs Number of Submissions
    color_scale = alt.Scale(scheme='pastel1')

    bar_chart = alt.Chart(submission_counts).mark_bar().encode(
    x=alt.X('project_id:O', title='Project ID'),
    y=alt.Y('submission_count:Q', title='Number of Submissions'),
    color=alt.Color('project_id:O', scale=color_scale, legend=None)
    ).properties(
    title='Submission Count by Project')

    # Display the bar chart in Streamlit
    st.altair_chart(bar_chart, use_container_width=True)
