import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

import requests

st.set_page_config(layout="wide")

SideBarLinks()

if not st.session_state["app_id"]:
    logger.error("No application ID found in session state")

try:
    response = requests.get(
        f"http://api:4000/app/applications/{st.session_state['app_id']}"
    )
    if response.status_code == 200:
        data = response.json()[0]
        st.title(f"{data.get('summary')}")
        with st.form("app_editor"):
            try:
                questions = requests.get(
                    f"http://api:4000/app/applications/{st.session_state['app_id']}/questions"
                )
                if questions.status_code == 200:
                    questions = questions.json()[0]
                st.write(
                    f"Please answer the following questions: {questions['applicantQuestions']}"
                )
                question_response = st.text_area(
                    "Question Response", value=data.get("questionResponse")
                )
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to server: {str(e)}")

            gpa = st.number_input("GPA", value=float(data.get("GPA")))

            submit_button = st.form_submit_button("Save changes")

            if submit_button:
                if not question_response:
                    st.error("Please enter responses to questions")
                elif not gpa:
                    st.error("Please enter your gpa")
                else:
                    data = {
                        "questionResponse": question_response,
                        "GPA": gpa,
                    }
                    with requests.Session() as session:
                        try:
                            session.headers.update({"Content-Type": "application/json"})
                            response = session.put(
                                f"http://api:4000/app/applications/{st.session_state['app_id']}",
                                json=data,
                            )
                            if response.status_code == 200:
                                st.success("Changes saved successfully")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to server: {str(e)}")

        with st.form("add_work_experience"):
            st.write("Previous Work Experience:")
            with requests.Session() as session:
                res = session.get(
                    f"http://api:4000/app/applications/{st.session_state['app_id']}/work_experience"
                )
                if res.status_code == 200:
                    we = res.json()
                    for i, work in enumerate(we):
                        st.write(f"{i+1}. {work['name']}")

            st.write("Add Work Experience:")
            name = st.text_input("Name")
            summary = st.text_area("Summary")

            sbutton = st.form_submit_button("Add Work Experience")

            if sbutton:
                if not name:
                    st.error("Please enter a name")
                elif not summary:
                    st.error("Please enter a summary")
                else:
                    with requests.Session() as session:
                        try:
                            response = session.post(
                                f"http://api:4000/app/applications/{st.session_state['app_id']}/work_experience",
                                json={
                                    "name": name,
                                    "summary": str(summary.rstrip().lstrip()),
                                },
                            )
                            if response.status_code == 201:
                                st.success("Work Experience added successfully")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to server: {str(e)}")

        with st.form("add_relevant_coursework"):
            st.write("Relevant Coursework:")
            with requests.Session() as session:
                res = session.get(
                    f"http://api:4000/app/applications/{st.session_state['app_id']}/related_coursework"
                )
                if res.status_code == 200:
                    we = res.json()
                    for i, work in enumerate(we):
                        st.write(f"{i+1}. {work['name']}")

            st.write("Add Relevant Coursework:")
            name = st.text_input("Name")
            summary = st.text_area("Summary")

            sbutton = st.form_submit_button("Add Relevant Coursework")

            if sbutton:
                if not name:
                    st.error("Please enter a name")
                elif not summary:
                    st.error("Please enter a summary")
                else:
                    with requests.Session() as session:
                        try:
                            response = session.post(
                                f"http://api:4000/app/applications/{st.session_state['app_id']}/related_coursework",
                                json={
                                    "name": name,
                                    "summary": str(summary.rstrip().lstrip()),
                                },
                            )
                            if response.status_code == 201:
                                st.success("Relevant Coursework added successfully")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to server: {str(e)}")

        with st.form("add_notable_skills"):
            st.write("Notable Skills:")
            with requests.Session() as session:
                res = session.get(
                    f"http://api:4000/app/applications/{st.session_state['app_id']}/notable_skills"
                )
                if res.status_code == 200:
                    we = res.json()
                    for i, work in enumerate(we):
                        st.write(f"{i+1}. {work['name']}")

            st.write("Add Notable Skill:")
            name = st.text_input("Name")
            summary = st.text_area("Summary")

            sbutton = st.form_submit_button("Add Notable Skill")

            if sbutton:
                if not name:
                    st.error("Please enter a name")
                elif not summary:
                    st.error("Please enter a summary")
                else:
                    with requests.Session() as session:
                        try:
                            response = session.post(
                                f"http://api:4000/app/applications/{st.session_state['app_id']}/notable_skills",
                                json={
                                    "name": name,
                                    "summary": str(summary.rstrip().lstrip()),
                                },
                            )
                            if response.status_code == 201:
                                st.success("Notable skill added successfully")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to server: {str(e)}")

except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to server: {str(e)}")
