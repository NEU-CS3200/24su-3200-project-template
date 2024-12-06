import logging

logger = logging.getLogger(__name__)

import requests
import streamlit as st
from modules.nav import SideBarLinks
import pandas as pd
import io

st.set_page_config(layout="wide")

SideBarLinks()

st.title("Login Times")

data = None

with requests.Session() as session:
    try:
        session.headers.update({"Content-Type": "application/json"})
        response = session.get("http://api:4000/adm/stats")
        if response.status_code == 200:
            data = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to server: {str(e)}")

if data:
    df = pd.DataFrame(data)
    st.dataframe(df)

    csv = df.to_csv(index=False)
    csv_file = io.StringIO(csv)

    st.download_button(
        label="Download CSV",
        data=csv_file.getvalue(),
        file_name="query_results.csv",
        mime="text/csv",
    )
