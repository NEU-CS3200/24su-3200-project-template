import logging

logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
import numpy as np
from modules.nav import SideBarLinks

st.set_page_config(layout="wide")

SideBarLinks()

st.title(f"Create Opening")
try:
    response = requests.get(f"http://api:4000/emp/employees")
    if response.status_code == 200:
        data = response.json()[0]
        with st.form("edit_profile"):
            address = st.text_input("Street Address:")
            city = st.text_input("City:")
            country = st.text_input("Country:")
            summary = st.text_input("Summary:")
            applicant_questions = st.text_input("Applicant Questions:")
            expected_salary = st.number_input(
                "Expected_Salary:",
                min_value=0.00,
                max_value=1000000.00,
                placeholder=0.00,
            )
            company_id = st.session_state["company_id"]

            submit_button = st.form_submit_button("Submit")

            if submit_button:
                req_data = {
                    "address": address,
                    "city": city,
                    "country": country,
                    "summary": summary,
                    "applicantQuestions": applicant_questions,
                    "expectedSalary": expected_salary,
                }
                with requests.Session() as session:
                    try:
                        session.headers.update({"Content-Type": "application/json"})
                        response = session.post(
                            f"http://api:4000/emp/{company_id}/create_position",
                            json=req_data,
                        )
                        if response.status_code == 200:
                            st.success("Position Opening Submitted Successfully")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to server: {str(e)}")
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to server: {str(e)}")
