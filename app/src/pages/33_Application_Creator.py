import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout="wide")

SideBarLinks()

with st.form("position_form"):
    st.write("Enter the position ID for this application:")
    position_id = st.number_input("Position ID", min_value=1)

    submit_button = st.form_submit_button("Check")

    if submit_button:
        response = requests.get(f"http://api:4000/pos/positions/{position_id}")
        if response.status_code == 200:
            st.session_state["position"] = response.json()[0]
            st.success("Position Found")

if st.session_state.get("position"):
    position = st.session_state.position
    with st.form("app_editor"):
        st.title(f"Application for {position['summary']}")
        st.write(
            f"Please answer the following questions: {position['applicantQuestions']}"
        )
        question_response = st.text_area("Question Response")
        gpa = st.number_input("GPA")

        s_button = st.form_submit_button("Create Application")

        if s_button:
            with requests.Session() as s:
                try:
                    response = s.post(
                        "http://api:4000/app/applications",
                        json={
                            "userId": st.session_state["id"],
                            "summary": f"Application for {position['summary']}",
                            "questionResponse": question_response,
                            "GPA": gpa,
                        },
                    )
                    response = s.post(
                        f"http://api:4000/app/applications/{response.json()['applicationId']}/add_position",
                        json={"positionId": position_id},
                    )
                    if response.status_code == 201:
                        st.success("Application created successfully")
                except requests.exceptions.RequestException as e:
                    logger.error(f"Error connecting to server: {str(e)}")

    st.write(
        "\* To add work experience, skills, coursework or other imformation, please edit this application after creation."
    )
