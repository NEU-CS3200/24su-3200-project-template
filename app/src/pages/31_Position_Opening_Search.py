import logging

logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
import numpy as np
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

st.title("Position Search")

df_1 = None

with st.form("position_value"):
    position_value = st.text_input(
        "Search Positions",
        placeholder="Enter company name or position id#",
    )

    submit_button = st.form_submit_button("Search")

    if submit_button:
        with requests.Session() as s:
            if not position_value:
                response = s.get("http://api:4000/pos/positions")
                if response.status_code == 200:
                    df_1 = response.json()
            else:
                try:
                    value = int(position_value)
                    response = s.get(f"http://api:4000/pos/positions/{value}")
                    if len(response.json()) != 0:
                        df_1 = response.json()
                except ValueError:
                    response = s.get(
                        f"http://api:4000/pos/positions_company/{str(position_value)}"
                    )
                    if len(response.json()) != 0:
                        df_1 = response.json()

if df_1 is not None:
    for row in df_1:
        with st.expander(f"{row['summary']}"):
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.write(f"Company: {row['compName']}")
            col2.write(f"Position: {row['summary']}")
            col3.write(f"Location: {row['city']}")
            col4.write(f"Salary: {row['expectedSalary']}")
            col5.write(f"ID: {row['id']}")
