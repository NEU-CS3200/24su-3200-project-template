import logging

logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
import numpy as np
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

st.title("Posted Positions")
df = None

try:
    response = requests.get(
        f"http://api:4000/emp/{st.session_state['company_id']}/positions"
    )
    if response.status_code == 200:
        df = pd.json_normalize(response.json())
        logger.info(df)
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to server: {str(e)}")

if df is not None:
    for index, row in df.iterrows():
        with st.expander(f"{row['compName']} {row['city']}"):
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.write("##### Company:")
            col1.write(f"{row['compName']}")
            col2.write("##### Location:")
            col2.write(f"{row['address']} {row['city']}, {row['country']}")
            col3.write("##### Salary:")
            col3.write(f"{row['expectedSalary']}")
            col4.write("##### Summary:")
            col4.write(f"{row['summary']}")
            col5.write("##### Questions:")
            col5.write(f"{row['applicantQuestions']}")
