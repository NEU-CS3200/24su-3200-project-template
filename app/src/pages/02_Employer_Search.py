import logging

import requests

logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
import numpy as np
from modules.nav import SideBarLinks


st.set_page_config(layout="wide")

SideBarLinks()

st.title(f"Employer Search")

try:
    test_response = requests.get("http://api:4000/emp/employees")

    if not test_response.status_code == 200:
        st.error("Failed to fetch employees")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to students API: {str(e)}")

with st.form("employer_search"):
    employer_value = st.text_input(
        "Search Employers", placeholder="Enter employer or company name", key="search"
    )

    submit_button = st.form_submit_button("Search")

    df = None

    if submit_button:
        if not employer_value:
            st.error("Please enter an employer name, employer id#, or company name")
        else:
            logger.info(f"Employer form submitted with data: {employer_value}")

            try:
                response1 = requests.get(
                    f"http://api:4000/emp/emp_company/{employer_value}"
                )
                response2 = requests.get(
                    f"http://api:4000/emp/emp_name/{employer_value}"
                )
                response3 = requests.get(
                    f"http://api:4000/emp/{employer_value}/employees"
                )
                if response1.status_code == 200:
                    if len(response1.json()) != 0:
                        df = pd.json_normalize(response1.json())
                if response2.status_code == 200:
                    if len(response2.json()) != 0:
                        df = pd.json_normalize(response2.json())
                if response3.status_code == 200:
                    if len(response3.json()) != 0:
                        df = pd.json_normalize(response3.json())
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

if df is not None:
    for index, row in df.iterrows():
        with st.expander(f"{row['firstName']} {row['lastName']}"):
            col1, col2, col3, col4 = st.columns(4)
            col1.write("##### Name:")
            col1.write(f"{row['name']}")
            col2.write("##### Job:")
            col2.write(f"{row['role']}")
            col3.write("##### Company:")
            col3.write(f"{row['compName']}")
            col4.write("##### Contact:")
            col4.write(f"{row['email']} | {row['mobile']}")
